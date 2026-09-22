#!/usr/bin/env python3
"""Lokaler v0.3-Supervisor. Nur er startet und stoppt Simulationen."""

from __future__ import annotations

import json
import signal
import subprocess
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from run_parameters import PARAMETERS, PRESETS


ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"
USER_PRESETS = ROOT / "user_presets.json"
ALLOWED_ORIGINS = {"http://127.0.0.1:8766", "http://localhost:8766"}
jobs: dict[str, dict[str, Any]] = {}
lock = threading.Lock()


def load_user_presets() -> dict:
    try:
        value = json.loads(USER_PRESETS.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def all_presets() -> dict:
    return {**PRESETS, **load_user_presets()}


def validate(values: dict) -> dict:
    unknown = set(values) - set(PARAMETERS)
    if unknown:
        raise ValueError(f"Unbekannte Parameter: {', '.join(sorted(unknown))}")
    clean = {}
    for name, spec in PARAMETERS.items():
        raw = values.get(name, spec["default"])
        kind = spec["type"]
        if kind == "text":
            value = str(raw).strip()[:120]
        elif kind == "bool":
            if not isinstance(raw, bool):
                raise ValueError(f"{spec['label']} muss wahr oder falsch sein")
            value = raw
        elif kind == "choice":
            value = str(raw)
            if value not in spec["choices"]:
                raise ValueError(f"Ungültiger Wert für {spec['label']}")
        elif kind == "int":
            if isinstance(raw, bool):
                raise ValueError(f"{spec['label']} muss eine ganze Zahl sein")
            value = int(raw)
        else:
            value = float(raw)
        if kind in {"int", "float"}:
            if value < spec.get("min", value) or value > spec.get("max", value):
                raise ValueError(f"{spec['label']} liegt außerhalb des erlaubten Bereichs")
        clean[name] = value
    if clean["population"] % 2:
        raise ValueError("Die Startpopulation muss gerade sein")
    return clean


def command_for(run_id: str, values: dict) -> list[str]:
    command = [sys.executable, str(ROOT / "run.py"), "--run-id", run_id, "--output", str(RUNS)]
    command += ["--open"] if values["mode"] == "open" else ["--ticks", str(values["ticks"])]
    flags = {
        "label": "--label", "seed": "--seed", "population": "--population",
        "start_energy": "--start-energy", "birth_energy": "--birth-energy",
        "birth_energy_fraction": "--birth-energy-fraction",
        "birth_min_heartbeats": "--birth-min-heartbeats", "novelty_base": "--novelty-base",
        "aging_cost_rate": "--aging-cost-rate", "genome_node_cost": "--genome-node-cost",
        "genome_edge_cost": "--genome-edge-cost", "entity_discovery_base": "--entity-discovery-base",
        "invitation_discovery_base": "--invitation-discovery-base",
        "life_state_discovery_base": "--life-state-discovery-base", "ram_world": "--ram-world",
        "population_model": "--population-model", "sample_every": "--sample-every",
        "checkpoint_every": "--checkpoint-every",
    }
    for name, flag in flags.items():
        command.extend((flag, str(values[name])))
    if values["uniform_p1"]:
        command.append("--uniform-p1")
    return command


def monitor(run_id: str, process: subprocess.Popen) -> None:
    output, _ = process.communicate()
    with lock:
        if run_id in jobs:
            jobs[run_id].update({"returncode": process.returncode, "output": output[-4000:], "running": False})


class Handler(BaseHTTPRequestHandler):
    def cors(self) -> None:
        origin = self.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")

    def respond(self, value: object, status: int = 200) -> None:
        data = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.cors(); self.end_headers(); self.wfile.write(data)

    def body(self) -> dict:
        length = min(int(self.headers.get("Content-Length", "0")), 1_000_000)
        value = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(value, dict):
            raise ValueError("JSON-Objekt erwartet")
        return value

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.cors(); self.end_headers()

    def do_GET(self):
        if self.path == "/api/schema":
            self.respond(PARAMETERS)
        elif self.path == "/api/presets":
            self.respond(all_presets())
        elif self.path == "/api/jobs":
            with lock:
                self.respond([{key: value for key, value in job.items() if key != "process"} for job in jobs.values()])
        else:
            self.respond({"error": "Nicht gefunden"}, 404)

    def do_POST(self):
        try:
            if self.headers.get("Origin") not in ALLOWED_ORIGINS:
                self.respond({"error": "Nicht erlaubter Ursprung"}, 403); return
            payload = self.body()
            if self.path == "/api/start":
                values = validate(payload.get("values", {}))
                run_id = str(uuid.uuid4())
                process = subprocess.Popen(
                    command_for(run_id, values), cwd=ROOT, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, start_new_session=True,
                )
                job = {"run_id": run_id, "pid": process.pid, "running": True, "values": values, "process": process}
                with lock: jobs[run_id] = job
                threading.Thread(target=monitor, args=(run_id, process), daemon=True).start()
                self.respond({"run_id": run_id, "status": "starting"}, 202)
            elif self.path == "/api/stop":
                run_id = str(payload.get("run_id", ""))
                with lock: job = jobs.get(run_id)
                if not job or not job["running"] or job["process"].poll() is not None:
                    self.respond({"error": "Run wird von diesem Supervisor nicht aktiv geführt"}, 409); return
                job["process"].send_signal(signal.SIGTERM)
                self.respond({"run_id": run_id, "status": "stop_requested"}, 202)
            elif self.path == "/api/resume":
                source_id = str(payload.get("run_id", ""))
                source = RUNS / source_id
                checkpoints = sorted((source / "checkpoints").glob("*.json")) if source.is_dir() else []
                if source.name != source_id or not checkpoints:
                    self.respond({"error": "Kein fortsetzbarer Checkpoint gefunden"}, 404); return
                run_id = str(uuid.uuid4())
                command = [sys.executable, str(ROOT / "run.py"), "--run-id", run_id, "--output", str(RUNS), "--resume", str(checkpoints[-1]), "--open", "--label", f"Fortsetzung {source_id[:8]}"]
                process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
                job = {"run_id": run_id, "pid": process.pid, "running": True, "resumed_from_run": source_id, "process": process}
                with lock: jobs[run_id] = job
                threading.Thread(target=monitor, args=(run_id, process), daemon=True).start()
                self.respond({"run_id": run_id, "status": "starting", "resumed_from_run": source_id}, 202)
            elif self.path == "/api/presets":
                name = str(payload.get("name", "")).strip()
                if not name:
                    raise ValueError("Presetname fehlt")
                values = validate(payload.get("values", {}))
                presets = load_user_presets()
                key = "user-" + uuid.uuid4().hex[:12]
                presets[key] = {"label": name[:80], "description": "Benutzerdefiniertes v0.3-Preset", "values": values}
                USER_PRESETS.write_text(json.dumps(presets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                self.respond({"key": key, "preset": presets[key]}, 201)
            else:
                self.respond({"error": "Nicht gefunden"}, 404)
        except (ValueError, json.JSONDecodeError) as error:
            self.respond({"error": str(error)}, 400)

    def log_message(self, _format, *_args):
        pass


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8767), Handler)
    print("Supervisor: http://127.0.0.1:8767")
    try: server.serve_forever()
    finally: server.server_close()


if __name__ == "__main__":
    main()
