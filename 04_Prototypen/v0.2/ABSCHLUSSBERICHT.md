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

`python3 -m unittest` führt 51 Tests erfolgreich aus. Hinzugekommen sind Prüfungen für zielnahe atomare Rekombination, vererbbare Suchkonstanten, genomischen Partnerrückzug, chronologische Run-Sortierung, Zustellung und Verfall eines Klopfers, mehrere Klopfer in FIFO-Reihenfolge, stabile erbliche Bindungsdauer, gegenseitige Dreiergruppen und die vollständige Finanzierung einer Geburt durch einen einzelnen Elternteil. Zusätzlich besteht `py_compile` für alle v0.2-Pythonmodule. Begrenzter und offener Smoke-Run ergaben getrennt `tick_limit_reached` und `natural_extinction`; die exportierte SQLite-Sicherung bestand `PRAGMA integrity_check`.

Ein erster 200-Tick-Vergleich warnt vor vorschneller Konsolidierung: Die alte v0.2-Referenz erzeugte sechs Nachkommen, davon fünf ohne `MEM_WRITE`. Das experimentelle variable Suchgenom erzeugte noch keine Nachkommen, 19 Überlebende und zwei genomische Rückzüge. Auch der neue uniforme Kontrolllauf erzeugte keine Nachkommen und endete mit 15 Überlebenden. Gegenüber 43.235 Energieeinheiten aus RAM und 2.035 Leseereignissen der alten Referenz erreichten die neuen Läufe nur 26.910/1.112 beziehungsweise 20.370/1.027. Damit ist nicht die Streuung allein ursächlich; die größere Rückzugsschaltung reduziert Ausführungsdichte und Wirtschaftlichkeit. Sie bleibt deshalb ausdrücklich experimentell.

P0, P1 und v0.1 wurden fachlich nicht geändert. In v0.2 ist der Genomkostentarif nach den ersten Beobachtungsläufen versuchsweise von 0,5/0,1 auf 0,05/0,01 abgesenkt; beide Werte bleiben parametrisiert. Weitere Core-Anpassungen sind die technische Versionskennung `0.2`, Lesekompatibilität für v0.1-Checkpoints und eine RNG-neutrale Beobachtungsspur für reale Rekombination/Mutation.

Lauf 6 zeigte als konkrete Ursache der Generationsgrenze, dass Vorschläge beim Absender lagen und vom Ziel nie gelesen wurden. Die daraufhin experimentell ergänzte Klingel transportiert den letzten gültigen Vorschlag mit Herkunft, verlangt aber weiterhin eine genomische Antwort. Im kontrollierten Lauf 7 mit denselben 50 Gründern und Seed 42 stieg die Generationstiefe von 2 auf 20 und die Nachkommenzahl von 22 auf 134. Zugleich wurden 1.097 Klopfer, 645 Überschreibungen und 8.604 energetisch abgewiesene Geburtsversuche beobachtet. Die Zustellungslücke ist damit nachgewiesen; die konkrete Klingeldynamik bleibt wegen möglicher Wiederholungs- und Konkurrenzschleifen vorläufig.

Nach Lauf 7 wurde die experimentelle Schicht erweitert: Nₖ macht die Zahl erinnerter Klopfer erblich, Tₚ die Mindestdauer einer unverändert gegenseitigen Gruppe. Das Startgenom liest nun bis zu zwei Klopfer in beide vorhandenen Partnerslots und kann dadurch technisch auch Dreiergruppen bilden. Diese Erweiterung ist noch kein Laufergebnis und keine Festschreibung des Fachmodells; Lauf 7 bleibt als historischer Einzelklopfer-Vergleich unverändert dokumentiert.

Lauf 8 erprobte diesen Stand mit 50 Gründern und 2.000 Ticks. Er erzeugte 43 Nachkommen bis Generation 5, 388 Klopfereignisse und nur 50 Verdrängungen, aber keine Dreiergeburt. Gegenüber Lauf 7 ist die Konkurrenz an der Klingel deutlich kleiner, während die Fortpflanzung geringer ausfiel. Die Bindungszeit ist eine plausible, aber mit diesem einzelnen kombinierten Versuch nicht isoliert belegte Ursache.

Mit dem optionalen Modus `--ram-world toys` kamen feste Muster, autonome Blasen und gekoppelte Schalter als rein RAM-basierte Umwelt hinzu. Lauf 9 zeigte, dass eine nur mittel/global gestreute Platzierung für die derzeitige Exploration unerreichbar blieb. Nach Staffelung über unmittelbaren, mittleren und globalen RAM erreichte Lauf 10 insgesamt 31 Spielzeugadressen, las sie 1.481-mal und löste 145 Schalterreaktionen aus. Diese Zahlen belegen Funktion und Kontakt, nicht bereits kausales Verständnis.

Lauf 11 entkoppelte erstmals Entity-ID und RAM-Standort. Alle 50 Gründer erhielten verschiedene, seed-reproduzierbare Positionen; die 29 Kinder entstanden höchstens 31 Zellen von mindestens einem Elternteil entfernt. Mit lokalen Offsets wurden nur sieben Spielzeugzellen getroffen. Das zeigt, dass die starke Interaktion in Lauf 10 wesentlich aus den gemeinsamen absoluten Suchwegen nahe RAM null stammte. Die geringere Begegnungsrate wird als räumliches Ergebnis dokumentiert und nicht durch populationsbezogene Objektplatzierung kaschiert.

Der anschließende Stabilitätstest Lauf 12 erreichte das Limit von 5.000 Ticks nicht und endete bei Tick 2.042 mit natürlicher Extinktion. Nach einem Maximum von 79 Lebenden bei Tick 370 fiel die Population dauerhaft; die letzte Geburt erfolgte bei Tick 1.140. Alle 36 Nachkommen besaßen `MEM_WRITE`, Generation 6 wurde erreicht, aber dynamische Spielzeuge blieben ungelesen. Für Seed 42 ist der aktuelle Stand deshalb keine stabile Kultur; alle 86 Todesfälle beruhten auf nicht mehr finanzierbarem Standby.

Läufe 14 und 15 verteilten Spielzeuge anschließend flächendeckend auf 128 Habitate. Beide Populationen starben trotz gut versorgter Einzeltiere aus. Lauf 15 lieferte 3.728 Ablehnungen durch die starre Einzelbeitragsregel und führte zur fachlichen Präzisierung der Geburtsfinanzierung: Entscheidend ist nun der gemeinsame Überschuss aller Eltern über ihrem jeweiligen `S₀`; zahlungsfähige Eltern können fehlende Anteile vollständig übernehmen.

Der direkte Vergleich Lauf 16 erreichte mit dieser Regel 75 Nachkommen, Generation 8 und eine letzte Geburt bei Tick 2.085. Damit verbesserte er Lauf 15 deutlich, bildete aber weiterhin keine stabile Kultur. Bei Tick 5.000 lebte allein Ada 4 mit 101.120,55 Energie und einem auf Größe 30 reduzierten Genom ohne ausführbares `MEM_WRITE`. Das Ergebnis trennt individuelle Energieeffizienz von populationsweitem Fortbestand. Eine erste Kostenrechnung spricht gegen den Genomtarif als alleinige Ursache; als nächster Schritt ist der Verlust des Sozialfragments je Generation auszuwerten.
