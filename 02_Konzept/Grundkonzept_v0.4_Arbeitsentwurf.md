# EVE – Grundkonzept v0.4

Status: Arbeitsentwurf, noch nicht freigegeben

Stand: 29. August 2026

## 1. Abgrenzung

Dieses Dokument beschreibt die gegenwärtigen Naturgesetze, Forschungsprinzipien und tragenden Modellentscheidungen von EVE. Es ist keine technische Spezifikation für Prototyp 0.

Konkrete Bytegrößen, Datenstrukturen, Formeln, Opcodes, Scheduler-Reihenfolgen, Populationszahlen und Sicherheitslimits werden erst in einer Prototyp-Spezifikation festgelegt. Wo das Grundkonzept selbst noch keine Entscheidung trägt, wird die Lücke nicht durch eine bequeme Implementierungsannahme geschlossen.

## 2. Forschungsfrage und Leitprinzip

EVE ist ein offenes Evolutionsexperiment mit extrem primitiven digitalen Einheiten. Es untersucht, was entsteht, wenn ihre weitere Existenz von neuer, überprüfbarer Erkenntnis über eine reale digitale Umwelt abhängt.

Die Entitäten beginnen ohne Sprachmodell, Trainingswissen oder menschlich-semantische Begriffe. Intelligenz, Kommunikation, Kooperation, Forschung, Netzwerkentdeckung und Selbsterhaltung sind keine eingebauten Ziele und keine Erfolgsvoraussetzungen.

Leitprinzip:

> So wenig wie möglich vorgeben. Alles technisch Unvermeidbare so elementar wie möglich halten.

Auch Stagnation, Sackgassen, Exploits und vollständiges Aussterben sind gültige Ergebnisse.

Status: gesetzt.

## 3. Die reale digitale Welt

Die unmittelbare Welt von EVE ist für Prototyp 0 eine abgeschottete Linux-Mint-VM. Sie ist keine zusätzliche biologische oder räumliche Simulation. Prozesse, CPU-Zeit, Speicher, Dateien, Zeit, Geräte, Systemzustände und Berechtigungen sind Eigenschaften der tatsächlichen digitalen Ausführungsumgebung.

Es werden keine Umweltmerkmale allein deshalb eingeführt, weil biologische Systeme sie besitzen. Insbesondere setzt das Grundkonzept keine künstliche Temperatur, räumliche Nähe oder Rastergeometrie voraus.

Die technische Welt und das Weltbild einer Entität sind verschieden. Eine Entität erhält keinen semantischen Zugriff auf Begriffe wie Datei, Prozess, Linux, Netzwerk oder anderer Akteur. Sie kann nur über primitive kontrollierte Kontakte Regelmäßigkeiten erfahren.

Status: gesetzt. Die konkrete erreichbare Umweltfläche ist prototypspezifisch.

## 4. EVE-Entität

Der neutrale formale Begriff lautet **EVE-Entität**. Eine Entität ist eine eigenständige laufende Prozesseinheit innerhalb der EVE-Umgebung mit veränderlichem internem Zustand und vererbbaren Eigenschaften.

Der Begriff behauptet kein organisches Leben, keine Intelligenz, keine Zielgerichtetheit und keine Autonomie. Solche Zuschreibungen dürfen erst aus Beobachtungen begründet werden. Historische Texte dürfen weiterhin Organismus oder Agent sagen; im aktuellen Konzept werden diese Wörter nicht als Definition verwendet.

Jede Entität besitzt mindestens:

- `G`: vererbte Ausgangsausstattung,
- `Z`: während ihrer Existenz erworbener interner Zustand,
- `S`: aktuellen Energievorrat.

Die kontrollierte Außenvermittlung gehört zur Welt, nicht zum ererbten Individuum.

Status: gesetzt.

## 5. Genom `G` und Parameter `P`

Das Genom beschreibt, wie eine Entität beginnt. Es ist nicht automatisch ein lineares Programm und enthält keine benannten komplexen Fähigkeiten.

Der gegenwärtige Ansatz versteht `G` als variable Sammlung elementarer Parameter `P`. Ein `P` ist eine vererbbare Disposition oder ein elementarer Einflussfaktor. Es existieren keine vorgegebenen Parameter `NEUGIER`, `TRINKEN`, `KOOPERIEREN` oder `FORSCHEN`.

