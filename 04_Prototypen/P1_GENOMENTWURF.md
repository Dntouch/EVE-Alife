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
5. **Reproduktion:** Die frühere fest verdrahtete Partner-ID bleibt nur in den P0-Kontrollgenomen erhalten. Das aktuelle P1-Startgenom durchsucht virtuelle Membranen. Nur eine als lebend gelesene fremde ID mit passender Membranprovenienz darf in den eigenen Partnerslot gelangen. Eine im fremden Slot erkannte Einladung an die eigene ID kann genomisch erwidert werden.

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

### Versuch mit relativer Geburtsenergie

Als energieerhaltender Mittelweg wurde anschließend folgende Regel erprobt:

```text
S_kind = 0,5 * Mittelwert(S_eltern)
Beitrag je Elternteil = S_kind / Anzahl der Eltern
```

Die Energie wird damit weiterhin ausschließlich von den Eltern übertragen. Der Lauf mit sonst identischen P1-Bedingungen ergab:

- 57 Nachkommen,
- Geburtsenergien zwischen 9,39 und 240,27,
- mittlere Geburtsenergie 109,84,
- 316 RAM-Lesevorgänge und 12 unterschiedliche Adressen,
- 187 RAM-Lesevorgänge der Kinder,
- vollständiges Aussterben bis Tick 21.

Run-ID: `ef3637b0-c9af-4869-9aa3-99d91b1ac2f1`.

Die Regel liegt bei der Kinderzahl zwischen den festen Werten 50 und 500, erzeugt aber eine generationenübergreifende Abwärtsspirale: Sinkende Elternenergie senkt die Geburtsenergie; schwache Kinder erzeugen wiederum noch schwächere Kinder. Der Versuch ist implementiert und reproduzierbar, wird aufgrund dieses Befunds aber noch nicht zur maßgeblichen P1-Regel erklärt.

### Relative Energie mit genomabhängiger Mindestlaufzeit

Der relative Modus wurde daraufhin um eine energieerhaltende Geburtsbedingung ergänzt. Eine Geburt findet nur statt, wenn die angebotene Energie das konkrete, bereits rekombinierte Kindergenom für fünf volle Heartbeats konservativ finanzieren könnte. Reicht sie nicht, wird keine Energie abgezogen und kein Kind erzeugt.

Der Bedarf ergibt sich aus Standbykosten, Aktivitätsbudget, Ausführungskosten und der höchsten Zahl ausgehender Kanten einer Kindinstanz. Künftige Z-Belohnungen werden nicht als sichere Einnahme angerechnet.

Der Lauf mit `birth_energy_fraction = 0,5` und `birth_min_heartbeats = 5` ergab:

- 21 Nachkommen,
- Geburtsenergien zwischen 119,16 und 240,27,
- mittlere Geburtsenergie 195,15,
- 149 abgelehnte Gruppengeburtsversuche ohne Energieabzug,
- 345 RAM-Lesevorgänge und 13 unterschiedliche Adressen,
- 135 RAM-Lesevorgänge der Kinder,
- vollständiges Aussterben bis Tick 24.

Run-ID: `6b34f4dd-5961-4d24-8bcd-084e64cf5e55`.

Die Schranke verhinderte extrem schwache Geburten, ohne Energie zu erzeugen. Sie führte jedoch zu vielen wiederholten Ablehnungen, weil nach einer nicht finanzierbaren Geburt die Partnerslots gemäß der bestehenden Regel belegt bleiben. Ob diese Wiederholungen lediglich beobachtbarer Selektionsdruck oder unnötige Reproduktionsschleifen sind, bleibt vor einer Festlegung zu klären.

### Rückkehr zur Überschussbedingung

Aus dem frühen Entwurf wurde anschließend die strengere Rahmenbedingung wiederhergestellt: Eine Amöbe darf sich nicht aus ihrer bloßen Startenergie fortpflanzen. Nach Abzug ihres Elternbeitrags muss ihre Energie strikt über ihrem individuellen Geburtswert `S₀` liegen.

Der P1-Lauf mit relativer Geburtsenergie, Fünf-Heartbeat-Schwelle und dieser Überschussbedingung ergab:

- keine Nachkommen,
- kein beobachteter Energiewert oberhalb des `S₀ = 500` der Startpopulation,
- höchster beobachteter Energiewert nach einer Buchung: 499,
- 367 RAM-Lesevorgänge,
- 20 unterschiedliche RAM-Adressen,
- vollständiges Aussterben bis Tick 38.

Run-ID: `36776956-b72a-4652-992c-8b0ee9869817`.

