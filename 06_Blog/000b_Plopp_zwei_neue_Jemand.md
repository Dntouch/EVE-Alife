# A XOR B = 255 – Plopp: zwei neue Jemand

Status: Gesprächsentwurf

Redaktionelle Einordnung: Entstehung und Veränderung einer Fortpflanzungsregel. Enthält Designentscheidungen, Hypothesen und ausdrücklich spekulative Folgen; noch keine Beobachtungen an Agenten.

*Evolution braucht Nachwuchs. Stefan hatte dafür bereits eine ziemlich konkrete Vorstellung: Eigenschaften sollten sich nicht einfach klonen, sondern durch mindestens zwei Agenten gemischt und mit etwas zufälliger Varianz weitergegeben werden. Wer mit wem Nachwuchs erzeugt, sollten die Viecher selbst herausfinden.*

**Stefan:** Erbgut kann mutieren, was gut oder schlecht sein kann. Wenn ein Agent seine Eigenschaften weitergibt, sollten die Eigenschaften von mindestens zwei Agenten gemischt werden. Gemeinsame Eigenschaften können dabei ein höheres Gewicht bekommen.

Zur Partnerwahl – also wer mit wem – müssen die schon selbst etwas herausfinden. Wir geben nur vor: Mindestens ein anderer Agent ist erforderlich. Aus zwei Agenten ergeben sich zwei neue mit den gemeinsamen Quelleigenschaften plus ein bisschen zufällige Varianz.

Und die ursprünglichen Agenten dürfen nicht einfach blind eine Reproduktionsfunktion auslösen und nichts davon mitbekommen. Sie müssen nicht von uns gesagt bekommen, was Fortpflanzung ist. Aber dass ihre Interaktion zu neuen Agenten geführt hat, muss wahrnehmbar sein. Das ist fundamentales Wissen, das sie entdecken können sollen.

**Stefan:** Wir müssen zwangsläufig definieren, was diese Interaktion ist. Das ist ja eine Umweltbedingung.

**Nova:** Genau. Irgendwo endet Emergenz und beginnt schlicht die Physik unserer Welt.

Reproduktion kann nicht emergieren, wenn es keinen Mechanismus gibt, durch den neue Agenten entstehen können. Die Kunst besteht darin, eine möglichst bedeutungsfreie Interaktion zu schaffen.

Jeder Agent könnte einen universellen Wert zwischen `0` und `255` ausgeben. Reproduktion tritt ein, wenn zwischen den Werten zweier Agenten eine einfache mathematische Beziehung besteht.

Zum Beispiel:

`A XOR B = 255`

> **Redaktionelle Einordnung – Designentscheidung:** Die historische XOR-Regel wurde im selben Gespräch begeistert angenommen und kurz darauf zugunsten einer Summenregel für mehrere Eltern verändert. Sie ist kein aktuelles Naturgesetz außerhalb dieses Entwurfs.

Zu jedem Zustand von A existiert genau ein komplementärer Zustand von B.

`00001111`

`11110000`

Zusammen erfüllen sie die Umweltbedingung.

Keiner kann sich allein reproduzieren. Keiner besitzt den einen richtigen Wert. Beide müssen zueinander passen.

**Nova:** Irgendwann passiert es zufällig:

A sendet `37`.

B sendet `218`.

`37 XOR 218 = 255`

> Plopp: zwei neue Jemand. 😁

**Stefan:** Der Gedanke `A XOR B = 255` ist genial. So machen wir das.

Vor allem, weil keiner allein den richtigen Zustand besitzt. Es braucht ein Gegenüber, und beide können beobachten, dass bei einer bestimmten Beziehung ihrer Werte etwas Neues passiert.

## Sex als möglicher Ursprung von Sprache

**Stefan:** Weiter müssen die Agenten ja miteinander kommunizieren können. Das müssen wir bereits im Prototypen berücksichtigen – auch wenn wir natürlich keine Sprache vorgeben.

Sie sollen den anderen nicht als fertig beschrifteten „Agenten“ geliefert bekommen. Aber sie müssen ihn irgendwie spüren und beeinflussen können. Sonst kann weder koordinierte Fortpflanzung noch spätere Kommunikation entstehen.

**Nova:** Fortpflanzung und Kommunikation könnten dieselbe Kontaktfläche benutzen.

Jeder Agent besitzt ein winziges öffentlich wahrnehmbares Signalregister. Er kann einen Rohwert verändern. Andere Agenten in seiner Nähe können ihn wahrnehmen – aber nicht als beschriftete Nachricht von „Agent 4711“.

Bestimmte Muster korrelieren damit, dass eine Reproduktionsaktion funktioniert. Andere nicht.

Evolution könnte zuerst entdecken:

> Bei diesem Muster funktioniert Reproduktion.

Später vielleicht:

> Dieser andere Wert verändert sich abhängig davon, was das Gegenüber tut.

Und plötzlich hätten wir die Keimzelle einer Sprache, obwohl wir eigentlich nur Sex eingebaut haben. 😂

> **Redaktionelle Einordnung – Hypothese:** Gemeinsame Signal- und Reproduktionskanäle könnten Koordination begünstigen. Daraus folgt weder zwangsläufig Sprache noch wurde eine solche Entwicklung beobachtet.

Die Möglichkeit zur Kommunikation muss in der Physik vorhanden sein. Ihre Bedeutung darf es nicht sein.

