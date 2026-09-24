# v0.4 – Lauf 003: Die Alterskante zwischen 0,01 und 0,008

## Fragestellung

Nach dem Populationsdurchbruch von Lauf 002 wurde die Altersrate von `0,005`
auf `0,01` angehoben. Zwei kurze, ansonsten gleiche Spielzeugläufe sollten
zeigen, ob alte Amöben dadurch früher abgelöst werden und ob weiterhin eine
tragfähige Folgepopulation entsteht.

Beide Läufe verwendeten Seed 42, 20 P1-Explorer mit je 500 Startenergie, 128
Spielzeughabitate, einen Neuheitsgrundwert von 60 und ein Ticklimit von 5.000.
Der zweite Lauf unterschied sich ausschließlich durch die Altersrate.

## Vergleich

| Kennzahl | Altersrate 0,01 | Altersrate 0,008 |
| --- | ---: | ---: |
| Run-ID | `dff5f41b-e7a5-4364-8289-eddcc8997ac7` | `704828a9-571f-4c7c-a355-78450ad38ad4` |
| erreichter Tick | 2.134 | 5.000 |
| Endzustand | ausgestorben | 117 lebend |
| Populationsmaximum | 33 | 117 |
| Amöben insgesamt | 38 | 350 |
| Nachkommen | 18 | 330 |
| letzter Nachwuchs | Tick 1.195 | Tick 4.991 |
| abgelehnte Fortpflanzungen | 406 | 2.930 |
| unterschiedliche Genome | 37 | 331 |
| Laufzeit | 26,3 s | 137,1 s |

Im `0,01`-Lauf starben alle 38 Amöben mit
`standby_unaffordable`. Die Population erreichte bereits bei Tick 450 ihr
Maximum, die letzte Geburt erfolgte bei Tick 1.195. Danach fehlte über 900
Ticks jede Generationenerneuerung. Die kumulierten Alterskosten wachsen mit
der Lebensdauer quadratisch und verbrauchten schließlich auch bei erfolgreichen
Sammlern die verfügbare Energie. Das Ergebnis ist daher keine plötzlich
versiegte Zuckerquelle, sondern eine demografische Altersfalle.

Der `0,008`-Lauf zeigt eine andere Dynamik. Nach einem ersten Maximum von 55
Lebenden bei Tick 800 fiel die Population bis auf 19 bei Tick 2.600 zurück.
Anschließend erholte sie sich und stieg bis Tick 5.000 auf 117. Es entstanden
bis zum letzten Messabschnitt weiter Kinder. Der Verlauf enthält damit die
gesuchte Welle und einen Generationswechsel, endet jedoch erneut in einer
beschleunigten Wachstumsphase. Ein langfristiges Gleichgewicht ist noch nicht
belegt.

## Leistungsbasis

Beide Läufe wurden vom weiterhin seriellen Fachkern ausgeführt. Der
`0,008`-Lauf erreichte 36,5 Ticks pro Sekunde bei durchschnittlich etwa 47
Lebenden. Der früh ausgestorbene `0,01`-Lauf erreichte 81,1 Ticks pro Sekunde
bei durchschnittlich etwa 18 Lebenden. Als grobe populationsbereinigte
Vergleichsgröße ergeben sich 1.716 beziehungsweise 1.488 Amöben-Ticks pro
Sekunde.

Diese Werte sind die Single-Core-Basis für die geplante Mehrkernumsetzung. Das
in `04_Prototypen/v0.4/MULTICORE.md` beschriebene Snapshot-/Intent-Modell ist
noch nicht implementiert; insbesondere existiert noch kein freigegebenes
`--workers 16`.

## Folgerung

`0,01` ist unter diesen Bedingungen zu hoch. `0,008` verhindert das
Aussterben und erzeugt zunächst die gewünschte Wellenbewegung, lässt am Ende
aber wieder deutliches Wachstum zu. Eine eventuelle Feinabstimmung zwischen
`0,0081` und `0,0089` wird erst nach der deterministischen Mehrkernumsetzung
fortgesetzt, damit die Versuchsreihe auf einer schnelleren und ausdrücklich
reproduzierbaren Ausführungsbasis entsteht.
