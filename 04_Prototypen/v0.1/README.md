# EVE-Alife – Prototyp v0.1

Der erste ausführbare Prototyp enthält einen eigenständigen Experimentkern und eine davon getrennte read-only **Lupe**. Beide verwenden ausschließlich die Python-Standardbibliothek.

## Bestandteile

- `eve_core.py`: Experimentzustand, Datenfluss, Energie, Reproduktion, Rekombination und Mutation
- `run.py`: getrennte Control-/CLI-Schicht, Events, Snapshots und Checkpoints
- `lupe.py`: read-only Webansicht persistierter Beobachtungsdaten
- `test_eve.py`: deterministische Kerntests
- `SPEZIFIKATION.md`: prototypspezifische Regeln und Parameter

Die mitgelieferte Population 0 ist nur ein technischer Demonstrator. Sie darf nicht als wissenschaftliches Experiment oder als beobachtete Emergenz interpretiert werden.

## Testen

```bash
cd 04_Prototypen/v0.1
python3 -m unittest -v
```

## Lauf starten

```bash
python3 run.py --ticks 100 --seed 42
```

Die Ausgabe nennt das erzeugte Run-Verzeichnis. Darin liegen:

- `metadata.json`: Run-ID, Seed, Konfiguration, EVE- und Git-Version
- `events.jsonl`: append-only Ereignisstrom
- `latest.json`: jüngster read-only Beobachtungssnapshot
- `snapshots/`: historische Beobachtungssnapshots
- `checkpoint.json`: vollständiger Zustand einschließlich Zufallszustand

Runs landen standardmäßig unter `runs/` und werden gemäß `.gitignore` nicht versioniert.

## Lupe starten

In einem zweiten Terminal:

```bash
python3 lupe.py runs/DEINE-RUN-ID
```

Danach ist die Lupe unter [http://127.0.0.1:8080](http://127.0.0.1:8080) erreichbar. Sie liest ausschließlich persistierte JSON-Dateien und besitzt keinen Zugriff auf veränderbare Core-Strukturen oder Control-Funktionen.

## Checkpoint fortsetzen

```bash
python3 run.py --resume runs/ALTE-RUN-ID/checkpoint.json --ticks 100
```

Das Fortsetzen erzeugt einen neuen, separat identifizierten Run und bewahrt den Ausgangslauf unverändert.
