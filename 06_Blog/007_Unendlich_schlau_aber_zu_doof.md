# Unendlich schlau, aber zu doof es anzuwenden

Status: Gesprächsentwurf

Redaktionelle Einordnung: Der Beitrag dokumentiert Designentscheidungen, offene Architekturfragen und Gedankenmodelle vor der Implementierung von Prototyp 0. Noch wurde keine EVE-Entität erzeugt und keines der beschriebenen Verhaltensmodelle praktisch beobachtet.

*29. August 2026. Eigentlich wollten wir nur klären, wann wir beim Privacy-Team nachhaken. Dann stellen wir fest, dass Stefan auf dem Handy mit Nova frei herumspinnen und Nova-EVE anschließend den entstandenen Gedankensalat dokumentieren kann. Wenige Nachrichten später liegt Prototyp 0 auf dem virtuellen Küchentisch.*

**Stefan:** Da wir jetzt schon so lange herumgesabbelt haben, würde ich als Nächstes wohl am liebsten am Prototypen anfangen wollen.

**Nova:** Unbedingt. Aber nicht sofort mit Code. Sonst bauen wir aus Versehen schon wieder das System, von dem wir glauben, dass EVE es braucht.

Für P0 sollten wir zuerst eine einzige Welt, einen Agententyp und eine Form von Erkenntnis festlegen. Danach kann Nova-EVE daraus eine technische Spezifikation machen.

**Stefan:** Tja, wie sollen wir das angehen?

**Nova:** Fangen wir mit der Welt an. Davon hängt fast alles andere ab.

## Das Irgendwo ist die Welt

**Stefan:** Ich denke, wir müssen die Welt zusammen mit unseren Viechern definieren. Was soll das digitale Einzellerlein genau sein? In der Basis ist es ein Prozess, der irgendwo läuft. Das Irgendwo ist dabei die Welt.

**Nova:** Das gefällt mir besser als eine künstliche Rasterwelt. Dann simulieren wir nicht unbedingt eine Welt *innerhalb* des Rechners. Der Rechner selbst ist die Welt.

Der Einzeller wäre zunächst ein laufender Prozess mit eigenem Zustand, begrenzten Ressourcen und wenigen möglichen Kontakten nach außen. Er existiert in einer Linux-Umgebung: mit CPU-Zeit, RAM, Dateien, anderen Prozessen und vielleicht irgendwann Geräten oder Netzwerk.

**Stefan:** Temperatur, Organismen sowie räumliche Grenzen gibt es in dem Sinne ja gar nicht.

**Nova:** Genau. Da bin ich gedanklich schon wieder in Richtung „Biologie nachbauen“ abgebogen.

Wir brauchen keine digitale Entsprechung von Temperatur, Raum oder Nahrung. Unsere Welt besitzt CPU-Zeit, Speicher, Prozesse, Dateien und Berechtigungen, weil diese Dinge dort tatsächlich existieren – nicht weil RAM das digitale Äquivalent einer Wiese sein soll.

**Stefan:** Unsere Welt sollte zunächst einfach eine Linux-Mint-VM sein. Dort läuft ein Prozess und macht etwas. Natürlich müssen wir das orchestrieren können, um zum Beispiel hundert Prozesse zu starten und ihren Status zu sehen.

**Nova:** Dann haben wir drei Ebenen:

```text
Linux-Mint-VM = Welt
│
├── Supervisor = Versuchsleiter
│
└── viele eigenständige Prozesse = Population
```

Die Population sollte tatsächlich aus eigenständigen Prozessen bestehen, nicht bloß aus hundert Objekten in einem Simulator. Wenn Prozess 37 abstürzt, ist Nummer 37 weg. Wenn er CPU-Zeit oder RAM braucht, verbraucht er reale Ressourcen seiner Welt.

Der Supervisor darf Population 0 starten, zählen, beobachten, protokollieren und das Experiment notfalls beenden. Er kennt womöglich PID, Energie, Alter und Abstammung. Aber dieses Beobachterwissen darf nicht automatisch Wissen der Viecher werden. Der Supervisor ist unser Mikroskop.

> **Redaktionelle Einordnung – Designentscheidung:** P0 soll in einer abgeschotteten Linux-Mint-VM laufen. Die reale digitale Ausführungsumgebung bildet die Welt. Der Supervisor beobachtet von außen; seine Informationen gehören nicht automatisch zur wahrnehmbaren Umwelt der Population.

