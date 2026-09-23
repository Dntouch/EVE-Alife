# EVE-Alife – Laufergebnisse v0.3

Diese Chronik umfasst ausschließlich Runs des Prototyps `v0.3`. Die Nummerierung
beginnt innerhalb der Version wieder bei Lauf 1 und folgt dem gespeicherten
Erzeugungszeitpunkt. Technische Supervisor- und Oberflächentests werden
mitgeführt, aber ausdrücklich nicht als wissenschaftliche Versuche behandelt.

| Lauf | Ticks | Am Ende lebend | Nachkommen | tiefste Generation | RAM-Energie | Einordnung |
| ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| [7](Lauf_007.md) | 10.000 | 13 | 163 | 28 | 3.546.740 | Altersrate 0,005; längerer, aber konfundierter Vergleich |
| [6](Lauf_006.md) | 5.000 | 1 | 89 | 12 | 916.670 | exakte Wiederholung von Lauf 5 |
| [5](Lauf_005.md) | 5.000 | 1 | 89 | 12 | 916.670 | Standardlauf; Clara 4 als letzte Überlebende |
| [4](Lauf_004.md) | 237 | 29 | 9 | 2 | 30.955 | früher kontrollierter Stopp des v0.3-Standards |
| [3](Lauf_003.md) | 86 | 58 | 8 | 1 | 21.090 | technischer Test des kontrollierten Stopps |
| [2](Lauf_002.md) | 12 | ausgestorben | 0 | 0 | 2 | technischer Test natürlicher Extinktion |
| [1](Lauf_001.md) | 200 | 79 | 29 | 2 | 62.295 | kurzer Simulations- und Lupe-Prüflauf |

## Vorläufiges Bild der Versuchsreihe

Die beiden 5.000-Tick-Läufe sind nicht nur in ihren Endwerten gleich. Die
Tabellen `measurements`, `entities`, `ancestry`, `genomes` und `events` sind
zeilenweise identisch. Damit bestätigt die Wiederholung den deterministischen
Run bei gleichem Seed und gleichen Parametern.

Im 5.000-Tick-Standardlauf endeten Geburten bei Tick 2.941. Danach sank die
Population von 17 bei Tick 3.000 auf eine einzige lebende Amöbe bei Tick 5.000.
Clara 4 überlebte mit einem Genom der Größe 23; dieses starke Schrumpfen war
bereits bei ihrer Geburt entstanden.

Lauf 7 erreichte über 10.000 Ticks 163 Nachkommen und Generation 28. Geburten
traten noch bis Tick 9.650 auf, die Population sank am Ende dennoch auf 13.
Dieser Lauf halbierte zugleich die Altersrate von `0,01` auf `0,005`. Er kann
daher nicht isoliert beantworten, ob eine bloße Verdopplung der Laufdauer auch
den Zeitpunkt eines Kollapses verdoppelt hätte.

Über beide langen Konfigurationen entstand kein einziges Kind mit einem Genom,
das größer als sämtliche unmittelbaren Elterngenome war. Im Standardlauf waren
33 von 89 Kindgenomen kleiner als alle Eltern; im 10.000-Tick-Lauf waren es 56
von 163. Das ist eine klare Beobachtung dieser Runs, aber noch keine Erklärung
des Mechanismus oder Selektionsvorteils.

## Nächste Analyse

Vor Änderungen an den Umweltbedingungen werden mindestens getrennt betrachtet:

- Altersrate und Laufdauer in einem faktoriell sauberen Vergleich,
- Geburten- und Sterberate in den einzelnen Zeitabschnitten,
- struktureller Bias der Rekombination zu kleineren Genomen,
- Fortpflanzungsfähigkeit kleiner Überlebendengenome,
- Energiegewinn, räumliche Begegnung und Populationsrückgang.

[Zur versionsübergreifenden Übersicht](../README.md)
