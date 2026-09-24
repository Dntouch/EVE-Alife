# EVE-Alife – Prototyp v0.4

> **Status:** neu angelegter Arbeitsstand vom 23. September 2026. v0.4 basiert
> auf dem abgeschlossenen Prototyp v0.3; `../v0.3/` bleibt konserviert.

## Ziel

v0.4 untersucht evolvierbare Gewichte gerichteter Genomkanten. Die Erweiterung
soll kein gewünschtes Verhalten in die Amöben einbauen. Sie soll lediglich
ermöglichen, dass Evolution die Wirkung vorhandener Verbindungen graduell
verändern kann, falls dies unter den jeweiligen Umweltbedingungen einen Vorteil
bietet.

Der neutrale künftige Wert `0` ist verbindlich als heutiges Kantenverhalten
definiert. Er bedeutet weder „abgeschaltet“ noch „wirkungslos“.

## Ausgangsstand

Übernommen wurden:

- der vollständige v0.3-Fachkern,
- Supervisor und Run-Lebenszyklus,
- die EVE-Lupe mit Leitstand, Historie, Chronik, Stammbaum und Genomanalyse,
- die 58 automatisierten Tests des Abschlussstands.

Nicht übernommen wurden Run-Rohdaten, Caches und v0.3-Screenshots. Die
v0.4-Lupe liest weiterhin die konservierten v0.2- und v0.3-Run-Verzeichnisse.

## Implementierter v0.4-Kern

Kantengewichte sind evolutionär aktiv. Alle Rumpf- und Altformatkanten beginnen
neutral bei `0`. Bei einer Geburt kann eine vorhandene Kante eine eigene
Gewichtsmutation erfahren. Kleine Schritte dominieren gemäß `P(k) ∝ 1/k²`,
große Sprünge bleiben ohne feste Gewichtsgrenze möglich; beide Richtungen sind
gleich wahrscheinlich. Zur Laufzeit gilt `T(v,w) = trunc(v × (100+w) / 100)`.

Gewichte werden mit den Anschlusskanten ihrer Segmente vererbt, in Genomfingerprints und Checkpoints
gespeichert und von der Lupe einschließlich des direkten Genomvergleichs
angezeigt. Sie verändern derzeit weder Kantenkosten noch Genomgröße.

Die Vererbung arbeitet in v0.4 mit evolvierbaren Genomplätzen beliebiger Größe.
P1 startet mit drei Plätzen. Ein Architektur-Elternteil liefert die kindlichen
Loci; strukturell homologe Varianten aller Eltern werden bevorzugt gepaart und
je Locus vollständig vererbt. Eine vorgegebene Zielgenomgröße existiert nicht
mehr. Duplikation, Verlust, Teilung und Verschmelzung verändern selten die
Platzarchitektur. Offene platzübergreifende Kanten werden semantisch neu
angeschlossen oder verworfen; Quelle und Gewicht bleiben erhalten.

Die geprüfte heutige Bedeutung einer Kante und der Neutralitätsvertrag stehen
in [KANTENGEWICHTE_KONZEPT.md](KANTENGEWICHTE_KONZEPT.md). Die technische und
fachliche Abgrenzung zu v0.3 steht in [VERSIONSGRENZE.md](VERSIONSGRENZE.md).
Die revidierte Vererbungsentscheidung, das Segmentmodell und die semantische
Reparatur von Schnittkanten stehen in
[SEGMENTVERERBUNG_KONZEPT.md](SEGMENTVERERBUNG_KONZEPT.md).

## Skalierbarer Beobachtungspfad

Der erste große v0.4-Lauf erreichte 9.446 erzeugte und 8.761 lebende Amöben,
bevor der Prozess bei Tick 4.034 durch einen OOM-Abbruch endete. Die vollständige
[Laufanalyse](../../07_Laufergebnisse/v0.4/Lauf_001.md) trennt den biologischen
Populationsdurchbruch vom technischen Ende.

