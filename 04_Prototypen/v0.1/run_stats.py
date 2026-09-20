"""Laufuebergreifende, rein beobachtende Statistik fuer EVE-Alife."""
from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import Any

from eve_core import amoeba_name


def _read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def summarize_run(run_dir: Path, run_number: int) -> dict[str, Any]:
    """Erzeugt eine kompakte Bilanz aus einem (auch aelteren) Lauf."""
    metadata = _read_json(run_dir / "metadata.json", {})
    latest = _read_json(run_dir / "latest.json", {})
    births: dict[int, dict[str, Any]] = {
        entity["id"]: {
            "tick": entity.get("born_at", 0),
            "name": entity.get("name") or amoeba_name(entity["id"]),
        }
        for entity in latest.get("entities", [])
        if isinstance(entity.get("id"), int)
    }
    entities = latest.get("entities", [])
    entity_by_id = {entity["id"]: entity for entity in entities}
    deaths: list[dict[str, Any]] = []
    offspring = 0
    energy_gained = 0.0
    direct_children: dict[int, int] = {}
    generation_depth: dict[int, int] = {}
    highest_energy: dict[int, float] = {
        entity["id"]: float(entity.get("energy", 0)) for entity in entities
    }
    ram_addresses: dict[int, set[int]] = {}
    personal_ram_energy: dict[int, float] = {}
    producer_energy: dict[int, float] = {}
    discoveries_by_entity: dict[int, int] = {}
    invitations_by_entity: dict[int, int] = {}
    writes_by_entity: dict[int, int] = {}
    parent_links: dict[int, tuple[int, ...]] = {}
    entity_discoveries = 0
    invitation_discoveries = 0
    ram_writes = 0

    def note_energy(entity_id: int, *values: Any) -> None:
        numeric = [float(value) for value in values if isinstance(value, (int, float))]
        if numeric:
            highest_energy[entity_id] = max(highest_energy.get(entity_id, float("-inf")), *numeric)

    event_path = run_dir / "events.jsonl"
    if event_path.exists():
        with event_path.open(encoding="utf-8") as lines:
            for line in lines:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                kind = event.get("kind")
                entity_id = event.get("entity_id")
                if kind == "birth" and isinstance(entity_id, int):
                    parents = [parent for parent in event.get("parents", []) if isinstance(parent, int)]
                    births[entity_id] = {
                        "tick": event.get("tick", 0),
                        "name": event.get("entity_name") or amoeba_name(entity_id),
                    }
                    note_energy(entity_id, event.get("energy"))
                    generation_depth[entity_id] = 0 if not parents else 1 + max(
                        (generation_depth.get(parent, 0) for parent in parents), default=0
                    )
                    if parents:
                        parent_links[entity_id] = tuple(parents)
                        offspring += 1
                        for parent in parents:
                            direct_children[parent] = direct_children.get(parent, 0) + 1
                elif kind == "death" and isinstance(entity_id, int):
                    born = births.get(entity_id, {"tick": 0, "name": amoeba_name(entity_id)})
                    deaths.append({
                        "entity_id": entity_id,
                        "name": born["name"],
                        "lifespan": max(0, event.get("tick", 0) - born["tick"]),
                    })
                elif isinstance(entity_id, int) and kind in {"standby", "node_fire", "reproduction_cost"}:
                    note_energy(entity_id, event.get("energy_before"), event.get("energy_after"))
                elif kind == "ram_read" and isinstance(entity_id, int):
                    reward = float(event.get("reward", 0) or 0)
                    energy_gained += reward
                    if not event.get("virtual"):
                        personal_ram_energy[entity_id] = personal_ram_energy.get(entity_id, 0.0) + reward
                    if not event.get("virtual") and isinstance(event.get("address"), int):
                        ram_addresses.setdefault(entity_id, set()).add(event["address"])
                    originators = [item for item in event.get("originators", []) if isinstance(item, int)]
                    if reward > 0 and originators:
                        share = reward / len(originators)
                        for originator in originators:
                            producer_energy[originator] = producer_energy.get(originator, 0.0) + share
                    if event.get("discovery_type") == "entity":
                        entity_discoveries += 1
                        discoveries_by_entity[entity_id] = discoveries_by_entity.get(entity_id, 0) + 1
                    elif event.get("discovery_type") == "invitation":
                        invitation_discoveries += 1
                        invitations_by_entity[entity_id] = invitations_by_entity.get(entity_id, 0) + 1
                elif kind == "ram_write" and isinstance(entity_id, int):
                    ram_writes += 1
                    writes_by_entity[entity_id] = writes_by_entity.get(entity_id, 0) + 1

    # Sehr alte Ereignisstroeme enthalten eventuell keine Geburtsereignisse fuer
    # fortgesetzte Entitaeten. Die Checkpoint-Abstammung schliesst diese Luecke.
    for entity in sorted(entities, key=lambda item: item["id"]):
        parents = [parent for parent in entity.get("parents", []) if isinstance(parent, int)]
        if parents:
            parent_links.setdefault(entity["id"], tuple(parents))
        generation_depth.setdefault(
            entity["id"], 0 if not parents else 1 + max(
                (generation_depth.get(parent, 0) for parent in parents), default=0
            ),
        )

    alive = sum(bool(entity.get("alive")) for entity in entities)
    total = len(entities) or len(births)
    extinct = total > 0 and alive == 0
    def entity_record(entity_id: int, value: float | int, **extra: Any) -> dict[str, Any]:
        return {
            "entity_id": entity_id,
            "name": births.get(entity_id, {}).get("name", amoeba_name(entity_id)),
            "value": value,
            **extra,
        }

    def maximum(values: dict[int, Any], **extra_by_id: dict[int, Any]) -> dict[str, Any] | None:
        if not values:
            return None
        entity_id = max(values, key=lambda item: values[item])
        return entity_record(
            entity_id, values[entity_id],
            **{key: mapping.get(entity_id) for key, mapping in extra_by_id.items()},
        )

    genome_sizes = {entity["id"]: entity.get("n_g", 0) for entity in entities}
    genome_f = {entity["id"]: entity.get("n_f", 0) for entity in entities}
    genome_p = {entity["id"]: entity.get("n_p", 0) for entity in entities}
    ages = {
        entity["id"]: max(0, latest.get("tick", 0) - entity.get("born_at", 0))
        if entity.get("alive") else next(
            (death["lifespan"] for death in deaths if death["entity_id"] == entity["id"]), 0
        )
        for entity in entities
    }
    alive_flags = {entity["id"]: bool(entity.get("alive")) for entity in entities}
    direct_descendants: dict[int, set[int]] = {}
    for child, parents in parent_links.items():
        for parent in parents:
            direct_descendants.setdefault(parent, set()).add(child)
    descendant_cache: dict[int, set[int]] = {}

    def descendants(entity_id: int) -> set[int]:
        if entity_id not in descendant_cache:
            result = set(direct_descendants.get(entity_id, ()))
            for child in tuple(result):
                result.update(descendants(child))
            descendant_cache[entity_id] = result
        return descendant_cache[entity_id]

    descendant_counts = {
        entity_id: len(descendants(entity_id))
        for entity_id in set(births) | set(direct_descendants)
        if descendants(entity_id)
    }
    summary = {
        "schema": 4,
        "run_id": metadata.get("run_id", run_dir.name),
        "run_number": run_number,
        "created_at": metadata.get("created_at"),
        "seed": metadata.get("seed", latest.get("config", {}).get("seed")),
        "tick": latest.get("tick", 0),
        "population_total": total,
        "population_alive": alive,
        "offspring": offspring,
        "energy_gained": energy_gained,
        "entity_discoveries": entity_discoveries,
        "invitation_discoveries": invitation_discoveries,
        "ram_writes": ram_writes,
        "mass_extinction": extinct,
        "shortest_life": min(deaths, key=lambda item: item["lifespan"], default=None),
        "longest_life": max(deaths, key=lambda item: item["lifespan"], default=None),
        "records": {
            "largest_genome": maximum(genome_sizes, n_f=genome_f, n_p=genome_p),
            "highest_energy": maximum(highest_energy),
            "most_direct_children": maximum(direct_children),
            "most_descendants": maximum(descendant_counts),
            "deepest_generation": maximum(generation_depth),
            "oldest_entity": maximum(ages, alive=alive_flags),
            "most_ram_addresses": maximum({key: len(value) for key, value in ram_addresses.items()}),
            "most_ram_energy": maximum(personal_ram_energy),
            "best_information_producer": maximum(producer_energy),
            "most_entity_discoveries": maximum(discoveries_by_entity),
            "most_invitations": maximum(invitations_by_entity),
            "most_ram_writes": maximum(writes_by_entity),
        },
    }
    return summary