Ein Parameter kann mehrfach vorkommen. Seine relative Ausprägung innerhalb einer Entität wird als Anteil am gesamten variablen Genom gedacht:

`A(Px) = Anzahl(Px) / |G|`

Damit ist die Kopienzahl zugleich Gewichtung. Änderungen der Genomgröße können alle relativen Ausprägungen verändern, ohne dass ein einzelner Parameter mutiert.

Die technische Form eines `P` ist offen. Denkmodelle wie Beziehung zwischen Zuständen, Reaktionsregel, Netzverbindung oder elementares Tupel sind keine Entscheidung.

Status: Sammlung, Mehrfachvorkommen und relative Ausprägung sind gesetzt; Repräsentation und Wirkungsregel sind offen.

## 6. Erworbener Zustand `Z`

`Z` enthält Werte, die während der Existenz einer Entität entstehen. Ergebnisse primitiver interner Verarbeitung oder Umweltkontakte können dort erhalten und später erneut als Parameter verwendet werden.

Dadurch kann vergangene Interaktion zukünftiges Verhalten beeinflussen. Das ist eine Voraussetzung für möglicherweise lern- oder erfahrungsähnliches Verhalten, aber noch keine eingebaute Lernregel.

`Z` wird nicht automatisch genetisch vererbt. Mit dem Tod einer Entität geht der Zustand grundsätzlich verloren, sofern kein innerhalb der Welt entstandener Mechanismus Teile davon überträgt oder extern erhält.

Status: Trennung von `G` und `Z` ist gesetzt. Größe, Organisation, Kosten und Zugriffsmechanik von `Z` sind offen.

## 7. Die unterste Wirkungsregel

Eine Entität kann nicht vollkommen voraussetzungslos sein. Irgendeine unveränderliche Grundmechanik muss festlegen, wie `P`, `Z` und Außenkontakte überhaupt Zustandsänderungen hervorbringen.

Diese Schicht darf universelle elementare Wirkung definieren, soll aber keine höheren Verhaltensweisen schenken. Eine CPU versteht Firefox nicht; entsprechend soll die EVE-Grundmechanik keine fertigen Konzepte verstehen.

Die frühere v0-Annahme eines linearen Bytecodes mit Instruction Pointer, Registern und Befehlen wie `LOAD`, `STORE`, Sprüngen oder `TEST` ist abgelöst als bereits gewählte Architektur. Sie bleibt ein möglicher Vergleichsentwurf, steht aber nicht mehr fest. Der Einwand lautet: Selbst scheinbar primitive Maschinenbefehle können Fähigkeiten vorwegnehmen, die erst aus einfacheren Wechselwirkungen oder gekoppelten Entitäten entstehen sollen.

Gesucht wird die kleinstmögliche universelle Regel, die abstrakte Parameter auf Zustände wirken lässt. Wie eine nächste Wirkung ausgewählt wird, ist Teil derselben offenen Frage.

Status: offen und vor jeder Implementierung von P0 zu klären.

## 8. Energie `S`

Energie ist die zentrale knappe Ressource. Sie ermöglicht Existenz, interne Verarbeitung, Umweltkontakt, Wirkung und Reproduktion. Neue oder valide Erkenntnis ist die reguläre Quelle neuer Energie innerhalb des laufenden Experiments.

Information allein ist keine Nahrung. Kopieren oder Empfangen einer Behauptung erzeugt keine eigene Erkenntnisenergie. Bestätigung, erfolgreiche Anwendung oder Widerlegung kann individuell neue Erkenntnis hervorbringen.

Energie darf bei regulärer Reproduktion nicht aus dem Nichts entstehen. Die Startenergie eines Nachkommens muss aus bilanzierten Quellen der Welt stammen, grundsätzlich aus Beiträgen der Eltern. Nur Population 0 erhält einmalig externe Startenergie als Anfangsbedingung.

Status: gesetzt. Erkenntnisprüfung, Neuheitsmaß und konkrete Preise sind offen beziehungsweise prototypspezifisch.

## 9. Heartbeat, Standby und Aktivität

