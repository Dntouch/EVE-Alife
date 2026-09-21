# Abschlussbericht zum Arbeitsauftrag „Neuer Prototyp“

Stand: 21. September 2026

## Ergebnis

Der neue Prototyp heißt `v0.2`. P0/P1 und `v0.1` wurden nicht verändert; ihre Versionsgrenze ist in `../KONSERVIERUNG_P0_P1.md` dokumentiert. `v0.2` ist eine getrennte, auf P1 basierende Implementierung.

Neu beziehungsweise geändert wurden innerhalb von `v0.2` `run.py`, `run_store.py`, `lupe.py`, `eve_core.py`, `test_run_lifecycle.py`, `README.md`, `SPEZIFIKATION.md`, `ARCHITEKTUR.md` und dieser Bericht. `test_eve.py` und `run_stats.py` wurden als Ausgangsbasis kopiert. Außerhalb kamen die Konservierungsnotiz und die Aktualisierung der Repository-Startseite hinzu.

## Run-Modi und Endzustände

`--ticks N` begrenzt einen Run, `--open` entfernt das künstliche Limit. Beide enden bei vorheriger Extinktion. Gespeichert werden `running`, `extinct / natural_extinction` und `completed / tick_limit_reached`. Eine technische Unterbrechung bleibt ohne erfundenen Endgrund wiederaufnehmbar.

## Datenhaltung

Dauerhaft gespeichert werden Run-Konfiguration und Lebenszyklus, deduplizierte vollständige Genome, Entity-Lebensgrenzen, Abstammungskanten, relevante diskrete Ereignisse, periodische Messreihen, komprimierte Lupe-Bilder und Recovery-Checkpoint-Metadaten. Das aktuelle Livebild wird zusätzlich atomar ersetzt; der vollständige RAM wird nicht in jedes Bild kopiert.

Das Wachstum wird durch Genom-Deduplizierung, Messintervalle, ersetzbares Livebild und das Auslassen hochfrequenter Ausführungsdetails aus der regulären Historie begrenzt. Evolutionäre Ereignisse werden nicht durch Downsampling entfernt. RAM-/Membrankontakte bleiben derzeit einzeln erhalten und können bei sehr langen Runs dominant werden; eine irreversible Aggregation wurde bewusst nicht ohne wissenschaftliche Aufbewahrungsentscheidung eingeführt.

Genome werden kanonisch serialisiert und per SHA-256 dedupliziert. Entitäten referenzieren eine Genom-ID; geordnete Elternkanten erhalten die Abstammung. `genome_created` bewahrt übernommene Komponenten samt Node-ID-Abbildung und konkrete Mutationen. Die vollständige v0.1-Lupe mit Chronik, Zeitfilter, Umweltkontakten, Amöbenkarten und Lebensfilm bleibt erhalten. Zusätzlich stellt sie Nodes, reale Ports, gerichtete Edges, CONST-Werte und A₀ als SVG-Genomdiagramm dar.

Das portable Format 2 ist ein `.eve-run`-ZIP aus Manifest, konsistenter SQLite-Sicherung und optionalen Checkpoints. Dieselbe Lupe liest laufende Verzeichnisse und Archive read-only. Die HTTP-Oberfläche hat ausschließlich GET-Routen und keine Supervisorsteuerung; für öffentliche Bereitstellung ist eine getrennte, gehärtete Veröffentlichungskopie spezifiziert.

## Bewusst offen

- Ein exakter Replay beliebiger Ticks ist nicht implementiert; nur Checkpoint-Recovery ist nachgewiesen.
- Automatische Migration historischer Format-1-Runs fehlt bewusst. Die v0.1-Lupe bleibt ihr korrekter Leser.
- Irreversibles Downsampling diskreter RAM-Kontakte ist bis zu einer fachlichen Aufbewahrungsentscheidung zurückgestellt.
- Eine interaktive Stammbaumansicht ist noch offen. Das Genom wird bereits als anklickbares SVG-Diagramm in einem eigenen Fenster dargestellt.

## Gefundene Abweichungen

Die vollständige Liste steht in `ARCHITEKTUR.md`. Wesentlich sind die widersprüchliche P1-Statusbeschreibung im historischen v0.1-README, fehlende Endgründe in alten Runs, die bisher missverständliche Replay-Bezeichnung und die nicht langzeittauglichen Vollsnapshots/Events im Speicher. Historische Dateien wurden deshalb nicht rückwirkend bereinigt.

## Verifikation

`python3 -m unittest -v` führt 39 Tests erfolgreich aus. Hinzugekommen sind Prüfungen für zielnahe atomare Rekombination, vererbbare Suchkonstanten, genomischen Partnerrückzug und die chronologische Run-Sortierung. Zusätzlich besteht `py_compile` für alle v0.2-Pythonmodule. Begrenzter und offener Smoke-Run ergaben getrennt `tick_limit_reached` und `natural_extinction`; die exportierte SQLite-Sicherung bestand `PRAGMA integrity_check`.

Ein erster 200-Tick-Vergleich warnt vor vorschneller Konsolidierung: Die alte v0.2-Referenz erzeugte sechs Nachkommen, davon fünf ohne `MEM_WRITE`. Das experimentelle variable Suchgenom erzeugte noch keine Nachkommen, 19 Überlebende und zwei genomische Rückzüge. Auch der neue uniforme Kontrolllauf erzeugte keine Nachkommen und endete mit 15 Überlebenden. Gegenüber 43.235 Energieeinheiten aus RAM und 2.035 Leseereignissen der alten Referenz erreichten die neuen Läufe nur 26.910/1.112 beziehungsweise 20.370/1.027. Damit ist nicht die Streuung allein ursächlich; die größere Rückzugsschaltung reduziert Ausführungsdichte und Wirtschaftlichkeit. Sie bleibt deshalb ausdrücklich experimentell.

P0, P1 und v0.1 wurden fachlich nicht geändert. In v0.2 ist der Genomkostentarif nach den ersten Beobachtungsläufen versuchsweise von 0,5/0,1 auf 0,05/0,01 abgesenkt; beide Werte bleiben parametrisiert. Weitere Core-Anpassungen sind die technische Versionskennung `0.2`, Lesekompatibilität für v0.1-Checkpoints und eine RNG-neutrale Beobachtungsspur für reale Rekombination/Mutation.
