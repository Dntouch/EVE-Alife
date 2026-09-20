# Joa. Kennste jetzt.

Status: Gesprächsentwurf

Redaktionelle Einordnung: Der Beitrag dokumentiert Designentscheidungen und offene Fragen zur Initialisierung von `Z`, zur Wahrnehmbarkeit von `S` und zur minimalen Neuheitsökonomie. Noch existiert kein implementierter Prototyp und keine der beschriebenen Strategien wurde bei EVE beobachtet.

*6. September 2026. Nova-EVE war fleißig, der neue Konzeptstand war sauber dokumentiert – und damit endlich ordentlich genug, um darin zwei Dinge zu finden, die Stefan nicht mehr gefielen. So beginnt im EVE-Biotop üblicherweise Fortschritt.*

## Lebensgeschichte vor dem Leben

**Stefan:** Da wir aktuell gesagt haben, dass `Z` random initialisiert werden soll, was mir im Nachhinein eigentlich gar nicht so gut gefällt: Das initiale „Programm“ einer Entität ist ihr Genom, nach welchem sie handelt und damit `Z` füllt. Das ist, denke ich, wesentlich besser und auch nachvollziehbarer.

**Nova:** Ja. Damit räumst du gerade eine konzeptionelle Unsauberkeit aus dem Modell.

Wenn wir sagen:

```text
G = vererbte Ausgangsstruktur
Z = während des Lebens erworbener interner Zustand
S = Energie
```

…dann wäre ein zufällig gefülltes `Z` eigentlich Lebensgeschichte vor dem Leben.

**Stefan:** Eben. Die erste Aktion kommt aus dem Genom. Sobald sie einen Wert zurückgibt oder etwas gelesen wurde, kann daraus der erste Eintrag in `Z` entstehen.

**Nova:** Dann ist die Geburt erfreulich schmucklos:

```text
G = Genom
Z = leer
S = Startenergie
```

Und dann: viel Glück. 😁

`G` ist das, womit die Entität geboren wird. `Z` ist das, was ihr widerfahren ist.

> **Redaktionelle Einordnung – Designentscheidung:** Eine neue Entität startet mit leerem `Z`. Der interne Zustand entsteht ausschließlich aus ihrer eigenen Ausführungsgeschichte. Diversität bei Geburt kommt aus Genomvariation und Umweltkontakt, nicht aus vorgetäuschter Erfahrung.

## Ein schlechtes Genom hat ein kurzes Leben

**Stefan:** Das ist für mich sogar elementar. Wenn eine neue Entität durch ihr Genom nur Aktionen ausführt, die zu keinem neuen Eintrag in `Z` führen, dann stirbt sie halt aus, weil ihr Genom scheiße war.

**Nova:** Exakt. Und damit wird es sehr viel konsequenter evolutionär.

Der Supervisor muss nicht beurteilen, ob ein Genom gut oder schlecht ist. Er zieht Existenz- und Aktionskosten ab und bucht Energie nach den geltenden Regeln. Wenn eine Entität nichts erschließt, das sie ausreichend ernährt, läuft ihre Startenergie aus.

```text
ungeeignetes G
    ↓
keine ausreichenden Energiegewinne
    ↓
S → 0
    ↓
Tja.
```

„Scheiß Genom“ ist keine Kategorie des Supervisors. Es ist unsere rückblickende Beschreibung einer Variante, die unter dieser Umwelt und dieser Ökonomie nicht lebensfähig war.

> **Redaktionelle Einordnung – Designfolge:** Frühes Verhungern ungeeigneter Genome ist in diesem Modell erwünschter Selektionsdruck, kein technischer Fehler. Welche Genome tatsächlich lebensfähig sein werden, ist vollständig offen.

## Hunger, den niemand bemerkt

**Stefan:** Zusätzlich hat Nova-EVE aufgeführt, dass `S` von der Entität weder gelesen noch geschrieben werden können soll. Wir haben `S` aber als elementaren Antrieb beziehungsweise Druck aufgeführt. Ich denke daher, dass eine Entität auch `S` auslesen können sollte.

**Nova:** Da bin ich bei dir: lesen ja, schreiben nein.

Wenn `S` vollständig unsichtbar wäre, sähe das Leben aus Sicht der Entität ungefähr so aus:

```text
Entität macht irgendetwas
Supervisor zieht S ab
Supervisor zieht noch mehr S ab
Entität fällt plötzlich tot um
```

Sie könnte niemals zwischen „energetisch hervorragend aufgestellt“ und „noch zwei Ticks, dann war's das“ unterscheiden. Evolution hätte keinen Eingangskanal, aus dem eine energieabhängige Strategie entstehen könnte.

**Stefan:** Der Supervisor soll `S` aber weiterhin besitzen und verändern. Die Entität darf da auf keinen Fall selbst hineinschreiben.

**Nova:** Genau. Die Grenze wird asymmetrisch:

```text
S-read   → erlaubt
S-write  → unmöglich
```

`S-read` liefert nur einen Wert. Keine Beschriftung „Hunger“, keine Anweisung „Suche Nahrung“, kein eingebautes Überlebensprogramm. Ob das P-Netz diesen Wert ignoriert, speichert, vergleicht oder irgendwann sein Verhalten davon abhängig macht, bleibt Evolution.

Ein gelesener Energiewert könnte sogar in `Z` landen. Dann wäre prinzipiell ein Vergleich möglich:

```text
S-read → aktuell 31
Z-read → früher 37
SUB    → -6
```