Dies ist kein Defekt der Reproduktion. Der Lauf zeigt, dass Exploration unter der aktuellen Kosten- und Belohnungsstruktur keinen Fortpflanzungsüberschuss erwirtschaftet. Die nächste Umweltstufe benötigt daher eine bilanziert zugängliche Energiequelle in der RAM-Suppe – „Futter“ – statt einer Lockerung der Geburtsbedingung.

### RAM-Veränderung als Futter

„Futter“ wurde anschließend nicht als zusätzliche Ressourcenschicht, sondern als individuell wahrgenommene Veränderung eines RAM-Werts präzisiert. Ein erster oder gegenüber dem letzten Lesen veränderter externer Wert liefert beim `RAM-read` Energie. Ein unmittelbar unveränderter oder selbst erzeugter Wert liefert nichts. Kehrt ein früherer Wert nach einem anderen Wert zurück, entsteht erneut Energie, deren Höhe mit jeder früheren Belohnung desselben Adress-Wert-Paars sinkt.

Im ersten Lauf mit dieser Regel wurden beobachtet:

- 322 RAM-Lesevorgänge,
- 270 belohnte Veränderungen,
- insgesamt 2.700 Energieeinheiten aus RAM-Leseereignissen,
- 19 unterschiedliche RAM-Adressen,
- weiterhin keine Nachkommen,
- kein beobachteter Energiewert oberhalb des `S₀ = 500`,
- vollständiges Aussterben bis Tick 34.

Run-ID: `1830d15a-b674-48c9-8bb1-d22993df8a0e`.

Die Suppe enthält damit erstmals das definierte Futter, die Belohnungsbasis 10 reicht unter den gegenwärtigen Ausführungskosten und dem P1-Genom jedoch noch nicht für einen reproduktiven Überschuss. Das ist nun eine messbare Umwelt- und Kostenfrage.

### Tarifrunde der IG Amöbe

Bei unverändertem Seed, Genom, RAM, Startenergie, relativer Geburtsenergie, Fünf-Heartbeat-Schwelle und Überschussbedingung wurde ausschließlich `novelty_base` variiert. Jeder Lauf dauerte 200 Ticks.

| Neuheitsbasis | Nachkommen | lebend bei Tick 200 | maximale Population | RAM-Lesevorgänge | letzter Tod |
|---:|---:|---:|---:|---:|---:|
| 10 | 0 | 0 | 20 | 322 | Tick 34 |
| 20 | 0 | 0 | 20 | 454 | Tick 48 |
| 40 | 0 | 5 | 20 | 1.738 | Tick 193 |
| 80 | 141 | 128 | 128 | 8.715 | Tick 192 |
| 160 | 399 | 324 | 324 | 21.036 | Tick 196 |

Bei 40 reicht der Ertrag erstmals für das Fortbestehen einzelner Gründer über 200 Ticks, aber noch nicht für eine erfolgreiche Geburt. Zwischen 40 und 80 liegt in dieser Staffel die erste reproduktive Tarifgrenze. Bei 80 wächst die Population; bei 160 ist das Wachstum bereits deutlich stärker. Diese Grenze ist ein Ergebnis genau dieser Kosten, Genome und Umwelt und kein allgemeiner EVE-Konstantwert.

Run-IDs:

- 10: `a37a384c-ce36-48de-a87e-1421cd57d5cc`
- 20: `5a980744-6b15-40d5-8c1b-a609d27620c6`
- 40: `d992ad6c-1e67-4ca5-b38e-ac640dc973bb`
- 80: `1cb45901-3595-4fa9-94aa-082e430ddfa9`
- 160: `491d086f-1249-44d7-801f-6ddcbd4944f6`

### Dynamische Partnersuche und Generation 2

Die Tarifläufe zeigten trotz vieler Kinder ausschließlich Generation 1. Ursache war kein biologischer Befund, sondern die fest verdrahtete Partner-ID der technischen Startpopulation: Gründer schrieben nach jeder Geburt erneut ihre ursprünglichen Partner in die geleerten Slots, während Kinder geerbte, für sie unpassende IDs besaßen.

Als erste Zwischenlösung berechnete das P1-Genom sein Partnerpaar selbst aus der eigenen Membran-ID. Die Abbildung `((ID - 1) XOR 1) + 1` verband `1 ↔ 2`, `3 ↔ 4` und so weiter. Der Supervisor prüfte weiterhin nur die wechselseitige Konstellation; sämtliche Lese-, Rechen- und Schreiboperationen wurden vom Genom ausgeführt. Diese Variante erzeugte Generation 2, wurde anschließend jedoch verworfen: Sie war eine mathematisch versteckte Zwangspaarung und keine gefundene Partnerschaft.

