# Spezifikation des Prototyps v0.4

v0.4 basiert fachlich auf dem abgeschlossenen Stand von v0.3. Die bestehende
Spezifikation des Simulationskerns gilt daher weiter; neu spezifiziert werden
vor allem Supervisor, Run-Verwaltung und die read-only Analyseoberfläche. Die
Bedien- und Darstellungsregeln der Lupe stehen in `LUPE.md`, die Auftragsgrenze
des Supervisors in `SUPERVISOR.md`. Der Ordner `../v0.2` bleibt konserviert.

## Fachmodell

Für Genom, Ports, A₀, K, Z, S, RAM, Membran, Energie, Mutation, Rekombination, Reproduktion und Scheduling gilt unverändert die Spezifikation von `../v0.1/SPEZIFIKATION.md` zusammen mit `../../02_Konzept/Genom_verstehen.md`. Bei Widersprüchen beschreibt diese Datei ausschließlich die neue technische Lauf- und Beobachtungsschicht; sie ändert keine biologische Regel.

Gerichtete Kanten besitzen in v0.4 ein ganzzahliges erbliches Gewicht. Der
neutrale Wert `0` entspricht exakt dem bisherigen Kantenverhalten. Eine Kante
transportiert `T(v,w) = trunc(v × (100+w) / 100)`; Quellen- und
Urheberprovenienz bleiben dabei unverändert. Gewichte werden mit ihren Kanten
rekombiniert und können ausschließlich bei der Geburt mutieren. Der Betrag
folgt ohne feste Obergrenze `P(k) ∝ 1/k²`, die Richtung wird gleichverteilt
gezogen. Altformate ohne Gewicht werden als `0` gelesen. Die vollständige
Semantik und die weiterhin offenen Entscheidungen stehen in
[`KANTENGEWICHTE_KONZEPT.md`](KANTENGEWICHTE_KONZEPT.md).

## Run-Modi

- `--ticks N`: begrenzter Run, `N >= 1`; beim Resume sind es N weitere Ticks.
- `--open`: kein künstliches Tick-Limit.
- Ohne Angabe gilt das Referenzlimit von Lauf 41 mit 2.000 Ticks.
- `--ticks` und `--open` schließen einander aus.

Vor jedem Heartbeat wird zuerst Extinktion, dann das Tick-Limit geprüft. Deshalb kann eine Population, die im letzten erlaubten Heartbeat ausstirbt, korrekt mit `natural_extinction` enden.

Ohne abweichende Parameter wird der eingefrorene P1-Endstand von Lauf 41 eingesetzt: Population `p1`, 20 Startamöben, Seed 42, zufälliger RAM, Startenergie 500, `birth_energy_fraction = 0.5`, `birth_min_heartbeats = 5`, `novelty_base = 60` und Altersrate 0,01. Nach dem mit Altersrate 0,005 stark wachsenden Lauf 002 kehrt der aktive v0.4-Standard damit zum höheren Alterstarif zurück, um die sehr langen Lebensspannen alter Amöben in folgenden Versuchen zu begrenzen. Der historische Preset `v02-run16` bleibt für kontrollierte Wiederholungen unverändert bei 0,005. Für v0.2 gilt versuchsweise der deutlich reduzierte Genomkostentarif 0,05 je Quadratwurzel der Funktionspunktzahl und 0,01 je Quadratwurzel der Kantenzahl. P0, P1 und v0.1 bleiben beim historischen Tarif 0,5/0,1. Alle Werte bleiben über die Kommandozeile parametrisiert.

Experimentell werden die P1-Gründergenome mit einer separaten, aus dem Run-Seed abgeleiteten Zufallsquelle variiert: Offset `−5 … +5`, Schrittweite aus `−4 … −1` oder `+1 … +4`, Geduld `32 … 96`, A₀ `96 … 104`, Klingelkapazität Nₖ `1 … 4` und Bindungszeit Tₚ `3 … 12`. Alle konkreten Werte stehen im Run-Manifest. `--uniform-p1` setzt Offset `−1`, Schritt `+1`, Geduld `64`, A₀ `100`, Nₖ `2` und Tₚ `5`.

### Experimentelle Klingel

Ein gültiges genomisches Schreiben einer fremden ID in den eigenen Partnerslot erzeugt zusätzlich beim gewählten Ziel einen eingehenden Klopfer mit der Herkunft des Absenders. Die erbliche Klingelkapazität Nₖ bestimmt, wie viele verschiedene, weiterhin gültige Vorschläge in Eingangsreihenfolge gehalten werden; sie liegt technisch zwischen 1 und 16. Ist die Kapazität erschöpft, verdrängt ein neuer Absender den ältesten. Wiederholtes Klopfen desselben Absenders erzeugt weder ein Duplikat noch eine neue Priorität. `MEM_READ` auf der eigenen Membran mit Offset `3` liefert über die Slots `0 … Nₖ−1` die noch lebenden Absender, deren Partnerslot weiterhin auf die Empfängerin zeigt. Das gelesene Signal trägt die Provenienz `KNOCK[ID]` und darf deshalb genomisch in einen eigenen Partnerslot übernommen werden.

Die Klingel erzeugt keine automatische Zustimmung: Nur ein tatsächlich ausgeführtes `MEM_READ` und ein daraus gespeistes `MEM_WRITE` der Empfängerin können erwidern. Erst die bereits bestehende wechselseitige Partnerprüfung kann danach eine reproduktive Gruppe aus zwei oder drei Amöben bilden. Der Supervisor wählt weder Partner noch Reaktion. Das v0.2-Startgenom enthält Schaltungen für die ersten beiden Klopfer und Partnerslots; Rekombination und Mutation können sie verändern oder verlieren.

