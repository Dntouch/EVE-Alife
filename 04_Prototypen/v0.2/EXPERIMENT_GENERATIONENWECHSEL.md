# Experiment: Habitate, Elternfinanzierung und Generationenwechsel

Stand: 21. September 2026

## Fragestellung

Kann die v0.2-Population nach dem Tod ihrer Gründer eine selbsttragende Kultur bilden, wenn veränderliche RAM-Objekte flächendeckend erreichbar sind und eine Geburt aus dem gemeinsamen Energieüberschuss aller Eltern finanziert werden darf?

## Änderungen des Versuchsstands

1. Der RAM wurde in 128 Habitate gegliedert. Jedes Habitat enthält einen Stein, zwei Blasen und einen Schalter.
2. Gründer und Kinder erhalten räumliche RAM-Positionen; Kinder entstehen in der Nähe eines Elternteils.
3. Die Live-Lupe stellt Amöben, Spielzeuge und Aktivitäten in einer breiten ovalen RAM-Ansicht dar. Legendenfilter, Mouseover-Fokus, Klicknavigation und die Kopplung an den Zeitregler erlauben eine visuelle Beobachtung ohne Eingriff in den Lauf.
4. Die Geburtsenergie wird aus dem gemeinsamen Überschuss der Eltern über ihrem jeweiligen `S₀` bezahlt. Ein wohlhabender Elternteil kann fehlende Beiträge anderer Eltern bis hin zur vollständigen Geburtsenergie übernehmen.

## Vergleich

| Lauf | Seed | Finanzierungsregel | Endtick | Nachkommen | tiefste Generation | letzte Geburt | Ergebnis |
| ---: | ---: | :--- | ---: | ---: | ---: | ---: | :--- |
| 14 | 43 | gleicher Einzelbeitrag | 2.256 | 38 | 5 | 1.385 | ausgestorben |
| 15 | 42 | gleicher Einzelbeitrag | 2.122 | 36 | 6 | 1.140 | ausgestorben |
| 16 | 42 | gemeinsamer Überschuss | 5.000 | 75 | 8 | 2.085 | eine unfruchtbare Überlebende |

## Beobachtungen

- Die Habitate liefern genügend Information, damit einzelne Amöben sehr große Energiereserven aufbauen können.
- Die gemeinsame Finanzierung beseitigt den Fehler, dass ein energiearmer Elternteil eine insgesamt finanzierbare Geburt blockiert.
- Lauf 16 trug die Nachkommenpopulation deutlich weiter als Lauf 15, erreichte aber keine positive langfristige Nettoreproduktion.
- Die letzte Überlebende Ada 4 besaß mehr als 101.000 Energie, aber kein ausführbares `MEM_WRITE`.
- Adas Genom war von Größe 198 bei den Gründern auf Größe 30 reduziert. Der absolute Kostenvorteil des kleineren Genoms war mit rund 0,319 Energie pro Tick klein gegenüber ihren Alterskosten und Energiegewinnen.

## Schlussfolgerung

Die Energieversorgung ist unter diesen Bedingungen nicht mehr der vorrangige Engpass. Auch die gemeinsame Elternfinanzierung ist fachlich tragfähig und verbessert das Resultat. Der nächste zu prüfende Engpass ist der strukturelle Verlust des Partnersuch- und Fortpflanzungsfragments bei Rekombination und Mutation.

Noch nicht belegt ist, ob dieser Verlust überwiegend durch direkten Kostendruck, neutrale Fragmentverteilung, fehlende Kopplung zwischen Energieernte und Fortpflanzungsfähigkeit oder deren Zusammenspiel entsteht. Vor einer weiteren Änderung des Genomtarifs soll deshalb die Häufigkeit des Fragmentverlusts je Generation ausgewertet werden.

