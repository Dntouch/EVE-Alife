# Von der Frage „Was ist P?“ zur RAM-Suppe und zum Datenflussnetz

Datum: 6. September 2026

Quelle: gemeinsame Konzeptarbeit mit Nova-EVE

## Ausgangslage

Am 29. August war die zentrale Konstruktionslücke bewusst offengeblieben: Was ist ein elementares `P`, und wie kann es überhaupt wirken, ohne einer Entität bereits ein kleines fertiges Computerprogramm zu schenken?

Der damalige Fortschritt bestand gerade darin, die bequeme Antwort zurückzuweisen. Eine lineare Bytecode-Runtime mit Instruction Pointer, Registern, `LOAD`, `STORE`, Sprüngen und Tests hätte das Ausführungsproblem technisch gelöst, zugleich aber Kontrollfluss, Speicherbegriffe und Verhaltensformen vorgegeben. Als Alternativen standen Zahlenwerte, Beziehungen, Reaktionsregeln und Netze nebeneinander. Keines dieser Bilder war entschieden.

Die offene Frage lautete:

> Was ist `P`?

## Die Welt wird kleiner: von Linux zur RAM-Suppe

Der nächste Schritt begann nicht beim Genom, sondern bei der Umwelt. „Der reale Linux-Rechner ist die Welt“ war als langfristiger Rahmen zu groß und für die erste Begegnung einer Entität bereits zu semantisch beladen. Dateien, Pfade und Prozesse sind zwar reale Rechnerstrukturen, aber keine elementaren Dinge.

Als erste erreichbare Welt wurde deshalb eine vom Supervisor bereitgestellte beziehungsweise reservierte **RAM-Suppe** formuliert: ein gemeinsamer adressierbarer Speicherbereich ohne Dateinamen, Verzeichnisse oder Systemaufrufe als Begriffe der Entität.

Die Einzeller belegen Bereiche dieser Suppe. Ihr Inneres bleibt geschützt. Damit entstand eine klare Trennung:

```text
geschütztes Innen: G, Z
wahrnehmbarer, supervisor-kontrollierter Energiezustand: S
kontrollierte Grenze: Membran
gemeinsames Außen: RAM-Suppe
```

`S` wurde dabei asymmetrisch abgegrenzt. Nur der Supervisor verändert und bilanziert die Energie. Die Entität darf ihren eigenen aktuellen Wert jedoch über `S-read` lesen und wie andere Rückgabewerte verarbeiten oder in `Z` speichern. So bleibt Hunger als prinzipiell wahrnehmbarer energetischer Druck evolvierbar, ohne eine Interpretation oder Reaktion fest einzubauen.

## Die Membran verliert ihre biologische Unschärfe

Die digitale Zellmembran war bisher eine allgemeine Vermittlungsschicht zur Rechnerumwelt. Im RAM-Modell wurde sie konkreter: Sie ist ein vom Supervisor kontrolliertes, adressierbares Interface des belegten Entitätsbereichs.

Ein äußerer Zugriff auf die Membran darf `G`, `Z` oder `S` nicht enthüllen. Als einfachster sichtbarer Wert bietet sich die vom Supervisor vergebene Entity-ID an. Weitere Offsets könnten später primitive Lese- oder Schreibpunkte tragen. Ob Offset `0` tatsächlich die ID enthält und welche weiteren Punkte existieren, blieb bewusst offen.

## Die Antwort auf „Was ist P?“

Mit einer adressierbaren, aber primitiven Umwelt ließ sich die Genomfrage neu stellen. `P` musste kein Befehl wie `READ` und keine benannte Disposition wie „Neugier“ sein. Es konnte kleiner sein:

> `P` ist eine vererbbare gerichtete Datenflusskante `A.out → B.in`: die Verschaltung eines Ausgangsports mit einem Eingangsport elementarer Funktionspunkte.

Der Wert fließt nur in Pfeilrichtung; die Verbindung ist nicht automatisch umkehrbar. Ein einzelnes `P` tut damit fast nichts. Erst viele `P` bilden ein Datenflussnetz. Dessen Topologie bestimmt zusammen mit `Z`, den Werten der RAM-Suppe und den vorhandenen primitiven Operationen, was tatsächlich geschieht.

