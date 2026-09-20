# EVE-Alife – Prototyp v0.1

Status: Technische Spezifikation im Aufbau

Stand: 20. September 2026

## 1. Grundlage und Geltungsbereich

Maßgebliche fachliche Grundlage ist ausschließlich das fortlaufende EVE-Alife-Grundkonzept in `02_Konzept/Grundkonzept_Arbeitsentwurf.md`. Zusätzlich gelten die übergeordneten Implementierungsregeln in `04_Prototypen/INSTRUKTIONEN_v0.1.md`.

Dieses Dokument legt austauschbare technische und prototypspezifische Regeln für v0.1 fest. Es erweitert das Grundkonzept nicht um allgemeine Naturgesetze. Bei einem Widerspruch hat das Grundkonzept Vorrang.

## 2. RAM-Neuheit und Urheberkette

### 2.1 Unsichtbare Metadaten

Jeder im P-Netz fließende Wert trägt zusätzlich supervisorseitige Quellen- und Urhebermetadaten. Sie sind für die Entität weder lesbar noch schreibbar und dienen ausschließlich Energiebuchung und Beobachtung.

### 2.2 Primitive Quellen

Für v0.1 gelten folgende Quellenschlüssel:

```text
CONST       -> G
S-read      -> S
RAM-read(a) -> RAM[a]
```

Alle `CONST`-Instanzen derselben Entität verwenden den gemeinsamen abstrakten Quellenschlüssel `G`. Ihre Instanzidentität oder ihr konkreter Wert erzeugt keine zusätzliche Quelle. Dadurch kann eine bloße Vervielfachung von `CONST`-Instanzen die Quellensättigung nicht umgehen.

Jede RAM-Adresse ist eine eigene Umweltquelle. Wiederholte Lesevorgänge derselben Adresse behalten daher unabhängig von ihrem wechselnden Inhalt denselben Quellenschlüssel.

### 2.3 Verarbeitung

`ADD`, `SUB`, `XOR` und `EQ` vereinigen die Provenienzmengen aller verwendeten Eingangswerte. Die Verarbeitung erzeugt keine neue Quelle und entfernt keine vorhandene Quelle.

`Z-write` speichert neben dem sichtbaren Wert dessen unsichtbare Provenienz. `Z-read` gibt den gespeicherten Wert mit genau dieser Provenienz wieder aus. Wiederholtes Speichern, Lesen oder Kopieren erzeugt dadurch keine neue Quelle.

`RAM-write` schreibt den sichtbaren Wert und ergänzt die eigene Entity-ID zur bereits am Signal vorhandenen Urhebermenge. `RAM-read(a)` übernimmt diese Menge. Verarbeitung vereinigt Urhebermengen ebenso wie Quellenmengen und entfernt keine Einträge.

### 2.4 Energiebuchung eines Leseereignisses

Der Supervisor hält je Entität und RAM-Adresse den zuletzt gelesenen Wert sowie einen Zähler je Adress-Wert-Paar. Ein unveränderter Wert liefert `0`. Ein gegenüber dem letzten Lesen veränderter externer Wert liefert in v0.1:

```text
reward(k) = novelty_base / (1 + k)
```

Dabei ist `k` die Zahl früherer belohnter Wechsel derselben Entität zu demselben Wert an derselben Adresse. Enthält die Urhebermenge die lesende Entity-ID, ist der Ertrag ebenfalls `0`. Jeder Lesevorgang aktualisiert den zuletzt gesehenen Wert. `Z-write` speichert weiterhin Wert und Metadaten, erzeugt aber keine Energie.

## 3. Membran und reproduktive Konstellation

### 3.1 Logische Membranwerte

Für v0.1 besitzt jede Entität mindestens folgende logische Membranwerte:

```text
Offset 0 -> eigene Entity-ID    [nur lesbar]
Offset 1 -> Partner-IDs[2]      [zwei Slots]
```

Offset 1 kann eine oder zwei unterschiedliche fremde Entity-IDs enthalten. Leere Slots sind zulässig. Die eigene ID und eine doppelt eingetragene ID zählen nicht als zusätzliche Partner.

Die technische Abbildung der zwei logischen Slots auf RAM-Adressen wird getrennt spezifiziert. Sie verändert nicht die fachliche Bedeutung des Membranoffsets.

### 3.2 Gültige Elterngruppen

Eine belegte Partnerliste beschreibt nur eine Absicht der jeweiligen Entität. Eine Geburt kann erst entstehen, wenn alle beteiligten lebenden Entitäten dieselbe Gruppe vollständig und wechselseitig benennen.

Für zwei Eltern gilt:

```text
A nennt B
B nennt A
```

