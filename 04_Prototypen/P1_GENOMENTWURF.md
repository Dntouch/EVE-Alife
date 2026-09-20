# P1 – Genomentwurf für beobachtbare Exploration

Status: Erste Arbeitsdefinition implementiert und technisch geprüft

Stand: 20. September 2026

## 1. Fragestellung

Kann eine Population mit unveränderter zufälliger RAM-Suppe durch ihr Genom unterschiedliche Umweltadressen erreichen, Werte aufnehmen und ihren weiteren Datenfluss vom Gelesenen abhängig machen?

P1 prüft noch keine Intelligenz und keine offene Evolution. Es prüft den kleinsten Schritt von einer technischen Ablaufprobe zu beobachtbarer, umweltabhängiger Aktivität.

## 2. Konstante Versuchsbedingungen

- Die RAM-Suppe bleibt zufällig und wird nicht mit Fundstellen oder Nahbereichsinseln präpariert.
- Seed, Populationsgröße, Startenergie und Kosten werden pro Vergleichslauf dokumentiert.
- Die P0-Ausführungssemantik, Z-Belohnung, Membran, Reproduktion und Mutation bleiben zunächst unverändert.
- Ein P1-Lauf wird stets gegen einen P0-Lauf mit denselben Umwelt- und Energieparametern verglichen.

## 3. Neue primitive Funktion: `GATE`

P0 kann mit `EQ` zwar einen Wahrheitswert erzeugen, aber nicht verhindern, dass ein Wert über eine Kante weitergesendet wird. Für eine echte datenabhängige Wirkung ergänzt P1 versuchsweise:

```text
GATE(value, condition) -> value, falls condition != 0
GATE(value, condition) -> keine Ausgabe, falls condition == 0
```

`GATE` interpretiert keine Bedeutung des Werts. Es prüft lediglich Null gegen Nichtnull, verbraucht beide Eingänge und übernimmt die vereinigte Provenienz. Alle vorhandenen Ausgangskanten erhalten die Ausgabe oder keine von ihnen. Kosten und Scheduling entsprechen einem gewöhnlichen Funktionspunkt.

Die Aufnahme in das allgemeine Grundkonzept erfolgt erst nach praktischer Prüfung.

## 4. P1-Startgenom

Das Startgenom besteht aus nachvollziehbaren Netzfragmenten, nicht aus einem Supervisorbefehl „erkunde“:

1. **Suchstand:** `Z_READ`, `CONST(1)`, `ADD` und `Z_WRITE` lesen eine gespeicherte Adresse, erhöhen sie und schreiben sie als nächsten Suchstand zurück.
2. **Umweltzugriff:** Derselbe Adresswert fließt zu `RAM_READ`.
3. **Fundspeicher:** Der gelesene RAM-Wert wird über einen eigenen `Z_WRITE` in Z abgelegt. Suchstand und Umweltinhalt verwenden getrennte Z-Adressen.
4. **Reaktion:** `EQ` und `GATE` können einen Pfad abhängig von einem gelesenen Wert öffnen. Die erste P1-Fixture darf eine einfache, ausdrücklich dokumentierte Bedingung verwenden; sie ist Teststruktur, keine behauptete biologische Bedeutung.
5. **Reproduktion:** Die bisherige fest verdrahtete Partner-ID darf in einem Kontrollgenom erhalten bleiben, wird aber getrennt vom Explorationsfragment ausgewiesen. So lassen sich Exploration und technische Fortpflanzung in der Lupe auseinanderhalten.

Z beginnt weiterhin leer. Der leere Lesezustand liefert wie in P0 den Wert `0`; damit kann das Netz ohne versteckte Initialisierung aus dem Supervisor anlaufen.

## 5. Varianten der Population 1

Für den ersten P1-Vergleich sind mindestens zwei Genome vorgesehen:

- **P1-Kontrolle:** P0-Demogenom bei den P1-Energieparametern.
- **P1-Explorer:** Suchstand-, RAM-Lese-, Fundspeicher- und Reaktionsfragment.

Spätere Varianten dürfen Fragmentkopien oder andere Konstanten besitzen. Ihre reale Kopienzahl bleibt Teil des Genoms und damit zugleich Vererbungsgewicht; ein externes Gewichtungsfeld wird nicht eingeführt.

## 6. Beobachtbare Kriterien

Die Lupe und der Ereignisstrom müssen ohne Bedeutungsbehauptung zeigen können:

- wie viele unterschiedliche RAM-Adressen gelesen wurden,
- welche Adressen eine Entität erreicht hat,
- welche Werte und Provenienzen aktuell in K und Z liegen,
- wie sich der gespeicherte Suchstand über Ticks verändert,
- welcher Funktionspunkt über welche P-Kante verbunden ist,
- wann ein `GATE` gesendet oder unterdrückt hat,
- ob Geburten, Lebensdauer und Adressvielfalt gegenüber der Kontrolle abweichen.

