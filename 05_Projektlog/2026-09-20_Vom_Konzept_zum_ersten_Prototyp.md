# 20. September 2026: Vom Konzept zum ersten laufenden Prototyp

Ausgangspunkt war ein redaktionelles Problem: Die beiden jüngsten Blogentwürfe enthielten wesentlich genauere Definitionen als der konsolidierte Konzeptstand v0.6. Beim Abgleich zeigte sich, dass nicht nur Text fehlte. Mehrere Regeln waren noch zu grob, um daraus ohne stillschweigende Erfindungen einen Prototyp zu bauen.

## Eine fortlaufende Konzeptdatei

Die parallelen Arbeitsdateien v0.4, v0.5 und v0.6 wurden aus dem Arbeitsbaum entfernt. Git übernimmt künftig die historische Versionierung. Der aktuelle Stand liegt fortlaufend in `02_Konzept/Grundkonzept_Arbeitsentwurf.md`; wichtige Meilensteine können zusätzlich über Konzeptversionsnummern und Git-Tags markiert werden. Die alten Fassungen bleiben über die Git-Historie wiederherstellbar.

## Obligatorische Ausführung statt Handlungsimpuls

Die zunächst gestellte Frage, was eine Entität zum Handeln bringt, erwies sich als falsch gestellt. Eine lebende Entität kann nicht entscheiden, ihr Genom nicht auszuführen. Der Supervisor aktiviert die genomische Struktur in jedem Heartbeat als Teil der Weltphysik.

Die tatsächlich mögliche Aktivität entsteht aus drei Größen:

```text
A₀   = erblicher Basiswert
Nₚ   = Anzahl der P-Kanten
S    = aktuell verfügbare Energie
```

`A₀` und ein Faktor aus `Nₚ` bestimmen den vorgesehenen Umfang; `S` begrenzt den finanzierbaren Umfang. `PAUSE` wurde als primitiver Funktionspunkt ergänzt. Eine Entität führt dadurch weiterhin ihr Genom aus, ein Datenfluss kann aber genetisch bedingt ohne weitere Wirkung enden.

## Konkrete Instanzen, Kanten und zwei Speicherarten

Das Genom besteht nun aus konkreten Funktionspunkt-Instanzen, gerichteten `P`-Kanten und singulären Metadaten. Zwei Instanzen desselben primitiven Typs bleiben unterscheidbare Bestandteile des Netzes.

Der kurzfristige Signalzustand wurde vom dauerhaften Zustand getrennt:

```text
G = Genom
K = kurzfristige Portwerte
Z = durch Z-write dauerhaft gespeicherter Zustand
S = Energie
```

`K` besitzt je Eingangsport einen Slot. Neu eintreffende Werte überschreiben ältere; verwendete Werte werden bei der Ausführung verbraucht. `K` wird weder vererbt noch energetisch belohnt. Erst ein ausdrückliches `Z-write` macht einen Wert zum dauerhaften erworbenen Zustand.

`CONST` wurde als eingangsloser primitiver Funktionspunkt aufgenommen. Sein Wert liegt erblich in `G`, kann selten mutieren und liefert einem bei Geburt sonst zustandslosen Netz erste genetisch gesetzte Werte.

## Ereignisartige Datenflussausführung

Eingangslose Punkte sind grundsätzlich bereit. Andere Punkte werden bereit, sobald alle erforderlichen Slots in `K` belegt sind. Innerhalb eines Heartbeats zieht der Core seed-reproduzierbar und semantikfrei aus den bereiten Instanzen. Eine ausgeführte Instanz sendet jeden Ausgangswert über alle angeschlossenen Kanten. Budget, Energie oder eine leere Bereitschaftsmenge beenden den Heartbeat. Zyklen bleiben erlaubt und werden nicht semantisch verboten.

## Neuheit wird nicht binär

Ein wiederholt nach `Z` geschriebener Wert bleibt belohnbar, liefert aber abnehmende Energie. Der erste Schreibvorgang ist der höchstwertige Erstfall, nicht die einzige belohnbare Situation. Eine supervisorseitige, für die Entität unsichtbare Lebenszeithistorie verhindert, dass Überschreiben den Wiederholungszähler zurücksetzt.

Für P0.1 trägt jeder Wert zusätzlich eine unsichtbare Provenienzmenge:

```text
CONST       -> G
S-read      -> S
RAM-read(a) -> RAM[a]
```

Verarbeitung vereinigt Provenienzen, erzeugt aber keine neue Quelle. Alle Konstanten teilen die abstrakte Quelle `G`, damit das Vervielfachen von `CONST`-Instanzen nicht die Quellensättigung umgeht.

## Zwei oder drei Eltern

Die Membran besitzt in P0.1 eine lesbare Entity-ID und zwei Partnerslots. Gültig sind vollständig wechselseitige Gruppen aus zwei oder drei lebenden Entitäten. Der Supervisor ergänzt keine Partner. Nach erfolgreicher Geburt leert er die Partnerslots aller Beteiligten; eine weitere Geburt verlangt eine erneut aufgebaute Konstellation.