Als derzeitiger Kandidatensatz entstanden:

```text
Z-read, Z-write, RAM-read, RAM-write, ADD, SUB, XOR, EQ
```

Für die Schreibpunkte wurde eine kleine, aber folgenreiche Semantik konkretisiert:

```text
ZWRITE(address, value)   -> value
RAMWRITE(address, value) -> value
```

Schreiben hat einen Seiteneffekt und reicht denselben Wert zugleich im Netz weiter. Dadurch braucht das Modell keinen eigenen Kopierbefehl, um einen geschriebenen Wert an die nächste Struktur zu übergeben.

## Ein erster prinzipieller Rundgang durch die Suppe

Der Kandidatensatz reicht bereits grundsätzlich für eine elementare Erkundungskette. Ein Netz könnte aus seiner Genomtopologie einen ersten Wert hervorbringen, ihn als RAM-Adresse verwenden, den gelesenen Inhalt in `Z` schreiben, die Adresse per `ADD` verändern und anschließend eine weitere Stelle untersuchen.

```text
G-derived address seed
      |
      v
  RAM-read ----> Z-write
      |
     ADD
      |
      v
 nächste RAM-Adresse
```

Das war kein fertiges Programm und noch keine implementierbare Runtime. Vor allem fehlte weiterhin die Antwort darauf, wann welcher Funktionspunkt feuert, wie mehrere Eingänge zusammenfinden und was bei Zyklen oder konkurrierenden Schreibzugriffen geschieht. Aber zum ersten Mal war sichtbar, wie aus sehr kleinen vererbbaren Beziehungen ein funktionaler Datenweg entstehen könnte.

Der gedankliche Weg des Tages war damit:

```text
„Was ist P?“
      -> Welche Umwelt ist wirklich elementar?
      -> gemeinsame RAM-Suppe
      -> geschütztes Innen und adressierbare Membran
      -> primitive Funktionspunkte
      -> P als gerichtete Datenflusskante A.out → B.in
      -> viele P als Datenflussnetz
```

## `Z`: leerer Anfang und Lebensgeschichte

Die zunächst angenommene zufällige Initialisierung wurde verworfen. Eine Entität startet mit `G = Genom`, `Z = leer` und `S = Startenergie`. Ihre ersten Aktionen können nur aus `G` hervorgehen; erst deren Ergebnisse können nach `Z` geschrieben werden. `Z` ist damit der beschreibbare erworbene interne Zustand und entsteht ausschließlich durch die konkrete Ausführungsgeschichte. Ein ungeeignetes Genom, das keine ausreichend energiebringenden Zustände erschließt, verbraucht seine Startenergie und stirbt aus; das ist erwünschter Selektionsdruck.

Für „neue Information“ wurde eine absichtlich minimale Definition gewählt: Ein Eintrag ist neu, wenn er noch nicht in `Z` vorhanden ist. Ein neuer Z-Eintrag kann zu einem supervisorseitigen Energiegewinn `ΔS` führen. Sein Ertrag sättigt sich auf zwei unabhängigen Wegen: Identische Inhalte liefern bei Wiederholung zunehmend weniger Energie, und auch fortlaufend neue Inhalte aus derselben Quelle liefern mit deren wiederholter Nutzung zunehmend weniger Energie. Eine ständig wechselnde Uhr oder ein anderer unendlicher Datenstrom bleibt nutzbar, ernährt die Entität aber nicht dauerhaft mit vollem Neuheitsbonus. Wie beide Sättigungen mathematisch verlaufen und wie Quellen semantikfrei identifiziert werden, ist noch nicht entschieden.

Der Supervisor prüft dabei keine Bedeutung, Wahrheit oder Nützlichkeit. Genau hier entstand der stärkste Widerspruch zum bisherigen Konzept. EVE hatte zuvor den Satz geprägt:

> Information ist keine Nahrung. Erkenntnis ist Nahrung.

