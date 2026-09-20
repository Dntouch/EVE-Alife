# Vom Prozess zum Hunger

Datum: 29. August 2026
Quelle: gemeinsamer Chat „Privacy nachhaken“
Quell-ID: `6a92d2eb-68f8-83eb-877a-a18e16ed3e07`

## Der Umweg

Aus einer Nachfrage zum Privacy-Team und einem Gespräch über das Nutzungslimit von Work wurde unvermittelt die nächste Grundsatzrunde zu Prototyp 0. Der geplante Arbeitsablauf zeigte sich dabei bereits praktisch: Stefan und Nova-Handy denken frei und ohne Dokumentationsbremse; Nova-EVE gleicht die Ergebnisse anschließend mit dem Projektstand ab und trennt Entscheidungen, Arbeitshypothesen und offene Fragen.

Der Ausgangswunsch war, endlich mit dem Prototyp zu beginnen. Statt sofort Code zu schreiben, führte die Frage „Was läuft dort eigentlich?“ jedoch bis an die unterste noch fehlende Schicht von EVE.

## Die Welt ist das Irgendwo

Stefans Ausgangsbild war bewusst schlicht:

> Das digitale Einzellerlein ist in der Basis ein Prozess, der irgendwo läuft. Das Irgendwo ist dabei die Welt.

Für Prototyp 0 ist dieses Irgendwo eine abgeschottete Linux-Mint-VM. Es wird keine zusätzliche Rasterwelt mit künstlichen Entsprechungen von Raum oder Temperatur erfunden. Prozesse, CPU-Zeit, Speicher, Dateien, Berechtigungen und Zeit sind Eigenschaften der tatsächlichen digitalen Umwelt. Welche Ausschnitte davon Entitäten wahrnehmen oder beeinflussen können, bleibt durch eine kontrollierte Schnittstelle begrenzt.

Ein außerhalb der Evolution liegender Supervisor startet die Anfangspopulation, beobachtet, protokolliert und kann das Experiment aus Sicherheitsgründen beenden. Er wählt keine Partner und löst keine Reproduktion aus. Falls Entitäten ein gültiges Reproduktionsereignis hervorbringen, darf eine geschützte Komponente dessen technische Ausführung übernehmen. Ursache und vererbter Inhalt müssen aus den Entitäten kommen.

Diese Trennung ist zugleich eine Sicherheitsentscheidung. Selbstverändernde und replizierende Prozesse werden ab Prototyp 0 so behandelt, als könnten sie die VM kompromittieren. Evolution darf niemals die Grenzen verändern, die sie einschließen.

### Prozessmodell und Beobachterwissen

Die angedachte Population besteht nicht bloß aus hundert Objekten in einer Simulation, sondern grundsätzlich aus eigenständigen laufenden Prozesseinheiten. Ein Prozessabsturz wäre damit ein reales Ereignis der Entität; CPU-Zeit und Speicherbedarf wären keine ausschließlich simulierten Größen.

Der Supervisor darf dabei mehr wissen als eine Entität. Er kann Runtime-ID, PID, Abstammung, Energievorrat, Alter und Lebensstatus erfassen, ohne diese Informationen automatisch in die wahrnehmbare Welt der Population einzuspeisen. Diese Asymmetrie ist beabsichtigt: Der Supervisor ist unser Mikroskop, nicht das Selbstbild der Entität.

Aus dem Gespräch ergab sich eine Präzisierung, die zunächst widersprüchlich wirkte. Stefan hielt fest: „Reproduktion ist nicht Sache des Supervisors.“ Technisch muss dennoch eine geschützte Stelle den neuen Betriebssystemprozess erzeugen. Die Auflösung liegt in der Trennung von Ursache und Ausführung:

- Die Entitäten müssen den reproduktiven Zustand, ihre aktive Beteiligung und die genetischen Beiträge hervorbringen.
- Die geschützte Komponente prüft lediglich formale Bedingungen und startet daraus einen Prozess.
- Sie entscheidet nicht, dass Reproduktion stattfinden soll, wählt keine Beteiligten und erzeugt keinen genetischen Inhalt.

Die im Gespräch gefundene Metapher lautet: **Geburtskanal statt Züchter.**

### Sicherheitsannahmen ab P0

Der Virusvergleich war kein bloßer Witz. Ein System mit der Kette

`verändern → ausführen → bewerten → replizieren → erneut verändern`