def write_summary(run_dir: Path, run_number: int) -> dict[str, Any]:
    summary = summarize_run(run_dir, run_number)
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def dashboard_data(runs_root: Path) -> dict[str, Any]:
    candidates = []
    for run_dir in runs_root.iterdir() if runs_root.exists() else ():
        if not run_dir.is_dir():
            continue
        metadata = _read_json(run_dir / "metadata.json", {})
        if metadata:
            candidates.append((metadata.get("created_at", ""), run_dir.name, run_dir))
    candidates.sort()
    runs = []
    for number, (_, _, run_dir) in enumerate(candidates, 1):
        summary_path = run_dir / "summary.json"
        summary = _read_json(summary_path)
        event_path = run_dir / "events.jsonl"
        # Alte oder weitergelaufene Runs werden automatisch neu bilanziert.
        if (
            not summary
            or summary.get("schema") != 4
            or summary.get("run_number") != number
            or (event_path.exists() and event_path.stat().st_mtime > summary_path.stat().st_mtime)
        ):
            summary = write_summary(run_dir, number)
        runs.append(summary)

    lives = [
        {**life, "run_number": run["run_number"], "run_id": run["run_id"]}
        for run in runs for life in (run.get("shortest_life"), run.get("longest_life"))
        if life is not None
    ]
    record_keys = (
        "largest_genome", "highest_energy", "most_direct_children", "most_descendants", "deepest_generation",
        "oldest_entity", "most_ram_addresses", "most_ram_energy", "best_information_producer",
        "most_entity_discoveries", "most_invitations", "most_ram_writes",
    )
    records = {}
    for key in record_keys:
        candidates = [
            {**record, "run_number": run["run_number"], "run_id": run["run_id"]}
            for run in runs if (record := run.get("records", {}).get(key)) is not None
        ]
        records[key] = max(candidates, key=lambda item: item["value"], default=None)
    return {
        "runs": len(runs),
        "mass_extinctions": sum(run["mass_extinction"] for run in runs),
        "offspring": sum(run["offspring"] for run in runs),
        "energy_gained": sum(run["energy_gained"] for run in runs),
        "shortest_life": min(lives, key=lambda item: item["lifespan"], default=None),
        "longest_life": max(lives, key=lambda item: item["lifespan"], default=None),
        "records": records,
        "history": list(reversed(runs)),
    }


