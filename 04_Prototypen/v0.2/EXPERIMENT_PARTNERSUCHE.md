# Vorläufiges Experiment: variable genomische Partnersuche

Status: experimentell, nicht als endgültige EVE-Regel festgeschrieben

## Anlass

Im ersten v0.2-Referenzlauf besaßen fünf von sechs Nachkommen keinen `MEM_WRITE`-Funktionspunkt. Zusätzlich bindet sich das P1-Suchgenom an die erste lebend gefundene Amöbe und kann einen lebenden, aber nicht antwortenden Vorschlag nicht zurückziehen. Rekombination und Suchverhalten erzeugen damit zwei getrennte Fortpflanzungsengpässe.

## Minimale Core-Fähigkeit

Eine Amöbe darf ausschließlich ihren eigenen Partnerslot genomisch mit `0` leeren. Der Supervisor trifft weder Zeitpunkt noch Partnerwahl. Todbeobachtung bleibt ein möglicher Grund, ist aber nicht mehr der einzige genomisch ausdrückbare Rückzug. Setzen einer fremden ID verlangt weiterhin den realen Fund einer lebenden fremden Membran.

## Suchverhalten bleibt Genom

Der Core kennt keine benannten Strategien. Das Startgenom drückt Verhalten ausschließlich mit vorhandenen Funktionspunkten, Kanten, `CONST`, K und Z aus. Experimentell veränderbare Werte sind:

- relativer Startoffset zur eigenen ID,
- vorzeichenbehaftete Schrittweite (Richtung und Raster),
- Geduld beziehungsweise Zahl eigener Prüfzyklen,
- später gegebenenfalls Suchspanne und Kandidatenbedingung.

Diese Werte sind vererbbar und durch die bestehende CONST-Mutation schrittweise veränderbar. Ausgangswerte werden reproduzierbar aus kleinen Bereichen gestreut; sie definieren keine Arten oder dauerhaften Klassen.

## Rekombination

Zusammenhängende Komponenten bleiben atomar. Statt zufälligem greedy Einfüllen wird eine Fragmentkombination gewählt, deren Größe die gezogene Zielgröße bestmöglich erreicht, ohne sie zu überschreiten. Unter gleich guten Kombinationen entscheidet der vorhandene Simulationszufall. Große Sozialkomponenten werden weder garantiert noch bevorzugt; sie sollen lediglich nicht mehr durch eine deutlich schlechter passende Folge kleiner Fragmente verdrängt werden.

## Prüffragen

- Sinkt der Anteil von Nachkommen ohne `MEM_WRITE`?
- Entstehen weiterhin unterschiedliche Genomgrößen und Komponentenkombinationen?
- Führen unterschiedliche Offsets und Schrittweiten zu unterschiedlichen Kontakten?
- Kann ein Genom eine erfolglose lebende Wahl selbst zurückziehen?
- Erhöht das die Zahl gegenseitiger Partnerschaften und Folgegenerationen?
- Entsteht ein neuer dominanter Suchmodus, ohne dass er technisch vorgegeben wurde?

Ergebnisse werden zunächst als Vergleich zum eingefrorenen P1-Lauf 41 und zum ersten v0.2-Referenzlauf dokumentiert. Eine Übernahme ins konsolidierte Konzept erfolgt nicht automatisch.

## Erster Vergleich über 200 Ticks

| Stand | Nachkommen | Lebend | RAM-Energie | RAM-Leseereignisse | Slot-Schreiben | Rückzüge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| alte v0.2-Referenz | 6 | 26 | 43.235 | 2.035 | 54 | 0 |
| variables Suchgenom | 0 | 19 | 26.910 | 1.112 | 26 | 2 |
| neues uniformes Kontrollgenom | 0 | 15 | 20.370 | 1.027 | 37 | 0 |

Run-IDs: Referenz `b24a6681-4ade-47e6-9532-61435cc9c774`, variabel `6a20088b-b100-4c12-9db1-6a6ee9c53586`, uniform `59389b3e-0390-467d-b3bc-e674ca967b9c`.

Die Streuung allein erklärt das Ergebnis nicht, weil auch der uniforme neue Kontrolllauf keine Geburt erreichte. Die zusätzliche Rückzugsschaltung vergrößert Genom und Kantenzahl, senkt damit Ausführungsbudget und erhöht Lebenshaltungskosten. Das ist ein reales Modellresultat der gewählten Darstellung und kein Grund, die Wirtschaft stillschweigend nachzuregeln. Vor einer Konsolidierung ist zu entscheiden, ob Rückzug mit weniger vorhandenen Bausteinen codiert, als eigene primitive Fähigkeit modelliert oder zunächst aus dem Startgenom entfernt werden soll.