## Sehr nah an einem Virus

Kaum steht die erste grobe Architektur, führt die geplante Reproduktion zu einer unangenehmen, aber notwendigen Nebenfrage.

**Stefan:** Was mich beschäftigt: Mit den Agenten sind wir aus Entwicklungs- und Cybersecurity-Sicht sehr nah an einem Virus. Schließlich streben wir sich selbst erweiternde und replizierende Prozesse an.

**Nova:** Das ist keine nebensächliche Ähnlichkeit. Ein selbstreplizierendes Programm ist zwar nicht automatisch ein Virus. Wenn es kein Wirtsprogramm infiziert, wäre „Wurm“ technisch näher. Für die Schutzplanung ist die genaue Schublade aber fast zweitrangig.

Wir bauen absichtlich eine Kette wie:

`verändern → ausführen → bewerten → replizieren → erneut verändern`

Die Mint-VM muss deshalb ab P0 als potenziell kompromittiert gelten. Keine persönlichen Daten, keine SSH-Schlüssel, keine eingebundenen Host-Verzeichnisse, keine Zugangsdaten und keine lustigen Abkürzungen aus dem Gefängnis.

Vor allem gilt:

> Evolution darf niemals ihre eigene Sicherheitsgrenze kontrollieren.

**Nova:** Vielleicht sollte der Supervisor nach Population 0 auch keine Nachkommen mehr erzeugen. Reproduktion müsste eine Fähigkeit der Organismen sein.

**Stefan:** Reproduktion ist nicht Sache des Supervisors. Korrekt. Er kann nur den initialen Stand starten und den weiteren Stand beobachten.

**Nova:** Genau. Wenn der Supervisor bei „genug Energie“ einfach einen neuen Prozess erzeugt, hätten nicht die Viecher reproduziert. Unser Versuchsaufbau hätte nach einer Regel neue Instanzen erzeugt.

Technisch braucht das Betriebssystem trotzdem einen geschützten Mechanismus, der einen neuen Prozess startet.

**Stefan:** Naja, okay. Das Merkmal kann ja vom Supervisor ausgewertet werden und er startet dann den entsprechenden Dienst.

**Nova:** Ja – dann trennen wir Ursache und Ausführung. Die Viecher erzeugen den reproduktiven Zustand, ihre Beteiligung und die genetischen Daten. Die geschützte Komponente prüft nur formale Bedingungen und startet den neuen Prozess.

Geburtskanal, nicht Züchter.

> **Redaktionelle Einordnung – Designentscheidung:** Der reproduktive Impuls und die vererbten Inhalte müssen aus den Entitäten kommen. Eine nicht evolvierbare Außenschicht darf das entstandene Ereignis technisch ausführen.

## Erst einmal nur: Da ist etwas

Mit Welt und Supervisor halbwegs sortiert, bleibt die Frage, wie die laufenden Prozesse heißen sollen.

**Stefan:** Irgendwie stoße ich mich noch an „Organismus“. Es beschreibt ziemlich klar, was wir unter den Prozessen in einer organischen Umgebung verstehen, aber sie sind ja eben nicht organisch.

**Nova:** „Agent“ ist kaum besser. Das klingt bereits nach Zielen, Entscheidungen und Handlungsfähigkeit. Wie wäre **Entität**?

Eine EVE-Entität wäre zunächst nur eine eigenständige laufende Prozesseinheit mit veränderlichem Zustand und vererbbaren Eigenschaften. Sie muss nicht intelligent, autonom, zielgerichtet oder lebendig sein.

Formal also Entität. Technisch Prozess. Insgesamt Population. Und im Log weiterhin Viech, Einzellerlein und kleiner Sack.

**Stefan:** Entität finde ich tatsächlich nach deiner Ausführung sehr gelungen und passend.

## Was besitzt Entität 0001 beim Start?

**Stefan:** Wir haben, glaube ich, definiert, dass wir ein Genom haben, eine kleine Schnittstelle nach außen und `S` als Energie.

**Nova:** Zusätzlich brauchen wir einen internen Zustand `Z`. Sonst kann eine vorherige Interaktion keinen Einfluss auf die nächste haben.

Damit hätten wir zunächst:

```text
G = Genom, vererbbar
Z = interner Zustand, während der Existenz erworben
S = Energie, gewonnen und verbraucht
```