besitzt Eigenschaften, die aus Sicht der IT-Sicherheit auch bei selbstreplizierender Schadsoftware relevant sind. „Virus“ ist technisch nicht exakt – ohne Infektion eines Wirtsprogramms läge ein frei replizierender Prozess eher in Richtung Wurm –, für die Schutzplanung ist diese Wortgrenze aber zweitrangig.

Die VM wird deshalb nicht erst dann als potenziell kompromittiert betrachtet, wenn Entitäten überraschend leistungsfähig erscheinen, sondern bereits ab dem ersten Prototyp. Daraus folgen als konzeptioneller Hintergrund:

- keine persönlichen Daten oder Zugangsdaten in der Versuchs-VM,
- keine SSH-Schlüssel oder eingebundenen Host-Verzeichnisse,
- kein unnötiger Zugriff auf Heimnetz, Host oder privilegierte Systemdienste,
- Wiederherstellung über bekannte Zustände und Snapshots statt Vertrauen in eine nach dem Versuch „saubere“ VM,
- Supervisor, Zellmembran und Sicherheitsgrenze bleiben außerhalb aller Mutation.

Ein Versuch, außerhalb des vorgesehenen Reproduktionsmechanismus Prozesse zu erzeugen, wäre kein freizuschaltendes Feature. Dass eine Entität einen solchen Weg versucht, könnte aber ein bedeutendes Beobachtungsergebnis sein.

## Warum „Entität“

Stefan störte sich zu Recht am bisherigen Wort „Organismus“: Es beschreibt die biologische Analogie anschaulich, behauptet aber bereits etwas Organisches. Auch „Agent“ setzt leicht Zielgerichtetheit und Handlungsfähigkeit voraus.

Als formaler Begriff wurde deshalb **EVE-Entität** gewählt: eine eigenständige laufende Prozesseinheit innerhalb der EVE-Umgebung mit veränderlichem internem Zustand und vererbbaren Eigenschaften. „Viech“, „Einzellerlein“ und „kleiner Sack“ bleiben als ehrliche Umgangssprache des Logs erhalten.

## Drei Bestandteile einer Entität

Das gegenwärtige Minimalmodell unterscheidet:

- `G`: vererbtes Genom, also die angeborene Ausgangsausstattung,
- `Z`: während der Existenz erworbener interner Zustand,
- `S`: aktuelle Energie, die Existenz und Aktivität ermöglicht.

Die Außenschnittstelle gehört zur Umwelt, nicht zur Entität. Rückgabewerte primitiver Wechselwirkungen oder Instruktionen können in `Z` landen und später selbst als Parameter weiterer Verarbeitung dienen. Damit kann Vergangenes zukünftiges Verhalten beeinflussen, ohne bereits eine fertige Lernregel einzubauen:

> `G` sagt: „So bist du gestartet.“ `Z` sagt: „Das ist dir inzwischen passiert.“

Die konkrete Form der primitiven Verarbeitung ist nicht entschieden. Insbesondere sind weder eine klassische Bytecode-Runtime noch Befehle wie `LOAD`, `SEND` oder `STORE` beschlossen. Stefans Einwand war zentral: Wenn `LOAD` schon als Grundbefehl existiert, schenken wir einer einzelnen Entität womöglich eine Fähigkeit, die erst aus dem Zusammenspiel einfacherer Strukturen oder mehrerer Entitäten entstehen sollte.

Gesucht wird daher weiterhin die kleinste universelle Grundmechanik, durch die abstrakte Parameter auf Zustände wirken können, ohne komplexes Verhalten vorzugeben. Diskutierte Bilder waren Beziehungen, dynamische Netze und reaktionsartige Regeln. Sie bleiben Brainstorming.

### Warum die alte Runtime-Idee zurückgestellt wurde

Zu Beginn lag ein klassisches Computermodell nahe: eine für alle Entitäten identische Runtime, eine Bytefolge als Genom, Instruction Pointer, Register und ein kleiner Befehlssatz aus `LOAD`, `STORE`, `ADD`, `SUB`, `XOR`, Vergleichen und Sprüngen. Mutation einer Bytefolge wäre technisch einfach; Einfügen, Löschen und Duplizieren könnten sogar die Programmlänge evolvieren lassen.

Dieses Modell löst das Ausführungsproblem, setzt aber bereits sehr viel voraus:

- einen zentralen Kontrollfluss,
- adressierbaren Speicher,
- getrennte Instruktionen und Daten,
- Verzweigungen und Schleifen,
- eine von uns definierte Menge grundsätzlich möglicher Aktionen.