Für drei Eltern gilt:

```text
A nennt B und C
B nennt A und C
C nennt A und B
```

Einseitige, unvollständige oder voneinander abweichende Einträge bilden keine gültige reproduktive Konstellation. Der Supervisor wählt oder ergänzt keine Partner; er erkennt ausschließlich den von den Entitäten vollständig hervorgebrachten Zustand und prüft anschließend die weiteren formalen Geburtsbedingungen.

Damit unterstützt v0.1 reproduktive Konstellationen aus genau zwei oder genau drei Eltern.

### 3.3 Primitive Eigenmembran-Zugriffe

P0.1 ergänzt den primitiven Funktionssatz um zwei allgemeine Zugriffe auf die eigene Membran:

```text
MEM-read(offset, slot)         -> value
MEM-write(offset, slot, value) -> value
```

`MEM-read` liest ausschließlich aus der Membran der ausführenden Entität. `MEM-write` schreibt ausschließlich in deren eigene, für sie schreibbare Membranstellen. Die Operationen können weder eine fremde Membran verändern noch auf `G`, `K`, `Z` oder `S` zugreifen.

Für die Partnerliste gilt logisch:

```text
MEM-read(0, 0)             -> eigene Entity-ID
MEM-write(1, 0, partnerID) -> erster Partnerslot
MEM-write(1, 1, partnerID) -> zweiter Partnerslot
```

Ein Schreibversuch auf Offset 0 oder einen nicht vorhandenen beziehungsweise nicht schreibbaren Slot verändert keinen Zustand. Die genaue Fehler- und Kostenbehandlung ist Teil der noch festzulegenden P0.1-Ausführungsparameter.

Fremde Membranen können ausschließlich über ihre vom Supervisor freigegebenen Adressen im gemeinsamen Adressraum gelesen werden. P0.1 verwendet dafür einen von der eigentlichen RAM-Suppe getrennten virtuellen Bereich ab dem konfigurierten `membrane_base`. Je Entity-ID liegen dort drei skalare Zellen in stabiler Reihenfolge:

```text
membrane_base + (Entity-ID - 1) * 3 + 0 -> Offset 0, Entity-ID
membrane_base + (Entity-ID - 1) * 3 + 1 -> Offset 1, Partnerslot 0
membrane_base + (Entity-ID - 1) * 3 + 2 -> Offset 1, Partnerslot 1
```

`RAM-read` darf diese Zellen lesen. Eine Adresse im virtuellen Membranbereich, für die noch keine Entität existiert, liefert in P0.1 den Wert `0` mit einer stabilen, sättigbaren `MEM_VOID`-Provenienz. `RAM-write` darf keine Adresse dieses Bereichs verändern; Schreibzugriff auf die eigene Partnerliste erfolgt ausschließlich über `MEM-write`. Der virtuelle Membranbereich verkleinert oder verschiebt die RAM-Suppe nicht. Ob und wie eine Entität solche Adressen findet und welche IDs sie in ihre eigene Partnerliste schreibt, ergibt sich aus ihrem P-Netz und der gemeinsamen Umwelt. Der Supervisor liefert keine Partnerauswahl.

`MEM-read` und `MEM-write` sind keine Reproduktionsbefehle. Sie stellen lediglich einen allgemeinen primitiven Zugriff auf die eigene kontrollierte Außenschnittstelle bereit. Erst die vollständig wechselseitige Belegung gemäß Abschnitt 3.2 bildet eine reproduktive Konstellation.

### 3.4 Verbrauch der Partnerlisten

Nach einer erfolgreich ausgeführten Geburt leert der Supervisor beide Partnerslots aller beteiligten Eltern. Die reproduktive Konstellation ist damit verbraucht. Eine weitere Geburt derselben Gruppe erfordert, dass sämtliche Beteiligten ihre vollständigen wechselseitigen Einträge erneut durch Ausführung ihrer P-Netze herstellen.

Bei einer ungültigen oder unvollständigen Konstellation werden keine Slots geleert. Auch wenn eine formal vollständige Gruppe eine weitere Geburtsbedingung, insbesondere den erforderlichen Energiebeitrag, nicht erfüllt, findet keine Geburt statt und der Supervisor verändert ihre Partnerlisten nicht.

### 3.5 Geburtsenergie und Elternbeiträge

P0.1 verwendet eine feste, in der Versuchskonfiguration dokumentierte Geburtsenergie `S_birth`.

```text
Beitrag je Elternteil = S_birth / Anzahl der Eltern
```