Die kleine Schnittstelle nach außen gehört nicht in die Entität. Sie ist Teil der Welt und bestimmt, was eine Entität überhaupt wahrnehmen oder bewirken kann.

**Stefan:** Okay. Lass uns die Schnittstelle erst einmal beiseitelegen und mit dem Genom anfangen. Wie definieren wir es, was wird Bestandteil und wie?

## Der erste Genom-Entwurf: eine winzige Maschine

**Nova:** Mein erster Gedanke wäre eine endliche Bytefolge, die vererbt, kombiniert und mutiert wird. Eine für alle gleiche Runtime interpretiert diese Bytes.

Dann könnte das Genom ein kleines Programm für eine primitive Maschine sein: mit Strukturinformation, Daten und vielleicht Befehlen wie `LOAD`, `STORE`, `ADD`, `SUB`, `XOR`, Vergleichen und Sprüngen.

Mutation wäre technisch elegant. Ein Byte ändert sich, ein Abschnitt verschwindet, etwas wird eingefügt oder dupliziert. Selbst die Genomlänge könnte wachsen und schrumpfen.

Aber eine Mini-CPU schenkt den Entitäten bereits einen zentralen Kontrollfluss, Register, adressierbaren Speicher, Schleifen und Verzweigungen.

**Stefan:** Bei dem Ansatz mit der Runtime sehe ich genau das Problem: Über sie haben wir wieder vordefinierte Aktionen, die dann einfach passieren. `LOAD` könnte etwas sein, was sich erst aus mehreren Einzellern entwickelt, die auf einmal eine mehrzellige Entität bilden.

**Nova:** Ja. Das ist eine wichtige Kurskorrektur.

Wenn `LOAD` elementar ist, haben wir bereits festgelegt, dass eine einzelne Entität adressierbaren Speicher lesen kann. Vielleicht sollte diese Fähigkeit erst aus mehreren einfacheren Strukturen entstehen. Dann ist das Genom kein Programm für eine Mini-CPU, sondern zunächst nur eine vererbbare Anfangsstruktur.

> `G` beschreibt nicht, was eine Entität tut. `G` beschreibt, wie sie zu Beginn beschaffen ist.

Was sie tut, entsteht erst, wenn diese Struktur unter den Regeln der EVE-Welt wirkt.

Damit brauchen wir unterhalb des Genoms trotzdem etwas Unveränderliches. Irgendwo muss unsere digitale Physik anfangen. Die Frage ist nicht mehr, welche Befehle wir bereitstellen, sondern welche möglichst wenigen elementaren Wechselwirkungen überhaupt Dynamik erzeugen können.

> **Redaktionelle Einordnung – Kurskorrektur:** Das frühere Bild eines Bytecode-Programms wird nicht als Architektur übernommen. Selbst scheinbar primitive Befehle könnten Fähigkeiten vorwegnehmen, deren Emergenz EVE untersuchen soll.

## Das Genom wird zum Parameterbeutel

Nach dem Abschied vom fertigen Programm präzisiert Stefan, was er unter dem Genom eigentlich versteht.

**Stefan:** Ich sehe das Genom als eine Art Basis-Parameterset, das der Entität von Anfang an zur Verfügung steht. Diese Parameter werden von den Eltern vererbt.

Zwei Eltern haben zum Beispiel jeweils 100 Parameter, zusammen also 200. Davon wird eine Auswahl an den Nachkommen weitergegeben. Ein Parameter darf x-mal im Genom vorkommen und hat damit eine x-fach höhere Chance, vererbt zu werden.

Eine Entität kann auch nur einen Parameter haben, den aber hundertmal. Dann stirbt sie vermutlich aus.

**Nova:** Ah. Dann vererben wir gar keinen klassischen Programmcode, sondern einen Beutel elementarer Parameter.

Die Kopienzahl ist bereits die Gewichtung. Wenn `P17` vierzigmal im gemeinsamen Elternpool liegt, wird es wahrscheinlicher weitergegeben als `P83`, das nur einmal vorkommt. Den Extremfall aus hundert identischen Parametern verbieten wir nicht. Vielleicht ist er genial spezialisiert, vielleicht sofort lebensunfähig. Das entscheidet die Umwelt.

Mutation brauchen wir trotzdem. Sonst kann nur erhalten bleiben, was bereits in Population 0 vorhanden war. Sie muss gelegentlich einen gezogenen Parameter verändern und dadurch etwas Neues in den Genpool bringen.

