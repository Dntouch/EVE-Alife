# Vorläufiges Experiment: Spielzeug in der RAM-Suppe

Status: experimentell, nicht als endgültige EVE-Umwelt festgeschrieben

## Ziel und Grenze

Die Amöben sollen schon vor einer späteren Öffnung zur Betriebssystemumwelt externe Veränderung, wiedererkennbare Struktur und einfache Ursache-Wirkung-Beziehungen antreffen. Es werden keine neuen Genomoperationen und keine semantischen Begriffe wie Nahrung, Gefahr oder Schalter eingeführt. Sämtliche Wahrnehmung und Betätigung erfolgt über die vorhandenen `RAM_READ`- und `RAM_WRITE`-Punkte.

## Lokale Koordinaten

Im Spielzeugmodus besitzt jede Amöbe eine eigene `ram_position`; ihre ID bleibt reine Identität. Ein genomisch berechneter RAM-Wert ist ein vorzeichenbehafteter lokaler Offset:

```text
reale Adresse = (ram_position + Offset) modulo RAM-Größe
```

Die ringförmige Abbildung vermeidet besondere Ränder. Membranadressen im separaten virtuellen Bereich bleiben absolut und damit von der Position unabhängig. Beobachtungsereignisse speichern den berechneten Offset und die tatsächlich berührte Adresse.

Gründerpositionen werden mit einer separaten, aus dem Run-Seed abgeleiteten Zufallsquelle über die gesamte Suppe verteilt. Ein Kind entsteht höchstens 32 Zellen von einem zufällig gewählten beteiligten Elternteil entfernt. Die Position ist derzeit nicht erblich und während des Lebens unveränderlich. Bewegung bleibt eine spätere, eigenständig zu spezifizierende genomische Fähigkeit.

Der Run-Modus `--ram-world toys` erzeugt mit einer vom Simulationszufall getrennten, aus dem Seed abgeleiteten Zufallsquelle 128 Spielzeuginseln. Der RAM-Ring wird dafür in gleich große Sektoren geteilt; innerhalb jedes Sektors liegt die Insel an einer seedabhängigen Position. Die Verteilung ist damit flächendeckend, aber weder an Gründer noch an spätere Kinder angepasst. Jede Insel enthält:

- einen **Stein** aus acht zusammenhängenden Zellen mit festem Zahlenmuster; er bleibt normal überschreibbar,
- zwei **Blubberblasen** mit individuellen Perioden von 17 bis 97 Ticks,
- einen **Schalter** aus Trigger- und direkt folgender Ausgabezelle.

Die frühere Mischung aus 16 Steinen, 16 Blasen und 8 Schaltern belegte nur 160 von 65.536 Zellen. Lauf 12 und der beginnende Lauf 13 zeigten, dass die meisten unbeweglichen lokalen Populationen dadurch kein dynamisches Spielzeug erreichen. Die Inselstruktur erhöht deshalb die Auffindbarkeit, ohne einer konkreten Amöbe eine Ressource zuzuteilen. Positionen, Werte, Rhythmen und Kopplungen sind für denselben Seed reproduzierbar und werden in Beobachtung und Checkpoint gespeichert.

## Energie und Herkunft

Eine Blase ist eine externe Umweltänderung und besitzt deshalb keine Amöben-Urheber. Wird ihr neuer Wert individuell als Veränderung gelesen, greift unverändert die bestehende Neuheitsökonomie.

Eine Schalterausgabe ist zwar eine Umweltreaktion, aber kausal von einem Schreibsignal ausgelöst. Sie übernimmt deshalb dessen Urheberkette einschließlich der betätigenden Amöbe. Diese kann sich nicht selbst durch den Schalter ernähren; eine andere, noch nicht beteiligte Amöbe kann die Veränderung entdecken. Damit entsteht ein möglicher sozialer Informationsgewinn, aber kein eingebauter Bonus.

Steine liefern keine wiederkehrende Sonderenergie. Ihr erstes Lesen kann wie jeder bislang unbekannte RAM-Wert belohnt werden.

## Beobachtung und offene Fragen

Autonome und ausgelöste Änderungen werden als `environment_change` mit Typ, Adresse, altem und neuem Wert protokolliert. Die Lupe bleibt read-only.

Zu prüfen ist insbesondere:

- Werden die niedrigen Spielzeuge tatsächlich gefunden?
- Entstehen wiederholte Besuche an Blasen oder Schaltern?
- Betätigen Genome einen Schalter und lesen sie oder andere Amöben dessen Ausgabe?
- Fördern externe Rhythmen tragfähige Populationen oder lediglich triviales Abgrasen?
- Muss die Dichte später gesenkt, räumlich anders verteilt oder dynamisch begrenzt werden?

Eine spätere Betriebssystemöffnung bleibt eine eigene Sicherheits- und Modellentscheidung. Dieser Spielzeugkasten simuliert weder Dateien noch Prozesse und erteilt keine zusätzliche Host-Berechtigung.
