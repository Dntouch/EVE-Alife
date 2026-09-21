# v0.2 – Lauf 11

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `3c87e310-3b4e-4099-91b0-3722588c7d9e` |
| Erzeugt | 2026-09-21T16:34:28.078736+00:00 |
| EVE-Version | 0.2 |
| Einordnung | erster Spielzeuglauf mit lokalen RAM-Koordinaten |

## Ergebnis

| Ticks | Entitäten gesamt | Am Ende lebend | Nachkommen | RAM-Energie |
| ---: | ---: | ---: | ---: | ---: |
| 500 | 79 | 78 | 29 | 186.720 |

- 50 verschiedene Gründerstandorte
- räumliche Spanne der Gründer: RAM 473 bis 64.521
- mittlere minimale Kind-Eltern-Distanz: 17,62 Zellen
- größte minimale Kind-Eltern-Distanz: 31 Zellen
- maximale gleichzeitig lebende Population: 79 bei Tick 370
- erreichte Spielzeugadressen: 7 von 160
- Lesezugriffe auf Spielzeugadressen: 7, ausschließlich Steinzellen
- autonome Blasenänderungen: 178
- Schalterreaktionen: 0
- Todesfälle: 1

Die fortlaufende Entity-ID bestimmt den Standort nicht mehr. Gründer sind über die ringförmige Suppe verteilt; jedes Kind lag innerhalb des festgelegten Radius 32 um mindestens einen Elternstandort.

Die lokale Sicht beseitigt zugleich die frühere unbeabsichtigte Bevorzugung niedriger RAM-Adressen: In Lauf 10 starteten alle Suchwege nahe null und trafen deshalb 31 Spielzeugadressen 1.481-mal. Mit verteilten Standorten traf Lauf 11 nur sieben Steinzellen. Blasen und Schalter waren funktional aktiv, lagen aber nicht auf den in 500 Ticks erkundeten lokalen Wegen. Das ist ein räumliches Ökologieergebnis und kein Defekt; eine höhere oder populationsbezogen platzierte Dichte wurde nicht nachträglich erzwungen.
