# EVE-Alife – Laufergebnisse

Dieser Bereich enthält die kompakten, versionierten Berichte der tatsächlich ausgeführten Prototyp-Läufe. Jeder Bericht hält Identität, Git-Stand, Konfiguration, Populationsresultat, Energiegewinn und Lebensrekorde fest.

Die vollständigen Rohdaten bleiben lokal unter `04_Prototypen/v0.1/runs/`: Ein einzelner Lauf kann hunderte Megabyte an Snapshots, RAM-Zuständen, Checkpoints und Ereignissen enthalten. Sie werden deshalb nicht ungeprüft in Git aufgenommen. Die Berichte hier sind aus diesen Rohdaten reproduzierbar.

Zusammenhängende Versuchsreihen werden zusätzlich ausgewertet:

- [Tarifrunde 40–90: IG Amöbe gegen Lebenshaltungskosten](Tarifrunde_040_bis_090.md)
- [Langzeitlauf mit Tarif 60](Langzeitlauf_Tarif_060.md)
- [Dynamische Partnersuche und Alterskosten](Partnersuche_und_Alterung.md)
- [Membransuche, Einladung und RAM-Schreiben](Membransuche_und_RAM_Schreiben.md)

## Übersicht

| Lauf | Ticks | Status | Nachkommen | Energiegewinn |
| ---: | ---: | :--- | ---: | ---: |
| [39](Lauf_039.md) | 1000 | 26 lebend | 17 | 342.314,83 |
| [38](Lauf_038.md) | 1000 | 28 lebend | 20 | 354.840,00 |
| [37](Lauf_037.md) | 1000 | 17 lebend | 14 | 278.035,00 |
| [36](Lauf_036.md) | 1000 | 38 lebend | 29 | 388.240,00 |
| [35](Lauf_035.md) | 300 | 27 lebend | 9 | 218.080,00 |
| [34](Lauf_034.md) | 300 | Massenaussterben | 0 | 17.380,00 |
| [33](Lauf_033.md) | 300 | Massenaussterben | 0 | 28.420,00 |
| [32](Lauf_032.md) | 1000 | 32 lebend | 51 | 1.232.700,00 |
| [31](Lauf_031.md) | 300 | 52 lebend | 38 | 289.080,00 |
| [30](Lauf_030.md) | 1000 | 179 lebend | 230 | 3.078.540,00 |
| [29](Lauf_029.md) | 200 | 146 lebend | 180 | 687.330,00 |
| [28](Lauf_028.md) | 200 | 142 lebend | 155 | 633.335,00 |
| [27](Lauf_027.md) | 200 | 128 lebend | 141 | 564.800,00 |
| [26](Lauf_026.md) | 200 | 116 lebend | 123 | 456.075,00 |
| [25](Lauf_025.md) | 200 | 82 lebend | 83 | 325.570,00 |
| [24](Lauf_024.md) | 200 | 78 lebend | 81 | 268.775,00 |
| [23](Lauf_023.md) | 200 | 59 lebend | 49 | 203.580,00 |
| [22](Lauf_022.md) | 200 | 50 lebend | 36 | 170.060,00 |
| [21](Lauf_021.md) | 200 | 29 lebend | 9 | 110.450,00 |
| [20](Lauf_020.md) | 200 | 18 lebend | 0 | 78.345,00 |
| [19](Lauf_019.md) | 200 | 5 lebend | 0 | 56.520,00 |
| [18](Lauf_018.md) | 200 | 324 lebend | 399 | 2.720.160,00 |
| [17](Lauf_017.md) | 200 | 128 lebend | 141 | 564.800,00 |
| [16](Lauf_016.md) | 200 | Massenaussterben | 0 | 2.700,00 |
| [15](Lauf_015.md) | 200 | 5 lebend | 0 | 56.520,00 |
| [14](Lauf_014.md) | 200 | Massenaussterben | 0 | 7.640,00 |
| [13](Lauf_013.md) | 100 | Massenaussterben | 0 | 2.700,00 |
| [12](Lauf_012.md) | 100 | Massenaussterben | 0 | 0,00 |
| [11](Lauf_011.md) | 100 | Massenaussterben | 21 | 0,00 |
| [10](Lauf_010.md) | 100 | Massenaussterben | 57 | 0,00 |
| [9](Lauf_009.md) | 100 | Massenaussterben | 10 | 0,00 |
| [8](Lauf_008.md) | 30 | Massenaussterben | 91 | 0,00 |
| [7](Lauf_007.md) | 30 | Massenaussterben | 93 | 0,00 |
| [6](Lauf_006.md) | 30 | Massenaussterben | 93 | 0,00 |
| [5](Lauf_005.md) | 100 | Massenaussterben | 93 | 0,00 |
| [4](Lauf_004.md) | 100 | Massenaussterben | 85 | 0,00 |
| [3](Lauf_003.md) | 100 | Massenaussterben | 82 | 0,00 |
| [2](Lauf_002.md) | 100 | Massenaussterben | 20 | 0,00 |
| [1](Lauf_001.md) | 100 | Massenaussterben | 1 | 0,00 |

## Aktualisieren

```bash
python3 04_Prototypen/v0.1/run_stats.py
```

Ein regulärer neuer Lauf aktualisiert seinen Bericht und diese Übersicht automatisch. Veröffentlicht wird der neue Stand mit dem nächsten Git-Commit und Push.
