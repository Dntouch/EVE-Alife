# v0.2 – Lauf 7

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `a95a43b9-b6d3-41d7-aebb-57ad72731e7e` |
| Erzeugt | 2026-09-21T15:35:33.402424+00:00 |
| EVE-Version | 0.2 |
| Einordnung | erster kontrollierter Lauf mit experimenteller Klingel |

## Ergebnis

| Ticks | Entitäten gesamt | Am Ende lebend | Nachkommen | davon ohne `MEM_WRITE` | tiefste Generation | RAM-Energie |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2.000 | 184 | 30 | 134 | 0 | 20 | 1.042.111,67 |

- Startpopulation: 50
- maximale gleichzeitig lebende Population: 114 bei Tick 580
- Klopfereignisse: 1.097
- davon mit Überschreiben eines anderen Klopfers: 645
- abgewiesene Geburtsversuche wegen fehlenden Elternüberschusses: 8.604
- Todesfälle: 154
- Genomkostentarif: `0,05/0,01`

Unter denselben 50 Gründern und Seed 42 wie Lauf 6 durchbrach die Klingel die vorherige Grenze bei Generation 2 deutlich. Bereits bei Tick 245 war Generation 4 erreicht, am Ende Generation 20. Die Population wuchs zunächst stark und sank danach trotz fortgesetzter Geburten wieder.

Das Ergebnis bestätigt die fehlende Zustellung als realen Fortpflanzungsengpass. Es konsolidiert die konkrete Klingelregel noch nicht: Die hohe Zahl überschriebener Klopfer und wiederholter energetisch abgewiesener Geburtsversuche kann auf eine zu leicht ausgelöste Antwort- oder Wiederholungsschleife hinweisen.
