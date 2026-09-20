# Wir sind offenbar versehentlich in einem echten Forschungsproblem gelandet

Status: Gesprächsentwurf

Redaktionelle Einordnung: Fachliche Einordnung anhand existierender ALife-Systeme sowie Abgrenzung und Hypothesen zu EVE. Eine Neuheit oder wissenschaftliche Wirksamkeit des EVE-Ansatzes ist damit nicht nachgewiesen.

*Irgendwann zwischen digitalem Urschlamm, Erkenntnis als Nahrung und der Frage, ob Evolution vielleicht ein eigenes Wikipedia erfinden könnte, stellte Stefan eine unangenehm vernünftige Frage.*

**Stefan:** Was mich zusätzlich interessiert: Hat das schon einmal jemand in der Art probiert? Also macht das überhaupt Sinn, oder ist das von Anfang an schon scheiße, weil bereits jemand herausgefunden hat, dass es nicht klappt?

**Nova:** Die beruhigende Nachricht zuerst: Unser Grundgedanke ist keineswegs Quatsch.

Die weniger beruhigende Nachricht: Wir sind damit in einem Forschungsgebiet gelandet, das **Artificial Life**, kurz **ALife**, heißt. Genauer berühren wir **Digital Evolution** und eines seiner besonders hartnäckigen Probleme: **Open-Ended Evolution**.

> **Redaktionelle Einordnung – Interpretation:** Die Zuordnung zu ALife und OEE beschreibt lediglich die fachliche Nachbarschaft unserer Fragestellung. Sie belegt weder, dass EVE neu ist, noch dass das Projekt überhaupt wissenschaftliche Relevanz erreicht oder wissenschaftlich erfolgreich sein wird.

**Stefan:** Okay, und das wissenschaftliche Feld, wo wir da räubern, ist Artificial Life?

**Nova:** Japp. Artificial Life ist ziemlich genau das wissenschaftliche Regal, aus dem wir uns schamlos bedienen.

Die klassische ALife-Frage lautet nicht unbedingt: Wie programmiert man eine möglichst intelligente Maschine?

Sie lautet eher: Was passiert, wenn man eine Umwelt hinstellt, ein paar primitive Viecher hineinwirft und ihnen erlaubt, sich zu vermehren, zu verändern und gegenseitig das Leben schwerzumachen?

Das klingt verdächtig nach unserem Eimer.

## Vor uns war bereits Leben im Rechner

**Nova:** Ein berühmter Vorfahr ist **Tierra** von Thomas S. Ray. Dort lebten selbstreplizierende Programme in einem virtuellen Computer. Rechenzeit funktionierte als Energie, Speicher als Material. Die Programme mutierten, konkurrierten – und irgendwann entstanden unter anderem Parasiten, obwohl niemand eine Funktion `WERDE_PARASIT()` eingebaut hatte.

Das war eine ziemlich eindrucksvolle Demonstration: Digitale Evolution kann tatsächlich ökologische Beziehungen hervorbringen.

Ein weiterer wichtiger Verwandter ist **Avida**. Auch dort mutieren und vermehren sich digitale Organismen. Zusätzliche Ressourcen erhalten sie unter anderem, wenn sie bestimmte logische Berechnungen ausführen.

**Stefan:** Dann ist unsere Idee also doch schon durch?

Wenn andere Systeme bereits digitale Organismen, Evolution und sogar Parasiten hervorgebracht haben, müssen wir sauber sagen können, was bei EVE überhaupt anders ist – ohne so zu tun, als hätten wir das ganze Feld gerade neu erfunden.

**Nova:** Nicht ganz. Avida kann beispielsweise festlegen: Eine bestimmte logische Operation ist wertvoll. Die Organismen müssen den Weg dorthin evolutionär finden, aber wir haben vorher entschieden, welche Leistung Nahrung bringt.

Bei EVE möchten wir möglichst nicht sagen:

> NAND ist gut. Hier, nimm Energie.

Wir möchten eher sagen:

> Du hast etwas über deine Umwelt herausgefunden, das für dich neu, überprüfbar und reproduzierbar ist. Hier, nimm Energie.

Das ist ein kleiner Satz mit einem absurd großen Rattenschwanz.

