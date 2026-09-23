# Versionsgrenze v0.3 → v0.4

`v0.3` ist mit Commit `2547064` konserviert. Seine Quell-, Dokumentations- und
Laufergebnisdateien werden für die Entwicklung von v0.4 nicht verändert.

Der Startstand von v0.4 wurde am 23. September 2026 aus den Quell- und
Dokumentationsdateien von v0.3 übernommen. Run-Daten, Python-Caches und der
v0.3-Screenshot-Satz wurden nicht kopiert. Die Lupe kann die konservierten
v0.2- und v0.3-Runs weiterhin lesen.

## Ziel der neuen Version

v0.4 ist die Genomrevision für evolvierbare Gewichte gerichteter Kanten. Die
Eigenschaft wird nicht eingebaut, um ein gewünschtes Verhalten zu erzeugen,
sondern um Evolution einen zusätzlichen möglichen Suchraum zu öffnen.

Der Ausgangsstand verhält sich zunächst exakt wie v0.3. Insbesondere gilt bis
zur bewussten Implementierung:

- Kanten besitzen zur Laufzeit noch kein Gewicht.
- Der neutrale künftige Wert `0` muss dem bisherigen Transport exakt entsprechen.
- Wertebereich, Kodierung, Mutationsschritt und mathematische Wirkung sind noch
  keine ausführbare Regel.
- Vor einer Formatänderung werden Laufzeitsemantik, Vererbung, Mutation,
  Fingerprint, Persistenz und Beobachtbarkeit gemeinsam festgelegt.

Das bisherige Run-Format 2 bleibt für den unveränderten Ausgangsstand gültig.
Sobald Kantengewichte persistiert werden, ist eine bewusste Formatentscheidung
erforderlich; sie wird nicht stillschweigend vorweggenommen.