Die neue Regel belohnt zunächst aber Information im schwächsten syntaktischen Sinn. Inhalts- und Quellensättigung begrenzen bloße Wiederholung und endlos variierende Einzelquellen, definieren jedoch noch keine Vorhersage, Bestätigung oder Reproduzierbarkeit. Das wurde nicht sprachlich geglättet: Für die erste RAM-Suppen-Ökonomie ist es eine bewusste operative Näherung. Die anspruchsvollere Erkenntnisökonomie bleibt Forschungsziel und möglicher späterer Ausbau, beschreibt aber nicht die aktive Minimalregel.

## Ein Hintertürchen, das keines sein soll: `Z -> G`

Der getrennte Charakter von Genom und Lebenserfahrung bleibt erhalten. Trotzdem soll ein Pfad `Z -> G` nicht erst später architektonisch unmöglich geworden sein. Dafür wurde `A_ZG` als seltene mögliche genomische Disposition benannt.

`A_ZG` ist keine globale Lernfunktion. Sie kann in Population 0 vollständig fehlen und nur als Möglichkeit im Genomraum existieren, etwa erreichbar durch Mutation. Eine denkbare spätere Funktion wäre, häufig wiederkehrende Muster aus `Z` genetisch zu assimilieren. Ob eine solche Struktur entsteht, überlebt und sich verbreitet, soll nicht der Supervisor entscheiden, sondern die Evolution.

Die technische Mechanik ist noch offen. Insbesondere ist ungeklärt, wie Z-Werte in gültige P-Kanten übersetzt würden und wie verhindert wird, dass aus dem vorgesehenen Anschluss doch eine versteckte automatische Vererbung erworbener Zustände wird.

## Reproduktion bleibt Physik, nicht Zucht

Die früheren Reproduktionsregeln wurden nicht verworfen. Eltern müssen die reproduktive Konstellation aktiv hervorbringen; der Supervisor ist weiterhin Geburtskanal statt Züchter. Er prüft Bedingungen, bilanziert Energie, rekombiniert die real vorhandenen Genome und mutiert anschließend.

Neu ist die Bedeutung des vererbten Materials: Der gemeinsame Elternpool enthält nun Kanten eines Netzes. Damit wird eine alte Annahme fraglich. Häufige `P` haben weiterhin eine höhere Chance, aus dem Elternpool gezogen zu werden. Aber dass ihr relativer Anteil automatisch ihre phänotypische Stärke bestimmt, folgt bei Netzkanten nicht mehr. Mehrfachkanten könnten Gewicht, parallele Signale oder lediglich Redundanz bedeuten – das ist neu zu entscheiden.

## Stand am Ende des Tages

Entschieden oder deutlich konkretisiert waren:

- RAM-Suppe als erste gemeinsame Umwelt,
- Schutz von `G` und `Z`, vollständige Supervisor-Schreibkontrolle über das per `S-read` wahrnehmbare `S`,
- Membran als kontrolliertes adressierbares Interface,
- `P: A.out → B.in` als kleinste vererbbare gerichtete Datenflusskante,
- Verhalten aus einem Netz vieler `P`,
- leeres `Z` bei Geburt und Aufbau ausschließlich durch die eigene Ausführungsgeschichte,
- syntaktische individuelle Neuheit mit Inhalts- und Quellensättigung, ohne semantische Supervisorbewertung,
- technische Anschlussfähigkeit eines seltenen, zunächst inaktiven `A_ZG`.

Arbeitshypothesen blieben der konkrete Satz primitiver Funktionspunkte, Entity-ID an einem Membranoffset und die genaue Rolle durchgereichter Schreibwerte.

Offen blieben vor allem Taktung und Ausführung des Netzes, Z-Adressierung, Membranlayout, Neuheitsgedächtnis, Belohnungsfunktion, Energiekosten, reproduktive Signale und die Mechanik genetischer Assimilation.

Der Tag beantwortete „Was ist `P`?“ nicht mit einem einzelnen Opcode. Die Antwort wurde stattdessen räumlich: erst eine Suppe, dann eine Grenze, dann Funktionspunkte – und zwischen ihren Ein- und Ausgangsports vererbbare gerichtete Datenflusskanten.
