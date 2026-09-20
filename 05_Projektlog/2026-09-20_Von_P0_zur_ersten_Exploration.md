# 20. September 2026: Von P0 zur ersten genomischen Exploration

## Ausgangslage

Nach dem ersten lauffähigen Prototyp wurde Population 0 vergrößert. Ziel war zunächst nicht, neue Umweltbedingungen einzuführen, sondern zu prüfen, ob mehr Entitäten oder mehr Energie das beobachtete Verhalten qualitativ verändern.

Ein zwischenzeitlicher technischer Explorationsversuch verwendete präparierte RAM-Inseln und ein besonderes Zählergenom. Dieser Aufbau war als Datenpfadtest nützlich, vermischte aber Genom- und Umweltänderungen. Für den kontrollierten Vergleich wurden die Umweltänderungen deshalb wieder entfernt.

## P0: Mehr Energie, gleiches Verhalten

Zwei Läufe verwendeten Seed `42`, 20 Startentitäten, dieselbe zufällige RAM-Suppe und dieselben P0-Demogenome. Nur die Startenergie unterschied sich.

| Messgröße | Energie 100 | Energie 500 |
|---|---:|---:|
| Nachkommen | 20 | 93 |
| Entitäten insgesamt | 40 | 113 |
| Signale | 1.662 | 7.835 |
| Z-Schreibvorgänge | 82 | 397 |
| letzte Geburt | Tick 4 | Tick 19 |
| letzter Tod | Tick 9 | Tick 24 |

Die energiereichere Population arbeitete länger und erzeugte mehr Nachkommen. Alle 397 Z-Schreibvorgänge trafen dennoch dieselbe Adresse. Die zusätzliche Energie vervielfachte den fest verdrahteten Ablauf, erzeugte aber keine Umweltuntersuchung.

P0 wurde damit als technischer Machbarkeitsnachweis abgeschlossen. Nachgewiesen waren Datenfluss, Speicher, Energie, Membran, Geburt, fragmentbasierte Vererbung, Mutation, Persistenz und Reproduzierbarkeit. Nicht nachgewiesen waren Exploration, Lernen, Anpassung oder tragfähige Populationsdynamik.

Die ausführliche Abgrenzung steht in `04_Prototypen/P0_ERGEBNISSE.md`.

## Die Lupe wird verständlicher

Die erste Lupe zeigte Zustandszähler und Z-Inhalte, setzte aber voraus, dass Betrachter die Kürzel und ihre Beziehungen bereits kannten. Die Beobachtungsschicht wurde deshalb erweitert, ohne eine Rückwirkung auf den Experimentkern einzuführen.

Neu sichtbar sind:

- Erklärungen und Tooltips für `G`, `P`, `K`, `Z`, `S` und RAM,
- konkrete Funktionspunkt-Instanzen und ihre erblichen Konstanten,
- sämtliche gerichteten P-Kanten,
- belegte K-Ports mit Wert und Provenienz,
- alle Z-Zellen mit Wert und Provenienz,
- eine aus historischen Snapshots berechnete Populationskurve,
- historische Zustände pro Tick,
- ein steuerbarer Lebensfilm für jede Entität.

Der Lebensfilm verwendet ausschließlich gespeicherte Snapshots und Events. Abspielen, Pause, Geschwindigkeit und Einzelschritte verändern keinen Zustand. Zusätzliche passive Ereignisse dokumentieren Standbykosten, Funktionsausführungen, RAM-Lesezugriffe und Reproduktionsbeiträge. Damit lässt sich nicht nur sehen, wie eine Entität zu einem Tick aussieht, sondern auch, was seit dem vorherigen Bild geschah.

## P1: Exploration liegt im Genom

Population 1 arbeitet wieder mit der unveränderten zufälligen RAM-Suppe. Ihre neue Fähigkeit stammt aus einem konkreten Genomfragment:

```text
Z[0] lesen
  -> 1 addieren
  -> neuen Suchstand nach Z[0] schreiben
  -> denselben Wert als RAM-Adresse lesen
  -> Fund nach Z[1] schreiben
  -> Nichtnull-Fund durch GATE nach Z[2] weiterleiten
```