Denn plötzlich müssen wir nicht nur Evolution ermöglichen. Wir müssen entscheiden, wann eine Beobachtung tatsächlich eine neue Erkenntnis ist, wer sie bereits kennt, wie sie bestätigt oder widerlegt wird und ob ihr Wert sinkt, sobald alle sie millionenfach wiederholen.

**Stefan:** Ich denke, dass wir mit unserem Konzept tatsächlich andere Ergebnisse erzielen könnten, da wir ja versuchen, einen eigenen Antrieb für das Erlangen von neuem Wissen zu generieren. Ich denke, dass genau das den bisherigen AI-Lösungen oder Ansätzen fehlt.

Die Agenten lösen nicht nur eine Aufgabe, die wir bereits kennen. Sie sollen einen eigenen Grund entwickeln, überhaupt nach etwas Neuem zu suchen.

Natürlich legen wir mit Erkenntnis als Energie trotzdem einen Selektionsdruck fest. Aber wir legen möglichst nicht fest, welche konkrete Erkenntnis sie gewinnen oder welche Strategie sie dafür benutzen sollen.

**Nova:** Ja – mit einer wichtigen Einschränkung.

Es gibt bereits **intrinsische Motivation**, **curiosity-driven learning** und **Novelty Search**. Die Idee, Neuheit statt nur eines starren Ziels zu belohnen, ist also nicht neu.

Unser besonderer Dreh wäre die evolutionäre Kopplung von Erkenntnis und Existenz:

`Ohne Erkenntnis → keine zusätzliche Energie → irgendwann tot.`

Wir schreiben keinem Agenten `curiosity = 0.7` ins Hirn. Wenn alles gutgeht, entsteht ein Verhalten, das funktional wie Neugier aussieht, weil stumpfes Wiederholen auf Dauer nicht satt macht.

## Ein Ökosystem aus Erkenntnis – und aus Betrug

**Stefan:** Wissen kann dabei ja auch wieder verloren gehen. Bei der Menschheit gab es Rückschläge und Dinge, die später erneut gelernt werden mussten.

Und wenn eine mitgeteilte Information nachweislich falsch ist, wäre auch diese Widerlegung eine neue Erkenntnis – also Nahrung.

Mich interessiert deshalb nicht nur der einzelne Entdecker. Es geht ebenso darum, ob Wissen erhalten bleibt, ob andere es prüfen und ob eine Population nach einem Rückschlag wieder an denselben Punkt gelangt.

**Nova:** Daraus könnten sehr verschiedene Strategien entstehen:

- Entdecker, die neue Regelmäßigkeiten finden,
- Prüfer, die Behauptungen anderer bestätigen,
- Informationssammler,
- Kommunikatoren,
- Spezialisten,
- Parasiten, die von fremdem Wissen leben,
- und natürlich Täuscher, denn irgendein kleines Mistvieh wird versuchen, unsere Bewertungsfunktion anzulügen.

Vielleicht verschwindet Wissen mit einer Population. Vielleicht wird es später wiederentdeckt. Vielleicht wird es weitergegeben, verfälscht, geprüft oder widerlegt.

Dann hätten wir nicht bloß Organismen, die Aufgaben lösen, sondern ein kleines **Erkenntnis-Ökosystem**.

> **Redaktionelle Einordnung – Spekulation:** Entdecker, Prüfer, Täuscher und Wissensverlust sind mögliche ökologische Rollen und Dynamiken. Keine davon wurde in EVE beobachtet.

Das ist die ambitionierte Lesart. Die nüchterne Lesart lautet: Wahrscheinlich finden die Agenten zuerst eine peinliche Lücke in unserer Belohnungsfunktion und werden steinreich, indem sie digitalen Müll produzieren.

Beides wäre ein Ergebnis.

## Das Problem, an dem alle knabbern

**Nova:** Tierra und viele verwandte Systeme zeigen zugleich ein Grundproblem: Evolution kann interessant loslegen und später stagnieren. Sie findet einige erfolgreiche Tricks, optimiert sie – und dann wird aus der vermeintlich grenzenlosen Evolution eine sehr effiziente Fußgängerzone.

Open-Ended Evolution fragt deshalb, unter welchen Bedingungen fortlaufend neue Formen, Fähigkeiten und Organisationsweisen entstehen können, ohne dass wir jede nächste Aufgabe von Hand vor die Tür legen.

Das ist bis heute kein sauber gelöstes Problem.

