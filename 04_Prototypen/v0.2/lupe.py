#!/usr/bin/env python3
"""Read-only Lupe für persistierte EVE-Beobachtungsdaten."""
from __future__ import annotations
import argparse, json, sqlite3, tempfile, zipfile, zlib
from collections import Counter, defaultdict
from threading import Lock
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from run_store import FORMAT_NAME, SCHEMA_VERSION

HTML = r'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EVE-Alife Lupe</title><style>
:root{--bg:#0d1210;--p:#151d19;--p2:#1b2620;--line:#34443a;--text:#e4eee7;--muted:#9bae9f;--green:#73dc8c;--amber:#e6bd68;--blue:#77b9e8;--red:#e17b72}*{box-sizing:border-box}body{font:15px/1.45 system-ui,sans-serif;background:var(--bg);color:var(--text);margin:0}main{max-width:1500px;margin:auto;padding:1.5rem}h1{margin:.1rem 0}.muted,.subtitle{color:var(--muted)}h2{margin-top:1.8rem}h3{margin:.4rem 0}.top,.metrics,.columns,.entities{display:grid;gap:.8rem}.top{grid-template-columns:1fr auto;align-items:end}.metrics{grid-template-columns:repeat(auto-fit,minmax(125px,1fr));margin:.8rem 0}.columns{grid-template-columns:1fr 1fr}.entities{grid-template-columns:repeat(auto-fit,minmax(430px,1fr))}.metric,.panel,.entity{background:var(--p);border:1px solid var(--line);border-radius:9px;padding:.8rem}.metric strong{color:var(--green);display:block;font-size:1.3rem}.record strong{color:var(--amber)}[data-tip]{text-decoration:underline dotted;text-underline-offset:3px;cursor:help}.help{border-left:3px solid var(--green);padding:.6rem .8rem;background:var(--p)}select,button{background:var(--p2);color:var(--text);border:1px solid var(--line);padding:.45rem .65rem;border-radius:5px}button{cursor:pointer}button:hover{border-color:var(--green)}canvas{width:100%;background:#111a15;border:1px solid var(--line);border-radius:6px}.entity.dead{opacity:.6}.entity>summary{cursor:pointer;font-weight:650;list-style:none}.badge{border-radius:999px;padding:.12rem .5rem;margin-left:.4rem;font-size:.8rem;background:#294131;color:#b9efc5}.dead .badge{background:#432b29;color:#f0b2ac}.entity-meta{color:var(--muted);margin:.5rem 0}.fragment-list{display:flex;gap:.5rem;flex-wrap:wrap;margin:.45rem 0 .8rem}.fragment{background:#101713;border:1px solid var(--line);border-radius:6px;padding:.4rem .55rem;min-width:180px;flex:1}.fragment b{color:var(--blue)}.fragment .missing{color:var(--red)}table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{padding:.35rem .45rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--muted)}.scroll{max-height:310px;overflow:auto}.empty{color:var(--muted);font-style:italic}.signal{color:var(--blue)}.source{color:var(--amber);font-size:.82rem}.edges,code{font-family:ui-monospace,monospace}code{color:#a9ebb7;background:#0d1511;padding:.1rem .3rem;border-radius:3px}.error{color:var(--red)}#dashboard{border-color:#66552f;margin-bottom:1rem}.record-list{columns:2;column-gap:2rem;margin:.5rem 0;padding-left:1.4rem}.record-list li{break-inside:avoid;margin:.3rem 0}.record-list b{color:var(--amber)}#replay{border-color:var(--green);margin:1.2rem 0}#replay[hidden]{display:none}.replay-controls,.timeline-controls{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}.replay-controls input[type=range]{flex:1;min-width:220px}.events-log{max-height:310px;overflow:auto;background:#0d1511;border-radius:6px;padding:.5rem 1.8rem}.events-log li{margin:.25rem 0}.life-button{margin:.15rem 0 .7rem}#chart{cursor:crosshair;touch-action:none}#timeline-panel{margin:1rem 0;border-color:#365d43}.selection-label{color:var(--green);font-weight:650}.activity-grid{display:grid;grid-template-columns:minmax(260px,.7fr) minmax(420px,1.3fr);gap:.8rem}@media(max-width:850px){.columns,.top,.activity-grid{grid-template-columns:1fr}.entities{grid-template-columns:1fr}.record-list{columns:1}main{padding:.8rem}}
 #run-status{margin:.8rem 0;border-color:var(--green);font-size:1.15rem}#run-status strong{font-size:1.4rem;color:var(--green)}.activity-grid{margin-bottom:1.2rem}.genome-diagram-toolbar{display:flex;justify-content:flex-end;margin:.35rem 0}.genome-diagram-link{cursor:pointer}.genome-graph{min-width:760px;width:100%;max-height:760px;background:#101713;border:1px solid var(--line);border-radius:7px}.genome-diagram-link:hover .genome-graph{border-color:var(--green);box-shadow:0 0 0 2px rgba(115,220,140,.12)}.graph-edges path{stroke:#668675;stroke-width:1.4;fill:none;opacity:.7}.graph-edges marker path{fill:var(--blue);stroke:none}.graph-nodes rect{fill:#1b3024;stroke:var(--green);stroke-width:1.2}.graph-nodes text{fill:var(--text);font:11px ui-monospace,monospace;text-anchor:middle}.graph-nodes text.small{fill:var(--amber);font-size:9px}
#live-soup{margin:1rem 0;border-color:#315b45;position:relative}#live-soup canvas{height:360px;background:radial-gradient(circle at center,#18251e,#090e0b)}#live-soup-head{display:flex;justify-content:space-between;align-items:center}#live-soup-numbers{color:var(--green);font:700 1.05rem ui-monospace,monospace}.live-legend{display:flex;gap:.55rem;flex-wrap:wrap;color:var(--muted);font-size:.82rem;margin-top:.55rem}.live-legend label{display:flex;align-items:center;gap:.28rem;border:1px solid var(--line);border-radius:999px;padding:.22rem .55rem;cursor:pointer;background:#101713}.live-legend label:has(input:not(:checked)){opacity:.38}.live-legend input{accent-color:var(--green);margin:0}.live-legend i{display:inline-block;width:.65rem;height:.65rem;border-radius:50%}.soup-tooltip{position:absolute;z-index:5;pointer-events:none;background:#0b120e;border:1px solid var(--green);border-radius:7px;padding:.45rem .6rem;box-shadow:0 5px 20px #0009;color:var(--text);font-size:.86rem}.soup-tooltip b{color:var(--green)}.entity.soup-focus{border-color:#fff;box-shadow:0 0 0 3px #73dc8c88,0 0 28px #73dc8c44}
.soup-tooltip{left:1.6rem!important;top:auto!important;bottom:3.2rem;max-width:min(28rem,calc(100% - 3.2rem))}
</style></head><body><main><div class="top"><div><h1>EVE-Alife · Lupe</h1><div class="subtitle">Read-only-Beobachtung eines laufenden oder archivierten Experiments</div></div><label>Zeitpunkt ansehen<br><select id="snap"><option value="latest">aktuell</option></select></label></div>
<section id="run-status" class="panel"><strong>Status wird geladen …</strong></section>
<section id="live-soup" class="panel"><div id="live-soup-head"><h2>Die Suppe lebt</h2><span id="live-soup-numbers">Tick — · 0 Amöben</span></div><canvas id="soup-canvas" width="1400" height="360"></canvas><div class="live-legend"><span><i style="background:#73dc8c"></i>Amöbe</span><span><i style="background:#77b9e8"></i>Lesen</span><span><i style="background:#e6bd68"></i>Schreiben</span><span><i style="background:#b98bea"></i>Blase/Schalter</span><span><i style="background:#fff"></i>Geburt</span><span><i style="background:#e17b72"></i>Tod</span></div></section>
<p class="help">Die Buchstaben bezeichnen Teile einer Amöbe. Fahre über <span data-tip title="Kurzerklärung direkt am Begriff">unterstrichene Begriffe</span>. Die Lupe kann den Lauf nicht verändern.</p><section id="dashboard" class="panel"><h2>Chronik des Biotops</h2><p class="muted">Laufübergreifende Bilanz aller gespeicherten Experimente. Ein Massenaussterben zählt, wenn in einem Lauf keine Amöbe überlebt.</p><div id="global-metrics" class="metrics"></div><div class="columns"><div><h3>Lebensrekorde</h3><div id="life-records" class="metrics"></div></div><div><h3>Letzte Läufe</h3><div id="run-history" class="scroll"></div></div></div><h3>Rekorde der Amöben</h3><ul id="biotope-records" class="record-list"></ul></section>
<div id="meta" class="metrics"></div><section id="replay" class="panel" hidden><div class="top"><div><h2 id="replay-title">Lebensfilm</h2><p id="replay-position" class="muted"></p></div><button onclick="closeReplay()">Schließen</button></div><div class="replay-controls"><button id="replay-prev" title="Ein Bild zurück">◀</button><button id="replay-play">▶ Abspielen</button><button id="replay-next" title="Ein Bild weiter">▶|</button><input id="replay-slider" type="range" min="0" value="0"><label>Tempo <select id="replay-speed"><option value="1800">langsam</option><option value="800" selected>normal</option><option value="300">schnell</option></select></label></div><h3>Was in diesem Schritt geschah</h3><ol id="replay-events" class="events-log"></ol><div id="replay-state"></div></section><section id="timeline-panel" class="panel"><div class="top"><div><h2>Population und Zeitfilter</h2><p class="muted">Klicken wählt einen Tick. Ziehen markiert einen Zeitraum. Die Auswahl steuert alle Ansichten darunter.</p></div><button id="timeline-all">Gesamten Lauf zeigen</button></div><canvas id="chart" width="1400" height="190"></canvas><div class="timeline-controls"><span id="selection-label" class="selection-label">Gesamter Lauf</span><span id="selection-help" class="muted"></span></div></section><section class="activity-grid"><div class="panel"><h2>Auswahl</h2><div id="selection-stats" class="metrics"></div></div><div class="panel"><h2>Was geschah?</h2><ol id="selection-events" class="events-log"></ol></div></section><section class="panel"><div class="top"><div><h2>Umweltkontakte</h2><p class="muted">Nur Kontakte innerhalb der gewählten Zeit und von den angezeigten Amöben.</p></div><label>Amöbe<br><select id="env-entity"><option value="all">alle</option></select></label></div><div id="env-stats" class="metrics"></div><canvas id="contacts" width="1400" height="140"></canvas><p class="muted">Jeder Balken ist eine besuchte Adresse; Höhe = Zahl der Zugriffe. Blau bedeutet Lesen, Orange Schreiben.</p><div id="env-recent" class="scroll"></div></section><h2>Amöben der Auswahl</h2><p class="muted">Gezeigt werden Amöben, die im gewählten Zeitpunkt lebten oder den gewählten Zeitraum berührten. Ihr Zustand stammt vom Ende der Auswahl.</p><section id="entities" class="entities"></section>
</main><script>
const select=document.querySelector('#snap'),box=document.querySelector('#entities'),metaBox=document.querySelector('#meta'),contactCanvas=document.querySelector('#contacts'),chartCanvas=document.querySelector('#chart'),replayBox=document.querySelector('#replay'),replaySlider=document.querySelector('#replay-slider'),envSelect=document.querySelector('#env-entity'),esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let replayFrames=[],replayIndex=0,replayTimer=null,environmentEvents=[],activityEvents=[],timelinePoints=[],currentTick=0,selection={mode:'all',start:0,end:0},dragStart=null,visibleIds=new Set();const genomeCache=new Map(),names=['Tom','Erna','Ada','Bruno','Clara','Dario','Emmi','Fritz','Greta','Hugo','Ida','Juri','Karla','Lino','Maja','Nils','Olga','Piet','Rosa','Sam','Tilda','Uwe','Vera','Willi','Xenia','Yara','Zeno','Alma','Ben','Cleo','Dora','Enno'],nameOf=id=>names[(id-1)%names.length]+(id>names.length?' '+(Math.floor((id-1)/names.length)+1):''),amoeba=e=>`${esc(e.name||nameOf(e.id))}${e.ram_position===undefined?'':` <span class="muted">@RAM ${e.ram_position}</span>`}`;
const nodeHelp={CONST:'Erbliche konstante Zahl',S_READ:'Liest die eigene Energie S',Z_READ:'Liest eine Z-Zelle',Z_WRITE:'Schreibt dauerhaft nach Z',RAM_READ:'Liest eine Zelle der gemeinsamen RAM-Suppe',RAM_WRITE:'Schreibt in die gemeinsame RAM-Suppe',MEM_READ:'Liest die eigene Membran',MEM_WRITE:'Schreibt in die eigene Membran',ADD:'Addiert zwei Werte',SUB:'Subtrahiert b von a',XOR:'Bitweises Exklusiv-Oder',EQ:'Liefert 1 bei Gleichheit, sonst 0',GATE:'Leitet einen Wert nur bei einer Bedingung ungleich 0 weiter',PAUSE:'Verbraucht die Eingabe ohne weitere Wirkung'};
const sig=s=>s?`<span class="signal">${esc(s.value)}</span><br><span class="source">Quelle: ${esc((s.sources||[]).join(' + ')||'—')}</span>`:'<span class="empty">leer</span>';
function nodes(g){return g?`<div class="scroll"><table><thead><tr><th>ID</th><th>Funktionspunkt</th><th>Erblicher Wert</th></tr></thead><tbody>${g.nodes.map(n=>`<tr><td>${n.id}</td><td><code data-tip title="${esc(nodeHelp[n.kind]||'Primitiver Funktionspunkt')}">${esc(n.kind)}</code></td><td>${n.constant===null?'—':esc(n.constant)}</td></tr>`).join('')}</tbody></table></div>`:'<p class="empty">Im älteren Snapshot nicht enthalten.</p>'}
function edges(g){return g&&g.edges.length?`<div class="scroll"><table class="edges"><thead><tr><th>Quelle</th><th></th><th>Ziel</th></tr></thead><tbody>${g.edges.map(p=>`<tr><td>#${p.source}.${esc(p.source_port)}</td><td>→</td><td>#${p.target}.${esc(p.target_port)}</td></tr>`).join('')}</tbody></table></div>`:'<p class="empty">Keine P-Kanten oder keine Details.</p>'}
function genomeSvg(g){if(!g||!g.nodes.length)return'<p>Kein Genomdiagramm verfügbar.</p>';const cols=6,dx=145,dy=92,w=cols*dx,h=Math.ceil(g.nodes.length/cols)*dy+35,pos=new Map(g.nodes.map((n,i)=>[n.id,{x:75+(i%cols)*dx,y:48+Math.floor(i/cols)*dy}]));const lines=g.edges.map(e=>{const a=pos.get(e.source),b=pos.get(e.target);return a&&b?`<path d="M${a.x} ${a.y+21} L${b.x} ${b.y-21}" marker-end="url(#arrow)"/><title>#${e.source}.${esc(e.source_port)} → #${e.target}.${esc(e.target_port)}</title>`:''}).join(''),boxes=g.nodes.map(n=>{const p=pos.get(n.id),value=n.constant===null?'':` · ${n.constant}`;return`<g><rect x="${p.x-55}" y="${p.y-21}" width="110" height="42" rx="7"/><text x="${p.x}" y="${p.y-3}">#${n.id} ${esc(n.kind)}</text><text class="small" x="${p.x}" y="${p.y+13}">${esc(value)}</text></g>`}).join('');return`<svg class="genome-graph" viewBox="0 0 ${w} ${h}" role="img" aria-label="Gerichteter Genomgraph"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z"/></marker></defs><g class="graph-edges">${lines}</g><g class="graph-nodes">${boxes}</g></svg>`}
function openGenomeDiagram(id){const g=genomeCache.get(id);if(!g)return;const popup=window.open('','eve-genome-'+id,'popup,width=1280,height=900,resizable=yes,scrollbars=yes');if(!popup)return alert('Das separate Genomfenster wurde vom Browser blockiert.');popup.document.open();popup.document.write(`<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Genom · Amöbe #${id}</title><style>body{margin:0;padding:1.2rem;background:#0d1210;color:#e4eee7;font:15px system-ui}h1{margin-top:0}.genome-graph{width:100%;min-width:1000px;background:#101713;border:1px solid #34443a;border-radius:8px}.graph-edges path{stroke:#668675;stroke-width:1.5;fill:none}.graph-edges marker path{fill:#77b9e8;stroke:none}.graph-nodes rect{fill:#1b3024;stroke:#73dc8c;stroke-width:1.2}.graph-nodes text{fill:#e4eee7;font:11px ui-monospace,monospace;text-anchor:middle}.graph-nodes text.small{fill:#e6bd68;font-size:9px}</style></head><body><h1>Genom · Amöbe #${id}</h1>${genomeSvg(g)}</body></html>`);popup.document.close();popup.focus()}
function genomeDiagram(g,id){if(!g||!g.nodes.length)return'<p class="empty">Kein Genomdiagramm verfügbar.</p>';genomeCache.set(id,g);return`<h3>Genomdiagramm</h3><div class="genome-diagram-toolbar"><button onclick="openGenomeDiagram(${id})">↗ In eigenem Fenster öffnen</button></div><div class="scroll genome-diagram-link" onclick="openGenomeDiagram(${id})" title="Für große Ansicht anklicken">${genomeSvg(g)}</div>`}
function kvals(k){const a=Object.entries(k||{});return a.length?`<table><thead><tr><th>Port</th><th>Wert</th></tr></thead><tbody>${a.map(([p,s])=>`<tr><td><code>${esc(p)}</code></td><td>${sig(s)}</td></tr>`).join('')}</tbody></table>`:'<p class="empty">K ist gerade leer.</p>'}
function zvals(z){return z?`<div class="scroll"><table><thead><tr><th>Adresse</th><th>Inhalt</th></tr></thead><tbody>${z.map((s,i)=>`<tr><td>${i}</td><td>${sig(s)}</td></tr>`).join('')}</tbody></table></div>`:'<p class="empty">Keine Details.</p>'}
function genomeFragments(g){if(!g)return[];const byId=new Map(g.nodes.map(n=>[n.id,n])),links=new Map(g.nodes.map(n=>[n.id,new Set()]));g.edges.forEach(p=>{links.get(p.source)?.add(p.target);links.get(p.target)?.add(p.source)});const unseen=new Set(byId.keys()),out=[];while(unseen.size){const first=unseen.values().next().value,stack=[first],ids=[];unseen.delete(first);while(stack.length){const id=stack.pop();ids.push(id);for(const next of links.get(id)||[])if(unseen.delete(next))stack.push(next)}const idSet=new Set(ids),partEdges=g.edges.filter(p=>idSet.has(p.source)&&idSet.has(p.target)),kinds=ids.map(id=>byId.get(id).kind),writes=ids.filter(id=>byId.get(id).kind==='MEM_WRITE'),social=writes.some(id=>{const ports=new Set(partEdges.filter(p=>p.target===id).map(p=>p.target_port));return['offset','slot','value'].every(p=>ports.has(p))}),caps=[];if(social)caps.push('Partnersuche & Handshake');else if(writes.length)caps.push('unvollständiges MEM_WRITE');if(kinds.includes('RAM_READ'))caps.push('RAM-Erkundung');if(kinds.includes('RAM_WRITE'))caps.push('RAM-Markierung');if(!caps.length)caps.push('unbenanntes Fragment');out.push({ids:ids.sort((a,b)=>a-b),edges:partEdges.length,kinds:[...new Set(kinds)].sort(),label:caps.join(' + '),social})}return out.sort((a,b)=>a.ids[0]-b.ids[0])}
function fragmentView(g){const fs=genomeFragments(g),social=fs.some(f=>f.social);return `<h3 data-tip title="Zusammenhängende Netzkomponenten werden bei der Rekombination als unteilbare erbliche Einheiten behandelt">Vererbbare Netzfragmente · ${fs.length}</h3><div class="fragment-list">${fs.map((f,i)=>`<div class="fragment"><b>Fragment ${i+1} · ${esc(f.label)}</b><br><span class="muted">${f.ids.length} F · ${f.edges} P · Knoten ${f.ids.join(', ')}</span><br><span class="source">${esc(f.kinds.join(' · '))}</span></div>`).join('')}</div><div class="entity-meta">Strukturell ausführbares MEM_WRITE: <b class="${social?'':'missing'}">${social?'vorhanden':'fehlt · Membranwert maximal 9'}</b>. Das garantiert noch keinen gültigen Partner oder sozialen Erfolg.</div>`}
function card(e,open,withReplay=true){const s0=e.start_energy??e.energy,fs=genomeFragments(e.genome),knockers=(e.knockers||[]).filter(Boolean);return `<details class="entity ${e.alive?'':'dead'}" data-entity="${e.id}" ${open.has(String(e.id))?'open':''}><summary>${amoeba(e)} <span class="muted">#${e.id}</span><span class="badge">${e.alive?'lebend':'tot'}</span></summary><div class="entity-meta"><span data-tip title="Aktuelle Energie">S ${e.energy.toFixed(2)}</span> · <span data-tip title="Energie bei der eigenen Geburt; muss nach einem Elternbeitrag überschritten bleiben">S₀ ${s0.toFixed(2)}</span> · geboren Tick ${e.born_at} · Eltern ${e.parents.join(', ')||'—'} · Partner ${e.partners.filter(x=>x!==null).join(', ')||'—'} · Klopfer ${knockers.join(', ')||'—'}</div>${withReplay?`<button class="life-button" onclick="startReplay(${e.id})">▶ ${amoeba(e)}s Leben abspielen</button>`:''}<div class="metrics"><div class="metric"><span data-tip title="Funktionspunkt-Instanzen">F</span><strong>${e.n_f}</strong></div><div class="metric"><span data-tip title="Datenflusskanten">P</span><strong>${e.n_p}</strong></div><div class="metric"><span data-tip title="Genomgröße F + P">G-Größe</span><strong>${e.n_g}</strong></div><div class="metric"><span data-tip title="Zusammenhängende vererbbare Netzkomponenten">Fragmente</span><strong>${fs.length}</strong></div><div class="metric"><span data-tip title="Erbliche Basisaktivität">A₀</span><strong>${e.activity_base}</strong></div><div class="metric"><span data-tip title="Erbliche Klingelkapazität">Nₖ</span><strong>${e.genome.knock_capacity||1}</strong></div><div class="metric"><span data-tip title="Erbliche Mindestbindungszeit">Tₚ</span><strong>${e.genome.bond_ticks||1}</strong></div></div>${genomeDiagram(e.genome,e.id)}${fragmentView(e.genome)}<div class="columns"><section><h3 data-tip title="Konkrete erbliche Rechenbausteine">G · Funktionspunkte</h3>${nodes(e.genome)}</section><section><h3 data-tip title="Gerichtete Verbindungen im Genom">P · Kanten</h3>${edges(e.genome)}</section><section><h3 data-tip title="Flüchtig belegte Eingangsports">K · Kurzzeit (${e.k_slots})</h3>${kvals(e.k)}</section><section><h3 data-tip title="Dauerhafter individueller Speicher">Z · Zustand (${e.z_used}/${(e.z||[]).length})</h3>${zvals(e.z)}</section></div></details>`}
function describe(e){const n=e.node_id===undefined?'':`#${e.node_id} `;switch(e.kind){case'birth':return`Geburt mit ${e.energy} Energie; Eltern: ${(e.parents||[]).join(', ')||'Startpopulation'}`;case'birth_rejected':return e.reason==='parent_surplus_required'?`Keine Geburt: Nach dem Beitrag bliebe S nicht über der eigenen Geburtsenergie S₀ (${e.start_energy.toFixed(2)})`:`Keine Geburt: angeboten ${e.offered_energy.toFixed(2)}, für die Mindestlaufzeit benötigt ${e.required_energy.toFixed(2)}`;case'death':return`Tod: ${e.reason==='standby_unaffordable'?'Standby nicht mehr finanzierbar':e.reason}`;case'standby':return`Standby kostet ${e.cost.toFixed(2)}${e.aging_cost?` (davon Alter ${e.aging_cost.toFixed(2)})`:''}; S ${e.energy_before.toFixed(2)} → ${e.energy_after.toFixed(2)}`;case'node_fire':return`${n}${e.node_kind} wird ausgeführt; Kosten ${e.cost.toFixed(2)}, S danach ${e.energy_after.toFixed(2)}`;case'gate':return`${n}GATE ${e.opened?'öffnet':'sperrt'} bei Bedingung ${e.condition}; Wert ${e.value}`;case'knock':return`klopft bei Amöbe #${e.target_id} an${e.overwritten_knocker?`; verdrängt Klopfer #${e.overwritten_knocker}`:''}`;case'ram_read':if(e.discovery_type==='entity')return`Lebende Amöbe #${e.target_id} gefunden; Energie +${e.reward.toFixed(2)}`;if(e.discovery_type==='invitation')return`Einladung von Amöbe #${e.target_id} erkannt; Energie +${e.reward.toFixed(2)}`;if(e.discovery_type==='life_state')return`Membranwert ${e.value} bei Amöbe #${e.target_id} erkannt${e.value===0?' (tot)':''}; Energie +${e.reward.toFixed(2)}`;return`${e.virtual?'Membran':'RAM'}[${e.address}] gelesen → ${e.value}${e.reward>0?`; neue externe Veränderung, Energie +${e.reward.toFixed(3)}`:e.self_origin?'; eigener Ursprung, keine Energie':e.changed===false?'; unverändert, keine Energie':''}`;case'ram_write':return`RAM[${e.address}] beschrieben → ${e.value}`;case'z_write':return`Z[${e.address}] ← ${e.value}; dauerhaft gespeichert, keine direkte Energie`;case'mem_write':return e.value===0?`Partnerslot ${e.slot} geleert: Amöbe #${e.cleared_partner} wurde tot beobachtet`:`Partnerslot ${e.slot} ← gefundene Amöbe #${e.value}`;case'mem_write_rejected':return`Partnerslot-Schreiben abgewiesen: Amöbe #${e.value} wurde nicht lebend mit passender Herkunft gefunden`;case'reproduction_cost':return`Geburtsbeitrag ${e.cost}; Kind #${e.child_id}`;case'signal':return`Signal ${e.value}: #${e.source} → #${e.target}`;default:return e.kind}}
function showReplay(i){if(!replayFrames.length)return;replayIndex=Math.max(0,Math.min(i,replayFrames.length-1));const f=replayFrames[replayIndex];replaySlider.value=replayIndex;document.querySelector('#replay-position').textContent=`Tick ${f.tick} · Bild ${replayIndex+1} von ${replayFrames.length}`;document.querySelector('#replay-events').innerHTML=f.events.length?f.events.map(e=>`<li>${esc(describe(e))}</li>`).join(''):'<li class="empty">In diesem gespeicherten Intervall kein Ereignis.</li>';document.querySelector('#replay-state').innerHTML=card(f.entity,new Set([String(f.entity.id)]),false)}
async function startReplay(id){stopReplay();const data=await fetch(`/api/entity/${id}/life`).then(r=>r.json());replayFrames=data.frames||[];if(!replayFrames.length){alert('Für diese Amöbe sind keine Replay-Snapshots vorhanden.');return}const e=replayFrames[0].entity;document.querySelector('#replay-title').textContent=`Lebensfilm · ${e.name||'Amöbe'} #${id}`;replaySlider.max=replayFrames.length-1;replayBox.hidden=false;showReplay(0);replayBox.scrollIntoView({behavior:'smooth'})}
function stopReplay(){if(replayTimer)clearInterval(replayTimer);replayTimer=null;document.querySelector('#replay-play').textContent='▶ Abspielen'}function closeReplay(){stopReplay();replayBox.hidden=true}function toggleReplay(){if(replayTimer){stopReplay();return}document.querySelector('#replay-play').textContent='⏸ Pause';replayTimer=setInterval(()=>{if(replayIndex>=replayFrames.length-1){stopReplay();return}showReplay(replayIndex+1)},Number(document.querySelector('#replay-speed').value))}
document.querySelector('#replay-prev').onclick=()=>{stopReplay();showReplay(replayIndex-1)};document.querySelector('#replay-next').onclick=()=>{stopReplay();showReplay(replayIndex+1)};document.querySelector('#replay-play').onclick=toggleReplay;replaySlider.oninput=()=>{stopReplay();showReplay(Number(replaySlider.value))};document.querySelector('#replay-speed').onchange=()=>{if(replayTimer){stopReplay();toggleReplay()}};
const maxTick=()=>timelinePoints.length?timelinePoints[timelinePoints.length-1].tick:0,tickFromPointer=e=>{const r=chartCanvas.getBoundingClientRect(),ratio=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)),raw=ratio*maxTick();return timelinePoints.reduce((best,p)=>Math.abs(p.tick-raw)<Math.abs(best-raw)?p.tick:best,timelinePoints[0]?.tick||0)},selectionRange=()=>selection.mode==='all'?[0,maxTick()]:[selection.start,selection.end];
function drawTimeline(){const points=timelinePoints,g=chartCanvas.getContext('2d'),w=chartCanvas.width,h=chartCanvas.height,maxAlive=Math.max(1,...points.map(q=>q.alive));g.clearRect(0,0,w,h);g.strokeStyle='#34443a';g.beginPath();g.moveTo(0,h-18);g.lineTo(w,h-18);g.stroke();g.strokeStyle='#73dc8c';g.lineWidth=3;g.beginPath();points.forEach((p,i)=>{const x=p.tick*w/Math.max(1,maxTick()),y=h-18-p.alive*(h-30)/maxAlive;i?g.lineTo(x,y):g.moveTo(x,y)});g.stroke();if(selection.mode!=='all'){const a=selection.start*w/Math.max(1,maxTick()),b=selection.end*w/Math.max(1,maxTick());g.fillStyle='rgba(119,185,232,.22)';g.fillRect(Math.min(a,b),0,Math.max(3,Math.abs(b-a)),h);g.strokeStyle='#77b9e8';g.lineWidth=2;g.beginPath();g.moveTo(a,0);g.lineTo(a,h);if(a!==b){g.moveTo(b,0);g.lineTo(b,h)}g.stroke()}g.fillStyle='#9bae9f';g.font='24px system-ui';g.fillText('0',6,h-3);const label=String(maxTick()),tw=g.measureText(label).width;g.fillText(label,w-tw-6,h-3)}
function drawEnvironment(){const chosen=envSelect.value,[start,end]=selectionRange(),events=environmentEvents.filter(e=>e.tick>=start&&e.tick<=end&&visibleIds.has(e.entity_id)&&(chosen==='all'||String(e.entity_id)===chosen));const grouped=new Map();events.forEach(e=>{const a=grouped.get(e.address)||{reads:0,writes:0};e.kind==='ram_read'?a.reads++:a.writes++;grouped.set(e.address,a)});const items=[...grouped.entries()].sort((a,b)=>a[0]-b[0]),g=contactCanvas.getContext('2d');g.clearRect(0,0,contactCanvas.width,contactCanvas.height);const max=Math.max(1,...items.map(([,v])=>v.reads+v.writes)),w=Math.max(2,contactCanvas.width/Math.max(1,items.length));items.forEach(([address,v],i)=>{const readHeight=v.reads*120/max,writeHeight=v.writes*120/max,x=i*w,width=w-1;g.fillStyle='#77b9e8';g.fillRect(x,contactCanvas.height-readHeight,width,readHeight);g.fillStyle='#e6bd68';g.fillRect(x,contactCanvas.height-readHeight-writeHeight,width,writeHeight)});const reads=events.filter(e=>e.kind==='ram_read').length,writes=events.length-reads,reward=events.reduce((sum,e)=>sum+(e.reward||0),0);document.querySelector('#env-stats').innerHTML=`<div class="metric">Adressen<strong>${items.length}</strong></div><div class="metric">Lesezugriffe<strong>${reads}</strong></div><div class="metric">Schreibzugriffe<strong>${writes}</strong></div><div class="metric">Energie aus RAM<strong>${reward.toFixed(2)}</strong></div>`;const recent=events.slice(-12).reverse();document.querySelector('#env-recent').innerHTML=recent.length?`<table><thead><tr><th>Tick</th><th>Amöbe</th><th>Zugriff</th><th>Adresse</th><th>Wert</th><th>Energie</th></tr></thead><tbody>${recent.map(e=>`<tr><td>${e.tick}</td><td>#${e.entity_id}</td><td>${e.kind==='ram_read'?'lesen':'schreiben'}</td><td>RAM[${e.address}]</td><td>${e.value}</td><td>${e.reward?`+${e.reward.toFixed(2)}`:'—'}</td></tr>`).join('')}</tbody></table>`:'<p class="empty">In der Auswahl kein RAM-Kontakt.</p>'}
async function runStatus(){const r=await fetch('/api/status',{cache:'no-store'}).then(x=>x.json()),label=r.status==='running'?'● CURRENTLY EVOLVING':r.end_reason==='natural_extinction'?'○ EXTINCT':'○ TICK LIMIT REACHED',mode=r.mode==='open'?'offener Run':`begrenzt auf ${r.tick_limit} Ticks`;document.querySelector('#run-status').innerHTML=`<strong>${label}</strong><div class="metrics"><div class="metric">Tick<strong>${Number(r.current_tick).toLocaleString()}</strong></div><div class="metric">Population<strong>${Number(r.population).toLocaleString()}</strong></div><div class="metric">Modus<strong>${mode}</strong></div><div class="metric">Run-ID<strong style="font-size:.75rem">${esc(r.run_id)}</strong></div></div>`}
function lifeRecord(label,r){return r?`<div class="metric record">${label}<strong>${esc(r.name)} · ${r.lifespan} Ticks</strong><span class="muted">Amöbe #${r.entity_id} aus Lauf ${r.run_number}</span></div>`:`<div class="metric">${label}<strong>—</strong><span class="muted">Noch kein abgeschlossenes Leben</span></div>`}
function recordCard(label,r,value,detail=''){return r?`<li>${label}: <b>${esc(r.name)} · ${value}</b> <span class="muted">(#${r.entity_id}, Lauf ${r.run_number}${detail?' · '+detail:''})</span></li>`:`<li>${label}: <span class="muted">noch nicht beobachtet</span></li>`}
async function dashboard(){const d=await fetch('/api/dashboard',{cache:'no-store'}).then(r=>r.json());document.querySelector('#global-metrics').innerHTML=`<div class="metric">Massenaussterben<strong>${d.mass_extinctions}</strong></div><div class="metric">Erzeugte Nachkommen<strong>${d.offspring}</strong></div><div class="metric">Gewonnene Energie<strong>${d.energy_gained.toFixed(2)}</strong></div><div class="metric">Gespeicherte Läufe<strong>${d.runs}</strong></div>`;document.querySelector('#life-records').innerHTML=lifeRecord('Kürzestes Leben',d.shortest_life)+lifeRecord('Längstes Leben',d.longest_life);document.querySelector('#run-history').innerHTML=d.history.length?`<table><thead><tr><th>Lauf</th><th>Tick</th><th>Status</th><th>Nachkommen</th><th>Energie</th></tr></thead><tbody>${d.history.slice(0,5).map(r=>`<tr><td>${r.run_number}</td><td>${r.tick}</td><td>${r.mass_extinction?'ausgestorben':r.population_alive+' lebend'}</td><td>${r.offspring}</td><td>${r.energy_gained.toFixed(2)}</td></tr>`).join('')}</tbody></table>`:'<p class="empty">Noch keine Läufe.</p>';const r=d.records;document.querySelector('#biotope-records').innerHTML=recordCard('Größtes Genom',r.largest_genome,r.largest_genome?r.largest_genome.value+' G':'',r.largest_genome?`F ${r.largest_genome.n_f} + P ${r.largest_genome.n_p}`:'')+recordCard('Höchste Energie',r.highest_energy,r.highest_energy?r.highest_energy.value.toFixed(2):'')+recordCard('Meiste direkte Kinder',r.most_direct_children,r.most_direct_children?r.most_direct_children.value:'')+recordCard('Größte Nachkommenschaft',r.most_descendants,r.most_descendants?r.most_descendants.value:'')+recordCard('Tiefste Generation',r.deepest_generation,r.deepest_generation?'Generation '+r.deepest_generation.value:'')+recordCard('Älteste Amöbe',r.oldest_entity,r.oldest_entity?r.oldest_entity.value+' Ticks':'',r.oldest_entity?(r.oldest_entity.alive?'lebend':'verstorben'):'')+recordCard('Meiste RAM-Adressen',r.most_ram_addresses,r.most_ram_addresses?r.most_ram_addresses.value:'')+recordCard('Meiste RAM-Energie',r.most_ram_energy,r.most_ram_energy?r.most_ram_energy.value.toFixed(2):'')+recordCard('Bester Informationsproduzent',r.best_information_producer,r.best_information_producer?r.best_information_producer.value.toFixed(2):'')+recordCard('Meiste Amöbenfunde',r.most_entity_discoveries,r.most_entity_discoveries?r.most_entity_discoveries.value:'')+recordCard('Meiste erkannte Einladungen',r.most_invitations,r.most_invitations?r.most_invitations.value:'')+recordCard('Meiste RAM-Schreibvorgänge',r.most_ram_writes,r.most_ram_writes?r.most_ram_writes.value:'')}
async function dashboardWithFertility(){await dashboard();const d=await fetch('/api/dashboard',{cache:'no-store'}).then(r=>r.json());document.querySelector('#run-history').innerHTML=d.history.length?`<table><thead><tr><th>Lauf</th><th>Tick</th><th>Status</th><th>Nachkommen</th><th>Unfruchtbar</th><th>Energie</th></tr></thead><tbody>${d.history.slice(0,5).map(r=>`<tr><td>${r.run_number}</td><td>${r.tick}</td><td>${r.mass_extinction?'ausgestorben':r.population_alive+' lebend'}</td><td>${r.offspring}</td><td>${r.infertile_offspring}</td><td>${r.energy_gained.toFixed(2)}</td></tr>`).join('')}</tbody></table>`:'<p class="empty">Noch keine Läufe.</p>'}
const soupCanvas=document.querySelector('#soup-canvas'),soupCtx=soupCanvas.getContext('2d');
let liveCursor=0,liveRamSize=65536,liveEntities=[],liveToys={},soupPulses=[],livePolling=false,hoveredSoupEntity=null,historicalSoup=false,soupHistoryTimers=[];
const soupTooltip=document.createElement('div');soupTooltip.className='soup-tooltip';soupTooltip.hidden=true;document.querySelector('#live-soup').appendChild(soupTooltip);
const soupVisible={amoebas:true,toys:true,reads:true,writes:true,environment:true,births:true,deaths:true},legendItems=[['amoebas','#73dc8c','Amöben'],['toys','#89948c','Spielzeuge'],['reads','#77b9e8','Lesen'],['writes','#e6bd68','Schreiben'],['environment','#b98bea','Umwelt'],['births','#ffffff','Geburten'],['deaths','#e17b72','Tode']];document.querySelector('.live-legend').innerHTML=legendItems.map(([key,color,label])=>`<label><input type="checkbox" data-soup-filter="${key}" checked><i style="background:${color}"></i>${label}</label>`).join('');document.querySelectorAll('[data-soup-filter]').forEach(input=>input.addEventListener('change',()=>{soupVisible[input.dataset.soupFilter]=input.checked}));
const soupPoint=(address,lane=0)=>{const a=(Number(address||0)/Math.max(1,liveRamSize))*Math.PI*2-Math.PI/2,cx=soupCanvas.width/2,cy=soupCanvas.height/2,rx=soupCanvas.width*.455+lane*13,ry=soupCanvas.height*.34+lane*9;return[cx+Math.cos(a)*rx,cy+Math.sin(a)*ry]};
function soupPulse(address,color,size,type,grow=20,entityIds=[]){if(address===undefined)return;soupPulses.push({address,color,size,type,grow,entityIds,born:performance.now()});if(soupPulses.length>600)soupPulses.splice(0,soupPulses.length-600)}
function drawSoup(now){const g=soupCtx,w=soupCanvas.width,h=soupCanvas.height,cx=w/2,cy=h/2,rx=w*.455,ry=h*.34;g.clearRect(0,0,w,h);g.strokeStyle='#34443a';g.lineWidth=18;g.beginPath();g.ellipse(cx,cy,rx,ry,0,0,Math.PI*2);g.stroke();g.strokeStyle='#1f3328';g.lineWidth=2;for(let i=0;i<24;i++){const a=i*Math.PI/12;g.beginPath();g.moveTo(cx+Math.cos(a)*(rx-15),cy+Math.sin(a)*(ry-10));g.lineTo(cx+Math.cos(a)*(rx+15),cy+Math.sin(a)*(ry+10));g.stroke()}
 if(soupVisible.toys){for(const stone of liveToys.stones||[]){const[x,y]=soupPoint(stone.start,1);g.fillStyle='#77827a';g.fillRect(x-3,y-3,6,6)}for(const bubble of liveToys.bubbles||[]){const[x,y]=soupPoint(bubble.address,1);g.strokeStyle='#b98bea';g.lineWidth=1.5;g.beginPath();g.arc(x,y,3.5,0,Math.PI*2);g.stroke()}for(const sw of liveToys.switches||[]){const[x,y]=soupPoint(sw.trigger,1);g.fillStyle='#e6bd68';g.beginPath();g.moveTo(x,y-4);g.lineTo(x+4,y+3);g.lineTo(x-4,y+3);g.closePath();g.fill()}}
 if(soupVisible.amoebas)for(const entity of liveEntities){if(!entity.alive||(hoveredSoupEntity&&entity.id!==hoveredSoupEntity.id))continue;const[x,y]=soupPoint(entity.position,-1);g.fillStyle='#73dc8c';g.beginPath();g.arc(x,y,hoveredSoupEntity?5:3.4,0,Math.PI*2);g.fill()}
 soupPulses=soupPulses.filter(p=>now-p.born<1800);for(const p of soupPulses){if(!soupVisible[p.type]||(hoveredSoupEntity&&!p.entityIds.includes(hoveredSoupEntity.id)))continue;const age=(now-p.born)/1800,[x,y]=soupPoint(p.address,0);g.globalAlpha=1-age;g.strokeStyle=p.color;g.lineWidth=p.type==='environment'?1.5:2.5;g.beginPath();g.arc(x,y,p.size+age*p.grow,0,Math.PI*2);g.stroke()}g.globalAlpha=1;requestAnimationFrame(drawSoup)}
async function pollSoup(){if(livePolling)return;livePolling=true;try{const d=await fetch(`/api/live-feed?after=${liveCursor}`,{cache:'no-store'}).then(r=>r.json());liveCursor=d.cursor||liveCursor;liveRamSize=d.ram_size||liveRamSize;liveEntities=d.entities||[];liveToys=d.toys||{};document.querySelector('#live-soup-numbers').textContent=`Tick ${Number(d.tick||0).toLocaleString()} · ${Number(d.population||0).toLocaleString()} Amöben`;const positions=new Map(liveEntities.map(e=>[e.id,e.position]));for(const e of d.events||[]){const owners=[e.entity_id,...(e.parents||[])].filter(Boolean);if(e.kind==='ram_read')soupPulse(e.address,'#77b9e8',3,'reads',15,owners);else if(e.kind==='ram_write')soupPulse(e.address,'#e6bd68',4,'writes',17,owners);else if(e.kind==='environment_change')soupPulse(e.address,'#b98bea',2,'environment',7,owners);else if(e.kind==='birth')soupPulse(e.ram_position,'#ffffff',7,'births',20,owners);else if(e.kind==='death')soupPulse(positions.get(e.entity_id),'#e17b72',7,'deaths',20,owners)}}catch(_e){}finally{livePolling=false}}
requestAnimationFrame(drawSoup);pollSoup();let soupPollTimer=setInterval(pollSoup,500);
soupCanvas.addEventListener('pointermove',event=>{const rect=soupCanvas.getBoundingClientRect(),px=(event.clientX-rect.left)*soupCanvas.width/rect.width,py=(event.clientY-rect.top)*soupCanvas.height/rect.height;let nearest=null,best=Infinity;for(const entity of liveEntities){if(!entity.alive)continue;const[x,y]=soupPoint(entity.position,-1),distance=Math.hypot(px-x,py-y);if(distance<best){best=distance;nearest=entity}}if(!nearest||best>11||!soupVisible.amoebas){hoveredSoupEntity=null;soupTooltip.hidden=true;soupCanvas.style.cursor='default';return}hoveredSoupEntity=nearest;soupCanvas.style.cursor='pointer';soupTooltip.hidden=false;soupTooltip.innerHTML=`<b>${esc(nearest.name||nameOf(nearest.id))} · #${nearest.id}</b><br>RAM ${Number(nearest.position).toLocaleString()} · S ${Number(nearest.energy).toFixed(2)}<br><span class="muted">Klicken für Details</span>`;soupTooltip.style.left=`${event.clientX-rect.left+14}px`;soupTooltip.style.top=`${event.clientY-rect.top+58}px`});
soupCanvas.addEventListener('pointerleave',()=>{hoveredSoupEntity=null;soupTooltip.hidden=true;soupCanvas.style.cursor='default'});
soupCanvas.addEventListener('click',async()=>{if(!hoveredSoupEntity)return;const entityId=hoveredSoupEntity.id;selection={mode:'all',start:0,end:maxTick()};select.value='latest';await applySelection();const card=document.querySelector(`details[data-entity="${entityId}"]`);if(!card)return;card.open=true;card.classList.add('soup-focus');card.scrollIntoView({behavior:'smooth',block:'start'});setTimeout(()=>card.classList.remove('soup-focus'),2200)});
function clearSoupHistory(){for(const timer of soupHistoryTimers)clearTimeout(timer);soupHistoryTimers=[];soupPulses=[]}
function historyPulse(event,positions){const owners=[event.entity_id,...(event.parents||[])].filter(Boolean);if(event.kind==='ram_read')soupPulse(event.address,'#77b9e8',3,'reads',15,owners);else if(event.kind==='ram_write')soupPulse(event.address,'#e6bd68',4,'writes',17,owners);else if(event.kind==='environment_change')soupPulse(event.address,'#b98bea',2,'environment',7,owners);else if(event.kind==='birth')soupPulse(event.ram_position??positions.get(event.entity_id),'#ffffff',7,'births',20,owners);else if(event.kind==='death')soupPulse(positions.get(event.entity_id),'#e17b72',7,'deaths',20,owners)}
let soupSelectionRequest=0;
async function syncSoupToSelection(){
 const request=++soupSelectionRequest;clearSoupHistory();
 if(selection.mode==='all'){historicalSoup=false;if(!soupPollTimer)soupPollTimer=setInterval(pollSoup,500);pollSoup();return}
 historicalSoup=true;if(soupPollTimer){clearInterval(soupPollTimer);soupPollTimer=null}
 const[start,end]=selectionRange(),snapshot=snapshotNames.filter(n=>parseInt(n)<=end).at(-1),path=snapshot?'/api/snapshot/'+snapshot:'/api/latest';
 try{
  const s=await fetch(path,{cache:'no-store'}).then(r=>r.json());if(request!==soupSelectionRequest||selection.mode==='all')return;
  liveRamSize=s.config?.ram_size||liveRamSize;liveToys=s.environment_toys||liveToys;liveEntities=(s.entities||[]).map(e=>({id:e.id,name:e.name,position:e.ram_position||0,energy:e.energy,alive:e.alive}));
  const positions=new Map(liveEntities.map(e=>[e.id,e.position])),allEvents=[...environmentEvents.filter(e=>e.tick>=start&&e.tick<=end),...activityEvents.filter(e=>e.tick>=start&&e.tick<=end&&['environment_change','birth','death'].includes(e.kind))].sort((a,b)=>a.tick-b.tick),stride=Math.max(1,Math.ceil(allEvents.length/1500)),events=allEvents.filter((_,index)=>index%stride===0);
  document.querySelector('#live-soup-numbers').textContent=selection.mode==='point'?`Tick ${end.toLocaleString()} · historische Ansicht`:`Ticks ${start.toLocaleString()}–${end.toLocaleString()} · Wiedergabe`;
  if(selection.mode==='point'||!events.length)return;
  const span=Math.max(1,end-start),duration=Math.min(9000,Math.max(2500,span*18));
  for(const event of events){const delay=(event.tick-start)/span*duration;soupHistoryTimers.push(setTimeout(()=>{if(request===soupSelectionRequest)historyPulse(event,positions)},delay))}
 }catch(_e){}
}
let soupSelectionDebounce=null;new MutationObserver(()=>{clearTimeout(soupSelectionDebounce);soupSelectionDebounce=setTimeout(syncSoupToSelection,180)}).observe(document.querySelector('#selection-label'),{childList:true,subtree:true,characterData:true});
let snapshotNames=[];
function eventsForSelection(){const [start,end]=selectionRange();return activityEvents.filter(e=>e.tick>=start&&e.tick<=end&&(!e.entity_id||visibleIds.has(e.entity_id)))}
function renderActivity(){const events=eventsForSelection(),counts={birth:0,death:0,discoveries:0,invitations:0,deadFinds:0,writes:0,rejections:0};events.forEach(e=>{if(e.kind==='birth'&&(e.parents||[]).length)counts.birth++;if(e.kind==='death')counts.death++;if(e.discovery_type==='entity')counts.discoveries++;if(e.discovery_type==='invitation')counts.invitations++;if(e.discovery_type==='life_state'&&!e.value)counts.deadFinds++;if(e.kind==='ram_write')counts.writes++;if(e.kind==='birth_rejected')counts.rejections++});document.querySelector('#selection-stats').innerHTML=`<div class="metric">Amöben<strong>${visibleIds.size}</strong></div><div class="metric">Geburten<strong>${counts.birth}</strong></div><div class="metric">Tode<strong>${counts.death}</strong></div><div class="metric">Funde<strong>${counts.discoveries}</strong></div><div class="metric">Tot aufgefunden<strong>${counts.deadFinds}</strong></div><div class="metric">Einladungen<strong>${counts.invitations}</strong></div><div class="metric">RAM-Schreiben<strong>${counts.writes}</strong></div>`;const important=events.filter(e=>e.kind!=='ram_write').slice(-150).reverse();document.querySelector('#selection-events').innerHTML=important.length?important.map(e=>`<li><b>Tick ${e.tick}</b> · Amöbe #${e.entity_id||'—'} · ${esc(describe(e))}</li>`).join(''):'<li class="empty">In dieser Auswahl wurde kein biologisch relevantes Ereignis protokolliert.</li>'}
async function applySelection(){const [start,end]=selectionRange(),snapshot=snapshotNames.filter(n=>parseInt(n)<=end).at(-1),path=snapshot?'/api/snapshot/'+snapshot:'/api/latest';try{const s=await fetch(path,{cache:'no-store'}).then(r=>r.json());if(s.error)throw Error(s.error);currentTick=s.tick;const deaths=new Map(activityEvents.filter(e=>e.kind==='death').map(e=>[e.entity_id,e.tick])),shown=s.entities.filter(e=>e.born_at<=end&&(!deaths.has(e.id)||deaths.get(e.id)>=start));visibleIds=new Set(shown.map(e=>e.id));const aliveAtEnd=shown.filter(e=>e.born_at<=end&&(!deaths.has(e.id)||deaths.get(e.id)>end)).length;const title=selection.mode==='all'?'Gesamter Lauf':selection.mode==='point'?`Tick ${end}`:`Ticks ${start}–${end}`;document.querySelector('#selection-label').textContent=title;document.querySelector('#selection-help').textContent=`Zustand aus Snapshot Tick ${s.tick}`;metaBox.innerHTML=`<div class="metric">Auswahl<strong>${title}</strong></div><div class="metric">Am Ende lebend<strong>${aliveAtEnd}</strong></div><div class="metric">Beteiligte Amöben<strong>${shown.length}</strong></div><div class="metric">Seed<strong>${s.config.seed}</strong></div><div class="metric">Run<strong style="font-size:.8rem">${esc(s.run_id||'—')}</strong></div>`;const open=new Set([...box.querySelectorAll('details[open]')].map(d=>d.dataset.entity)),chosen=envSelect.value;box.innerHTML=shown.length?shown.map(e=>card(e,open)).join(''):'<p class="empty">Keine Amöbe berührt diese Auswahl.</p>';envSelect.innerHTML='<option value="all">alle</option>'+shown.map(e=>`<option value="${e.id}">${amoeba(e)} #${e.id}</option>`).join('');if([...envSelect.options].some(o=>o.value===chosen))envSelect.value=chosen;renderActivity();drawEnvironment();drawTimeline()}catch(e){box.innerHTML=`<p class="error">${esc(e.message)}</p>`}}
async function list(){const [a,t,e,activity]=await Promise.all([fetch('/api/snapshots').then(r=>r.json()),fetch('/api/timeline').then(r=>r.json()),fetch('/api/environment').then(r=>r.json()),fetch('/api/activity').then(r=>r.json())]);snapshotNames=a;timelinePoints=t;environmentEvents=e;activityEvents=activity;selection={mode:'all',start:0,end:maxTick()};select.innerHTML='<option value="latest">aktuell</option>'+a.map(x=>`<option value="${esc(x)}">Tick ${parseInt(x)}</option>`).join('');drawTimeline()}
chartCanvas.onpointerdown=e=>{dragStart=tickFromPointer(e);chartCanvas.setPointerCapture(e.pointerId)};chartCanvas.onpointermove=e=>{if(dragStart===null)return;const now=tickFromPointer(e);selection={mode:now===dragStart?'point':'range',start:Math.min(dragStart,now),end:Math.max(dragStart,now)};drawTimeline();document.querySelector('#selection-label').textContent=selection.mode==='point'?`Tick ${now}`:`Ticks ${selection.start}–${selection.end}`};chartCanvas.onpointerup=async e=>{if(dragStart===null)return;const now=tickFromPointer(e);selection={mode:now===dragStart?'point':'range',start:Math.min(dragStart,now),end:Math.max(dragStart,now)};dragStart=null;await applySelection()};
document.querySelector('#timeline-all').onclick=()=>{selection={mode:'all',start:0,end:maxTick()};select.value='latest';applySelection()};envSelect.onchange=drawEnvironment;select.onchange=()=>{if(select.value==='latest')selection={mode:'all',start:0,end:maxTick()};else{const tick=parseInt(select.value);selection={mode:'point',start:tick,end:tick}}applySelection()};Promise.all([runStatus(),dashboardWithFertility(),list()]).then(applySelection);setInterval(runStatus,2000);
</script></body></html>'''

def legacy_handler_for(run_dir: Path):
    activity_cache: list[dict] | None = None
    activity_lock = Lock()

    def activity_events() -> list[dict]:
        nonlocal activity_cache
        if activity_cache is not None:
            return activity_cache
        with activity_lock:
            if activity_cache is not None:
                return activity_cache
            selected = []
            event_path = run_dir / "events.jsonl"
            if event_path.exists():
                with event_path.open(encoding="utf-8") as stream:
                    for line in stream:
                        event = json.loads(line)
                        if event["kind"] in {
                            "birth", "death", "birth_rejected", "mem_write",
                            "mem_write_rejected", "reproduction_cost", "ram_write",
                            "environment_change",
                        } or (event["kind"] == "ram_read" and event.get("reward", 0) > 0):
                            selected.append(event)
            activity_cache = selected
            return selected

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/": data, kind = HTML.encode(), "text/html; charset=utf-8"
            elif self.path == "/api/dashboard":
                data = json.dumps(dashboard_data(run_dir.parent)).encode()
                kind = "application/json; charset=utf-8"
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
            elif self.path == "/api/activity":
                data = json.dumps(activity_events()).encode(); kind = "application/json; charset=utf-8"
            elif self.path == "/api/environment":
                event_path = run_dir / "events.jsonl"
                events = []
                if event_path.exists():
                    for line in event_path.read_text(encoding="utf-8").splitlines():
                        event = json.loads(line)
                        if event["kind"] in {"ram_read", "ram_write"} and not event.get("virtual"):
                            events.append({
                                "tick": event["tick"], "kind": event["kind"],
                                "entity_id": event["entity_id"], "address": event["address"],
                                "value": event["value"], "reward": event.get("reward", 0),
                                "changed": event.get("changed"),
                                "self_origin": event.get("self_origin", False),
                            })
                data = json.dumps(events).encode(); kind = "application/json; charset=utf-8"
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

def legacy_main() -> None:
    parser = argparse.ArgumentParser(description="Read-only EVE-Alife Lupe")
    parser.add_argument("run_dir", type=Path); parser.add_argument("--port", type=int, default=8080); args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(args.run_dir.resolve()))
    print(f"Lupe: http://127.0.0.1:{args.port}"); server.serve_forever()

def readonly_connection(database: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def unpack_event(row: sqlite3.Row) -> dict:
    return {"tick": row["tick"], "kind": row["kind"], **json.loads(row["payload_json"])}


def dashboard_data(run_root: Path) -> dict:
    history, lives, offspring, energy = [], [], 0, 0.0
    candidates: dict[str, list[dict]] = defaultdict(list)
    dated_directories = []
    for directory in run_root.iterdir() if run_root.exists() else []:
        database = directory / "run.sqlite3"
        if not database.exists():
            continue
        try:
            with readonly_connection(database) as db:
                row = db.execute("SELECT created_at FROM run WHERE singleton=1").fetchone()
                if row is not None:
                    dated_directories.append((row[0], directory))
        except sqlite3.Error:
            continue
    for number, (_created_at, directory) in enumerate(sorted(dated_directories), 1):
        database = directory / "run.sqlite3"
        if not database.exists():
            continue
        try:
            with readonly_connection(database) as db:
                run = db.execute("SELECT * FROM run WHERE singleton=1").fetchone()
                births = db.execute("SELECT count(DISTINCT child_id) FROM ancestry").fetchone()[0]
                offspring += births
                events = [unpack_event(row) for row in db.execute("SELECT tick,kind,payload_json FROM events ORDER BY event_id")]
                gained = sum((event.get("reward", 0) or 0) for event in events if event["kind"] == "ram_read")
                energy += gained
                history.append({
                    "run_number": number, "run_id": run["run_id"],
                    "created_at": run["created_at"], "tick": run["current_tick"],
                    "population_alive": run["population"],
                    "mass_extinction": run["end_reason"] == "natural_extinction",
                    "offspring": births, "infertile_offspring": 0, "energy_gained": gained,
                })
                lives.extend(
                    {"entity_id": row["entity_id"], "name": row["name"],
                     "lifespan": row["died_tick"] - row["born_tick"], "run_number": number}
                    for row in db.execute("SELECT * FROM entities WHERE died_tick IS NOT NULL")
                )
                latest_row = db.execute("SELECT payload_zlib FROM observations ORDER BY tick DESC LIMIT 1").fetchone()
                if latest_row is None:
                    continue
                snapshot = json.loads(zlib.decompress(latest_row[0]))
                entities = {entity["id"]: entity for entity in snapshot["entities"]}
                history[-1]["infertile_offspring"] = sum(
                    bool(entity.get("parents"))
                    and not any(node["kind"] == "MEM_WRITE" for node in entity["genome"]["nodes"])
                    for entity in entities.values()
                )
                children: dict[int, set[int]] = defaultdict(set)
                parents: dict[int, list[int]] = defaultdict(list)
                for edge in db.execute("SELECT child_id,parent_id FROM ancestry"):
                    children[edge["parent_id"]].add(edge["child_id"])
                    parents[edge["child_id"]].append(edge["parent_id"])
                generations: dict[int, int] = {}
                def generation(entity_id: int) -> int:
                    if entity_id not in generations:
                        generations[entity_id] = 0 if not parents[entity_id] else 1 + max(generation(parent) for parent in parents[entity_id])
                    return generations[entity_id]
                def descendants(entity_id: int) -> int:
                    found, pending = set(), list(children[entity_id])
                    while pending:
                        child = pending.pop()
                        if child not in found:
                            found.add(child); pending.extend(children[child])
                    return len(found)
                ram_addresses: dict[int, set[int]] = defaultdict(set)
                ram_energy: Counter = Counter(); producers: Counter = Counter()
                discoveries: Counter = Counter(); invitations: Counter = Counter(); writes: Counter = Counter()
                for event in events:
                    entity_id = event.get("entity_id")
                    if event["kind"] in {"ram_read", "ram_write"} and not event.get("virtual") and entity_id:
                        ram_addresses[entity_id].add(event.get("address"))
                    if event["kind"] == "ram_read" and entity_id:
                        reward = event.get("reward", 0) or 0; ram_energy[entity_id] += reward
                        originators = event.get("originators", [])
                        for originator in originators:
                            producers[originator] += reward / max(1, len(originators))
                        if event.get("discovery_type") == "entity": discoveries[entity_id] += 1
                        if event.get("discovery_type") == "invitation": invitations[entity_id] += 1
                    if event["kind"] == "ram_write" and entity_id: writes[entity_id] += 1
                for entity_id, entity in entities.items():
                    base = {"entity_id": entity_id, "name": entity.get("name", f"Amöbe {entity_id}"), "run_number": number}
                    candidates["largest_genome"].append({**base, "value": entity["n_g"], "n_f": entity["n_f"], "n_p": entity["n_p"]})
                    candidates["highest_energy"].append({**base, "value": entity["energy"]})
                    candidates["most_direct_children"].append({**base, "value": len(children[entity_id])})
                    candidates["most_descendants"].append({**base, "value": descendants(entity_id)})
                    candidates["deepest_generation"].append({**base, "value": generation(entity_id)})
                    candidates["oldest_entity"].append({**base, "value": run["current_tick"] - entity["born_at"], "alive": entity["alive"]})
                    candidates["most_ram_addresses"].append({**base, "value": len(ram_addresses[entity_id])})
                    candidates["most_ram_energy"].append({**base, "value": float(ram_energy[entity_id])})
                    candidates["best_information_producer"].append({**base, "value": float(producers[entity_id])})
                    candidates["most_entity_discoveries"].append({**base, "value": discoveries[entity_id]})
                    candidates["most_invitations"].append({**base, "value": invitations[entity_id]})
                    candidates["most_ram_writes"].append({**base, "value": writes[entity_id]})
        except sqlite3.Error:
            continue
    record_names = (
        "largest_genome", "highest_energy", "most_direct_children", "most_descendants",
        "deepest_generation", "oldest_entity", "most_ram_addresses", "most_ram_energy",
        "best_information_producer", "most_entity_discoveries", "most_invitations", "most_ram_writes",
    )
    return {
        "mass_extinctions": sum(item["mass_extinction"] for item in history),
        "offspring": offspring, "energy_gained": energy, "runs": len(history),
        "shortest_life": min(lives, key=lambda item: item["lifespan"], default=None),
        "longest_life": max(lives, key=lambda item: item["lifespan"], default=None),
        "history": list(reversed(history)),
        "records": {name: max(candidates[name], key=lambda item: item["value"], default=None) for name in record_names},
    }


def handler_for(run_dir: Path):
    database = run_dir / "run.sqlite3"

    def observation(db: sqlite3.Connection, tick: int | None = None) -> dict:
        query = "SELECT payload_zlib FROM observations"
        arguments: tuple = ()
        if tick is None:
            query += " ORDER BY tick DESC LIMIT 1"
        else:
            query += " WHERE tick=?"
            arguments = (tick,)
        row = db.execute(query, arguments).fetchone()
        if row is None:
            return {"error": "Kein gespeichertes Lupe-Bild"}
        return json.loads(zlib.decompress(row[0]))

    class Handler(BaseHTTPRequestHandler):
        def respond(self, value: object, status: int = 200) -> None:
            data = json.dumps(value, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers(); self.wfile.write(data)

        def do_GET(self):
            request = urlsplit(self.path)
            path = request.path
            if path == "/":
                data = HTML.encode(); self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(data); return
            try:
                with readonly_connection(database) as db:
                    if path == "/api/status":
                        self.respond(dict(db.execute("SELECT * FROM run WHERE singleton=1").fetchone()))
                    elif path == "/api/dashboard":
                        self.respond(dashboard_data(run_dir.parent))
                    elif path == "/api/latest":
                        try: self.respond(json.loads((run_dir / "live.json").read_text(encoding="utf-8")))
                        except FileNotFoundError: self.respond(observation(db))
                    elif path == "/api/live-feed":
                        query = parse_qs(request.query)
                        after = max(0, int(query.get("after", [0])[0]))
                        try:
                            live = json.loads((run_dir / "live.json").read_text(encoding="utf-8"))
                        except FileNotFoundError:
                            live = observation(db)
                        newest = int(db.execute("SELECT coalesce(max(event_id),0) FROM events").fetchone()[0])
                        if after == 0:
                            after = max(0, newest - 250)
                        rows = db.execute(
                            """SELECT event_id,tick,kind,payload_json FROM events
                               WHERE event_id>? AND kind IN
                               ('ram_read','ram_write','environment_change','birth','death')
                               ORDER BY event_id LIMIT 1000""",
                            (after,),
                        )
                        events = []
                        cursor = after
                        for row in rows:
                            cursor = row["event_id"]
                            event = unpack_event(row)
                            if event["kind"] != "ram_read" or not event.get("virtual"):
                                events.append(event)
                        self.respond({
                            "tick": live.get("tick", 0),
                            "population": live.get("population", 0),
                            "ram_size": live.get("config", {}).get("ram_size", 1),
                            "entities": [
                                {"id": entity["id"], "name": entity.get("name"),
                                 "position": entity.get("ram_position", 0),
                                 "energy": entity.get("energy", 0),
                                 "alive": bool(entity.get("alive"))}
                                for entity in live.get("entities", [])
                            ],
                            "toys": live.get("environment_toys", {}),
                            "events": events, "cursor": cursor, "newest": newest,
                        })
                    elif path == "/api/snapshots":
                        self.respond([f"{row[0]:012d}.json" for row in db.execute("SELECT tick FROM observations ORDER BY tick")])
                    elif path == "/api/timeline":
                        self.respond([{"tick": row[0], "alive": row[1]} for row in db.execute("SELECT tick,population FROM measurements ORDER BY tick")])
                    elif path in {"/api/activity", "/api/environment"}:
                        events = [unpack_event(row) for row in db.execute("SELECT tick,kind,payload_json FROM events ORDER BY event_id")]
                        if path == "/api/activity":
                            events = [event for event in events if event["kind"] in {"birth", "death", "birth_rejected", "mem_write", "mem_write_rejected", "knock", "reproduction_cost", "ram_write", "genome_created", "environment_change"} or (event["kind"] == "ram_read" and event.get("reward", 0) > 0)]
                        else:
                            events = [event for event in events if event["kind"] in {"ram_read", "ram_write"} and not event.get("virtual")]
                        self.respond(events)
                    elif path.startswith("/api/entity/") and path.endswith("/life"):
                        raw_id = path.removeprefix("/api/entity/").removesuffix("/life")
                        if not raw_id.isdigit(): self.respond({"error": "Ungültige ID"}, 400); return
                        entity_id = int(raw_id)
                        events = [unpack_event(row) for row in db.execute("SELECT tick,kind,payload_json FROM events WHERE entity_id=? ORDER BY event_id", (entity_id,))]
                        frames, previous = [], -1
                        for row in db.execute("SELECT tick,payload_zlib FROM observations ORDER BY tick"):
                            snapshot = json.loads(zlib.decompress(row[1]))
                            entity = next((item for item in snapshot["entities"] if item["id"] == entity_id), None)
                            if entity is not None:
                                frames.append({"tick": row[0], "entity": entity, "events": [event for event in events if previous < event["tick"] <= row[0]]})
                                previous = row[0]
                        self.respond({"entity_id": entity_id, "frames": frames})
                    elif path.startswith("/api/snapshot/"):
                        name = path.removeprefix("/api/snapshot/")
                        if Path(name).name != name or not name.endswith(".json") or not name[:-5].isdigit():
                            self.respond({"error": "Ungültiger Snapshot"}, 400); return
                        self.respond(observation(db, int(name[:-5])))
                    else:
                        self.respond({"error": "Nicht gefunden"}, 404)
            except (sqlite3.Error, ValueError, zlib.error) as error:
                self.respond({"error": str(error)}, 500)

        def log_message(self, _format, *_args):
            pass
    return Handler


def validate_source(source: Path) -> None:
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("format") != FORMAT_NAME or manifest.get("format_version") != SCHEMA_VERSION:
        raise ValueError("Nicht unterstütztes EVE-Run-Format")


def main() -> None:
    parser = argparse.ArgumentParser(description="Erweiterte read-only EVE-Alife-Lupe")
    parser.add_argument("source", type=Path); parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(); temporary = None; source = args.source.resolve()
    if source.is_file():
        temporary = tempfile.TemporaryDirectory(prefix="eve-lupe-")
        with zipfile.ZipFile(source) as archive:
            for name in ("manifest.json", "run.sqlite3"):
                if name not in archive.namelist(): parser.error("Ungültiges EVE-Run-Archiv")
                archive.extract(name, temporary.name)
        source = Path(temporary.name)
    try: validate_source(source)
    except (OSError, ValueError, json.JSONDecodeError) as error: parser.error(str(error))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(source))
    print(f"Lupe: http://127.0.0.1:{args.port}")
    try: server.serve_forever()
    finally:
        server.server_close()
        if temporary: temporary.cleanup()


if __name__ == "__main__": main()
