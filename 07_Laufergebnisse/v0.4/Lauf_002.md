# v0.4 – Lauf 002: Bis zum letzten Tick

## Identität

- Run-ID: `f7625e0e-9bf2-4457-bd00-b438282b80b8`
- Label: `v0.4 Homologe Genomplätze · Seed 42 · 5000 Ticks · Wiederholung`
- Seed: `42`
- Startpopulation: `20`
- Tick-Limit: `5000`
- Alterskosten: `0,005`
- Genommodell: homologe, größenfreie Vererbungsplätze
- RAM-Welt: `toys`
- Messintervall: `10`
- Checkpointintervall: `10000`
- Git-Commit: `95bba0ad34b0b710b0cf3e4647b6039288f4feb4`
- Laufzeit: 24. September 2026, 15:14:34 bis 17:36:38 UTC

## Ergebnis

Der Lauf erreichte Tick 5.000 regulär. Damit bestand der nach Lauf 001
revidierte Beobachtungspfad erstmals einen vollständigen großen v0.4-Lauf.

| Kennzahl | Endstand |
| --- | ---: |
| Tick | 5.000 |
| Amöben insgesamt | 31.082 |
| lebend | 28.264 |
| verstorben | 2.818 |
| Nachkommen | 31.062 |
| tiefste Generation | 45 |
| Gründer noch lebend | 0 von 20 |
| unterschiedliche Genomfingerabdrücke | 29.842 |
| gespeicherte Ereignisse | 5.901.539 |
| Run-Verzeichnis | 4,3 GB |

Die Population wuchs bis zum letzten Messpunkt weiter. Noch in Tick 5.000
wurden Kinder geboren. Der Endstand ist zugleich das gemessene
Populationsmaximum. Die nach Lauf 001 offene Frage ist damit beantwortet: Die
Population überschritt 20.000 Lebende bereits in Tick 4.870 und erreichte bis
Tick 5.000 deutlich mehr als 20.000.

