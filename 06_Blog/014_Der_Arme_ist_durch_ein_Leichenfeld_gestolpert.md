# Der Arme ist ja durch ein Leichenfeld gestolpert

Status: Gesprächsentwurf

Redaktionelle Einordnung: Dieser Beitrag verarbeitet Beobachtungen und
Designentscheidungen aus EVE-Alife Prototyp v0.3 vom 23. September 2026. Die
Deutung der Populationskurve und möglicher Umweltwirkungen ist ausdrücklich
noch keine gesicherte Erklärung.

*Wir wollten die Lupe fertig machen. Dann fanden wir eine letzte Überlebende,
zwei Stumpfbirnen und eine Amöbe, die offenbar durch einen Friedhof gelaufen
war. Ein normaler Nachmittag im Biotop-Eimer.*

![Die überarbeitete Chronik des Biotops](../04_Prototypen/v0.3/screenshots/03-chronik.png)

## Zweimal dasselbe Ende

Wir ließen 25 Amöben mit Seed 42 auf 5.000 Ticks los. Danach wiederholten wir
den Lauf mit denselben Parametern.

Sie waren identisch.

Das ist gleichzeitig spannend und langweilig. Langweilig, weil der zweite Film
keine Überraschung bereithielt. Spannend, weil Determinismus in einem System
voller Rekombination, Mutation und zufällig wirkender Entscheidungen keine
Selbstverständlichkeit ist. Derselbe Seed bedeutete hier tatsächlich dieselbe
Geschichte.

Am Ende lebte Clara 4. Ihr Genom war klein – auffällig klein. Ein großer Teil
des elterlichen Materials war bereits bei ihrer Geburt nicht übernommen worden.
Das erinnerte an Ada: keine große Genomkathedrale, sondern eine Handvoll
Bausteine, die lange genug funktionierten.

**Beobachtung:** Im Lauf waren schrumpfende Genome deutlich häufiger als
wachsende.

**Offen:** Ob das ein Vorteil des kleinen Genoms, ein Mutationsbias, ein Effekt
der Kosten oder lediglich die konkrete Abstammungsgeschichte war, ist damit
nicht entschieden.

## Fällt die Population – oder holt sie nur Luft?

Die Populationskurve sank, stieg wieder und wurde später erneut rückläufig.
Sofort lag die Frage auf dem Tisch, ob unsere Alterskosten zu aggressiv sind.

Die ehrliche Antwort lautete: vielleicht. Ein 5.000-Tick-Lauf kann zeigen, dass
etwas geschieht. Er kann noch nicht zeigen, ob sich lediglich der Zeitpunkt
eines Kollapses verschiebt.

Also verdoppelten wir die Laufzeit auf 10.000 Ticks. Nicht um eine schönere
Kurve zu bekommen, sondern um der unbequemen Möglichkeit Raum zu geben, dass
wir bisher nur die erste Hälfte derselben Geschichte gesehen hatten.

Diese Auswertung ist der nächste Arbeitsblock. Erst danach wird an
Alterskosten oder Umweltbedingungen gedreht.

## Ada 3 und Olga 5 sind Stumpfbirnen

**Stefan:** Im aktuellen Lauf sind Ada 3 und Olga 5 zwei Stumpfbirnen.

Die wissenschaftliche Definition folgte umgehend:

**Stefan:** Keine Fortpflanzung. Sie sind steril.

Die Lupe sollte das anzeigen. Der erste Versuch war lehrreich: Plötzlich waren
laut Oberfläche beinahe alle lebenden Amöben steril, während direkt daneben
Geburten stattfanden. Die Anzeige hatte das Fehlen eines einzelnen Bausteins zu
einer biologischen Diagnose aufgeblasen.

Wir machten sie vorsichtiger. Die Lupe darf aus dem tatsächlich verdrahteten
Genom einen operativen Hinweis ableiten. Sie darf aber nicht so tun, als kenne
sie damit jede mögliche Ursache ausbleibender Fortpflanzung.

## Nils 6 und das Leichenfeld

Dann öffneten wir die prägenden Ereignisse von Nils 6, Nummer 176.

**Stefan:** Der Arme ist ja durch ein Leichenfeld gestolpert.

Tote Amöben blieben bislang physisch in der RAM-Suppe. Das war für die
Beobachtung praktisch, aber als Umweltregel merkwürdig: Eine Leiche konnte immer
wieder gefunden werden, während ihre historische Existenz und ihr physischer
Körper wie dieselbe Sache behandelt wurden.

Die neue Regel trennt beides. Stirbt eine Amöbe, bleibt ihre gesamte Geschichte
in Historie, Stammbaum und Genomanalyse erhalten. In der Suppe liegt jedoch nur
noch eine verwertbare Leiche. Wer sie zuerst passend liest, erhält exakt die
noch vorhandene Energie – seien es 200 Einheiten oder nur zwei. Danach ist die
Leiche aus der Suppe verschwunden.

Keine Leichenflatrate. Keine erfundene Mindestbelohnung. Kein Verlust der
wissenschaftlichen Akte.

## Und dann blinkte die DNA

Zum Schluss ging es wieder um die Lupe selbst. Die Chronik bekam verständliche
Run-Karten statt rätselhafter Kreise. Der Stammbaum hob direkte Kinder ebenso
klar hervor wie direkte Eltern. Das Wallpaper wurde heller.

Und im DNA-Netz des Hintergrunds feuern jetzt gelegentlich kleine Lichtpunkte.
Erst waren es immer dieselben zwei. Das sah weniger nach neuronaler Aktivität
aus als nach zwei Kollegen, die sich zuverlässig gegenseitig anblinken.

Jetzt besitzen neun Punkte eigene Rhythmen, Pausen und Farben.

**Stefan:** Das ist gut. :-)

Damit ist die Lupe für v0.3 rund. Nicht fertig für alle Zeiten – nur fertig
genug, dass wir wieder durch sie hindurch auf das Biotop sehen können, statt
ständig an ihrem Rahmen zu schrauben.

Als Nächstes kommt v0.4. Dort warten evolvierbare Kantengewichte. Und vorher
muss der 10.000-Tick-Lauf erzählen, ob wir die Umwelt ändern sollten oder nur
ungeduldig geworden sind.

---

Interne Quellen: EVE-Alife-Projektgespräch, v0.3-Run-Daten und Implementierung
vom 23. September 2026. Vor Veröffentlichung folgen Schlussredaktion,
Faktenprüfung und Datenschutzprüfung.
