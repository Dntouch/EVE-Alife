#!/usr/bin/env python3
"""Supervisor für begrenzte und offene EVE-Alife-v0.4-Runs."""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import time
import uuid
from random import Random
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from eve_core import Config, Simulation, demo_genome, explorer_demo_genome, p1_explorer_genome
from run_store import SCHEMA_VERSION, RunStore, atomic_json, export_archive, utc_now


def git_commit(project_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=project_root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def live_observation(sim: Simulation, run_id: str, started_at: datetime) -> dict:
    """Aktuelles Lupe-Bild; absichtlich flüchtig und ohne vollständigen RAM."""
    value = sim.live_observation()
    value.update({
        "run_id": run_id, "status": "running", "end_reason": None,
        "population": sum(entity.alive for entity in sim.entities.values()),
        "started_at": started_at.isoformat(),
        "runtime_seconds": (datetime.now(timezone.utc) - started_at).total_seconds(),
    })
    return value


def main() -> None:
    canonical_runs = Path(__file__).resolve().parent / "runs"
    parser = argparse.ArgumentParser(description="EVE-Alife Prototyp v0.4")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--ticks", type=int, default=2000, help="Tick-Limit (P1-Referenz: 2000)")
    mode.add_argument("--open", action="store_true", help="Ohne künstliches Tick-Limit bis zur Extinktion")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=canonical_runs)
    parser.add_argument("--run-id", help=argparse.SUPPRESS)
    parser.add_argument("--label", default="", help="Optionale Bezeichnung des Runs")
    parser.add_argument("--resume", type=Path, help="Checkpoint als Ausgangszustand")
    parser.add_argument("--sample-every", type=int, default=10, help="Mess- und Lupe-Bild-Intervall")
    parser.add_argument("--checkpoint-every", type=int, default=10_000, help="Recovery-Checkpoint-Intervall; 0 deaktiviert")
    parser.add_argument("--archive", type=Path, help="Abgeschlossenen Run zusätzlich als .eve-run exportieren")
    parser.add_argument("--population", type=int, default=20, help="Gerade Größe der P1-Ausgangspopulation")
    parser.add_argument("--start-energy", type=float, default=500.0, help="Startenergie je Entität")
    parser.add_argument("--birth-energy", type=float, default=50.0, help="Energie eines Kindes, vollständig von den Eltern bezahlt")
    parser.add_argument("--birth-energy-fraction", type=float, default=0.5, help="Geburtsenergie als Anteil der mittleren aktuellen Elternenergie")
    parser.add_argument("--birth-min-heartbeats", type=int, default=5, help="Mindestzahl vollständig finanzierbarer Heartbeats des Kindergenoms")
    parser.add_argument("--novelty-base", type=float, default=60.0, help="P1-Tarif für den ersten belohnten RAM-Wechsel")
    parser.add_argument("--aging-cost-rate", type=float, default=0.01, help="Zusätzliche Standby-Kosten je bereits gelebtem Heartbeat")
    parser.add_argument("--genome-node-cost", type=float, default=0.05, help="Faktor der unterlinear wachsenden Funktionspunktkosten")
    parser.add_argument("--genome-edge-cost", type=float, default=0.01, help="Faktor der unterlinear wachsenden Kantenkosten")
    parser.add_argument("--entity-discovery-base", type=float, default=10.0, help="Energie für den neuen Fund einer lebenden fremden Amöbe")
    parser.add_argument("--invitation-discovery-base", type=float, default=20.0, help="Energie für eine neu erkannte Einladung im fremden Partnerslot")
    parser.add_argument("--life-state-discovery-base", type=float, default=10.0, help="Energie für einen neu erkannten Lebenszustand einer fremden Amöbe")
    parser.add_argument(
        "--ram-world", choices=("random", "islands", "bare", "toys"), default="random",
        help="RAM-Suppe: absoluter Zahlenbrei, statische Inseln, räumliche Welt ohne Spielzeuge oder Spielzeugkasten",
    )
    parser.add_argument("--population-model", choices=("p1", "demo", "technical-explorer"), default="p1")
    parser.add_argument("--explorers", action="store_true", help="Technische Population mit rückgekoppeltem RAM-Adresszähler")
    parser.add_argument("--p1-explorers", action="store_true", help="Population 1 mit persistentem Suchstand und GATE-Reaktion")
    parser.add_argument("--uniform-p1", action="store_true", help="Kontrolllauf mit identischen P1-Gründergenomen wie Lauf 41")
    args = parser.parse_args()

    population_model = args.population_model
    if args.explorers:
        population_model = "technical-explorer"
    if args.p1_explorers:
        population_model = "p1"

    if args.ticks is not None and args.ticks < 1:
        parser.error("--ticks muss mindestens 1 sein")
    if args.sample_every < 1 or args.checkpoint_every < 0:
        parser.error("--sample-every muss positiv und --checkpoint-every darf nicht negativ sein")
    tick_limit = None if args.open else args.ticks

    try:
        run_id = str(uuid.UUID(args.run_id)) if args.run_id else str(uuid.uuid4())
    except ValueError:
        parser.error("--run-id muss eine gültige UUID sein")
    run_dir = args.output / run_id
    if run_dir.exists():
        parser.error(f"Run existiert bereits: {run_id}")
    (run_dir / "checkpoints").mkdir(parents=True)
    if args.resume:
        sim = Simulation.from_checkpoint(json.loads(args.resume.read_text(encoding="utf-8")))
        config = sim.config
        population_label = "resumed-checkpoint"
        if tick_limit is not None:
            tick_limit += sim.tick
    else:
        if args.population < 2 or args.population % 2:
            parser.error("--population muss eine gerade Zahl >= 2 sein")
        if args.start_energy <= 0 or args.birth_energy <= 0:
            parser.error("--start-energy und --birth-energy müssen positiv sein")
        if args.birth_energy_fraction is not None and not 0 < args.birth_energy_fraction <= 1:
            parser.error("--birth-energy-fraction muss größer 0 und höchstens 1 sein")
        if args.birth_min_heartbeats < 0:
            parser.error("--birth-min-heartbeats darf nicht negativ sein")
        if min(args.novelty_base, args.entity_discovery_base, args.invitation_discovery_base, args.life_state_discovery_base) < 0:
            parser.error("Energieerträge dürfen nicht negativ sein")
        if min(args.aging_cost_rate, args.genome_node_cost, args.genome_edge_cost) < 0:
            parser.error("Lebenshaltungskosten dürfen nicht negativ sein")
        if args.explorers and args.p1_explorers:
            parser.error("--explorers und --p1-explorers schließen einander aus")
        config = Config(
            seed=args.seed, birth_energy=args.birth_energy,
            birth_energy_fraction=args.birth_energy_fraction,
            birth_min_heartbeats=args.birth_min_heartbeats,
            novelty_base=args.novelty_base,
            aging_cost_rate=args.aging_cost_rate,
            genome_node_cost=args.genome_node_cost,
            genome_edge_cost=args.genome_edge_cost,
            entity_discovery_base=args.entity_discovery_base,
            invitation_discovery_base=args.invitation_discovery_base,
            life_state_discovery_base=args.life_state_discovery_base,
            toy_habitats=128 if args.ram_world == "toys" else 0,
            local_ram_coordinates=args.ram_world in {"bare", "toys"},
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
        founder_variants = []
        founder_rng = Random(args.seed ^ 0xA11FE)
        position_rng = Random(args.seed ^ 0xB1070F)
        for entity_id in range(1, args.population + 1):
            partner_id = entity_id + 1 if entity_id % 2 else entity_id - 1
            if population_model == "p1":
                if args.uniform_p1:
                    variant = {"search_offset": -1, "search_step": 1, "search_patience": 64, "activity_base": 100, "knock_capacity": 2, "bond_ticks": 5}
                else:
                    variant = {
                        "search_offset": founder_rng.randint(-5, 5),
                        "search_step": founder_rng.choice((-4, -3, -2, -1, 1, 2, 3, 4)),
                        "search_patience": founder_rng.randint(32, 96),
                        "activity_base": founder_rng.randint(96, 104),
                        "knock_capacity": founder_rng.randint(1, 4),
                        "bond_ticks": founder_rng.randint(3, 12),
                    }
                genome = p1_explorer_genome(partner_id, **variant)
                founder_variants.append({"entity_id": entity_id, **variant})
            else:
                factory = explorer_demo_genome if population_model == "technical-explorer" else demo_genome
                genome = factory(partner_id, ram_start=(entity_id * 313) % config.ram_size)
            ram_position = position_rng.randrange(config.ram_size) if config.local_ram_coordinates else 0
            sim.add_entity(genome, energy=args.start_energy, ram_position=ram_position)
        population_label = "p1-explorer" if population_model == "p1" else "technical-demonstrator-not-research-result"
    project_root = Path(__file__).resolve().parents[2]
    created_at = utc_now()
    metadata = {
        "run_id": run_id,
        "label": args.label.strip(),
        "format_version": SCHEMA_VERSION,
        "prototype_version": "0.4",
        "created_at": created_at,
        "mode": "open" if args.open else "limited",
        "tick_limit": tick_limit,
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
        "explorer_fixture": population_model == "technical-explorer" if not args.resume else None,
        "p1_explorer_population": population_model == "p1" if not args.resume else None,
        "p1_founder_variants": founder_variants if not args.resume and population_model == "p1" else None,
        "resumed_from": str(args.resume) if args.resume else None,
        "resumed_from_run": args.resume.parent.parent.name if args.resume else None,
    }
    started_at = datetime.fromisoformat(created_at)
    stop_requested = False

    def request_stop(_signum: int, _frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True

    # SIGINT/SIGTERM erzeugen keinen fachlichen Endgrund. Der Run bleibt als
    # "running" wiederaufnehmbar; ein Checkpoint wird bestmöglich geschrieben.
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    end_reason = None
    with RunStore(run_dir, create=True) as store:
        store.initialize(metadata)
        store.sync_entities(sim)
        store.append_events(sim.events)
        sim.events.clear()
        store.sample(sim)
        store.observe(sim, run_id)
        store.update_running(sim)
        last_live_write = 0.0
        while True:
            if not any(entity.alive for entity in sim.entities.values()):
                end_reason = "natural_extinction"
                break
            if tick_limit is not None and sim.tick >= tick_limit:
                end_reason = "tick_limit_reached"
                break
            if stop_requested:
                end_reason = "user_requested"
                break
            sim.heartbeat()
            tick_events = sim.events
            birth_ids = [
                int(event["entity_id"]) for event in tick_events
                if event["kind"] == "birth"
            ]
            if birth_ids:
                store.sync_entities(sim, birth_ids)
            store.append_events(tick_events)
            sim.events = []
            if sim.tick == 1 or sim.tick % args.sample_every == 0:
                store.sample(sim)
                store.observe(sim, run_id)
                store.flush(sim)
            if args.checkpoint_every and sim.tick % args.checkpoint_every == 0:
                checkpoint = run_dir / "checkpoints" / f"{sim.tick:012d}.json"
                atomic_json(checkpoint, sim.checkpoint())
                store.record_checkpoint(checkpoint, sim.tick)
            now = time.monotonic()
            if sim.tick == 1 or now - last_live_write >= 0.5:
                atomic_json(run_dir / "live.json", live_observation(sim, run_id, started_at))
                last_live_write = now
        store.sample(sim)
        store.observe(sim, run_id)
        if end_reason:
            if end_reason == "user_requested":
                checkpoint = run_dir / "checkpoints" / f"{sim.tick:012d}.json"
                atomic_json(checkpoint, sim.checkpoint())
                store.record_checkpoint(checkpoint, sim.tick)
            store.finish(sim, end_reason)
            final_live = live_observation(sim, run_id, started_at)
            final_live.update({"status": "extinct" if end_reason == "natural_extinction" else ("stopped" if end_reason == "user_requested" else "completed"), "end_reason": end_reason})
            atomic_json(run_dir / "live.json", final_live)
        else:
            checkpoint = run_dir / "checkpoints" / f"{sim.tick:012d}.json"
            atomic_json(checkpoint, sim.checkpoint())
            store.record_checkpoint(checkpoint, sim.tick)
    if args.archive and end_reason:
        export_archive(run_dir, args.archive)
    print(json.dumps({
        "run_id": run_id, "run_dir": str(run_dir), "tick": sim.tick,
        "living_population": sum(entity.alive for entity in sim.entities.values()),
        "entities_total": len(sim.entities), "status": "running" if not end_reason else ("extinct" if end_reason == "natural_extinction" else "completed"),
        "end_reason": end_reason,
    }))


if __name__ == "__main__":
    main()
