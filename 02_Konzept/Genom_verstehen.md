# Das EVE-Alife-Genom verstehen

Diese Einführung erklärt das Genom-Modell von EVE-Alife ohne Vorwissen. Sie
beschreibt den vorläufig eingefrorenen P1-Stand und ergänzt die technische
Spezifikation; sie ersetzt sie nicht.

> **Kurzfassung:** Ein Genom ist hier kein Text und keine Befehlsliste. Es ist
> eine vererbbare Sammlung einfacher Arbeitsstellen, ihrer gerichteten
> Verbindungen und eines Aktivitätswerts. Während eines Lebens fließen Werte
> durch diese Struktur. Welche Wirkung daraus entsteht, hängt außerdem vom
> momentanen Zustand und von der Umwelt ab.

## 1. Vier Dinge vorweg

Für das weitere Verständnis reichen zunächst diese vier Unterscheidungen:

```text
im Genom gespeichert                 entsteht erst während des Lebens

Funktionspunkte                      K: kurzfristig anliegende Signale
gerichtete Kanten P                  Z: dauerhaft gespeicherter Zustand
Basisaktivität A₀                    S: aktuelle Energie
                                     gelesene Werte aus RAM und Membranen
```

`G` ist das **Genom**. Es wird vererbt. `K`, `Z` und `S` gehören nicht zum
Genom. Ein Kind beginnt mit leerem `K`, leerem `Z` und einer bilanzierten
Startenergie. Diese Trennung ist wichtig: Ein geerbter Aufbau ist nicht
dasselbe wie die Erlebnisse und Ergebnisse, die später daraus entstehen.

## 2. Der kleinste Baustein: ein Funktionspunkt

### Was ist das?

Ein Funktionspunkt ist eine einzelne, sehr einfache Arbeitsstelle. Er kann zum
Beispiel eine feste Zahl liefern, zwei Zahlen addieren, einen Wert aus der
Umwelt lesen oder einen Wert in den persönlichen Speicher schreiben.

Ein Funktionspunkt ist **keine** vollständige Fähigkeit wie „suche Nahrung“.
Er erledigt nur seine primitive Einzelaufgabe.

### Warum gibt es ihn?

EVE-Alife soll komplexeres Verhalten nicht als fertigen Befehl vorgeben.
Deshalb stellt die Welt nur elementare Operationen bereit. Erst ihre
Verschaltung kann eine größere Wirkung ergeben.

### Wie sieht das aus?

```text
                  Eingänge       Funktionspunkt       Ausgang
                     a ─────────┐
                                ├──► [ ADD #7 ] ─────► value
                     b ─────────┘
```

`ADD #7` bedeutet: Dies ist die konkrete ADD-Instanz mit der innerhalb dieses
Genoms eindeutigen ID `7`. Ein zweiter Punkt `ADD #12` wäre trotz gleicher
Operation ein anderer Genombestandteil.

Die beschrifteten Anschlussstellen heißen **Ports**. `ADD` besitzt die
Eingangsports `a` und `b` und den Ausgangsport `value`.

### Mini-Beispiel

```text
[ CONST #1: 4 ] ──► gibt immer den Wert 4 aus
```

`CONST` benötigt keinen Eingang. Sein Wert `4` ist bei dieser konkreten
Instanz im Genom gespeichert. Normale Abläufe während des Lebens ändern ihn
nicht.

### Technische Bedeutung im P1-Code

Ein Funktionspunkt wird als `Node` gespeichert:

```text
Node(id, kind, constant)
```

- `id` unterscheidet Instanzen innerhalb eines Genoms.
- `kind` nennt den primitiven Typ.
- `constant` wird nur für `CONST` benötigt und enthält dessen erblichen Wert.

Der aktuelle Code kennt:

| Typ | Alltagsbeschreibung |
| --- | --- |
| `CONST` | erblichen festen Wert liefern |
| `S_READ` | eigene aktuelle Energie lesen |
| `Z_READ`, `Z_WRITE` | persönlichen dauerhaften Zustand lesen oder schreiben |
| `RAM_READ`, `RAM_WRITE` | gemeinsame RAM-Suppe lesen oder schreiben |
| `MEM_READ`, `MEM_WRITE` | kontrollierte eigene Membranschnittstelle benutzen |
| `ADD`, `SUB`, `XOR`, `EQ` | zwei Werte elementar verarbeiten oder vergleichen |
| `GATE` | Wert nur bei einer Nichtnull-Bedingung weitergeben |
| `PAUSE` | Eingang verbrauchen und keinen Wert ausgeben |

