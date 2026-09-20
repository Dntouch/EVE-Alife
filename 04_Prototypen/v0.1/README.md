# EVE-Alife – Prototyp v0.1

Der erste ausführbare Prototyp enthält einen eigenständigen Experimentkern und eine davon getrennte read-only **Lupe**. Beide verwenden ausschließlich die Python-Standardbibliothek.

## Bestandteile

- `eve_core.py`: Experimentzustand, Datenfluss, Energie, Reproduktion, Rekombination und Mutation
- `run.py`: getrennte Control-/CLI-Schicht, Events, Snapshots und Checkpoints
- `lupe.py`: read-only Webansicht persistierter Beobachtungsdaten
- `test_eve.py`: deterministische Kerntests
- `SPEZIFIKATION.md`: prototypspezifische Regeln und Parameter

Die abschließenden P0-Beobachtungen stehen in `../P0_ERGEBNISSE.md`. Der daraus abgeleitete, noch nicht implementierte Genomentwurf für P1 steht in `../P1_GENOMENTWURF.md`.

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

Eine größere technische Demonstrationspopulation wird paarweise initialisiert:

```bash
python3 run.py --ticks 100 --seed 42 --population 20
```

`--population` muss für diesen Demonstrator gerade und mindestens `2` sein. Die Paarbildung ist eine Testvorrichtung für Population 0 und keine evolutionäre Partnerwahl.

Ein spielerischer Explorationslauf mit höherer Startenergie, dünn besetzten RAM-Inseln und einem technischen Adresszähler in Population 0:

```bash
python3 run.py --ticks 100 --seed 42 --population 20 \
  --start-energy 500 --ram-world islands --explorers
```

Auch der Adresszähler ist nur eine Testvorrichtung. Im Inselmodus liegt zusätzlich je Startentität eine kleine Wertinsel in unmittelbarer Nähe ihrer genetischen Startadresse, damit der Datenpfad im kurzen Demonstrationslauf tatsächlich auf nichtleere Umweltwerte treffen kann. Beobachtetes Scannen oder Finden darf daher nicht als emergente Exploration interpretiert werden.

Die implementierte Population 1 arbeitet dagegen mit der unveränderten zufälligen RAM-Suppe. Ihr Genom hält den Suchstand in `Z[0]`, speichert gelesene Werte in `Z[1]` und leitet Nichtnull-Werte über `GATE` nach `Z[2]` weiter:

```bash
python3 run.py --ticks 30 --seed 42 --population 20 \
  --start-energy 500 --snapshot-every 1 --p1-explorers
```

`--snapshot-every 1` ist keine biologische Bedingung, sondern liefert der Lupe für den Lebensfilm ein Bild pro Heartbeat. `--explorers` bezeichnet weiterhin die ältere technische Fixture mit präparierbaren RAM-Inseln; sie darf nicht mit der P1-Population verwechselt werden.

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

Die Lupe erklärt `G`, `P`, `K`, `Z`, `S` und RAM direkt in der Oberfläche. Für jeden gespeicherten Snapshot zeigt sie pro Entität die konkreten Funktionspunkt-Instanzen, P-Kanten, belegten K-Ports und sämtliche Z-Adressen. Ältere Runs enthalten diese erweiterten Genom- und K-Daten noch nicht; dafür muss mit dem aktuellen Core ein neuer Lauf erzeugt werden.

Über **Leben abspielen** öffnet die Lupe einen read-only Lebensfilm einer einzelnen Entität. Er lässt sich abspielen, pausieren, beschleunigen und bildweise vor- oder zurücksetzen. Zu jedem gespeicherten Tick zeigt er den damaligen Zustand von `S`, `K`, `Z`, Genom und Partnern sowie die seit dem vorherigen Bild aufgetretenen Ereignisse in lesbarer Form. Die zeitliche Auflösung entspricht `--snapshot-every`; für einen lückenlosen Lebensfilm sollte der Lauf mit `--snapshot-every 1` erzeugt werden.

Replay-fähige neue Läufe protokollieren zusätzlich Standby-Buchungen, ausgeführte Funktionspunkte, RAM-Lesevorgänge und Reproduktionsbeiträge. Diese Ereignisse sind reine Beobachtungsdaten und verändern weder Scheduling noch Zustand oder Zufallsstrom. Ältere Runs können mit den damals vorhandenen Ereignissen abgespielt werden, enthalten aber entsprechend weniger Erklärungen.

## Checkpoint fortsetzen

```bash
python3 run.py --resume runs/ALTE-RUN-ID/checkpoint.json --ticks 100
```

Das Fortsetzen erzeugt einen neuen, separat identifizierten Run und bewahrt den Ausgangslauf unverändert.