Bei zwei Eltern trägt jeder Elternteil die Hälfte, bei drei Eltern jeder ein Drittel. Eine Geburt findet nur statt, wenn jedes Mitglied der gültigen Gruppe seinen vollständigen Anteil bezahlen kann. Teilzahlungen, Ausgleichszahlungen eines anderen Elternteils und ein Energiezuschuss des Supervisors sind ausgeschlossen.

Bei erfolgreicher Geburt zieht der Supervisor die Beiträge ab und weist dem Kind exakt deren Summe als Startenergie zu. Die Energiebilanz der Reproduktion ist damit nullsummig.

Jede Entität bewahrt zusätzlich den Energiewert `S₀`, mit dem sie selbst geboren wurde. Eine Geburt ist nur zulässig, wenn für jeden einzelnen Elternteil strikt gilt:

```text
S_nach_Beitrag > S₀
```

Die bloße Startenergie kann damit keine Fortpflanzung finanzieren. Nur ein während des eigenen Lebens erwirtschafteter Überschuss darf an ein Kind übertragen werden. Scheitert diese Prüfung, wird keine Energie abgezogen, kein Kind erzeugt und keine Partnerliste geleert.

Scheitert die Energieprüfung, wird keine Energie abgezogen, kein Kind erzeugt und keine Partnerliste geleert. `S_birth` ist in P0.1 ein austauschbarer Versuchsparameter und kein erbliches Merkmal oder allgemeines Naturgesetz.

## 4. Vererbung und Mutation

### 4.1 Vererbung von `A₀`

Der singuläre erbliche Basisaktivitätswert `A₀` wird nicht gemittelt oder aus mehreren Elternwerten zusammengesetzt. Das Kind zieht den vollständigen Wert genau eines beteiligten Elternteils mit Gleichverteilung:

```text
zwei Eltern -> jeder Elternwert mit Wahrscheinlichkeit 1/2
drei Eltern -> jeder Elternwert mit Wahrscheinlichkeit 1/3
```

Der gezogene Wert wird zunächst unverändert übernommen. Erst die nach der Rekombination stattfindende seltene Mutation darf ihn gegebenenfalls verändern. Die Auswahl verwendet ausschließlich den dokumentierten Zufallsstrom des Experimentkerns.

### 4.2 Größenmaße

P0.1 verwendet die im Grundkonzept getrennten Größen:

```text
Nₚ = |P|
N_G = |F| + |P|
```

Der Aktivitätsfaktor verwendet `Nₚ`. Zielgröße, Fragmentumfang und die Obergrenze eines Kindergenoms verwenden `N_G`. Für jede Geburt gilt:

```text
N_G(Kind) <= Summe N_G(Eltern)
```

`A₀` und weitere genau einmal vorhandene Metadaten zählen nicht zu `N_G`.

### 4.3 Zielgröße des Kindergenoms

Für jede Geburt wählt der Experimentkern zunächst einen beteiligten Elternteil gleichverteilt aus. Die genetische Zielgröße des Kindes wird aus einer Normalverteilung um `N_G` dieses Elternteils gezogen. Die Standardabweichung ist ein dokumentierter P0.1-Konfigurationsparameter.

Der gezogene Wert wird auf eine ganze Zahl gerundet und begrenzt:

```text
1 <= N_G_Ziel(Kind) <= Summe N_G(Eltern)
```

Bei unterschiedlich großen Eltern entstehen dadurch mehrere elterliche Attraktoren statt einer automatischen Bevorzugung ihres arithmetischen Mittels.

### 4.4 Fragmentziehung

Die realen Genome aller beteiligten Eltern bilden für diese Geburt einen gemeinsamen Pool. Für ein Fragment wird eine darin noch nicht gezogene Funktionspunkt-Instanz als Startpunkt gewählt. Von dort wächst der Instanzensatz semantikfrei zufällig entlang real vorhandener ein- oder ausgehender Kanten zu ebenfalls noch nicht gezogenen Instanzen. Er bleibt zu jedem Zeitpunkt zusammenhängend.

Zu einem Fragment gehören anschließend alle elterlichen `P`-Kanten, deren beide Endpunkte im gezogenen Instanzensatz liegen. Dadurch bleibt die intern tatsächlich vorhandene Teilstruktur vollständig erhalten; der Supervisor wählt keine vermeintlich nützlichen Einzelkanten aus.

Nach Übernahme eines Fragments werden seine Instanzen und internen Kanten für diese Geburt aus dem Elternpool entfernt. Die Ziehung erfolgt damit ohne Zurücklegen. Weitere Fragmente werden gezogen, solange mindestens ein Fragment in die noch freie genetische Zielgröße passt. Ein Fragment, dessen `N_G` die verbleibende Zielgröße überschreitet, wird nicht zerschnitten, sondern verworfen und neu gezogen. Kann kein zulässiges Fragment mehr gebildet werden, darf das Kind unter seiner Zielgröße bleiben.