Die anschließende Wiederholung bestand den vollständigen Härtetest. Sie erreichte
Tick 5.000 mit 31.082 erzeugten und 28.264 lebenden Amöben, 29.842 verschiedenen
Genomen sowie 5,9 Millionen persistierten Ereignissen. Der Speicherpfad blieb
stabil; nun begrenzt der serielle Fachkern den Durchsatz. Eine einzelne
Slotverschmelzung begründete außerdem eine am Laufende 13 Amöben umfassende,
vollständig lebende Zwei-Slot-Linie. Die
[Analyse von Lauf 002](../../07_Laufergebnisse/v0.4/Lauf_002.md) dokumentiert
Ergebnis, Reproduktionsabweichung und die neuen Skalierungsgrenzen der Lupe.

Als Konsequenz für folgende Läufe wurde die Standard-Altersrate von `0,005` auf
`0,01` angehoben. Die Änderung soll alte Amöben früher energetisch belasten und
ist eine neue Versuchsbedingung, keine nachträgliche Umdeutung von Lauf 002. Der
historische Preset `v02-run16` bleibt unverändert bei `0,005`.

Der anschließende Vergleich zeigte die Empfindlichkeit dieser Stellschraube:
Mit `0,01` starb die Population bei Tick 2.134 aus, während sie mit `0,008`
Tick 5.000 mit 117 Lebenden erreichte. Die Population fiel dabei zunächst von
55 auf 19 und wuchs anschließend erneut. Die [Analyse von Lauf
003](../../07_Laufergebnisse/v0.4/Lauf_003.md) hält Altersfalle, Wellenverlauf
und Single-Core-Basiswerte fest. Eine feinere Abstimmung wird erst nach der
deterministischen Mehrkernumsetzung fortgesetzt.

Persistierte Ereignisse werden nun unmittelbar aus dem Simulationsspeicher
freigegeben. Das Live-Bild ist kompakt und auf zwei Aktualisierungen pro Sekunde
begrenzt; periodische wissenschaftliche Beobachtungen bleiben davon getrennt.
Status, Commit und Manifest werden am Messintervall gebündelt. Entitäten und
Genome werden nur bei ihrer Entstehung registriert.

## Testen

```bash
cd 04_Prototypen/v0.4
python3 -m unittest -v
python3 benchmark_performance.py --population 1000 --ticks 10
```

## Starten

```bash
python3 run.py --ticks 500
python3 supervisor.py
python3 lupe.py runs/DEINE-RUN-ID --port 8766
```

Für räumlich verteilte Gründer ohne vorgefertigte Umweltspielzeuge steht
`--ram-world bare` zur Verfügung. Der Modus behält lokale RAM-Koordinaten und
zufällige Startpositionen, erzeugt aber keine Steine, Blasen oder Schalter.

Große Läufe werden in der Lupe bewusst begrenzt dargestellt: Der Stammbaum lädt
ein Familienfenster um eine gewählte Amöbe (Eltern und Großeltern sowie Kinder
und Enkel, höchstens 400 Knoten), die RAM-Suppe zeichnet wählbar nur alle
5/10/25/50/100 Ticks neu, und der Evolutionsverlauf ergänzt nur neue
Messpunkte. Interaktive Ereignislisten sind serverseitig auf die jüngsten
50.000 passenden Ereignisse begrenzt.

Die deterministische Nutzung mehrerer Kerne für einen einzelnen Lauf ist in
`MULTICORE.md` spezifiziert. Ein naiver Prozesspool ist nicht freigeschaltet,
weil RAM-, Membran- und Kadaverzugriffe innerhalb eines Ticks heute
reihenfolgeabhängig sind.

## Bestandteile

- `eve_core.py`: ereignisgesteuerter Fachkern und Genom
- `run.py`, `run_store.py`: Run-Ausführung und Persistenz
- `supervisor.py`, `run_parameters.py`: kontrollierte Run-Steuerung
- `lupe.py`, `assets/v04.js`, `assets/v04.css`: Analyseoberfläche
- `benchmark_performance.py`: reproduzierbarer CPU- und Beobachtungsbenchmark
- `PERFORMANCE.md`: OOM-Ursache, Gegenmaßnahmen und Referenzmessung
- `MULTICORE.md`: deterministisches Snapshot-/Intent-Modell für 16 Worker
- `KANTENGEWICHTE_KONZEPT.md`: fachlicher Ausgangspunkt der Genomrevision
- `SEGMENTVERERBUNG_KONZEPT.md`: geplante Segmente und Anschlusskanten
- `test_*.py`: 68 Regressionstests einschließlich skalierbarer Persistenz