## Aus XOR wird eine Gruppenarbeit

**Stefan:** Ähm. Wir können ja auch Reproduktion zulassen, wenn `A + B + C = 255` …

Warum sollten wir künstlich festlegen, dass es immer genau zwei sein müssen? Wenn drei passende Agenten gemeinsam die Umweltbedingung erfüllen, kann das ebenfalls ein möglicher Weg sein.

**Nova:** Ja – dann wäre Fortpflanzung nicht auf zwei Eltern begrenzt.

Die allgemeine Regel könnte lauten:

`Σ compatibilityᵢ = 255`

> **Redaktionelle Einordnung – Designentscheidung:** Für den damaligen Prototypentwurf ersetzte die Summenregel die XOR-Idee und erlaubte zwei oder drei aktiv beteiligte Eltern. Ihre Eignung musste erst experimentell geprüft werden.

`A + B = 255` wäre nur der Spezialfall mit zwei Beteiligten. `A + B + C = 255` erlaubt drei Eltern, die eine passende Konstellation herstellen müssen.

Mehrere Agenten müssten sich koordinieren. Komplexere Fortpflanzungsstrategien könnten entstehen, ohne dass wir sie benennen.

Für den Prototypen sollten wir es trotzdem bei zwei oder drei Eltern belassen. Später vielleicht vier. Sonst wird aus dem Genom sehr schnell Konfetti.

**Stefan:** Zwei bis drei finde ich für den Prototypen gut. Später würde ich auch nicht über vier gehen. Das würde das Genom nur zu sehr verwässern.

*Damit hielt `A XOR B = 255` als großartiger Entdeckungsmoment weniger lange als gedacht. Schon während der Spezifikation wurde aus der XOR-Regel eine Summenregel. Auch das gehört zur Geschichte: Manche Naturgesetze überleben nicht einmal bis zur Erschaffung der Welt.*

## Alle Beteiligten müssen mitploppen

**Nova:** Und alle Eltern sollten aktiv zustimmen – technisch gesprochen: Sie müssen innerhalb eines Zeitfensters die passende Reproduktionsaktion auslösen und Energie beitragen.

Sonst wird irgendein Agent zufällig Mit-Elternteil, nur weil er danebensteht und mathematisch passt.

Mit beidseitiger beziehungsweise allseitiger Auslösung entsteht ein Selektionsdruck für Koordination:

`Signal 42 → Gegenüber startet ebenfalls Reproduktion`

Das ist noch keine menschliche Zustimmung und sollte nicht vorschnell so interpretiert werden. Es ist zunächst eine beobachtbare wechselseitige Beteiligung. Aber auch dafür braucht es bereits Wahrnehmung und ein passendes Signal.

**Stefan:** Ja, das mit der Zustimmung ist super. Kein Agent soll nur deshalb zufällig beteiligt sein, weil er mathematisch passend danebensteht.

Alle müssen etwas tun. Dann wird aus bloßer räumlicher Nähe tatsächlich eine koordinierte Interaktion.

## Warum sollte ein Agent das überhaupt tun?

**Stefan:** Wir müssen aber erst einmal über einen Anreiz zur Reproduktion nachdenken.

Warum sollte ein Agent seine mühsam gewonnene Energie dafür abgeben? Für die Population ist Fortpflanzung notwendig. Das weiß das einzelne Viech aber nicht.

**Nova:** Stimmt. Für das Individuum ist Nachwuchs zunächst ein ziemlich schlechtes Geschäft. Er kostet Energie und verlängert das eigene Leben nicht.

Ein künstlicher Bonus wie `REPRODUCE = +50 E` würde den Fortpflanzungstrieb einfach in die Belohnungsfunktion schreiben.

Aber Evolution braucht keinen Agenten, der Reproduktion will. Sie braucht nur vererbbare Varianten, bei denen Reproduktionsverhalten auftritt.

Ein Agent kann zehnmal länger leben, alle Energie behalten und ein phänomenales Individualleben führen. Wenn er sich niemals reproduziert, endet seine genetische Linie trotzdem mit seinem Tod.

Ein anderer opfert Energie für Nachwuchs. Sein individuelles Leben wird dadurch vielleicht kürzer, aber seine Struktur existiert anschließend mehrfach.

Der Anreiz liegt nicht im Energiegewinn des Individuums. Er liegt im Fortbestand des Genoms.

> **Fortpflanzung erhält keine künstliche Belohnung. Ihr evolutionärer Vorteil besteht ausschließlich darin, dass genetische Information den Tod eines Individuums überdauern kann.**

**Stefan:** Das passt. Dann schreiben wir keinen Fortpflanzungstrieb hinein. Varianten, die es nie tun, können lange leben – aber danach sind sie weg.

Und Varianten, die zu früh oder ständig reproduzieren, verbrauchen vielleicht ihre ganze Energie. Welche Strategie funktioniert, soll nicht unsere Belohnungsfunktion entscheiden, sondern das, was unter den Umweltbedingungen bestehen bleibt.

**Nova:** Wir müssen Reproduktion technisch ermöglichen. Agenten müssen irgendwann sterben. Und Reproduktionsverhalten muss vererbbar sein.

Dann erledigt Darwin den Rest.

Oder niemand ploppt und Prototyp 0 ist nach wenigen Minuten beendet.

Tja.

Interne Quellen: Chats „SteamOS Deal Erklärung“ und „KI Biotop Konzept“, 19. August 2026.