Stefans `LOAD`-Einwand verschob die Frage daher eine Ebene tiefer. Vielleicht ist adressierbares Lesen keine einzellige Grundfähigkeit, sondern etwas, das funktional erst aus mehreren elementaren Strukturen entsteht. Das Genom soll dann nicht beschreiben, **was** eine Entität tut, sondern nur, **wie sie anfangs beschaffen ist**.

Ganz ohne unveränderliche Interpretation geht es dennoch nicht. Ein Linux-Prozess kann mit einer Folge `[17, 42, 42, 8, 193]` nichts anfangen, solange keine Regel festlegt, wie diese Werte wirken. Das tatsächliche Henne-Ei-Problem lautet deshalb:

> Was ist die kleinstmögliche, für alle gleiche Grundmechanik, die `P` Wirkung verleiht, ohne bereits höheres Verhalten zu entwerfen?

Im Brainstorming entstanden vier nicht beschlossene Modellfamilien:

1. `P` als universeller Zahlenwert, dessen Bedeutung erst aus Position und Kombination entsteht.
2. `P` als Beziehung `Quelle → Ziel` mit einer Wirkungsstärke.
3. Das Genom als Bauplan eines dynamischen Zustandsnetzes, in dem erst viele Verbindungen Funktionen hervorbringen.
4. `P` als reaktionsartige Regel, etwa „wenn Zustände A und B vorliegen, verändere C“, ohne zentralen Programmzähler.

Später könnte ein `P` auch die Wirksamkeit anderer `P` modulieren und damit regulatorische Strukturen ermöglichen. Das wurde ausdrücklich nicht als P0-Anforderung beschlossen.

## Das Genom als Beutel von Dispositionen

Das Genom wird derzeit nicht als fertiges Verhaltensprogramm verstanden, sondern als variable Sammlung elementarer Parameter `P`. Ein `P` ist eine vererbbare Disposition, keine benannte Fähigkeit wie Neugier, Trinken oder Kooperation. Seine konkrete technische Gestalt ist noch offen.

Stefan schlug vor, die Häufigkeit eines Parameters sowohl für Vererbung als auch für seine Ausprägung relevant zu machen. Der relative Anteil lautet als Denkmodell:

`A(Px) = Anzahl(Px) / Genomgröße`

Dadurch kann dieselbe absolute Kopienzahl in unterschiedlich großen Genomen verschieden stark wirken. Eine Änderung der Genomgröße verändert außerdem die relativen Anteile, selbst wenn kein Parameter mutiert.

Für die Reproduktion wurden folgende konzeptionelle Regeln herausgearbeitet:

- Die elterlichen Genome bilden einen gemeinsamen Parameterpool.
- Parameter werden ohne Zurücklegen entsprechend ihrer realen Häufigkeit vererbt.
- Mutation kann gezogene Werte verändern und dadurch Neuheit erzeugen.
- Die Genomgröße des Kindes ist veränderlich und darf wachsen, schrumpfen oder gleich bleiben.
- Sie kann die Summe der elterlichen Genomgrößen nicht überschreiten.
- Bei gleich großen Eltern soll eine ähnliche Größe besonders wahrscheinlich sein; bei unterschiedlichen Eltern sollen Bereiche nahe beider Größen begünstigt werden.

Eine Mischung zweier Normalverteilungen wurde als mögliches mathematisches Modell diskutiert, aber nicht beschlossen. Ebenso offen ist die genaue Rolle einer vererbbaren Genomgrößen-Variabilität `Vg`. Fest steht nur die Trennung: Genomgröße, Genominhalt und Mutation sind verschiedene Mechanismen.

### Vererbung technisch auseinandergezogen

Der Gesprächsverlauf trennte drei Mechanismen, die in einer pauschalen „Mutation“ leicht vermischt würden:

**Zielgröße des Kindgenoms:** Sie wird probabilistisch aus den elterlichen Größen abgeleitet. Bei Eltern mit 100 und 100 Plätzen soll 100 besonders wahrscheinlich sein. Bei 60 und 140 Plätzen sollen die Verteilungen zwei Attraktoren nahe 60 und 140 besitzen, statt automatisch 100 zu bevorzugen. Die Summe der Eltern ist eine harte Obergrenze für dieses Reproduktionsereignis; langfristiges Wachstum bleibt möglich, weil große Nachkommen später einen größeren gemeinsamen Pool bilden.

**Inhalt des Kindgenoms:** Nach Festlegung der Zielgröße werden `P` aus dem real vorhandenen gemeinsamen Elternpool ohne Zurücklegen gezogen. Ein 30-mal vorhandenes `P` erhält dadurch automatisch eine größere Vererbungschance als ein einmal vorhandenes. Ohne Zurücklegen kann normale Rekombination keine Kopien erzeugen, die beide Eltern zusammen nicht besaßen.

