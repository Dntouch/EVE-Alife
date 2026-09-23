# v0.3 – Lauf 7

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `988690e0-ce93-4e14-8eb5-d11a589ec184` |
| Erzeugt | 2026-09-23T15:58:24.486049+00:00 |
| Seed | 42 |
| Altersrate | 0,005 |
| Einordnung | 10.000-Tick-Lauf mit halbierter Altersrate |

## Ergebnis

| Endtick | Startpopulation | Entitäten gesamt | Am Ende lebend | Nachkommen | Maximum | tiefste Generation | Genome | RAM-Energie |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10.000 | 20 | 183 | 13 | 163 | 55 bei Tick 1.500 | 28 | 130 | 3.546.740 |

Die Population stieg zunächst bis auf 55, ging anschließend zurück und zeigte
mehrere vorübergehende Erholungen: 37 bei Tick 4.000, 41 bei Tick 4.500, 32 bei
Tick 5.000, 40 bei Tick 5.500 und 29 bei Tick 7.500. Danach fiel sie bis auf 13
am Ticklimit. Geburten traten noch bis Tick 9.650 auf; die Population war also
anders als in Lauf 5 nicht seit langem reproduktiv erloschen.

| Zeitraum | Geburten einschließlich Gründer | Todesfälle |
| :--- | ---: | ---: |
| Tick 0–999 | 47 | 3 |
| Tick 1.000–1.999 | 32 | 25 |
| Tick 2.000–2.999 | 16 | 18 |
| Tick 3.000–3.999 | 19 | 31 |
| Tick 4.000–4.999 | 20 | 25 |
| Tick 5.000–5.999 | 13 | 13 |
| Tick 6.000–6.999 | 11 | 19 |
| Tick 7.000–7.999 | 10 | 11 |
| Tick 8.000–8.999 | 10 | 13 |
| Tick 9.000–9.999 | 5 | 12 |

## Überlebende und Genome

Von den 13 Überlebenden besaßen Ada 3 (#67) und Dario 6 (#166) Genome der
Größe 23, Olga 5 (#145) ein Genom der Größe 30. Die übrigen zehn lagen bei 191.
Ada 3 hatte mit 348.024,08 die höchste Endenergie, Dario 6 erreichte 132.481,27.
Die kleinen Genome waren energetisch erfolgreich, doch Ada 3 und Olga 5 hatten
keine direkten Kinder. Das erlaubt die Beschreibung „individuell erfolgreich,
populationsbiologisch steril“, nicht aber die Aussage, kleine Genome seien
generell steril.

Von 163 Kindgenomen waren 56 kleiner als sämtliche unmittelbaren Elterngenome;
107 entsprachen in der Größe mindestens einem Elternteil. Kein Kind war größer
als alle Eltern. Drei besonders starke Reduktionen erzeugten Ada 3 mit Größe 23
aus Eltern der Größen 168 und 191, Olga 5 mit Größe 30 aus 198 und 168 sowie
Dario 6 mit Größe 23 aus 191 und 168.

## Aussagegrenze

Dieser Lauf ist kein sauberer Test der These „doppelte Laufzeit verschiebt nur
den Kollaps“, weil gegenüber Lauf 5 gleichzeitig die Altersrate halbiert wurde.
Beobachtet wurde eine länger fortgesetzte Reproduktion und eine größere
Generationstiefe. Ob dies durch geringere Alterskosten, längere Beobachtungszeit
oder ihre Wechselwirkung entstand, muss eine kontrollierte Vergleichsmatrix
trennen.

Der Run erreicht das Ticklimit mit lebender und noch spät reproduzierender
Population. Ein Kollaps ist bis Tick 10.000 nicht beobachtet; ein langfristig
stabiler Zustand ist ebenso wenig belegt.
