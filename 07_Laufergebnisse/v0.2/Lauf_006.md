# v0.2 – Lauf 6

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `aa267dcd-cde3-416c-b539-c9eaa22b25d8` |
| Erzeugt | 2026-09-21T15:14:11.718438+00:00 |
| EVE-Version | 0.2 |
| Einordnung | 50 Startamöben, vorgesehenes Limit 5.000 Ticks |

## Ergebnis

| Endtick | Entitäten gesamt | Am Ende lebend | Nachkommen | davon ohne `MEM_WRITE` | RAM-Energie | Endgrund |
| ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 2.704 | 72 | 0 | 22 | 0 | 877.596,67 | natürliche Extinktion |

- Startpopulation: 50
- künstliches Tick-Limit: 5.000; wegen Extinktion nicht erreicht
- RAM-Leseereignisse: 27.424, davon 18.595 in der normalen RAM-Suppe
- 1.699 verschiedene normale RAM-Leseadressen
- RAM-Schreibvorgänge: 10.694 auf 56 Adressen im Bereich 1–63
- Todesfälle: 72, sämtlich wegen nicht mehr finanzierbarem Standby
- Genomkostentarif: `0,05/0,01`
- Gespeicherte Beobachtung: alle 10 Ticks
- Recovery-Checkpoints: 0; das Standardintervall 10.000 wurde nicht erreicht

Die größere Startpopulation führte zunächst zu 22 Kindern und einem Maximum von mindestens 67 gleichzeitig lebenden Amöben. Nach Tick 797 entstanden keine weiteren Entitäten; anschließend schrumpfte die Population bis zum ersten natürlichen Massenaussterben von v0.2. Alle Nachkommen besaßen mindestens einen `MEM_WRITE`-Funktionspunkt. Der Engpass lag in diesem Lauf daher nicht mehr in der bloßen Verfügbarkeit dieses Funktionspunkts.
