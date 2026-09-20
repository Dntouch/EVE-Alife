# EVE-Alife – Laufergebnisse

Dieser Bereich enthält die kompakten, versionierten Berichte der tatsächlich ausgeführten Prototyp-Läufe. Jeder Bericht hält Identität, Git-Stand, Konfiguration, Populationsresultat, Energiegewinn und Lebensrekorde fest.

Die vollständigen Rohdaten bleiben lokal unter `04_Prototypen/v0.1/runs/`: Ein einzelner Lauf kann hunderte Megabyte an Snapshots, RAM-Zuständen, Checkpoints und Ereignissen enthalten. Sie werden deshalb nicht ungeprüft in Git aufgenommen. Die Berichte hier sind aus diesen Rohdaten reproduzierbar.

## Übersicht

| Lauf | Ticks | Status | Nachkommen | Energiegewinn |
| ---: | ---: | :--- | ---: | ---: |
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
