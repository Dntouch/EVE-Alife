# Performance und Speichergrenze in v0.4

## Anlass

Run `0ccf273f-6bc6-4a91-a42c-7bca96f9d70b` wurde bei Tick 4.034 vom
Linux-OOM-Killer beendet. Der Prozess hielt zuletzt ungefähr 52,35 GB anonymen
physischen Speicher und mehrere Gigabyte Swap. Ursache war vor allem die seit
Laufbeginn im Core behaltene Ereignisliste. Ein pro Tick vollständig neu
erzeugtes Live-Bild verstärkte Zeit- und Spitzenspeicherverbrauch.

## Behobene Skalierungsfehler

1. Persistierte Tick-Ereignisse werden anschließend aus `Simulation.events`
   entfernt.
2. `live.json` wird durch monotone Zeitmessung auf höchstens zwei Schreibvorgänge
   pro Sekunde begrenzt.
3. `Simulation.live_observation()` enthält nur Leitstandsdaten. RAM-Kopie,
   Genomtopologie, K, Z und wachsende Wissenshistorien bleiben außen vor.
4. SQLite-Commit, Run-Status und Manifest werden am Messintervall gebündelt.
5. Der Writer registriert nur neue Entitäten; Genomfingerprints werden gecacht.
6. `benchmark_performance.py` misst Beobachtungskosten getrennt vom Fachkern und
   erstellt ein `cProfile` der Heartbeats.

Periodische vollständige Analysebeobachtungen, wissenschaftlich relevante
Ereignisse, Ausführungsreihenfolge und Zufallsverbrauch bleiben unverändert.

## Reproduzierbarer Benchmark

Aufruf:

```bash
cd 04_Prototypen/v0.4
python3 benchmark_performance.py --population 1000 --ticks 10
```

Messung vom 24. September 2026 auf der EVE-Workstation:

| Kennzahl | Ergebnis |
|---|---:|
| Start-/Endpopulation | 1.000 / 1.000 |
| Core-Durchsatz | 3,319 Ticks/s |
| ehemaliges vollständiges Live-JSON | 2.036.662 Bytes |
| kompaktes Live-JSON | 285.878 Bytes |
| Größenreduktion | Faktor 7,12 |
| Aufbau vollständiges Livebild, dreimal | 0,125887 s |
| Aufbau kompaktes Livebild, dreimal | 0,012469 s |
| Aufbau-Beschleunigung | Faktor 10,1 |
| vermiedener Genom-Vollscan, zehnmal | 0,305333 s |

Die Zahlen sind ein reproduzierbarer Mikrobenchmark und keine Hochrechnung des
abgebrochenen Runs. Bei 200 Amöben ergaben sich Faktor 12,68 bei der Größe und
Faktor 12,4 beim Aufbau.

## Verbleibendes CPU-Profil

Bei 1.000 Amöben und zehn Ticks entfielen von 3,013 Sekunden profilierter
Core-Zeit kumulativ:

- 2,895 Sekunden auf `_execute_entity`,
- 0,896 Sekunden auf `_ready`,
- 0,303 Sekunden auf `_fire`,
- 0,173 Sekunden auf `_transport_signal`.

Nach Entfernung der Beobachtungsbremse liegt der nächste substanzielle
Optimierungsbereich damit im seriellen Fachkern. Eine Parallelisierung würde
wegen gemeinsamen RAMs, fester Entity-Reihenfolge und deterministischer
Wirkungen eine zweiphasige Semantik benötigen und ist nicht Teil dieser
semantikneutralen Revision.

