#!/usr/bin/env python3
"""Reproducible CPU and observation benchmark for EVE v0.4.

This benchmark never writes to canonical runs.  It separates simulation-core
cost from the former full live serialization so performance work does not alter
the scientific heartbeat semantics.
"""

from __future__ import annotations

import argparse
import cProfile
import hashlib
import io
import json
import pstats
import time

from eve_core import Config, Simulation, demo_genome
from run_store import RunStore, canonical_json


def build_simulation(population: int, seed: int) -> Simulation:
    simulation = Simulation(Config(seed=seed, mutation_probability=0.0))
    for entity_id in range(1, population + 1):
        partner = entity_id + 1 if entity_id % 2 else entity_id - 1
        simulation.add_entity(demo_genome(partner), energy=10_000.0)
    simulation.events.clear()
    return simulation


def measure(callable_, repeats: int = 1) -> tuple[float, object]:
    started = time.perf_counter()
    value = None
    for _ in range(repeats):
        value = callable_()
    return time.perf_counter() - started, value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--population", type=int, default=200)
    parser.add_argument("--ticks", type=int, default=25)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    simulation = build_simulation(args.population, args.seed)
    full_seconds, full_json = measure(
        lambda: json.dumps(simulation.observation(), separators=(",", ":")), 3,
    )
    live_seconds, live_json = measure(
        lambda: json.dumps(simulation.live_observation(), separators=(",", ":")), 3,
    )

    def legacy_genome_scan() -> None:
        for entity in simulation.entities.values():
            encoded = canonical_json(RunStore._genome_data(entity.genome))
            hashlib.sha256(encoded.encode()).hexdigest()

    genome_scan_seconds, _ = measure(legacy_genome_scan, 10)

    profiler = cProfile.Profile()
    profiler.enable()
    started = time.perf_counter()
    for _ in range(args.ticks):
        simulation.heartbeat()
        simulation.events.clear()
    core_seconds = time.perf_counter() - started
    profiler.disable()
    report = io.StringIO()
    pstats.Stats(profiler, stream=report).strip_dirs().sort_stats("cumulative").print_stats(15)

    result = {
        "population_initial": args.population,
        "population_final": sum(entity.alive for entity in simulation.entities.values()),
        "ticks": args.ticks,
        "core_seconds": round(core_seconds, 6),
        "core_ticks_per_second": round(args.ticks / core_seconds, 3),
        "legacy_live_bytes": len(full_json),
        "compact_live_bytes": len(live_json),
        "live_size_reduction_factor": round(len(full_json) / max(1, len(live_json)), 2),
        "legacy_live_build_seconds_3x": round(full_seconds, 6),
        "compact_live_build_seconds_3x": round(live_seconds, 6),
        "live_build_speedup": round(full_seconds / max(1e-12, live_seconds), 2),
        "avoided_genome_rescan_seconds_10x": round(genome_scan_seconds, 6),
    }
    print(json.dumps(result, indent=2))
    print("\nTop cumulative simulation-core functions:\n")
    print(report.getvalue())


if __name__ == "__main__":
    main()