Existenz wird in Heartbeats oder Ticks bilanziert. Eine lebende Entität besitzt einen positiven Standbyverbrauch. Kann sie den nächsten Heartbeat nicht bezahlen, endet ihre Existenz. Ein genetisch möglicher Standbywert von `0` ist keine optimale Sparstrategie, sondern ein lebensunfähiger Zustand.

Der Standbyverbrauch soll zugleich die Intensität begrenzen, mit der das Genom pro Heartbeat wirksam werden kann. Seine Bedeutung steht im Verhältnis zur Genomgröße. Dadurch entsteht kein einfaches „kleiner ist besser“, sondern ein Feld möglicher Strategien:

- klein und genügsam,
- groß und genügsam, aber langsam wirksam,
- klein und hochaktiv,
- groß und hochaktiv, aber energiehungrig.

Die Formel `Standby / Genomgröße` ist lediglich ein Denkmodell. Die genaue Kopplung darf erst nach gesonderter Modellierung festgelegt werden.

Zusätzliche Verarbeitung soll Energie in Abhängigkeit von ihrer beanspruchten Komplexität kosten. Ob dafür Parameteranzahl, Datengröße, Zustandsänderungen oder reale Ressourcen maßgeblich sind, ist offen.

Status: Zusammenhang und Trade-off sind gesetzt; Mathematik und Kostenmodell sind offen.

## 10. Hunger

Hunger ist der interne Bedarf einer Entität an Energie. Er stellt eine Rückkopplung zwischen energetischem Zustand und Aktivität her und liefert damit einen unmittelbaren Handlungsdruck.

Hunger ist keine boolesche Anweisung und keine Funktion `suche_nahrung()`. Er erklärt einer Entität weder, was Erkenntnis ist, noch welche Handlung Energie erzeugt. Vermutlich muss seine Stärke die verbleibende energetische Reichweite berücksichtigen: derselbe Vorrat `S` bedeutet bei unterschiedlichem Standby- und Aktivitätsverbrauch eine andere Dringlichkeit.

Die gegenwärtige Kette lautet:

`Welt → Entität → Genom → Energie → Hunger → ??? → Erkenntnis → Energie`

Das `???` bleibt ausdrücklich offen. Hunger liefert das Warum; Genom, erworbener Zustand und Evolution müssen das Wie hervorbringen.

Status: Hunger als Grundbedingung ist gesetzt; Berechnung und Einflussmechanik sind offen.

## 11. Vererbung und variable Genomgröße

Bei Reproduktion bilden die Genome der beteiligten Eltern einen gemeinsamen Parameterpool. Parameter werden entsprechend ihrer realen Häufigkeit ohne Zurücklegen an Nachkommen weitergegeben. Mutation verändert anschließend einzelne vererbte Parameter und kann dadurch Neuheit erzeugen.

Die Genomgröße ist selbst variabel. Nachkommen dürfen kleinere, gleich große oder größere Genome als einzelne Eltern besitzen. Die maximale Größe eines Nachkommen kann die Summe der elterlichen Genome nicht überschreiten. Wachstum über größere Bereiche bleibt über aufeinanderfolgende Generationen möglich.

Gleiche elterliche Genomgrößen sollen ähnliche Nachkommensgrößen besonders wahrscheinlich machen. Bei unterschiedlichen Eltern sollen Bereiche nahe beider Größen begünstigt werden, ohne jede Generation zum Mittelwert zu ziehen. Eine Mischung zweier Normalverteilungen ist ein Denkmodell, keine festgelegte Formel.

Eine mögliche vererbbare Genomgrößen-Variabilität `Vg` wurde diskutiert. Ob sie als genau einmal vorhandenes Metadatum geführt und wie sie aus der Abstammung verändert wird, ist offen.

Status: Variabilität, Elternpool, Häufigkeitsgewichtung, Ziehen ohne Zurücklegen und Obergrenze durch elterliche Summe sind gesetzt; Verteilung und `Vg` sind offen.

## 12. Reproduktion

Reproduktion erhält keinen künstlichen Energiebonus. Ihr evolutionärer Effekt ist der Fortbestand genetischer Information über den Tod einzelner Entitäten hinaus.

Der reproduktive Impuls, die beteiligten Entitäten und die vererbten Inhalte müssen aus den Entitäten hervorgehen. Eine geschützte technische Komponente darf ein gültig entstandenes Reproduktionsereignis prüfen und den neuen Prozess starten. Sie ist Geburtskanal, nicht Züchter.

