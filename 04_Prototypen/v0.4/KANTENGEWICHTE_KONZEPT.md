# Konzeptionelle Genomerweiterung: evolvierbare Kantengewichte

Status: für v0.4 festgelegt und im Simulationskern implementiert.

## Ziel und Nicht-Ziel

Gerichtete Genomkanten sollen künftig ein vererbbares und mutierbares Gewicht
besitzen können. Diese Eigenschaft wird nicht eingeführt, um ein bestimmtes
Verhalten hervorzubringen. Sie öffnet lediglich einen zusätzlichen
Evolutionsraum. Ob Gewichte nützlich, neutral oder nachteilig sind, entscheidet
ausschließlich Selektion im jeweiligen Biotop.

Die Rumpfamöben behalten ihre bestehende funktionierende Struktur. Sämtliche
vorhandenen und aus älteren Formaten geladenen Kanten besitzen zunächst das
neutrale Gewicht `0`. Dieses Gewicht schaltet eine Kante nicht ab, sondern
bezeichnet ausdrücklich ihr bisheriges Verhalten.

```text
negative Werte ← veränderte/hemmende Wirkung
                         0 = bisherige Wirkung
                                      veränderte/verstärkende Wirkung → positive Werte
```

Die Begriffe „hemmend“ und „verstärkend“ beschreiben den proportionalen Einfluss
auf den transportierten Zahlenwert.

## Exakte Bedeutung einer Kante im aktuellen Prototyp

Eine Kante ist derzeit eine gerichtete, portgenaue Transportverbindung mit
vier Angaben:

```text
(Quellinstanz, Quellport) → (Zielinstanz, Zielport)
```

Wenn ein Funktionspunkt feuert, erzeugt er je nach Typ Signale an benannten
Ausgangsports. Für jede ausgehende Kante geschieht anschließend:

1. Das Signal des bezeichneten Quellports wird gewählt.
2. Existiert an diesem Port kein Signal, transportiert die Kante nichts.
3. Andernfalls wird dasselbe Signal unverändert in den bezeichneten Zielport
   des flüchtigen K-Speichers geschrieben.
4. Sind danach alle Eingangsports des Zielpunkts belegt, kann dieser bei einer
   späteren zufälligen Auswahl feuern.

Ein Signal besteht aus einem vorzeichenbehafteten 64-Bit-Zahlenwert sowie
seiner Quellen- und Urheberprovenienz. Die Kante verändert derzeit keinen
dieser Bestandteile.

Mehrere Kanten auf denselben Zielport werden nicht summiert. Ein später
eintreffendes Signal überschreibt die dort wartende Belegung. Die zufällige
Ausführungsreihenfolge kann daher bei konkurrierenden Kanten relevant sein.
Belegte Ports bleiben über Ausführungsschritte und Heartbeats erhalten, bis
der Zielpunkt sie beim Feuern verbraucht oder ein anderes Signal sie
überschreibt. Rückkopplungen sind dadurch möglich.

Eine ausgehende Kante zählt unabhängig von ihrem transportierten Wert zu den
Ausführungskosten des Quellpunkts. Die Kantenzahl beeinflusst außerdem das
Aktivitätsbudget und die Genom-Unterhaltskosten.

## Minimaler Vertrag der geplanten Erweiterung

Das Gewicht gehört zur Kante und wirkt auf die Übertragung zwischen
Quell- und Zielport. Abstrakt gilt:

```text
übertragener Wert = T(Quellwert, Kantengewicht)
T(v, 0) = v
```

Für v0.4 ist die Funktion festgelegt als:

```text
T(v, w) = trunc(v × (100 + w) / 100)
```

`trunc` rundet gegen null. Das Ergebnis wird anschließend wie alle übrigen
Maschinenwerte auf die bestehende vorzeichenbehaftete 64-Bit-Darstellung
abgebildet. Damit bewirkt `w = 0` exakt 100 Prozent, `w = 100` 200 Prozent,
`w = -100` blockiert das Signal numerisch und Werte unter `-100` kehren sein
Vorzeichen um. Es gibt keine besondere Gewichtsunter- oder -obergrenze.

Weiterhin vorgesehen sind folgende Invarianten:

- Gewicht `0` erhält das bisherige Laufzeitverhalten exakt.
- Eine Kante bleibt bei Gewicht `0` vorhanden, aktiv und kostenwirksam.
- Die Gewichtung erfolgt vor dem Schreiben in den Zielport.
- Quellen- und Urheberprovenienz des Signals bleiben erhalten.
- Gewichte führen nicht automatisch zu Summierung, neuronaler Aktivierung
  oder gleichzeitiger Netzauswertung.
- Das Genom bleibt ein ereignisgesteuertes, portbasiertes Signalnetz.

## Vererbung, Mutation und Beobachtbarkeit

- Das Gewicht wird zusammen mit seiner Kante vererbt.
- Bei der Rekombination eines Segments bleiben die Gewichte seiner internen
  Kanten und ausgehenden Anschlusskanten erhalten.
- Eine Umverdrahtung ändert nicht implizit das Gewicht der Kante.
- Das Gewicht kann ausschließlich während der Genomerzeugung bei einer Geburt
  mutieren. Eine Gewichtsmutation ist eine zusätzliche Mutationsklasse neben
  den bereits vorhandenen Klassen.
- Der Änderungsbetrag `k >= 1` wird ohne feste Obergrenze mit
  `P(k) ∝ 1/k²` gezogen. Kleine Schritte dominieren; große Sprünge bleiben
  selten möglich. Das Vorzeichen des Schritts wird unabhängig mit gleicher
  Wahrscheinlichkeit gezogen.
- Es gibt keine bevorzugte Mutationsrichtung und keinen eingebauten Druck weg
  vom Neutralwert.
- Lupe, Genomvergleich, Abstammungsanalyse und Mutationsprovenienz müssen eine
  Gewichtsänderung als eigene genomische Veränderung ausweisen können.
- Genomfingerprints und kanonische Serialisierung berücksichtigen das Gewicht.
- Ältere Genome ohne Gewicht werden kompatibel als Gewicht `0` gelesen.

## Für spätere Genomrevisionen offen

Noch nicht festgelegt sind ein möglicher Einfluss des Gewichtsbetrags auf
Ausführungs- oder Unterhaltskosten und die Initialisierung künftig neu
entstehender Kanten. Im aktuellen Kern entstehen durch Mutation noch keine
neuen Kanten; sämtliche Rumpf- und Altformatkanten beginnen neutral bei `0`.