Der dafür ergänzte primitive Funktionspunkt `GATE(value, condition)` sendet `value` nur dann weiter, wenn `condition` ungleich null ist. Er interpretiert keine Bedeutung und trifft keine Wahl für die Entität. Er ermöglicht lediglich erstmals, dass ein Datenwert den weiteren Datenfluss unterdrückt oder freigibt. `GATE` bleibt vorerst eine prototypspezifische Arbeitshypothese.

Das bisherige Reproduktionsfragment mit fest gesetzter Partner-ID blieb als ausdrücklich technische Kontrollstruktur im Startgenom. Exploration und Partnerbildung lassen sich dadurch in der Lupe getrennt betrachten.

## Erster kontrollierter P1-Lauf

Konfiguration:

```text
Seed                 42
Startpopulation      20
Startenergie         500 je Entität
RAM                   unverändert zufällig
Snapshotabstand      1 Tick
Laufdauer            30 Ticks
```

Run-ID: `d89c01b8-8651-454e-b98a-a17da9a71757`

Beobachtet wurden:

- 312 RAM-Lesevorgänge,
- 12 unterschiedliche RAM-Adressen populationsweit,
- 5 bis 11 unterschiedliche Adressen je ursprünglicher Startentität,
- 304 Schreibvorgänge auf der Suchstandadresse `Z[0]`,
- 244 Fundspeicherungen auf `Z[1]`,
- 210 konditional weitergeleitete Werte auf `Z[2]`,
- 269 geöffnete GATE-Ausführungen,
- 91 Nachkommen,
- vollständiges Aussterben bis Tick 23.

Kein gelesener Wert war in diesem kurzen Adressbereich null. Daher wurde noch keine geschlossene GATE-Ausführung beobachtet. Außerdem suchten die Startentitäten aufgrund ihres gleichen Ausgangsgenoms weitgehend im Gleichschritt und erzeugten populationsweit nur zwölf unterschiedliche Adressen.

## Einordnung

- **Beobachtung:** Die P1-Genome erzeugten über mehrere Ticks wechselnde RAM-Adressen und hielten den Suchstand in Z fest.
- **Beobachtung:** Fundwert, Suchstand und konditional weitergeleiteter Wert landeten in getrennten Z-Zellen.
- **Designentscheidung:** `GATE` und die konkrete P1-Startstruktur wurden von uns eingebaut.
- **Interpretation:** Die Adressänderung darf im eng definierten technischen Sinn als Exploration bezeichnet werden, weil sie aus dem genomischen Datenfluss entsteht.
- **Keine Beobachtung:** Neugier, Lernen, zielgerichtete Suche, Bewertung eines Fundes, Anpassung oder langfristige Überlebensfähigkeit.

P1 beantwortet damit eine kleine, aber notwendige Frage: Eine EVE-Entität kann aus ihrem Genom heraus einen fortschreitenden Zugriff auf eine unveränderte Umwelt erzeugen. Die nächste Frage lautet nicht mehr, ob sie überhaupt suchen kann, sondern wie aus gleichförmiger Suche unterschiedliche, vererbbare Suchstrategien werden könnten.

## Korrektur: Die Kinder starteten noch mit P0-Energie

Die Einzelansicht der Lupe machte anschließend eine nicht kontrollierte Differenz sichtbar: Die P1-Startpopulation besaß je 500 Energie, Kinder wurden jedoch weiterhin mit der alten P0-Geburtsenergie 50 erzeugt. `S_birth` war korrekt energieerhaltend von den Eltern bezahlt worden, passte aber nicht zum beabsichtigten Vergleich.

Die Control-Schicht erhielt deshalb den ausdrücklichen Parameter `--birth-energy`. P0 behält den Standardwert 50. Im korrigierten P1-Lauf wurden Start- und Geburtsenergie beide auf 500 gesetzt; dies bleibt eine Versuchsentscheidung und wird nicht automatisch vererbt.

| Messgröße | P1 mit `S_birth=50` | P1 mit `S_birth=500` |
|---|---:|---:|
| Nachkommen | 91 | 10 |
| RAM-Lesevorgänge | 312 | 357 |
| unterschiedliche RAM-Adressen | 12 | 22 |
| RAM-Lesevorgänge der Kinder | 116 | 183 |
| unterschiedliche Adressen der Kinder | 4 | 22 |
| letzter Tod | Tick 23 | Tick 39 |

