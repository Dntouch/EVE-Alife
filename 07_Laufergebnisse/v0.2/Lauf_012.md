# v0.2 – Lauf 12

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `b924d981-e9af-4092-aab5-c8d988cdd950` |
| Erzeugt | 2026-09-21T16:42:03.429055+00:00 |
| EVE-Version | 0.2 |
| Einordnung | Stabilitätsprüfung des räumlichen Spielzeugmodells bis maximal 5.000 Ticks |

## Ergebnis

| Endtick | Entitäten gesamt | Am Ende lebend | Nachkommen | tiefste Generation | RAM-Energie | Endgrund |
| ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 2.042 | 86 | 0 | 36 | 6 | 543.120 | natürliche Extinktion |

- Startpopulation: 50
- maximale Population: 79 bei Tick 370
- letzter Nachwuchs: Tick 1.140
- Geburten aus Zweiergruppen: 36
- Geburten aus Dreiergruppen: 0
- Nachkommen ohne `MEM_WRITE`: 0
- Klopfereignisse: 376, davon 44 Verdrängungen
- abgewiesene Geburtsversuche: 3.746
- erreichte Spielzeugadressen: 8 von 160
- Spielzeug-Lesezugriffe: 9, ausschließlich Steinzellen
- autonome Blasenänderungen: 762
- Todesursache aller 86 Amöben: Standby nicht mehr finanzierbar

## Populationsverlauf

| Tick | Lebend |
| ---: | ---: |
| 0 | 50 |
| 250 | 73 |
| 500 | 78 |
| 750 | 57 |
| 1.000 | 30 |
| 1.250 | 29 |
| 1.500 | 18 |
| 1.750 | 10 |
| 2.000 | 3 |
| 2.042 | 0 |

Der Lauf erreichte das gesetzte Limit von 5.000 Ticks nicht. Die Kultur wuchs zunächst, überschritt ihre Startpopulation bis Tick 750 und reproduzierte sich bis Tick 1.140. Danach fehlte nachhaltiger Energiegewinn; sämtliche Todesfälle traten durch nicht mehr finanzierbaren Standby ein.

Für Seed 42 ist der aktuelle Stand damit keine stabile Kultur. Unfruchtbarkeit war nicht der Engpass, und auch die Zustellung funktionierte bis Generation 6. Die dynamischen Spielzeuge waren lokal nicht erreichbar: Trotz 762 Blasenänderungen wurde keine Blase und kein Schalter gelesen. Aus einem einzelnen Seed folgt noch keine allgemeine Aussage über andere räumliche Verteilungen.
