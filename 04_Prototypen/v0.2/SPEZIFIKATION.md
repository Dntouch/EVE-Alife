# Spezifikation des Prototyps v0.2

## Fachmodell

Für Genom, Ports, A₀, K, Z, S, RAM, Membran, Energie, Mutation, Rekombination, Reproduktion und Scheduling gilt unverändert die Spezifikation von `../v0.1/SPEZIFIKATION.md` zusammen mit `../../02_Konzept/Genom_verstehen.md`. Bei Widersprüchen beschreibt diese Datei ausschließlich die neue technische Lauf- und Beobachtungsschicht; sie ändert keine biologische Regel.

## Run-Modi

- `--ticks N`: begrenzter Run, `N >= 1`; beim Resume sind es N weitere Ticks.
- `--open`: kein künstliches Tick-Limit.
- Ohne Angabe gilt das Referenzlimit von Lauf 41 mit 2.000 Ticks.
- `--ticks` und `--open` schließen einander aus.

Vor jedem Heartbeat wird zuerst Extinktion, dann das Tick-Limit geprüft. Deshalb kann eine Population, die im letzten erlaubten Heartbeat ausstirbt, korrekt mit `natural_extinction` enden.

Ohne abweichende Parameter wird der eingefrorene P1-Endstand von Lauf 41 eingesetzt: Population `p1`, 20 Startamöben, Seed 42, zufälliger RAM, Startenergie 500, `birth_energy_fraction = 0.5`, `birth_min_heartbeats = 5`, `novelty_base = 60` und Altersrate 0,01. Für v0.2 gilt versuchsweise der deutlich reduzierte Genomkostentarif 0,05 je Quadratwurzel der Funktionspunktzahl und 0,01 je Quadratwurzel der Kantenzahl. P0, P1 und v0.1 bleiben beim historischen Tarif 0,5/0,1. Beide v0.2-Werte bleiben über die Kommandozeile parametrisiert.

Experimentell werden die P1-Gründergenome mit einer separaten, aus dem Run-Seed abgeleiteten Zufallsquelle variiert: Offset `−5 … +5`, Schrittweite aus `−4 … −1` oder `+1 … +4`, Geduld `32 … 96` und A₀ `96 … 104`. Alle konkreten Werte stehen im Run-Manifest. `--uniform-p1` setzt für einen Kontrolllauf Offset `−1`, Schritt `+1`, Geduld `64` und A₀ `100`.

Die Rekombination hält Komponenten weiterhin atomar, wählt aber eine Kombination, die die gezogene Zielgröße bestmöglich erreicht, ohne sie zu überschreiten. Unter gleich großen Ergebnissen entscheidet der Simulationszufall. Ein eigener belegter Partnerslot darf durch ein genomisch erzeugtes, provenienzbehaftetes `0` zurückgezogen werden; fremde oder unbelegte Slots werden dadurch nicht verändert. Das vorläufige Rückzugsgenom zählt eigene Prüfzyklen in Z und ist ausdrücklich Experiment, nicht konsolidiertes Konzept.

## Status und Endgrund

| Phase | `status` | `end_reason` |
| --- | --- | --- |
| aktiv oder technisch unterbrochen | `running` | `NULL` |
| natürliche Population null | `extinct` | `natural_extinction` |
| Limit mit Population größer null | `completed` | `tick_limit_reached` |

Technische Unterbrechung ist in v0.2 kein abgeschlossener Zustand. Fortsetzung erzeugt wie bereits in v0.1 einen neuen, separat identifizierten Run und referenziert den Quellcheckpoint in den Metadaten.

## Beobachtungsdaten

Persistiert werden Konfiguration und Lebenszyklus, vollständige deduplizierte Genome, Entity-Lebensgrenzen, Elternkanten, reale Rekombinations-/Mutationsprovenienz im Ereignis `genome_created`, weitere relevante diskrete Core-Ereignisse, periodische Messpunkte, komprimierte Lupe-Bilder ohne RAM und ein Katalog der Recovery-Checkpoints. `live.json` enthält zusätzlich den aktuellen beobachtbaren Entity-Zustand, aber keinen vollständigen RAM.

Nicht in die reguläre Historie geschrieben werden die hochfrequenten Ereignisse `node_fire`, `signal`, `standby` und `heartbeat`. Sie ändern das Fachmodell nicht und wären ohne expliziten Diagnoselauf nicht langfristig tragfähig. Ein exakter Tick-Replay wird nicht versprochen.

## Format und Konsistenz

- Formatname: `eve-alife-run`
- Formatversion: `2`
- Datenbank: SQLite mit Fremdschlüsseln und WAL im laufenden Betrieb
- Manifest und Livebild: atomar ersetztes UTF-8-JSON
- Archivsuffix: `.eve-run` (ZIP)
- Genomidentität: SHA-256 über kanonisches JSON der Nodes, Edges und A₀

IDs gelten innerhalb eines Runs. Ein Genomfingerprint ist inhaltsbezogen und nicht als fachliche globale Identität über alle künftigen Schema-Versionen definiert.

## Read-only-Grenze

Die Lupe bindet standardmäßig nur `127.0.0.1`, öffnet SQLite mit `mode=ro` und bietet ausschließlich `GET`-Routen. Das HTML hat keine Supervisorbefehle. Eine öffentliche Bereitstellung erfordert zusätzlich einen gehärteten vorgeschalteten Dienst, Größenlimits, Archivvalidierung und eine getrennte Veröffentlichungskopie.
