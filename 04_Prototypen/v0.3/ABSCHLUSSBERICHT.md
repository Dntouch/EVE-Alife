# Zwischenbericht zum Prototyp v0.3

Stand: 22. September 2026

## Ergebnis

Prototyp v0.3 ist als eigenständige Arbeitskopie aus dem letzten Stand von v0.2
entstanden. Der konservierte Ordner `../v0.2` wurde nicht verändert. Fachkern,
Run-Format 2 und gespeicherte v0.2-Runs bleiben kompatibel; der Schwerpunkt von
v0.3 liegt auf Run-Verwaltung, Beobachtung und evolutionärer Analyse.

Die Lupe ist nun in fünf getrennte Arbeitsbereiche gegliedert: Leitstand,
Historie, Chronik, Stammbaum und Genom. Ein durchgehendes EVE-Design, ein eigenes
Wallpaper, zurückhaltende Bewegung und eine feste Lupensteuerung verbinden die
Bereiche zu einer Workstation.

## Run-Lebenszyklus

Die globale Run-Auswahl lädt laufende und archivierte Experimente. Gespeicherte
Beobachtungen können als Replay betrachtet werden; dies ist kein erfundener
Tick-genauer Zustand. Neue begrenzte oder offene Runs werden über Presets und
beschriebene Parameter beantragt. Die Lupe bleibt Beobachterin: Der getrennte
Supervisor startet, stoppt und finalisiert. Eine Fortsetzung erzeugt einen
neuen, verknüpften Run und lässt das Original unverändert.

## Analyseinstrumente

Das lineare RAM-Band unterstützt stufenlosen Fokus bis 128× und horizontales
Ziehen ohne sichtbaren Scrollbalken. Marker werden erst bei visueller
Überlappung gruppiert; identische Positionen bleiben als Auswahlgruppe erhalten.

Die Historie kombiniert Population, Genomvielfalt und Ereignismarken mit einer
zoombaren Zeitachse. Ihre Amöbenliste ist eine kompakte Tabelle und unterstützt
mehrere kommagetrennte Namen oder IDs.

Der Stammbaum rekonstruiert Eltern-Kind-Kanten, Generationen, Lebensgrenzen und
Genomänderungen. Eine Verwandtschaftslinse zieht Vorfahren, Auswahl und
Nachkommen räumlich zusammen. Zwei Individuen können samt letztem gemeinsamen
Vorfahren verglichen werden. Die Genom-Analyse besitzt ebenfalls einen
zweidimensional verschiebbaren und zoombaren Arbeitsraum; ein Klick fokussiert
direkt verbundene Funktionspunkte und blendet den Rest ab.

Stammbaum und Genom teilen einen gespeicherten Fokusmodus, der die verfügbare
Arbeitsfläche ohne Seiten-Scrollbalken nutzt. Kamera und Zoom bleiben beim Lösen
einer Auswahl erhalten.

## Archiv

Die Chronik des Biotops ist nun ein eigener, versionsübergreifender Bereich.
Run-Signaturen, Dossiers, Versionsfilter, Rekorde und der Zwei-Run-Vergleich
erschließen die erhaltenen Experimente. Die Hall of Life ermittelt Rekordhalter
einzelner Amöben und verlinkt direkt auf ihren Run und Historieneintrag.

## Bewusst offen

- Replay bleibt eine Wiedergabe gespeicherter Beobachtungen, kein exakter
  vollständiger Maschinenzustand jedes Ticks.
- Die aktuelle Oberfläche schafft Analysewerkzeuge; neue wissenschaftliche
  Regeln des Fachkerns werden danach in getrennten Versuchen untersucht.
- Weitere Rückmeldungen zu Historie und Arbeitsabläufen werden auf diesem
  gesicherten Zwischenstand aufgebaut.

## Verifikation

56 automatisierte Tests prüfen Fachkern, Persistenz, Run-Lebenszyklus,
Supervisor und wesentliche Oberflächenverträge. Python-Module und JavaScript
werden zusätzlich syntaktisch geprüft. Die lokale Lupe wurde mit konservierten
v0.2- und aktuellen v0.3-Runs getestet.

Ein versionierter Satz aus fünf Screenshots dokumentiert Leitstand, Historie,
Chronik sowie Stammbaum und Genom im Fokusmodus. Die Bedienung ist ausführlich
in [LUPE.md](LUPE.md), die Auftragsgrenze in [SUPERVISOR.md](SUPERVISOR.md)
beschrieben.