Die genaue Portliste steht im Code zentral in `PORTS`. Viele dieser Typen und
Signaturen sind im allgemeinen Grundkonzept noch Arbeitshypothesen; sie sind
aber im gegenwärtigen Prototyp konkret implementiert.

## 3. Die Verbindung: eine gerichtete Kante `P`

### Was ist das?

Ein Funktionspunkt allein weiß nicht, wohin sein Ergebnis gehen soll. Eine
Linie mit Pfeil verbindet deshalb einen Ausgang eines Punktes mit einem
Eingang eines anderen Punktes:

```text
[ CONST #1: 4 ] ───────────────► [ RAM_READ #2 ]
        value        Kante P          address
```

Die Linie ist die **Kante**. Sie bedeutet praktisch: Gibt Punkt `#1` einen
Wert am Ausgang `value` aus, wird dieser Wert an den Eingang `address` von
Punkt `#2` übertragen. Im Beispiel liest `RAM_READ #2` dadurch RAM-Adresse 4.

### Warum gibt es sie?

Die Kanten legen fest, welcher erzeugte Wert auf welche spätere Operation
wirken kann. Ohne Kante verfällt ein ausgegebener Wert. Mit anderen Kanten
könnte dieselbe `4` beispielsweise als Zahl für eine Addition oder als
Adresse im persönlichen Speicher dienen.

### Technische Bedeutung

Eine Kante wird im Code als `Edge` mit vier Angaben gespeichert:

```text
Edge(source, source_port, target, target_port)
```

Für das Bild oben lautet sie:

```text
Edge(1, "value", 2, "address")
```

Die Richtung ist nicht umkehrbar. Die Validierung verlangt, dass beide
Instanz-IDs vorhanden sind und dass Ausgangs- und Eingangsport zum jeweiligen
Funktionspunkttyp passen. Selbstverbindungen und Kreise sind zulässig.

`P` ist die Bezeichnung des Konzepts für eine solche gerichtete
Datenflusskante. Ein einzelnes `P` bedeutet weder „lesen“ noch „suchen“ oder
„fortpflanzen“. Seine Wirkung ergibt sich erst daraus, welche konkreten Ports
welcher konkreten Instanzen es verbindet.

## 4. Mehrere Punkte werden zu einem Datenflussnetz

Nun werden drei einfache Arbeitsstellen verbunden:

```text
[ CONST #1: 4 ] ── address ──► [ RAM_READ #2 ]
        │                              │
        │ address                      │ value
        ▼                              ▼
                         [ Z_WRITE #3 ]
```

Genauer sind dies drei Kanten:

```text
#1.value ──► #2.address
#1.value ──► #3.address
#2.value ──► #3.value
```

Die feste `4` bestimmt hier sowohl die gelesene RAM-Adresse als auch die
Zieladresse im persönlichen Speicher. Der gelesene RAM-Wert wird zum zweiten
Eingang von `Z_WRITE` geleitet. Sobald dort Adresse und Wert vorliegen, kann
`Z_WRITE` den Wert in `Z[4]` ablegen.

Das Netz ist trotzdem keine feste Befehlsfolge. Der Supervisor wählt unter
allen gerade ausführungsbereiten Punkten semantikfrei und durch den Lauf-Seed
reproduzierbar zufällig aus. Eingangslose Punkte wie `CONST` sind immer
bereit. Ein Punkt mit Eingängen wird bereit, sobald an allen benötigten Ports
ein Signal liegt.

## 5. Wo wartet ein Wert? Der Signalzustand `K`

Wenn eine Kante einen Wert anliefert, wird er nicht im Genom gespeichert. Er
liegt vorübergehend am Zielport im Signalzustand `K`:

```text
K["3:address"] = 4
K["3:value"]   = gelesener RAM-Wert
```

Für jeden Eingangsport gibt es höchstens einen solchen Platz. Ein später
ankommender Wert überschreibt dort einen noch nicht verbrauchten älteren Wert.
Sobald der Funktionspunkt ausführt, verbraucht und leert er seine Eingänge.

`K` kann über Heartbeat-Grenzen hinweg Werte behalten, ist aber kein frei
adressierbarer Speicher, wird nicht vererbt und ist bei Geburt leer. Für eine
bewusste dauerhafte Ablage muss das Netz `Z_WRITE` ausführen.

