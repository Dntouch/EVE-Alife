# Die Lupe in Prototyp v0.4

Die Lupe ist die read-only Analyseoberfläche von EVE-Alife. Sie liest laufende
und archivierte Runs, verändert aber weder Simulation noch Run-Daten. Start,
Stopp und Fortsetzung gehören dem getrennten Supervisor.

## Arbeitsbereiche

### Leitstand

Der Leitstand beobachtet den gewählten Run. Das lineare RAM-Band kann gezoomt
und durch Ziehen im leeren Bereich horizontal verschoben werden. Amöben werden
erst dann gruppiert, wenn ihre Markierungen im aktuellen Zoomlevel überlappen.
Identische RAM-Positionen bleiben als auswählbare Gruppe erhalten.

Die Run-Auswahl lädt auch konservierte v0.2-Runs. Das Replay spielt gespeicherte
Beobachtungsbilder ab und ist ausdrücklich kein exakter Tick-Replay.

### Historie

Der Evolutionsverlauf zeigt Population, Genomvielfalt, Geburten, Tode und
laufübergreifend konsistente Schlüsselereignisse. Ziehen wählt einen Zeitraum,
`Strg`/`Cmd` plus Mausrad zoomt und Umschalt-Ziehen verschiebt die sichtbare
Zeitachse. Während eines laufenden Experiments aktualisiert sich die Darstellung
alle zehn Sekunden automatisch. Zoom, Position und Auswahl bleiben dabei
erhalten; ein manueller Aktualisieren-Knopf zeigt zugleich den letzten Abruf an.

Die Amöbenliste unterstützt mehrere kommagetrennte Suchbegriffe als ODER-Suche,
beispielsweise `Ada, Vera, #99`. Suchbegriffe erscheinen als einzeln entfernbare
Chips; nicht gefundene Begriffe werden kenntlich gemacht.

Der Amöben-Desk zeigt unter anderem K, Z, Startenergie S₀, Genomgröße,
Generation, direkte Kinder und den aus der tatsächlich verdrahteten Struktur
abgeleiteten Fortpflanzungsstatus. Vom Leitstand und Stammbaum aus wird die
gewählte Amöbe unmittelbar im Desk geöffnet. Eltern-Kind-Genome können nach
unverändert geerbten, veränderten, anderweitig geerbten, neuen und nicht
übernommenen Bestandteilen verglichen werden.

### Chronik

Die Chronik ist das versionsübergreifende EVE-Archiv. Sie führt v0.2, v0.3 und v0.4
zusammen, ohne ihre Versuchsreihen fachlich gleichzusetzen. Informative
Run-Karten, Run-Dossiers, wirksame Versionsfilter, Run-Rekorde und ein
Zwei-Run-Vergleich erschließen das Archiv. Ein Klick auf eine Run-Karte führt
sichtbar zum zugehörigen Dossier. Die „Hall of Life“ bewahrt die Rekordhalter
einzelner Amöben und öffnet auf Klick den zugehörigen Run und Historieneintrag.

### Stammbaum

Der Stammbaum ist eine evolutionäre Zeitlandschaft. Er zeigt Elternkanten,
Generationen, Lebensstatus, Genomänderungen und Schlüsselereignisse. Beim
Anklicken einer Amöbe bildet eine Verwandtschaftslinse ihre Vorfahren links und
ihre Nachkommen rechts ab. Vorfahren erscheinen cyan, Nachkommen violett.
Unmittelbare Eltern und unmittelbare Kinder werden gegenüber entfernteren
Beziehungen besonders hell dargestellt.

Während eines laufenden Experiments wird der Stammbaum alle zehn Sekunden
nachgeführt, ohne Auswahl, Zoom oder Kameraposition zu verlieren. Umfangreiche
Bäume erscheinen in der Gesamtansicht zunächst als Gruppen aus gleicher
Generation und ähnlicher Geburtszeit. Ein Klick auf eine Gruppe löst sie
räumlich auf; anschließend kann eine einzelne Amöbe fokussiert werden.

Umschalt-Klick vergleicht zwei Amöben und ermittelt ihren letzten gemeinsamen
Vorfahren. Mausrad und Ziehen steuern den zweidimensionalen Arbeitsraum. Ein
Klick auf freie Fläche löst den Fokus und stellt die vorherige Kameraposition
wieder her; `Gesamt` kehrt bewusst zur vollständigen Zeitlandschaft zurück.

