#!/usr/bin/env python3
"""Read-only Lupe für persistierte EVE-Beobachtungsdaten."""
from __future__ import annotations
import argparse, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HTML = r'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EVE-Alife Lupe</title><style>
:root{--bg:#0d1210;--p:#151d19;--p2:#1b2620;--line:#34443a;--text:#e4eee7;--muted:#9bae9f;--green:#73dc8c;--amber:#e6bd68;--blue:#77b9e8;--red:#e17b72}*{box-sizing:border-box}body{font:15px/1.45 system-ui,sans-serif;background:var(--bg);color:var(--text);margin:0}main{max-width:1500px;margin:auto;padding:1.5rem}h1{margin:.1rem 0}.muted,.subtitle{color:var(--muted)}h2{margin-top:1.8rem}h3{margin:.4rem 0}.top,.terms,.metrics,.columns,.entities{display:grid;gap:.8rem}.top{grid-template-columns:1fr auto;align-items:end}.terms{grid-template-columns:repeat(auto-fit,minmax(155px,1fr))}.metrics{grid-template-columns:repeat(auto-fit,minmax(125px,1fr));margin:.8rem 0}.columns{grid-template-columns:1fr 1fr}.entities{grid-template-columns:repeat(auto-fit,minmax(430px,1fr))}.term,.metric,.panel,.entity{background:var(--p);border:1px solid var(--line);border-radius:9px;padding:.8rem}.term b,.metric strong{color:var(--green)}.metric strong{display:block;font-size:1.3rem}[data-tip]{text-decoration:underline dotted;text-underline-offset:3px;cursor:help}.help{border-left:3px solid var(--green);padding:.6rem .8rem;background:var(--p)}select,button{background:var(--p2);color:var(--text);border:1px solid var(--line);padding:.45rem .65rem;border-radius:5px}button{cursor:pointer}button:hover{border-color:var(--green)}canvas{width:100%;background:#111a15;border:1px solid var(--line);border-radius:6px}.entity.dead{opacity:.6}.entity>summary{cursor:pointer;font-weight:650;list-style:none}.badge{border-radius:999px;padding:.12rem .5rem;margin-left:.4rem;font-size:.8rem;background:#294131;color:#b9efc5}.dead .badge{background:#432b29;color:#f0b2ac}.entity-meta{color:var(--muted);margin:.5rem 0}table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{padding:.35rem .45rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--muted)}.scroll{max-height:310px;overflow:auto}.empty{color:var(--muted);font-style:italic}.signal{color:var(--blue)}.source{color:var(--amber);font-size:.82rem}.edges,code{font-family:ui-monospace,monospace}code{color:#a9ebb7;background:#0d1511;padding:.1rem .3rem;border-radius:3px}.error{color:var(--red)}#replay{border-color:var(--green);margin:1.2rem 0}#replay[hidden]{display:none}.replay-controls{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}.replay-controls input[type=range]{flex:1;min-width:220px}.events-log{max-height:240px;overflow:auto;background:#0d1511;border-radius:6px;padding:.5rem 1.8rem}.events-log li{margin:.25rem 0}.life-button{margin:.15rem 0 .7rem}@media(max-width:850px){.columns,.top{grid-template-columns:1fr}.entities{grid-template-columns:1fr}main{padding:.8rem}}
</style></head><body><main><div class="top"><div><h1>EVE-Alife · Lupe</h1><div class="subtitle">Read-only-Beobachtung eines gespeicherten Laufs</div></div><label>Zeitpunkt ansehen<br><select id="snap"><option value="latest">aktuell</option></select></label></div>
<p class="help">Die Buchstaben bezeichnen Teile einer Amöbe. Fahre über <span data-tip title="Kurzerklärung direkt am Begriff">unterstrichene Begriffe</span>. Die Lupe kann den Lauf nicht verändern.</p><section class="terms">
<div class="term"><b>G · Genom</b><br>Erbliche Funktionspunkte, Verbindungen und Basisaktivität A₀.</div><div class="term"><b>P · Pfade</b><br>Gerichtete Kanten, über die Werte zwischen Funktionspunkten fließen.</div><div class="term"><b>K · Kurzzeit</b><br>Flüchtige Portwerte; beim Benutzen verbraucht und nicht vererbt.</div><div class="term"><b>Z · Zustand</b><br>Dauerhaft gespeicherte Werte samt Herkunft; bei Geburt leer.</div><div class="term"><b>S · Energie</b><br>Bezahlt Existenz, Ausführung und Reproduktion.</div><div class="term"><b>RAM · Suppe</b><br>Gemeinsamer, für alle erreichbarer roher Zahlenraum.</div></section>
<div id="meta" class="metrics"></div><section id="replay" class="panel" hidden><div class="top"><div><h2 id="replay-title">Lebensfilm</h2><p id="replay-position" class="muted"></p></div><button onclick="closeReplay()">Schließen</button></div><div class="replay-controls"><button id="replay-prev" title="Ein Bild zurück">◀</button><button id="replay-play">▶ Abspielen</button><button id="replay-next" title="Ein Bild weiter">▶|</button><input id="replay-slider" type="range" min="0" value="0"><label>Tempo <select id="replay-speed"><option value="1800">langsam</option><option value="800" selected>normal</option><option value="300">schnell</option></select></label></div><h3>Was in diesem Schritt geschah</h3><ol id="replay-events" class="events-log"></ol><div id="replay-state"></div></section><section class="columns"><div class="panel"><h2>Population</h2><canvas id="chart" width="700" height="150"></canvas><p class="muted">Lebende Entitäten in den empfangenen Snapshots.</p></div><div class="panel"><h2>RAM-Suppe</h2><canvas id="ram" width="1024" height="96"></canvas><p class="muted">Erste 4.096 Zellen: rot negativ, grün nichtnegativ.</p></div></section><h2>Entitäten</h2><p class="muted">Aufklappen, um Genom und Speicher zum gewählten Tick zu sehen.</p><section id="entities" class="entities"></section>
</main><script>
const select=document.querySelector('#snap'),box=document.querySelector('#entities'),metaBox=document.querySelector('#meta'),ramCanvas=document.querySelector('#ram'),chartCanvas=document.querySelector('#chart'),replayBox=document.querySelector('#replay'),replaySlider=document.querySelector('#replay-slider'),esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let replayFrames=[],replayIndex=0,replayTimer=null;
const nodeHelp={CONST:'Erbliche konstante Zahl',S_READ:'Liest die eigene Energie S',Z_READ:'Liest eine Z-Zelle',Z_WRITE:'Schreibt dauerhaft nach Z',RAM_READ:'Liest eine Zelle der gemeinsamen RAM-Suppe',RAM_WRITE:'Schreibt in die gemeinsame RAM-Suppe',MEM_READ:'Liest die eigene Membran',MEM_WRITE:'Schreibt in die eigene Membran',ADD:'Addiert zwei Werte',SUB:'Subtrahiert b von a',XOR:'Bitweises Exklusiv-Oder',EQ:'Liefert 1 bei Gleichheit, sonst 0',GATE:'Leitet einen Wert nur bei einer Bedingung ungleich 0 weiter',PAUSE:'Verbraucht die Eingabe ohne weitere Wirkung'};
const sig=s=>s?`<span class="signal">${esc(s.value)}</span><br><span class="source">Quelle: ${esc((s.sources||[]).join(' + ')||'—')}</span>`:'<span class="empty">leer</span>';
function nodes(g){return g?`<div class="scroll"><table><thead><tr><th>ID</th><th>Funktionspunkt</th><th>Erblicher Wert</th></tr></thead><tbody>${g.nodes.map(n=>`<tr><td>${n.id}</td><td><code data-tip title="${esc(nodeHelp[n.kind]||'Primitiver Funktionspunkt')}">${esc(n.kind)}</code></td><td>${n.constant===null?'—':esc(n.constant)}</td></tr>`).join('')}</tbody></table></div>`:'<p class="empty">Im älteren Snapshot nicht enthalten.</p>'}
function edges(g){return g&&g.edges.length?`<div class="scroll"><table class="edges"><thead><tr><th>Quelle</th><th></th><th>Ziel</th></tr></thead><tbody>${g.edges.map(p=>`<tr><td>#${p.source}.${esc(p.source_port)}</td><td>→</td><td>#${p.target}.${esc(p.target_port)}</td></tr>`).join('')}</tbody></table></div>`:'<p class="empty">Keine P-Kanten oder keine Details.</p>'}
function kvals(k){const a=Object.entries(k||{});return a.length?`<table><thead><tr><th>Port</th><th>Wert</th></tr></thead><tbody>${a.map(([p,s])=>`<tr><td><code>${esc(p)}</code></td><td>${sig(s)}</td></tr>`).join('')}</tbody></table>`:'<p class="empty">K ist gerade leer.</p>'}
function zvals(z){return z?`<div class="scroll"><table><thead><tr><th>Adresse</th><th>Inhalt</th></tr></thead><tbody>${z.map((s,i)=>`<tr><td>${i}</td><td>${sig(s)}</td></tr>`).join('')}</tbody></table></div>`:'<p class="empty">Keine Details.</p>'}
function card(e,open,withReplay=true){return `<details class="entity ${e.alive?'':'dead'}" data-entity="${e.id}" ${open.has(String(e.id))?'open':''}><summary>Amöbe #${e.id}<span class="badge">${e.alive?'lebend':'tot'}</span></summary><div class="entity-meta"><span data-tip title="Energievorrat S">S ${e.energy.toFixed(2)}</span> · geboren Tick ${e.born_at} · Eltern ${e.parents.join(', ')||'—'} · Partner ${e.partners.filter(x=>x!==null).join(', ')||'—'}</div>${withReplay?`<button class="life-button" onclick="startReplay(${e.id})">▶ Leben abspielen</button>`:''}<div class="metrics"><div class="metric"><span data-tip title="Funktionspunkt-Instanzen">F</span><strong>${e.n_f}</strong></div><div class="metric"><span data-tip title="Datenflusskanten">P</span><strong>${e.n_p}</strong></div><div class="metric"><span data-tip title="Genomgröße F + P">G-Größe</span><strong>${e.n_g}</strong></div><div class="metric"><span data-tip title="Erbliche Basisaktivität">A₀</span><strong>${e.activity_base}</strong></div></div><div class="columns"><section><h3 data-tip title="Konkrete erbliche Rechenbausteine">G · Funktionspunkte</h3>${nodes(e.genome)}</section><section><h3 data-tip title="Gerichtete Verbindungen im Genom">P · Kanten</h3>${edges(e.genome)}</section><section><h3 data-tip title="Flüchtig belegte Eingangsports">K · Kurzzeit (${e.k_slots})</h3>${kvals(e.k)}</section><section><h3 data-tip title="Dauerhafter individueller Speicher">Z · Zustand (${e.z_used}/${(e.z||[]).length})</h3>${zvals(e.z)}</section></div></details>`}
function describe(e){const n=e.node_id===undefined?'':`#${e.node_id} `;switch(e.kind){case'birth':return`Geburt mit ${e.energy} Energie; Eltern: ${(e.parents||[]).join(', ')||'Startpopulation'}`;case'death':return`Tod: ${e.reason==='standby_unaffordable'?'Standby nicht mehr finanzierbar':e.reason}`;case'standby':return`Standby kostet ${e.cost}; S ${e.energy_before.toFixed(2)} → ${e.energy_after.toFixed(2)}`;case'node_fire':return`${n}${e.node_kind} wird ausgeführt; Kosten ${e.cost.toFixed(2)}, S danach ${e.energy_after.toFixed(2)}`;case'gate':return`${n}GATE ${e.opened?'öffnet':'sperrt'} bei Bedingung ${e.condition}; Wert ${e.value}`;case'ram_read':return`${e.virtual?'Membran':'RAM'}[${e.address}] gelesen → ${e.value}`;case'ram_write':return`RAM[${e.address}] beschrieben → ${e.value}`;case'z_write':return`Z[${e.address}] ← ${e.value}; Energiegewinn +${e.reward.toFixed(3)}`;case'mem_write':return`Partnerslot ${e.slot} ← Amöbe #${e.value}`;case'reproduction_cost':return`Geburtsbeitrag ${e.cost}; Kind #${e.child_id}`;case'signal':return`Signal ${e.value}: #${e.source} → #${e.target}`;default:return e.kind}}
function showReplay(i){if(!replayFrames.length)return;replayIndex=Math.max(0,Math.min(i,replayFrames.length-1));const f=replayFrames[replayIndex];replaySlider.value=replayIndex;document.querySelector('#replay-position').textContent=`Tick ${f.tick} · Bild ${replayIndex+1} von ${replayFrames.length}`;document.querySelector('#replay-events').innerHTML=f.events.length?f.events.map(e=>`<li>${esc(describe(e))}</li>`).join(''):'<li class="empty">In diesem gespeicherten Intervall kein Ereignis.</li>';document.querySelector('#replay-state').innerHTML=card(f.entity,new Set([String(f.entity.id)]),false)}
async function startReplay(id){stopReplay();const data=await fetch(`/api/entity/${id}/life`).then(r=>r.json());replayFrames=data.frames||[];if(!replayFrames.length){alert('Für diese Amöbe sind keine Replay-Snapshots vorhanden.');return}document.querySelector('#replay-title').textContent=`Lebensfilm · Amöbe #${id}`;replaySlider.max=replayFrames.length-1;replayBox.hidden=false;showReplay(0);replayBox.scrollIntoView({behavior:'smooth'})}
function stopReplay(){if(replayTimer)clearInterval(replayTimer);replayTimer=null;document.querySelector('#replay-play').textContent='▶ Abspielen'}function closeReplay(){stopReplay();replayBox.hidden=true}function toggleReplay(){if(replayTimer){stopReplay();return}document.querySelector('#replay-play').textContent='⏸ Pause';replayTimer=setInterval(()=>{if(replayIndex>=replayFrames.length-1){stopReplay();return}showReplay(replayIndex+1)},Number(document.querySelector('#replay-speed').value))}
document.querySelector('#replay-prev').onclick=()=>{stopReplay();showReplay(replayIndex-1)};document.querySelector('#replay-next').onclick=()=>{stopReplay();showReplay(replayIndex+1)};document.querySelector('#replay-play').onclick=toggleReplay;replaySlider.oninput=()=>{stopReplay();showReplay(Number(replaySlider.value))};document.querySelector('#replay-speed').onchange=()=>{if(replayTimer){stopReplay();toggleReplay()}};
function drawTimeline(points){const g=chartCanvas.getContext('2d');g.clearRect(0,0,chartCanvas.width,chartCanvas.height);g.strokeStyle='#73dc8c';g.lineWidth=2;g.beginPath();points.forEach((p,i)=>{const x=i*chartCanvas.width/Math.max(1,points.length-1),y=chartCanvas.height-8-p.alive*(chartCanvas.height-16)/Math.max(1,...points.map(q=>q.alive));i?g.lineTo(x,y):g.moveTo(x,y)});g.stroke()}
async function list(){const [a,t]=await Promise.all([fetch('/api/snapshots').then(r=>r.json()),fetch('/api/timeline').then(r=>r.json())]);select.innerHTML='<option value="latest">aktuell</option>'+a.map(x=>`<option value="${esc(x)}">Tick ${parseInt(x)}</option>`).join('');drawTimeline(t)}
async function update(){try{const p=select.value==='latest'?'/api/latest':'/api/snapshot/'+select.value,s=await fetch(p,{cache:'no-store'}).then(r=>r.json());if(s.error)throw Error(s.error);const alive=s.entities.filter(e=>e.alive).length;metaBox.innerHTML=`<div class="metric">Tick<strong>${s.tick}</strong></div><div class="metric">Lebend<strong>${alive}</strong></div><div class="metric">Geboren gesamt<strong>${s.entities.length}</strong></div><div class="metric">Seed<strong>${s.config.seed}</strong></div><div class="metric">Run<strong style="font-size:.8rem">${esc(s.run_id||'—')}</strong></div>`;const open=new Set([...box.querySelectorAll('details[open]')].map(d=>d.dataset.entity));box.innerHTML=s.entities.map(e=>card(e,open)).join('');const x=ramCanvas.getContext('2d'),cells=s.ram.slice(0,4096);x.clearRect(0,0,ramCanvas.width,ramCanvas.height);cells.forEach((v,i)=>{const q=Math.abs(v)%236+20;x.fillStyle=`rgb(${v<0?q:20},${v>=0?q:20},70)`;x.fillRect(i%1024,Math.floor(i/1024)*24,1,24)})}catch(e){box.innerHTML=`<p class="error">${esc(e.message)}</p>`}}
select.onchange=update;list().then(update);setInterval(()=>{if(select.value==='latest')update()},1000);
</script></body></html>'''

def handler_for(run_dir: Path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/": data, kind = HTML.encode(), "text/html; charset=utf-8"
            elif self.path == "/api/latest":
                try: data = (run_dir / "latest.json").read_bytes()
                except FileNotFoundError: data = json.dumps({"error": "Noch kein Snapshot"}).encode()
                kind = "application/json; charset=utf-8"
            elif self.path == "/api/snapshots":
                data = json.dumps(sorted(p.name for p in (run_dir / "snapshots").glob("*.json"))).encode(); kind = "application/json; charset=utf-8"
            elif self.path == "/api/timeline":
                timeline = []
                for path in sorted((run_dir / "snapshots").glob("*.json")):
                    snapshot = json.loads(path.read_text(encoding="utf-8"))
                    timeline.append({"tick": snapshot["tick"], "alive": sum(e["alive"] for e in snapshot["entities"])})
                data = json.dumps(timeline).encode(); kind = "application/json; charset=utf-8"
            elif self.path.startswith("/api/entity/") and self.path.endswith("/life"):
                raw_id = self.path.removeprefix("/api/entity/").removesuffix("/life")
                if not raw_id.isdigit(): self.send_error(400); return
                entity_id = int(raw_id)
                events = []
                event_path = run_dir / "events.jsonl"
                if event_path.exists():
                    events = [
                        event for line in event_path.read_text(encoding="utf-8").splitlines()
                        if (event := json.loads(line)).get("entity_id") == entity_id
                    ]
                frames, previous_tick = [], -1
                for path in sorted((run_dir / "snapshots").glob("*.json")):
                    snapshot = json.loads(path.read_text(encoding="utf-8"))
                    entity = next((e for e in snapshot["entities"] if e["id"] == entity_id), None)
                    if entity is None: continue
                    tick = snapshot["tick"]
                    frames.append({
                        "tick": tick, "entity": entity,
                        "events": [e for e in events if previous_tick < e["tick"] <= tick],
                    })
                    previous_tick = tick
                    if not entity["alive"]: break
                if not frames: self.send_error(404); return
                data = json.dumps({"entity_id": entity_id, "frames": frames}).encode(); kind = "application/json; charset=utf-8"
            elif self.path.startswith("/api/snapshot/"):
                name = self.path.removeprefix("/api/snapshot/")
                if Path(name).name != name or not name.endswith(".json"): self.send_error(400); return
                try: data = (run_dir / "snapshots" / name).read_bytes()
                except FileNotFoundError: self.send_error(404); return
                kind = "application/json; charset=utf-8"
            else: self.send_error(404); return
            self.send_response(200); self.send_header("Content-Type", kind); self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(data)
        def log_message(self, format, *args): pass
    return Handler

def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only EVE-Alife Lupe")
    parser.add_argument("run_dir", type=Path); parser.add_argument("--port", type=int, default=8080); args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(args.run_dir.resolve()))
    print(f"Lupe: http://127.0.0.1:{args.port}"); server.serve_forever()

if __name__ == "__main__": main()