Die Lupe soll diese Entwicklung außerdem als steuerbaren Lebensfilm einer einzelnen Entität wiedergeben. Replay ist ausschließlich eine nachträgliche Darstellung persistierter Snapshots und Events und keine erneute Ausführung des Genoms.

„Exploration“ bedeutet für P1 ausschließlich messbare Adressvielfalt und fortschreitenden Umweltzugriff. „Entdeckung“, „Lernen“ oder „Anpassung“ werden daraus nicht automatisch abgeleitet.

## 7. Abnahmekriterien vor P2

P1 ist technisch erfolgreich, wenn ein deterministischer Lauf bei identischer Umwelt gegenüber der P0-Kontrolle:

1. mehrere RAM-Adressen aus genomisch erzeugten Adresswerten liest,
2. Suchstand und gelesene Inhalte in der Lupe tickweise nachvollziehbar macht,
3. mindestens einen datenabhängig geöffneten oder unterdrückten Pfad nachweist,
4. nach Checkpoint-Fortsetzung denselben Verlauf erzeugt und
5. keine Rückwirkung der Lupe auf den Core besitzt.

## 8. Erste Implementierung

Die erste P1-Variante ist im Prototyp als `p1_explorer_genome` umgesetzt und über `--p1-explorers` auswählbar. Ihre Z-Belegung ist fest nachvollziehbar:

```text
Z[0] = fortgeschriebener Suchstand
Z[1] = zuletzt gelesener RAM-Wert
Z[2] = letzter durch GATE weitergeleiteter Nichtnull-Wert
```

Ein technischer Lauf mit Seed `42`, 20 Startentitäten, unveränderter zufälliger RAM-Suppe und je 500 Startenergie ergab:

- 312 RAM-Lesevorgänge,
- 12 unterschiedliche RAM-Adressen in der Gesamtpopulation,
- zwischen 5 und 11 unterschiedliche Adressen je ursprünglicher Startentität,
- 269 geöffnete `GATE`-Ausführungen,
- Schreibvorgänge auf allen drei vorgesehenen Z-Adressen,
- 91 Nachkommen und vollständiges Aussterben bis Tick 23.

Run-ID: `d89c01b8-8651-454e-b98a-a17da9a71757`.

Damit sind fortschreitender Umweltzugriff, persistenter Suchstand und konditionale Weiterleitung technisch nachgewiesen. Im zufälligen Adressbereich dieses kurzen Laufs wurde kein Wert `0` gelesen; deshalb wurde `GATE` noch nie geschlossen. Unterschiedliche Startentitäten durchliefen außerdem weitgehend denselben niedrigen Adressbereich. Beides sind Befunde für die nächste Populationsvariante, keine Gründe, die Umwelt künstlich zu verändern.

### Korrektur der Geburtsenergie

Der erste Lauf übernahm unbemerkt die P0-Geburtsenergie `S_birth = 50`, obwohl die künstliche P1-Startpopulation je 500 Energie besaß. Die 91 Kinder waren deshalb energetisch nicht mit ihren Eltern vergleichbar. Dies war kein Vererbungsfehler: Startenergie und die vollständig von den Eltern bezahlte Geburtsenergie waren getrennte Versuchsparameter. Für einen kontrollierten P1-Vergleich müssen beide ausdrücklich denselben Wert erhalten.

Ein korrigierter Lauf mit ansonsten identischen Bedingungen und `S_birth = 500` ergab:

- 10 statt 91 Nachkommen,
- 357 RAM-Lesevorgänge,
- 22 unterschiedliche RAM-Adressen populationsweit,
- 183 RAM-Lesevorgänge durch Kinder,
- 322 geöffnete und weiterhin keine geschlossene `GATE`-Ausführung,
- vollständiges Aussterben bis Tick 39 statt Tick 23.

Run-ID: `9a0f25fc-5cfd-43eb-bb50-1f30baeaa008`.

Die höhere Geburtsenergie erzeugte weniger Geburten, gab jedem Kind aber genügend Energie für eine längere eigene Ausführung. Die Kinder erreichten im korrigierten Lauf alle 22 populationsweit besuchten Adressen; bei Geburtsenergie 50 hatten sie nur vier unterschiedliche Adressen erreicht. Dieser korrigierte Lauf ist die maßgebliche P1-Referenz. `--start-energy` und `--birth-energy` bleiben getrennt sichtbar, weil ihre Gleichsetzung eine dokumentierte Versuchsentscheidung und kein allgemeines Naturgesetz ist.