## 6. Was ist eine Funktionsgruppe?

### Die kurze, wichtige Antwort

**„Funktionsgruppe“ ist im aktuellen EVE-Alife-Konzept und im P1-Code kein
definierter Genombestandteil.** Es gibt dort kein Feld, keinen Typ und keine
zusätzliche Gruppennummer dieses Namens. Deshalb wäre es eine neue Regel, den
Begriff nachträglich als feste Einheit zu definieren.

Zwei tatsächlich vorhandene Begriffe können leicht damit verwechselt werden:

1. **Zusammenhängende Netzkomponente:** Funktionspunkte, die über Kanten
   direkt oder mittelbar miteinander verbunden sind. Im aktuellen P1-Code
   werden solche Komponenten bei der Rekombination als ganze Fragmente
   behandelt.
2. **Reproduktionsgruppe:** zwei oder drei lebende Entitäten mit gegenseitig
   passenden Partnerslots. Das ist eine Gruppe von Wesen, keine Gruppe von
   Funktionspunkten im Genom.

### Wie sieht eine zusammenhängende Komponente aus?

```text
Komponente A                         Komponente B

[ CONST ] ──► [ RAM_READ ]           [ S_READ ] ──► [ PAUSE ]
      └──────────► [ Z_WRITE ]

             keine Kante zwischen A und B
```

Die Bezeichnungen „Fragment A“, „Fragment B“ und „Fragment C“ im
P1-Startgenom sind erklärende Namen im Quelltext. Sie sind nicht als
Funktionsgruppen-Metadaten im `Genome`-Objekt gespeichert. Der Code ermittelt
Zusammenhang allein aus den tatsächlich vorhandenen Kanten.

### Dokumentierter Klärungsbedarf

Wenn mit „Funktionsgruppe“ künftig etwas anderes als eine zusammenhängende
Komponente gemeint sein soll, benötigt das Projekt dafür eine ausdrückliche
Konzeptentscheidung. Diese Einführung nimmt sie nicht vor.

## 7. Jetzt das Ganze: das Genom `G`

### Was ist das?

Das Genom ist der vererbbare Aufbau, mit dem ein Wesen startet. Man kann es
sich als Bauplan für mögliche Datenwege vorstellen — nicht als aufgezeichnetes
Leben und nicht als fertiges Drehbuch.

### Warum gibt es das?

Unterschiedliche Genome können Werte anders erzeugen, verbinden, lesen,
speichern und schreiben. Dadurch können in derselben Umwelt unterschiedliche
Wirkungen entstehen. Bei der Fortpflanzung werden Strukturen rekombiniert und
selten mutiert. So kann die Umwelt indirekt darüber entscheiden, welche
erblichen Strukturen häufiger Nachkommen hinterlassen.

### Tatsächliche Struktur im Code

```text
GENOM G
│
├── nodes: Funktionspunkt-Instanzen F
│     └── je Instanz: ID, Typ, bei CONST zusätzlich der feste Wert
│
├── edges: gerichtete P-Kanten
│     └── je Kante: Quell-ID/-Port und Ziel-ID/-Port
│
└── activity_base: Basisaktivität A₀
```

Es gibt **keine** gespeicherte Liste von Funktionsgruppen. Ebenfalls nicht im
Genom liegen aktuelle Energie, `K`, `Z`, Partnerslots, Lebensalter,
RAM-Inhalte, frühere Beobachtungen oder bereits ausgeführte Handlungen.

Der Code verwendet zwei Größen:

```text
Nₚ = Anzahl der Kanten
N_G = Anzahl der Funktionspunkte + Anzahl der Kanten
```

`A₀` ist ein einzelnes erbliches und mutierbares Metadatum. Es zählt im
Konzept nicht zur variablen Größe `N_G`.

## 8. Ein möglichst kleines vollständiges Beispielwesen

Das folgende Beispiel ist kein zusätzliches Naturgesetz und kein neues
Startgenom. Es ist ein gültiges kleines Genom aus ausschließlich bereits
implementierten P1-Bausteinen. Sein einziger Zweck ist, den bestehenden
Mechanismus vollständig zu zeigen.

### 8.1 Genotyp: Was ist gespeichert?

```text
Funktionspunkte

#1  CONST(4)
#2  RAM_READ
#3  Z_WRITE

Kanten

#1.value ──► #2.address
#1.value ──► #3.address
#2.value ──► #3.value

Basisaktivität

A₀ = 8
```

