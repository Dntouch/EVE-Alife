# EVE-Alife – Prototyp v0.3

> **Status:** abgeschlossener Arbeitsstand vom 23. September 2026. v0.3 basiert auf dem letzten Stand von
> v0.2. Der Ordner `../v0.2/` bleibt unverändert konserviert.

## Ziel des ersten v0.3-Wurfs

Die Lupe wurde von einer langen Sammelseite zu einer Analyse-Anwendung mit fünf
Arbeitsbereichen: Leitstand, Historie, Chronik, Stammbaum und Genom. Die
Live-Suppe erscheint als lineares, zoombares RAM-Band; ein kleiner Ringhinweis
bewahrt die zyklische Bedeutung des Adressraums. Amöben werden ausschließlich
dann gruppiert, wenn ihre Markierungen im aktuellen Zoomlevel überlappen.

Der Stand führt außerdem das EVE-Designsystem, eine feste Navigation, ein
eigenes v0.3-Wallpaper und einen seitlichen Amöben-Fokus ein. Genomkarten werden
nicht mehr innerhalb der Amöbenkarten gerendert, sondern in einem eigenen,
zoombaren Arbeitsraum oder optional in einem separaten Fenster untersucht.

Der Stammbaum verbindet gespeicherte Elternkanten, Lebensgrenzen und
Genomprovenienz zu einer evolutionären Zeitlandschaft. Die Chronik führt
konservierte v0.2- und neue v0.3-Runs in einem versionsübergreifenden Archiv
zusammen. Eine vollständige Bedien- und Beobachtungsbeschreibung steht in
[LUPE.md](LUPE.md).

Der Leitstand besitzt einen globalen Run-Katalog für v0.2- und v0.3-Läufe,
Beobachtungs-Replay sowie eine getrennte Supervisorsteuerung. Der Supervisor
startet begrenzte und offene Runs aus validierten Presets, stoppt sie
kontrolliert und kann einen Abschlusscheckpoint als neuen, verknüpften Run
fortsetzen. Details stehen in [SUPERVISOR.md](SUPERVISOR.md).

Die wissenschaftliche Grenze bleibt sichtbar: historische Beobachtungsbilder
sind persistierte Messpunkte und kein exakter Tick-Replay. Die Lupe bleibt
vollständig read-only.

Zum Abschlussstand gehören außerdem der direkte Eltern-Kind-Genomvergleich,
eine interaktive versionsübergreifende Chronik, generationstreue Anzeigenamen
aus einem Pool von 500 Namen und einmalig verwertbare Leichen in der RAM-Suppe.
Die historische Amöbe bleibt nach der Verwertung vollständig analysierbar.
Evolvierbare Kantengewichte sind lediglich für v0.4 konzipiert und in v0.3
nicht aktiv.

## Versions- und Formatgrenze

- Implementierung und Gestaltung: Prototyp v0.3
- Ausgangsbasis: konservierter Prototyp v0.2
- Run-Datenformat: weiterhin Format 2
- Bestehende v0.2-Runs und `.eve-run`-Archive bleiben lesbar
- Ein Datenformat 3 wird erst eingeführt, wenn neue fachliche Daten es erfordern

`v0.2` ist der Prototyp für langfristig beobachtbare Evolution. Er startet vom konservierten P1-Endstand und ergänzt Run-Lebenszyklus, strukturierte Datenhaltung sowie eine gemeinsame Live-/Archiv-Lupe. Abweichende v0.2-Experimente werden ausdrücklich benannt und über die Run-Konfiguration nachvollziehbar gehalten.

Die Ausgangsbasis ist bewusst der eingefrorene P1-Endstand aus Lauf 41: 20 P1-Amöben, Seed 42, zufälliger RAM-Schlamm, Startenergie 500, relative Geburtsenergie 0,5, fünf finanzierbare Mindest-Heartbeats und Informationstarif 60. Ohne weitere Populationsparameter startet `run.py` genau diese Referenzkonfiguration. Technische Demo-Populationen sind nur noch ausdrücklich mit `--population-model demo` oder `--population-model technical-explorer` wählbar.

Der v0.2-Standard erprobt einen auf ein Zehntel abgesenkten Genomkostentarif (`0,05` für Funktionspunkte, `0,01` für Kanten). Der historische P1-Tarif bleibt in v0.1 unverändert; über `--genome-node-cost` und `--genome-edge-cost` kann er für Kontrollläufe weiterhin gewählt werden.

Die derzeitige experimentelle P1-Population streut Offset, vorzeichenbehaftete Schrittweite, Geduld und A₀ reproduzierbar über den Seed. `--uniform-p1` erzeugt den Kontrollfall mit identischen Startwerten. Diese Suchwerte sind normale Genomkonstanten und keine fest benannten Strategien. Hintergrund und offene Prüffragen stehen in [EXPERIMENT_PARTNERSUCHE.md](EXPERIMENT_PARTNERSUCHE.md).

Seit der Auswertung von Lauf 6 besitzt v0.2 außerdem eine experimentelle Klingel. Lauf 7 erprobte zunächst genau einen eingehenden Klopfer. Der folgende Arbeitsstand macht deren Kapazität `Nₖ` und die notwendige stabile Bindungsdauer `Tₚ` vererbbar. Annahme, Erwiderung und das Belegen eines zweiten Partnerslots bleiben genomische Handlungen; die technische Schicht stellt lediglich reale Vorschläge mit Herkunft zu und zählt die Stabilität einer vollständig gegenseitigen Zwei- oder Dreiergruppe.

