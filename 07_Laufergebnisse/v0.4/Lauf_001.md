# v0.4 – Lauf 001: Der Populationsdurchbruch endet im Arbeitsspeicher

## Identität

- Run-ID: `0ccf273f-6bc6-4a91-a42c-7bca96f9d70b`
- Label: `v0.4 Homologe Genomplätze · Seed 42 · 5000 Ticks`
- Seed: `42`
- Startpopulation: `20`
- Tick-Limit: `5000`
- Alterskosten: `0,005`
- Genommodell: drei homologe, größenfreie Vererbungsplätze
- RAM-Welt: `toys`
- Messintervall: `10`
- Checkpointintervall: `10000`

## Ergebnisstatus

Der Lauf endete **nicht fachlich**, sondern wurde am 24. September 2026 um
02:45:40 Uhr vom Linux-OOM-Killer beendet. Manifest und Datenbank tragen deshalb
weiter den letzten publizierten Status `running`. Die folgenden Zahlen bezeichnen
den letzten konsistent lesbaren Zustand und kein reguläres Laufende.

| Kennzahl | Letzter Stand |
|---|---:|
| Tick | 4.034 |
| Amöben insgesamt | 9.446 |
| lebend | 8.761 |
| verstorben | 685 |
| Nachkommen | 9.426 |
| tiefste Generation | 38 |
| Gründer noch lebend | 1 von 20 |
| gespeicherte Ereignisse | 1.696.250 |
| unterschiedliche Genomfingerabdrücke | 8.823 |
| Genomgröße | durchgehend 198 G = 76 F + 122 P |

Die Frage, ob bis Tick 5.000 mehr als 20.000 Amöben entstanden wären, ist damit
**nicht beantwortet**. Bis Tick 4.034 waren es 9.446. Die Population wuchs zu
diesem Zeitpunkt weiterhin stark: von 6.712 lebenden Amöben bei Tick 3.940 auf
8.653 bei Tick 4.030 und 8.761 im letzten Live-Zustand.

## Biologische Beobachtung

Das homologe Platzmodell beseitigte den zuvor beobachteten systematischen
Genomverlust. Sämtliche registrierten Genome behielten 198 Genomteile. Zugleich
entstanden 8.823 verschiedene Fingerabdrücke; konstante Größe bedeutete also
nicht genetische Identität.

Nur neun der 9.426 Geburten trugen eine protokollierte Einzelmutation:

- vier Änderungen von `bond_ticks`,
- je eine Kanten-, Kantengewichts-, Knoten- und `knock_capacity`-Mutation,
- eine Platzteilung.

Die große Vielfalt entstand daher überwiegend aus Rekombination. Der Lauf
erreichte Generation 38 und zeigte erstmals eine über viele Generationen
tragfähige, stark wachsende Population. 26.620 Fortpflanzungsversuche wurden
abgelehnt, 18.853 Fortpflanzungskosten gebucht und 436 Leichen verwertet.

## Technische Todesursache

Das Kernelprotokoll weist den getöteten `python3`-Prozess eindeutig aus:

- etwa 52,35 GB anonymer physischer Speicher,
- etwa 8,5 GB ausgelagerter Speicher,
- 55,3 GB gemeldeter Spitzenverbrauch der zugehörigen Anwendungseinheit.

Die Simulation hielt ihre seit Laufbeginn erzeugte Ereignisliste zusätzlich zur
SQLite-Persistenz vollständig im Python-Speicher. Gleichzeitig wurde nach jedem
Tick ein immer größeres vollständiges Live-Bild geschrieben. Das letzte
`live.json` war 405 MB groß; `run.sqlite3` erreichte 1,3 GB. Beim Aufbau des
Live-Bildes entstanden weitere große temporäre Objektgraphen.

Da das erste reguläre Recovery-Checkpoint erst für Tick 10.000 vorgesehen war,
existiert kein vollständiger Zustand mit RAM, Zufallszustand und internen
Amöbenspeichern. Eine exakte deterministische Fortsetzung ist daher unmöglich.
Die Datenbank und das letzte Live-Bild bleiben als abgebrochene Beobachtung
erhalten.

## Konsequenz

Die Simulation wurde fachlich nicht verändert. Der Datenpfad wurde anschließend
so umgebaut, dass Ereignisse nach ihrer Persistenz freigegeben, Live-Bilder auf
zwei Aktualisierungen pro Sekunde begrenzt, Live- und Analysedaten getrennt,
Statusschreibvorgänge gebündelt und Genome nur bei neuen Entitäten registriert
werden. Ein reproduzierbarer Benchmark liegt dem v0.4-Prototyp bei.

