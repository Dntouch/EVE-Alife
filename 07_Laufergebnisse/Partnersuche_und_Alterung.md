# Dynamische Partnersuche und Alterskosten

Die bisherigen Tarifläufe erzeugten viele Nachkommen, aber keine Enkel. Die fest im technischen Startgenom hinterlegten Partner-IDs privilegierten die Gründerpaare und machten Kinder faktisch steril. Gleichzeitig konnten erfolgreiche Gründer bei konstantem Standby unbegrenzt alt werden.

## Änderungen

- P1 berechnet den Partner aus der eigenen Laufzeit-ID: `((ID - 1) XOR 1) + 1`.
- Die Berechnung und das Schreiben des Partnerslots erfolgen vollständig durch das Genom.
- Nach erfolgreicher Geburt bleiben die Partnerslots wie bisher leer und müssen erneut beschrieben werden.
- Neue Läufe zahlen zusätzlich `Alter × 0,01` Energie je Heartbeat.
- Es gibt weiterhin kein festes Höchstalter.

## Generationstest

[Lauf 31](Lauf_031_c61fd90c.md) über 300 Ticks:

- 58 Entitäten insgesamt,
- 52 am Ende lebend,
- 38 Nachkommen,
- erstmals Generation 2,
- das Nachkommenpaar 41/42 erzeugte selbst zwei Kinder.

Damit ist die vollständige Sterilität der Nachkommen beseitigt.

## Langzeitvergleich bei Tarif 60

[Lauf 32](Lauf_032_b623e0f1.md) über 1.000 Ticks:

| Tick | Lebend | Insgesamt geboren |
| ---: | ---: | ---: |
| 100 | 30 | 31 |
| 200 | 39 | 43 |
| 300 | 52 | 58 |
| 400 | 56 | 67 |
| 500 | 58 | 70 |
| 600 | 54 | 70 |
| 700 | 49 | 71 |
| 800 | 41 | 71 |
| 900 | 34 | 71 |
| 1.000 | 32 | 71 |

Endstand: 51 Nachkommen, 32 lebend, 39 verstorben, Generationstiefe 2 und 1.232.700 gewonnene Energie. 19 der 20 Gründer starben; Emmi erreichte dennoch 1.000 Ticks.

## Einordnung

Die Alterskosten wirken und brechen das bisherige nahezu unbegrenzte Gründerprivileg deutlich auf. Tarif 60 ermöglicht weiterhin langfristiges Überleben und Fortpflanzung, trägt unter den neuen Bedingungen aber nach Tick 500 kein weiteres Populationswachstum.

Die Partnersuche löst das ursprüngliche Sterilitätsproblem nur teilweise: Enkel existieren, Generation 3 noch nicht. Das vollständige Partnerfragment übersteht die bisherige Rekombination offenbar nicht zuverlässig genug. Dieser Befund sollte vor einer weiteren Tariferhöhung untersucht werden.
