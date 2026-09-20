# EVE-Alife – Prototyp v0.1

Der erste ausführbare Prototyp enthält einen eigenständigen Experimentkern und eine davon getrennte read-only **Lupe**. Beide verwenden ausschließlich die Python-Standardbibliothek.

## Bestandteile

- `eve_core.py`: Experimentzustand, Datenfluss, Energie, Reproduktion, Rekombination und Mutation
- `run.py`: getrennte Control-/CLI-Schicht, Events, Snapshots und Checkpoints
- `lupe.py`: read-only Webansicht persistierter Beobachtungsdaten
- `run_stats.py`: laufübergreifende Bilanz für Chronik und Massenaussterben
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
  --start-energy 500 --birth-energy 500 \
  --snapshot-every 1 --p1-explorers
```

`--snapshot-every 1` ist keine biologische Bedingung, sondern liefert der Lupe für den Lebensfilm ein Bild pro Heartbeat. `--explorers` bezeichnet weiterhin die ältere technische Fixture mit präparierbaren RAM-Inseln; sie darf nicht mit der P1-Population verwechselt werden.

Startenergie und Geburtsenergie sind getrennte Versuchsparameter. `--start-energy` betrifft nur die künstlich eingesetzte Startpopulation. `--birth-energy` bestimmt die vollständig von den Eltern bezahlte Energie jedes Kindes. Für den kontrollierten P1-Vergleich werden beide auf `500` gesetzt, damit Nachkommen nicht allein aufgrund der alten P0-Geburtsenergie von `50` nur ein Zehntel des anfänglichen Energievorrats besitzen.

Alternativ kann die Geburtsenergie relativ zur aktuellen mittleren Elternenergie berechnet werden:

```bash
python3 run.py --ticks 100 --seed 42 --population 20 \
  --start-energy 500 --birth-energy-fraction 0.5 \
  --birth-min-heartbeats 5 --snapshot-every 1 --p1-explorers
