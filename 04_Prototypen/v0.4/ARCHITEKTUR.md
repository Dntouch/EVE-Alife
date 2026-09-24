# Architektur v0.4: Genomrevision auf der EVE-Workstation

Prototyp v0.4 übernimmt Fachkern, Run-Format und Persistenzarchitektur von v0.3
und erweitert darauf die Bedien-, Analyse- und Supervisorschicht. Die folgenden
Abschnitte beschreiben deshalb zunächst die unverändert gültige v0.2-Basis;
Lupe und Supervisor von v0.4 sind ergänzend in `LUPE.md` und `SUPERVISOR.md`
dokumentiert. Der konservierte Ordner `../v0.2` wird nicht verändert.

## Ziele und Grenze

`v0.2` erweitert Supervisor, Beobachtung und Datenhaltung und nimmt das konservierte P1-Fachmodell als Ausgangsbasis. Fachliche v0.2-Experimente werden getrennt dokumentiert und über Run-Konfigurationen nachvollziehbar gehalten. Die Architektur trennt den schreibenden Simulationsprozess strikt von read-only Beobachtern:

```text
Simulation → Supervisor → SQLite-Run + flüchtiges Livebild
                              ↓
                    lokale read-only Lupe
                              ↓ Export
                         .eve-run-Archiv
                              ↓
                    read-only/public Lupe
```

Die Lupe besitzt weder eine Control-Route noch eine Referenz auf veränderliche Core-Objekte. Eine spätere öffentliche Live-Ansicht darf nur replizierte `GET`-Daten erhalten, niemals Zugriff auf Supervisor, Arbeitsverzeichnis oder Schreib-API.

## Run-Lebenszyklus

Ein Run ist `limited` mit positivem `tick_limit` oder `open` mit `tick_limit = NULL`. Beide beginnen im Status `running`. Natürliche Extinktion führt zu `status = extinct` und `end_reason = natural_extinction`. Nur ein noch lebender, begrenzter Run kann mit `status = completed` und `end_reason = tick_limit_reached` enden. SIGINT/SIGTERM erzeugen keinen falschen Fachendgrund: Der Datensatz bleibt `running` und erhält einen Recovery-Checkpoint.

## Persistentes Datenmodell (Formatversion 2)

`run.sqlite3` enthält:

- `run`: ID, Konfiguration, Versionen, Modus, Status, Endgrund, Zeiten, Tick und Population;
- `genomes`: kanonisch serialisierte Struktur, SHA-256-Fingerprint, A₀ und Größen; identische Genome stehen nur einmal;
- `entities`: stabile Entity-ID, Lebensgrenzen und Genom-ID;
- `ancestry`: geordnete Eltern-Kind-Kanten;
- `events`: indexierte diskrete, im Modell vorhandene Ereignisse;
- `measurements`: periodische Population, Gesamtzahl und Zahl verschiedener Genome;
- `observations`: komprimierte periodische Amöbenzustände für Zeitfilter und Lebensfilm, ohne vollständigen RAM;
- `checkpoints`: reservierter Katalog für verifizierte Recovery-Dateien.

`manifest.json` ist ein kleiner, atomar ersetzter Einstiegspunkt mit `format = eve-alife-run` und `format_version = 2`. `live.json` ist ein atomar ersetztes, flüchtiges Übersichtsbild ohne vollständigen RAM, Genomtopologien, K-/Z-Signale oder wachsende Wissenshistorien. Es wird höchstens zweimal pro Sekunde erneuert. Die periodischen `observations` konservieren die Untersuchungstiefe der v0.1-Lupe in konfigurierbarer Auflösung. Technische Logs gehören nicht in diese Tabellen.

## Speicherung und Skalierung

Nicht dauerhaft pro Tick gespeichert werden vollständiger RAM, vollständiger Zustand aller Viecher, `node_fire`, `signal`, `standby` und `heartbeat`. Diese hochfrequenten Details bleiben im aktuellen Livebild oder in optionalen Recovery-Checkpoints. Diskrete Geburts-, Todes-, Reproduktions-, Membran- und reale RAM-Kontaktereignisse bleiben erhalten. Messwerte werden in konfigurierbaren Intervallen persistiert. Genome werden inhaltlich dedupliziert.

Damit wächst der reguläre Datensatz näherungsweise mit `verschiedenen Genomen + Viechern + Abstammungskanten + relevanten Ereignissen + komprimierten Beobachtungen im gewählten Intervall`, nicht zwangsläufig mit `Ticks × Population × RAM-Vollzustand`. Beispiel: Bei 10 Millionen Ticks erzeugt `sample_every=100` 100.001 Beobachtungspunkte statt 10 Millionen Vollbilder. RAM-Kontakte können weiterhin dominant werden; eine spätere Aggregation braucht zuerst eine wissenschaftliche Aufbewahrungsentscheidung und ist daher in v0.2 nicht irreversibel eingebaut.

