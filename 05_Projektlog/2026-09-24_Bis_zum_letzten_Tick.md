# 24. September 2026 – Bis zum letzten Tick

## Die Wiederholung

Nach dem OOM-Abbruch des ersten großen v0.4-Laufs wurde derselbe sichtbare
Versuchsrahmen erneut gestartet: 20 Gründer, Seed 42, Toys-Welt, Altersrate
0,005 und ein Limit von 5.000 Ticks. Der revidierte Datenpfad sollte diesmal
nicht selbst zum Todesgrund des Biotops werden.

Der Run brauchte 2 Stunden und 22 Minuten, erreichte aber regulär Tick 5.000.
31.082 Amöben waren bis dahin entstanden, 28.264 lebten noch. Die Population
wuchs am letzten Tick weiter. Die alte Frage, ob bis Tick 5.000 mehr als 20.000
Amöben leben würden, beantwortete der Lauf bereits in Tick 4.870.

## Das Nadelöhr zieht um

Der Linux-OOM-Killer blieb aus. 5,9 Millionen Ereignisse und 4,3 GB Run-Daten
lagen nach dem Lauf auf der Platte, ohne erneut als vollständige Ereignisliste
im Simulationsprozess zu wachsen. Damit bestand die Speicherrevision ihren
praktischen Härtetest.

Stattdessen wurde der serielle Fachkern zum sichtbaren Engpass. Jenseits von
20.000 Lebenden dauerten zehn Ticks mehrere Minuten. Mehrkernunterstützung ist
damit kein abstraktes Zukunftsthema mehr. Sie darf allerdings die feste
Entity-Reihenfolge, das gemeinsame RAM und die Reproduzierbarkeit nicht still
verändern. Als nächster Entwurf bietet sich eine zweiphasige Semantik an:
Wirkungen parallel vorbereiten und anschließend deterministisch committen.

## Das Browser-Wollknäuel

Die Amöben bildeten in der Toys-Welt sichtbare räumliche Häufchen. Der
Stammbaum war dieser Population jedoch nicht gewachsen. Seine Gesamtansicht lud
den vollständigen Graphen und große Ereignismengen in Chromium. Der
Rendererverbrauch stieg auf 8,4 GB RAM; erst das Schließen des Tabs senkte ihn
wieder auf etwa 1,2 GB.

Die Konsequenz ist eine fachliche Neugestaltung und nicht nur schnelleres
JavaScript. Für eine gewählte Amöbe sollen Vor- und Nachfahren auf wenige
Generationen und eine harte Knotenzahl begrenzt werden. Abgeschnittene Äste
werden sichtbar und gezielt aufklappbar. Die Gesamtansicht soll Abstammungslinien
aggregieren und erst beim Hineinzoomen Einzeltiere laden. Server-APIs müssen
Ausschnitte, Aggregate und Pagination liefern.

## Ein anderer Verlauf trotz Seed 42

Der zweite Lauf reproduzierte den ersten nicht exakt. Beide Populationskurven
stimmen bis Tick 1.230 überein und weichen ab Tick 1.240 erstmals voneinander
ab. Am Tick 4.000 lebten im ersten Lauf 7.956, im zweiten 2.547 Amöben. Der
zweite Verlauf überholte später dennoch den alten Endstand und erreichte 28.264.

Die Manifeste nennen unterschiedliche Git-Commits; ein damaliger nicht
committeter Arbeitsstand ist darüber hinaus nicht rekonstruierbar. Gleicher Seed
und gleiche sichtbare Parameter reichen daher nicht als Beleg identischer
Ausführung. Vor weiteren Reproduktionsaussagen muss der erste unterschiedliche
Geburts- und Ereignisverlauf um Tick 1.240 untersucht werden.

## Die Zwei-Slot-Dynastie

