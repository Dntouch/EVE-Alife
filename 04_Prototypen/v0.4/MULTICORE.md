# Multicore-Ausführung für einen einzelnen Lauf

Ein Profil eines 30-Tick-P1-Laufs zeigt rund 61 % der Laufzeit im Heartbeat.
Davon entfallen rund 69 % auf das wiederholte Bestimmen ausführbarer
Genomknoten (`_ready`). Der eigentliche Knotenbrand ist vergleichsweise klein.

Die Amöben eines Ticks können nicht korrekt als 16 unabhängige Jobs auf den
heutigen Zustand losgelassen werden: RAM-Schreiben, Schalterreaktionen,
Membranlesen und das Plündern eines Kadavers verändern noch innerhalb desselben
Ticks den Zustand, den nachfolgende Amöben sehen. Ein naiver Prozesspool würde
damit seedgleiche Läufe abhängig vom Betriebssystem-Timing machen.

## Verbindliches Tickmodell

1. RAM, Membranen, Umwelt und Lebenszustände werden am Tickanfang eingefroren.
2. Die 16 Worker führen disjunkte Amöbengruppen gegen diesen Snapshot aus.
3. Worker liefern Zustandsänderungen als Intents zurück.
4. Intents werden stabil nach `(entity_id, sequence)` eingespielt; Konflikte
   werden dabei einmalig entschieden.
5. Reproduktion erfolgt nach dem Commit zentral und deterministisch.

Der sequentielle Modus bleibt Referenz. Run-Metadaten müssen künftig
`execution_model` und `workers` enthalten; Checkpoints dürfen nur im gleichen
Modell fortgesetzt werden.

## Abnahmekriterien

- Gleicher Seed, gleiche Workerzahl und Konfiguration ergeben bitidentische Runs.
- Konflikttests decken RAM-Schreiben, Schalter, Membranpartner und Kadaver ab.
- Ein Benchmark weist den Break-even für den Prozesspool aus.
- Ein abgebrochener 16-Worker-Lauf lässt keine Kindprozesse zurück.

Erst nach diesen Tests wird `--workers 16` in CLI und Lupe freigeschaltet.
