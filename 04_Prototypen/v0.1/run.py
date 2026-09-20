#!/usr/bin/env python3
"""CLI/Control-Schicht für einen reproduzierbaren EVE-Alife-P0.1-Lauf."""

from __future__ import annotations

import argparse
import json
import subprocess
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from eve_core import Config, Simulation, demo_genome


def git_commit(project_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=project_root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="EVE-Alife Prototyp v0.1")
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("runs"))
    parser.add_argument("--resume", type=Path, help="Checkpoint als Ausgangszustand")
    parser.add_argument("--snapshot-every", type=int, default=10)
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
        config = Config(seed=args.seed)
        sim = Simulation(config)
        sim.add_entity(demo_genome(2), energy=100.0)
        sim.add_entity(demo_genome(1), energy=100.0)
        population_label = "technical-demonstrator-not-research-result"
    project_root = Path(__file__).resolve().parents[2]
    metadata = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed,
        "eve_version": sim.version,
        "git_commit": git_commit(project_root),
        "configuration": asdict(config),
        "population_0": population_label,
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
    print(json.dumps({
        "run_id": run_id, "run_dir": str(run_dir), "tick": sim.tick,
        "living_population": sum(entity.alive for entity in sim.entities.values()),
        "entities_total": len(sim.entities),
    }))


if __name__ == "__main__":
    main()
