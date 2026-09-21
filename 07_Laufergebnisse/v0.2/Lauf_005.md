# v0.2 – Lauf 5

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `c2b30f1a-88dd-4368-a1bd-807745379e95` |
| Erzeugt | 2026-09-21T13:13:08.092424+00:00 |
| EVE-Version | 0.2 |
| Einordnung | erster 2.000-Tick-Lauf mit reduziertem Genomkostentarif |

## Ergebnis

| Ticks | Entitäten gesamt | Am Ende lebend | Nachkommen | davon ohne `MEM_WRITE` | RAM-Energie |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2.000 | 27 | 11 | 7 | 0 | 401.840 |

- RAM-Leseereignisse: 11.702, davon 8.760 in der normalen RAM-Suppe
- 1.234 verschiedene normale RAM-Leseadressen
- RAM-Schreibvorgänge: 4.782 auf 24 Adressen im Bereich 1–26
- Todesfälle: 16, sämtlich wegen nicht mehr finanzierbarem Standby
- Genomkostentarif: `0,05/0,01`
- Gespeicherte Beobachtung: alle 10 Ticks
- Recovery-Checkpoints: 0; das Standardintervall 10.000 wurde nicht erreicht

Wie im 500-Tick-Lauf entstanden sieben Nachkommen, diesmal über den längeren Zeitraum jedoch keine weiteren. Alle Kinder behielten mindestens einen `MEM_WRITE`-Funktionspunkt. Die Leseexploration erreichte wesentlich mehr RAM-Adressen, während die Schreibzugriffe weiterhin auf den ID-nahen Bereich konzentriert blieben.