Seit Lauf 16 wird eine Geburt aus dem gemeinsamen Überschuss aller Eltern über ihrem jeweils individuellen `S₀` finanziert. Ausgangspunkt bleibt der gleiche Anteil; nicht finanzierbare Anteile werden von den übrigen Eltern übernommen. Der Versuchsstand und sein nicht stabiler Generationenwechsel sind in [EXPERIMENT_GENERATIONENWECHSEL.md](EXPERIMENT_GENERATIONENWECHSEL.md) dokumentiert.

Die Architekturentscheidungen stehen in [ARCHITEKTUR.md](ARCHITEKTUR.md), die präzisen Regeln in [SPEZIFIKATION.md](SPEZIFIKATION.md). P0/P1 bleiben gemäß [KONSERVIERUNG_P0_P1.md](../KONSERVIERUNG_P0_P1.md) unter `v0.1` erhalten.

Die tatsächlich ausgeführten Versuche werden getrennt von Spezifikation und
Implementierung unter [Laufergebnisse v0.3](../../07_Laufergebnisse/v0.3/README.md)
geführt. Ihre Laufnummern beginnen innerhalb dieser Version bei 1. Technische
Supervisor- und Oberflächenläufe sind dort als solche gekennzeichnet.

## Testen

```bash
cd 04_Prototypen/v0.3
python3 -m unittest -v
```

## Begrenzter Run

```bash
python3 run.py --ticks 2000
```

Der Run endet bei vorheriger natürlicher Extinktion oder bei Tick 2000. Ein Ende mit lebender Population erhält `tick_limit_reached`, niemals `natural_extinction`.

## Offener Run

```bash
python3 run.py --open
```

Der Supervisor setzt kein Tick-Limit. Der reguläre fachliche Endgrund ist natürliche Extinktion. `Ctrl-C` beziehungsweise SIGTERM schreibt einen Recovery-Checkpoint und erfindet keinen Endgrund.

Wichtige Speicherparameter:

```bash
python3 run.py --open --sample-every 100 --checkpoint-every 10000
```

`sample-every` steuert kompakte Messpunkte und komprimierte Lupe-Bilder, `checkpoint-every` vollständige Recovery-Zustände. Das atomare `live.json` ist kein Archiv und darf ersetzt werden.

## Lupe

```bash
python3 lupe.py runs/DEINE-RUN-ID
```

Die Analysefähigkeiten der älteren Lupe bleiben erhalten, sind aber auf fünf
getrennte Arbeitsbereiche verteilt. Die Lupe öffnet SQLite ausschließlich
read-only. Start-, Stopp- und Fortsetzungsaufträge werden an den getrennten
Supervisor gesendet; die Mutation des Run-Zustands bleibt dessen Verantwortung.

### Spielzeug in der Suppe

Mit `--ram-world toys` entsteht eine reproduzierbare experimentelle Umwelt aus 128 über den RAM-Ring verteilten Spielzeuginseln. Jede Insel verbindet ein festes Zahlenmuster, zwei langsame externe Blasen und einen gekoppelten Schalter. Veränderungen liefern nach der vorhandenen Neuheitsregel Energie. Schalter bewahren jedoch die Urheberkette ihres Auslösers und erlauben deshalb keine Selbstfütterung. Die vollständige vorläufige Festlegung steht in [EXPERIMENT_UMWELTSPIELZEUG.md](EXPERIMENT_UMWELTSPIELZEUG.md).

Im Spielzeugmodus sind Entity-ID und Standort getrennt. `RAM_READ` und `RAM_WRITE` verwenden genomische Werte als lokale Offsets relativ zu `ram_position`; Kinder werden nahe einem zufällig gewählten Elternstandort abgelegt. Eine Bewegung während des Lebens existiert noch nicht.

## Portables Archiv

Beim begrenzten Run kann direkt exportiert werden:

```bash
python3 run.py --ticks 1000 --archive mein-lauf.eve-run
python3 lupe.py mein-lauf.eve-run
```

Das Archiv enthält ein versioniertes Manifest und eine konsistente Datenbanksicherung. Auch ein bestehender Run kann über `run_store.export_archive(...)` exportiert werden.

## Bestandteile

- `eve_core.py`: vom P1-Fachkern abgeleiteter v0.3-Experimentkern
- `run.py`: Run-Prozess und Lebenszyklus
- `run_store.py`: Schema, Deduplizierung, Manifest und Archivexport
- `lupe.py`: gemeinsame read-only Analyse- und Archivansicht
- `supervisor.py`: getrennte Start-, Stopp- und Fortsetzungssteuerung
- `run_parameters.py`: validiertes Parameterschema und Presets
- `assets/v03.js`, `assets/v03.css`: EVE-Arbeitsoberfläche
- `test_eve.py`: übernommene deterministische Fachmodelltests
- `test_run_lifecycle.py`: Lifecycle-, Datenhaltungs-, Lupe- und Archivtests
- `test_supervisor.py`: Supervisor- und Presettests
- `run_stats.py`: historische v0.1-Auswertung, nur für Kompatibilitätsbezug mitkopiert

`run_stats.py` ist nicht der v0.2-Datenspeicher und wird vom neuen Supervisor nicht aufgerufen.