122.082 Fortpflanzungsversuche wurden abgelehnt, 62.126
Fortpflanzungskosten gebucht und 1.848 Leichen verwertet. Die einzige Amöbe der
tiefsten Generation 45 war `Cejara 45` (#28676), geboren in Tick 4.968 und am
Laufende lebend.

## Abweichung von Lauf 001

Seed und sichtbare Fachparameter entsprechen Lauf 001, die Verläufe sind jedoch
nicht identisch. Bis Tick 1.230 stimmen die gemessenen Populationen exakt
überein; in Tick 1.240 erscheint die erste Abweichung. Danach verstärkt sie sich:

| Tick | Lauf 001 | Lauf 002 |
| ---: | ---: | ---: |
| 2.000 | 103 | 94 |
| 3.000 | 534 | 332 |
| 4.000 | 7.956 | 2.547 |

Lauf 001 endete in Tick 4.034 mit 8.761 Lebenden. Lauf 002 überschritt diesen
Wert erst in Tick 4.540 und wuchs anschließend bis 28.264.

Gleicher Seed garantiert Reproduktion nur mit exakt demselben ausführbaren
Arbeitsstand. Das Manifest von Lauf 001 nennt Commit `95988a8`, Lauf 002 Commit
`95bba0a`; außerdem kann das Manifest einen seinerzeit nicht committen
Arbeitsbaum nicht abbilden. Ob der erste Unterschied lediglich aus dieser
Versionsgrenze oder aus einer unbeabsichtigten semantischen Wirkung der
Performance-Revision stammt, ist offen. Der Ereignisverlauf um Tick 1.240 muss
vor einer Behauptung semantikneutraler Reproduktion gesondert verglichen werden.

## Genome und Mutationen

Alle 29.842 unterschiedlichen Genome behielten dieselbe Größe:

- 76 Funktionspunkte,
- 122 Kanten,
- 198 Genomteile insgesamt.

Die Vielfalt entstand fast vollständig durch Rekombination. Unter 31.062
Kindgenomen wurden nur 29 protokollierte Einzelmutationen gefunden:

| Mutationsklasse | Anzahl |
| --- | ---: |
| Aktivität | 5 |
| Knoten | 5 |
| `bond_ticks` | 5 |
| `knock_capacity` | 5 |
| Kante | 4 |
| Kantengewicht | 4 |
| Slotverschmelzung | 1 |

Die vier Gewichtsmutationen erzeugten ausschließlich kleine negative Werte von
`-1` oder `-2`. Über alle einzigartigen Genome fanden sich sieben nichtneutrale
Kanten, weil mutierte Kanten weitervererbt wurden.

### Die Zwei-Slot-Dynastie

Kein Genom besaß mehr als drei Slots. 29.830 Genome hatten drei Slots, zwölf
unterschiedliche Genome zwei Slots. Die Abweichung geht vollständig auf eine
einzige Mutation zurück: In Tick 4.502 verschmolzen bei `Dadra 37` (#9197) Slot
2 und Slot 1. Dabei wechselten 42 Knoten den Slot; Anzahl und Inhalt der Knoten
und Kanten blieben unverändert.

Die neue Architektur wurde weitervererbt. Am Laufende lebten 13 Amöben mit zwei
Slots und zwölf verschiedenen Genomfingerabdrücken; keine von ihnen war bis
dahin verstorben. Zur Linie gehörten unter anderem `Orora 38`, `Cebela 39`,
`Damera 40`, `Arwen 41` und `Ceciel 42`.

Es trat weder eine Slotteilung noch eine Slotduplikation oder Slotlöschung auf.
Das ist bei der geringen Mutationsrate kein Hinweis auf eine Bevorzugung der
Verschmelzung: Pro Geburt beträgt die Chance für jede der vier strukturellen
Klassen ungefähr `0,001 × 0,10 × 0,25 = 0,000025`, also eins zu 40.000. Bei
31.062 Geburten liegt der Erwartungswert je Klasse unter eins.

## Technische Beobachtungen

Der Simulationsprozess überstand die wachsende Population ohne erneuten
Speicherkollaps. Persistierte Ereignisse blieben auf der Platte, statt sich wie
in Lauf 001 vollständig im Python-Prozess anzusammeln. Der Preis des
Populationsdurchbruchs war nun CPU-Zeit: Mit mehr als 20.000 Lebenden benötigten
zehn Ticks mehrere Minuten. Der serielle Fachkern ist damit der nächste klare
Skalierungsengpass. Eine Mehrkernarchitektur muss gemeinsame Wirkungen
deterministisch ordnen; als Arbeitsrichtung bietet sich eine zweiphasige
Ausführung aus paralleler Berechnung und geordnetem Commit an.

Die Lupe zeigte eine zweite Skalierungsgrenze. Der unbeschränkte Gesamtstammbaum
und parallel geladene Ereignismengen ließen einen Chromium-Renderer auf 8,4 GB
RAM anwachsen. Der Lupe-Server wurde während des Laufs gestoppt. Erforderlich
sind serverseitig begrenzte Verwandtschaftsausschnitte, Pagination und eine
aggregierte Gesamtansicht statt eines vollständigen Knoten-Kanten-Graphs.

## Aussagegrenze und nächste Schritte

Der Lauf belegt einen vollständigen Populationsdurchbruch dieses konkreten
Arbeitsstands, nicht allgemein die Stabilität des Modells. Die Population war
am Ticklimit noch stark wachsend; ein Gleichgewicht wurde nicht beobachtet.

Als nächste getrennte Arbeiten folgen:

1. Ereignisvergleich ab Tick 1.240 zur Klärung der Reproduktionsgrenze.
2. Deterministische Mehrkernarchitektur für den Fachkern.
3. Begrenzter Vor- und Nachfahrenfokus mit harter Knotenobergrenze.
4. Aggregierte, zoombare Gesamtansicht und paginierte Lupe-APIs.
5. Kontrollierte Strukturmutationsläufe, bevor der Zwei-Slot-Linie ein
   Selektionsvorteil zugeschrieben wird.
