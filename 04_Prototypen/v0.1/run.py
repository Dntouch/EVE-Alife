#!/usr/bin/env python3
"""CLI/Control-Schicht für einen reproduzierbaren EVE-Alife-P0.1-Lauf."""

from __future__ import annotations

import argparse
import json
import subprocess
import uuid
from random import Random
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from eve_core import Config, Simulation, demo_genome, explorer_demo_genome, p1_explorer_genome
from run_stats import update_readme_dashboard, write_summary


def git_commit(project_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=project_root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    canonical_runs = Path(__file__).resolve().parent / "runs"
    parser = argparse.ArgumentParser(description="EVE-Alife Prototyp v0.1")
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--output", type=Path, default=canonical_runs)
    parser.add_argument("--resume", type=Path, help="Checkpoint als Ausgangszustand")
    parser.add_argument("--snapshot-every", type=int, default=10)
    parser.add_argument("--population", type=int, default=2, help="Gerade Größe der technischen Demonstrationspopulation")
    parser.add_argument("--start-energy", type=float, default=100.0, help="Startenergie je Entität in Population 0")
    parser.add_argument("--birth-energy", type=float, default=50.0, help="Energie eines Kindes, vollständig von den Eltern bezahlt")
    parser.add_argument("--birth-energy-fraction", type=float, help="Alternative Geburtsenergie als Anteil der mittleren aktuellen Elternenergie")
    parser.add_argument("--birth-min-heartbeats", type=int, default=0, help="Mindestzahl vollständig finanzierbarer Heartbeats des Kindergenoms")
    parser.add_argument("--novelty-base", type=float, default=10.0, help="Energie für den ersten belohnten Wechsel zu einem RAM-Adress-Wert-Paar")
    parser.add_argument("--ram-world", choices=("random", "islands"), default="random")
    parser.add_argument("--explorers", action="store_true", help="Technische Population mit rückgekoppeltem RAM-Adresszähler")
    parser.add_argument("--p1-explorers", action="store_true", help="Population 1 mit persistentem Suchstand und GATE-Reaktion")
    args = parser.parse_args()

    run_id = str(uuid.uuid4())
    run_dir = args.output / run_id
    snapshots = run_dir / "snapshots"
    snapshots.mkdir(parents=True)
    if args.resume:
        sim = Simulation.from_checkpoint(json.loads(args.resume.read_text(encoding="utf-8")))
        config = sim.config
        population_label = "resumed-checkpoint"
    else:
        if args.population < 2 or args.population % 2:
            parser.error("--population muss eine gerade Zahl >= 2 sein")
        if args.start_energy <= 0 or args.birth_energy <= 0:
            parser.error("--start-energy und --birth-energy müssen positiv sein")
        if args.birth_energy_fraction is not None and not 0 < args.birth_energy_fraction <= 1:
            parser.error("--birth-energy-fraction muss größer 0 und höchstens 1 sein")
        if args.birth_min_heartbeats < 0:
            parser.error("--birth-min-heartbeats darf nicht negativ sein")
        if args.novelty_base < 0:
            parser.error("--novelty-base darf nicht negativ sein")
        if args.explorers and args.p1_explorers:
            parser.error("--explorers und --p1-explorers schließen einander aus")
        config = Config(
            seed=args.seed, birth_energy=args.birth_energy,
            birth_energy_fraction=args.birth_energy_fraction,
            birth_min_heartbeats=args.birth_min_heartbeats,
            novelty_base=args.novelty_base,
        )
        ram = None
        if args.ram_world == "islands":
            ram = [0] * config.ram_size
            world_rng = Random(args.seed ^ 0xE7E)
            for island in range(64):
                start = world_rng.randrange(config.ram_size - 8)
                base = world_rng.randint(-(1 << 15), (1 << 15) - 1)
                for offset in range(8):
                    ram[start + offset] = base + island * 17 + offset
            # Technische Nahbereichsinseln für die Startpunkte der Demonstrationspopulation.
            for entity_id in range(1, args.population + 1):
                start = (entity_id * 313) % config.ram_size
                for offset in range(1, 9):
                    ram[(start + offset) % config.ram_size] = entity_id * 1000 + offset
        sim = Simulation(config, ram=ram)
        for entity_id in range(1, args.population + 1):
            partner_id = entity_id + 1 if entity_id % 2 else entity_id - 1
            if args.p1_explorers:
                genome = p1_explorer_genome(partner_id)
            else:
                factory = explorer_demo_genome if args.explorers else demo_genome
                genome = factory(partner_id, ram_start=(entity_id * 313) % config.ram_size)
            sim.add_entity(genome, energy=args.start_energy)
        population_label = "p1-explorer" if args.p1_explorers else "technical-demonstrator-not-research-result"
    project_root = Path(__file__).resolve().parents[2]
    metadata = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed,
        "eve_version": sim.version,
        "git_commit": git_commit(project_root),
        "configuration": asdict(config),
        "population_0": population_label,
        "population_0_size": len(sim.entities) if not args.resume else None,
        "population_0_start_energy": args.start_energy if not args.resume else None,
        "birth_energy": config.birth_energy,
        "birth_energy_fraction": config.birth_energy_fraction,
        "birth_min_heartbeats": config.birth_min_heartbeats,
        "ram_world": args.ram_world if not args.resume else None,
        "explorer_fixture": args.explorers if not args.resume else None,
        "p1_explorer_population": args.p1_explorers if not args.resume else None,
        "resumed_from": str(args.resume) if args.resume else None,
    }
    write_json(run_dir / "metadata.json", metadata)
    event_cursor = 0
    with (run_dir / "events.jsonl").open("w", encoding="utf-8") as event_file:
        for _ in range(args.ticks):
            sim.heartbeat()
            for event in sim.events[event_cursor:]:
                event_file.write(json.dumps(event, ensure_ascii=False) + "\n")
            event_cursor = len(sim.events)
            snapshot = sim.observation()
            snapshot["run_id"] = run_id
            snapshot["git_commit"] = metadata["git_commit"]
            if sim.tick % args.snapshot_every == 0 or sim.tick == 1:
                write_json(snapshots / f"{sim.tick:08d}.json", snapshot)
            write_json(run_dir / "latest.json", snapshot)
            write_json(run_dir / "checkpoint.json", sim.checkpoint())
    ordered_runs = sorted(
        [
            path for path in args.output.iterdir()
            if path.is_dir() and (path / "metadata.json").exists()
        ],
        key=lambda path: json.loads(
            (path / "metadata.json").read_text(encoding="utf-8")
        ).get("created_at", ""),
    )
    run_number = ordered_runs.index(run_dir) + 1
    write_summary(run_dir, run_number)
    if args.output.resolve() == canonical_runs:
        update_readme_dashboard(project_root / "README.md", canonical_runs)
    print(json.dumps({
        "run_id": run_id, "run_number": run_number, "run_dir": str(run_dir), "tick": sim.tick,
        "living_population": sum(entity.alive for entity in sim.entities.values()),
        "entities_total": len(sim.entities),
    }))


if __name__ == "__main__":
    main()
