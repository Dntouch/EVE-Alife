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