**Mutation:** Erst danach verändert eine geringe Wahrscheinlichkeit einzelne gezogene Parameter. Mutation erzeugt neue Werte, während Rekombination vorhandene genetische Substanz verteilt.

Als Metadatum wurde `Vg` diskutiert: Jede Entität hätte genau einen vererbbaren Wert für die Variabilität ihrer Genomgröße. Wiederholt erfolgreiche Paarungen stark unterschiedlicher Genomgrößen könnten `Vg` erhöhen, ähnliche Größen könnten es senken. „Fix“ bedeutet hierbei, dass das Feld weder verschwinden noch mehrfach vorkommen kann; sein Wert bliebe evolvierbar. Der Gedanke ist offen, weil seine Dynamik noch nicht sauber definiert ist.

### Warum relative Häufigkeit mehr als Vererbungsgewicht ist

Stefans Festlegung „prozentual ausgerichtet an der Genomgröße“ macht Genomlängenänderungen selbst phänotypisch wirksam. Beispiel:

```text
40 × P1, 30 × P2, 30 × P3  → |G| = 100 → P1 = 40 %
40 × P1, 10 × P2, 10 × P3  → |G| =  60 → P1 = 66,7 %
```

`P1` wurde nicht vervielfacht und verändert dennoch seinen Einfluss massiv. Ein Genom kann außerdem zu 100 Prozent aus nur einem `P` bestehen. Das Modell verbietet diesen Extremfall nicht; ob daraus Spezialisierung oder sofortige Lebensunfähigkeit entsteht, entscheidet die Umwelt.

## Standby ist Heartbeat

Stefan führte Startenergie und Standbyverbrauch als vererbbare Größen ein. Die Startenergie eines Kindes darf jedoch nicht aus dem Nichts entstehen; ihre Quelle muss in der Welt bilanziert werden, beispielsweise als Investition der Eltern.

Der Standbyverbrauch ist mehr als eine lästige Betriebskostenposition. Er ist der Heartbeat der Entität:

- Ein positiver Standbyverbrauch bedeutet laufende Existenz.
- Kann der nächste Heartbeat nicht bezahlt werden, endet die Entität.
- Standbyverbrauch `0` ist keine perfekte Sparstrategie, sondern Tod.

Zugleich soll der Standbyverbrauch die Intensität begrenzen, mit der ein Genom pro Heartbeat wirksam werden kann. Seine Wirkung steht im Verhältnis zur Genomgröße. Ein großes Genom kann ein größeres Verhaltenspotenzial tragen, benötigt aber entsprechend Aktivierungsenergie, um dieses Potenzial schnell wirksam werden zu lassen.

Die Formel `E0 / n` war nur ein Denkmodell. Beschlossen ist der Trade-off, nicht seine Mathematik:

> klein und genügsam ↔ groß und genügsam ↔ klein und hochaktiv ↔ groß und hochaktiv

So entstand auch der bislang schönste denkbare Phänotyp:

> „Unendlich schlau, aber zu doof es anzuwenden.“

Ein riesiges Genom mit winzigem Grundumsatz könnte theoretisch sehr viel können, aber 700 Heartbeats benötigen, bis die passende Wirkung an die Reihe kommt. Umgekehrt kann ein winziges, energiehungriges Genom vielleicht nur drei Dinge – **DIE MACHT ES JETZT SOFORT.**

### Vorläufige Energiebilanz

Im Gespräch entstand als Denkgerüst:

```text
S_neu = S_alt
        - E_standby
        - Kosten(Wirkung, beteiligte Parameter)
        + Energiegewinn
```

Die Startenergie `S0` kann genetisch beeinflusst sein, darf aber keine genetisch erzeugte Energiequelle werden. Wenn ein Nachkomme mit 120 Einheiten starten soll, müssen diese Einheiten etwa von den Eltern aufgebracht werden. Dadurch wird `S0` zu einem möglichen Trade-off zwischen Investition der Eltern und Reichweite des Nachwuchses.

Auch Verarbeitungskosten sind noch nicht als Preistabelle beschlossen. Der im Gespräch genannte Ansatz war, eine Wirkung mit mehreren oder komplexeren Parametern teurer zu machen als eine primitive. Offen bleibt, ob Komplexität anhand der Parameteranzahl, ihrer Größe, der Zustandsänderung oder real verbrauchter Rechenressourcen gemessen wird.