Als Code-Daten entspräche das:

```python
Genome(
    nodes=[
        Node(1, "CONST", 4),
        Node(2, "RAM_READ"),
        Node(3, "Z_WRITE"),
    ],
    edges=[
        Edge(1, "value", 2, "address"),
        Edge(1, "value", 3, "address"),
        Edge(2, "value", 3, "value"),
    ],
    activity_base=8,
)
```

Dieses Wesen besitzt eine zusammenhängende Komponente. Es besitzt keine im
Genom gespeicherte „Funktionsgruppe“.

### 8.2 Auswirkung: Was kann während eines Heartbeats geschehen?

Der konkrete Auswahlpfad hängt vom Seed und von den gleichzeitig bereiten
Punkten ab. Eine mögliche, vollständig regelgerechte Folge ist:

1. Der Supervisor zieht den Lebensunterhalt aus Grund-, Genom- und
   Alterskosten von `S` ab.
2. Aus `A₀ = 8` und drei Kanten berechnet der aktuelle Code das Budget
   `floor(8 / sqrt(3)) = 4` Ausführungsversuche, mindestens jedoch einen.
3. Zunächst ist nur `CONST #1` bereit. Es gibt `4` aus.
4. Seine zwei Kanten legen die `4` in `K` an `#2.address` und `#3.address`.
5. Nun sind `CONST #1` und `RAM_READ #2` bereit. Wird `RAM_READ #2`
   ausgewählt, liest es `RAM[4]` und sendet den gefundenen Wert an
   `#3.value`.
6. Sobald `#3.address` und `#3.value` belegt sind, ist `Z_WRITE #3` bereit.
   Wird es innerhalb des Budgets ausgewählt, speichert es den Wert in `Z[4]`.

```text
GENOTYP                              MÖGLICHE AUSWIRKUNG

CONST-Wert 4                         Adresse 4 wird erzeugt
3 gerichtete Kanten        ─────►    RAM[4] wird gelesen
A₀ = 8                               gelesener Wert kann in Z[4] landen
```

Das Wort „kann“ ist hier wesentlich. Die Auswahl ist zufällig, aber mit
demselben Seed reproduzierbar. `CONST` bleibt stets bereit und kann erneut
gezogen werden. Darum garantiert dieses Genom nicht, dass `Z_WRITE` in jedem
einzelnen Heartbeat tatsächlich ausführt.

Ein erfolgreicher erster externer oder seit dem letzten Lesen veränderter
RAM-Wert kann nach der aktuellen Minimalökonomie Energie liefern. Ein
unveränderter Wert oder ein Wert mit eigener Entity-ID in seiner Urheberkette
liefert keine solche Belohnung. Das Schreiben nach `Z` selbst liefert keine
Energie.

## 9. Vom Genom zum Verhalten

Für ein beliebiges Wesen gilt im aktuellen Prototyp vereinfacht:

```text
Genom G
  │  bestimmt Punkte, Kanten und A₀
  ▼
ausführungsbereite Punkte + kurzfristige Werte K
  │  semantikfreie, seed-reproduzierbare Auswahl
  ▼
primitive Operationen
  │
  ├── verändern eventuell Z
  ├── lesen oder verändern eventuell RAM/Membran
  └── können Informationsbelohnungen und damit S beeinflussen
  ▼
beobachtbare Wirkung und weitere Ausführungsmöglichkeiten
```

Der Supervisor stellt die allgemeine Physik bereit: Aktivierung, Portlogik,
Energieabrechnung, geschützte Speicher, Reproduktionsprüfung, Rekombination
und Mutation. Er schreibt dem Wesen aber kein Ziel wie „erkunde“ vor und wählt
keine Operation danach aus, ob sie nützlich erscheint.

## 10. Das sieht nicht nur aus wie ein neuronales Netz

Punkte und Pfeile erinnern optisch an ein neuronales Netz. Diese Zeichnung
rechtfertigt aber keine Übernahme neuronaler Begriffe. Im dokumentierten
EVE-Alife-Stand gibt es insbesondere keine Neuronen, Aktivierungsfunktionen,
Trainingsphase, Gradienten oder erlernten Kantengewichte.

Die Punkte führen benannte primitive Operationen aus. Die Kanten transportieren
konkrete ganzzahlige Werte zwischen benannten Ports. Eine Kante besitzt im
aktuellen Code kein Gewicht. Lernen während des Lebens verändert das Genom
nicht; der vorgesehene Pfad `Z -> G` ist konzeptionell anschlussfähig, aber
derzeit inaktiv und nicht implementiert.

