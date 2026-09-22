"""Versionierte, read-only veröffentlichbare Run-Datenhaltung für EVE-Alife v0.3."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import tempfile
import zipfile
import zlib
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 2
FORMAT_NAME = "eve-alife-run"

# Zustandsrekonstruktion auf Tick-Ebene ist nicht Ziel dieses Stroms. Die sehr
# häufigen Ausführungsdetails bleiben in Checkpoints bzw. im flüchtigen Livebild.
PERSISTED_EVENT_KINDS = {
    "birth", "death", "birth_rejected", "reproduction_cost", "genome_created",
    "ram_read", "ram_write", "mem_read", "mem_write", "mem_write_rejected", "knock",
    "environment_change",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


class RunStore:
    """Single-writer SQLite store; readers may concurrently open it read-only."""

    def __init__(self, run_dir: Path, create: bool = False) -> None:
        self.run_dir = run_dir
        self.path = run_dir / "run.sqlite3"
        run_dir.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.manifest_extra: dict[str, Any] = {}
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        if create:
            self._create_schema()

    def _create_schema(self) -> None:
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS run (
            singleton INTEGER PRIMARY KEY CHECK(singleton=1),
            run_id TEXT NOT NULL UNIQUE, format_version INTEGER NOT NULL,
            prototype_version TEXT NOT NULL, created_at TEXT NOT NULL,
            started_at TEXT NOT NULL, finished_at TEXT,
            mode TEXT NOT NULL CHECK(mode IN ('limited','open')),
            tick_limit INTEGER, status TEXT NOT NULL,
            end_reason TEXT, current_tick INTEGER NOT NULL DEFAULT 0,
            population INTEGER NOT NULL DEFAULT 0, config_json TEXT NOT NULL,
            git_commit TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS genomes (
            genome_id INTEGER PRIMARY KEY, fingerprint TEXT NOT NULL UNIQUE,
            genome_json TEXT NOT NULL, n_f INTEGER NOT NULL, n_p INTEGER NOT NULL,
            n_g INTEGER NOT NULL, activity_base INTEGER NOT NULL,
            first_seen_tick INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS entities (
            entity_id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            born_tick INTEGER NOT NULL, died_tick INTEGER, death_reason TEXT,
            ram_position INTEGER NOT NULL DEFAULT 0,
            genome_id INTEGER NOT NULL REFERENCES genomes(genome_id)
        );
        CREATE TABLE IF NOT EXISTS ancestry (
            child_id INTEGER NOT NULL REFERENCES entities(entity_id),
            parent_id INTEGER NOT NULL, parent_order INTEGER NOT NULL,
            PRIMARY KEY(child_id,parent_order)
        );
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY, tick INTEGER NOT NULL,
            kind TEXT NOT NULL, entity_id INTEGER, payload_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS events_tick_kind ON events(tick,kind);
        CREATE INDEX IF NOT EXISTS events_entity_tick ON events(entity_id,tick);
        CREATE TABLE IF NOT EXISTS measurements (
            tick INTEGER PRIMARY KEY, population INTEGER NOT NULL,
            entities_total INTEGER NOT NULL, genomes_distinct INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS observations (
            tick INTEGER PRIMARY KEY, payload_zlib BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS checkpoints (
            tick INTEGER PRIMARY KEY, relative_path TEXT NOT NULL,
            sha256 TEXT NOT NULL, bytes INTEGER NOT NULL
        );
        """)
        self.db.commit()

    def initialize(self, manifest: dict[str, Any]) -> None:
        self.manifest_extra = {
            key: value for key, value in manifest.items()
            if key not in {"configuration"}
        }
        self.db.execute(
            """INSERT INTO run VALUES
            (1,:run_id,:format_version,:prototype_version,:created_at,:started_at,NULL,
             :mode,:tick_limit,'running',NULL,0,0,:config_json,:git_commit)""",
            {**manifest, "started_at": manifest["created_at"],
             "config_json": canonical_json(manifest["configuration"])},
        )
        self.db.commit()
        self.write_manifest()

    @staticmethod
    def _genome_data(genome: Any) -> dict[str, Any]:
        return {
            "activity_base": genome.activity_base,
            "knock_capacity": genome.knock_capacity,
            "bond_ticks": genome.bond_ticks,
            "nodes": [asdict(node) for node in genome.nodes],
            "edges": [asdict(edge) for edge in genome.edges],
        }

    def register_genome(self, genome: Any, tick: int) -> int:
        value = self._genome_data(genome)
        encoded = canonical_json(value)
        fingerprint = hashlib.sha256(encoded.encode()).hexdigest()
        self.db.execute(
            """INSERT OR IGNORE INTO genomes
            (fingerprint,genome_json,n_f,n_p,n_g,activity_base,first_seen_tick)
            VALUES(?,?,?,?,?,?,?)""",
            (fingerprint, encoded, len(genome.nodes), len(genome.edges),
             len(genome.nodes) + len(genome.edges), genome.activity_base, tick),
        )
        row = self.db.execute(
            "SELECT genome_id FROM genomes WHERE fingerprint=?", (fingerprint,)
        ).fetchone()
        assert row is not None
        return int(row[0])

    def sync_entities(self, simulation: Any) -> None:
        for entity in simulation.entities.values():
            genome_id = self.register_genome(entity.genome, entity.born_at)
            inserted = self.db.execute(
                """INSERT OR IGNORE INTO entities
                (entity_id,name,born_tick,ram_position,genome_id) VALUES(?,?,?,?,?)""",
                (entity.id, entity.name, entity.born_at, entity.ram_position, genome_id),
            ).rowcount
            if inserted:
                self.db.executemany(
                    "INSERT INTO ancestry(child_id,parent_id,parent_order) VALUES(?,?,?)",
                    [(entity.id, parent, order) for order, parent in enumerate(entity.parents)],
                )

    def append_events(self, events: Iterable[dict[str, Any]]) -> None:
        for event in events:
            kind = event["kind"]
            if kind not in PERSISTED_EVENT_KINDS:
                continue
            payload = dict(event)
            tick = int(payload.pop("tick"))
            payload.pop("kind")
            entity_id = payload.get("entity_id")
            self.db.execute(
                "INSERT INTO events(tick,kind,entity_id,payload_json) VALUES(?,?,?,?)",
                (tick, kind, entity_id, canonical_json(payload)),
            )
            if kind == "death" and entity_id is not None:
                self.db.execute(
                    "UPDATE entities SET died_tick=?, death_reason=? WHERE entity_id=?",
                    (tick, payload.get("reason"), entity_id),
                )

    def sample(self, simulation: Any) -> None:
        population = sum(entity.alive for entity in simulation.entities.values())
        self.db.execute(
            "INSERT OR REPLACE INTO measurements VALUES(?,?,?,?)",
            (simulation.tick, population, len(simulation.entities),
             self.db.execute("SELECT count(*) FROM genomes").fetchone()[0]),
        )

    def observe(self, simulation: Any, run_id: str) -> None:
        """Periodisches Lupe-Bild wie in v0.1, jedoch ohne redundante RAM-Kopie."""
        observation = simulation.observation()
        observation.pop("ram", None)
        observation["run_id"] = run_id
        payload = json.dumps(observation, ensure_ascii=False, separators=(",", ":")).encode()
        self.db.execute(
            "INSERT OR REPLACE INTO observations VALUES(?,?)",
            (simulation.tick, sqlite3.Binary(zlib.compress(payload, level=6))),
        )

    def record_checkpoint(self, path: Path, tick: int) -> None:
        content = path.read_bytes()
        self.db.execute(
            "INSERT OR REPLACE INTO checkpoints VALUES(?,?,?,?)",
            (tick, str(path.relative_to(self.run_dir)), hashlib.sha256(content).hexdigest(), len(content)),
        )
        self.db.commit()

    def update_running(self, simulation: Any) -> None:
        population = sum(entity.alive for entity in simulation.entities.values())
        self.db.execute(
            "UPDATE run SET current_tick=?, population=? WHERE singleton=1",
            (simulation.tick, population),
        )
        self.db.commit()
        self.write_manifest()

    def finish(self, simulation: Any, end_reason: str) -> None:
        if end_reason not in {"natural_extinction", "tick_limit_reached", "user_requested"}:
            raise ValueError(f"Unbekannter Endgrund: {end_reason}")
        status = "extinct" if end_reason == "natural_extinction" else ("stopped" if end_reason == "user_requested" else "completed")
        population = sum(entity.alive for entity in simulation.entities.values())
        self.db.execute(
            """UPDATE run SET status=?,end_reason=?,finished_at=?,current_tick=?,population=?
            WHERE singleton=1""",
            (status, end_reason, utc_now(), simulation.tick, population),
        )
        self.db.commit()
        self.write_manifest()
        self.db.execute("PRAGMA wal_checkpoint(TRUNCATE)")

    def write_manifest(self) -> None:
        self.db.row_factory = sqlite3.Row
        row = self.db.execute("SELECT * FROM run WHERE singleton=1").fetchone()
        self.db.row_factory = None
        if row is None:
            return
        data = dict(row)
        data.pop("singleton")
        data["configuration"] = json.loads(data.pop("config_json"))
        data.update({
            "format": FORMAT_NAME,
            "database": "run.sqlite3",
            "observation_interface": "read-only",
        })
        for key, value in self.manifest_extra.items():
            data.setdefault(key, value)
        atomic_json(self.run_dir / "manifest.json", data)

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "RunStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def export_archive(run_dir: Path, destination: Path) -> Path:
    """Create a portable immutable snapshot; transient WAL files are excluded."""
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("format_version") != SCHEMA_VERSION:
        raise ValueError("Nicht unterstützte Run-Formatversion")
    source = sqlite3.connect(run_dir / "run.sqlite3")
    temporary = destination.with_suffix(destination.suffix + ".tmp.sqlite3")
    target = sqlite3.connect(temporary)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(run_dir / "manifest.json", "manifest.json")
        archive.write(temporary, "run.sqlite3")
        for checkpoint in sorted((run_dir / "checkpoints").glob("*.json")):
            archive.write(checkpoint, f"checkpoints/{checkpoint.name}")
    temporary.unlink()
    return destination