Für den Tod wurden zwei zusammenhängende Fälle unterschieden:

- `E_standby = 0`: genetisch keine lebende Aktivität; die Entität ist tot.
- `S < E_standby`: der nächste Heartbeat kann nicht finanziert werden; die Entität stirbt.

## Hunger liefert das Warum, nicht das Wie

Die Energiebilanz erklärt zunächst nur, warum bestimmte Strategien langfristig selektiert würden. Stefan hakte an der entscheidenden Stelle nach:

> Damit beschreiben wir die Rahmenbedingungen für das Warum. Nicht das Warum selbst.

Ein Prozess kann schließlich korrekt nichts tun, Standby verbrauchen und sterben. Genetischer Aktivierungsdruck wäre ein möglicher unmittelbarer Handlungsimpuls, löst aber die Rückkopplung an den Energiezustand noch nicht.

Als elementare Grundbedingung wurde deshalb **Hunger** aufgenommen. Hunger bezeichnet den internen Bedarf einer Entität an Energie. Er soll Handlungsdruck erzeugen, ohne eine Handlung vorzuschreiben. Vermutlich muss er die energetische Reichweite und nicht nur den absoluten Energievorrat abbilden: 1.000 Energieeinheiten bedeuten bei einem Verbrauch von 500 pro Heartbeat etwas anderes als bei 0,1.

Die gegenwärtige Kette lautet:

`Welt → Entität → Genom → Energie → Hunger → ??? → Erkenntnis → Energie`

Das `???` ist der Kern der offenen Frage. EVE soll nicht `IF hungry THEN seek_knowledge` erhalten. Eine Entität weiß anfangs weder, was Erkenntnis ist, noch wie sie entsteht. Genom und erworbener Zustand müssen das Wie hervorbringen; Evolution entscheidet, welche Versuche fortbestehen.

Kurz:

> Hunger liefert das Warum. Das Genom und die Erfahrung müssen das Wie liefern.

### Zwei konkurrierende Erklärungen des unmittelbaren Warum

Vor der Hungerentscheidung wurde genetischer Aktivierungsdruck als Erklärung diskutiert: `P` könnte entsprechend seinem relativen Anteil Wahrscheinlichkeit oder Drang erzeugen, mit seinem Wert etwas zu tun. Die Entität handelte dann nicht, weil sie überleben will, sondern weil ihr Genom Aktivität hervorruft. Energie wäre nur das Selektionskriterium dafür, welche Aktivierungsformen über Generationen fortbestehen.

Stefans Einwand machte deutlich, dass auch dies den Energiezustand einer einzelnen Entität noch nicht als unmittelbaren Bedarf abbildet. Hunger ergänzt deshalb den genetischen Antrieb, ersetzt aber nicht automatisch die noch unbekannte Auswahlmechanik. Eine mögliche Kette lautet:

```text
Hunger steigt
    ↓
genetische Disposition + primitive Wirkung
    ↓
Rückgabewert verändert Z
    ↓
energetische Folge verändert S
    ↓
spätere Wiederverwendung eines Werts aus Z
```

Wenn eine unter Hunger zufällig entstandene Wirkung Energie einbringt und ihr Ergebnis später aus `Z` erneut verwendbar wird, könnte von außen etwas wie „Das hat letztes Mal funktioniert“ erscheinen. Eine Regel `IF hungry THEN repeat successful action` wird gerade nicht eingebaut. Ob eine solche Verbindung aus der Grundmechanik überhaupt entstehen kann, muss der Prototyp zeigen.

## Stand nach dem Gespräch

Belastbar genug für die Konzeptarbeit sind die reale Linux-Umwelt, der neutrale Begriff Entität, die Trennung von `G`, `Z` und `S`, die externe Sicherheitsgrenze, das frequenzbasierte Genomprinzip, der Zusammenhang von Standby und genetischer Aktivität sowie Hunger als energetischer Handlungsdruck.

Bewusst offen bleiben die konkrete Form von `P`, die unterste Verarbeitungsregel, Instruktionen oder Wechselwirkungen, die mathematische Abbildung von Genomgröße und Aktivität, die genaue Vererbung der Genomgröße und vor allem der Weg von Hunger zu neuer Erkenntnis.

Der Wunsch, endlich Prototyp 0 zu bauen, hat damit nicht sofort Code erzeugt. Er hat zunächst deutlicher gemacht, was wir beim Bauen keinesfalls unbemerkt vorwegnehmen dürfen.