Die feste Geburtsenergie wird gleichmäßig von allen Eltern bezahlt und vollständig auf das Kind übertragen. `A₀` übernimmt das Kind unvermischt von einem gleichverteilt gezogenen Elternteil.

Vererbt werden zusammenhängende Netzfragmente. Ein Fragment wächst zufällig von einer realen Instanz entlang realer Kanten. Mehrfach vorhandene Strukturen erhalten durch ihre zusätzlichen Startpunkte automatisch höheres Vererbungsgewicht. Die Fragmente werden ohne Zurücklegen gezogen und im Kind zunächst nicht künstlich verbunden. Mutation tritt standardmäßig mit Wahrscheinlichkeit `0,001` auf und verändert höchstens eine Instanz, eine Kante oder `A₀`.

## Prototyp v0.1

Der Experimentkern wurde mit der Python-Standardbibliothek selbst implementiert. Die getrennte Control-Schicht erzeugt Run-ID, Seed, Konfiguration, Git-Commit, Events, historische Snapshots und einen vollständigen Checkpoint einschließlich Zufallszustand. Ein fortgesetzter Run reproduziert denselben weiteren Verlauf.

Die erste Lupe ist ein separater read-only HTTP-Dienst. Sie liest ausschließlich persistierte Beobachtungsdaten und zeigt Population, RAM-Suppe, Entitäten, Abstammung und historische Snapshots. Sie besitzt keine Control-Funktion und keinen Zugriff auf veränderbare Core-Strukturen.

## Erste Beobachtung

Der technische Demonstrationslauf mit Seed `42` war kein wissenschaftlicher Versuch. Seine Population 0 wurde absichtlich so gebaut, dass Datenfluss, `Z-write`, Membran und Geburt praktisch geprüft werden konnten.

Beobachtet wurden:

- zwei gestartete Eltern,
- eine gültige wechselseitige Partnerkonstellation,
- eine energieerhaltende Geburt,
- mehrere `Z-write`-Ereignisse mit sinkender Wiederholungsbelohnung,
- anschließend der Tod aller drei Entitäten.

Das vollständige Aussterben ist kein Fehler und keine Widerlegung des Modells. Es zeigt zunächst nur, dass die technische Demonstrationspopulation unter den gewählten P0.1-Kosten nicht dauerhaft lebensfähig war.

Sechs deterministische Kerntests bestanden. Checkpoint-Fortsetzung sowie die read-only Endpunkte der Lupe wurden zusätzlich praktisch geprüft.

Der Stand wurde als Commit `a5d660d` (`Build EVE-Alife prototype v0.1`) nach `origin/main` übertragen.

## Einordnung

- **Designentscheidung:** die in diesem Eintrag beschriebenen Naturgesetze und P0.1-Parameter.
- **Beobachtung:** Geburt, Schreibereignisse und Aussterben im technischen Demonstrationslauf.
- **Keine Beobachtung:** Lernen, Intelligenz, Kooperation, Anpassung oder erfolgreiche Evolution.

Tja. Das erste digitale Einzellerlein bekam ein Kind. Dann waren alle tot. Für einen ersten Arbeitstag ist das erstaunlich biologisch und noch kein bisschen aussagekräftig.

## Nachtrag: Abschluss von P0

Ein kontrollierter Folgelauf mit 20 Startentitäten verglich ausschließlich zwei Startenergien. Seed, zufällige RAM-Suppe und P0-Demogenome blieben identisch. Mit Energie 100 entstanden 20 Nachkommen und die letzte Entität starb in Tick 9. Mit Energie 500 entstanden 93 Nachkommen und die letzte Entität starb in Tick 24.

Die zusätzliche Energie machte den Ablauf größer und länger, aber nicht anders. Alle 397 Z-Schreibvorgänge des energiereicheren Laufs trafen dieselbe Adresse. Die Amöben waren technisch aktiv, erkundeten die Umwelt jedoch nicht sinnvoll. P0 wird daher als erfolgreicher Nachweis der Maschine und ausdrücklich nicht als Nachweis interessanten Verhaltens abgeschlossen. Die vollständige Auswertung steht in `04_Prototypen/P0_ERGEBNISSE.md`; daraus folgt der P1-Genomentwurf in `04_Prototypen/P1_GENOMENTWURF.md`.

## Nachtrag: Population 1 beginnt zu suchen

Das erste P1-Genom hält nun selbst einen Suchstand in Z, erhöht ihn durch sein Datenflussnetz, liest die daraus entstandene RAM-Adresse und speichert den Fund getrennt vom Suchstand. Der neue primitive Funktionspunkt `GATE` kann einen Wert abhängig von einer Null-/Nichtnull-Bedingung weiterleiten oder unterdrücken.

Unter denselben kontrollierten Rahmenbedingungen des energiereichen P0-Laufs erreichten die 20 Startamöben jeweils mehrere RAM-Adressen, ohne dass die Suppe dafür präpariert wurde. Das ist noch keine offene oder intelligente Exploration. Erstmals ist die Veränderung der besuchten Umweltadressen aber eine Wirkung des ausgeführten Genoms und nicht bloß eine vorab festgelegte Liste im Supervisor.
