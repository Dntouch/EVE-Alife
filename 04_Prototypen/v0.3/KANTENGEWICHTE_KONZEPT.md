# Konzeptionelle Genomerweiterung: evolvierbare Kantengewichte

Status: fachlich vorgesehen, im Simulationskern noch nicht implementiert.

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

Die Begriffe „hemmend“ und „verstärkend“ beschreiben hier nur den vorgesehenen
Suchraum. Sie legen noch keine mathematische Operation fest.

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

Dieser Neutralitätsvertrag ist verbindlich. Die konkrete Funktion `T` bleibt
bis zur gemeinsamen Überarbeitung von Genomgröße, Redundanz,
Funktionsbausteinen und Mutationsmechanik offen.

Weiterhin vorgesehen sind folgende Invarianten:

- Gewicht `0` erhält das bisherige Laufzeitverhalten exakt.
- Eine Kante bleibt bei Gewicht `0` vorhanden, aktiv und kostenwirksam.
- Die Gewichtung erfolgt vor dem Schreiben in den Zielport.
- Quellen- und Urheberprovenienz des Signals bleiben erhalten.
- Gewichte führen nicht automatisch zu Summierung, neuronaler Aktivierung
  oder gleichzeitiger Netzauswertung.
- Das Genom bleibt ein ereignisgesteuertes, portbasiertes Signalnetz.

## Vererbung, Mutation und Beobachtbarkeit

Für die spätere Implementierung gilt:

- Das Gewicht wird zusammen mit seiner Kante vererbt.
- Bei der Rekombination eines Fragments bleiben dessen Kantengewichte erhalten.
- Eine Umverdrahtung ändert nicht implizit das Gewicht der Kante.
- Die Mutationsmechanik muss das Gewicht einer bestehenden Kante verändern
  können. Dies ist eine zusätzliche Möglichkeit neben Entstehung, Entfernung
  und Umverdrahtung von Kanten.
- Es gibt keine bevorzugte Mutationsrichtung und keinen eingebauten Druck weg
  vom Neutralwert.
- Lupe, Genomvergleich, Abstammungsanalyse und Mutationsprovenienz müssen eine
  Gewichtsänderung als eigene genomische Veränderung ausweisen können.
- Genomfingerprints und kanonische Serialisierung müssen das Gewicht
  berücksichtigen, sobald die Erweiterung implementiert wird.
- Ältere Genome ohne Gewicht werden dann kompatibel als Gewicht `0` gelesen.

## Bewusst offene Entscheidungen

Noch nicht festgelegt werden:

- Wertebereich und Bitbreite,
- Kodierung und Serialisierungsform,
- typische oder mögliche Mutationsschritte,
- Begrenzung, Sättigung oder Überlauf,
- die genaue Wirkung positiver und negativer Werte,
- ein möglicher Einfluss auf Ausführungs- oder Unterhaltskosten,
- die Behandlung eines Gewichts bei neu entstehenden Kanten.

Diese Entscheidungen dürfen nicht isoliert getroffen werden. Sie gehören in
die nächste gemeinsame Genomrevision. Bis dahin beschreibt dieses Dokument
eine vorgesehene Fähigkeit, aber keine bereits aktive biologische Regel.