Der korrigierte Lauf erzeugte erheblich weniger Kinder, aber diese Kinder konnten ihr Genom wesentlich länger ausführen und trugen deutlich stärker zur Exploration bei. Vollständiges Aussterben blieb bestehen.

Maßgebliche korrigierte Run-ID: `9a0f25fc-5cfd-43eb-bb50-1f30baeaa008`.

## Versuch: Geburtsenergie als Anteil der Elternenergie

Der feste Wert 500 erschien anschließend als zu hoher Preis für eine einzelne Geburt. Deshalb wurde ein vollständig energieerhaltender relativer Modus ergänzt. Das Kind erhielt die Hälfte der mittleren aktuellen Elternenergie; alle Eltern bezahlten davon gleiche Anteile.

| Messgröße | fest 50 | fest 500 | 50 % des Elternmittels |
|---|---:|---:|---:|
| Nachkommen | 91 | 10 | 57 |
| mittlere Geburtsenergie | 50 | 500 | 109,84 |
| RAM-Lesevorgänge | 312 | 357 | 316 |
| unterschiedliche RAM-Adressen | 12 | 22 | 12 |
| RAM-Lesevorgänge der Kinder | 116 | 183 | 187 |
| letzter Tod | Tick 23 | Tick 39 | Tick 21 |

Die relative Regel verteilte Energie weniger extrem, stabilisierte die Population jedoch nicht. Weil jede Generation mit der bereits gesunkenen aktuellen Elternenergie rechnete, reichten die Geburtsenergien schließlich bis auf 9,39 hinunter. Das erzeugte erneut viele sehr schwache Kinder und ein früheres vollständiges Aussterben.

Der Modus bleibt als reproduzierbarer Versuchsparameter implementiert. Der Befund spricht aber dagegen, `0,5 * Mittelwert(S_eltern)` ohne weitere Bedingung bereits als neue allgemeine Reproduktionsregel festzulegen.

## Mindestlaufzeit statt Energiegeschenk

Als nächste Hypothese wurde die relative Geburtsenergie beibehalten, eine Geburt aber nur zugelassen, wenn das konkrete Kindergenom mit dieser Energie fünf volle Heartbeats finanzieren könnte. Die Schwelle erzeugt keine Energie: Unterschreitet das Angebot den berechneten Bedarf, gibt es kein Kind und keinen Energieabzug.

Der Bedarf wird konservativ aus Standby, Aktivitätsbudget, Ausführungskosten und maximaler Kantenzahl einer Kindinstanz berechnet. Mögliche spätere Belohnungen zählen nicht als garantierte Energie.

| Messgröße | 50 % ohne Schwelle | 50 % + 5 Heartbeats |
|---|---:|---:|
| Nachkommen | 57 | 21 |
| kleinste Geburtsenergie | 9,39 | 119,16 |
| mittlere Geburtsenergie | 109,84 | 195,15 |
| RAM-Lesevorgänge | 316 | 345 |
| unterschiedliche RAM-Adressen | 12 | 13 |
| letzter Tod | Tick 21 | Tick 24 |

Die Mindestlaufzeit beseitigte die extrem schwachen Geburten. 149 Gruppengeburtsversuche wurden ohne Energieverlust abgelehnt. Diese hohe Zahl entsteht, weil eine gescheiterte Geburt gemäß der gesetzten P0-Regel die Partnerslots nicht leert und die Gruppe im nächsten Heartbeat erneut geprüft wird. Der Mechanismus ist damit energetisch sauber, zeigt aber eine neue offene Frage zur Behandlung wiederholt nicht finanzierbarer Konstellationen.

Run-ID: `6b34f4dd-5961-4d24-8bcd-084e64cf5e55`.

## Startenergie ist kein Fortpflanzungskapital

Die Versuche mit festen und relativen Geburtsenergien hatten eine frühere Grundidee verdeckt: Eine Amöbe sollte sich mit ihrer bloßen Startenergie überhaupt nicht fortpflanzen können. Für jede Entität wird deshalb der eigene Geburtswert `S₀` festgehalten. Nach einer Geburt muss jeder Elternteil seinen Beitrag bezahlt haben und trotzdem strikt über `S₀` liegen.