29.830 unterschiedliche Genome besaßen weiterhin drei Slots. Zwölf Genome
hatten nur zwei. Sämtliche Zwei-Slot-Genome gingen auf `Dadra 37` (#9197)
zurück: In Tick 4.502 verschmolzen zwei ihrer Slots, ohne die konstante Größe von
76 Knoten und 122 Kanten zu ändern.

Bis zum Laufende wurde diese Architektur an eine kleine Linie weitergegeben.
13 Zwei-Slot-Amöben lebten noch, keine war gestorben. Das ist eine interessante
Beobachtung, aber noch kein Selektionsbeleg. Bei 31.062 Geburten trat nur eine
einzige strukturelle Mutation auf; dass sie eine Verschmelzung und keine
Teilung war, ist mit der gleichmäßigen Mutationsauswahl und dem Erwartungswert
von weniger als einem Ereignis je Strukturklasse gut als Zufall erklärbar.

## Ergebnis

Der Lauf beantwortete seine ursprüngliche Frage und stellte drei neue:

- Warum trennen sich die deterministischen Verläufe erstmals in Tick 1.240?
- Wie wird der Fachkern mehrkernfähig, ohne seine Semantik zu verlieren?
- Wie beobachtet man eine Population dieser Größe, ohne den Browser zum zweiten
  Biotop mit eigenem Massenaussterben zu machen?

Die vollständigen Zahlen stehen in der [Laufanalyse
v0.4/002](../07_Laufergebnisse/v0.4/Lauf_002.md).

## Entscheidung für folgende Läufe

Vor einem weiteren großen Lauf wird die Standard-Altersrate von 0,005 auf 0,01
angehoben. Lauf 002 ließ alte Amöben nach der gemeinsamen Einschätzung zu lange
leben; ihre wachsende Zahl verstärkte zugleich den seriellen Rechenaufwand. Die
Änderung ist eine bewusst neue Versuchsbedingung. Der historische
`v02-run16`-Preset bleibt bei 0,005, damit frühere Referenzkonfigurationen nicht
stillschweigend verändert werden.

## Ausblick auf v0.5: Umwelt wird genomisch wirksam

Die Analyse der Neuheitsökonomie zeigte einen weiteren Grund für das starke
Wachstum: Jedes Kind beginnt mit leerem Umweltgedächtnis und kann dieselben
Werte erneut als subjektiv neu verwerten. `K` transportiert Wahrnehmung und `Z`
bewahrt individuelle Erfahrung, doch der Pfad endet dort. Der Laufzeitzustand
wird nicht vererbt und kann das Genom nicht verändern.

Für v0.5 wird deshalb der bereits im Grundkonzept vorgesehene Rückkanal `Z -> G`
aktiv ausgearbeitet. Die beabsichtigte Kausalkette lautet:

`Umwelt -> K -> Z -> G -> Nachkommen`

Dabei soll weder die Umwelt zielgerichtet in das Genom schreiben noch das
gesamte `Z` automatisch kopiert werden. Das vorhandene Genom muss selbst eine
Strategie hervorbringen, ausgewählte Erfahrung begrenzt und gegen Energiekosten
in eine vererbbare Form zu überführen. Damit erhält die Umwelt erstmals über
individuelle Lebenserfahrung direkten, aber weiterhin evolvierbaren Einfluss
auf spätere Genome.

## Nachspiel: Wo die Alterskante liegt

Die auf `0,01` angehobene Altersrate wirkte stärker als erwartet. Ein neuer
Spielzeuglauf erzeugte nur 18 Nachkommen und starb in Tick 2.134 vollständig
aus. Alle 38 Todesfälle entstanden durch unbezahlbare Standby-Kosten. Zucker
war vorhanden; die steigenden kumulierten Alterskosten und eine bereits in Tick
1.195 endende Fortpflanzung ließen jedoch keine junge Ersatzpopulation zurück.

Die unmittelbare Wiederholung mit ansonsten gleichen Bedingungen und einer
Altersrate von `0,008` erreichte Tick 5.000. Die Population stieg zunächst auf
55, sank bis Tick 2.600 auf 19 und erholte sich anschließend auf 117 Lebende.
Der Lauf zeigt damit erstmals die gesuchte Wellenform, am Ende allerdings auch
wieder beschleunigtes Wachstum. Die Feinabstimmung im Bereich `0,0081` bis
`0,0089` bleibt als spätere Versuchsreihe vorgemerkt.

Die Laufzeit von 137,1 Sekunden ist zugleich die neue Single-Core-Basis. Trotz
des Mehrkernkonzepts lief der Fachkern noch seriell: Das Snapshot-/Intent-Modell
ist spezifiziert, aber `--workers 16` noch nicht implementiert. Diese Umsetzung
hat vor weiteren Parameterreihen Vorrang.
