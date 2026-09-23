# 23. September 2026 – Vom Analysewerkzeug zur runden Lupe

## Ziel des Tages

Der am Vortag gesicherte v0.3-Zwischenstand sollte nicht um ein weiteres großes
Werkzeug erweitert, sondern als zusammenhängende Lupe fertiggestellt werden.
Im Mittelpunkt standen Arbeitswege, fehlende Beobachtungsdaten, visuelle
Eindeutigkeit und die Frage, welche Änderungen noch zu v0.3 gehören.

## Historie und Amöben-Desk

Die Historie wurde zu einem vertiefbaren Arbeitsbereich umgebaut. Die kompakte
Amöbenliste bewahrt nun wieder K, Z und Startenergie S₀, zeigt Genomgröße,
Generation und einen vorsichtig abgeleiteten Fortpflanzungsstatus. Auswahlwege
aus Leitstand und Stammbaum öffnen die betreffende Amöbe unmittelbar, statt nur
in den richtigen Arbeitsbereich zu wechseln.

Der Evolutionsverlauf und die RAM-Suppe berücksichtigen die tatsächliche
Pixeldichte des Bildschirms. Dadurch bleiben beide Canvas-Ansichten beim
Skalieren scharf. Der RAM-Zoom verlangt nun eine bewusste Modifikatortaste;
gewöhnliches Scrollen verändert nicht mehr versehentlich den Ausschnitt.

## Genome und Abstammung

Die Genomanalyse zeigt die Gesamtgröße einer Amöbe und erklärt ausgewählte
Funktionspunkte in ihrer möglichen Wirkung. Ein neuer Eltern-Kind-Vergleich
macht unverändert geerbte, veränderte, aus dem anderen Elternteil stammende,
neue und nicht übernommene Genomteile sichtbar. Das ist zunächst bewusst ein
kleiner, nachvollziehbarer Vergleich und kein automatisches Evolutionsurteil.

Im Stammbaum werden unmittelbare Eltern und unmittelbare Kinder gegenüber
weiter entfernten Beziehungen heller hervorgehoben. Eltern stehen zusätzlich
explizit im Detailbereich. Übergänge zur Historie und zum Genom übernehmen die
gewählte Amöbe. Fokusmodus, Kamera und Verwandtschaftslinse wurden gegen
Überlagerungen und abgeschnittene Arbeitsflächen nachgeschärft.

## Chronik und Erscheinungsbild

Die kreisförmigen Run-Signaturen der Chronik wurden durch informative
Archivkarten ersetzt. Jede Karte zeigt Status, Datum, Kurz-ID, Laufdauer,
Populationsmaximum, Nachkommen, Genomvielfalt, Generationstiefe und gewonnene
RAM-Energie. Die Filter für v0.2 und v0.3 zeigen Trefferzahlen und wirken nun
tatsächlich. Ein Klick führt sichtbar zum zugehörigen Run-Dossier.

Das EVE-Wallpaper wurde heller abgestimmt. Neun unabhängig getaktete Lichtpunkte
erzeugen im rechten DNA-Netz gelegentliche cyan- und violettfarbene Impulse.
Bei reduzierter Bewegung bleiben sie aus.

## Kleine biologische Ergänzungen

Anzeigenamen verwenden jetzt einen Pool von 500 Namen und tragen die wirkliche
Generation als Suffix. Die Namen bleiben reine Beobachtungsidentitäten und
verbrauchen keinen Simulationszufall.

Tote Amöben bleiben wissenschaftlich vollständig in Lupe, Historie und
Stammbaum erhalten, können aber als physische Leichen aus der RAM-Suppe
verschwinden. Der erste passende Fund überträgt ausschließlich die tatsächlich
verbliebene Energie; anschließend ist die Leiche nicht mehr lesbar. Das
Ereignis wird dauerhaft protokolliert.

## Grenze zu v0.4

Evolvierbare Kantengewichte wurden fachlich untersucht, aber nicht aktiviert.
Dokumentiert sind die heutige Laufzeitbedeutung einer Kante, der neutrale Wert
`0` und die offenen Fragen zu Wertebereich, Kodierung, Mutation und Wirkung.
Diese Genomänderung gehört ausdrücklich in v0.4.

Als nächster wissenschaftlicher Arbeitsblock folgt die detaillierte Analyse des
10.000-Tick-Laufs `988690e0-ce93-4e14-8eb5-d11a589ec184`. Erst daraus sollen
begründete Versuche zu Alterskosten und weiteren Umweltbedingungen entstehen.

## Abschluss

**Beobachtet:** Zwei Wiederholungen mit identischem Seed und identischen
Parametern verliefen identisch. Der längere 10.000-Tick-Lauf zeigt eine deutlich
reichere Populationsgeschichte und viele schrumpfende Genome; eine belastbare
Ursachenaussage folgt daraus noch nicht.

**Designentscheidung:** v0.3 wird an dieser Stelle als Beobachtungs- und
Analysewerkzeug abgeschlossen. Kantengewichte und mögliche Änderungen der
Umweltbedingungen werden nicht nachträglich in diesen Stand gemischt.

## Artefakte

- [Abschlussbericht v0.3](../04_Prototypen/v0.3/ABSCHLUSSBERICHT.md)
- [Lupe v0.3](../04_Prototypen/v0.3/LUPE.md)
- [Konzept für Kantengewichte](../04_Prototypen/v0.3/KANTENGEWICHTE_KONZEPT.md)
- [Aktueller Screenshot-Satz](../04_Prototypen/v0.3/screenshots/)
- [Blogentwurf 014](../06_Blog/014_Der_Arme_ist_durch_ein_Leichenfeld_gestolpert.md)