README_START = "<!-- EVE_STATS_START -->"
README_END = "<!-- EVE_STATS_END -->"


def _number(value: float) -> str:
    rendered = f"{value:,.2f}"
    return rendered.replace(",", "X").replace(".", ",").replace("X", ".")


def render_readme_dashboard(stats: dict[str, Any]) -> str:
    def life(record: dict[str, Any] | None) -> str:
        if not record:
            return "—"
        return (
            f"**{record['name']}** (Amöbe #{record['entity_id']}), "
            f"{record['lifespan']} Ticks in Lauf {record['run_number']}"
        )

    rows = []
    for run in stats["history"][:5]:
        status = "ausgestorben" if run["mass_extinction"] else f"{run['population_alive']} lebend"
        rows.append(
            f"| {run['run_number']} | {run['tick']} | {status} | "
            f"{run['offspring']} | {_number(run['energy_gained'])} |"
        )
    table = "\n".join(rows) if rows else "| — | — | noch keine Läufe | — | — |"
    record_labels = (
        ("largest_genome", "Größtes Genom", " G"),
        ("highest_energy", "Höchste Energie", ""),
        ("most_direct_children", "Meiste direkte Kinder", ""),
        ("most_descendants", "Größte Nachkommenschaft", ""),
        ("deepest_generation", "Tiefste Generation", ""),
        ("oldest_entity", "Älteste Amöbe", " Ticks"),
        ("most_ram_addresses", "Meiste RAM-Adressen", ""),
        ("most_ram_energy", "Meiste RAM-Energie", ""),
        ("best_information_producer", "Bester Informationsproduzent", ""),
        ("most_entity_discoveries", "Meiste Amöbenfunde", ""),
        ("most_invitations", "Meiste erkannte Einladungen", ""),
        ("most_ram_writes", "Meiste RAM-Schreibvorgänge", ""),
    )
    record_rows = []
    for key, label, suffix in record_labels:
        record = stats.get("records", {}).get(key)
        if record:
            value = _number(record["value"]) if isinstance(record["value"], float) else record["value"]
            record_rows.append(
                f"| {label} | **{record['name']}** (#{record['entity_id']}) | "
                f"{value}{suffix} | {record['run_number']} |"
            )
        else:
            record_rows.append(f"| {label} | — | noch nicht beobachtet | — |")
    return f"""{README_START}
## Live aus dem Biotop

| Massenaussterben | Nachkommen | Gewonnene Energie | Gespeicherte Läufe |
| ---: | ---: | ---: | ---: |
| **{stats['mass_extinctions']}** | **{stats['offspring']}** | **{_number(stats['energy_gained'])}** | **{stats['runs']}** |

- Kürzestes abgeschlossenes Leben: {life(stats['shortest_life'])}
- Längstes abgeschlossenes Leben: {life(stats['longest_life'])}

| Rekord | Amöbe | Wert | Lauf |
| :--- | :--- | ---: | ---: |
{chr(10).join(record_rows)}

| Lauf | Ticks | Status | Nachkommen | Energiegewinn |
| ---: | ---: | :--- | ---: | ---: |
{table}

_Automatisch aus den lokal gespeicherten Runs erzeugt. Der veröffentlichte Stand entspricht dem letzten Git-Push. [Definitionen und Dashboard](04_Prototypen/v0.1/README.md)_
{README_END}"""