Im ersten Lauf unter dieser wiederhergestellten Regel entstanden keine Kinder. Keine der 20 Startamöben überschritt jemals ihre Geburtsenergie 500; der höchste beobachtete Wert nach einer Buchung war 499. Trotzdem führten sie 367 RAM-Lesevorgänge auf 20 unterschiedlichen Adressen aus und starben bis Tick 38 vollständig aus.

Der Befund trennt zwei Fähigkeiten:

- Das P1-Genom kann die RAM-Suppe fortschreitend untersuchen.
- Die gegenwärtige Umweltökonomie liefert dabei keinen reproduktiven Energieüberschuss.

Damit verschiebt sich die nächste Aufgabe folgerichtig von der Geburtsmechanik zur Umwelt: In der Suppe muss bilanziertes „Futter“ existieren, das eine Entität durch Umweltkontakt erschließen kann. Eine Geburt bleibt energieerhaltend und setzt einen real erwirtschafteten Überschuss voraus.

Run-ID: `36776956-b72a-4652-992c-8b0ee9869817`.

## Die Suppe selbst wird zum Futter

Futter wurde anschließend präzisiert: Es ist keine zweite unsichtbare Ressourcenschicht, sondern die von einer Amöbe sequenziell wahrgenommene Veränderung eines RAM-Werts. Liest sie an derselben Adresse beispielsweise `17 -> 42 -> 17 -> 17`, sind die ersten drei Lesezustände belohnbar; das zweite `17` liefert weniger als das erste und die unmittelbare Wiederholung liefert nichts.

RAM-Zellen tragen dafür eine unsichtbare Urheberkette. Eine Amöbe darf RAM weiterhin überschreiben, erhält aber keine Energie aus einem Wert, an dessen Erzeugung sie selbst beteiligt war. Andere, noch nicht beteiligte Amöben können die Veränderung erschließen. Die Energie entsteht beim `RAM-read`; `Z-write` bleibt dauerhafter Speicher ohne direkte Belohnung.

Der erste Lauf dieser Ökonomie erzeugte 270 belohnte Veränderungen und insgesamt 2.700 Energieeinheiten bei 322 RAM-Lesevorgängen. Dennoch überschritt keine Amöbe ihre Geburtsenergie 500, es entstanden keine Kinder und die Population starb bis Tick 34 aus. Die Suppe bietet nun Nahrung im definierten Sinn; Menge beziehungsweise Ertrag stehen aber noch nicht in einem tragfähigen Verhältnis zu den Ausführungskosten.

Run-ID: `1830d15a-b674-48c9-8bb1-d22993df8a0e`.

## Tarifverhandlungen mit der Suppe

Da die Amöben Nahrung fanden, aber die Lebenshaltungskosten den Ertrag überstiegen, wurde ausschließlich die Neuheitsbasis variiert. Alle übrigen Bedingungen blieben unverändert.

| Neuheitsbasis | Nachkommen | lebend bei Tick 200 | RAM-Lesevorgänge | belohnte Veränderungen | ausgezahlte Energie |
|---:|---:|---:|---:|---:|---:|
| 10 | 0 | 0 | 322 | 270 | 2.700 |
| 20 | 0 | 0 | 454 | 382 | 7.640 |
| 40 | 0 | 5 | 1.738 | 1.413 | 56.520 |
| 80 | 141 | 128 | 8.715 | 7.060 | 564.800 |
| 160 | 399 | 324 | 21.036 | 17.001 | 2.720.160 |

Die Versuchsreihe zeigt einen deutlichen Übergang zwischen 40 und 80. Bei 40 überleben einzelne Gründer bis zum Ende des Beobachtungsfensters, erwirtschaften aber keine erfolgreiche Geburt. Bei 80 entsteht erstmals eine wachsende Population. Bei 160 nimmt das Wachstum bis Tick 200 stark zu.

Damit ist die Umweltökonomie nun experimentell kalibrierbar. Die gewählte Neuheitsbasis ist keine Naturkonstante; sie bestimmt gemeinsam mit Ausführungs- und Lebenshaltungskosten, ob Exploration energetisch defizitär, gerade bestandserhaltend oder stark wachstumsfördernd ist.