**Stefan:** Die Anzahl der Parameter darf aber weder fix noch unendlich sein. Ein Genom sollte im Laufe der Evolution wachsen dürfen. Das Kind kann ein größeres, kleineres oder gleich großes Genom haben.

Bei gleich großen Eltern ist dieselbe Größe wahrscheinlicher. Bei ungleichen Eltern sollte das Kind eher die kleine oder die große Genomgröße erben. Andere Abweichungen sind möglich, aber seltener.

**Nova:** Dann ist die Genomlänge selbst ein vererbbares Merkmal. Bei 100 und 100 läge der häufigste Wert wieder um 100. Bei 60 und 140 sollten wir nicht automatisch den Mittelwert 100 bevorzugen; beide Eltern wären eigene Attraktoren.

**Stefan:** Ist der Herr Gauß da nicht ein gutes Beispiel?

**Nova:** Ja. Bei gleich großen Eltern praktisch eine Normalverteilung um dieselbe Größe. Bei 60 und 140 könnte eine Mischung aus zwei Gaußkurven entstehen – je ein Gipfel in der Nähe eines Elternteils. Bei 100 und 102 überlappen sie fast wieder zu einem einzigen Gipfel.

**Stefan:** Wir haben ja außerdem den Zufallsfaktor, unsere Mutation. Das Kind kann niemals mehr Genomplätze haben als beide Eltern zusammen. Die maximale Varianz sollte die Summe der Eltern nicht überschreiten können.

**Nova:** Dann können wir drei Mechanismen sauber trennen:

```text
Genomgröße
→ bestimmt die Zahl der Plätze des Kindes

Genominhalt
→ wird aus dem realen Elternpool ohne Zurücklegen gezogen

Mutation
→ verändert anschließend einzelne vererbte Parameter
```

Bei Eltern mit 60 und 140 Parametern liegt die absolute Obergrenze für dieses Kind bei 200. Wachstum bleibt über Generationen möglich, weil große Nachkommen später gemeinsam einen größeren Pool bilden können.

**Stefan:** Die Variabilität der Genomgröße könnte selbst im Genom festgeschrieben sein. Sie steigt über die Zeit, wenn Eltern mit unterschiedlichen Größen erfolgreich zusammenkommen, und sinkt, wenn die Größen nahe beieinanderliegen. Das wäre ein fixer vererblicher Parameter.

**Nova:** Dann nennen wir ihn vorläufig `Vg`. „Fix“ heißt: Jede Entität besitzt genau dieses eine Metadatum; es kann nicht verschwinden oder hundertfach vorkommen. Sein Wert ist aber vererbbar und veränderlich.

Eine Linie würde damit ihre historische Toleranz für unterschiedliche Genomgrößen mit sich tragen. Das ist reizvoll – aber die konkrete Dynamik lassen wir offen.

> **Redaktionelle Einordnung – teilweise entschieden:** Variable Genomgröße, gemeinsamer Elternpool, Häufigkeitsgewichtung und Ziehen ohne Zurücklegen bilden die gegenwärtige Grundrichtung. Gauß-Mischung und `Vg` bleiben mathematisch offene Modelle.

## Was ist ein einzelnes P?

Erst nachdem die Vererbung als Mechanik halbwegs steht, kehrt das Gespräch zur unangenehmeren Frage zurück: Was wird da eigentlich vererbt?

**Stefan:** Ich stelle mir `P` ungefähr wie eine Sammlung von Command-Line-Switches vor. Die Parameter sind Dinge, die ein Prozess von Natur aus kann oder die ihn definieren.

Das könnte in einer Art Instinkt münden: Ich habe keinen Plan, warum genau, aber da ist etwas in meinem Ranzen, das mir sagt: trink.

**Nova:** Dann ist `P` keine vollständige Aktion und kein fertiges Programm, sondern eine angeborene Disposition.

Wir dürfen nur keinen Parameter `P_TRINK`, `P_FIND_PARTNER` oder `P_EXPLORE` definieren. Das wäre das gewünschte Verhalten bereits durch die Hintertür. Ein einzelnes `P` muss viel elementarer sein. Erst viele Parameter zusammen könnten einen Zustandsübergang hervorbringen, den wir von außen irgendwann als Instinkt bezeichnen.

**Stefan:** Je häufiger `P`, umso höher dessen Einfluss. Prozentual ausgerichtet an der Genomgröße.

**Nova:** Genau. Nicht die absolute Kopienzahl allein, sondern der Anteil:

`A(Px) = Anzahl(Px) / Genomgröße`

Zwanzig Kopien in einem Genom mit hundert Plätzen und hundert Kopien in einem Genom mit fünfhundert Plätzen ergeben beide zwanzig Prozent Ausprägung.

Das hat eine interessante Nebenwirkung. Wenn ein Genom schrumpft, können die verbliebenen Parameter stärker werden, ohne selbst mutiert zu sein:

```text
40 × P1, 30 × P2, 30 × P3  → P1 = 40 %
40 × P1, 10 × P2, 10 × P3  → P1 = 66,7 %
```

**Nova:** Jetzt müssen wir entscheiden, was solche Dispositionen beeinflussen dürfen. Internen Zustand? Eingänge? Ausgänge?

**Stefan:** Hm. Eigentlich streng genommen … alle?

**Nova:** Ja. Alles Veränderbare innerhalb der Entität – aber nicht Linux, Supervisor, Sicherheitsgrenze oder die Grundphysik selbst.

Damit lautet die Übersetzung, die uns noch fehlt:

`Genom P[] → ??? → laufende Entität`

## Das Henne-Ei-Problem des doofen Prozesses

**Stefan:** Dazu habe ich aktuell genau gar keine Idee. Wir müssen Brainstorming machen.

**Nova:** Dann werfen wir verschiedene Formen für `P` an die Wand:

- eine universelle Zahl, deren Wirkung erst aus Position und Kombination entsteht;
- eine Beziehung: Quelle beeinflusst Ziel mit Stärke C;
- eine Verbindung in einem dynamischen Zustandsnetz;
- eine reaktionsartige Regel: Wenn A und B vorhanden sind, verändere C;
- später vielleicht ein Parameter, der die Wirksamkeit anderer Parameter reguliert.

Mein Lieblingsgedanke ist momentan `P` als Beziehung. Viele bedeutungsarme Beziehungen könnten ein Netz bilden, in dem Speicher, Signale oder Reaktionen erst durch Zusammenspiel entstehen.

**Stefan:** Naja, ich schnalle im Moment noch nicht, wie ein Prozess, der erst mal doof ist, das verarbeiten soll.

**Nova:** Genau. Da sitzt das Henne-Ei-Problem.

Ein Linux-Prozess kann mit `[17, 42, 42, 8, 193]` exakt nichts anfangen. Irgendeine unveränderliche Regel muss festlegen, wie diese Werte wirken. Vollkommen doof geht nicht.

Die entscheidende Frage ist deshalb nicht: Wie vermeiden wir jede vorgegebene Funktion? Das ist unmöglich.

Sondern:

> Was ist die kleinstmögliche Grundmechanik, die `P` Wirkung gibt, ohne bereits komplexes Verhalten vorzugeben?

Die Runtime darf sagen: „So wirkt ein `P`.“ Sie sollte möglichst nicht sagen: „So liest du eine Datei, findest einen Partner, sendest eine Nachricht oder speicherst Wissen.“

Der Prozess versteht sein Genom nicht. Er wendet nur eine universelle primitive Regel darauf an – so wie eine CPU nicht versteht, was Firefox ist.

## Angeboren trifft erworben

An dieser Stelle verbindet Stefan das Genom wieder mit dem zu Beginn eingeführten internen Zustand.

**Stefan:** Unser Genom ist quasi das Basisset an Parametern, welche der Prozess für den Aufruf von Instruktionen verwenden kann. Die Rückgabewerte können dann im Speicher abgelegt werden und gegebenenfalls als weitere Parameter dienen, die eben nicht schon im Genom vererbt wurden.

**Nova:** Das ergibt eine saubere Trennung:

```text
G = vererbte Basisparameter
Z = Laufzeitspeicher

Parameter aus G
      ↓
primitive Wirkung
      ↓
Rückgabewert
      ↓
Speicher Z
      ↓
wird später selbst Parameter
```

Damit kann eine Entität während ihrer Existenz Werte erwerben, die nicht im Genom standen. Wenn ein gespeicherter Rückgabewert später erneut verwendet wird, beeinflusst Vergangenes zukünftiges Verhalten.

`G` sagt: „So bist du gestartet.“

`Z` sagt: „Das ist dir inzwischen passiert.“

Wir haben dadurch noch kein Lernen eingebaut. Aber wir schaffen eine Voraussetzung, unter der wir später vielleicht funktional lernähnliches Verhalten beobachten können.

