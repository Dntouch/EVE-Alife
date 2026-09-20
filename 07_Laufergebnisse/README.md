# EVE-Alife – Laufergebnisse

Dieser Bereich enthält die kompakten, versionierten Berichte der tatsächlich ausgeführten Prototyp-Läufe. Jeder Bericht hält Identität, Git-Stand, Konfiguration, Populationsresultat, Energiegewinn und Lebensrekorde fest.

Die vollständigen Rohdaten bleiben lokal unter `04_Prototypen/v0.1/runs/`: Ein einzelner Lauf kann hunderte Megabyte an Snapshots, RAM-Zuständen, Checkpoints und Ereignissen enthalten. Sie werden deshalb nicht ungeprüft in Git aufgenommen. Die Berichte hier sind aus diesen Rohdaten reproduzierbar.

Zusammenhängende Versuchsreihen werden zusätzlich ausgewertet:

- [Tarifrunde 40–90: IG Amöbe gegen Lebenshaltungskosten](Tarifrunde_040_bis_090.md)
- [Langzeitlauf mit Tarif 60](Langzeitlauf_Tarif_060.md)
- [Dynamische Partnersuche und Alterskosten](Partnersuche_und_Alterung.md)

## Übersicht

| Lauf | Ticks | Status | Nachkommen | Energiegewinn |
| ---: | ---: | :--- | ---: | ---: |
| [32](Lauf_032_b623e0f1.md) | 1000 | 32 lebend | 51 | 1.232.700,00 |
| [31](Lauf_031_c61fd90c.md) | 300 | 52 lebend | 38 | 289.080,00 |
| [30](Lauf_030_8f28241b.md) | 1000 | 179 lebend | 230 | 3.078.540,00 |
| [29](Lauf_029_17abde73.md) | 200 | 146 lebend | 180 | 687.330,00 |
| [28](Lauf_028_3a3366dc.md) | 200 | 142 lebend | 155 | 633.335,00 |
| [27](Lauf_027_7fda6f10.md) | 200 | 128 lebend | 141 | 564.800,00 |
| [26](Lauf_026_a919c655.md) | 200 | 116 lebend | 123 | 456.075,00 |
| [25](Lauf_025_24d981c0.md) | 200 | 82 lebend | 83 | 325.570,00 |
| [24](Lauf_024_a647f0d3.md) | 200 | 78 lebend | 81 | 268.775,00 |
| [23](Lauf_023_6518e4f4.md) | 200 | 59 lebend | 49 | 203.580,00 |
| [22](Lauf_022_f01a4e07.md) | 200 | 50 lebend | 36 | 170.060,00 |
| [21](Lauf_021_c9aea05d.md) | 200 | 29 lebend | 9 | 110.450,00 |
| [20](Lauf_020_c82035b5.md) | 200 | 18 lebend | 0 | 78.345,00 |
| [19](Lauf_019_679e5e69.md) | 200 | 5 lebend | 0 | 56.520,00 |
| [18](Lauf_018_491d086f.md) | 200 | 324 lebend | 399 | 2.720.160,00 |
| [17](Lauf_017_1cb45901.md) | 200 | 128 lebend | 141 | 564.800,00 |
| [16](Lauf_016_a37a384c.md) | 200 | Massenaussterben | 0 | 2.700,00 |
| [15](Lauf_015_d992ad6c.md) | 200 | 5 lebend | 0 | 56.520,00 |
| [14](Lauf_014_5a980744.md) | 200 | Massenaussterben | 0 | 7.640,00 |
| [13](Lauf_013_1830d15a.md) | 100 | Massenaussterben | 0 | 2.700,00 |
| [12](Lauf_012_36776956.md) | 100 | Massenaussterben | 0 | 0,00 |
| [11](Lauf_011_6b34f4dd.md) | 100 | Massenaussterben | 21 | 0,00 |
| [10](Lauf_010_ef3637b0.md) | 100 | Massenaussterben | 57 | 0,00 |
| [9](Lauf_009_9a0f25fc.md) | 100 | Massenaussterben | 10 | 0,00 |
| [8](Lauf_008_d89c01b8.md) | 30 | Massenaussterben | 91 | 0,00 |
| [7](Lauf_007_d9824a2e.md) | 30 | Massenaussterben | 93 | 0,00 |
| [6](Lauf_006_41e5600c.md) | 30 | Massenaussterben | 93 | 0,00 |
| [5](Lauf_005_ad446878.md) | 100 | Massenaussterben | 93 | 0,00 |
| [4](Lauf_004_82e5f305.md) | 100 | Massenaussterben | 85 | 0,00 |
| [3](Lauf_003_13a21897.md) | 100 | Massenaussterben | 82 | 0,00 |
| [2](Lauf_002_3074f571.md) | 100 | Massenaussterben | 20 | 0,00 |
| [1](Lauf_001_1955ab29.md) | 100 | Massenaussterben | 1 | 0,00 |

## Aktualisieren

```bash
python3 04_Prototypen/v0.1/run_stats.py
```

Ein regulärer neuer Lauf aktualisiert seinen Bericht und diese Übersicht automatisch. Veröffentlicht wird der neue Stand mit dem nächsten Git-Commit und Push.
