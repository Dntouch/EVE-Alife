from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

from eve_core import Config, Simulation, demo_genome
from lupe import HTML, dashboard_data, readonly_connection
from run_store import RunStore, export_archive


HERE = Path(__file__).resolve().parent


class RunLifecycleTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> tuple[dict, Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        result = subprocess.run(
            [sys.executable, str(HERE / "run.py"), *arguments, "--output", temporary.name,
             "--sample-every", "1", "--checkpoint-every", "0"],
            check=True, text=True, capture_output=True,
        )
        value = json.loads(result.stdout)
        return value, Path(value["run_dir"])

    def test_limited_run_has_distinct_tick_limit_end_reason(self) -> None:
        value, run_dir = self.run_cli("--ticks", "2", "--seed", "7")
        self.assertEqual(value["end_reason"], "tick_limit_reached")
        with sqlite3.connect(run_dir / "run.sqlite3") as db:
            self.assertEqual(
                db.execute("SELECT mode,status,end_reason,current_tick FROM run").fetchone(),
                ("limited", "completed", "tick_limit_reached", 2),
            )

    def test_default_run_uses_frozen_p1_reference_start(self) -> None:
        _, run_dir = self.run_cli("--ticks", "1")
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["configuration"]["seed"], 42)
        self.assertEqual(manifest["configuration"]["novelty_base"], 60.0)
        self.assertEqual(manifest["configuration"]["birth_energy_fraction"], 0.5)
        self.assertEqual(manifest["configuration"]["birth_min_heartbeats"], 5)
        self.assertEqual(manifest["configuration"]["genome_node_cost"], 0.05)
        self.assertEqual(manifest["configuration"]["genome_edge_cost"], 0.01)
        with sqlite3.connect(run_dir / "run.sqlite3") as db:
            payload = db.execute("SELECT payload_zlib FROM observations ORDER BY tick DESC LIMIT 1").fetchone()[0]
        observation = json.loads(zlib.decompress(payload))
        self.assertEqual(len(observation["entities"]), 20)
        self.assertEqual(len(observation["entities"][0]["genome"]["nodes"]), 67)
        variants = manifest["p1_founder_variants"]
        self.assertEqual(len(variants), 20)
        self.assertGreater(len({(item["search_offset"], item["search_step"], item["search_patience"], item["activity_base"]) for item in variants}), 1)
        self.assertTrue(all(item["search_step"] != 0 for item in variants))

    def test_v01_lupe_features_and_genome_diagram_are_retained(self) -> None:
        for label in ("Chronik des Biotops", "Lebensfilm", "Umweltkontakte", "Population und Zeitfilter"):
            self.assertIn(label, HTML)
        self.assertIn("function genomeDiagram", HTML)
        self.assertIn("function openGenomeDiagram", HTML)
        self.assertIn("In eigenem Fenster öffnen", HTML)
        self.assertIn("Unfruchtbar", HTML)
        self.assertIn(".activity-grid{margin-bottom:1.2rem}", HTML)
        self.assertIn("const readHeight=v.reads*120/max", HTML)

    def test_extended_dashboard_keeps_amoeba_records(self) -> None:
        _, run_dir = self.run_cli("--ticks", "1")
        dashboard = dashboard_data(run_dir.parent)
        self.assertEqual(dashboard["runs"], 1)
        self.assertEqual(dashboard["history"][0]["infertile_offspring"], 0)
        self.assertIsNotNone(dashboard["records"]["largest_genome"])
        self.assertIsNotNone(dashboard["records"]["highest_energy"])

    def test_dashboard_orders_runs_by_creation_time_newest_first(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        run_root = Path(temporary.name)
        run_dirs = []
        for seed in (7, 8):
            result = subprocess.run(
                [sys.executable, str(HERE / "run.py"), "--ticks", "1", "--seed", str(seed),
                 "--output", str(run_root), "--sample-every", "1", "--checkpoint-every", "0"],
                check=True, text=True, capture_output=True,
            )
            run_dirs.append(Path(json.loads(result.stdout)["run_dir"]))

        lexical_first, lexical_last = sorted(run_dirs)
        dates = {
            lexical_first: "2026-01-02T00:00:00+00:00",
            lexical_last: "2026-01-01T00:00:00+00:00",
        }
        for run_dir, created_at in dates.items():
            with sqlite3.connect(run_dir / "run.sqlite3") as db:
                db.execute("UPDATE run SET created_at=? WHERE singleton=1", (created_at,))

        dashboard = dashboard_data(run_root)
        self.assertEqual(
            [(run["run_number"], run["created_at"]) for run in dashboard["history"]],
            [(2, dates[lexical_first]), (1, dates[lexical_last])],
        )

    def test_open_run_ends_only_in_natural_extinction(self) -> None:
        value, run_dir = self.run_cli("--open", "--start-energy", "1", "--seed", "7")
        self.assertEqual(value["end_reason"], "natural_extinction")
        with sqlite3.connect(run_dir / "run.sqlite3") as db:
            self.assertEqual(
                db.execute("SELECT mode,tick_limit,status,population FROM run").fetchone(),
                ("open", None, "extinct", 0),
            )

    def test_genomes_are_deduplicated_and_ancestry_is_queryable(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        run_dir = Path(temporary.name)
        sim = Simulation(Config(seed=3))
        genome = demo_genome(2)
        first = sim.add_entity(genome, 100)
        second = sim.add_entity(demo_genome(2), 100, (first.id,))
        manifest = {
            "run_id": "test", "format_version": 2, "prototype_version": "0.2",
            "created_at": "2026-01-01T00:00:00+00:00", "mode": "limited",
            "tick_limit": 1, "configuration": {}, "git_commit": "test",
        }
        with RunStore(run_dir, create=True) as store:
            store.initialize(manifest)
            store.sync_entities(sim)
            store.append_events(sim.events)
            store.update_running(sim)
        with sqlite3.connect(run_dir / "run.sqlite3") as db:
            self.assertEqual(db.execute("SELECT count(*) FROM genomes").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT parent_id FROM ancestry WHERE child_id=?", (second.id,)).fetchone()[0], first.id)

    def test_recombination_trace_records_real_fragments_and_mutation(self) -> None:
        sim = Simulation(Config(seed=11, mutation_probability=1.0))
        parents = [sim.add_entity(demo_genome(partner), 100) for partner in (2, 1)]
        sim._recombine(parents)
        trace = sim._last_genome_trace
        self.assertIsNotNone(trace)
        self.assertTrue(trace["inherited_fragments"])
        self.assertIn(trace["size_parent_id"], (1, 2))
        self.assertIn(trace["activity_parent_id"], (1, 2))
        self.assertIn(trace["mutation"]["class"], ("activity", "node", "edge"))

    def test_portable_archive_contains_manifest_and_consistent_database(self) -> None:
        _, run_dir = self.run_cli("--ticks", "1")
        archive_path = run_dir.parent / "run.eve-run"
        export_archive(run_dir, archive_path)
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual({"manifest.json", "run.sqlite3"}, set(archive.namelist()))
            archive.extract("run.sqlite3", run_dir.parent / "unpacked")
        with sqlite3.connect(run_dir.parent / "unpacked" / "run.sqlite3") as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")

    def test_lupe_database_connection_is_read_only(self) -> None:
        _, run_dir = self.run_cli("--ticks", "1")
        with readonly_connection(run_dir / "run.sqlite3") as db:
            self.assertEqual(db.execute("SELECT end_reason FROM run").fetchone()[0], "tick_limit_reached")
            with self.assertRaises(sqlite3.OperationalError):
                db.execute("DELETE FROM measurements")


if __name__ == "__main__":
    unittest.main()
