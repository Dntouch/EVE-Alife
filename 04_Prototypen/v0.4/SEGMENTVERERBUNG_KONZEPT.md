# Genomsegmente und Anschlusskanten

Status: fachlich festgelegt und im v0.4-Simulationskern implementiert.

## Revidierte Entscheidung

Die bisherige Regel, eine über Kanten vollständig zusammenhängende
Netzkomponente als unteilbare Vererbungseinheit zu behandeln, wird für v0.4
revidiert. Funktionaler Zusammenhang und erbliche Segmentierung sind
verschiedene Eigenschaften.

Die alte Regel erzeugt einen technischen Klippeneffekt. Auch die anschließend
erprobte Zielgenomgröße erwies sich als falsche Abstraktion: Nicht reparierbare
Schnittkanten hinterließen leere Kapazität und erzeugten einen systematischen
Schrumpfungsdrift. Die Gesamtgenomgröße ist deshalb ab jetzt Ergebnis der
Vererbung und Mutation, keine vor der Geburt gezogene Behältergröße.

## Segmentmodell

Ein Genom besteht künftig aus erblichen Segmenten. Ein Segment enthält:

- seine Funktionspunkte,
- seine internen Kanten,
- seine ausgehenden Anschlusskanten.

Interne Kanten besitzen Quelle und Ziel im selben Segment und werden mit dem
Segment unverändert übernommen. Eine Anschlusskante besitzt ihren Quellpunkt
im Segment und führt im Elterngenom zu einem anderen Segment. Sie gehört
erblich zum Quellsegment; Quellpunkt, Quellport und Kantengewicht bleiben bei
der Übernahme erhalten.

## Vererbungsplätze und Homologie

Die P1-Rumpfamöbe beginnt mit drei Vererbungsplätzen beliebiger Größe. Diese
drei Plätze sind nur die Ausgangsarchitektur; weder ihre Zahl noch ihre Größe
ist dauerhaft festgeschrieben.

Bei einer Geburt wird zunächst ein Architektur-Elternteil gezogen. Seine
vorhandenen Plätze bestimmen die kindlichen Loci. Für jeden Platz werden bei den
anderen Eltern homologe Varianten gesucht. Homologie bewertet ausschließlich
strukturelle Merkmale: Funktionspunkttypen, Kantentopologie, Ports und relative
Größe. Verhalten, Energieertrag oder vermeintlicher Nutzen gehen nicht in die
Bewertung ein. Ab einer dokumentierten Mindesthomologie wird zufällig eine der
gefundenen elterlichen Varianten vollständig vererbt.

Die Gesamtgenomgröße ergibt sich danach aus den tatsächlich geerbten Plätzen.
Es gibt keine Zielgenomgröße und kein Abschneiden zur Erfüllung einer
Kapazität.

## Semantische Reparatur einer Anschlusskante

Stammen zwei homologe Plätze des Kindes von verschiedenen Eltern, kann das
konkrete Ziel einer platzübergreifenden Anschlusskante fehlen. Nur solche
offenen Anschlusskanten werden neu verdrahtet:

1. Zuerst wird ein noch unbelegter Eingang mit exakt derselben Zielpunktart und
   demselben Zielport gesucht.
2. Fehlt ein exaktes Ziel, darf ein noch unbelegter Eingang derselben
   allgemeinen Portrolle verwendet werden. `a` und `b` bilden dabei gemeinsam
   die Rolle `operand`; alle anderen Portnamen sind ihre eigene Rolle.
3. Unter gleichwertigen Kandidaten wird zufällig gewählt.
4. Gibt es kein semantisch kompatibles, unbelegtes Ziel, entfällt die Kante.
5. Quellpunkt, Quellport und Kantengewicht bleiben erhalten.

Diese Semantik beschreibt Anschlussphysik, kein gewünschtes Verhalten: Sie
garantiert weder Lebensfähigkeit noch Nutzen und repariert keine fehlenden
Funktionsgruppen. Sie verhindert lediglich Verbindungen wie `condition` nach
`slot`, die im ersten v0.4-Lauf überwiegend bedeutungslosen Verdrahtungsmüll
erzeugten.

## Strukturmutation

Neben Inhaltsmutationen existiert eine seltenere Mutationsebene für die
Platzarchitektur:

- `slot_duplicate`: ein Platz wird mit seinen Punkten und Kanten dupliziert,
- `slot_delete`: ein Platz und seine Verbindungen gehen verloren,
- `slot_split`: Punkte eines Platzes werden auf einen neuen Platz verteilt,
- `slot_fuse`: zwei Plätze verschmelzen.

Eine Duplikation ist zunächst stark homolog zum Ursprung und kann anschließend
unabhängig mutieren. Damit können Zahl und Größe der Plätze evolutionär wachsen
oder schrumpfen, ohne eine gewünschte Richtung vorzugeben.

## Konkrete v0.4-Ausführung

- Jeder Funktionspunkt speichert eine positive Segment-ID.
- Das P1-Rumpfgenom besitzt drei ausdrücklich vergebene Vererbungsplätze.
- Bei alten Genomen ohne Segmentangabe bildet jeder Funktionspunkt zunächst ein
  eigenes Segment; dadurch wird keine unbekannte Zusammengehörigkeit erfunden.
- Ein zufällig gewählter Architektur-Elternteil bestimmt die vorhandenen Loci.
- Strukturell homologe elterliche Varianten werden bevorzugt gepaart; pro Locus
  wird eine vollständige Variante zufällig vererbt.
- Die Genomgröße entsteht aus den geerbten Varianten und Strukturmutationen.
- Segment-IDs werden im Kind kompakt und eindeutig neu vergeben.
- Eine Kante gehört zum Segment ihres Quellpunkts. Gewicht und Quellport werden
  unverändert übernommen.
- Fehlt an einer platzübergreifenden Anschlusskante das ursprüngliche Ziel, wird zuerst ein exakter,
  danach ein rollenkompatibler und stets unbelegter Eingang gesucht. Fehlt ein
  Kandidat, wird die Kante verworfen.
- Das Rekombinationsprotokoll bewahrt ursprüngliche, konkret aufgelöste und
  weggefallene Anschlusskanten.

## Noch offene Punkte

- ob die Homologieschwelle nach Laufdaten angepasst werden muss,
- ob zusätzlich Rekombination innerhalb stark homologer Plätze sinnvoll wird,
- ob mehrfach belegte Eingangsports künftig eine andere Laufzeitsemantik benötigen,
- ob die zunächst kleine Menge allgemeiner Portrollen weiter verfeinert werden muss.
