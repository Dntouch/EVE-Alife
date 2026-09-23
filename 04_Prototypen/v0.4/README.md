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

## Noch nicht implementiert

Kantengewichte sind im Ausgangsstand nicht evolutionär aktiv. Vor der
Implementierung werden gemeinsam festgelegt:

- mathematische Wirkung positiver und negativer Werte,
- Wertebereich und Rechenverhalten bei Grenzen,
- Genomkodierung und Run-Format,
- Vererbung und Rekombination,
- Mutationswahrscheinlichkeit und Schrittverteilung,
- Kostenwirkung,
- Darstellung in Lupe, Genomvergleich und Stammbaum.

Die geprüfte heutige Bedeutung einer Kante und der Neutralitätsvertrag stehen
in [KANTENGEWICHTE_KONZEPT.md](KANTENGEWICHTE_KONZEPT.md). Die technische und
fachliche Abgrenzung zu v0.3 steht in [VERSIONSGRENZE.md](VERSIONSGRENZE.md).

## Testen

```bash
cd 04_Prototypen/v0.4
python3 -m unittest -v
```

## Starten

```bash
python3 run.py --ticks 500
python3 supervisor.py
python3 lupe.py runs/DEINE-RUN-ID --port 8766
```

## Bestandteile

- `eve_core.py`: ereignisgesteuerter Fachkern und Genom
- `run.py`, `run_store.py`: Run-Ausführung und Persistenz
- `supervisor.py`, `run_parameters.py`: kontrollierte Run-Steuerung
- `lupe.py`, `assets/v04.js`, `assets/v04.css`: Analyseoberfläche
- `KANTENGEWICHTE_KONZEPT.md`: fachlicher Ausgangspunkt der Genomrevision
- `test_*.py`: übernommene Regressionstests und kommende v0.4-Tests
