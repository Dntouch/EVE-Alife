# P0 – Ergebnis und Abschluss

Stand: 20. September 2026

## Ziel

P0 sollte nicht bereits interessantes Leben erzeugen. Es sollte zeigen, dass die beschlossene Maschine ausführbar, reproduzierbar und beobachtbar ist: Genomnetze, kurz- und langfristiger Zustand, Energie, gemeinsame RAM-Suppe, Membran, Reproduktion, Vererbung, Mutation, Ereignisse, Snapshots und Checkpoints.

Dieses Ziel wurde erreicht. Sechs ursprüngliche Kerntests und ein ergänzter Test der Beobachtungsschnittstelle laufen deterministisch. Die Lupe bleibt eine getrennte, ausschließlich lesende Schicht.

## Kontrollierter Vergleich

Für den abschließenden Vergleich blieben Seed `42`, 20 Startentitäten, die ursprünglichen P0-Demogenome und die zufällig initialisierte RAM-Suppe unverändert. Nur die Startenergie wurde verändert.

| Messgröße | Startenergie 100 | Startenergie 500 |
|---|---:|---:|
| Startentitäten | 20 | 20 |
| Nachkommen | 20 | 93 |
| Entitäten insgesamt | 40 | 113 |
| Signale | 1.662 | 7.835 |
| Schreibvorgänge nach Z | 82 | 397 |
| Letzte Geburt | Tick 4 | Tick 19 |
| Letzter Tod | Tick 9 | Tick 24 |

Referenzläufe:

- Energie 100: `3074f571-dcd4-43ce-ae05-4e931ee13895`
- Energie 500: `ad446878-ac8a-4a8e-98e2-23c0638ddb2a`

Die Run-Verzeichnisse sind lokale Versuchsdaten und werden nicht in Git versioniert.

## Beobachtung

Die höhere Energie erzeugte mehr Ausführungen, Geburten und Z-Schreibvorgänge und verschob das Aussterben nach hinten. Sie erzeugte jedoch kein qualitativ anderes Verhalten. Im energiereicheren Lauf gingen alle 397 Z-Schreibvorgänge weiterhin an dieselbe Z-Adresse. Die Entitäten wiederholten im Wesentlichen den fest verdrahteten technischen Demonstrationsablauf.

## Interpretation

P0 weist nach, dass die technische Physik arbeitet. P0 weist nicht nach, dass die Population ihre Umwelt erkundet, auf Funde reagiert, lernt oder sich erfolgreich anpasst. Mehr Startenergie verstärkt und verlängert das vorhandene Verhalten, ersetzt aber keine dafür geeignete genomische Struktur.

Das Aussterben ist deshalb weder ein Defekt noch ein biologisches Ergebnis. Population 0 war eine Prüfvorrichtung für Datenfluss und Geburt, keine tragfähige Ausgangspopulation.

## Konsequenz für P1

P1 verändert zunächst nicht die Umwelt. Die zufällige RAM-Suppe bleibt bestehen. Stattdessen erhält die Startpopulation Genome, die einen Suchstand dauerhaft halten, RAM-Adressen nacheinander erreichen, gelesene Inhalte speichern und datenabhängige Pfade aktivieren können. Damit wird erstmals prüfbar, ob beobachtbare Umweltinteraktion statt bloßer Wiederholung entsteht.