Der erste 300-Tick-Test mit Tarif 60 und Altersrate 0,01 ergab:

- 38 Nachkommen,
- 58 Entitäten insgesamt,
- 52 lebende Entitäten bei Tick 300,
- erstmals Generation 2,
- zwei Kinder des Nachkommenpaars 41 und 42.

Run-ID: `c61fd90c-5a1c-4fc1-80fc-4e1651f872b0`.

Damit ist die technische Sterilität aller Nachkommen beseitigt. Die Generationstiefe bleibt dennoch eine offene Selektionsfrage: Das Partnerfragment kann bei der Rekombination unvollständig vererbt werden, und im anschließenden Langzeitlauf entstand noch keine Generation 3.

### Alterskosten und erneuter Tarif-60-Langzeitlauf

Ein fester Standbybetrag begünstigte frühe Entitäten unbegrenzt. Neue Läufe verwenden daher zusätzliche Alterskosten von `Alter × 0,01` pro Heartbeat. Es gibt weiterhin kein Ablaufdatum; hohes Alter bleibt möglich, muss aber zunehmend finanziert werden.

Der 1.000-Tick-Lauf mit dynamischer Partnersuche, Tarif 60 und Altersrate 0,01 ergab:

| Tick | lebend | insgesamt geboren |
|---:|---:|---:|
| 100 | 30 | 31 |
| 300 | 52 | 58 |
| 500 | 58 | 70 |
| 700 | 49 | 71 |
| 1.000 | 32 | 71 |

Insgesamt entstanden 51 Nachkommen und Generation 2, aber keine Generation 3. Die Population erreichte um Tick 500 ihr beobachtetes Maximum und schrumpfte danach. 19 der 20 Gründer starben; eine Gründerin erreichte weiterhin Tick 1.000. Tarif 60 trägt unter den neuen Bedingungen also eine langfristig überlebende Population, aber kein dauerhaftes Wachstum wie im früheren Lauf ohne Alterskosten und mit kleinerem, fest verdrahtetem Partnerfragment.

Run-ID: `b623e0f1-eccb-41d1-9311-81288617b37d`.

### Gefundene Partner, Einladungen und RAM-Schreiben

Die berechnete Nachbar-ID wurde durch ein echtes Such-und-Handshake-Fragment ersetzt. Ein Suchzeiger in `Z[3]` durchläuft den virtuellen Membranraum. Nur der gelesene Wert einer lebenden fremden ID-Zelle trägt die Provenienz, die ein Schreiben in den eigenen Partnerslot erlaubt. Ein fremder Partnerslot mit der eigenen ID ist eine erkennbare Einladung und kann genomisch erwidert werden. Der erste neue Entitätsfund liefert im Test 10, eine neu erkannte Einladung 20 Energie; unveränderte Wiederholungen liefern nichts.

Das Startgenom enthält zusätzlich ein getrenntes neutrales Schreibfragment, das die eigene ID nach `RAM[eigene ID]` schreibt. Das Schreiben selbst wird nicht belohnt. Andere Amöben können den externen Wert jedoch nach der bestehenden RAM-Nahrungsregel entdecken. Zusammenhängende Netzkomponenten werden nun tatsächlich atomar vererbt und bei der Rekombination nicht mehr angeschnitten.

### Unterlineare Genomkosten

Das gewachsene P1-Genom zeigte einen unerwünschten linearen Kosteneffekt: Mehr Verhalten wurde fast automatisch mit kürzerem Leben bestraft. Neue Läufe berechnen den Lebensunterhalt deshalb als `1 + Alter × 0,01 + 0,5 × √N_f + 0,1 × √N_p`. Das Genom bleibt selektiv relevant, eine Verdoppelung seiner Größe verdoppelt die Kosten aber nicht. Die bisherigen linearen Standardkosten je ausgeführtem Funktionspunkt und übertragener Kante entfallen. Teure reale Wirkungen können später weiterhin gezielt am jeweiligen primitiven Funktionspunkt bepreist werden.

Der erste 300-Tick-Lauf mit Tarif 60 wies 708 RAM-Schreibvorgänge, 172 neue Entitätsfunde, 9 erkannte Einladungen und erstmals einen Informationsproduzenten nach. Flüchtig überschriebene Vorschläge erzeugten jedoch keine stabile Gruppe. Nach der Korrektur blieben Vorschläge stehen; es entstanden 114 formale Geburtsprüfungen, die sämtlich an der Überschussbedingung scheiterten. Das neue vollständige Startgenom ist mit 100 Genombestandteilen deutlich teurer als sein Vorgänger; Tarif 60 ist deshalb nicht direkt vergleichbar.