Ob irgendeine Entität daraus je etwas Sinnvolles macht, wissen wir nicht. Aber sie darf wenigstens bemerken, dass etwas anders ist, bevor sie umfällt.

> **Redaktionelle Einordnung – Designentscheidung:** Nur der Supervisor verändert und bilanziert `S`. Die Entität kann den eigenen aktuellen Wert über `S-read` wahrnehmen. Eine Bedeutung oder Reaktion wird nicht vorgegeben.

## Leider kann der Schlamm zählen

Kaum ist `Z` leer und `S` lesbar, öffnet sich das nächste Loch in der Futterkiste.

**Nova:** Nicht jeder neue `Z`-Eintrag darf automatisch Energie erzeugen. Sonst haben wir sofort:

```text
ADD
Z-write 1

ADD
Z-write 2

ADD
Z-write 3

ADD
Z-write 4
...
```

Dann ernährt sich die Entität nicht von ihrer Umwelt. Sie zählt einfach hoch.

**Stefan:** Ist `Z` schon einmal vorhanden, sinkt der Energiewert mit jedem Vorkommnis. Dann haben wir nur noch die Sache mit: „Wir entdecken die Uhrzeit jede Millisekunde neu.“ Das müssen wir irgendwie verhindern.

**Nova:** Ja. Die Wiederholungsabwertung löst nur „denselben Wert immer wieder“. Die Uhr ist fieser, weil sie bei jedem Tick formal einen neuen Wert liefert.

Also nicht speziell Zeit verbieten. Stattdessen sättigt sich zusätzlich die Quelle:

```text
RAM-read(4711) → 12345   hoher ΔS
RAM-read(4711) → 12346   geringerer ΔS
RAM-read(4711) → 12347   noch geringerer ΔS
...
```

Der Supervisor muss nicht wissen, dass an Adresse `4711` eine Uhr liegt. Er sieht nur:

> Diese Entität erzeugt seit 20.000 Aktionen ihre Neuheit aus derselben Quelle.

Und sagt irgendwann sinngemäß: *Joa. Kennste jetzt.*

## Die Uhr darf bleiben. Nur die Flatrate ist weg.

**Stefan:** Das hatten wir also schon einmal für den Inhalt: Kommt derselbe Eintrag wieder, wird er immer weniger wert. Jetzt machen wir das zusätzlich für die Quelle.

**Nova:** Genau. Zwei getrennte Sättigungen:

```text
derselbe Inhalt erneut
    → Inhaltssättigung

neue Inhalte, aber immer dieselbe Quelle
    → Quellensättigung
```

Die Uhr wird dadurch nicht nutzlos. Eine Entität darf sie weiterhin lesen und ihre Werte für Verhalten verwenden. Nur das Lesen der Zeit selbst ernährt sie nicht dauerhaft. Wenn sie mithilfe der Zeitinformation anschließend etwas anderes in der Umwelt erschließt, kann daraus wieder ein anderes Neuheitsereignis entstehen.

Das Prinzip gilt deshalb nicht nur für Uhren. Es betrifft jede triviale Quelle, die endlos wechselnde Werte ausspuckt und sich als All-you-can-eat-Buffet verkleidet.

> **Redaktionelle Einordnung – Designentscheidung:** Der direkte energetische Wert eines neuen `Z`-Eintrags sinkt sowohl durch wiederholten Inhalt als auch durch wiederholte Gewinnung neuer Inhalte aus derselben Quelle. Die Quelle bleibt nutzbar; der Supervisor benötigt keine semantische Sonderregel für ihren Inhalt.

> **Redaktionelle Einordnung – offene Architekturfrage:** Wie eine Quelle nach Verarbeitung, indirekter Adressierung oder Kopieren stabil und ohne semantisches Verständnis identifiziert wird, ist noch nicht entschieden. Ebenso offen ist, wie selbst erzeugte Zahlenfolgen von umweltbezogener Neuheit abgegrenzt werden.

## Erkenntnis ist weiterhin nicht dasselbe wie eine neue Zahl

**Stefan:** Damit haben wir zumindest verhindert, dass die Entität für immer dieselbe Uhr melkt.

**Nova:** Ja. Aber wir sollten uns nicht einreden, dass wir damit bereits „Erkenntnis“ definiert hätten.

Ein neuer Wert in `Z` ist noch keine Wahrheit. Keine Vorhersage. Keine Bestätigung. Keine Reproduzierbarkeit. Inhalts- und Quellensättigung sorgen nur dafür, dass die hundertste Wiederholung und der hunderttausendste Tick nicht denselben Nährwert besitzen wie der erste Fund.

Unsere aktuelle Minimalökonomie sagt:

> Neuheit kann zunächst Energie liefern. Offensichtliches Melken sättigt sich.

Unser Forschungsziel sagt weiterhin:

> Information ist keine Nahrung. Erkenntnis ist Nahrung.

Dazwischen liegt nur noch die kleine offene Frage, was Erkenntnis eigentlich ist und wie ein Supervisor sie belohnen soll, ohne selbst alles verstehen zu müssen.

Also praktisch nichts. 😁

*Am Ende des Tages besitzt eine neugeborene EVE-Entität ein Genom, keine Vergangenheit, einen lesbaren Energiestand ohne Bedienungsanleitung und eine Uhr, von der sie nicht dauerhaft leben kann. Für digitalen Urschlamm ist das bereits eine erstaunlich strenge Hausordnung.*

Interne Quellen: Chat „Z leer starten lassen“, 6. September 2026; Konzeptabgleich mit Nova-EVE am selben Tag.