```

Ist `--birth-energy-fraction` gesetzt, hat dieser Modus Vorrang vor `--birth-energy`. Bei `0.5` erhält das Kind die Hälfte der mittleren aktuellen Elternenergie; der Betrag wird weiterhin vollständig und zu gleichen Teilen von den Eltern bezahlt. Zulässig sind Werte größer `0` bis einschließlich `1`.

`--birth-min-heartbeats 5` verlangt zusätzlich, dass diese angebotene Energie das konkrete Kindergenom für fünf volle Heartbeats finanzieren könnte. Der konservative Bedarf umfasst Standby, das Aktivitätsbudget des Kindes, Ausführungskosten und die höchste mögliche Zahl ausgehender Kanten einer ausgeführten Instanz; mögliche Z-Belohnungen werden nicht vorweggenommen. Reicht die angebotene Elternenergie nicht aus, findet keine Geburt statt, es wird nichts abgezogen und die Partnerslots bleiben gemäß der bestehenden P0-Regel belegt.

Unabhängig vom gewählten Geburtsenergiemodell speichert jede Entität ihre eigene Geburtsenergie als `S₀`. Nach dem Elternbeitrag muss jeder Elternteil strikt mehr als sein eigenes `S₀` behalten. Die Startenergie ist damit ausschließlich Existenzvorschuss; Fortpflanzung kann nur aus selbst erwirtschaftetem Überschuss bezahlt werden.

Die Lupe stellt die RAM-Suppe nicht mehr als abstraktes Farbfeld ihrer Rohwerte dar. Die Ansicht **Umweltkontakte** zeigt ausschließlich tatsächlich gelesene oder geschriebene Adressen, Zugriffshäufigkeiten, die letzten Kontakte und einen Filter je Amöbe.

In der aktuellen Minimalökonomie entsteht Energie unmittelbar beim Lesen eines gegenüber dem letzten eigenen Lesen veränderten externen RAM-Werts. Ein unveränderter Wert sowie ein Wert mit eigener Entity-ID in seiner Urheberkette liefern nichts. Kehrt nach einem zwischenzeitlichen anderen Wert ein früherer Wert zurück, ist er erneut belohnbar, jedoch mit abnehmendem Ertrag. `Z-write` dient nur noch der dauerhaften Speicherung und erzeugt keine Energie.

Der Ertrag des ersten belohnten Wechsels ist über `--novelty-base` ein Versuchsparameter. Die erste Tarifreihe verwendete bei sonst identischen Bedingungen die Werte `10`, `20`, `40`, `80` und `160`.

Die Ausgabe nennt das erzeugte Run-Verzeichnis. Darin liegen:

- `metadata.json`: Run-ID, Seed, Konfiguration, EVE- und Git-Version
- `events.jsonl`: append-only Ereignisstrom
- `latest.json`: jüngster read-only Beobachtungssnapshot
- `snapshots/`: historische Beobachtungssnapshots
- `checkpoint.json`: vollständiger Zustand einschließlich Zufallszustand
- `summary.json`: kompakte Laufbilanz für das Dashboard

Runs landen standardmäßig unter `runs/` und werden gemäß `.gitignore` nicht versioniert.

## Lupe starten

In einem zweiten Terminal:

```bash
python3 lupe.py runs/DEINE-RUN-ID
```

Danach ist die Lupe unter [http://127.0.0.1:8080](http://127.0.0.1:8080) erreichbar. Sie liest ausschließlich persistierte JSON-Dateien und besitzt keinen Zugriff auf veränderbare Core-Strukturen oder Control-Funktionen.

Die Lupe erklärt `G`, `P`, `K`, `Z`, `S` und RAM direkt in der Oberfläche. Für jeden gespeicherten Snapshot zeigt sie pro Entität die konkreten Funktionspunkt-Instanzen, P-Kanten, belegten K-Ports und sämtliche Z-Adressen. Ältere Runs enthalten diese erweiterten Genom- und K-Daten noch nicht; dafür muss mit dem aktuellen Core ein neuer Lauf erzeugt werden.

Jede Amöbe erhält außerdem einen menschenlesbaren, innerhalb ihres Laufs eindeutigen Namen. Die Vergabe folgt ausschließlich der Entity-ID und verbraucht keinen Simulationszufall; Namen beeinflussen das Verhalten daher nicht. Alte Runs erhalten in der Lupe dieselben Namen nachträglich aus ihrer ID, neue Runs speichern sie auch in Snapshots, Checkpoints und Geburtsereignissen.

Die **Chronik des Biotops** bilanziert alle Runs im gemeinsamen `runs/`-Verzeichnis. Sie zeigt die Zahl der Massenaussterben, erzeugte Nachkommen, insgesamt aus RAM gewonnene Energie sowie das kürzeste und längste abgeschlossene Leben mit Name, Entity-ID und Laufnummer. Als Massenaussterben zählt genau ein Lauf, dessen Population am Ende vollständig erloschen ist. Lebende Amöben gehen nicht in die Lebensdauerrekorde ein. Für ältere Runs erzeugt die Lupe einmalig eine kompakte `summary.json`; danach muss sie nicht bei jedem Aufruf den vollständigen Ereignisstrom erneut lesen.

Zusätzlich führt die Chronik historische Amöbenrekorde: größtes Genom, höchste jemals beobachtete Energie, meiste direkte Kinder, tiefste Generation, höchstes erreichtes Alter, meiste verschiedene gelesene RAM-Adressen, höchster persönlicher RAM-Energiegewinn und erfolgreichster Informationsproduzent. Direkte Kinder und Generationstiefe bleiben bewusst getrennte Größen. Beim Informationsproduzenten wird eine ausgezahlte Leseenergie gleichmäßig auf die in der Herkunftskette des RAM-Werts enthaltenen Urheber verteilt; Eigenfütterung bleibt wie im Core ausgeschlossen. Solange die P1-Population keine fremd belohnten Werte schreibt, bleibt dieser Rekord folgerichtig leer.

Nach jedem regulär abgeschlossenen Lauf aktualisiert `run.py` außerdem den markierten Statistikblock in der Git-Startseite des Projekts und den eigenen Markdown-Bericht unter `07_Laufergebnisse/`. Die großen Run-Daten bleiben lokal und ignoriert; nur die kompakten Ergebnisberichte werden versioniert und mit dem nächsten Commit/Push veröffentlicht. Nach importierten oder manuell veränderten Runs lässt sich dieselbe Aktualisierung ausdrücklich anstoßen:

```bash
python3 run_stats.py
```

Über **Leben abspielen** öffnet die Lupe einen read-only Lebensfilm einer einzelnen Entität. Er lässt sich abspielen, pausieren, beschleunigen und bildweise vor- oder zurücksetzen. Zu jedem gespeicherten Tick zeigt er den damaligen Zustand von `S`, `K`, `Z`, Genom und Partnern sowie die seit dem vorherigen Bild aufgetretenen Ereignisse in lesbarer Form. Die zeitliche Auflösung entspricht `--snapshot-every`; für einen lückenlosen Lebensfilm sollte der Lauf mit `--snapshot-every 1` erzeugt werden.

Replay-fähige neue Läufe protokollieren zusätzlich Standby-Buchungen, ausgeführte Funktionspunkte, RAM-Lesevorgänge und Reproduktionsbeiträge. Diese Ereignisse sind reine Beobachtungsdaten und verändern weder Scheduling noch Zustand oder Zufallsstrom. Ältere Runs können mit den damals vorhandenen Ereignissen abgespielt werden, enthalten aber entsprechend weniger Erklärungen.

## Checkpoint fortsetzen

```bash
python3 run.py --resume runs/ALTE-RUN-ID/checkpoint.json --ticks 100
```

Das Fortsetzen erzeugt einen neuen, separat identifizierten Run und bewahrt den Ausgangslauf unverändert.