Die erbliche Bindungszeit Tₚ ist die Zahl aufeinanderfolgender Reproduktionsprüfungen, während der dieselbe Gruppe vollständig gegenseitig verbunden bleiben muss. Für eine Gruppe gilt das Maximum der Tₚ-Werte ihrer Mitglieder. Trennung oder Umbesetzung setzt nur die Stabilität dieser konkreten Gruppe zurück. Nach einer Geburt werden wie bisher ihre Partnerslots geleert. Nₖ und Tₚ werden bei Rekombination jeweils von einem Elternteil übernommen und können um eins mutieren. Diese Metadaten legen keine Suchstrategie und keine Gruppengröße fest; sie bleiben als Experiment offen.

Die Geburtsenergie wird aus dem gemeinsamen Energieüberschuss der Eltern über ihrem jeweils individuellen Geburtswert `S₀` finanziert. Ausgangspunkt ist eine gleichmäßige Aufteilung. Reicht der Überschuss eines Elternteils dafür nicht, wird sein Fehlbetrag gleichmäßig auf die noch zahlungsfähigen Eltern verteilt. Eine Geburt ist möglich, sobald der gemeinsame Überschuss die vollständige Kindesenergie deckt; damit darf auch ein einzelner Elternteil sämtliche Kosten tragen. Kein Beitrag senkt ein Elternteil unter `S₀`. `S₀` bleibt individueller Lebenszustand und ist weder eine maximale Energiekapazität noch ein Genommerkmal.

Der v0.4-Simulationskern kombiniert evolvierbare Vererbungsplätze beliebiger
Größe. P1 startet mit drei Plätzen. Die Architektur eines Elternteils liefert
die kindlichen Loci; strukturell homologe elterliche Varianten werden bevorzugt
gepaart und vollständig vererbt. Die Gesamtgenomgröße ist Ergebnis dieser
Vererbung und der seltenen Duplikation, Löschung, Teilung oder Verschmelzung von
Plätzen. Eine vor der Geburt gezogene Zielgenomgröße existiert nicht.
Platzübergreifende offene Anschlusskanten werden ausschließlich an semantisch
kompatible, unbelegte Eingänge gekoppelt oder verworfen. Die Einzelheiten stehen in
[`SEGMENTVERERBUNG_KONZEPT.md`](SEGMENTVERERBUNG_KONZEPT.md).

Ein eigener belegter Partnerslot darf durch ein genomisch erzeugtes,
provenienzbehaftetes `0` zurückgezogen werden; fremde oder unbelegte Slots
werden dadurch nicht verändert. Das vorläufige Rückzugsgenom zählt eigene
Prüfzyklen in Z und ist ausdrücklich Experiment, nicht konsolidiertes Konzept.

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

## Experimenteller RAM-Spielzeugkasten

`--ram-world toys` ergänzt die gemeinsame RAM-Suppe um 128 reproduzierbare Spielzeuginseln in gleich großen RAM-Sektoren. Jede Insel enthält ein achtzelliges festes Muster, zwei autonom wechselnde Zellen und eine gekoppelte Schreib-/Ausgabezelle. Die genaue Position im Sektor ist seedabhängig und nicht auf Amöben ausgerichtet. Die Amöben benutzen dafür ausschließlich `RAM_READ` und `RAM_WRITE`; der Spielzeugkasten fügt keine Genomoperation und keine vorgegebene Bedeutung hinzu.

In diesem Modus besitzt jede Amöbe eine von ihrer ID unabhängige RAM-Position. Genomisch berechnete RAM-Adressen werden als lokale Offsets interpretiert und ringförmig auf die physische Suppe abgebildet. Gründer sind über die Suppe verteilt; Kinder entstehen innerhalb von 32 Zellen um einen zufällig gewählten Elternstandort. Position und Radius sind Umweltparameter, keine Genomwerte. Die historischen Modi `random` und `islands` behalten ihre absolute Adressierung.

Autonome Änderungen besitzen keine Urheber. Ausgelöste Schalterreaktionen bewahren dagegen die Urheberkette des Schreibsignals einschließlich der auslösenden Amöbe. Deshalb gilt die bestehende Neuheitsenergie auch für Umweltänderungen, ohne Selbstfütterung über einen Schalter zu ermöglichen. Details und offene Prüffragen stehen im konservierten v0.3-Dokument [`EXPERIMENT_UMWELTSPIELZEUG.md`](../v0.3/EXPERIMENT_UMWELTSPIELZEUG.md). Die Modi `random` und `islands` bleiben für historische Vergleiche unverändert verfügbar.

## Format und Konsistenz

- Formatname: `eve-alife-run`
- Formatversion: `2`
- Datenbank: SQLite mit Fremdschlüsseln und WAL im laufenden Betrieb
- Manifest und Livebild: atomar ersetztes UTF-8-JSON
- Archivsuffix: `.eve-run` (ZIP)
- Genomidentität: SHA-256 über kanonisches JSON der Nodes, Edges, A₀, Nₖ und Tₚ

IDs gelten innerhalb eines Runs. Ein Genomfingerprint ist inhaltsbezogen und nicht als fachliche globale Identität über alle künftigen Schema-Versionen definiert.

## Read-only-Grenze

Die Lupe bindet standardmäßig nur `127.0.0.1`, öffnet SQLite mit `mode=ro` und bietet ausschließlich `GET`-Routen. Das HTML hat keine Supervisorbefehle. Eine öffentliche Bereitstellung erfordert zusätzlich einen gehärteten vorgeschalteten Dienst, Größenlimits, Archivvalidierung und eine getrennte Veröffentlichungskopie.