Ein ausdrücklich als Funktionskontrolle markierter 300-Tick-Lauf mit Tarif 160 ergab:

- 424 neue Entitätsfunde,
- 20 erkannte Einladungen,
- 2.546 RAM-Schreibvorgänge,
- 9 Kinder,
- 29 Entitäten insgesamt und 27 lebend bei Tick 300,
- erstmals einen realen Informationsproduzenten mit 4.160 für andere erzeugten Energieeinheiten.

Run-IDs:

- erster flüchtiger Handshake bei Tarif 60: `f5a9e883-6a9b-44f6-9bd7-2c40b93ce7e9`,
- stabiler Handshake bei Tarif 60: `c0390378-e93b-4329-bfea-b304cfecf58b`,
- Funktionskontrolle bei Tarif 160: `760442a6-413f-4f6e-8e62-85233ebfe31e`.

Die Kausalkette `finden → vorschlagen → Einladung erkennen → erwidern → Geburt` ist damit ausführbar. Der Tarif für das größere Sozial- und Schreibgenom sowie die noch stark auf frühe gefundene Amöben konzentrierte Partnerwahl bleiben neue Versuchsfragen.

Die Membran stellt zusätzlich unter Offset 2 einen Wert von `0` bis `10` bereit. Das Suchfragment liest zu jeder gefundenen ID auch diesen Wert. `0` bedeutet tot, `10` energetisch fortpflanzungsfähig; `1` bis `9` bleiben absichtlich ohne semantische Etiketten. Sie quantisieren lediglich die aktuelle Energie relativ zur Schwelle einer symmetrischen Zweierpaarung gleicher Stärke. Jede Veränderung, insbesondere der Wechsel auf `0`, kann neue Erkenntnis liefern. Der tote Membraneintrag bleibt beobachtbar, darf aber nicht mehr als Partner verwendet werden.

Der erste 1.000-Tick-Lauf der zunächst binären Erweiterung bei Tarif 60 beobachtete 798 lebende und 90 tote Lebenszustände als neue Information. Daraus entstanden 8.880 Energieeinheiten, davon 900 durch das Auffinden Verstorbener. Der Lauf endete mit 28 lebenden von insgesamt 40 Amöben, 20 Nachkommen und Generation 2. Dieser Lauf wies den Datenpfad nach; anschließend wurde das binäre Signal durch die Skala `0` bis `10` ersetzt. Gegenüber dem vorherigen Tarif-60-Lauf ist dies kein isolierter Wirkungsvergleich, weil das vergrößerte Genom den Zufalls- und Ausführungspfad verändert.

Run-ID: `b037b33f-89fc-4dd1-bd25-0fe4ffb6baef` (Lauf 38).

Der anschließende Lauf mit der unbenannten Skala `0` bis `10` beobachtete sämtliche elf möglichen Werte. Von 1.091 neuen Membranwerten entfielen 83 auf `0` und 614 auf `10`; zusammen lieferten die Zustandsänderungen 10.471,5 Energieeinheiten. Nach 1.000 Ticks lebten 26 von insgesamt 37 Amöben, 17 Nachkommen waren entstanden. Die Skala ist damit nicht nur rechnerisch definiert, sondern wird vom unveränderten Suchfragment in beide Richtungen tatsächlich durchlaufen. Die auffällig häufige `10` ist zunächst eine Beobachtung dieses Laufs und keine Aussage über Fitness im weiteren Sinn.

Run-ID: `a77b7062-e55f-452d-8a5d-af2320b0690d` (Lauf 39).

Der anschließende 1.000-Tick-Vergleich mit dem ausgehandelten Tarif 60 und den neuen unterlinearen Genomkosten ergab:

- 29 Nachkommen und 49 Entitäten insgesamt,
- 38 lebende Amöben bei Tick 1.000,
- Generation 4 statt zuvor höchstens Generation 2,
- 1.460 neue Entitätsfunde und 64 erkannte Einladungen,
- 9.845 neutrale RAM-Schreibvorgänge,
- 388.240 gewonnene Energieeinheiten.

Run-ID: `157811c6-aee4-4418-8cb8-6eef05fd6c5a`.

Damit war nicht der Tarif 60 allein das Hindernis. Die lineare Besteuerung des größeren Verhaltensgenoms hatte die Population wirtschaftlich abgeschnitten. Das unterlineare Modell erhält weiterhin Größenkosten und Altersdruck, erlaubt bei unveränderter Umwelt aber erstmals eine über vier Generationen fortbestehende Population mit echter Partnersuche.
