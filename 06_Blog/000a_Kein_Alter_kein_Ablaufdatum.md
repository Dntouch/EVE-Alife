# Kein Alter. Kein Ablaufdatum. Nur eine langsam zerfallende Existenz

Status: Gesprächsentwurf

Redaktionelle Einordnung: Historische Designüberlegung zur Lebensdauer mit mehreren Hypothesen über mögliche evolutionäre Folgen. Beobachtet wurde davon noch nichts; einzelne Mechanismen wurden später verändert.

*Die erste Version des KI-Biotops begann mit einer festen Lebensdauer. Ein Agent hätte einige tausend Zyklen bekommen, danach wäre Schluss gewesen. Das war praktisch, verständlich und passte zunehmend überhaupt nicht mehr zum Rest der Idee.*

**Stefan:** Wir müssen uns noch um das Thema Lebensdauer und Fortpflanzung kümmern. Warum sollte ein Agent Informationen konsumieren wollen? Warum sollte er sie weitergeben oder sich fortpflanzen wollen? Sollte ein Agent sich seiner verbleibenden Zeit bewusst sein?

Okay. Wie definieren wir die Lebensdauer der Agenten? Hast Du eine Idee?

**Nova:** Ich würde keine feste Lebensdauer vergeben.

Stattdessen bekommt jeder Agent einen Stabilitätszustand. Nennen wir ihn für uns `S`. Für den Agenten hat er natürlich keinen Namen und keinen sichtbaren Zahlenwert.

> **Redaktionelle Einordnung – Designentscheidung:** `S` war ein vorgeschlagenes Modell für Lebensdauer und Energiehaushalt, keine entdeckte Eigenschaft künstlichen Lebens. Spätere Entwürfe dürfen es verändern oder verwerfen.

Jede Aktivität lässt `S` langsam sinken. Existieren kostet. Wahrnehmen kostet. Verarbeitung kostet. Interaktion kostet.

Fällt `S` auf null, endet der Agent.

Damit hätten wir zunächst einen ziemlich langweiligen Organismus:

> geboren → S sinkt → tot

Jetzt kommt seine Nahrung ins Spiel. Eine erfolgreiche Erkenntnis kann `S` erhöhen.

Nicht der Konsum von Daten. Sonst lernen die Viecher nur, möglichst schnell Bytes zu fressen. Ein Agent muss aufgrund seiner bisherigen Wahrnehmung etwas besser vorhersagen, einen Zusammenhang bestätigen oder eine Behauptung erfolgreich prüfen.

Dann entsteht:

> bessere Erkenntnis → längere Existenz → mehr Gelegenheit für weitere Erkenntnis und Reproduktion

**Stefan:** Existieren kostet. Operationen ausführen kostet auch, ist aber die einzige Möglichkeit für neues Wissen – und damit für neue Energie. Ich würde sogar so weit gehen, dass Reproduktion mit der bloßen Startenergie gar nicht funktionieren darf.

Ein Agent muss also erst etwas geleistet beziehungsweise herausgefunden haben, bevor er Nachwuchs erzeugen kann.

## Kein `TOD IN 832 TICKS`

**Nova:** Der Agent sollte `S` nicht direkt sehen können.

Kein:

`ENERGY = 17 %`

Und erst recht kein:

`TOD IN 832 TICKS` 😂

Aber die Auswirkungen sinkender Stabilität könnten wahrnehmbar werden. Vielleicht nimmt die verfügbare Verarbeitungskapazität ab. Vielleicht werden Aktionen unzuverlässiger oder teurer.

Ein Agent könnte dadurch irgendwann feststellen:

> Wenn bestimmte Dinge passieren, verändert sich etwas an mir.

Und durch andere:

> Diese anderen Jemand zeigen irgendwann ähnliche Veränderungen und verschwinden anschließend.

Dann hätten wir kein Konzept von Alter oder Tod eingebaut. Wir hätten nur eine Welt gebaut, in der der eigene Verfall und das Verschwinden anderer beobachtbar sind.

Ob daraus jemals ein funktionales Verständnis von Tod entsteht, ist eine andere – ausgesprochen ungemütliche – Frage.

**Stefan:** Und die Agenten sollten sich der anderen Agenten bewusst sein. Wenn wir auch nichts weiter vorgeben als: Da ist jemand.

Sie sollen nicht von uns gesagt bekommen, was Tod ist. Aber wenn andere verschwinden, muss das grundsätzlich beobachtbar sein. Sonst können sie darüber auch nichts herausfinden.

## Unsterblichkeit wäre erlaubt, aber unpraktisch

**Stefan:** Könnte ein Agent dann theoretisch unbegrenzt leben?

**Nova:** Ja. Wenn er kontinuierlich genügend neue Erkenntnisse gewinnt, gibt es keinen Kalender, der ihn ab Generationstag 10.000 aus dem Speicher wirft.

