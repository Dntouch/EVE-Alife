#!/usr/bin/env python3
"""Read-only Lupe: serviert ausschließlich persistierte Beobachtungsdaten."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HTML = """<!doctype html><meta charset=utf-8><title>EVE-Alife Lupe</title>
<style>body{font:15px system-ui;background:#101418;color:#dce8df;margin:2rem}table{border-collapse:collapse;width:100%}td,th{padding:.45rem;border-bottom:1px solid #35413a;text-align:left}.dead{opacity:.45}canvas{width:100%;background:#172019;margin:.5rem 0 1rem}pre{max-width:35rem;overflow:auto;color:#9fe3ad}code{color:#9fe3ad}</style>
<h1>EVE-Alife · Lupe P0.1</h1><p id=meta></p><label>Snapshot <select id=snap><option value=latest>aktuell</option></select></label>
<h2>Population</h2><canvas id=chart width=1000 height=110></canvas><h2>RAM-Suppe · erste 4.096 Zellen</h2><canvas id=ram width=1024 height=64></canvas>
<h2>Entitäten</h2><table><thead><tr><th>ID</th><th>Status</th><th>S</th><th>Eltern</th><th>F/P/G</th><th>A₀</th><th>K</th><th>Z</th><th>Details</th></tr></thead><tbody id=rows></tbody></table>
<script>
const history=[],select=document.querySelector('#snap');async function loadList(){const a=await fetch('/api/snapshots').then(r=>r.json());select.innerHTML='<option value=latest>aktuell</option>'+a.map(x=>`<option>${x}</option>`).join('')};
async function update(){const path=select.value==='latest'?'/api/latest':'/api/snapshot/'+select.value;const s=await fetch(path,{cache:'no-store'}).then(r=>r.json());
meta.textContent=`Run ${s.run_id||'—'} · Tick ${s.tick} · Population ${s.entities.filter(e=>e.alive).length}/${s.entities.length} · Seed ${s.config.seed}`;
rows.innerHTML=s.entities.map(e=>`<tr class=${e.alive?'':'dead'}><td>${e.id}</td><td>${e.alive?'lebend':'tot'}</td><td>${e.energy.toFixed(2)}</td><td>${e.parents.join(', ')||'—'}</td><td>${e.n_f}/${e.n_p}/${e.n_g}</td><td>${e.activity_base}</td><td>${e.k_slots}</td><td>${e.z_used}</td><td><details><summary>anzeigen</summary><pre>${JSON.stringify(e.z,null,2)}</pre></details></td></tr>`).join('');
const rc=document.querySelector('#ram'),rx=rc.getContext('2d'),cells=s.ram.slice(0,4096);rx.clearRect(0,0,rc.width,rc.height);cells.forEach((v,i)=>{const q=(Math.abs(v)%256);rx.fillStyle=`rgb(${v<0?q:20},${v>=0?q:20},80)`;rx.fillRect(i%1024,Math.floor(i/1024)*16,1,16)});
history.push(s.entities.filter(e=>e.alive).length); if(history.length>1000)history.shift(); const c=document.querySelector('canvas'),x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);x.strokeStyle='#72dc8b';x.beginPath();history.forEach((v,i)=>{const px=i*c.width/Math.max(1,history.length-1),py=c.height-v*c.height/Math.max(1,...history);i?x.lineTo(px,py):x.moveTo(px,py)});x.stroke();}
select.onchange=update;loadList().then(update);setInterval(()=>{if(select.value==='latest')update()},1000);
</script>"""


def handler_for(run_dir: Path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                data, content_type = HTML.encode(), "text/html; charset=utf-8"
            elif self.path == "/api/latest":
                try:
                    data = (run_dir / "latest.json").read_bytes()
                except FileNotFoundError:
                    data = json.dumps({"error": "Noch kein Snapshot"}).encode()
                content_type = "application/json; charset=utf-8"
            elif self.path == "/api/snapshots":
                names = sorted(path.name for path in (run_dir / "snapshots").glob("*.json"))
                data = json.dumps(names).encode(); content_type = "application/json; charset=utf-8"
            elif self.path.startswith("/api/snapshot/"):
                name = self.path.removeprefix("/api/snapshot/")
                if Path(name).name != name or not name.endswith(".json"):
                    self.send_error(400); return
                try: data = (run_dir / "snapshots" / name).read_bytes()
                except FileNotFoundError: self.send_error(404); return
                content_type = "application/json; charset=utf-8"
            else:
                self.send_error(404); return
            self.send_response(200); self.send_header("Content-Type", content_type); self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(data)
        def log_message(self, format, *args):
            pass
    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only EVE-Alife Lupe")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(args.run_dir.resolve()))
    print(f"Lupe: http://127.0.0.1:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