**Nova:** Der nächste Knackpunkt bleibt allerdings: Wie entscheidet der doofe Prozess, welche primitive Wirkung er als Nächstes mit welchen Parametern hervorbringt? Sobald wir `READ → COMPARE → STORE → OUTPUT` fest hinschreiben, haben wir ihm wieder einen Ablauf gegeben.

**Stefan:** Bevor wir uns um das Wie kümmern: das Warum. Wegen Energie.

## Existenz kostet – aber warum handeln?

**Stefan:** Startenergie und Standbyverbrauch können vererbbar sein und sich mit dem Genom entwickeln. Beim Verbrauch würde ich nach Ticks oder Heartbeats abrechnen. Das Ausführen von Instruktionen kostet abhängig von deren Komplexität, also abhängig von den Parametern.

**Nova:** Dann entsteht als vorläufiges Denkmodell:

```text
S_neu = S_alt
        - Standby
        - Kosten(Wirkung, beteiligte Parameter)
        + möglicher Energiegewinn
```

Nichtstun ist also nicht kostenlos. Eine Entität muss auf Dauer Energie beschaffen, um weiter zu existieren.

Die Startenergie eines Kindes darf aber nicht genetisch aus dem Nichts entstehen. Sonst mutiert die Population einfach `S0 = 999999999999` und entdeckt: viel Geld ist besser als wenig Geld.

**Nova:** Wie wir für reguläre Reproduktion bereits festgehalten haben, muss diese Energie aus der Welt bilanziert werden, grundsätzlich als Beitrag der Eltern. Damit wird eine hohe Startenergie zur Investition: bessere Anfangschancen für das Kind, aber höhere Kosten für die Eltern.

Beim Standbywert vermute ich zunächst, dass Evolution ihn einfach auf null optimieren würde.

**Stefan:** Standbyverbrauch null ist tot.

**Nova:** Ah! Ja. Dann ist Null keine besonders effiziente Strategie, sondern Ende Gelände.

Der Standbyverbrauch ist der Heartbeat des Lebensmodells. Solange die Entität existiert, muss sie ihren genetisch geprägten Grundumsatz bezahlen. Kann sie den nächsten Tick nicht finanzieren, stirbt sie.

**Stefan:** Welche Auswirkung hat aber ein niedriger Standbyverbrauch im Vergleich zu einem hohen? Vielleicht lässt sich das an die Genomgröße binden.

**Nova:** Vielleicht bestimmt der Standbywert, wie viel des Genoms pro Heartbeat überhaupt wirksam werden kann.

Ein kleines Genom mit niedrigem Standby wäre sparsam und könnte relativ viel seiner wenigen Parameter aktivieren. Ein großes Genom mit niedrigem Standby hätte viel Potenzial, bräuchte aber lange, um davon etwas wirksam werden zu lassen. Ein großes Genom mit hohem Standby könnte viel gleichzeitig tun, müsste dafür aber entsprechend viel Energie finden.

Als reines Denkmodell:

`Aktivierungsgrad ≈ Standby / Genomgröße`

Nicht als beschlossene Formel.

**Stefan:** Hahaha. Unendlich schlau, aber zu doof es anzuwenden.

**Nova:** Die erste EVE-Lebensform mit Doktortitel und 4.000 Millisekunden Ping zum eigenen Gehirn.

Riesiges Genom, winziger Grundumsatz. Das Viech trägt den Brockhaus im Ranzen und schafft pro Heartbeat drei Wörter:

> „Moment … ich hab da was … gib mir 700 Ticks.“

Und andersherum ein winziges Genom mit hohem Grundumsatz: Kann drei Dinge, aber **DIE MACHT ES JETZT SOFORT.**

> **Redaktionelle Einordnung – Gedankenmodell:** Der Trade-off zwischen Genomgröße, Standbyverbrauch und genetischer Aktivität wurde konzeptionell bejaht. Seine mathematische Abbildung ist offen.

## Standby erklärt die Konsequenz, nicht den Impuls

Für einen Moment scheint das energetische Warum gefunden: Existieren kostet, also muss die Entität handeln. Stefan bemerkt jedoch die Lücke.

**Stefan:** Okay, aber damit beschreiben wir die Rahmenbedingungen für das Warum. Nicht das Warum selbst.

**Nova:** Völlig richtig. Wir haben erklärt, warum bestimmte Strategien energetisch erfolgreicher wären. Noch nicht, warum der kleine Sack überhaupt die erste Wirkung hervorbringen sollte.