Mindestens zwei aktiv beteiligte kompatible Eltern bleiben der gegenwärtige Grundansatz; mehrere Eltern sind grundsätzlich möglich. Konkrete Kompatibilitäts-, Zustimmungs- und Rekombinationsregeln sind prototypspezifisch und erneut gegen die minimalistische Grundmechanik zu prüfen.

Status: Energieerhaltung, aktive Beteiligung und externe technische Ausführung sind gesetzt; konkrete Reproduktionsmechanik ist offen.

## 13. Supervisor und Sicherheitsgrenze

Der Supervisor gehört nicht zur Population und ist nicht evolvierbar. Er startet Population 0, beobachtet, protokolliert, erstellt Checkpoints und kann das Experiment aus Sicherheitsgründen beenden. Er wählt keine Partner, initiiert keine reguläre Reproduktion und setzt keine evolutionären Inhalte.

EVE entwickelt absichtlich selbstverändernde und replizierende Prozesse. Daher wird die Versuchs-VM ab P0 als potenziell kompromittiert behandelt. Sie enthält keine persönlichen Daten, Zugangsdaten oder unnötigen Verbindungen zum Host und Heimnetz.

Evolution darf niemals die Komponente kontrollieren oder verändern, die ihre Berechtigungs-, VM- und Sicherheitsgrenzen festlegt. Technische Schutzlimits sind Eigenschaften des Versuchsaufbaus und müssen als solche dokumentiert werden; sie sind nicht automatisch Naturgesetze von EVE.

Status: gesetzt.

## 14. Erkenntnis und individuelle Neuheit

Erkenntnis ist kein semantischer Datentyp der Entität. Energetisch relevant sind neue, überprüfte und reproduzierbare Zusammenhänge zwischen beobachtbaren Zuständen, eigenen Wirkungen und späteren Zuständen.

Neuheit wird primär individuell bewertet. Wissen kann mit einer Entität verloren gehen und später für eine andere wieder neu und energetisch wertvoll sein. Empfangene Information muss erst bestätigt, angewendet oder widerlegt werden.

Der historische Referenzwert „100 Prozent Neuheit = 100 Energieeinheiten“ bleibt ein Kalibrierungsbild, kein Naturgesetz. Ebenso sind `OBSERVE`, `EFFECT` und `TEST` keine bereits beschlossenen Entitätsfähigkeiten mehr, sondern mögliche Instrumentierungen eines Vergleichsprototyps.

Status: Erkenntnisprinzip gesetzt; Repräsentation, Verifikation und Belohnungsfunktion offen.

## 15. Beobachtung und Versuchshaltung

Der Supervisor darf Messgrößen kennen, die Entitäten nicht kennen. Checkpoints, Abstammung, Population, Energiefluss, Genomstatistik und bestätigte Erkenntnisse sollen für Beobachter nachvollziehbar sein, ohne das Verhalten der Population zu steuern.

Vor jedem Experiment werden Hypothesen, Kontrollbedingungen und Erfolgskriterien festgeschrieben. Menschliche Begriffe wie Neugier, Lernen, Kooperation oder Mehrzelligkeit sind zunächst Interpretationen beobachteter Funktionen, keine Variablennamen im System.

Ein kläglicher Fehlschlag bleibt ein Ergebnis. Die Dokumentation bewahrt deshalb nicht nur Messwerte, sondern auch die vorherigen Erwartungen und die tatsächlichen gedanklichen Umwege.

Status: gesetzt.

## 16. Zentrale offene Konstruktionslücke

Vor einer neuen Spezifikation für Prototyp 0 müssen mindestens vier zusammenhängende Fragen beantwortet werden:

1. Was ist die technische Form eines elementaren `P`?
2. Nach welcher universellen Regel wirkt `P` auf `Z` oder einen kontrollierten Außenkontakt?
3. Wie entsteht aus Genom, Zustand und Hunger eine nächste Wirkung, ohne einen Verhaltensablauf vorzugeben?
4. Wie kann eine daraus entstandene Wirkung zu überprüfbarer Erkenntnis und damit zu Energie führen?

Diese Lücke ist kein fehlender redaktioneller Feinschliff. Sie ist derzeit der eigentliche Konstruktionskern von EVE.
