# EVE-Alife – Laufergebnisse v0.2

Diese Chronik umfasst ausschließlich Runs des Prototyps `v0.2` und beginnt deshalb wieder mit Lauf 1. Sortiert wird nach dem gespeicherten Erzeugungszeitpunkt, nicht nach der UUID des Run-Verzeichnisses.

| Lauf | Ticks | Am Ende lebend | Nachkommen | ohne `MEM_WRITE` | RAM-Energie | Einordnung |
| ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| [16](Lauf_016.md) | 5000 | 1 | 75 | 1 | 952.613,33 | gemeinsame Elternfinanzierung; Ada 4 erreicht allein das Ticklimit |
| [15](Lauf_015.md) | 2122 | ausgestorben | 36 | 0 | 570.868,33 | 128 Habitate, Seed 42, alte Einzelbeitragsregel |
| [14](Lauf_014.md) | 2256 | ausgestorben | 38 | 0 | 446.340 | erster Lauf mit 128 Habitaten, Seed 43 |
| [13](Lauf_013.md) | 3357 | ausgestorben | 38 | 0 | 473.156,67 | zweiter dünner Stabilitätstest, Seed 43 |
| [12](Lauf_012.md) | 2042 | ausgestorben | 36 | 0 | 543.120 | 5.000-Tick-Stabilitätstest; natürliche Extinktion |
| [11](Lauf_011.md) | 500 | 78 | 29 | 0 | 186.720 | lokale RAM-Koordinaten und räumliche Geburt |
| [10](Lauf_010.md) | 500 | 79 | 31 | 0 | 177.350 | erreichbarer Spielzeugkasten in drei RAM-Zonen |
| [9](Lauf_009.md) | 500 | 83 | 34 | 0 | 176.570 | erster Spielzeug-Smoke-Run; Objekte nicht erreicht |
| [8](Lauf_008.md) | 2000 | 4 | 43 | 0 | 548.355 | variable Mehrfachklingel und Bindungszeit |
| [7](Lauf_007.md) | 2000 | 30 | 134 | 0 | 1.042.111,67 | erster Vergleich mit experimenteller Klingel |
| [6](Lauf_006.md) | 2704 | ausgestorben | 22 | 0 | 877.596,67 | 50 Gründer; natürliches Ende vor Limit 5.000 |
| [5](Lauf_005.md) | 2000 | 11 | 7 | 0 | 401.840 | 2.000 Ticks mit G-Tarif 0,05/0,01 |
| [4](Lauf_004.md) | 500 | 27 | 7 | 0 | 90.825 | reduzierter G-Tarif 0,05/0,01 |
| [3](Lauf_003.md) | 200 | 15 | 0 | 0 | 20.370 | uniforme Suchparameter, Kontrolllauf |
| [2](Lauf_002.md) | 200 | 19 | 0 | 0 | 26.910 | variable Suchparameter und Rückzug |
| [1](Lauf_001.md) | 200 | 26 | 6 | 5 | 43.235 | frühe v0.2-Referenz vor Suchvariation |

Die ersten drei Läufe verwenden noch den historischen Genomkostentarif `0,5/0,1`. Ab Lauf 4 gilt der experimentelle v0.2-Tarif `0,05/0,01`. Dadurch sind die Ergebnisse nicht als reine Wiederholungen, sondern als dokumentierte Modellstände innerhalb des Prototyps zu lesen.

Läufe 14 und 15 führen die flächendeckende Umwelt mit 128 Spielzeughabitaten ein. Lauf 16 verwendet erstmals die gemeinsame Elternfinanzierung: Fehlende Beiträge eines Elternteils können aus dem Überschuss der übrigen Eltern übernommen werden, ohne deren jeweiliges `S₀` zu unterschreiten. Der Vergleich ist in [Experiment Generationenwechsel](../../04_Prototypen/v0.2/EXPERIMENT_GENERATIONENWECHSEL.md) zusammengefasst.

[Zur versionsübergreifenden Übersicht](../README.md)
