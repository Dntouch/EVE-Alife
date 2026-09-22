# 22. September 2026 – Die Lupe wird zur EVE-Workstation

## Ausgangslage

Die Lupe konnte bereits viel, aber sie behandelte beinahe alles als Inhalt einer
langen Seite. Live-Beobachtung, historische Auswertung, Amöbenkarten und Genome
lagen dicht beieinander. Die Oberfläche erfüllte ihren Zweck, wirkte jedoch wie
ein gewachsenes Diagnosewerkzeug und nicht wie ein zusammenhängendes Instrument.

Für Prototyp v0.3 wurde der letzte Stand von v0.2 kopiert und anschließend
konservativ weiterentwickelt. Der Ordner v0.2 blieb unverändert. Auch das
Run-Datenformat blieb bei Version 2, weil für die neue Oberfläche keine neuen
fachlichen Simulationsdaten erfunden werden mussten.

![Die Chronik des Biotops mit Run-Signaturen und Hall of Life](../04_Prototypen/v0.3/screenshots/03-chronik.png)

## Vom Livebild zum Leitstand

Live und Historie wurden getrennt. Das RAM erschien fortan als lineares Band
statt als Oval. Der Ring blieb als fachlicher Hinweis sichtbar, aber die
Arbeitsfläche ließ sich nun bis 128-fach zoomen und ohne sichtbaren Scrollbalken
durch Ziehen verschieben. Überlappende Amöben werden abhängig vom aktuellen
Zoomlevel gruppiert; identische Positionen öffnen eine explizite Auswahl.

Die Run-ID wurde zur globalen Run-Auswahl. Alte Runs können geladen und ihre
gespeicherten Beobachtungen als Replay betrachtet werden. Ein separater
Supervisor übernahm Start, kontrollierten Stopp und Fortsetzung. Damit blieb die
Lupe fachlich read-only, obwohl sie als Bedienoberfläche Aufträge auslösen kann.

## Die Genomkarte wird ein Arbeitsraum

Die Genomdarstellung zog in einen eigenen Bereich. Funktionspunkte erhielten
eine EVE-Farbsprache, Ports, gerichtete Verbindungen und ein räumliches Raster.
Ein Klick fokussiert zusammenhängende Beziehungen; der übrige Graph wird
unscharf. Weil Genome evolutionär stark wachsen können, lässt sich der Raum in
beide Richtungen verschieben und bis 64-fach zoomen.

## Eine Landschaft aus Abstammung

Der neue Stammbaum wurde nicht als Organigramm, sondern als evolutionäre
Zeitlandschaft gebaut. Gespeicherte Elternkanten, Lebensgrenzen und
Rekombinationsprovenienz bilden seine Datenbasis. Eine Verwandtschaftslinse
zieht die gewählte Amöbe mit ihren Vorfahren und Nachkommen zusammen. Der
Vergleich zweier Individuen markiert ihre Entwicklungspfade und bestimmt den
letzten gemeinsamen Vorfahren.

Schlüsselereignisse wie erste Fortpflanzung, Populationsmaximum und größter
Genomsprung verwenden dieselbe visuelle Sprache in Stammbaum und Historie.
Protokollierte Ereignisse bleiben von analytisch erkannten Auffälligkeiten
unterschieden.

## Historie und Chronik werden getrennt

Der Evolutionsverlauf der Historie erhielt Population, Genomvielfalt,
Geburts-/Todesimpulse, Scanner, Ereignismarken und eine zoombare Zeitachse. Die
Amöbensuche kann mehrere kommagetrennte Namen oder IDs gleichzeitig filtern.

Die bisherige „Chronik des Biotops“ war dagegen keine Analyse eines einzelnen
Runs. Sie wurde zu einem eigenen Archivbereich. Dort stehen v0.2- und v0.3-Runs
als Run-Signaturen, können verglichen und direkt in Leitstand, Historie oder
Stammbaum geöffnet werden. Die Hall of Life bewahrt die Rekordhalter einzelner
Amöben über alle archivierten Runs.

## Fokusmodus

Stammbaum und Genom erwiesen sich als zu mächtig für eine gewöhnliche
Dashboard-Kachel. Beide erhielten einen Fokusmodus, der die Arbeitsfläche bis an
Navigation und Lupensteuerung erweitert und den Seiten-Scrollbalken entfernt.
Die Einstellung bleibt beim Wechsel der Werkzeuge erhalten.

## Stand am Tagesende

**Beobachtet:** Die neue Lupe liest sowohl v0.2- als auch v0.3-Runs, ohne das
Format zu ändern. 56 automatisierte Tests sichern Fachkern, Datenhaltung,
Supervisor und wesentliche Oberflächenverträge.

**Designentscheidung:** v0.3 ist zunächst eine neue Beobachtungs- und
Arbeitsoberfläche auf dem konservierten v0.2-Fachstand. Neue wissenschaftliche
Regeln werden erst nach der Oberflächenarbeit wieder getrennt untersucht.

**Offen:** Weitere Rückmeldungen zu Historie und Arbeitsabläufen werden am
Folgetag gesammelt. Der heutige Stand wird bewusst als Zwischenstand gesichert.

## Artefakte

- [Prototyp v0.3](../04_Prototypen/v0.3/README.md)
- [Lupe v0.3](../04_Prototypen/v0.3/LUPE.md)
- [Supervisor v0.3](../04_Prototypen/v0.3/SUPERVISOR.md)
- [Versionierter Screenshot-Satz](../04_Prototypen/v0.3/screenshots/)
- [Blogentwurf 013](../06_Blog/013_Die_Lupe_die_einen_Stammbaum_verschluckte.md)
