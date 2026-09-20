# Langzeitlauf · Tarif 60

## Fragestellung

Der Arbeitgeber EVE-Alife Industries hält einen Energieertrag von 90 für zu teuer. Reicht der in der Tarifrunde bereits reproduktionsfähige Tarif 60 auch über eine deutlich längere Laufzeit, oder bricht die Population später zusammen beziehungsweise wächst unkontrolliert?

## Versuchsaufbau

- [Lauf 30](Lauf_030_8f28241b.md)
- Seed: 42
- 20 P1-Explorer
- 1.000 Ticks
- Energieertrag (`novelty_base`): 60
- Startenergie: 500 je Amöbe
- relative Geburtsenergie: 0,5
- Mindestreserve des Kindes: 5 vollständig finanzierbare Heartbeats
- zufällige RAM-Suppe mit 65.536 Zellen
- Beobachtungssnapshot alle 10 Ticks; vollständiger Ereignisstrom

## Populationsverlauf

| Tick | Lebend | Insgesamt geboren |
| ---: | ---: | ---: |
| 1 | 20 | 20 |
| 100 | 36 | 42 |
| 200 | 59 | 69 |
| 300 | 73 | 92 |
| 400 | 89 | 115 |
| 500 | 106 | 136 |
| 600 | 120 | 160 |
| 700 | 137 | 184 |
| 800 | 155 | 207 |
| 900 | 169 | 228 |
| 1.000 | 179 | 250 |

## Endstand

- 230 Nachkommen
- 179 lebende Amöben
- 71 verstorbene Amöben
- 3.078.540 gewonnene Energieeinheiten
- kürzestes abgeschlossenes Leben: Willi, 15 Ticks
- längstes abgeschlossenes Leben: Erna 5, 138 Ticks

## Beobachtung

Tarif 60 trägt die Population über 1.000 Ticks. An keinem der betrachteten 100-Tick-Punkte sinkt die Zahl der Lebenden. Gleichzeitig zeigt der Verlauf keine explosive Vervielfachung: Die Zahl aller Geburten wächst nach Tick 100 grob linear um etwa 21 bis 27 Amöben je 100 Ticks. Die lebende Population wächst ebenfalls weiter, zuletzt jedoch langsamer.

Der Lauf widerlegt damit für diese Bedingungen sowohl einen späten vollständigen Zusammenbruch als auch eine unmittelbare exponentielle Bevölkerungsexplosion. Er beweist noch kein dauerhaftes Gleichgewicht: Nach 1.000 Ticks wächst die Population weiterhin, und ein einzelner Seed beschreibt keine Streuung zwischen verschiedenen Umweltinitialisierungen.

## Vorläufiges Verhandlungsergebnis

**Tarif 60 ist als langfristig tragfähiger Versuchstarif akzeptabel.** Aus Sicht der IG Amöbe finanziert er nicht nur das Überleben, sondern kontinuierliche Fortpflanzung. Aus Sicht des Arbeitgebers bleibt das Wachstum im beobachteten Zeitraum beherrschbar. Die nächste belastbare Prüfung wären mehrere Seeds oder ein nochmals längerer Lauf, nicht eine weitere Erhöhung des Tarifs.
