# v0.2 – Lauf 8

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `7b1c6959-158a-4627-be3c-3fed81170ac9` |
| Erzeugt | 2026-09-21T16:03:11.808963+00:00 |
| EVE-Version | 0.2 |
| Einordnung | erster Lauf mit vererbbarer Mehrfachklingel und Bindungszeit |

## Ergebnis

| Ticks | Entitäten gesamt | Am Ende lebend | Nachkommen | davon ohne `MEM_WRITE` | tiefste Generation | RAM-Energie |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2.000 | 93 | 4 | 43 | 0 | 5 | 548.355 |

- Startpopulation: 50
- maximale gleichzeitig lebende Population: 84 bei Tick 550
- Klopfereignisse: 388
- davon mit Verdrängung des ältesten Klopfers: 50
- abgewiesene Geburtsversuche: 4.710
- Geburten aus Zweiergruppen: 43
- Geburten aus Dreiergruppen: 0
- Todesfälle: 89
- Genomkostentarif: `0,05/0,01`
- Gründer-Nₖ: 10×1, 20×2, 11×3, 9×4
- Gründer-Tₚ: erblich gestreut von 3 bis 12

Gegenüber Lauf 7 sank die Zahl verdrängter Klopfer von 645 auf 50. Die Mehrfachklingel beseitigt damit einen großen Teil der Zustellungskonkurrenz. Gleichzeitig erreichte dieser einzelne Lauf mit 43 Nachkommen und Generation 5 deutlich weniger Fortpflanzung als der Einzelklopfer-Lauf 7 mit 134 Nachkommen und Generation 20. Die zusätzlich erforderliche stabile Bindungszeit ist eine naheliegende Ursache, lässt sich aus einem Lauf aber nicht isoliert beweisen.

Alle 43 Geburten stammten aus gegenseitigen Zweiergruppen. Die neue Schaltung und der Core können Dreiergruppen bilden, der Lauf lieferte jedoch keine vollständig gegenseitige Dreierbeziehung bis zur Geburt. Nₖ und Tₚ bleiben deshalb ausdrücklich experimentell; insbesondere folgt aus diesem Ergebnis weder eine optimale Kapazität noch eine geeignete Bindungsdauer.
