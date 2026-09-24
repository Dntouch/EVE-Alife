# Die Rammler fraßen den RAM

Status: Gesprächsentwurf

Redaktionelle Einordnung: Dieser Beitrag verarbeitet den ersten großen
Populationsdurchbruch von EVE-Alife v0.4 am 23. und 24. September 2026. Der Lauf
wurde technisch abgebrochen; Aussagen über seinen möglichen Zustand bei Tick
5.000 wären Spekulation.

*Wir wollten wissen, ob am Ende mehr als 20.000 Amöben leben. Am Ende lebte vor
allem die Erkenntnis, dass 64 Gigabyte Arbeitsspeicher auch nur eine
Umweltbedingung sind.*

## Kleine Rammler

Das neue Genommodell begann unscheinbar. Ein Kind erbte nicht mehr eine
willkürliche Zahl von Genompositionen, in die vollständige Funktionsgruppen
irgendwie hineinpassen mussten. Es erbte homologe Plätze. Ein Platz durfte groß
sein. Entscheidend war seine Rolle, nicht seine Länge.

Dann vermehrten sie sich.

Nicht ein bisschen. Aus 20 Gründern wurden erst Hunderte, dann Tausende. Die
Gründer lebten lange, ihre Nachkommen blieben fortpflanzungsfähig, und der
Stammbaum bekam genau den Belastungstest, den wir kurz zuvor eingebaut hatten.

**Stefan:** Unsere Amöben sind kleine Rammler geworden.

Das war keine Übertreibung. Bei Tick 4.034 waren 9.446 Amöben entstanden. 8.761
davon lebten noch. Die Population war weiterhin steil unterwegs.

## Ein sehr stabiler Körper, viele verschiedene Geschichten

Der auffälligste Befund lag im Genom. Frühere Modelle produzierten häufig
verstümmelte Kinder, weil ein vollständiger Funktionsbereich nicht mehr in das
zugeloste Zielgenom passte. Diesmal behielten alle registrierten Genome exakt
198 Bestandteile: 76 Funktionspunkte und 122 Kanten.

Trotzdem waren 8.823 Genomfingerabdrücke verschieden.

**Beobachtung:** Die Vielfalt entstand fast vollständig durch Rekombination,
nicht durch Größenänderung. Nur neun Geburten trugen eine protokollierte
Einzelmutation.

Das ist noch kein Beweis, dass das neue Modell „richtig“ ist. Aber es ist ein
starker Hinweis darauf, dass wir zuvor nicht Evolution beobachtet hatten,
sondern teilweise den Schaden unserer Verpackungsregel.

## Läuft Python eigentlich auf mehreren Kernen?

Mit wachsender Population wurde der Lauf immer langsamer. Die naheliegende Frage
lautete, ob Python nur einen Kern benutze. Tat es. Doch das war nicht das
dringendste Problem.

Die Lupe schrieb nach jedem Tick ein vollständiges Live-Bild. Zuletzt war diese
eine Datei 405 Megabyte groß. Noch schlimmer: Die Simulation behielt alle
Ereignisse seit Laufbeginn im Arbeitsspeicher, obwohl 1.696.250 davon längst in
SQLite angekommen waren.

Wir beschlossen, den Lauf trotzdem unangetastet zu Ende laufen zu lassen und
erst danach aufzuräumen.

Der Computer entschied anders.

## Arbeits­speicherengpass vermieden

Um 02:45 Uhr meldete der Desktop freundlich, ein Speicherengpass sei vermieden
worden. Das war eine ausgesprochen optimistische Formulierung. Der Linux-Kernel
hatte den EVE-Prozess mit rund 52 Gigabyte physischem Speicher und weiteren
Gigabyte Swap erschossen.

Der Run blieb in seinen Dateien auf „running“, weil kein Programm mehr lebte,
das ihm den Tod hätte bescheinigen können.

Es gab auch keinen Checkpoint. Der war erst für Tick 10.000 vorgesehen. Wir
hatten einen Lauf mit Limit 5.000 gestartet und einen Rettungsring hinter das
Ziel gelegt.

**Beobachtung:** Der letzte konsistente Zustand liegt bei Tick 4.034.

**Offen:** Ob die Population bis Tick 5.000 die Marke von 20.000 überschritten
hätte, wissen wir nicht. Wer aus der ansteigenden Kurve eine Gewissheit macht,
erzählt eine hübsche Geschichte, aber kein Ergebnis.

## Die Biologie bleibt, der Datenmüll geht

Die Reparatur verändert keine Reihenfolge, keine Mutation und keine
Umweltwirkung. Sie trennt lediglich die lebende Simulation von ihrer
Beobachtungsbürokratie:

- Persistierte Ereignisse verlassen den Arbeitsspeicher.
- Die Lupe bekommt ein schlankes Live-Bild höchstens zweimal pro Sekunde.
- Vollständige wissenschaftliche Beobachtungen bleiben im Messintervall.
- Genome werden bei ihrer Entstehung registriert, nicht bei jedem Tick erneut.
- Datenbank und Manifest werden in konsistenten Paketen veröffentlicht.

Im Benchmark ist das kompakte Live-Bild bei 1.000 Amöben rund siebenmal kleiner
und etwa zehnmal schneller zu bauen. Danach liegt die verbleibende Rechenzeit
tatsächlich überwiegend dort, wo sie hingehört: in der Ausführung der Genome.

Die Amöben dürfen also weiter Rammler sein. Sie sollen nur nicht mehr jeden
Gedanken, den sie jemals hatten, gleichzeitig im Arbeitsspeicher tragen.

---

Interne Quellen: Run `0ccf273f-6bc6-4a91-a42c-7bca96f9d70b`, Kernelprotokoll,
v0.4-Datenbank, Projektgespräch und Performance-Benchmark vom 24. September
2026. Vor Veröffentlichung folgen Schlussredaktion, Faktenprüfung und
Datenschutzprüfung.

