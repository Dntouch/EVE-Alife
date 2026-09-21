# EVE-Alife – Prototyp v0.2

`v0.2` ist der Prototyp für langfristig beobachtbare Evolution. Er startet vom konservierten P1-Endstand und ergänzt Run-Lebenszyklus, strukturierte Datenhaltung sowie eine gemeinsame Live-/Archiv-Lupe. Abweichende v0.2-Experimente werden ausdrücklich benannt und über die Run-Konfiguration nachvollziehbar gehalten.

Die Ausgangsbasis ist bewusst der eingefrorene P1-Endstand aus Lauf 41: 20 P1-Amöben, Seed 42, zufälliger RAM-Schlamm, Startenergie 500, relative Geburtsenergie 0,5, fünf finanzierbare Mindest-Heartbeats und Informationstarif 60. Ohne weitere Populationsparameter startet `run.py` genau diese Referenzkonfiguration. Technische Demo-Populationen sind nur noch ausdrücklich mit `--population-model demo` oder `--population-model technical-explorer` wählbar.

Der v0.2-Standard erprobt einen auf ein Zehntel abgesenkten Genomkostentarif (`0,05` für Funktionspunkte, `0,01` für Kanten). Der historische P1-Tarif bleibt in v0.1 unverändert; über `--genome-node-cost` und `--genome-edge-cost` kann er für Kontrollläufe weiterhin gewählt werden.

Die derzeitige experimentelle P1-Population streut Offset, vorzeichenbehaftete Schrittweite, Geduld und A₀ reproduzierbar über den Seed. `--uniform-p1` erzeugt den Kontrollfall mit identischen Startwerten. Diese Suchwerte sind normale Genomkonstanten und keine fest benannten Strategien. Hintergrund und offene Prüffragen stehen in [EXPERIMENT_PARTNERSUCHE.md](EXPERIMENT_PARTNERSUCHE.md).

Die Architekturentscheidungen stehen in [ARCHITEKTUR.md](ARCHITEKTUR.md), die präzisen Regeln in [SPEZIFIKATION.md](SPEZIFIKATION.md). P0/P1 bleiben gemäß [KONSERVIERUNG_P0_P1.md](../KONSERVIERUNG_P0_P1.md) unter `v0.1` erhalten.

Die tatsächlich ausgeführten Versuche werden getrennt von Spezifikation und Implementierung unter [Laufergebnisse v0.2](../../07_Laufergebnisse/v0.2/README.md) geführt. Ihre Laufnummern beginnen innerhalb dieser Version bei 1.

## Testen

```bash
cd 04_Prototypen/v0.2
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

Die v0.1-Lupe wurde nicht ersetzt: Chronik, Zeitfilter, Umweltkontakte, Amöbenkarten, K/Z-Ansichten und Lebensfilm bleiben erhalten. Hinzu kommen Live-/Endstatus, die v0.2-Datenquelle und ein bildliches SVG-Genomdiagramm mit gerichteten Kanten. Die Lupe öffnet SQLite ausschließlich read-only und besitzt keine Steuerroute.

## Portables Archiv

Beim begrenzten Run kann direkt exportiert werden:

```bash
python3 run.py --ticks 1000 --archive mein-lauf.eve-run
python3 lupe.py mein-lauf.eve-run
```

Das Archiv enthält ein versioniertes Manifest und eine konsistente Datenbanksicherung. Auch ein bestehender Run kann über `run_store.export_archive(...)` exportiert werden.

## Bestandteile

- `eve_core.py`: vom P1-Fachkern abgeleiteter v0.2-Experimentkern
- `run.py`: Supervisor und Lebenszyklus
- `run_store.py`: Schema, Deduplizierung, Manifest und Archivexport
- `lupe.py`: gemeinsame read-only Live-/Archivansicht
- `test_eve.py`: übernommene deterministische Fachmodelltests
- `test_run_lifecycle.py`: neue Lifecycle-, Datenhaltungs- und Archivtests
- `run_stats.py`: historische v0.1-Auswertung, nur für Kompatibilitätsbezug mitkopiert

`run_stats.py` ist nicht der v0.2-Datenspeicher und wird vom neuen Supervisor nicht aufgerufen.