### Genom

Die Genomanalyse stellt Funktionspunkte, Ports und gerichtete Verbindungen als
EVE-Netzkarte dar. Klick auf einen Funktionspunkt hebt seine direkten Beziehungen
hervor und blendet Unbeteiligtes ab. Der Arbeitsraum kann zweidimensional
verschoben und bis 64-fach gezoomt werden. Eine Genomkarte lässt sich weiterhin
in einem separaten Fenster öffnen.

Vererbungsplätze sind unmittelbar sichtbar: Jeder Platz besitzt eine eigene
Farbkontur und Kennung an seinen Funktionspunkten. Eine dynamische Legende nennt
je Platz Funktionspunkte, interne Kanten und ausgehende Anschlusskanten. Ein
Klick auf einen Platz isoliert seinen Inhalt und alle beteiligten Übergänge.
Interne Kanten erscheinen in der Platzfarbe; platzübergreifende Anschlusskanten
sind gestrichelt und tragen Quell- und Zielplatz in den Analysedaten.

Kantengewichte sind Bestandteil derselben Analyse. Kopfzeile und Legende zeigen
Zahl und Spannweite veränderter Gewichte. Farbe und Stärke einer Kante
unterscheiden neutrale, verstärkende, dämpfende, blockierende und invertierende
Übertragung. Ein Klick auf die Kante öffnet Quelle, Ziel, erbliches Gewicht,
Quell- und Zielport, interne beziehungsweise platzübergreifende Zugehörigkeit,
prozentuale Übertragung und ihre strukturelle Folge. Im direkten
Eltern-Kind-Vergleich zählt und markiert die Lupe veränderte Kantengewichte und
stellt Eltern- und Kindwert gegenüber. Historische Genome ohne Gewicht werden
in allen Ansichten neutral als `0` dargestellt.

## Fokusmodus

Stammbaum und Genom besitzen einen gemeinsamen Fokusmodus. `Vergrößern`, die
Taste `F` und `Esc` schalten ihn. Navigation und Lupensteuerung bleiben sichtbar,
der Seiten-Scrollbalken verschwindet und die Analyse nutzt den restlichen
Bildschirm. Die Präferenz bleibt beim Wechsel zwischen den Arbeitsbereichen und
innerhalb der Browsersitzung erhalten. Zoom, Position und Auswahl werden nicht
neu initialisiert.

## Run-Steuerung und Beobachtungsgrenze

Die Lupe sendet ausschließlich explizite Start-, Stopp- und Fortsetzungsaufträge
an den Supervisor auf Port 8767. Ein kontrollierter Stopp wird vom Supervisor
ausgeführt und als `user_requested` finalisiert. Eine Fortsetzung erzeugt immer
einen neuen, verknüpften Run; der alte Run bleibt unverändert.

Gespeicherte Beobachtungen liegen je nach Konfiguration nicht für jeden Tick
vor. Historische Zustände zwischen zwei Beobachtungen werden deshalb nicht
erfunden. Protokollierte Ereignisse und automatisch erkannte Auffälligkeiten
werden in Tooltips unterschieden.

## Start

```bash
cd 04_Prototypen/v0.4
python3 supervisor.py
python3 lupe.py runs/DEINE-RUN-ID --port 8766
```

Die Lupe ist anschließend unter `http://127.0.0.1:8766/` erreichbar.

Für den Zugriff aus einem vertrauenswürdigen lokalen Netzwerk kann sie
ausdrücklich auf allen Netzwerkschnittstellen gebunden werden:

```bash
python3 lupe.py runs/DEINE-RUN-ID --host 0.0.0.0 --port 8766
```

Der Supervisor bleibt dabei ausschließlich lokal gebunden. Die Lupe besitzt
keine Anmeldung oder TLS-Verschlüsselung und darf in dieser Form nicht direkt
ins öffentliche Internet freigegeben werden.

## Screenshots

Ein eigener v0.4-Screenshot-Satz entsteht erst, wenn die Genomrevision sichtbar
und fachlich prüfbar ist. Der konservierte v0.3-Abschluss bleibt unter
[`../v0.3/screenshots/`](../v0.3/screenshots/) dokumentiert.
