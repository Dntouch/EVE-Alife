(() => {
  const main = document.querySelector('main');
  if (!main || document.querySelector('.eve-rail')) return;

  const rail = document.createElement('aside');
  rail.className = 'eve-rail';
  rail.innerHTML = `
    <img class="eve-logo" src="/assets/eve-e-logo.png" alt="EVE">
    <nav class="eve-nav" aria-label="Hauptnavigation">
      <button class="active" data-view="live"><span>◉</span>Leitstand</button>
      <button data-view="history"><span>⌁</span>Historie</button>
      <button data-view="chronicle"><span>◫</span>Chronik</button>
      <button data-view="lineage"><span>⑂</span>Stammbaum</button>
      <button data-view="genome"><span>⌬</span>Genom</button>
    </nav>
    <div class="eve-rail-status">Read only</div>`;
  document.body.prepend(rail);
  const neuralField=document.createElement('div');
  neuralField.className='eve-neural-field';
  neuralField.setAttribute('aria-hidden','true');
  neuralField.innerHTML=[[78,13,'cyan',7.1,-1.3],[88,19,'violet',11.7,-6.2],[95,31,'cyan',8.9,-4.4],[82,39,'cyan',13.4,-9.1],[92,49,'violet',9.8,-2.7],[75,58,'violet',14.6,-11.8],[87,66,'cyan',10.9,-7.5],[96,75,'violet',12.3,-3.8],[80,84,'cyan',15.1,-13.2]].map(([x,y,color,duration,delay])=>`<i class="${color}" style="--x:${x}%;--y:${y}%;--pulse:${duration}s;--delay:${delay}s"></i>`).join('');
  document.body.prepend(neuralField);

  const commandbar = document.createElement('header');
  commandbar.className = 'eve-commandbar';
  commandbar.innerHTML = `
    <h1>EVE · Lupe <small>Prototyp v0.4 · Evolutionsanalyse</small></h1>
    <div class="eve-command-meta">
      <div class="run-controls"><select id="eve-run-select" aria-label="Run auswählen"><option>Runs werden geladen …</option></select><button type="button" id="eve-replay">▶ Replay</button><button type="button" id="eve-new-run">＋ Neuer Lauf</button><button type="button" id="eve-resume-run" hidden>↗ Fortsetzen</button><button type="button" id="eve-stop-run" class="danger" hidden>■ Stoppen</button></div>
      <span class="eve-chip live">● Daten verbunden</span>
      <span class="eve-chip">Nur Lesen</span>
    </div>`;
  main.prepend(commandbar);
  const legacyTop = main.querySelector(':scope > .top');
  const timeControl = legacyTop?.querySelector('label');
  if (timeControl) {
    const timeSelect = timeControl.querySelector('select');
    timeControl.className = 'eve-time-control';
    timeControl.innerHTML = '<span>◷ Zeitpunkt</span>';
    timeControl.append(timeSelect);
    commandbar.querySelector('.eve-command-meta').prepend(timeControl);
  }

  const direct = [...main.children].filter(node => node !== commandbar && !node.classList.contains('top'));
  const liveView = document.createElement('section');
  liveView.className = 'eve-view active'; liveView.dataset.view = 'live';
  liveView.innerHTML = '<header class="eve-view-header"><h2>Leitstand</h2><p>Der gewählte Lauf als lebendes System. Zoome in die RAM-Suppe, beobachte Aktivität und hefte einzelne Amöben an.</p></header>';
  const historyView = document.createElement('section');
  historyView.className = 'eve-view'; historyView.dataset.view = 'history';
  historyView.innerHTML = '<header class="eve-view-header"><h2>Historische Analyse</h2><p>Gespeicherte Messpunkte, Ereignisse und Lebenslinien. Historische Bilder sind kein exakter Tick-Replay.</p></header>';
  const chronicleView = document.createElement('section');
  chronicleView.className = 'eve-view'; chronicleView.dataset.view = 'chronicle';
  chronicleView.innerHTML = '<header class="eve-view-header"><h2>Chronik des Biotops</h2><p>Das EVE-Archiv über alle erhaltenen Experimente, Generationen und Prototypversionen.</p></header><div id="chronicle-workspace" class="chronicle-loading panel">Run-Archiv wird kartiert …</div>';
  const genomeView = document.createElement('section');
  genomeView.className = 'eve-view'; genomeView.dataset.view = 'genome';
  genomeView.innerHTML = `<header class="eve-view-header"><h2>Genom-Analyse</h2><p>Der eigene Arbeitsraum für Genomkarten und generationenübergreifende Vergleiche.</p></header><div id="genome-workspace" class="genome-landing panel"><div><img src="/assets/eve-e-logo.png" alt=""><h3>Wähle eine Amöbe</h3><p>Öffne eine Amöbe aus der Historienliste oder aus einem Cluster des Live-Leitstands.</p></div></div>`;
  const lineageView = document.createElement('section');
  lineageView.className = 'eve-view'; lineageView.dataset.view = 'lineage';
  lineageView.innerHTML = `<header class="eve-view-header"><h2>Evolutionäre Zeitlandschaft</h2><p>Abstammung, Selektion und Genomveränderung über den gesamten Lauf.</p></header><div id="lineage-workspace" class="lineage-loading panel">Evolutionäre Linien werden rekonstruiert …</div>`;
  main.append(liveView, historyView, chronicleView, lineageView, genomeView);

  const liveIds = new Set(['run-status', 'live-soup']);
  direct.forEach(node => (liveIds.has(node.id) ? liveView : node.id === 'dashboard' ? chronicleView : historyView).append(node));
  document.querySelector('#dashboard')?.classList.add('legacy-chronicle-source');

  const runAnalysisDock=document.createElement('details');
  runAnalysisDock.className='run-analysis-dock';runAnalysisDock.open=true;
  runAnalysisDock.innerHTML='<summary><div><small>EVE · RUN TRAJECTORY</small><h3>Verlauf & Zeitreise</h3></div><span>Population, Ereignisse und historischen Zeitpunkt wählen</span><b>▾</b></summary><div class="run-analysis-content"></div>';
  const runAnalysisContent=runAnalysisDock.querySelector('.run-analysis-content');
  ['meta','replay','timeline-panel'].forEach(id=>{const element=document.querySelector(`#${id}`);if(element)runAnalysisContent.append(element)});
  const evolutionMeta=document.querySelector('#meta');
  if(evolutionMeta){evolutionMeta.classList.add('evolution-summary');let rebuilding=false;new MutationObserver(()=>{if(rebuilding||evolutionMeta.querySelector('.evolution-summary-grid'))return;const values=new Map([...evolutionMeta.querySelectorAll('.metric')].map(metric=>[metric.childNodes[0]?.textContent?.trim(),metric.querySelector('strong')?.textContent?.trim()]));const entities=window.eveV04Entities||[],ordered=entities.filter(entity=>Number.isFinite(Number(entity.n_g))).sort((a,b)=>Number(a.n_g)-Number(b.n_g)),small=ordered[0],large=ordered.at(-1);rebuilding=true;evolutionMeta.innerHTML=`<div class="evolution-summary-context"><small>EVE · ZEITREISE</small><b>${values.get('Auswahl')||'Gesamter Lauf'}</b><span>${document.querySelector('#selection-help')?.textContent||''}</span></div><dl class="evolution-summary-grid"><div><dt>Am Ende lebend</dt><dd>${values.get('Am Ende lebend')||'—'}</dd></div><div><dt>Beteiligte Amöben</dt><dd>${values.get('Beteiligte Amöben')||entities.length}</dd></div><div class="genome-min"><dt>Kleinstes Genom</dt><dd>${small?`${small.n_g} G · ${small.name||`#${small.id}`}`:'—'}</dd></div><div class="genome-max"><dt>Größtes Genom</dt><dd>${large?`${large.n_g} G · ${large.name||`#${large.id}`}`:'—'}</dd></div><div><dt>Seed</dt><dd>${values.get('Seed')||'—'}</dd></div><div class="run"><dt>Run</dt><dd>${values.get('Run')||'—'}</dd></div></dl>`;rebuilding=false}).observe(evolutionMeta,{childList:true})}
  if(evolutionMeta){const summaryKick=setInterval(()=>{if(!evolutionMeta.querySelector('.metric')||!window.eveV04Entities?.length)return;clearInterval(summaryKick);const trigger=document.createElement('i');trigger.hidden=true;evolutionMeta.append(trigger)},100)}
  liveView.append(runAnalysisDock);

  const historyContext=document.createElement('button');
  historyContext.type='button';historyContext.className='history-selection-context';
  historyView.querySelector('.eve-view-header').after(historyContext);
  const updateHistoryContext=()=>{const label=document.querySelector('#selection-label')?.textContent||'Gesamter Lauf',help=document.querySelector('#selection-help')?.textContent||'';historyContext.innerHTML=`<span><small>AKTIVE ZEITAUSWAHL</small><b>${label}</b></span><em>${help}</em><strong>Im Leitstand ändern →</strong>`};
  updateHistoryContext();
  const selectionLabel=document.querySelector('#selection-label');if(selectionLabel)new MutationObserver(updateHistoryContext).observe(selectionLabel,{childList:true,subtree:true,characterData:true});
  historyContext.onclick=()=>{window.eveV04.setView('live');requestAnimationFrame(()=>document.querySelector('#timeline-panel')?.scrollIntoView({behavior:'smooth',block:'center'}))};

  const timelinePanel=document.querySelector('#timeline-panel'),timelineCanvas=document.querySelector('#chart');
  if(timelinePanel&&timelineCanvas){const heading=timelinePanel.querySelector('h2'),copy=timelinePanel.querySelector('.muted');heading.textContent='Evolutionsverlauf';copy.textContent='Population, Genomvielfalt und Schlüsselereignisse. Ziehen wählt aus, Mausrad zoomt, Umschalt-Ziehen verschiebt.';const controls=document.createElement('div');controls.className='evolution-quick-actions';controls.innerHTML='<button type="button" data-evolution-range="all">Gesamt</button><button type="button" data-evolution-range="last">Letzte 100 Ticks</button><button type="button" data-evolution-range="peak">Populationsmaximum</button><button type="button" data-evolution-range="change">Stärkste Veränderung</button>';timelinePanel.querySelector('.top').append(controls);const legend=document.createElement('div');legend.className='evolution-legend';legend.innerHTML='<span class="population"><i></i>Population</span><span class="genomes"><i></i>Genomvielfalt</span><span class="birth"><i></i>Geburt</span><span class="death"><i></i>Tod</span><span class="milestone"><i></i>Schlüsselereignis</span>';const stage=document.createElement('div');stage.className='evolution-chart-stage';timelineCanvas.before(legend);timelineCanvas.replaceWith(stage);stage.append(timelineCanvas);stage.insertAdjacentHTML('beforeend','<div id="timeline-tooltip" class="evolution-tooltip" hidden></div>');controls.querySelectorAll('button').forEach(button=>button.onclick=()=>{const kind=button.dataset.evolutionRange,full=maxTick();if(kind==='all'){timelineViewport={start:0,end:full};selection={mode:'all',start:0,end:full}}else if(kind==='last'){const start=Math.max(0,full-100);timelineViewport={start,end:full};selection={mode:'range',start,end:full}}else{const target=kind==='peak'?[...timelinePoints].sort((a,b)=>b.alive-a.alive)[0]?.tick:(timelineMilestones.find(item=>item.kind==='genome_jump')?.tick??full),span=Math.min(100,full);timelineViewport={start:Math.max(0,target-span/2),end:Math.min(full,target+span/2)};selection={mode:'point',start:target,end:target}}applySelection()})}

  const historyEntities=document.querySelector('#entities');
  if(historyEntities){
    document.querySelector('.activity-grid')?.classList.add('history-legacy-block');
    document.querySelector('#contacts')?.closest('section')?.classList.add('history-legacy-block');
    historyEntities.previousElementSibling?.classList.add('history-legacy-label');
    historyEntities.previousElementSibling?.previousElementSibling?.classList.add('history-legacy-label');
  }

  const soupHead = document.querySelector('#live-soup-head');
  if (soupHead) {
    const toolbar = document.createElement('div');
    toolbar.className = 'ram-toolbar';
    toolbar.innerHTML = '<button type="button" data-ram-zoom="out" title="Herauszoomen">−</button><button type="button" data-ram-zoom="in" title="Hineinzoomen">+</button><button type="button" data-ram-reset>Gesamt</button><span class="ram-zoom-label">Zoom 1×</span><span class="ram-navigation-help">Ziehen: bewegen · Strg + Mausrad: zoomen · Doppelklick: fokussieren</span><span class="ram-minimap" aria-label="Position im gesamten RAM"><i></i></span><span class="ram-ring" aria-hidden="true"></span><span class="ram-ring-label">zyklischer RAM</span>';
    soupHead.after(toolbar);
  }

  const drawer = document.createElement('aside');
  drawer.className = 'amoeba-drawer';
  drawer.setAttribute('aria-live', 'polite');
  drawer.innerHTML = '<h3>Keine Amöbe ausgewählt</h3><p class="muted">Klicke eine einzelne Amöbe im RAM-Band an.</p>';
  document.body.append(drawer);

  const runDialog = document.createElement('dialog');
  runDialog.className = 'run-dialog';
  runDialog.innerHTML = '<form method="dialog"><header><div><small>EVE · SUPERVISOR</small><h2>Neuen Lauf starten</h2></div><button value="cancel" aria-label="Schließen">×</button></header><div class="run-dialog-loading">Parameterschema wird geladen …</div></form>';
  document.body.append(runDialog);

  let focusedAnalysisView = null;
  let analysisFocusPreferred = sessionStorage.getItem('eve-analysis-focus') === '1';
  const setAnalysisFocus = (view, enabled, remember = true) => {
    if (remember) { analysisFocusPreferred=enabled; sessionStorage.setItem('eve-analysis-focus',enabled?'1':'0'); }
    document.querySelectorAll('.eve-view.analysis-focus').forEach(item => item.classList.remove('analysis-focus'));
    document.body.classList.toggle('analysis-focus-mode', enabled);
    focusedAnalysisView = enabled ? view : null;
    if (enabled) view.classList.add('analysis-focus');
    document.querySelectorAll('[data-analysis-focus]').forEach(button => {
      const active = enabled && view.contains(button);
      button.setAttribute('aria-pressed', String(active));
      button.textContent = active ? '⛶ Verkleinern' : '⛶ Vergrößern';
    });
  };
  const bindAnalysisFocus = container => {
    const button = container.querySelector('[data-analysis-focus]');
    if (!button || button.dataset.bound) return;
    const active=container.closest('.eve-view').classList.contains('analysis-focus');
    button.dataset.bound = 'true'; button.setAttribute('aria-pressed', String(active)); button.textContent=active?'⛶ Verkleinern':'⛶ Vergrößern';
    button.onclick = () => { const view=container.closest('.eve-view'); setAnalysisFocus(view, !view.classList.contains('analysis-focus')); };
  };
  document.addEventListener('keydown', event => {
    const typing = event.target.matches?.('input,textarea,select,[contenteditable="true"]');
    if (event.key === 'Escape' && focusedAnalysisView) { event.preventDefault(); setAnalysisFocus(focusedAnalysisView, false); }
    else if ((event.key === 'f' || event.key === 'F') && !typing) {
      const active=document.querySelector('.eve-view.active');
      if (active?.dataset.view === 'lineage' || active?.dataset.view === 'genome') { event.preventDefault(); setAnalysisFocus(active, !active.classList.contains('analysis-focus')); }
    }
  });

  let lastDataSignal = 0;
  window.eveV04 = {
    setView(name) {
      if (focusedAnalysisView && focusedAnalysisView.dataset.view !== name) setAnalysisFocus(focusedAnalysisView, false, false);
      document.querySelectorAll('.eve-view').forEach(view => view.classList.toggle('active', view.dataset.view === name));
      document.querySelectorAll('.eve-nav button').forEach(button => button.classList.toggle('active', button.dataset.view === name));
      if (name === 'lineage') initLineage();
      if (name === 'chronicle') initChronicle();
      if (analysisFocusPreferred && (name === 'lineage' || name === 'genome')) {
        const target=document.querySelector(`.eve-view[data-view="${name}"]`);
        requestAnimationFrame(()=>setAnalysisFocus(target,true,false));
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    showEntity(entity) {
      if (!entity) return;
      drawer.innerHTML = `<h3>${entity.name || `Amöbe #${entity.id}`} <span class="muted">#${entity.id}</span></h3><div class="drawer-grid"><div><small>RAM</small>${Number(entity.position).toLocaleString()}</div><div><small>Energie</small>${Number(entity.energy).toFixed(2)}</div><div><small>Status</small>${entity.alive ? 'lebend' : 'beendet'}</div><div><small>Beobachtung</small>live</div></div><div class="drawer-actions"><button type="button" data-drawer-details>Details</button><button type="button" data-drawer-genome>Genom</button><button type="button" data-drawer-close>Schließen</button></div>`;
      drawer.classList.add('open');
      drawer.querySelector('[data-drawer-close]').onclick = () => drawer.classList.remove('open');
      drawer.querySelector('[data-drawer-details]').onclick = () => {
        sessionStorage.setItem('eve-open-entity', String(entity.id));
        this.setView('history');
        const snapshot = document.querySelector('#snap');
        if (snapshot) {
          snapshot.value = 'latest';
          snapshot.dispatchEvent(new Event('change'));
        }
        drawer.classList.remove('open');
      };
      drawer.querySelector('[data-drawer-genome]').onclick = () => {
        const full = window.eveV04Entities?.find(item => item.id === entity.id);
        if (full) this.showGenome(full);
      };
    },
    showCluster(entities) {
      drawer.innerHTML = `<h3>${entities.length} Amöben an derselben RAM-Position</h3><p class="muted">Zoomen kann identische Koordinaten nicht trennen. Wähle eine Amöbe direkt aus.</p><div class="cluster-list">${entities.map(entity => `<button type="button" data-cluster-entity="${entity.id}"><span>${entity.name || `Amöbe #${entity.id}`} <small>#${entity.id}</small></span><span>S ${Number(entity.energy).toFixed(1)}</span></button>`).join('')}</div><div class="drawer-actions"><button type="button" data-drawer-close>Schließen</button></div>`;
      drawer.classList.add('open');
      drawer.querySelector('[data-drawer-close]').onclick = () => drawer.classList.remove('open');
      drawer.querySelectorAll('[data-cluster-entity]').forEach(button => button.onclick = () => {
        const entity = entities.find(item => item.id === Number(button.dataset.clusterEntity));
        this.showEntity({ ...entity, name: entity.name || `Amöbe #${entity.id}` });
      });
    },
    async showGenomeById(entityId) {
      const cached = window.eveV04Entities?.find(item => Number(item.id) === Number(entityId));
      if (cached?.genome) { this.showGenome(cached); return; }
      const workspace = document.querySelector('#genome-workspace');
      this.setView('genome');
      workspace.className = 'genome-workspace panel';
      workspace.innerHTML = '<div class="genome-loading"><span>⌬</span><b>Genom wird geladen</b><p>Die vollständige Erbinformation wird aus dem Laufarchiv abgerufen.</p></div>';
      try {
        const response = await fetch(`/api/entity/${Number(entityId)}`, { cache: 'no-store' });
        const entity = await response.json();
        if (!response.ok || entity.error) throw new Error(entity.error || 'Genom konnte nicht geladen werden');
        this.showGenome(entity);
      } catch (error) {
        workspace.innerHTML = `<div class="genome-loading error"><span>!</span><b>Genom konnte nicht geladen werden</b><p>${String(error.message || error)}</p></div>`;
      }
    },
    showGenome(entity) {
      if (!entity?.genome) return;
      const workspace = document.querySelector('#genome-workspace');
      workspace.className = 'genome-workspace panel';
      const fragments = window.genomeFragments(entity.genome).length;
      workspace.innerHTML = `<header><div><small class="muted">EVE · GENOMISCHE TOPOLOGIE · AMÖBE #${entity.id}</small><h3>${entity.name || `Amöbe #${entity.id}`} · Genom</h3><div class="genome-stats"><span class="genome-stat genome-total">Gesamtgröße <b>${entity.genome.nodes.length + entity.genome.edges.length} G</b></span><span class="genome-stat">Funktionspunkte <b>${entity.genome.nodes.length}</b></span><span class="genome-stat">Verbindungen <b>${entity.genome.edges.length}</b></span><span class="genome-stat">Fragmente <b>${fragments}</b></span><span class="genome-stat">A₀ <b>${entity.genome.activity_base}</b></span><span class="genome-stat">Nₖ <b>${entity.genome.knock_capacity || 1}</b></span><span class="genome-stat">Tₚ <b>${entity.genome.bond_ticks || 1}</b></span></div></div><div class="genome-toolbar"><button type="button" data-genome-zoom="out" title="Herauszoomen">−</button><button type="button" data-genome-zoom="in" title="Hineinzoomen">+</button><button type="button" data-genome-reset>Gesamt</button><span class="genome-zoom-label">Zoom 1×</span><button type="button" data-genome-popup>↗ Separates Fenster</button><button type="button" data-analysis-focus>⛶ Vergrößern</button></div></header><div class="genome-legend"><span class="read"><i></i>Lesen</span><span class="write"><i></i>Schreiben</span><span class="logic"><i></i>Logik</span><span class="const"><i></i>Konstanten</span><span class="process"><i></i>Verarbeitung</span><strong class="genome-focus-label">Modul anklicken, um Beziehungen zu fokussieren</strong></div><div class="genome-analysis-body"><div class="genome-scroll">${window.genomeSvg(entity.genome)}</div><aside class="genome-node-inspector"><div class="genome-node-empty"><span>⌬</span><b>Funktionspunkt auswählen</b><p>Hier erscheint, was der Punkt verarbeitet und welche Wirkung seine Verbindungen haben können.</p></div></aside></div>`;
      bindAnalysisFocus(workspace);
      window.genomeDiagram(entity.genome, entity.id);
      workspace.querySelector('[data-genome-popup]').onclick = () => window.openGenomeDiagram(entity.id);
      const svg = workspace.querySelector('.genome-graph'), nodes = [...svg.querySelectorAll('[data-node]')], edges = [...svg.querySelectorAll('[data-source]')], focusLabel = workspace.querySelector('.genome-focus-label'), zoomLabel=workspace.querySelector('.genome-zoom-label'), inspector=workspace.querySelector('.genome-node-inspector');
      const nodeData=new Map(entity.genome.nodes.map(node=>[String(node.id),node]));
      const descriptions={
        CONST:'Gibt einen im Genom gespeicherten Zahlenwert als Signal aus.',S_READ:'Liest den aktuellen Energiezustand der Amöbe.',Z_READ:'Liest einen Wert aus dem dauerhaften Z-Gedächtnis.',Z_WRITE:'Schreibt einen Wert in das dauerhafte Z-Gedächtnis.',RAM_READ:'Liest einen Wert aus der gemeinsamen RAM-Suppe.',RAM_WRITE:'Schreibt einen Wert in die gemeinsame RAM-Suppe.',MEM_READ:'Liest einen Eintrag aus dem eigenen Membran- und Partnergedächtnis.',MEM_WRITE:'Schreibt eine Referenz in das eigene Membran- und Partnergedächtnis.',ADD:'Addiert seine Eingangssignale.',SUB:'Zieht ein Eingangssignal von einem anderen ab.',XOR:'Verknüpft zwei Zahlenwerte bitweise exklusiv.',EQ:'Prüft, ob zwei Eingangswerte gleich sind.',GATE:'Gibt ein Signal nur weiter, wenn die Bedingung erfüllt ist.',PAUSE:'Beendet diesen Signalweg ohne weitere Aktion.'
      };
      const intrinsicEffects={RAM_WRITE:'ein Wert in der gemeinsamen RAM-Suppe verändert werden kann',MEM_WRITE:'eine Partnerreferenz in der eigenen Membran angelegt, geändert oder entfernt werden kann',Z_WRITE:'ein Wert im dauerhaften Z-Gedächtnis verändert werden kann',PAUSE:'dieser Signalweg an dieser Stelle endet'};
      const consequence=(target,edge)=>({RAM_READ:`bestimmt mit, welche RAM-Adresse gelesen wird`,RAM_WRITE:`bestimmt mit, welche RAM-Adresse oder welcher Wert geschrieben wird`,MEM_READ:`bestimmt mit, welcher Membranplatz gelesen wird`,MEM_WRITE:`bestimmt mit, welcher Partnerplatz oder welche Referenz gespeichert wird`,Z_READ:`bestimmt mit, welche Gedächtnisstelle gelesen wird`,Z_WRITE:`bestimmt mit, welche Gedächtnisstelle oder welcher Wert gespeichert wird`,GATE:`beeinflusst ${Number(edge.target_port)===0?'das weitergeleitete Signal':'die Schaltbedingung'}`,EQ:'liefert einen Operanden für den Gleichheitsvergleich',ADD:'fließt in die Addition ein',SUB:'fließt in die Subtraktion ein',XOR:'fließt in die XOR-Verknüpfung ein',PAUSE:'endet an diesem Haltepunkt'}[target.kind]||`wird an Eingang ${Number(edge.target_port)+1} von ${target.kind} weitergegeben`);
      const emptyInspector=()=>{inspector.innerHTML='<div class="genome-node-empty"><span>⌬</span><b>Funktionspunkt auswählen</b><p>Hier erscheint, was der Punkt verarbeitet und welche Wirkung seine Verbindungen haben können.</p></div>'};
      const resetFocus = () => { svg.classList.remove('has-genome-focus'); nodes.forEach(node => node.classList.remove('is-selected','is-related','is-dimmed')); edges.forEach(edge => edge.classList.remove('is-related','is-dimmed')); focusLabel.textContent='Modul anklicken, um Beziehungen zu fokussieren';emptyInspector(); };
      const focusNode = node => {
        const id = node.dataset.node, related = new Set([id]);
        edges.forEach(edge => { const active=edge.dataset.source===id||edge.dataset.target===id;edge.classList.toggle('is-related',active);edge.classList.toggle('is-dimmed',!active);if(active){related.add(edge.dataset.source);related.add(edge.dataset.target)}});
        nodes.forEach(item => { const selected=item.dataset.node===id, connected=related.has(item.dataset.node);item.classList.toggle('is-selected',selected);item.classList.toggle('is-related',connected&&!selected);item.classList.toggle('is-dimmed',!connected)});
        svg.classList.add('has-genome-focus');
        focusLabel.textContent=`Modul #${id} · ${related.size-1} direkte Beziehungen`;
        const selected=nodeData.get(id),incoming=entity.genome.edges.filter(edge=>String(edge.target)===id),outgoing=entity.genome.edges.filter(edge=>String(edge.source)===id);
        const link=(edge,direction)=>{const other=nodeData.get(String(direction==='in'?edge.source:edge.target));return other?`<button type="button" data-inspect-node="${other.id}"><small>${direction==='in'?`Eingang ${Number(edge.target_port)+1} · von`:`Ausgang ${Number(edge.source_port)+1} · zu`}</small><b>#${other.id} · ${other.kind}</b>${direction==='out'?`<span>${consequence(other,edge)}</span>`:''}</button>`:''};
        const effects=[intrinsicEffects[selected.kind],...outgoing.map(edge=>{const target=nodeData.get(String(edge.target));return target?consequence(target,edge):''})].filter(Boolean);
        inspector.innerHTML=`<small class="genome-node-kicker">EVE · FUNCTION TRACE</small><h3>#${id} · ${selected.kind}</h3>${selected.constant!==null&&selected.constant!==undefined?`<div class="genome-node-value"><small>Erblicher Wert</small><b>${selected.constant}</b></div>`:''}<p class="genome-node-description">${descriptions[selected.kind]||'Verarbeitet Signale innerhalb des Genomnetzwerks.'}</p><section><h4>Eingänge <span>${incoming.length}</span></h4><div class="genome-node-flow">${incoming.map(edge=>link(edge,'in')).join('')||'<p>Keine eingehende Verbindung.</p>'}</div></section><section><h4>Weiterleitung <span>${outgoing.length}</span></h4><div class="genome-node-flow">${outgoing.map(edge=>link(edge,'out')).join('')||'<p>Keine ausgehende Verbindung.</p>'}</div></section><div class="genome-consequence"><small>HAT STRUKTURELL ZUR FOLGE, DASS</small><strong>${effects.length?effects.join('; '):'das Signal an diesem Punkt nicht weitergeführt wird'}.</strong><p>Ob und wie stark diese Wirkung im Lauf eintritt, hängt von Eingangswerten, Aktivierung und Umweltzustand ab.</p></div>`;
        inspector.querySelectorAll('[data-inspect-node]').forEach(button=>button.onclick=()=>{const target=nodes.find(item=>item.dataset.node===button.dataset.inspectNode);if(target)focusNode(target)});
      };
      nodes.forEach(node => { node.addEventListener('click',event=>{event.stopPropagation();focusNode(node)});node.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();focusNode(node)}}) });
      const initial=svg.viewBox.baseVal,baseView={x:initial.x,y:initial.y,w:initial.width,h:initial.height};let view={...baseView},genomeDrag=null,suppressGenomeClick=false;
      const applyView=()=>{svg.setAttribute('viewBox',`${view.x} ${view.y} ${view.w} ${view.h}`);zoomLabel.textContent=`Zoom ${(baseView.w/view.w).toFixed(baseView.w/view.w<2?1:0)}×`};
      const clampView=()=>{const marginX=baseView.w*.08,marginY=baseView.h*.08;view.x=Math.max(baseView.x-marginX,Math.min(baseView.x+baseView.w-view.w+marginX,view.x));view.y=Math.max(baseView.y-marginY,Math.min(baseView.y+baseView.h-view.h+marginY,view.y))};
      const zoomAt=(factor,clientX=null,clientY=null)=>{const rect=svg.getBoundingClientRect(),rx=clientX===null ? .5 : (clientX-rect.left)/rect.width,ry=clientY===null ? .5 : (clientY-rect.top)/rect.height,anchorX=view.x+rx*view.w,anchorY=view.y+ry*view.h,newW=Math.max(baseView.w/64,Math.min(baseView.w,view.w*factor)),newH=newW*baseView.h/baseView.w;view={x:anchorX-rx*newW,y:anchorY-ry*newH,w:newW,h:newH};clampView();applyView()};
      workspace.querySelector('[data-genome-zoom="in"]').onclick=()=>zoomAt(.72);workspace.querySelector('[data-genome-zoom="out"]').onclick=()=>zoomAt(1/.72);workspace.querySelector('[data-genome-reset]').onclick=()=>{view={...baseView};applyView()};
      svg.addEventListener('wheel',event=>{event.preventDefault();zoomAt(event.deltaY<0 ? .82 : 1/.82,event.clientX,event.clientY)},{passive:false});
      svg.addEventListener('pointerdown',event=>{if(event.target.closest?.('[data-node]'))return;genomeDrag={pointerId:event.pointerId,x:event.clientX,y:event.clientY,startX:view.x,startY:view.y,moved:false};svg.setPointerCapture(event.pointerId);svg.classList.add('is-panning');event.preventDefault()});
      svg.addEventListener('pointermove',event=>{if(!genomeDrag)return;const rect=svg.getBoundingClientRect(),dx=event.clientX-genomeDrag.x,dy=event.clientY-genomeDrag.y;view.x=genomeDrag.startX-dx/rect.width*view.w;view.y=genomeDrag.startY-dy/rect.height*view.h;if(Math.hypot(dx,dy)>4){genomeDrag.moved=true;suppressGenomeClick=true}clampView();applyView()});
      const finishGenomeDrag=event=>{if(!genomeDrag||event.pointerId!==genomeDrag.pointerId)return;const moved=genomeDrag.moved;genomeDrag=null;svg.classList.remove('is-panning');if(svg.hasPointerCapture(event.pointerId))svg.releasePointerCapture(event.pointerId);if(moved)setTimeout(()=>{suppressGenomeClick=false},0)};svg.addEventListener('pointerup',finishGenomeDrag);svg.addEventListener('pointercancel',finishGenomeDrag);
      svg.addEventListener('click',event=>{if(suppressGenomeClick){suppressGenomeClick=false;return}if(event.target.closest?.('[data-node]'))return;resetFocus()});
      this.setView('genome');
    },
    async showGenomeComparison(childId, parentId) {
      const workspace=document.querySelector('#genome-workspace');
      this.setView('genome');
      workspace.className='genome-workspace genome-compare-workspace panel';
      workspace.innerHTML='<div class="genome-compare-loading">Vererbungsweg wird rekonstruiert …</div>';
      try {
        const data=await fetch(`/api/genome-compare?parent=${parentId}&child=${childId}`,{cache:'no-store'}).then(response=>response.json());
        if(data.error)throw Error(data.error);
        const safe=value=>String(value??'—').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
        const parentNodes=new Map(data.parent.genome.nodes.map(node=>[Number(node.id),node])),allParentNodes=new Map(Object.entries(data.parent_genomes||{}).map(([id,item])=>[Number(id),new Map(item.genome.nodes.map(node=>[Number(node.id),node]))])),childNodes=new Map(data.child.genome.nodes.map(node=>[Number(node.id),node])),fragments=data.trace.inherited_fragments||[],origin=new Map(),selectedSources=new Set(),selectedEdgeKeys=new Set(),selectedOriginalEdgeKeys=new Set(),otherEdgeKeys=new Set();
        const edgeKey=edge=>`${edge.source}.${edge.source_port}>${edge.target}.${edge.target_port}`;
        fragments.forEach(fragment=>{const mapping=new Map(Object.entries(fragment.node_mapping||{}).map(([source,target])=>[Number(source),Number(target)]));mapping.forEach((target,source)=>{origin.set(target,{parentId:Number(fragment.parent_id),source});if(Number(fragment.parent_id)===Number(parentId))selectedSources.add(source)});(fragment.edges||[]).forEach(edge=>{const mapped={source:mapping.get(Number(edge.source)),source_port:edge.source_port,target:mapping.get(Number(edge.target)),target_port:edge.target_port};if(mapped.source&&mapped.target){if(Number(fragment.parent_id)===Number(parentId)){selectedEdgeKeys.add(edgeKey(mapped));selectedOriginalEdgeKeys.add(edgeKey(edge))}else otherEdgeKeys.add(edgeKey(mapped))}})});
        const mutation=data.trace.mutation||null,nodeStatus=new Map();
        data.child.genome.nodes.forEach(node=>{const inherited=origin.get(Number(node.id));if(!inherited){nodeStatus.set(Number(node.id),'new');return}if(inherited.parentId!==Number(parentId)){nodeStatus.set(Number(node.id),'other');return}const source=parentNodes.get(inherited.source),changed=!source||source.kind!==node.kind||source.constant!==node.constant||mutation?.class==='node'&&Number(mutation.node_id)===Number(node.id);nodeStatus.set(Number(node.id),changed?'modified':'inherited')});
        const lostNodes=data.parent.genome.nodes.filter(node=>!selectedSources.has(Number(node.id))),edgeStatus=new Map();data.child.genome.edges.forEach(edge=>edgeStatus.set(edgeKey(edge),selectedEdgeKeys.has(edgeKey(edge))?'inherited':otherEdgeKeys.has(edgeKey(edge))?'other':'new'));const lostEdges=data.parent.genome.edges.filter(edge=>!selectedOriginalEdgeKeys.has(edgeKey(edge)));
        const cols=7,dx=154,dy=104,width=Math.max(980,cols*dx),rows=Math.ceil(data.child.genome.nodes.length/cols),height=Math.max(430,rows*dy+115),positions=new Map(data.child.genome.nodes.map((node,index)=>[Number(node.id),{x:82+(index%cols)*dx,y:76+Math.floor(index/cols)*dy}]));
        const paths=data.child.genome.edges.map(edge=>{const a=positions.get(Number(edge.source)),b=positions.get(Number(edge.target));if(!a||!b)return'';const status=edgeStatus.get(edgeKey(edge))||'new',bend=Math.max(25,Math.abs(b.y-a.y)*.4);return`<path class="compare-edge ${status}" data-compare-edge="${safe(edgeKey(edge))}" data-status="${status}" d="M${a.x} ${a.y+25} C${a.x} ${a.y+bend} ${b.x} ${b.y-bend} ${b.x} ${b.y-25}"/>`}).join('');
        const boxes=data.child.genome.nodes.map(node=>{const p=positions.get(Number(node.id)),status=nodeStatus.get(Number(node.id)),source=origin.get(Number(node.id));return`<g class="compare-node ${status}" data-compare-node="${node.id}" data-status="${status}" tabindex="0"><circle cx="${p.x}" cy="${p.y}" r="34"/><rect x="${p.x-59}" y="${p.y-25}" width="118" height="50" rx="9"/><text class="compare-id" x="${p.x-48}" y="${p.y-6}">#${node.id}</text><text x="${p.x}" y="${p.y+8}">${safe(node.kind)}</text>${node.constant!==null?`<text class="compare-value" x="${p.x}" y="${p.y+20}">${safe(node.constant)}</text>`:''}<title>${status} · Kind #${node.id}${source?` · Quelle #${source.source}`:''}</title></g>`}).join('');
        const parentOptions=(data.parents||[]).map(id=>{const known=window.eveV04Entities?.find(entity=>Number(entity.id)===Number(id));return`<option value="${id}" ${Number(id)===Number(parentId)?'selected':''}>${safe(known?.name||`Amöbe #${id}`)} · #${id}</option>`}).join('');
        const counts={inherited:[...nodeStatus.values()].filter(value=>value==='inherited').length,modified:[...nodeStatus.values()].filter(value=>value==='modified').length,other:[...nodeStatus.values()].filter(value=>value==='other').length,new:[...nodeStatus.values()].filter(value=>value==='new').length,lost:lostNodes.length};
        workspace.innerHTML=`<header class="genome-compare-head"><div><small>EVE · GENETIC INHERITANCE</small><h3>${safe(data.parent.name)} <span>→</span> ${safe(data.child.name)}</h3><p>Direkter Eltern-Kind-Vergleich · ${data.evidence==='recorded'?'Herkunft aus protokollierter Rekombination':'Herkunft strukturell abgeleitet'}</p></div><div><label>Elternteil<select data-compare-parent>${parentOptions}</select></label><button data-compare-close>Einzelgenom</button></div></header><section class="genome-delta-strip"><div><small>Genomgröße</small><b>${data.parent.n_g} → ${data.child.n_g}</b><span>${data.child.n_g-data.parent.n_g>=0?'+':''}${data.child.n_g-data.parent.n_g}</span></div><div class="inherited"><small>Unverändert geerbt</small><b>${counts.inherited}</b></div><div class="modified"><small>Verändert</small><b>${counts.modified}</b></div><div class="other"><small>Anderer Elternteil</small><b>${counts.other}</b></div><div class="new"><small>Neu</small><b>${counts.new}</b></div><div class="lost"><small>Nicht übernommen</small><b>${counts.lost}</b></div></section><div class="genome-compare-toolbar"><div class="genome-compare-legend"><button class="active inherited" data-compare-filter="inherited"><i></i>unverändert</button><button class="active modified" data-compare-filter="modified"><i></i>verändert</button><button class="active other" data-compare-filter="other"><i></i>anderer Elternteil</button><button class="active new" data-compare-filter="new"><i></i>neu</button><button class="active lost" data-compare-filter="lost"><i></i>verloren</button></div><span>Klick auf ein Modul öffnet den Herkunftsbefund</span></div><div class="genome-compare-layout"><div class="genome-compare-stage"><svg class="genome-compare-graph" viewBox="0 0 ${width} ${height}" role="img"><defs><pattern id="compare-grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="rgba(65,157,222,.075)"/></pattern></defs><rect width="100%" height="100%" fill="url(#compare-grid)"/><g class="compare-edges">${paths}</g><g class="compare-nodes">${boxes}</g></svg><section class="lost-genome-fragments"><header><small>NICHT IN DAS KIND ÜBERNOMMEN</small><span>${lostNodes.length} Funktionspunkte · ${lostEdges.length} Verbindungen</span></header><div>${lostNodes.map(node=>`<button data-lost-node="${node.id}" data-status="lost"><b>#${node.id} ${safe(node.kind)}</b><small>${node.constant===null?'ohne erblichen Wert':`Wert ${safe(node.constant)}`}</small></button>`).join('')||'<p class="empty">Das gesamte Elterngenom wurde übernommen.</p>'}</div></section></div><aside class="genome-diff-inspector"><div class="genome-diff-empty"><span>⌬</span><b>Unterschied auswählen</b><p>Die Karte zeigt das Genom des Kindes. Nicht übernommene Teile stehen darunter.</p></div></aside></div>`;
        const parameterNames={activity_base:'A₀ Basisaktivität',knock_capacity:'Nₖ Klingelkapazität',bond_ticks:'Tₚ Bindungszeit'},parameterStrip=document.createElement('section');parameterStrip.className='genome-parameter-deltas';parameterStrip.innerHTML=Object.entries(parameterNames).map(([key,label])=>{const before=data.parent.genome[key],after=data.child.genome[key],changed=before!==after,sourceKey={activity_base:'activity_parent_id',knock_capacity:'knock_capacity_parent_id',bond_ticks:'bond_ticks_parent_id'}[key],source=data.trace[sourceKey];return`<button class="${changed?'changed':'stable'}" data-parameter="${key}"><small>${label}</small><b>${before} → ${after}</b><span>${source?`geerbt von #${source}`:'Herkunft nicht protokolliert'}</span></button>`}).join('');workspace.querySelector('.genome-delta-strip').after(parameterStrip);
        const compareTools=document.createElement('div');compareTools.className='genome-compare-zoom';compareTools.innerHTML='<button data-compare-zoom="out">−</button><button data-compare-zoom="in">+</button><button data-compare-reset>Gesamt</button><span>Zoom 1×</span>';workspace.querySelector('.genome-compare-toolbar').append(compareTools);const compareSvg=workspace.querySelector('.genome-compare-graph'),baseView={x:0,y:0,w:width,h:height};let compareView={...baseView},compareDrag=null;const applyCompareView=()=>{compareSvg.setAttribute('viewBox',`${compareView.x} ${compareView.y} ${compareView.w} ${compareView.h}`);compareTools.querySelector('span').textContent=`Zoom ${(baseView.w/compareView.w).toFixed(baseView.w/compareView.w<2?1:0)}×`},clampCompare=()=>{compareView.x=Math.max(0,Math.min(baseView.w-compareView.w,compareView.x));compareView.y=Math.max(0,Math.min(baseView.h-compareView.h,compareView.y))},zoomCompare=(factor,cx=null,cy=null)=>{const rect=compareSvg.getBoundingClientRect(),rx=cx===null?.5:(cx-rect.left)/rect.width,ry=cy===null?.5:(cy-rect.top)/rect.height,ax=compareView.x+rx*compareView.w,ay=compareView.y+ry*compareView.h,nw=Math.max(baseView.w/32,Math.min(baseView.w,compareView.w*factor)),nh=Math.max(baseView.h/32,Math.min(baseView.h,compareView.h*factor));compareView={x:ax-rx*nw,y:ay-ry*nh,w:nw,h:nh};clampCompare();applyCompareView()};compareTools.querySelector('[data-compare-zoom="in"]').onclick=()=>zoomCompare(.72);compareTools.querySelector('[data-compare-zoom="out"]').onclick=()=>zoomCompare(1/.72);compareTools.querySelector('[data-compare-reset]').onclick=()=>{compareView={...baseView};applyCompareView()};compareSvg.addEventListener('wheel',event=>{event.preventDefault();zoomCompare(event.deltaY<0?.82:1/.82,event.clientX,event.clientY)},{passive:false});compareSvg.addEventListener('pointerdown',event=>{if(event.target.closest('[data-compare-node]'))return;compareDrag={id:event.pointerId,x:event.clientX,y:event.clientY,vx:compareView.x,vy:compareView.y};compareSvg.setPointerCapture(event.pointerId);compareSvg.classList.add('panning')});compareSvg.addEventListener('pointermove',event=>{if(!compareDrag)return;const rect=compareSvg.getBoundingClientRect();compareView.x=compareDrag.vx-(event.clientX-compareDrag.x)/rect.width*compareView.w;compareView.y=compareDrag.vy-(event.clientY-compareDrag.y)/rect.height*compareView.h;clampCompare();applyCompareView()});const stopCompareDrag=event=>{if(!compareDrag||event.pointerId!==compareDrag.id)return;compareDrag=null;compareSvg.classList.remove('panning')};compareSvg.addEventListener('pointerup',stopCompareDrag);compareSvg.addEventListener('pointercancel',stopCompareDrag);
        const inspector=workspace.querySelector('.genome-diff-inspector'),statusLabel={inherited:'Unverändert geerbt',modified:'Verändert geerbt',other:'Vom anderen Elternteil',new:'Neu im Kind',lost:'Nicht übernommen'};
        const inspect=(status,node,source=null)=>{const mutationHit=mutation?.class==='node'&&Number(mutation.node_id)===Number(node.id),parentNode=source?allParentNodes.get(Number(source.parentId))?.get(Number(source.source)):null;inspector.innerHTML=`<small>EVE · INHERITANCE DETAIL</small><h3>${statusLabel[status]}</h3><div class="diff-status ${status}">${safe(node.kind)} · #${node.id}</div>${parentNode?`<div class="node-diff"><span><small>Eltern #${source.parentId} · Modul #${source.source}</small><b>${safe(parentNode.kind)}</b><em>${parentNode.constant===null?'—':safe(parentNode.constant)}</em></span><i>→</i><span><small>Kind · Modul #${node.id}</small><b>${safe(node.kind)}</b><em>${node.constant===null?'—':safe(node.constant)}</em></span></div>`:''}<p>${status==='inherited'?'Funktionsart und erblicher Wert wurden nachweislich unverändert übernommen.':status==='modified'?`Das Modul stammt nachweislich von diesem Elternteil und wurde verändert.${mutationHit?' Die gespeicherte Mutation betrifft genau dieses Modul.':''}`:status==='other'?`Die gespeicherte Rekombination ordnet dieses Modul Elternteil #${source?.parentId} zu.`:status==='new'?'Für dieses Modul existiert keine gespeicherte Elternzuordnung. Es ist neu oder die Provenienz ist unvollständig.':'Dieses Modul des gewählten Elternteils wurde nicht in das Kind übernommen.'}</p><dl><div><dt>Beleg</dt><dd>${data.evidence==='recorded'?'Rekombinationsprotokoll':'Strukturvergleich'}</dd></div>${mutationHit?`<div><dt>Mutation</dt><dd>${safe(mutation.class)}</dd></div>`:''}</dl>`};
        workspace.querySelectorAll('[data-compare-node]').forEach(group=>group.onclick=()=>{const node=childNodes.get(Number(group.dataset.compareNode)),source=origin.get(node.id);inspect(group.dataset.status,node,source)});workspace.querySelectorAll('[data-lost-node]').forEach(button=>button.onclick=()=>inspect('lost',parentNodes.get(Number(button.dataset.lostNode))));
        workspace.querySelectorAll('[data-parameter]').forEach(button=>button.onclick=()=>{const key=button.dataset.parameter,before=data.parent.genome[key],after=data.child.genome[key],sourceKey={activity_base:'activity_parent_id',knock_capacity:'knock_capacity_parent_id',bond_ticks:'bond_ticks_parent_id'}[key],source=data.trace[sourceKey];inspector.innerHTML=`<small>EVE · HERITABLE PARAMETER</small><h3>${safe(parameterNames[key])}</h3><div class="node-diff"><span><small>Elternteil #${parentId}</small><b>${before}</b></span><i>→</i><span><small>Kind #${childId}</small><b>${after}</b></span></div><p>${source?`Das Rekombinationsprotokoll ordnet den Wert Elternteil #${source} zu.`:'Für diesen Parameter ist keine Herkunft protokolliert.'}${before!==after?' Der Wert unterscheidet sich im direkten Vergleich.':' Der Wert blieb gegenüber dem gewählten Elternteil stabil.'}</p>`});
        workspace.querySelectorAll('[data-compare-filter]').forEach(button=>button.onclick=()=>{button.classList.toggle('active');const status=button.dataset.compareFilter,visible=button.classList.contains('active');workspace.querySelectorAll(`[data-status="${status}"],.${status}.compare-edge`).forEach(element=>element.classList.toggle('compare-hidden',!visible))});
        workspace.querySelector('[data-compare-parent]').onchange=event=>this.showGenomeComparison(childId,Number(event.target.value));workspace.querySelector('[data-compare-close]').onclick=()=>{const entity=window.eveV04Entities?.find(item=>Number(item.id)===Number(childId));if(entity)this.showGenome(entity)};requestAnimationFrame(()=>window.scrollTo({top:0,behavior:'auto'}));
      } catch(error) { workspace.innerHTML=`<p class="error">Genomvergleich konnte nicht geladen werden: ${String(error.message||error)}</p>`; }
    },
    renderEntityBrowser(entities, target) {
      window.eveV04Entities = entities;
      const byId = new Map(entities.map(entity => [entity.id, entity]));
      const generations = new Map();
      const generationOf = entity => {
        if (generations.has(entity.id)) return generations.get(entity.id);
        const parents = (entity.parents || []).map(id => byId.get(id)).filter(Boolean);
        const generation = parents.length ? 1 + Math.max(...parents.map(generationOf)) : 0;
        generations.set(entity.id, generation);
        return generation;
      };
      const safe=value=>String(value??'—').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
      const allEvents=typeof activityEvents==='undefined'?[]:activityEvents;
      const eventFor=(entity,event)=>Number(event.entity_id)===entity.id||(event.parents||[]).map(Number).includes(entity.id)||Number(event.target_id)===entity.id;
      const reproductionState=entity=>{const genome=entity.genome||{},edges=genome.edges||[],writers=(genome.nodes||[]).filter(node=>node.kind==='MEM_WRITE'),required=['offset','slot','value'],operational=writers.some(node=>{const ports=new Set(edges.filter(edge=>Number(edge.target)===Number(node.id)).map(edge=>String(edge.target_port)));return required.every(port=>ports.has(port))});return{operational,label:operational?'fortpflanzungsfähig':'steril',reason:operational?'vollständig verdrahtetes MEM_WRITE':'kein vollständig verdrahtetes MEM_WRITE'}};
      const labelFor=event=>({birth:'Geburt',death:'Tod',corpse_scavenged:'Leiche verwertet',ram_read:'RAM gelesen',ram_write:'RAM geschrieben',environment_change:'Umwelt',knock:'Kontakt',reproduction_cost:'Nachkomme',birth_rejected:'Geburt abgewiesen',mem_write:'Bindung',mem_write_rejected:'Bindung abgewiesen',genome_created:'Genomänderung'}[event.kind]||String(event.kind||'Ereignis').replaceAll('_',' '));
      const toneFor=event=>event.kind==='death'||event.kind.endsWith?.('rejected')?'danger':event.kind==='birth'||event.kind==='reproduction_cost'?'birth':event.kind==='ram_read'||event.kind==='ram_write'?'ram':event.kind.includes?.('genome')?'mutation':'signal';
      const description=event=>{try{return typeof describe==='function'?describe(event):labelFor(event)}catch(_error){return labelFor(event)}};
      const childIds=entity=>entities.filter(item=>(item.parents||[]).map(Number).includes(entity.id)).map(item=>item.id);
      // Mehrere Amöben mit Komma suchen bleibt der dokumentierte Suchvertrag.
      target.innerHTML = `<div class="history-desk"><header class="history-desk-head"><div><small>EVE · INDIVIDUAL ANALYSIS</small><h2>Amöben-Desk</h2><p>Lebenslinien lesen, Beziehungen verfolgen und bei Bedarf bis zum Einzelereignis vertiefen.</p></div><span>${entities.length} Individuen in der Auswahl</span></header><div class="amoeba-browser"><section class="amoeba-list-panel panel"><div class="amoeba-list-tools"><input type="search" placeholder="Ada, Vera, #24 …" aria-label="Amöben suchen"><select aria-label="Amöben sortieren"><option value="id">ID</option><option value="generation">Generation</option><option value="energy">Energie</option><option value="name">Name</option></select></div><div class="amoeba-search-state" hidden><div class="amoeba-search-chips"></div><span class="amoeba-search-missing"></span></div><div class="amoeba-list"><div class="amoeba-row header"><span>Individuum</span><span>Gen.</span><span>Status</span><span>Energie</span></div><div class="amoeba-list-rows">${entities.map(entity => `<button class="amoeba-row" type="button" data-entity-row="${entity.id}" data-generation="${generationOf(entity)}" data-energy="${Number(entity.energy)}" data-name="${safe(entity.name||'')}" data-search="${safe(`${entity.name||''} #${entity.id}`.toLocaleLowerCase('de'))}"><span><i></i>${safe(entity.name || `Amöbe #${entity.id}`)} <small>#${entity.id}</small></span><span>${generationOf(entity)}</span><span class="${entity.alive ? 'status-live' : 'status-dead'}">${entity.alive ? 'lebend' : 'tot'}</span><span>${Number(entity.energy).toFixed(1)}</span></button>`).join('')}</div></div></section><section class="amoeba-detail"><div class="amoeba-detail-empty panel"><div>Wähle links eine Amöbe aus.</div></div></section></div></div>`;
      const detail = target.querySelector('.amoeba-detail');
      entities.forEach(entity=>{const fertility=reproductionState(entity);if(fertility.operational)return;const status=target.querySelector(`[data-entity-row="${entity.id}"] span:nth-child(3)`);if(status)status.insertAdjacentHTML('beforeend','<small class="status-sterile">steril</small>')});
      const selectEntity = id => {
        const entity = byId.get(id); if (!entity) return;
        target.querySelectorAll('[data-entity-row]').forEach(row => row.classList.toggle('active', Number(row.dataset.entityRow) === id));
        const events=allEvents.filter(event=>eventFor(entity,event)).sort((a,b)=>a.tick-b.tick),children=childIds(entity),born=Number(entity.born_at||0),died=events.find(event=>event.kind==='death'&&Number(event.entity_id)===id)?.tick??null,end=died??Math.max(born,typeof maxTick==='function'?maxTick():born),life=Math.max(0,end-born),ram=events.filter(event=>event.kind==='ram_read'||event.kind==='ram_write'),reads=ram.filter(event=>event.kind==='ram_read'),writes=ram.filter(event=>event.kind==='ram_write'),reward=reads.reduce((sum,event)=>sum+Number(event.reward||0),0),addresses=new Set(ram.map(event=>event.address).filter(value=>value!==undefined)),important=events.filter(event=>['birth','death','corpse_scavenged','knock','reproduction_cost','genome_created','mem_write','environment_change'].includes(event.kind)||(event.kind==='ram_read'&&event.discovery_type));
        const fertility=reproductionState(entity);
        const markerEvents=important.filter(event=>event.tick!==born),markerStride=Math.max(1,Math.ceil(markerEvents.length/18)),markers=[{tick:born,kind:'birth',label:'Geburt'},...markerEvents.filter((event,index)=>index%markerStride===0||index===markerEvents.length-1)];if(entity.alive)markers.push({tick:end,kind:'now',label:'Auswahl'});
        const eventButton=(event,index)=>`<button type="button" class="history-event ${toneFor(event)}" data-event-index="${index}"><span>Tick ${Number(event.tick).toLocaleString()}</span><b>${safe(labelFor(event))}</b><small>${safe(description(event))}</small></button>`;
        detail.innerHTML=`<article class="amoeba-dossier panel"><header class="amoeba-dossier-head"><div><small>GEN ${generationOf(entity)} · AMÖBE #${entity.id}</small><h2>${safe(entity.name||`Amöbe #${entity.id}`)}</h2><p>${entity.alive?'Lebende Linie':'Abgeschlossene Lebenslinie'} · Tick ${born}–${died??'heute'} · Eltern ${(entity.parents||[]).map(parent=>`#${parent}`).join(', ')||'Gründerpopulation'}</p></div><div class="amoeba-dossier-actions"><button data-life-replay>▶ Lebensfilm</button><button data-open-lineage>⑂ Stammbaum</button><button data-open-genome>⌬ Genom</button></div></header><div class="amoeba-telemetry"><div><small>Status</small><strong class="${entity.alive?'live':'dead'}">${entity.alive?'lebend':'tot'}</strong></div><div><small>Lebensdauer</small><strong>${life} Ticks</strong></div><div><small>Energie</small><strong>${Number(entity.energy).toFixed(2)}</strong></div><div><small>Genom</small><strong>${entity.n_g} G</strong><span>${entity.n_f} F + ${entity.n_p} P</span></div><div><small>Kinder</small><strong>${children.length}</strong></div><div><small>RAM-Kontakte</small><strong>${ram.length}</strong></div></div><section class="amoeba-life-track"><header><div><small>PERSÖNLICHE ZEITACHSE</small><b>Tick ${born}–${end}</b></div><span>Markierung anklicken für Befund</span></header><div class="life-track"><i></i>${markers.map((event,index)=>{const position=life?Math.max(0,Math.min(100,(Number(event.tick)-born)/life*100)):0;return`<button type="button" class="life-marker ${toneFor(event)}" style="--life-x:${position}%" data-marker-index="${index}" title="Tick ${event.tick} · ${safe(labelFor(event))}"><span>${index===0?'◆':event.kind==='death'?'×':'●'}</span></button>`}).join('')}</div><div class="life-track-labels"><span>Geburt · ${born}</span><span>${entity.alive?'Auswahl':'Tod'} · ${end}</span></div></section><nav class="amoeba-tabs" aria-label="Analysen"><button class="active" data-dossier-tab="life">Lebenslauf <span>${important.length}</span></button><button data-dossier-tab="environment">Umwelt <span>${addresses.size}</span></button><button data-dossier-tab="evolution">Evolution <span>${children.length}</span></button><button data-dossier-tab="raw">Rohdaten <span>${events.length}</span></button></nav><div class="amoeba-analysis-layout"><div class="amoeba-tab-content"><section data-tab-panel="life"><header class="analysis-section-head"><div><small>EVE · LIFE STREAM</small><h3>Prägende Ereignisse</h3></div><span>verdichtet auf biologisch relevante Spuren</span></header><div class="history-event-stream">${important.length?important.slice(-40).reverse().map((event,index)=>eventButton(event,events.indexOf(event))).join(''):'<p class="empty">Keine prägenden Ereignisse protokolliert.</p>'}</div></section><section data-tab-panel="environment" hidden><header class="analysis-section-head"><div><small>EVE · ENVIRONMENT</small><h3>Umweltprofil</h3></div><span>${addresses.size} besuchte Adressen</span></header><div class="environment-orbit"><div><small>Lesen</small><b>${reads.length}</b></div><div><small>Schreiben</small><b>${writes.length}</b></div><div><small>RAM-Energie</small><b>+${reward.toFixed(2)}</b></div></div><div class="history-event-stream">${ram.length?ram.slice(-30).reverse().map(event=>eventButton(event,events.indexOf(event))).join(''):'<p class="empty">Keine Umweltkontakte in der Auswahl.</p>'}</div></section><section data-tab-panel="evolution" hidden><header class="analysis-section-head"><div><small>EVE · LINEAGE</small><h3>Evolutionäre Beziehungen</h3></div><span>Generation ${generationOf(entity)}</span></header><div class="evolution-relations"><div><small>Vorfahren</small><b>${(entity.parents||[]).length}</b><p>${(entity.parents||[]).map(parent=>byId.get(parent)?.name||`#${parent}`).join(' · ')||'Gründeramöbe'}</p></div><div class="selected"><small>Fokus</small><b>${safe(entity.name||`#${id}`)}</b><p>Genom ${entity.n_g} · A₀ ${entity.activity_base}</p></div><div><small>Direkte Kinder</small><b>${children.length}</b><p>${children.slice(0,8).map(child=>byId.get(child)?.name||`#${child}`).join(' · ')||'keine'}</p></div></div><div class="evolution-actions"><button data-open-lineage>Verwandtschaft in der Zeitlandschaft öffnen</button><button data-open-genome>Genomtopologie studieren</button></div></section><section data-tab-panel="raw" hidden><header class="analysis-section-head"><div><small>EVE · RAW OBSERVATIONS</small><h3>Protokollierte Einzelereignisse</h3></div><span>vollständige Tiefe · ${events.length} Einträge</span></header><div class="history-event-stream raw">${events.length?events.slice().reverse().map((event,index)=>eventButton(event,events.length-1-index)).join(''):'<p class="empty">Keine Einzelereignisse protokolliert.</p>'}</div></section></div><aside class="history-inspector"><button class="history-inspector-close" title="Detail schließen">×</button><div class="history-inspector-empty"><span>⌁</span><b>Detailinspektor</b><p>Wähle einen Punkt der Lebenslinie oder ein Ereignis.</p></div></aside></div></article>`;
        const reproductionCell=detail.querySelector('.amoeba-telemetry>div:nth-child(5)');
        reproductionCell.innerHTML=`<small>Fortpflanzung</small><strong class="${fertility.operational?'fertile':'sterile'}">${fertility.label}</strong><span>${children.length} Kinder · ${fertility.reason}</span>`;
        if(!entity.alive){const statusCell=detail.querySelector('.amoeba-telemetry>div:first-child'),scavenged=events.find(event=>event.kind==='corpse_scavenged'&&Number(event.target_id)===entity.id),corpseStatus=entity.corpse_available===true?'Leiche in der RAM-Suppe':scavenged?`Leiche verwertet · Finder #${scavenged.entity_id} · +${Number(scavenged.reward||0).toFixed(2)} Energie`:entity.corpse_available===false?'Leiche nicht mehr in der RAM-Suppe':'Leichenstatus in diesem älteren Lauf nicht protokolliert';statusCell.insertAdjacentHTML('beforeend',`<span>${corpseStatus}</span>`)}
        const signalCard=(label,signal)=>`<div class="memory-cell"><small>${safe(label)}</small><b>${safe(signal?.value??'—')}</b><span>${safe((signal?.sources||[]).join(' · ')||'ohne Herkunft')}</span>${signal?.originators?.length?`<em>Urheber ${safe(signal.originators.join(', '))}</em>`:''}</div>`;
        const kEntries=Object.entries(entity.k||{}),zEntries=(entity.z||[]).map((signal,index)=>[index,signal]).filter(([,signal])=>signal!==null&&signal!==undefined),memoryButton=document.createElement('button'),memoryPanel=document.createElement('section');
        detail.querySelector('.amoeba-telemetry>div:nth-child(3)').insertAdjacentHTML('beforeend',`<span>S₀ ${Number(entity.start_energy??entity.energy).toFixed(2)}</span>`);
        memoryButton.dataset.dossierTab='memory';memoryButton.innerHTML=`Speicher <span>${kEntries.length+zEntries.length}</span>`;detail.querySelector('[data-dossier-tab="raw"]').before(memoryButton);
        memoryPanel.dataset.tabPanel='memory';memoryPanel.hidden=true;memoryPanel.innerHTML=`<header class="analysis-section-head"><div><small>EVE · INTERNAL STATE</small><h3>Kurzzeit K und Zustand Z</h3></div><span>Zustand am gewählten historischen Zeitpunkt</span></header><div class="memory-summary"><div><small>Startenergie S₀</small><b>${Number(entity.start_energy??entity.energy).toFixed(2)}</b><span>individueller Geburtssockel</span></div><div><small>K belegt</small><b>${kEntries.length}</b><span>flüchtige Eingangsports</span></div><div><small>Z belegt</small><b>${zEntries.length} / ${(entity.z||[]).length}</b><span>dauerhafte Speicherzellen</span></div></div><div class="amoeba-memory-grid"><section><header><div><small>K · KURZZEIT</small><h4>Wartende Eingangssignale</h4></div><span>${kEntries.length}</span></header><div class="memory-cells">${kEntries.length?kEntries.map(([key,signal])=>signalCard(key,signal)).join(''):'<p class="empty">K ist an diesem Zeitpunkt leer.</p>'}</div></section><section><header><div><small>Z · ZUSTAND</small><h4>Dauerhafte Speicherwerte</h4></div><span>${zEntries.length}</span></header><div class="memory-cells">${zEntries.length?zEntries.map(([index,signal])=>signalCard(`Z[${index}]`,signal)).join(''):'<p class="empty">Z enthält noch keine gespeicherten Werte.</p>'}</div></section></div>`;
        detail.querySelector('[data-tab-panel="raw"]').before(memoryPanel);
        const inspector=detail.querySelector('.history-inspector'),openEvent=index=>{const event=events[index];if(!event)return;const fields=Object.entries(event).filter(([key])=>!['tick','kind','entity_id'].includes(key)).slice(0,12);inspector.classList.add('open');inspector.innerHTML=`<button class="history-inspector-close" title="Detail schließen">×</button><small>EVE · EVENT DETAIL</small><h3>${safe(labelFor(event))}</h3><div class="inspector-tick">Tick ${Number(event.tick).toLocaleString()}</div><p>${safe(description(event))}</p><dl>${fields.map(([key,value])=>`<div><dt>${safe(key.replaceAll('_',' '))}</dt><dd>${safe(Array.isArray(value)?value.join(', '):typeof value==='object'?JSON.stringify(value):value)}</dd></div>`).join('')}</dl><button data-sync-tick>◷ Zeitpunkt in Historie wählen</button>`;inspector.querySelector('.history-inspector-close').onclick=()=>inspector.classList.remove('open');inspector.querySelector('[data-sync-tick]').onclick=()=>{const choices=[...document.querySelector('#snap').options].filter(option=>option.value!=='latest');if(!choices.length)return;const nearest=choices.reduce((best,option)=>Math.abs(Number(option.value)-event.tick)<Math.abs(Number(best.value)-event.tick)?option:best,choices[0]);document.querySelector('#snap').value=nearest.value;document.querySelector('#snap').dispatchEvent(new Event('change'))}};
        detail.querySelector('.history-inspector-close').onclick=()=>inspector.classList.remove('open');
        detail.querySelectorAll('[data-event-index]').forEach(button=>button.onclick=()=>openEvent(Number(button.dataset.eventIndex)));
        detail.querySelectorAll('[data-marker-index]').forEach(button=>button.onclick=()=>{const event=markers[Number(button.dataset.markerIndex)];const index=events.indexOf(event);if(index>=0)openEvent(index);else{inspector.classList.add('open');inspector.innerHTML=`<button class="history-inspector-close">×</button><small>EVE · LIFE MARKER</small><h3>${safe(event.label)}</h3><div class="inspector-tick">Tick ${event.tick}</div><p>${event.kind==='birth'?'Beginn dieser Lebenslinie.':'Zustand am Ende der gewählten Historienauswahl.'}</p>`;inspector.querySelector('.history-inspector-close').onclick=()=>inspector.classList.remove('open')}});
        detail.querySelectorAll('[data-dossier-tab]').forEach(button=>button.onclick=()=>{detail.querySelectorAll('[data-dossier-tab]').forEach(item=>item.classList.toggle('active',item===button));detail.querySelectorAll('[data-tab-panel]').forEach(panel=>panel.hidden=panel.dataset.tabPanel!==button.dataset.dossierTab);inspector.classList.remove('open')});
        detail.querySelector('[data-life-replay]').onclick=()=>window.startReplay?.(entity.id);
        detail.querySelectorAll('[data-open-genome]').forEach(button=>button.onclick=()=>this.showGenome(entity));
        detail.querySelectorAll('[data-open-lineage]').forEach(button=>button.onclick=()=>{this.setView('lineage');setTimeout(()=>document.querySelector(`[data-lineage-id="${entity.id}"]`)?.dispatchEvent(new MouseEvent('click',{bubbles:true})),180)});
        const evolutionActions=detail.querySelector('.evolution-actions');
        (entity.parents||[]).forEach(parentId=>{const parent=byId.get(Number(parentId)),button=document.createElement('button');button.className='genome-compare-launch';button.textContent=`⌬ ${parent?.name||`#${parentId}`} → ${entity.name||`#${entity.id}`} vergleichen`;button.onclick=()=>this.showGenomeComparison(entity.id,Number(parentId));evolutionActions.prepend(button)});
      };
      target.querySelectorAll('[data-entity-row]').forEach(row => row.onclick = () => selectEntity(Number(row.dataset.entityRow)));
      const search=target.querySelector('input[type="search"]'),searchState=target.querySelector('.amoeba-search-state'),chips=target.querySelector('.amoeba-search-chips'),missing=target.querySelector('.amoeba-search-missing'),sort=target.querySelector('.amoeba-list-tools select'),rows=target.querySelector('.amoeba-list-rows');
      search.oninput = () => {
        const terms=[...new Set(search.value.split(',').map(term=>term.trim()).filter(Boolean))],normalized=terms.map(term=>term.toLocaleLowerCase('de')),matches=new Map(terms.map(term=>[term,0]));
        target.querySelectorAll('[data-entity-row]').forEach(row=>{const text=row.dataset.search,hits=normalized.map((term,index)=>{const hit=text.includes(term);if(hit)matches.set(terms[index],matches.get(terms[index])+1);return hit});row.hidden=terms.length>0&&!hits.some(Boolean)});
        searchState.hidden=!terms.length;chips.innerHTML=terms.map(term=>`<button type="button" data-search-term="${safe(term)}">${safe(term)} <span>×</span></button>`).join('');const absent=terms.filter(term=>matches.get(term)===0);missing.textContent=absent.length?`Nicht gefunden: ${absent.join(', ')}`:'';
        chips.querySelectorAll('[data-search-term]').forEach(button=>button.onclick=()=>{const remove=button.dataset.searchTerm;search.value=terms.filter(term=>term!==remove).join(', ');search.dispatchEvent(new Event('input'))});
      };
      sort.onchange=()=>{const items=[...rows.children],key=sort.value;items.sort((a,b)=>key==='name'?a.dataset.name.localeCompare(b.dataset.name,'de'):key==='energy'?Number(b.dataset.energy)-Number(a.dataset.energy):key==='generation'?Number(a.dataset.generation)-Number(b.dataset.generation):Number(a.dataset.entityRow)-Number(b.dataset.entityRow));items.forEach(row=>rows.append(row))};
      if (entities.length) { const requested=Number(sessionStorage.getItem('eve-open-entity')),initial=byId.has(requested)?requested:entities[0].id;selectEntity(initial);if(byId.has(requested)){sessionStorage.removeItem('eve-open-entity');requestAnimationFrame(()=>target.querySelector(`[data-entity-row="${requested}"]`)?.scrollIntoView({block:'center'}))} }
    },
    updateZoom(value) {
      const label = document.querySelector('.ram-zoom-label');
      if (label) label.textContent = `Zoom ${value.toFixed(value < 2 ? 1 : 0)}×`;
    },
    signalDataArrival() {
      const now = Date.now();
      if (now - lastDataSignal < 3200) return;
      lastDataSignal = now;
      const soup = document.querySelector('#live-soup');
      if (!soup || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      soup.classList.remove('data-arrival');
      void soup.offsetWidth;
      soup.classList.add('data-arrival');
      setTimeout(() => soup.classList.remove('data-arrival'), 1400);
    }
  };

  let chronicleStarted=false;
  async function initChronicle(){
    if(chronicleStarted)return;chronicleStarted=true;const root=document.querySelector('#chronicle-workspace');
    try{const data=await fetch('/api/chronicle',{cache:'no-store'}).then(response=>response.json());if(data.error)throw Error(data.error);renderChronicle(root,data)}catch(error){chronicleStarted=false;root.innerHTML=`<p class="error">Chronik konnte nicht geladen werden: ${String(error.message||error)}</p>`}
  }
  function renderChronicle(root,data){
    const safe=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char])),runs=data.runs||[],byId=new Map(runs.map(run=>[run.run_id,run]));
    const stateLabel=run=>run.status==='running'?'läuft':run.end_reason==='natural_extinction'?'Extinktion':run.end_reason==='user_requested'?'kontrolliert gestoppt':run.status==='completed'?'abgeschlossen':run.status;
    const statusClass=run=>run.status==='running'?'running':run.end_reason==='natural_extinction'?'extinct':run.end_reason==='user_requested'?'stopped':'complete';
    const recordLabels={peak_population:'Größte Population',longest_run:'Längster Lauf',most_offspring:'Meiste Nachkommen',genome_diversity:'Größte Genomvielfalt',deepest_generation:'Tiefste Generation',energy_gained:'Meiste RAM-Energie'},recordValue=(key,run)=>key==='peak_population'?run.peak_population:key==='longest_run'?`${run.ticks} Ticks`:key==='most_offspring'?run.offspring:key==='genome_diversity'?run.genomes:key==='deepest_generation'?`Generation ${run.deepest_generation}`:Number(run.energy_gained).toFixed(2),amoebaLabels={largest_genome:'Größtes Genom',longest_life:'Längstes Leben',direct_children:'Meiste direkte Kinder',descendants:'Größte Nachkommenschaft',deepest_generation:'Tiefste Generation',highest_energy:'Höchste Energie'},amoebaValue=(key,item)=>key==='largest_genome'?`${item.value} G`:key==='longest_life'?`${item.value} Ticks`:key==='deepest_generation'?`Generation ${item.value}`:key==='highest_energy'?Number(item.value).toFixed(2):item.value;
    root.className='chronicle-workspace';
    root.innerHTML=`<section class="chronicle-summary">${[['Experimente',data.totals.runs],['Nachkommen',data.totals.offspring],['Extinktionen',data.totals.extinctions],['RAM-Energie',Number(data.totals.energy_gained).toFixed(2)]].map(([label,value])=>`<div><small>${label}</small><strong>${value}</strong></div>`).join('')}</section><section class="chronicle-filter panel"><div><small>EVE · ARCHIVE INDEX</small><h3>Run-Signaturen</h3></div><div class="chronicle-version-filter"><button class="active" data-version="all">Alle</button>${(data.totals.versions||[]).map(version=>`<button data-version="${safe(version)}">v${safe(version)}</button>`).join('')}</div></section><section class="chronicle-map panel"><div class="chronicle-axis">${runs.map((run,index)=>`<button type="button" class="chronicle-run ${statusClass(run)}" data-chronicle-run="${run.run_id}" data-version="${safe(run.prototype_version)}" style="--run-index:${index}"><span class="chronicle-orbit"></span><strong>${safe(run.label)}</strong><small>v${safe(run.prototype_version)} · ${run.ticks} Ticks</small><i>${run.peak_population}</i></button>`).join('')}</div></section><section class="chronicle-main"><div class="chronicle-dossier panel"><p class="empty">Wähle eine Run-Signatur aus.</p></div><div class="chronicle-records panel"><small>EVE · ARCHIVE RECORDS</small><h3>Run-Rekorde</h3><div>${Object.entries(data.records||{}).map(([key,run])=>run?`<button type="button" data-record-run="${run.run_id}"><span>${recordLabels[key]||key}</span><b>${safe(run.label)}</b><strong>${recordValue(key,run)}</strong></button>`:'').join('')}</div></div></section><section class="chronicle-hall panel"><header><div><small>EVE · HALL OF LIFE</small><h3>Rekordhalter der Amöben</h3></div><span>Über alle archivierten Runs</span></header><div>${Object.entries(data.amoeba_records||{}).map(([key,item])=>item?`<button type="button" data-hall-run="${item.run_id}" data-hall-entity="${item.entity_id}"><small>${amoebaLabels[key]||key}</small><span class="chronicle-medal">✦</span><b>${safe(item.name)} <i>#${item.entity_id}</i></b><strong>${amoebaValue(key,item)}</strong><em>${safe(item.run_label)} · v${safe(item.prototype_version)}</em></button>`:'').join('')}</div></section><section class="chronicle-compare panel"><header><div><small>EVE · RUN COMPARISON</small><h3>Zwei Experimente vergleichen</h3></div><div><select data-compare-run="a"></select><span>↔</span><select data-compare-run="b"></select></div></header><div class="chronicle-comparison"></div></section>`;
    const archiveDate=value=>value?new Date(value).toLocaleDateString('de-DE',{day:'2-digit',month:'2-digit',year:'2-digit'}):'ohne Datum';
    const runGrid=root.querySelector('.chronicle-axis');
    runGrid.className='chronicle-run-grid';
    root.querySelector('.chronicle-filter h3').textContent='Gespeicherte Läufe';
    const filterLead=root.querySelector('.chronicle-filter>div:first-child');
    filterLead.insertAdjacentHTML('beforeend',`<span class="chronicle-filter-count" data-filter-count>${runs.length} Läufe sichtbar</span>`);
    root.querySelectorAll('.chronicle-version-filter [data-version]').forEach(button=>{const count=button.dataset.version==='all'?runs.length:runs.filter(run=>String(run.prototype_version)===button.dataset.version).length;button.insertAdjacentHTML('beforeend',`<b>${count}</b>`)});
    root.querySelectorAll('[data-chronicle-run]').forEach((button,index)=>{const run=runs[index];button.removeAttribute('style');button.innerHTML=`<span class="chronicle-run-head"><em>v${safe(run.prototype_version)}</em><i class="chronicle-run-state">${safe(stateLabel(run))}</i></span><strong>${safe(run.label)}</strong><small>${archiveDate(run.created_at)} · ${safe(run.run_id.slice(0,8))}</small><span class="chronicle-run-metrics"><span><small>Ticks</small><b>${run.ticks}</b></span><span><small>Maximum</small><b>${run.peak_population}</b></span><span><small>Nachkommen</small><b>${run.offspring}</b></span><span><small>Genome</small><b>${run.genomes}</b></span><span><small>Generation</small><b>${run.deepest_generation}</b></span><span><small>RAM-Energie</small><b>${Number(run.energy_gained).toFixed(1)}</b></span></span><span class="chronicle-run-open">Details öffnen <b>↓</b></span>`});
    const dossier=root.querySelector('.chronicle-dossier'),formatDate=value=>value?new Date(value).toLocaleString('de-DE',{dateStyle:'medium',timeStyle:'short'}):'—';
    const openRun=(id,view='live')=>{sessionStorage.setItem('eve-open-view',view);location.href=`/?run=${encodeURIComponent(id)}`};
    const selectRun=id=>{const run=byId.get(id);if(!run)return;root.querySelectorAll('[data-chronicle-run]').forEach(button=>{const active=button.dataset.chronicleRun===id;button.classList.toggle('active',active);const prompt=button.querySelector('.chronicle-run-open');if(prompt)prompt.innerHTML=active?'Ausgewählt <b>↓</b>':'Details öffnen <b>↓</b>'});dossier.innerHTML=`<header><div><small>RUN ${safe(run.run_id.slice(0,8))} · v${safe(run.prototype_version)}</small><h3>${safe(run.label)}</h3><span class="chronicle-status ${statusClass(run)}">${stateLabel(run)}</span></div><div class="chronicle-dossier-actions"><button data-open="live">Leitstand</button><button data-open="history">Historie</button><button data-open="lineage">Stammbaum</button></div></header><p class="muted">Gestartet ${formatDate(run.created_at)} · ${run.mode==='open'?'offener Lauf':`Limit ${run.tick_limit} Ticks`}</p><div class="chronicle-dossier-grid"><div><small>Laufdauer</small><b>${run.ticks} Ticks</b></div><div><small>Maximum</small><b>${run.peak_population} Amöben</b><span>Tick ${run.peak_tick}</span></div><div><small>Nachkommen</small><b>${run.offspring}</b></div><div><small>Genomvielfalt</small><b>${run.genomes}</b></div><div><small>Generationstiefe</small><b>${run.deepest_generation}</b></div><div><small>RAM-Energie</small><b>${Number(run.energy_gained).toFixed(2)}</b></div></div>${run.resumed_from?`<p class="chronicle-continuation">↗ Fortsetzung aus ${safe(typeof run.resumed_from==='string'?run.resumed_from.slice(0,12):'vorherigem Run')}</p>`:''}`;dossier.querySelectorAll('[data-open]').forEach(button=>button.onclick=()=>openRun(id,button.dataset.open))};
    const revealRun=id=>{selectRun(id);dossier.classList.remove('revealed');void dossier.offsetWidth;dossier.classList.add('revealed');dossier.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})};
    root.querySelectorAll('[data-chronicle-run]').forEach(button=>button.onclick=()=>revealRun(button.dataset.chronicleRun));root.querySelectorAll('[data-record-run]').forEach(button=>button.onclick=()=>revealRun(button.dataset.recordRun));
    root.querySelectorAll('[data-hall-run]').forEach(button=>button.onclick=()=>{sessionStorage.setItem('eve-open-entity',button.dataset.hallEntity);openRun(button.dataset.hallRun,'history')});
    root.querySelectorAll('.chronicle-version-filter [data-version]').forEach(button=>button.onclick=()=>{root.querySelectorAll('.chronicle-version-filter [data-version]').forEach(item=>item.classList.toggle('active',item===button));const visible=[];root.querySelectorAll('[data-chronicle-run]').forEach(item=>{item.hidden=button.dataset.version!=='all'&&item.dataset.version!==button.dataset.version;if(!item.hidden)visible.push(item)});root.querySelector('[data-filter-count]').textContent=`${visible.length} ${visible.length===1?'Lauf':'Läufe'} sichtbar`;const selected=root.querySelector('[data-chronicle-run].active');if(selected?.hidden&&visible.length)selectRun(visible.at(-1).dataset.chronicleRun)});
    const selects=[...root.querySelectorAll('[data-compare-run]')],options=runs.map(run=>`<option value="${run.run_id}">${safe(run.label)} · v${safe(run.prototype_version)}</option>`).join('');selects.forEach(select=>select.innerHTML=options);if(runs.length>1)selects[1].selectedIndex=runs.length-1;
    const compare=()=>{const a=byId.get(selects[0].value),b=byId.get(selects[1].value),target=root.querySelector('.chronicle-comparison');if(!a||!b){target.innerHTML='<p class="empty">Mindestens zwei Runs erforderlich.</p>';return}const metrics=[['Ticks','ticks'],['Populationsmaximum','peak_population'],['Nachkommen','offspring'],['Genome','genomes'],['Generation','deepest_generation'],['RAM-Energie','energy_gained']];target.innerHTML=metrics.map(([label,key])=>{const av=Number(a[key]),bv=Number(b[key]),max=Math.max(1,av,bv),winner=av===bv?'gleich':av>bv?'a':'b';return `<div class="chronicle-compare-row"><span>${label}</span><div><i style="width:${av/max*100}%"></i><b class="${winner==='a'?'winner':''}">${key==='energy_gained'?av.toFixed(1):av}</b></div><div><i style="width:${bv/max*100}%"></i><b class="${winner==='b'?'winner':''}">${key==='energy_gained'?bv.toFixed(1):bv}</b></div></div>`}).join('')};selects.forEach(select=>select.onchange=compare);compare();if(runs.length)selectRun(runs.at(-1).run_id);
  }

  let lineageStarted = false;
  async function initLineage() {
    if (lineageStarted) return;
    lineageStarted = true;
    const root = document.querySelector('#lineage-workspace');
    try {
      const data = await fetch('/api/lineage', { cache: 'no-store' }).then(response => response.json());
      if (data.error) throw Error(data.error);
      renderLineage(root, data);
    } catch (error) {
      lineageStarted = false;
      root.innerHTML = `<p class="error">Stammbaum konnte nicht geladen werden: ${String(error.message || error)}</p>`;
    }
  }

  function renderLineage(root, data) {
    const entities = data.entities || [], byId = new Map(entities.map(entity => [entity.id, entity]));
    if (!entities.length) { root.innerHTML = '<p class="empty">Dieser Run enthält noch keine Amöben.</p>'; return; }
    const h = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    const maxTick = Math.max(1, data.current_tick || 0, ...entities.map(entity => entity.died ?? entity.born));
    const maxGeneration = Math.max(0, ...entities.map(entity => entity.generation));
    const generationRows = new Map();
    entities.forEach(entity => { const row = generationRows.get(entity.generation) || []; row.push(entity); generationRows.set(entity.generation, row); });
    generationRows.forEach(row => row.sort((a,b) => a.born-b.born || a.id-b.id));
    const width = Math.max(1500, Math.min(5200, maxTick * 8 + 360));
    const laneGap = 74, generationGap = 46;
    let lane = 0;
    for (let generation=0; generation<=maxGeneration; generation++) {
      const row = generationRows.get(generation) || [];
      row.forEach(entity => { entity._lane = lane++; });
      lane += Math.max(1, Math.ceil(generationGap / laneGap));
    }
    const height = Math.max(620, lane * laneGap + 150);
    const xFor = tick => 130 + tick / maxTick * (width - 260);
    const yFor = entity => 92 + entity._lane * laneGap;
    const clusterBuckets = new Map(), bucketSpan = Math.max(1, Math.ceil(maxTick / 12));
    entities.forEach(entity => { const key=`${entity.generation}:${Math.floor(entity.born/bucketSpan)}`,bucket=clusterBuckets.get(key)||[];bucket.push(entity);clusterBuckets.set(key,bucket); });
    const clusterSvg = entities.length < 120 ? '' : [...clusterBuckets.entries()].filter(([,bucket])=>bucket.length>3).map(([key,bucket])=>{const x=bucket.reduce((sum,e)=>sum+xFor(e.born),0)/bucket.length,y=bucket.reduce((sum,e)=>sum+yFor(e),0)/bucket.length,r=13+Math.min(28,Math.sqrt(bucket.length)*7);return `<g class="lineage-cluster" data-cluster="${key}" data-lineage-tip="Verdichtete Linie|${bucket.length} Amöben|Generation ${bucket[0].generation}" transform="translate(${x} ${y})"><circle r="${r}"/><title>${bucket.length} Amöben · Generation ${bucket[0].generation}</title></g>`}).join('');
    const childrenCount = entity => entity.children.length;
    const lifespan = entity => (entity.died ?? maxTick) - entity.born;
    const score = (entity, metric) => metric === 'genome' ? entity.n_g : metric === 'life' ? lifespan(entity) : childrenCount(entity);
    const maxScores = { genome:Math.max(...entities.map(e=>e.n_g),1), life:Math.max(...entities.map(lifespan),1), children:Math.max(...entities.map(childrenCount),1) };
    const mutationLabel = provenance => {
      const mutation = provenance?.mutation;
      if (!mutation) return 'keine Einzelmutation protokolliert';
      const type = mutation.class || mutation.kind || mutation.type || 'Mutation';
      return String(type).replaceAll('_',' ');
    };
    const edgeSvg = entities.flatMap(child => child.parents.filter(parentId => byId.has(parentId)).map(parentId => {
      const parent=byId.get(parentId), x1=xFor(parent.born), x2=xFor(child.born), y1=yFor(parent), y2=yFor(child);
      const bend=Math.max(26,(x2-x1)*.46), delta=child.parent_deltas?.[String(parentId)]?.total || 0;
      return `<path class="lineage-edge ${child.provenance?.mutation?'mutated':''}" data-from="${parentId}" data-to="${child.id}" data-delta="${delta}" d="M${x1} ${y1} C${x1+bend} ${y1} ${x2-bend} ${y2} ${x2} ${y2}"><title>${h(parent.name)} → ${h(child.name)} · Genom Δ ${delta>=0?'+':''}${delta} · ${h(mutationLabel(child.provenance))}</title></path>`;
    })).join('');
    const nodeSvg = entities.map(entity => `<g class="lineage-node ${entity.alive?'alive':'extinct'}" data-lineage-id="${entity.id}" tabindex="0" transform="translate(${xFor(entity.born)} ${yFor(entity)})"><circle class="lineage-halo" r="24"/><circle class="lineage-core" r="8"/><text class="lineage-name" x="13" y="-8">${h(entity.name)}</text><text class="lineage-meta" x="13" y="9">#${entity.id} · G${entity.generation}</text><title>${h(entity.name)} #${entity.id} · geboren ${entity.born} · ${entity.alive?'lebend':`gestorben ${entity.died}`} · Genom ${entity.n_g}</title></g>`).join('');
    const generationBands = [...generationRows].map(([generation,row]) => {
      const firstY=yFor(row[0])-34,lastY=yFor(row.at(-1))+34;
      return `<g class="lineage-generation"><rect x="0" y="${firstY}" width="${width}" height="${lastY-firstY}"/><text x="20" y="${firstY+20}">GEN ${generation}</text></g>`;
    }).join('');
    const eventSvg = entities.filter(entity=>entity.parents.length).map(entity=>`<path class="lineage-event ${entity.provenance?.mutation?'major':''}" data-event-id="${entity.id}" d="M${xFor(entity.born)} 48V${height-38}"><title>Geburt ${h(entity.name)} · Tick ${entity.born}</title></path>`).join('');
    const milestoneSvg=(data.milestones||[]).map(event=>`<g class="lineage-milestone ${event.kind}" data-milestone-tick="${event.tick}" data-lineage-tip="${h(event.label)}|Tick ${event.tick}${event.value!==undefined?`|Wert ${event.value}`:''}|${h(event.source||'analytische Markierung')}"><path d="M${xFor(event.tick)} 30V${height-20}"/><circle cx="${xFor(event.tick)}" cy="30" r="5"/><title>${h(event.label)} · Tick ${event.tick}${event.value!==undefined?` · ${event.value}`:''}</title></g>`).join('');
    const milestoneBar=(data.milestones||[]).map(event=>`<button type="button" data-milestone-button="${event.tick}"><small>TICK ${event.tick}</small>${h(event.label)}${event.value!==undefined?` · ${event.value}`:''}</button>`).join('');
    root.className='lineage-workspace panel';
    root.innerHTML=`<header class="lineage-toolbar"><div><small>EVE · PHYLOGENETISCHE KARTE</small><h3>${entities.length} Amöben · ${maxGeneration+1} Generationen · Tick 0–${maxTick.toLocaleString()}</h3></div><div class="lineage-actions"><label>Linienwert <select data-lineage-metric><option value="children">Nachkommen</option><option value="life">Lebensdauer</option><option value="genome">Genomgröße</option></select></label><button data-lineage-zoom="out">−</button><button data-lineage-zoom="in">+</button><button data-lineage-reset>Gesamt</button><span class="lineage-zoom-label">Übersicht</span><button type="button" data-analysis-focus>⛶ Vergrößern</button></div></header><div class="lineage-legend"><span><i class="alive"></i>lebend</span><span><i class="extinct"></i>ausgestorben</span><span><i class="mutation"></i>Mutation</span><strong>Klick: Verwandtschaft · Umschalt-Klick: vergleichen · Doppelklick: Zeitpunkt</strong></div><div class="lineage-milestone-bar">${milestoneBar}</div><section class="lineage-compare"><div data-compare-slot="a"><small>VERGLEICH A</small><b>Amöbe wählen</b></div><div class="lineage-common"><small>LETZTER GEMEINSAMER VORFAHR</small><b>—</b></div><div data-compare-slot="b"><small>VERGLEICH B</small><b>Umschalt-Klick</b></div><button data-compare-clear>× Vergleich leeren</button></section><div class="lineage-stage"><svg class="lineage-graph" viewBox="0 0 ${width} ${height}" role="img" aria-label="Evolutionärer Stammbaum"><defs><pattern id="lineage-grid" width="80" height="74" patternUnits="userSpaceOnUse"><path d="M80 0H0V74" fill="none" stroke="rgba(65,157,222,.065)"/></pattern><filter id="lineage-glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect class="lineage-grid" width="100%" height="100%" fill="url(#lineage-grid)"/>${generationBands}<g class="lineage-events">${eventSvg}${milestoneSvg}</g><g class="lineage-edges">${edgeSvg}</g><g class="lineage-nodes">${nodeSvg}</g><g class="lineage-cluster-nodes">${clusterSvg}</g><path class="lineage-playhead" data-lineage-tip="Ausgewählter Zeitpunkt|Tick ${maxTick}" d="M130 35V${height-25}"/></svg><div class="lineage-tooltip" hidden></div></div><aside class="lineage-inspector"><div><small>EVOLUTIONÄRER FOKUS</small><h3>Wähle eine Amöbe oder eine verdichtete Linie.</h3><p>Direkte Vorfahren, Geschwister und Nachkommen werden hervorgehoben.</p></div></aside>`;
    bindAnalysisFocus(root);
    const svg=root.querySelector('.lineage-graph'), nodes=[...svg.querySelectorAll('.lineage-node')], edges=[...svg.querySelectorAll('.lineage-edge')], inspector=root.querySelector('.lineage-inspector');
    new MutationObserver(()=>{if(!focusId)return;const entity=byId.get(focusId);if(!entity)return;if(!inspector.querySelector('[data-direct-parents]')){const block=document.createElement('section');block.className='lineage-direct-parents';block.dataset.directParents='';block.innerHTML=`<small>UNMITTELBARE ELTERN</small><div>${entity.parents.length?entity.parents.map(parentId=>{const parent=byId.get(parentId);return`<button type="button" data-focus-parent="${parentId}"><b>${h(parent?.name||`Amöbe #${parentId}`)}</b><span>#${parentId}${parent?` · Gen ${parent.generation}`:''}</span></button>`}).join(''):'<span class="lineage-founder">Gründeramöbe · keine Eltern im Lauf</span>'}</div>`;inspector.firstElementChild?.append(block);block.querySelectorAll('[data-focus-parent]').forEach(button=>button.onclick=()=>{const parent=byId.get(Number(button.dataset.focusParent));if(parent)focus(parent)})}if(entity.parents.length&&!inspector.querySelector('[data-lineage-genome-compare]')){const button=document.createElement('button');button.dataset.lineageGenomeCompare='';button.textContent='⌬ Genom mit Elternteil vergleichen';button.onclick=()=>window.eveV04.showGenomeComparison(entity.id,entity.parents[0]);const actions=inspector.querySelector('.lineage-inspector-actions');if(actions)actions.append(button)}}).observe(inspector,{childList:true,subtree:true});
    new MutationObserver(()=>{if(!focusId)return;const entity=byId.get(focusId);if(!entity)return;edges.forEach(edge=>{edge.classList.toggle('direct-parent',Number(edge.dataset.to)===entity.id&&entity.parents.includes(Number(edge.dataset.from)));edge.classList.toggle('direct-child',Number(edge.dataset.from)===entity.id&&entity.children.includes(Number(edge.dataset.to)))})}).observe(inspector,{childList:true});
    inspector.addEventListener('click',event=>{const button=event.target.closest('[data-open-history]');if(!button||!focusId)return;event.preventDefault();event.stopImmediatePropagation();sessionStorage.setItem('eve-open-entity',String(focusId));window.eveV04.setView('history');const snapshot=document.querySelector('#snap');if(snapshot){snapshot.value='latest';snapshot.dispatchEvent(new Event('change'))}},true);
    const originalPositions=new Map(entities.map(entity=>[entity.id,{x:xFor(entity.born),y:yFor(entity)}])),lensPositions=new Map();
    const edgeCurve=(from,to)=>{const bend=Math.max(30,Math.abs(to.x-from.x)*.42);return `M${from.x} ${from.y} C${from.x+bend} ${from.y} ${to.x-bend} ${to.y} ${to.x} ${to.y}`};
    const positionOf=id=>lensPositions.get(id)||originalPositions.get(id);
    const redrawLineageEdges=()=>edges.forEach(edge=>{const from=positionOf(Number(edge.dataset.from)),to=positionOf(Number(edge.dataset.to));if(from&&to)edge.setAttribute('d',edgeCurve(from,to))});
    const animateViewTo=target=>{const start={...view},began=performance.now(),duration=520,ease=t=>1-Math.pow(1-t,3);const frame=now=>{const t=Math.min(1,(now-began)/duration),p=ease(t);view={x:start.x+(target.x-start.x)*p,y:start.y+(target.y-start.y)*p,w:start.w+(target.w-start.w)*p,h:start.h+(target.h-start.h)*p};applyView();if(t<1)requestAnimationFrame(frame)};requestAnimationFrame(frame)};
    const focusLens=(entity,before,after)=>{lensPositions.clear();const family=[entity.id,...before,...after].map(id=>byId.get(id)).filter(Boolean),byGeneration=new Map();family.forEach(member=>{const row=byGeneration.get(member.generation)||[];row.push(member);byGeneration.set(member.generation,row)});const generations=[...byGeneration.keys()].sort((a,b)=>a-b),stepX=235,centerX=width/2,centerY=height/2;generations.forEach(generation=>{const row=byGeneration.get(generation).sort((a,b)=>a.born-b.born||a.id-b.id),gap=Math.max(64,Math.min(96,430/Math.max(1,row.length-1)));row.forEach((member,index)=>lensPositions.set(member.id,{x:centerX+(generation-entity.generation)*stepX,y:centerY+(index-(row.length-1)/2)*gap}))});const nodeLayer=svg.querySelector('.lineage-nodes');nodes.forEach(node=>{const id=Number(node.dataset.lineageId),next=positionOf(id),previous=originalPositions.get(id);if(lensPositions.has(id)){node.animate([{transform:`translate(${previous.x}px,${previous.y}px)`},{transform:`translate(${next.x}px,${next.y}px)`}],{duration:420,easing:'cubic-bezier(.2,.8,.2,1)'});node.setAttribute('transform',`translate(${next.x} ${next.y})`);nodeLayer.append(node)}});redrawLineageEdges();const points=[...lensPositions.values()],minX=Math.min(...points.map(p=>p.x)),maxX=Math.max(...points.map(p=>p.x)),minY=Math.min(...points.map(p=>p.y)),maxY=Math.max(...points.map(p=>p.y)),stage=svg.getBoundingClientRect(),padding=110,targetW=Math.max(560,maxX-minX+padding*2),targetH=Math.max(360,maxY-minY+padding*2),ratio=stage.width/Math.max(1,stage.height);let w=Math.max(targetW,targetH*ratio),hh=w/ratio;if(hh>height){hh=height;w=hh*ratio}animateViewTo({x:(minX+maxX)/2-w/2,y:(minY+maxY)/2-hh/2,w,h:hh});};
    const resetLens=()=>{lensPositions.clear();nodes.forEach(node=>{const id=Number(node.dataset.lineageId),position=originalPositions.get(id);node.setAttribute('transform',`translate(${position.x} ${position.y})`)});redrawLineageEdges();if(returnView){const target=returnView;returnView=null;animateViewTo(target)}};
    const base={x:0,y:0,w:width,h:height}; let view={...base}, returnView=null, drag=null, moved=false, focusId=null, compare=[];
    const ancestors=id=>{const found=new Set(),pending=[id];while(pending.length){const n=pending.pop();for(const p of byId.get(n)?.parents||[])if(!found.has(p)){found.add(p);pending.push(p)}}return found};
    const descendants=id=>{const found=new Set(),pending=[id];while(pending.length){const n=pending.pop();for(const c of byId.get(n)?.children||[])if(!found.has(c)){found.add(c);pending.push(c)}}return found};
    const pathTo=(id, stop=null)=>{const result=new Set([id]),pending=[id];while(pending.length){const n=pending.pop();if(n===stop)continue;for(const p of byId.get(n)?.parents||[])if(!result.has(p)){result.add(p);pending.push(p)}}return result};
    const commonAncestor=(a,b)=>{const aa=ancestors(a);aa.add(a);const bb=ancestors(b);bb.add(b);return [...aa].filter(id=>bb.has(id)).sort((x,y)=>byId.get(y).generation-byId.get(x).generation||byId.get(y).born-byId.get(x).born)[0]};
    const provenanceHtml=entity=>{const p=entity.provenance;if(!p)return '<p>Gründeramöbe – kein Geburtsgenom rekombiniert.</p>';const deltas=entity.parents.map(id=>{const d=entity.parent_deltas?.[String(id)]||{};return `<span>zu #${id}: F ${d.nodes>=0?'+':''}${d.nodes||0} · P ${d.edges>=0?'+':''}${d.edges||0}</span>`}).join('');return `<div class="lineage-deltas">${deltas}</div><p><b>${h(mutationLabel(p))}</b> · ${p.inherited_fragments||0} Fragmente übernommen<br><small>Größen-Elternteil #${p.size_parent_id||'—'} · A₀-Elternteil #${p.activity_parent_id||'—'}</small></p>`};
    const focus=entity=>{if(!svg.classList.contains('focused'))returnView={...view};focusId=entity.id;const before=ancestors(entity.id),after=descendants(entity.id),siblings=new Set(entity.parents.flatMap(id=>byId.get(id)?.children||[])),related=new Set([entity.id,...before,...after,...siblings]);nodes.forEach(node=>{const id=Number(node.dataset.lineageId);node.classList.toggle('selected',id===entity.id);node.classList.toggle('ancestor',before.has(id));node.classList.toggle('descendant',after.has(id));node.classList.toggle('sibling',siblings.has(id)&&id!==entity.id);node.classList.toggle('related',related.has(id));node.classList.toggle('dimmed',!related.has(id))});edges.forEach(edge=>{const from=Number(edge.dataset.from),to=Number(edge.dataset.to),ancestral=before.has(from)&&(before.has(to)||to===entity.id),descendent=after.has(to)&&(after.has(from)||from===entity.id),active=ancestral||descendent;edge.classList.toggle('ancestor',ancestral);edge.classList.toggle('descendant',descendent);edge.classList.toggle('related',active);edge.classList.toggle('dimmed',!active)});svg.classList.add('focused');focusLens(entity,before,after);inspector.innerHTML=`<div><small>GEN ${entity.generation} · AMÖBE #${entity.id}</small><h3>${h(entity.name)}</h3><p>Tick ${entity.born} geboren · ${entity.alive?'noch lebend':`Tick ${entity.died} gestorben`} · ${entity.children.length} direkte Kinder · ${after.size} Nachkommen insgesamt · Genom ${entity.n_f} F + ${entity.n_p} P</p><div class="lineage-path-legend"><span class="ancestor">← ${before.size} Vorfahren</span><span class="descendant">${after.size} Nachkommen →</span></div>${provenanceHtml(entity)}</div><div class="lineage-inspector-actions"><button data-open-history>Historie</button><button data-open-genome>Genom studieren</button><button data-at-birth>◷ Geburt ansehen</button><button data-as-compare>Zum Vergleich</button></div>`;inspector.querySelector('[data-open-history]').onclick=()=>{window.eveV04.setView('history');document.querySelector(`[data-entity-row="${entity.id}"]`)?.click()};inspector.querySelector('[data-open-genome]').onclick=()=>window.eveV04.showGenomeById(entity.id);inspector.querySelector('[data-at-birth]').onclick=()=>syncTick(entity.born);inspector.querySelector('[data-as-compare]').onclick=()=>addCompare(entity.id)};
    const addCompare=id=>{if(compare.includes(id))return;if(compare.length===2)compare=[];compare.push(id);updateCompare()};
    const updateCompare=()=>{nodes.forEach(n=>n.classList.remove('ancestor','descendant','sibling'));edges.forEach(e=>e.classList.remove('ancestor','descendant'));root.querySelector('[data-compare-slot="a"] b').textContent=compare[0]?`${byId.get(compare[0]).name} #${compare[0]}`:'Amöbe wählen';root.querySelector('[data-compare-slot="b"] b').textContent=compare[1]?`${byId.get(compare[1]).name} #${compare[1]}`:'Umschalt-Klick';nodes.forEach(n=>n.classList.toggle('compare',compare.includes(Number(n.dataset.lineageId))));if(compare.length<2){root.querySelector('.lineage-common b').textContent='—';return}const common=commonAncestor(...compare),a=byId.get(compare[0]),b=byId.get(compare[1]);root.querySelector('.lineage-common b').textContent=common?`${byId.get(common).name} #${common}`:'keiner im Run';const paths=new Set([...pathTo(a.id,common),...pathTo(b.id,common)]);nodes.forEach(n=>{const id=Number(n.dataset.lineageId);n.classList.toggle('dimmed',!paths.has(id));n.classList.toggle('related',paths.has(id))});edges.forEach(e=>{const active=paths.has(Number(e.dataset.from))&&paths.has(Number(e.dataset.to));e.classList.toggle('dimmed',!active);e.classList.toggle('related',active)});svg.classList.add('focused');inspector.innerHTML=`<div><small>EVOLUTIONÄRER VERGLEICH</small><h3>${h(a.name)} ↔ ${h(b.name)}</h3><p>${common?`Gemeinsamer Vorfahr ${h(byId.get(common).name)} #${common}, Generation ${byId.get(common).generation}.`:'Kein gemeinsamer Vorfahr innerhalb dieses Runs.'}</p><div class="lineage-comparison-grid"><span>${h(a.name)}<b>${a.n_g} G</b><small>Gen ${a.generation} · ${a.children.length} Kinder</small></span><span>Δ Genom<b>${Math.abs(a.n_g-b.n_g)}</b><small>Δ A₀ ${Math.abs(a.activity_base-b.activity_base)}</small></span><span>${h(b.name)}<b>${b.n_g} G</b><small>Gen ${b.generation} · ${b.children.length} Kinder</small></span></div></div>`};
    const syncTick=tick=>{const select=document.querySelector('#snap'),options=[...select.options].filter(o=>o.value!=='latest');if(!options.length)return;const closest=options.reduce((best,o)=>Math.abs(parseInt(o.value)-tick)<Math.abs(parseInt(best.value)-tick)?o:best,options[0]);select.value=closest.value;select.dispatchEvent(new Event('change'));window.eveV04.setView('history')};
    root.querySelectorAll('[data-milestone-button]').forEach(button=>button.onclick=()=>syncTick(Number(button.dataset.milestoneButton)));
    const updatePlayhead=()=>{const select=document.querySelector('#snap');const tick=select.value==='latest'?maxTick:parseInt(select.value),at=Number.isFinite(tick)?tick:maxTick,playhead=root.querySelector('.lineage-playhead');playhead.setAttribute('d',`M${xFor(at)} 35V${height-25}`);playhead.dataset.lineageTip=`Ausgewählter Zeitpunkt|Tick ${at}`;nodes.forEach(node=>{const entity=byId.get(Number(node.dataset.lineageId));node.classList.toggle('future',entity.born>at);node.classList.toggle('alive-at-tick',entity.born<=at&&(entity.died===null||entity.died>at))});edges.forEach(edge=>edge.classList.toggle('future',byId.get(Number(edge.dataset.to)).born>at))};
    document.querySelector('#snap').addEventListener('change',updatePlayhead); updatePlayhead();
    const lineageTooltip=root.querySelector('.lineage-tooltip'),lineageStage=root.querySelector('.lineage-stage');
    svg.addEventListener('pointermove',event=>{const marker=event.target.closest('[data-lineage-tip]');if(!marker){lineageTooltip.hidden=true;return}const [title,...details]=marker.dataset.lineageTip.split('|'),stageRect=lineageStage.getBoundingClientRect();lineageTooltip.innerHTML=`<b>${h(title)}</b>${details.map(detail=>`<span>${h(detail)}</span>`).join('')}`;lineageTooltip.style.left=`${Math.min(stageRect.width-190,Math.max(12,event.clientX-stageRect.left+14))}px`;lineageTooltip.style.top=`${Math.max(12,event.clientY-stageRect.top-62)}px`;lineageTooltip.hidden=false});svg.addEventListener('pointerleave',()=>{lineageTooltip.hidden=true});
    nodes.forEach(node=>{const activate=event=>{const entity=byId.get(Number(node.dataset.lineageId));if(event.shiftKey)addCompare(entity.id);else focus(entity)};node.addEventListener('click',activate);node.addEventListener('dblclick',event=>{event.preventDefault();syncTick(byId.get(Number(node.dataset.lineageId)).born)});node.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();activate(event)}})});
    root.querySelector('[data-compare-clear]').onclick=()=>{compare=[];focusId=null;svg.classList.remove('focused');nodes.forEach(n=>n.classList.remove('selected','related','dimmed','compare','ancestor','descendant','sibling'));edges.forEach(e=>e.classList.remove('related','dimmed','ancestor','descendant'));resetLens();updateCompare();inspector.innerHTML='<div><small>EVOLUTIONÄRER FOKUS</small><h3>Vergleich geleert.</h3><p>Wähle eine Amöbe, um ihre Abstammung zu untersuchen.</p></div>'};
    const applyMetric=()=>{const metric=root.querySelector('[data-lineage-metric]').value,max=maxScores[metric];nodes.forEach(node=>{const value=score(byId.get(Number(node.dataset.lineageId)),metric),r=7+8*Math.sqrt(value/max);node.querySelector('.lineage-core').setAttribute('r',r)});edges.forEach(edge=>{const parent=byId.get(Number(edge.dataset.from)),value=score(parent,metric);edge.style.strokeWidth=`${1.2+4*Math.sqrt(value/max)}`})};root.querySelector('[data-lineage-metric]').onchange=applyMetric;applyMetric();
    const applyView=()=>{svg.setAttribute('viewBox',`${view.x} ${view.y} ${view.w} ${view.h}`);const z=base.w/view.w;root.querySelector('.lineage-zoom-label').textContent=z<1.7?'Linienübersicht':`Zoom ${z.toFixed(z<3?1:0)}×`;svg.classList.toggle('overview',z<1.7)};
    const clamp=()=>{view.x=Math.max(-base.w*.03,Math.min(base.w-view.w+base.w*.03,view.x));view.y=Math.max(-base.h*.05,Math.min(base.h-view.h+base.h*.05,view.y))};
    const zoom=(factor,cx=null,cy=null)=>{const rect=svg.getBoundingClientRect(),rx=cx===null ? .5 : (cx-rect.left)/rect.width,ry=cy===null ? .5 : (cy-rect.top)/rect.height,ax=view.x+rx*view.w,ay=view.y+ry*view.h,nw=Math.max(base.w/32,Math.min(base.w,view.w*factor)),nh=nw*rect.height/rect.width;view={x:ax-rx*nw,y:ay-ry*nh,w:nw,h:Math.min(base.h,nh)};clamp();applyView()};
    root.querySelector('[data-lineage-zoom="in"]').onclick=()=>zoom(.72);root.querySelector('[data-lineage-zoom="out"]').onclick=()=>zoom(1/.72);root.querySelector('[data-lineage-reset]').onclick=()=>{returnView=null;root.querySelector('[data-compare-clear]').click();animateViewTo({...base})};
    svg.addEventListener('wheel',event=>{event.preventDefault();zoom(event.deltaY<0?.82:1/.82,event.clientX,event.clientY)},{passive:false});svg.addEventListener('pointerdown',event=>{if(event.target.closest('.lineage-node,.lineage-cluster'))return;drag={id:event.pointerId,x:event.clientX,y:event.clientY,vx:view.x,vy:view.y};moved=false;svg.setPointerCapture(event.pointerId);svg.classList.add('panning')});svg.addEventListener('pointermove',event=>{if(!drag)return;const rect=svg.getBoundingClientRect(),dx=event.clientX-drag.x,dy=event.clientY-drag.y;view.x=drag.vx-dx/rect.width*view.w;view.y=drag.vy-dy/rect.height*view.h;moved ||= Math.hypot(dx,dy)>4;clamp();applyView()});const endDrag=event=>{if(!drag||event.pointerId!==drag.id)return;drag=null;svg.classList.remove('panning');if(svg.hasPointerCapture(event.pointerId))svg.releasePointerCapture(event.pointerId)};svg.addEventListener('pointerup',endDrag);svg.addEventListener('pointercancel',endDrag);svg.addEventListener('click',event=>{if(event.target.closest('.lineage-node,.lineage-cluster'))return;if(moved){moved=false;return}if(svg.classList.contains('focused')||lensPositions.size)root.querySelector('[data-compare-clear]').click()});applyView();
    svg.querySelectorAll('.lineage-cluster').forEach(cluster=>cluster.addEventListener('click',event=>{event.stopPropagation();const members=clusterBuckets.get(cluster.dataset.cluster)||[],cx=members.reduce((sum,e)=>sum+xFor(e.born),0)/members.length,cy=members.reduce((sum,e)=>sum+yFor(e),0)/members.length;view={x:cx-base.w/6,y:cy-base.h/6,w:base.w/3,h:base.h/3};clamp();applyView();inspector.innerHTML=`<div><small>VERDICHTETE LINIE</small><h3>${members.length} Amöben · Generation ${members[0]?.generation??'—'}</h3><p>Die Gruppe wurde aufgelöst. Klicke nun ein Individuum für seine vollständige Verwandtschaft an.</p></div>`}));applyView();
  }

  document.querySelectorAll('.eve-nav button').forEach(button => button.addEventListener('click', () => window.eveV04.setView(button.dataset.view)));
  document.querySelector('[data-ram-zoom="in"]')?.addEventListener('click', () => window.dispatchEvent(new CustomEvent('eve:ramzoom', { detail: 2 })));
  document.querySelector('[data-ram-zoom="out"]')?.addEventListener('click', () => window.dispatchEvent(new CustomEvent('eve:ramzoom', { detail: .5 })));
  document.querySelector('[data-ram-reset]')?.addEventListener('click', () => window.dispatchEvent(new CustomEvent('eve:ramreset')));

  let activeRunId = null, replayTimer = null, replayIndex = 0;
  const runSelect = document.querySelector('#eve-run-select');
  const stopButton = document.querySelector('#eve-stop-run');
  const resumeButton = document.querySelector('#eve-resume-run');
  async function loadRuns() {
    const [runs, status] = await Promise.all([fetch('/api/runs', { cache: 'no-store' }).then(r => r.json()), fetch('/api/status', { cache: 'no-store' }).then(r => r.json())]);
    activeRunId = status.run_id;
    runSelect.innerHTML = runs.map(run => {
      const name = run.label || `Run ${run.run_id.slice(0, 8)}`;
      const state = run.status === 'running' ? '● läuft' : `${run.current_tick || 0} Ticks`;
      return `<option value="${run.run_id}" ${run.run_id === activeRunId ? 'selected' : ''}>${name} · v${run.prototype_version} · ${state}</option>`;
    }).join('');
    stopButton.hidden = status.status !== 'running';
    stopButton.disabled = false;
    stopButton.textContent = '■ Stoppen';
    resumeButton.hidden = status.status !== 'stopped';
    document.querySelector('.eve-chip.live').textContent = status.status === 'running' ? '● Daten verbunden' : status.status === 'stopped' ? '■ Run gestoppt' : '○ Archivansicht';
  }
  runSelect.addEventListener('change', () => { location.href = `/?run=${encodeURIComponent(runSelect.value)}`; });

  document.querySelector('#eve-replay').addEventListener('click', event => {
    const button = event.currentTarget;
    if (replayTimer) { clearInterval(replayTimer); replayTimer = null; button.textContent = '▶ Replay'; return; }
    const options = [...document.querySelector('#snap').options].filter(option => option.value !== 'latest');
    if (!options.length) return;
    replayIndex = 0; button.textContent = '⏸ Replay';
    const step = () => {
      if (replayIndex >= options.length) { clearInterval(replayTimer); replayTimer = null; button.textContent = '↺ Replay'; return; }
      const select = document.querySelector('#snap'); select.value = options[replayIndex++].value; select.dispatchEvent(new Event('change'));
    };
    step(); replayTimer = setInterval(step, 650);
  });

  stopButton.addEventListener('click', async () => {
    if (!activeRunId || !confirm('Diesen Run kontrolliert stoppen? Der Supervisor schreibt einen Abschlusscheckpoint und finalisiert den Run.')) return;
    const response = await fetch('http://127.0.0.1:8767/api/stop', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ run_id: activeRunId }) });
    const result = await response.json();
    if (!response.ok) alert(result.error || 'Stoppsignal konnte nicht gesendet werden.');
    else {
      stopButton.disabled = true;
      const started = Date.now();
      const followStop = async () => {
        try {
          const status = await fetch('/api/status', { cache: 'no-store' }).then(response => response.json());
          if (status.status !== 'running') {
            stopButton.textContent = `✓ Gestoppt bei Tick ${Number(status.current_tick).toLocaleString()}`;
            document.querySelector('.eve-chip.live').textContent = '■ Run gestoppt';
            resumeButton.hidden = status.status !== 'stopped';
            await loadRuns();
            setTimeout(() => { stopButton.hidden = true; }, 2200);
            return;
          }
          const seconds = Math.floor((Date.now() - started) / 1000);
          stopButton.textContent = `Stopp angefordert … ${seconds}s`;
          setTimeout(followStop, 500);
        } catch (_error) {
          stopButton.textContent = 'Status wird geprüft …';
          setTimeout(followStop, 1000);
        }
      };
      followStop();
    }
  });
  resumeButton.addEventListener('click', async () => {
    if (!activeRunId || !confirm('Diesen Run aus seinem letzten Checkpoint als neuen offenen Run fortsetzen? Der bestehende Run bleibt unverändert.')) return;
    resumeButton.disabled = true; resumeButton.textContent = 'Fortsetzung startet …';
    const response = await fetch('http://127.0.0.1:8767/api/resume', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ run_id: activeRunId }) });
    const result = await response.json();
    if (!response.ok) { alert(result.error || 'Fortsetzung fehlgeschlagen.'); resumeButton.disabled=false; resumeButton.textContent='↗ Fortsetzen'; return; }
    setTimeout(() => { location.href = `/?run=${encodeURIComponent(result.run_id)}`; }, 900);
  });

  async function prepareRunDialog() {
    const form = runDialog.querySelector('form');
    try {
      const [schema, presets] = await Promise.all([
        fetch('http://127.0.0.1:8767/api/schema').then(r => { if (!r.ok) throw Error(); return r.json(); }),
        fetch('http://127.0.0.1:8767/api/presets').then(r => r.json()),
      ]);
      const field = ([name, spec]) => {
        const common = `name="${name}" data-kind="${spec.type}" title="${spec.description}"`;
        let input;
        if (spec.type === 'choice') input = `<select ${common}>${spec.choices.map(value => `<option value="${value}">${value}</option>`).join('')}</select>`;
        else if (spec.type === 'bool') input = `<input type="checkbox" ${common}>`;
        else if (spec.type === 'text') input = `<input type="text" ${common}>`;
        else input = `<input type="number" ${common} min="${spec.min}" max="${spec.max}" step="${spec.step || (spec.type === 'int' ? 1 : 'any')}">`;
        return `<label class="parameter-field"><span>${spec.label}<button type="button" class="parameter-help" title="${spec.description}">?</button></span>${input}<small>${spec.description}</small></label>`;
      };
      form.innerHTML = `<header><div><small>EVE · SUPERVISOR</small><h2>Neuen Lauf starten</h2></div><button value="cancel" aria-label="Schließen">×</button></header><section class="preset-bar"><label>Preset<select id="run-preset">${Object.entries(presets).map(([key,preset]) => `<option value="${key}">${preset.label}</option>`).join('')}</select></label><span id="preset-description"></span></section><div class="parameter-grid">${Object.entries(schema).map(field).join('')}</div><div class="run-summary"><strong>Startauftrag</strong><span id="run-summary-text"></span></div><footer><button type="button" id="save-preset">Preset speichern</button><span class="dialog-error" role="alert"></span><button value="cancel">Abbrechen</button><button type="button" id="start-run" class="primary">Run starten</button></footer>`;
      const presetSelect = form.querySelector('#run-preset');
      const applyPreset = () => {
        const preset = presets[presetSelect.value];
        Object.entries(preset.values).forEach(([name,value]) => { const input=form.elements[name]; if(input) input.type==='checkbox'?input.checked=value:input.value=value; });
        form.querySelector('#preset-description').textContent = preset.description;
        updateSummary();
      };
      const values = () => Object.fromEntries(Object.entries(schema).map(([name,spec]) => { const input=form.elements[name]; let value=input.type==='checkbox'?input.checked:input.value; if(spec.type==='int')value=Number.parseInt(value);if(spec.type==='float')value=Number.parseFloat(value);return[name,value] }));
      const updateSummary = () => { const value=values(); form.querySelector('#run-summary-text').textContent = `${value.mode === 'open' ? 'Offener Run' : `${value.ticks} Ticks`} · ${value.population} Gründer · Seed ${value.seed} · ${value.ram_world}`; form.elements.ticks.disabled=value.mode==='open'; };
      presetSelect.onchange=applyPreset; form.querySelectorAll('input,select').forEach(input=>input.addEventListener('change',updateSummary));
      form.querySelector('#save-preset').onclick=async()=>{const name=prompt('Name des neuen Presets');if(!name)return;const response=await fetch('http://127.0.0.1:8767/api/presets',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,values:values()})});if(response.ok){form.querySelector('.dialog-error').textContent='Preset gespeichert.'}else{const result=await response.json();form.querySelector('.dialog-error').textContent=result.error}};
      form.querySelector('#start-run').onclick=async()=>{const button=form.querySelector('#start-run'),error=form.querySelector('.dialog-error');button.disabled=true;error.textContent='Supervisor startet den Run …';try{const response=await fetch('http://127.0.0.1:8767/api/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({values:values()})}),result=await response.json();if(!response.ok)throw Error(result.error);error.textContent=`Run ${result.run_id.slice(0,8)} startet …`;setTimeout(()=>{location.href=`/?run=${encodeURIComponent(result.run_id)}`},900)}catch(reason){error.textContent=reason.message||'Supervisor nicht erreichbar';button.disabled=false}};
      applyPreset();
    } catch (_error) {
      form.querySelector('.run-dialog-loading').textContent = 'Der Supervisor ist nicht erreichbar. Starte supervisor.py auf Port 8767.';
    }
  }
  document.querySelector('#eve-new-run').addEventListener('click', async () => { if (!runDialog.querySelector('#run-preset')) await prepareRunDialog(); runDialog.showModal(); });
  setInterval(()=>{const meta=document.querySelector('#meta'),entities=window.eveV04Entities||[];if(!meta?.querySelector('.metric')||!entities.length)return;const values=new Map([...meta.querySelectorAll('.metric')].map(metric=>[metric.childNodes[0]?.textContent?.trim(),metric.querySelector('strong')?.textContent?.trim()])),ordered=entities.filter(entity=>Number.isFinite(Number(entity.n_g))).sort((a,b)=>Number(a.n_g)-Number(b.n_g)),small=ordered[0],large=ordered.at(-1);meta.classList.add('evolution-summary');meta.innerHTML=`<div class="evolution-summary-context"><small>EVE · ZEITREISE</small><b>${values.get('Auswahl')||'Gesamter Lauf'}</b><span>${document.querySelector('#selection-help')?.textContent||''}</span></div><dl class="evolution-summary-grid"><div><dt>Am Ende lebend</dt><dd>${values.get('Am Ende lebend')||'—'}</dd></div><div><dt>Beteiligte Amöben</dt><dd>${values.get('Beteiligte Amöben')||entities.length}</dd></div><div class="genome-min"><dt>Kleinstes Genom</dt><dd>${small?`${small.n_g} G · ${small.name||`#${small.id}`}`:'—'}</dd></div><div class="genome-max"><dt>Größtes Genom</dt><dd>${large?`${large.n_g} G · ${large.name||`#${large.id}`}`:'—'}</dd></div><div><dt>Seed</dt><dd>${values.get('Seed')||'—'}</dd></div><div class="run"><dt>Run</dt><dd>${values.get('Run')||'—'}</dd></div></dl>`},250);
  loadRuns().then(()=>{const requested=sessionStorage.getItem('eve-open-view');if(requested){sessionStorage.removeItem('eve-open-view');window.eveV04.setView(requested)}}).catch(() => { runSelect.innerHTML = '<option>Run-Katalog nicht erreichbar</option>'; });
})();