Jede Ziehung beginnt an einer realen Instanz. Mehrfach vorhandene Netzstrukturen besitzen dadurch entsprechend mehr mögliche Startpunkte und Wachstumspfade; ihre reale Kopienzahl wirkt ohne gesondertes Gewichtungsfeld auf die Vererbungswahrscheinlichkeit.

### 4.5 Montage des Kindergenoms

Gezogene Fragmente werden mit neuen, nur innerhalb des Kindergenoms eindeutigen Instanz-IDs kopiert. Kanten innerhalb eines Fragments werden auf diese neuen IDs abgebildet.

Die Fragmente werden als disjunkte Netzkomponenten in das Kindergenom übernommen. Der Supervisor erzeugt keine zusätzlichen Kanten zwischen ihnen und versucht nicht, ihre Funktionen zu erkennen oder sie sinnvoll zu verbinden. Eine spätere Verbindung oder Umgestaltung kann nur aus der seltenen Mutation oder aus künftigen, ausdrücklich beschlossenen Mechanismen entstehen.

### 4.6 Seltene lokale Mutation

P0.1 verwendet eine konfigurierbare Mutationswahrscheinlichkeit je Kind mit folgendem Standardwert:

```text
p_mut = 0,001
```

Die Mutationsprüfung findet nach Rekombination und Montage des Kindergenoms statt. Tritt keine Mutation ein, bleibt das montierte Genom unverändert. Tritt sie ein, wird genau eine der für das konkrete Genom anwendbaren Mutationsklassen gleichverteilt gewählt:

1. **Instanzmutation:** Eine Funktionspunkt-Instanz wechselt zu einem zufälligen primitiven Typ mit kompatibler Portsignatur. Bei einer `CONST`-Instanz darf stattdessen ihr erblicher Wert verändert werden.
2. **Kantenmutation:** Genau ein Endpunkt einer vorhandenen Kante wird auf einen zufälligen kompatiblen Port umgelegt. Das neue Ziel darf in einem anderen geerbten Fragment liegen und dadurch erstmals zwei Komponenten verbinden.
3. **Aktivitätsmutation:** `A₀` wird um genau `-1` oder `+1` verändert, ohne den für P0.1 zulässigen Mindestwert zu unterschreiten.

Pro Geburt findet höchstens eine Mutation statt. P0.1 besitzt keine gesonderte Einfüge-, Lösch-, Duplikations- oder Kaskadenmutation. Die reguläre Versuchskonfiguration verwendet den Standardwert; Tests dürfen `p_mut` gezielt überschreiben, damit alle Mutationspfade reproduzierbar geprüft werden können.

## 5. Standardkonfiguration des Demonstrationslaufs

Die folgenden Werte sind austauschbare P0.1-Versuchsparameter und keine Naturgesetze:

```text
Werttyp                 signed 64-bit, Wrap-around
RAM-Suppe               65.536 Zellen
Z                       64 Zellen je Entität
Adressierung             Modulo der jeweiligen Speichergröße
membrane_base           1.000.000

A₀ Mindestwert          1
F(Nₚ)                   1 / sqrt(max(1, Nₚ))
A_ist                    max(1, floor(A₀ * F(Nₚ))), durch S begrenzt

Standbykosten           1,0 Energie je Heartbeat
Funktionsausführung     1,0 Energie
Kantenübertragung       0,1 Energie je übertragener Kante

S_birth                 50,0 Energie
Neuheitsbasis           10,0 Energie
reward(k)               10 / (1+k) je erneutem Wechsel zu (Adresse, Wert)
p_mut                   0,001 je Kind
```

Ein Heartbeat bucht zuerst den Standbyverbrauch ab. Entitäten, die ihn nicht bezahlen können, sterben vor ihrer Ausführung. Die übrigen Entitäten werden in stabiler Entity-ID-Reihenfolge ausgeführt; die Auswahl bereiter Funktionspunkte erfolgt ausschließlich über den Seed-Zufallsstrom. Anschließend prüft der Supervisor reproduktive Konstellationen, führt mögliche Geburten aus und erzeugt Beobachtungsdaten. Reale Laufzeit hat keinen Einfluss auf diese Reihenfolge.

Population 0 des mitgelieferten Standardlaufs ist eine ausdrücklich gekennzeichnete technische Demonstrationspopulation. Sie dient dem Nachweis von Datenfluss, `Z-write`, Membranzugriff und Geburt und ist kein wissenschaftlicher Versuchsaufbau oder Ergebnis.