Seit der Performance-Revision vom 24. September 2026 bildet jedes
Messintervall zugleich eine Veröffentlichungsgrenze: Ereignisse werden pro Tick
in die laufende SQLite-Transaktion übertragen und danach aus dem
Simulationsspeicher entfernt; Commit, Run-Status und Manifest werden gebündelt
publiziert. Neue Entitäten und ihre Genome werden ausschließlich bei der Geburt
registriert. Ein Writer-Cache vermeidet die erneute Serialisierung bereits
bekannter Genome. Diese Änderungen betreffen Beobachtung und Persistenz, nicht
Reihenfolge, Zufall oder Fachzustand eines Heartbeats.

Auslöser war der OOM-Abbruch des Runs
`0ccf273f-6bc6-4a91-a42c-7bca96f9d70b`: Die nie geleerte Ereignisliste ließ
den Prozess bei 9.446 erzeugten Amöben auf rund 52 GB RSS wachsen. Die
vollständige [Laufanalyse](../../07_Laufergebnisse/v0.4/Lauf_001.md) hält den
Befund und seine Grenzen fest.

## Historie, Genomgraph und Abstammung

Die Kombination aus unveränderlicher Entity-ID, Elternkanten und deduplizierter vollständiger Genomstruktur beantwortet Elternschaft, Genombesitz, Linien, ausgestorbene Seitenlinien und Genomgrößenverläufe. Nodes enthalten reale Funktionspunkttypen, CONST-Werte und Segment-IDs; Edges enthalten Quell-/Zielinstanz, reale Ports und Kantengewichte; A₀ bleibt erhalten. Das ist die direkte Datenbasis für Graphdarstellung und Genomvergleiche.

Das Ereignis `genome_created` protokolliert zusätzlich den gezogenen Architektur- und A₀-Elternteil, jeden übernommenen Vererbungsplatz samt Homologiezuordnung, die Abbildung elterlicher auf kindliche Node-IDs, ursprüngliche, neu gekoppelte und weggefallene Anschlusskanten sowie die konkret ausgeführte Inhalts- oder Strukturmutation mit Vorher-/Nachherwert. Die Instrumentierung verbraucht keinen zusätzlichen Zufall und verändert keine Auswahl; Determinismus- und Fachmodelltests sichern diese Beobachtungsgrenze ab.

## Live, Archiv, Recovery und Replay

Live und Archiv benutzen dieselben SQL-Abfragen und dieselbe Lupe. Bei einem Archiv fehlt lediglich das flüchtige Livebild. `--checkpoint-every` schreibt vollständige Core-Checkpoints für Recovery; ein unterbrochener Checkpoint kann als neuer Run fortgesetzt werden. Vorhandene Core-Tests belegen deterministisches Fortsetzen eines Checkpoints.

Das ist kein exakter Replay eines beliebigen historischen Ticks: Zwischen Checkpoints werden nicht alle Scheduler-, K-, Z-, RAM- und RNG-Zustände persistiert. Evolutionäre Historie und exakter Simulations-Replay bleiben ausdrücklich getrennte Eigenschaften.

## Portable und öffentliche Archive

Ein `.eve-run` ist ein ZIP mit `manifest.json`, einer konsistenten SQLite-Sicherung und optionalen Checkpoints. Die Lupe öffnet das Archiv in einem temporären Verzeichnis und die Datenbank im SQLite-Modus `mode=ro`. Schema-Versionen werden nicht stillschweigend umgedeutet. Für Veröffentlichung sollten Recovery-Checkpoints wegen Größe und möglicher unnötiger interner Details weggelassen, Dateigröße/Integrität vor Annahme begrenzt und Archive außerhalb des Webroots entpackt werden. Eine öffentliche Instanz stellt ausschließlich feste `GET`-Routen bereit.

## Festgestellte Bestandsabweichungen

- `v0.1/README.md` bezeichnet `P1_GENOMENTWURF.md` noch als nicht implementiert, während das Dokument selbst und der Code P1 als implementiert ausweisen.
- `v0.1` nennt den Prozess teils P0.1, obwohl er inzwischen P1-Funktionen enthält.
- Die alte Dashboardlogik wertet Population null als Massenaussterben, besitzt aber keinen gespeicherten Endgrund.
- Historische Snapshots heißen in der Lupe teils Replay, sind jedoch kein exakter Simulations-Replay.
- `v0.1` speichert vollständigen RAM in jedem Beobachtungssnapshot und hält alle Events im RAM; beides ist für offene Langzeitläufe ungeeignet.

Diese Punkte werden nicht rückwirkend in P0/P1 korrigiert, sondern an der Versionsgrenze dokumentiert.