## 11. Vererbung: Was bekommt ein Kind?

Bei einer gültigen Reproduktionskonstellation erzeugt der Supervisor ein
Kindergenom aus elterlicher Struktur. Das Kind übernimmt nicht `K`, `Z` oder
die Erlebnisse seiner Eltern.

Im aktuellen P1-Code geschieht vereinfacht:

1. Eine Zielgröße wird um die Genomgröße eines zufällig gewählten Elternteils
   gezogen und begrenzt.
2. Aus allen Eltern werden die über Kanten zusammenhängenden Komponenten
   ermittelt.
3. Passende ganze Komponenten werden zufällig ohne Zurücklegen ausgewählt.
4. Ihre Instanz-IDs werden für das Kind neu und eindeutig vergeben; ihre
   inneren Kanten bleiben erhalten.
5. `A₀` stammt von einem zufällig gewählten Elternteil.
6. Danach findet mit der konfigurierten sehr kleinen Wahrscheinlichkeit genau
   ein Mutationsvorgang statt.

Mehrfach real vorhandene Strukturen bieten entsprechend mehr reale
Auswahlmöglichkeiten. Ein externes Gewichtungsfeld dafür gibt es nicht.

### Abweichung zwischen Konzept und P1-Implementierung

Das Grundkonzept beschreibt ein kleineres zusammenhängendes Fragment, das von
einer gezogenen Startinstanz entlang realer Kanten bis zu einer Zielgröße
wächst. Der aktuelle P1-Code schneidet eine zusammenhängende Komponente
dagegen nicht an, sondern behandelt die **gesamte Komponente atomar**.

Diese Einführung entscheidet nicht, welche Variante künftig maßgeblich sein
soll. Für Aussagen über tatsächlich ausgeführte P1-Läufe gilt das Verhalten
des Codes; für die allgemeine Zielrichtung bleibt die abweichende Beschreibung
im Grundkonzept sichtbar.

## 12. Genau eine minimale Mutation

Wir mutieren das Beispielwesen einmal. Voraussetzung ist, dass bei der Geburt
überhaupt das seltene Mutationsereignis eintritt und darin die Kantenmutation
gewählt wird. Der aktuelle Code kann dann genau ein Ende einer vorhandenen
Kante auf einen gültigen Port umhängen.

Hier wird nur die Quelle der dritten Kante geändert:

```text
VORHER                              NACHHER

#2.value ──► #3.value               #1.value ──► #3.value

#3 erhält gelesenen RAM-Wert         #3 erhält dort ebenfalls die Konstante 4
```

Das vollständige Vorher/Nachher-Bild:

```text
VORHER                              NACHHER

#1 ──► #2 ──► #3                    #1 ──► #2
 └──────────► #3                     ├────► #3.address
                                      └────► #3.value
```

### Was wurde im Genom verändert?

Nur Quellinstanz und Quellport einer Kante wurden von `#2.value` auf
`#1.value` umgehängt.

### Was blieb gleich?

- dieselben drei Funktionspunkte und Instanz-IDs,
- der erbliche `CONST`-Wert `4`,
- die Zahl der Kanten,
- `A₀ = 8`,
- alle übrigen Kanten.

`K`, `Z` und `S` sind keine mitmutierten Genombestandteile. Das Kind beginnt
ohnehin mit eigenem leerem `K` und `Z` sowie seiner bilanzierten Energie.

### Unmittelbare technische Folge

`RAM_READ #2` kann weiterhin `RAM[4]` lesen, sein Ergebnis besitzt aber keine
ausgehende Kante mehr und verfällt. `Z_WRITE #3` erhält für Adresse **und**
Wert die Konstante `4`; es kann deshalb `4` nach `Z[4]` schreiben. Der
gelesene Umweltwert gelangt nicht mehr dorthin.

### Mögliche Verhaltens- und Evolutionsfolge

Das mutierte Wesen kann RAM weiterhin lesen und dadurch unter passenden
Bedingungen Energie erhalten. Es bewahrt den gelesenen Wert aber nicht mehr
an dieser Stelle in `Z`. Falls ein späterer Netzteil genau diesen gespeicherten
Umweltwert benötigt hätte, wäre dieser Datenweg nun unterbrochen. In einer
anderen Umwelt oder Netzstruktur könnte die Änderung neutral sein.

