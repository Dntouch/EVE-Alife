# Versionsgrenze v0.2 → v0.3

`v0.2` ist konserviert und wird für die Entwicklung von v0.3 nicht verändert.
Der Startstand von v0.3 wurde aus den Quell- und Dokumentationsdateien des
letzten v0.2-Stands übernommen; Laufdaten und Python-Caches wurden nicht kopiert.

v0.3 beginnt als Oberflächen- und Informationsarchitektur-Revision. Das
persistierte Run-Datenformat bleibt deshalb vorerst `eve-alife-run`, Version 2.
Eine neue Formatversion setzt eine fachlich notwendige Schemaänderung voraus und
wird nicht allein wegen einer neuen Darstellung eingeführt.

## Umgesetzter Zwischenstand vom 22. September 2026

- getrennte Arbeitsbereiche für Leitstand, Historie, Chronik, Stammbaum und Genom
- EVE-Navigation und eigenes Hintergrundmotiv
- lineares, zoombares und verschiebbares RAM-Band
- bildschirmabhängige Gruppierung überlappender Amöben
- seitlicher Fokus für eine gezielt beobachtete Amöbe
- zoombarer Genom-Arbeitsraum mit Beziehungsfokus und optionalem Einzelfenster
- evolutionäre Zeitlandschaft mit Verwandtschaftslinse und Genomprovenienz
- EVE-Evolutionsverlauf mit Population, Genomvielfalt und Schlüsselereignissen
- versionsübergreifendes Run-Archiv mit Run-Vergleich und Hall of Life
- gemeinsamer Fokusmodus für Stammbaum und Genom
- getrennter Supervisor für Presets, offene Runs, kontrollierten Stopp und Fortsetzung
- ausdrückliche Kennzeichnung der Read-only- und Replay-Grenzen

Diese Funktionen erweitern Beobachtung, Navigation und Bedienung. Sie ändern
keine v0.2-Fachregel. Neue wissenschaftliche Regeln oder persistierte
Simulationsgrößen erfordern weiterhin eine bewusste Spezifikations- und
Formatentscheidung.