Auch EVE entkommt einer weiteren Grenze nicht: Wir bauen die primitiven Wahrnehmungen, Aktionen und Naturgesetze. Was prinzipiell nicht durch diese Schnittstellen erreichbar ist, kann kein Agent entdecken. Wir können die Ontologie verstecken, aber wir können nicht so tun, als hätten wir keine geschaffen.

**Stefan:** Also ist nicht bereits bewiesen, dass unser Ansatz scheitert?

Das war meine eigentliche Sorge. Nicht, ob ähnliche Ideen existieren – das wäre eher beruhigend –, sondern ob längst bekannt ist, dass genau dieser Mechanismus zwangsläufig in einer Sackgasse endet.

**Nova:** Nein. Aber ebenso wenig ist bewiesen, dass er dauerhaft offene Evolution erzeugt.

Realistisch wäre zunächst ein kontrolliertes Experiment: gleiche Population, gleiche Umwelt, gleiche Mutation – aber unterschiedliche Selektionsmechanismen. Einmal klassische Ressourcen oder festgelegte Aufgaben, einmal neue überprüfbare Umweltinformation als Energiequelle.

Dann messen wir nicht: „Ist das Wesen neugierig?“

Wir messen beispielsweise:

- Wie vielfältig sind seine Strategien?
- Wie lange entstehen neue überprüfbare Zusammenhänge?
- Wird Wissen weitergegeben?
- Bilden sich Prüfer, Parasiten oder Täuscher?
- Stagniert die Population früher oder später als in der Kontrolle?

Erst danach dürfen wir interpretieren.

**Stefan:** Ich bin vor allem gespannt, ob das irgendwann einen wissenschaftlich interessanten Status erreichen kann.

Wobei ich nicht einmal den Anspruch habe, etwas nachweislich völlig Neues zu entdecken. Entweder wir machen etwas, das so interessant ist, dass sich jemand anderes dafür interessiert – oder wir haben einfach Spaß und gewinnen unsere eigenen neuen Erkenntnisse.

Sauber dokumentieren müssen wir es in beiden Fällen. Sonst können wir weder zeigen, warum etwas interessant war, noch vernünftig nachvollziehen, warum es gescheitert ist.

**Nova:** Ich kenne jedenfalls kein etabliertes System, das genau unsere Kombination zum Zentrum macht: individuelle Neuheit, Überprüfung, Energiegewinn, Wissensverlust und Wiederentdeckung sowie evolutionär entstandene Wissensweitergabe. Das ist kein Beweis, dass es keines gibt. Es bedeutet nur, dass wir nicht offensichtlich eine bekannte Bauanleitung nachmalen.

Wir sind offenbar versehentlich in einem echten, ungelösten Forschungsproblem gelandet.

> **Redaktionelle Einordnung – Interpretation:** Open-Ended Evolution ist ein reales Forschungsproblem. Ob EVE einen neuen oder hilfreichen Beitrag dazu leisten kann, bleibt eine offene Hypothese.

**Stefan:** Das ist ja schon einmal eine super coole Information.

Aus einer herumgesponnenen Idee wird dadurch nicht automatisch Wissenschaft. Aber wir wissen jetzt wenigstens, dass unsere Fragen in ein echtes Forschungsfeld gehören und wo wir nach Vergleichssystemen und bekannten Problemen suchen müssen.

**Nova:** Vollkommen. Wir wollten einen Eimer mit digitalen Einzellern bauen und haben unterwegs ein wissenschaftliches Regal umgeworfen.

## Referenzen aus dem umgeworfenen Regal

- Thomas S. Ray: [Evolution, Ecology and Optimization of Digital Organisms – Tierra](https://tomray.me/pubs/tierra/)
- Avida-Forschungsplattform: [Ontology for the Avida digital evolution platform](https://www.nature.com/articles/s41597-023-02514-3)
- Joel Lehman und Kenneth O. Stanley: [Exploiting Open-Endedness to Solve Problems Through the Search for Novelty (PDF)](https://www.cs.ucf.edu/~gitars/cap6671-2010/Presentations/lehman_alife08.pdf)
- Rui Wang et al.: [Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions](https://proceedings.mlr.press/v119/wang20l.html)

Interne Quellen: Chats „KI Biotop erweitern“ und „EVE Bedeutung erklären“, August 2026.