Evolution verfolgt dabei keine Absicht. Hinterlässt eine erbliche Variante
unter den gegebenen Bedingungen mehr fortpflanzungsfähige Nachkommen, kann
sie in späteren Generationen häufiger werden. Führt sie zu weniger oder gar
keinen Nachkommen, kann sie verschwinden. Eine einzelne Mutation garantiert
weder Vorteil noch Nachteil.

## 13. Was kann im aktuellen Code mutieren?

Trifft das seltene Mutationsereignis nach der Rekombination ein, wählt der
Code genau eine der für dieses Genom verfügbaren Klassen:

- **Basisaktivität:** `A₀` steigt oder sinkt um 1, aber nicht unter 1.
- **Funktionspunkt:** Ein `CONST`-Wert kann um 1 steigen oder sinken. Andernfalls
  kann der Typ zu einem anderen implementierten Typ mit exakt derselben
  Ein-/Ausgangssignatur wechseln, sofern es einen solchen Typ gibt.
- **Kante:** Entweder das Quellende oder das Zielende einer bestehenden Kante
  wird auf einen zum Port passenden Funktionspunkt umgehängt.

Der aktuelle Mutationscode fügt keine Funktionspunkte oder Kanten hinzu und
löscht keine. Die Genomgröße kann sich bei der Rekombination ändern, nicht
durch diese konkrete P1-Mutationsroutine.

## 14. Gesicherte Grenzen und offene Punkte

Damit Erklärung nicht unbemerkt zu neuer Spezifikation wird, sind diese
Grenzen ausdrücklich festzuhalten:

- „Funktionsgruppe“ ist derzeit nicht definiert oder gespeichert.
- Konzept und Code unterscheiden sich bei der Bildung vererbter Fragmente:
  lokal wachsender Teilgraph gegenüber ganzer zusammenhängender Komponente.
- Die exakte allgemeine Formel, die `A₀`, Genomgröße und finanzierbare
  Aktivität verbindet, ist im Konzept offen. Der P1-Code verwendet konkret
  `max(1, floor(A₀ / sqrt(max(1, Nₚ))))`.
- Das Konzept lässt Ausführungs- und Kantenkosten prototypspezifisch. In der
  aktuellen Standardkonfiguration sind beide `0`; unterlineare
  Genom-Unterhaltskosten werden pro Heartbeat berechnet.
- Die Bedeutung doppelter identischer Kanten bleibt im Grundkonzept als
  offene Frage geführt. Der Code speichert und verarbeitet Listeneinträge;
  daraus wird hier keine zusätzliche allgemeine Bedeutung abgeleitet.
- `GATE` und mehrere weitere primitive Typen sind im Prototyp implementiert,
  im allgemeinen Konzept aber weiterhin als Arbeitshypothese markiert.

## 15. Selbsttest für Leserinnen und Leser

Nach dieser Einführung sollte sich das Modell so zusammenfassen lassen:

> Das Genom speichert konkrete einfache Funktionspunkte, gerichtete Kanten
> zwischen ihren Ports und die Basisaktivität. Werte fließen während der
> Simulation über diese Kanten und warten kurz in `K`. Punkte können daraus
> rechnen, Umwelt und Membran lesen oder schreiben und Werte dauerhaft in `Z`
> ablegen. `K`, `Z`, Energie und Erlebnisse gehören nicht zum Genom. Bei der
> Fortpflanzung werden im P1-Code zusammenhängende Komponenten kombiniert und
> danach selten einzelne genetische Angaben mutiert. Andere Strukturen können
> dadurch andere Wirkungen haben und unter denselben Umweltbedingungen
> unterschiedlich viele Nachkommen ermöglichen — ohne Ziel oder Absicht der
> Evolution.

## 16. Technische Vertiefung und Quellen

- [Grundkonzept, besonders Abschnitt 6 und 10](Grundkonzept_Arbeitsentwurf.md)
- [P1-Genomentwurf und vorläufiger Abschlussstand](../04_Prototypen/P1_GENOMENTWURF.md)
- [Technische Spezifikation des Prototyps](../04_Prototypen/v0.1/SPEZIFIKATION.md)
- [Bedienung und Beobachtung des Prototyps](../04_Prototypen/v0.1/README.md)
- [Aktuelle Referenzimplementierung](../04_Prototypen/v0.1/eve_core.py)
