# 24. September 2026 – Die Rammler fraßen den RAM

## Ausgangslage

Nach der Einführung homologer, größenfreier Genomplätze wurde ein Lauf mit 20
Amöben, Seed 42 und 5.000 Ticks gestartet. Frühere v0.4-Versuche waren rasch
ausgestorben und hatten ausschließlich schrumpfende Nachkommengenome erzeugt.

## Populationsdurchbruch

Der neue Lauf zeigte das gegenteilige Bild. Die Population wuchs über viele
Generationen weiter. Beim letzten konsistenten Zustand in Tick 4.034 waren 9.446
Amöben entstanden, davon 8.761 lebend. Die tiefste Linie erreichte Generation
38. Nur einer der 20 Gründer lebte noch.

Alle registrierten Genome besaßen 198 Teile. Zugleich existierten 8.823
verschiedene Fingerabdrücke. Damit beseitigte das Platzmodell den beobachteten
Größenkollaps, ohne Rekombinationsvielfalt zu unterdrücken. Neun protokollierte
Einzelmutationen stehen 9.426 Geburten gegenüber.

## Technischer Abbruch

Der Lauf erreichte sein Limit nicht. Der Kernel beendete den Python-Prozess am
24. September um 02:45:40 Uhr wegen globalen Speichermangels. Das Kernelprotokoll
weist rund 52,35 GB physischen Speicher für den Prozess aus; die zugehörige
Anwendungseinheit erreichte 55,3 GB Spitze und 9,4 GB Swap-Spitze.

Ursachen waren keine biologischen Zustandsgrößen allein, sondern zwei
Beobachtungsfehler:

1. Die vollständige Ereignisliste blieb nach der SQLite-Persistenz im
   Simulationsprozess erhalten.
2. Nach jedem Tick wurde ein vollständiges, zuletzt 405 MB großes Live-Bild
   erzeugt und atomar geschrieben.

Die Datenbank enthält 1.696.250 Ereignisse und ist 1,3 GB groß. Wegen des auf
10.000 gesetzten Checkpointintervalls existiert kein Recovery-Checkpoint. Eine
deterministische Fortsetzung ist nicht möglich. Der Run bleibt als technisch
abgebrochene Beobachtung erhalten und darf nicht als vollständiger 5.000-Tick-
Lauf interpretiert werden.

## Performance-Revision

Ohne Änderung der Simulationssemantik wurden folgende Maßnahmen umgesetzt:

- Ereignisse werden nach der Persistenz pro Tick aus dem RAM freigegeben.
- `live.json` wird höchstens zweimal pro Sekunde aktualisiert.
- Der Live-Zustand enthält keine RAM-Kopie, Genome, K-/Z-Signale oder wachsende
  Wissenshistorien.
- SQLite-Commit, Status und Manifest werden am Messintervall gebündelt.
- Entitäten und Genome werden nur bei ihrer Entstehung registriert; identische
  Genome werden zusätzlich im Writer gecacht.
- Ein reproduzierbarer Benchmark trennt Simulationskern und Beobachtungskosten.

Bei 1.000 synthetischen Amöben war das kompakte Live-Bild 7,12-mal kleiner und
10,1-mal schneller aufgebaut. Das CPU-Profil verortet den verbleibenden Aufwand
vor allem in `_execute_entity` und `_ready`; Mehrkernbetrieb bleibt damit ein
späteres Architekturthema und keine Voraussetzung für die aktuelle Reparatur.

## Qualitätssicherung

Die Testsuite wurde um Schutzprüfungen für den kompakten Live-Zustand, die
einmalige Genomregistrierung und die weiterhin vollständigen periodischen
Beobachtungen erweitert. Alle 67 Tests bestanden.

## Artefakte

- [Laufanalyse v0.4/001](../07_Laufergebnisse/v0.4/Lauf_001.md)
- [Blogentwurf 015](../06_Blog/015_Die_Rammler_frassen_den_RAM.md)
- [v0.4-Architektur](../04_Prototypen/v0.4/ARCHITEKTUR.md)
- [Performance-Benchmark](../04_Prototypen/v0.4/benchmark_performance.py)