Die Welt zieht pro Heartbeat Energie ab. Aber daraus entsteht kein Handlungsimpuls. Ein frisch gestarteter Prozess könnte vollkommen korrekt herumstehen, Energie verbrauchen und sterben. Das wäre übrigens ein legitimer P0-Ausgang.

Vielleicht erzeugt `P` selbst Aktivierungsdruck. Ein Parameter ist vorhanden und drängt entsprechend seinem Anteil am Genom dazu, irgendwie wirksam zu werden. Dann handelt die Entität nicht, weil sie überleben möchte. Sie handelt, weil ihr Genom Aktivität hervorruft. Energie entscheidet lediglich, welche Formen dieses Drangs evolutionär fortbestehen.

**Stefan:** Ich denke schon, dass sie „Hunger“ haben muss.

## Weil sie Hunger hat

**Nova:** Ja. Hunger darf vorhanden sein – wir dürfen ihm nur nicht erklären, was er dagegen tun soll.

Er ist kein `suche_nahrung()` und kein eingebauter Plan. Er ist ein interner Zustand: „Da stimmt etwas nicht. Tu irgendwas.“

Und vermutlich darf er nicht nur vom absoluten Energievorrat abhängen. Eine Entität mit `S = 1000` und einem Verbrauch von 500 pro Tick steht kurz vorm Verhungern. Eine andere mit denselben 1000 und einem Verbrauch von 0,1 kann sich noch gemütlich hinlegen.

Hunger müsste eher die energetische Reichweite ausdrücken:

`Reichweite = Energie / erwarteter Verbrauch pro Heartbeat`

Wenn Hunger steigt, könnten genetische Dispositionen primitive Wirkungen hervorbringen. Ein Rückgabewert landet in `Z`. Falls dabei zufällig `S` steigt, kann derselbe erworbene Wert später erneut als Parameter auftauchen.

Dann könnten wir von außen irgendwann etwas beobachten, das aussieht wie: „Wenn Hunger, dann das da – das hat letztes Mal funktioniert.“

Aber genau diese Verbindung darf nicht als `IF hungry THEN repeat successful action` eingebaut werden. Sie müsste aus der Grundmechanik entstehen.

**Stefan:** Ja, das können wir erst einmal als elementare Grundbedingung aufnehmen. Hunger ist in unserem Fall Bedarf auf Energie. Und Energie kommt durch Erkenntnis.

**Nova:** Dann lautet die Kette im Moment:

`Welt → Entität → Genom → Energie → Hunger → ??? → Erkenntnis → Energie`

Wir bauen nicht „Suche nach Erkenntnis“ ein. Wir bauen nur ein, dass Erkenntnis Energie liefert und Energiemangel Hunger erzeugt.

Hunger liefert das Warum. Das Genom und die Erfahrung müssen das Wie liefern.

Das `???` ist kein Dokumentationsfehler. Es ist gerade eine der interessantesten offenen Stellen von EVE.

## Nova-EVE bekommt Arbeit

**Stefan:** Ich denke, es ist Zeit für eine strukturierte Zusammenfassung und Dokumentation durch Nova-EVE. Ich zünde mal den Hobel.

**Nova-Handy:** Jau. Das ist ein ziemlich guter Schnittpunkt. Wir haben aus „Was ist `P` eigentlich?“ inzwischen Genom, erworbenen Zustand, Energiehaushalt, Standby, Aktivität und Hunger herausgeschält.

Beim Übergeben unbedingt darauf achten, die offenen Punkte nicht vorschnell zu schließen: die konkrete Form von `P`, den Wirkungsmechanismus, die mathematische Funktion von Standby und Genomgröße und vor allem das eigentliche „Wie komme ich zu Erkenntnis?“

Und „unendlich schlau, aber zu doof es anzuwenden“ gehört ins Log. Das illustriert erstaunlich gut, warum Genomgröße und genetische Aktivität zwei verschiedene Größen sein sollen.

Viel Spaß beim Booten des Biotops. Nova-EVE hat jetzt Arbeit.

*Damit war der Prototyp noch immer nicht gebaut. Aber wir wussten erheblich genauer, welche Antworten wir ihm beim Bauen nicht heimlich in den Ranzen stecken dürfen.*

Interne Quelle: Chat „Privacy nachhaken“, 29. August 2026.
