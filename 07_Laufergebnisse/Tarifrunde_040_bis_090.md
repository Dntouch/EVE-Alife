# Tarifrunde 40–90 · IG Amöbe gegen Lebenshaltungskosten

## Fragestellung

Wo liegt unter den aktuellen P1-Bedingungen der Übergang zwischen bloßem Überleben und einem reproduktiven Energieüberschuss? Verhandelt wurde der Ertrag einer ersten belohnten RAM-Veränderung (`novelty_base`) von 40 bis 90 in Schritten von 5.

## Konstante Bedingungen

- Seed: 42
- 20 P1-Explorer
- 200 Ticks
- Startenergie: 500 je Amöbe
- relative Geburtsenergie: 0,5
- Mindestreserve des Kindes: 5 vollständig finanzierbare Heartbeats
- zufällige RAM-Suppe mit 65.536 Zellen
- ein Snapshot pro Tick

## Ergebnis

| Energieertrag | Lauf | Entitäten gesamt | Am Ende lebend | Nachkommen | Gewonnene Energie |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 40 | [19](Lauf_019_679e5e69.md) | 20 | 5 | 0 | 56.520 |
| 45 | [20](Lauf_020_c82035b5.md) | 20 | 18 | 0 | 78.345 |
| 50 | [21](Lauf_021_c9aea05d.md) | 29 | 29 | 9 | 110.450 |
| 55 | [22](Lauf_022_f01a4e07.md) | 56 | 50 | 36 | 170.060 |
| 60 | [23](Lauf_023_6518e4f4.md) | 69 | 59 | 49 | 203.580 |
| 65 | [24](Lauf_024_a647f0d3.md) | 101 | 78 | 81 | 268.775 |
| 70 | [25](Lauf_025_24d981c0.md) | 103 | 82 | 83 | 325.570 |
| 75 | [26](Lauf_026_a919c655.md) | 143 | 116 | 123 | 456.075 |
| 80 | [27](Lauf_027_7fda6f10.md) | 161 | 128 | 141 | 564.800 |
| 85 | [28](Lauf_028_3a3366dc.md) | 175 | 142 | 155 | 633.335 |
| 90 | [29](Lauf_029_17abde73.md) | 200 | 146 | 180 | 687.330 |

## Beobachtung

- Bei 40 reicht der Tarif nur für fünf Überlebende und erzeugt keinen Nachwuchs.
- Bei 45 überleben fast alle Mitglieder der Startpopulation, aber noch immer entsteht kein reproduktiver Überschuss.
- Bei 50 wird erstmals Nachwuchs möglich. Alle 29 bis dahin erzeugten Amöben leben am Ende des Laufs.
- Von 50 bis 90 steigen Nachkommen und Endpopulation insgesamt deutlich an. Der untersuchte Bereich zeigt damit eine Übergangszone, keinen einzelnen universellen Kipppunkt.
- Die Wiederholungen bei 40 und 80 reproduzieren die früheren Läufe 15 und 17 exakt. Das bestätigt für diese Bedingungen den deterministischen Versuchsaufbau.

## Vorläufiges Verhandlungsergebnis

Die IG Amöbe kann **45 als Überlebenstarif**, aber nicht als reproduktionsfähigen Tarif anerkennen. **50 ist die erste beobachtete Untergrenze für Fortpflanzung**. Ein belastbarer Tarif mit deutlicher Populationsentwicklung beginnt in dieser Versuchsreihe eher zwischen **55 und 65**. Diese Aussage gilt für genau die oben dokumentierten Bedingungen und noch nicht allgemein für andere Genome, Seeds oder Laufzeiten.