def update_readme_dashboard(readme: Path, runs_root: Path) -> dict[str, Any]:
    stats = dashboard_data(runs_root)
    block = render_readme_dashboard(stats)
    content = readme.read_text(encoding="utf-8")
    if README_START in content and README_END in content:
        before, remainder = content.split(README_START, 1)
        _, after = remainder.split(README_END, 1)
        content = before.rstrip() + "\n\n" + block + "\n\n" + after.lstrip("\n")
    else:
        anchor = "\n## Bereiche"
        if anchor not in content:
            raise ValueError("README-Anker '## Bereiche' fehlt")
        before, after = content.split(anchor, 1)
        content = before.rstrip() + "\n\n" + block + "\n\n## Bereiche" + after
    readme.write_text(content.rstrip() + "\n", encoding="utf-8")
    return stats


def _markdown_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "ja" if value else "nein"
    return str(value).replace("|", "\\|")


def publish_run_reports(runs_root: Path, results_root: Path) -> list[Path]:
    """Schreibt kleine, versionierbare Berichte; Rohdaten bleiben lokal."""
    stats = dashboard_data(runs_root)
    results_root.mkdir(parents=True, exist_ok=True)
    written = []
    index_rows = []
    for run in reversed(stats["history"]):
        run_dir = runs_root / run["run_id"]
        metadata = _read_json(run_dir / "metadata.json", {})
        filename = f"Lauf_{run['run_number']:03d}.md"
        path = results_root / filename
        status = "Massenaussterben" if run["mass_extinction"] else f"{run['population_alive']} lebend"
        config = metadata.get("configuration", {})
        config_rows = "\n".join(
            f"| `{key}` | {_markdown_value(value)} |" for key, value in sorted(config.items())
        ) or "| — | — |"
        shortest = run.get("shortest_life")
        longest = run.get("longest_life")
        report = f"""# Lauf {run['run_number']}

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `{run['run_id']}` |
| Erzeugt | {_markdown_value(run.get('created_at'))} |
| Seed | {_markdown_value(run.get('seed'))} |
| Git-Commit | `{metadata.get('git_commit', 'unbekannt')}` |
| EVE-Version | {_markdown_value(metadata.get('eve_version'))} |

## Ergebnis

| Ticks | Entitäten gesamt | Am Ende lebend | Nachkommen | Gewonnene Energie | Status |
| ---: | ---: | ---: | ---: | ---: | :--- |
| {run['tick']} | {run['population_total']} | {run['population_alive']} | {run['offspring']} | {_number(run['energy_gained'])} | {status} |

- Kürzestes abgeschlossenes Leben: {shortest['name'] + ', ' + str(shortest['lifespan']) + ' Ticks' if shortest else '—'}
- Längstes abgeschlossenes Leben: {longest['name'] + ', ' + str(longest['lifespan']) + ' Ticks' if longest else '—'}
- Neue fremde Amöben gefunden: {run.get('entity_discoveries', 0)}
- Einladungen an die eigene ID erkannt: {run.get('invitation_discoveries', 0)}
- RAM-Schreibvorgänge: {run.get('ram_writes', 0)}

## Konfiguration

| Parameter | Wert |
| :--- | :--- |
{config_rows}

_Automatisch aus den lokalen Beobachtungsdaten erzeugter, versionierbarer Laufbericht. Ereignisstrom, Snapshots, RAM und Checkpoint bleiben wegen ihrer Größe lokal._
"""
        path.write_text(report, encoding="utf-8")
        written.append(path)
        index_rows.append(
            f"| [{run['run_number']}]({filename}) | {run['tick']} | {status} | "
            f"{run['offspring']} | {_number(run['energy_gained'])} |"
        )
    index = f"""# EVE-Alife – Laufergebnisse

Dieser Bereich enthält die kompakten, versionierten Berichte der tatsächlich ausgeführten Prototyp-Läufe. Jeder Bericht hält Identität, Git-Stand, Konfiguration, Populationsresultat, Energiegewinn und Lebensrekorde fest.

Die vollständigen Rohdaten bleiben lokal unter `04_Prototypen/v0.1/runs/`: Ein einzelner Lauf kann hunderte Megabyte an Snapshots, RAM-Zuständen, Checkpoints und Ereignissen enthalten. Sie werden deshalb nicht ungeprüft in Git aufgenommen. Die Berichte hier sind aus diesen Rohdaten reproduzierbar.

Zusammenhängende Versuchsreihen werden zusätzlich ausgewertet:

- [Tarifrunde 40–90: IG Amöbe gegen Lebenshaltungskosten](Tarifrunde_040_bis_090.md)
- [Langzeitlauf mit Tarif 60](Langzeitlauf_Tarif_060.md)
- [Dynamische Partnersuche und Alterskosten](Partnersuche_und_Alterung.md)
- [Membransuche, Einladung und RAM-Schreiben](Membransuche_und_RAM_Schreiben.md)

## Übersicht

| Lauf | Ticks | Status | Nachkommen | Energiegewinn |
| ---: | ---: | :--- | ---: | ---: |
{chr(10).join(reversed(index_rows))}

## Aktualisieren

```bash
python3 04_Prototypen/v0.1/run_stats.py
```

Ein regulärer neuer Lauf aktualisiert seinen Bericht und diese Übersicht automatisch. Veröffentlicht wird der neue Stand mit dem nächsten Git-Commit und Push.
"""
    index_path = results_root / "README.md"
    index_path.write_text(index, encoding="utf-8")
    return [index_path, *written]


def main() -> None:
    parser = argparse.ArgumentParser(description="EVE-Statistik fuer die Git-Startseite aktualisieren")
    parser.add_argument("--runs", type=Path, default=Path(__file__).resolve().parent / "runs")
    parser.add_argument("--readme", type=Path, default=Path(__file__).resolve().parents[2] / "README.md")
    parser.add_argument("--results", type=Path, default=Path(__file__).resolve().parents[2] / "07_Laufergebnisse")
    args = parser.parse_args()
    stats = update_readme_dashboard(args.readme, args.runs)
    publish_run_reports(args.runs, args.results)
    print(json.dumps({key: value for key, value in stats.items() if key != "history"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
