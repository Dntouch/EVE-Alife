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
    deaths: list[dict[str, Any]] = []
    offspring = 0
    energy_gained = 0.0
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
                    births[entity_id] = {
                        "tick": event.get("tick", 0),
                        "name": event.get("entity_name") or amoeba_name(entity_id),
                    }
                    if event.get("parents"):
                        offspring += 1
                elif kind == "death" and isinstance(entity_id, int):
                    born = births.get(entity_id, {"tick": 0, "name": amoeba_name(entity_id)})
                    deaths.append({
                        "entity_id": entity_id,
                        "name": born["name"],
                        "lifespan": max(0, event.get("tick", 0) - born["tick"]),
                    })
                elif kind == "ram_read":
                    energy_gained += float(event.get("reward", 0) or 0)
    entities = latest.get("entities", [])
    alive = sum(bool(entity.get("alive")) for entity in entities)
    total = len(entities) or len(births)
    extinct = total > 0 and alive == 0
    summary = {
        "schema": 1,
        "run_id": metadata.get("run_id", run_dir.name),
        "run_number": run_number,
        "created_at": metadata.get("created_at"),
        "seed": metadata.get("seed", latest.get("config", {}).get("seed")),
        "tick": latest.get("tick", 0),
        "population_total": total,
        "population_alive": alive,
        "offspring": offspring,
        "energy_gained": energy_gained,
        "mass_extinction": extinct,
        "shortest_life": min(deaths, key=lambda item: item["lifespan"], default=None),
        "longest_life": max(deaths, key=lambda item: item["lifespan"], default=None),
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
            or summary.get("schema") != 1
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
    return {
        "runs": len(runs),
        "mass_extinctions": sum(run["mass_extinction"] for run in runs),
        "offspring": sum(run["offspring"] for run in runs),
        "energy_gained": sum(run["energy_gained"] for run in runs),
        "shortest_life": min(lives, key=lambda item: item["lifespan"], default=None),
        "longest_life": max(lives, key=lambda item: item["lifespan"], default=None),
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
    return f"""{README_START}
## Live aus dem Biotop

| Massenaussterben | Nachkommen | Gewonnene Energie | Gespeicherte Läufe |
| ---: | ---: | ---: | ---: |
| **{stats['mass_extinctions']}** | **{stats['offspring']}** | **{_number(stats['energy_gained'])}** | **{stats['runs']}** |

- Kürzestes abgeschlossenes Leben: {life(stats['shortest_life'])}
- Längstes abgeschlossenes Leben: {life(stats['longest_life'])}

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
        filename = f"Lauf_{run['run_number']:03d}_{run['run_id'][:8]}.md"
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