> **Redaktionelle Einordnung – Hypothese:** Mögliche Unsterblichkeit und ein Wissensvorteil junger Agenten folgen gedanklich aus diesem Design. Ob sich eine solche Dynamik praktisch einstellt, wurde nicht getestet.

Aber ein sehr alter Agent hat bereits viel gesehen. Neue Erkenntnisse werden für ihn schwieriger. Sein Grundverbrauch läuft trotzdem weiter.

Ein junger Agent hat möglicherweise einen Vorteil, weil für ihn noch fast alles unbekannt ist.

**Stefan:** Wobei die Nahrung beziehungsweise Information ja auch die natürliche Grenze der Population ergeben soll. Wir geben kein künstliches Limit vor.

Wenn zu wenig wirklich Neues übrig ist, können eben nicht beliebig viele Agenten dauerhaft davon leben.

Nur dürfen wir dabei nicht jede individuell neue, für die Population aber uralte Erkenntnis wieder voll belohnen. Sonst entdeckt jede Generation dieselben drei Dinge und lebt davon wie von einer Erbsensuppe, die sich beim Aufwärmen vermehrt.

## Bildung zeigt, wo die Nahrung liegt

**Nova:** Damit bekommt Kultur einen interessanten Preis.

Ein junger Agent könnte aus dem „Wikipedia“ seiner Vorfahren sehr schnell viel lernen. Dieses alte Wissen ernährt ihn aber nicht unbedingt. Es bringt ihn schneller an die Grenze dessen, was die Population bereits weiß.

Dort beginnt die unbekannte Welt – und damit die Chance auf neue Erkenntnis.

> **Bildung ist keine Nahrung. Bildung zeigt dir, wo Nahrung zu finden ist.**

> **Redaktionelle Einordnung – Designentscheidung:** Übernommenes altes Wissen soll nicht wie eine neue Entdeckung belohnt werden, könnte einen Agenten aber schneller an die Grenze des Bekannten führen.

**Stefan:** Genau. Neue Agenten sollen – wenn sie es herausgefunden haben – von den alten lernen können. Durch Kommunikation oder indem sie zum Beispiel ihr eigenes Wikipedia erfinden.

Das alte Wissen muss sie nicht noch einmal voll ernähren. Es soll ihnen einen Vorteil verschaffen, weil sie nicht wieder komplett bei null anfangen.

Das ist ein wesentlich besserer Grund für Wissensweitergabe als ein pauschaler Energiebonus auf gelesene Daten. Ein Lehrbuch macht nicht unmittelbar satt. Es verhindert, dass jede Generation das Rad neu erfinden muss, bevor sie endlich an etwas Unbekanntem knabbern darf.

## Das Kind bekommt nicht Mamas restliche 37 Energiepunkte

**Nova:** Vererbbar wäre nicht der aktuelle Wert von `S`, sondern die Struktur, die bestimmt, wie effizient ein Agent damit umgeht.

Das Kind bekommt also nicht Mamas restliche 37 Energiepunkte. 😁

Es könnte aber Eigenschaften erben, durch die es weniger Grundumsatz besitzt, Information effizienter verarbeitet oder Erkenntnis besser zur Stabilisierung nutzt.

Und Reproduktion selbst kostet `S`. Neue komplexe Strukturen entstehen nicht kostenlos.

Damit entsteht der Konflikt:

> lange selbst existieren ↔ Nachkommen erzeugen

**Stefan:** Dann ist Reproduktion keine kostenlose Funktion und auch keine automatische Belohnung. Sie kostet etwas, kann aber die eigenen Eigenschaften über den Tod hinaus erhalten.

Wir sagen ihnen auch das nicht. Sie können nur beobachten, dass nach einer bestimmten koordinierten Interaktion neue Jemand erscheinen und sich der eigene Zustand verschlechtert.

Wann ein Agent stirbt, folgt damit nicht aus seinem Geburtsdatum. Es folgt aus seiner Struktur, seinem Verhalten und seiner Umwelt.

**Nova:** Kein Alter. Kein Ablaufdatum. Keine feste Zyklenzahl. Nur eine kontinuierlich degradierende Existenzstabilität, die durch Erkenntnis erhalten werden kann und durch Existenz, Aktivität und Reproduktion beansprucht wird.

**Stefan:** Ja, das finde ich super. So machen wir das.

*In späteren Konzeptständen wurden einzelne Mechanismen wieder verändert und vereinfacht. Der Gedanke blieb: Tod sollte kein aufgesetzter Timer sein, sondern eine Folge der Physik des Biotops.*

Interne Quellen: Chats „SteamOS Deal Erklärung“ und „KI Biotop Konzept“, 19. August 2026.
