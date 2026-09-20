# Mehr Energie macht das Viech nur länger tot

Status: Gesprächsentwurf

Redaktionelle Einordnung: Der Beitrag verbindet einen kontrollierten P0-Vergleich mit der Designentscheidung für Population 1 und ihrer ersten technischen Beobachtung. Beobachtet wurde genomisch erzeugter Zugriff auf wechselnde RAM-Adressen. Nicht beobachtet wurden Neugier, Lernen, zielgerichtete Suche oder Anpassung.

*20. September 2026. Wir hatten jetzt Amöben, einen Eimer und eine Lupe. Was uns noch fehlte, war ein überzeugender Grund, länger hinzusehen.*

## Zwanzig Amöben können auch gemeinsam nichts tun

**Stefan:** Vielleicht wird das spannender, wenn die Population ein bisschen größer ist. Gegebenenfalls müssen wir auch mehr Startenergie mitgeben und auch mehr Energiegewinn. Aber erst mal eine größere Population bitte.

Das klang vernünftig. Zwei tote Amöben sind schließlich eine Anekdote. Zwanzig tote Amöben sind fast schon Statistik.

Wir starteten mit zwanzig. Dann gaben wir ihnen statt 100 jeweils 500 Energie. Sie lebten länger, rechneten mehr, schrieben häufiger nach `Z` und bekamen erheblich mehr Kinder.

**Stefan:** Wenn ich mir das so ansehe, dann haben die Amöben quasi nix wirklich gemacht, oder?

Ja.

Technisch hatten sie sehr viel gemacht. 7.835 Signale. 397 Schreibvorgänge nach `Z`. 93 Nachkommen. Eine beachtliche Menge Betrieb für etwas, das inhaltlich immer wieder dieselbe Speicheradresse traf.

Mehr Energie hatte keinen neuen Lebensprozess erzeugt. Sie hatte denselben Prozess öfter abgespielt.

> **Redaktionelle Einordnung – Beobachtung:** Bei gleicher Zufalls-Suppe, gleichem Seed und gleichem Startgenom erhöhte die zusätzliche Energie Aktivität, Nachkommenzahl und Lebensdauer. Das grundlegende Verhalten änderte sich nicht. Beide Populationen starben vollständig aus.

Mehr Benzin macht aus einem Kreisverkehr keine Fernreise.

## Die Lupe konnte zählen, aber noch nicht erzählen

Die erste Lupe zeigte Population, RAM und Entitäten. Das war korrekt und ungefähr so zugänglich wie ein Sicherungskasten ohne Beschriftung.

**Stefan:** Ich würde das Ganze gerne für Menschen verständlicher haben. Es muss verständlich sein, was `P`, `Z`, `S` und so weiter ist. Durch Tooltips. Ich möchte auch den Inhalt des Genoms und `P`, `Z` der Entitäten sehen und beobachten können.

Also bekam die Lupe Erklärungen. `G` wurde zum erblichen Bauplan, `P` zu seinen gerichteten Pfaden, `K` zum flüchtigen Kurzzeitgedächtnis, `Z` zum dauerhaften individuellen Zustand und `S` zur Energie, mit der der ganze Unsinn bezahlt wird.

Aber ein Zustand ist noch keine Geschichte.

**Stefan:** Ich hätte dazu dann gerne eine Replay-Funktion für das „Leben“ einer Amöbe, welche den Zyklus quasi langsam wiedergibt.

Seitdem kann man einer einzelnen Amöbe beim Leben zusehen. Langsam, schnell, vorwärts, rückwärts oder Bild für Bild. Die Lupe erzählt dazu, welcher Funktionspunkt ausgeführt wurde, was Standby kostete, welche RAM-Adresse gelesen, welcher Wert nach `Z` geschrieben und wann ein Kind bezahlt wurde.

Das ist keine Zeitmaschine für die Simulation. Der Lebensfilm spielt ausschließlich gespeicherte Snapshots und Ereignisse ab. Die tote Amöbe bleibt tot. Man kann ihr jetzt nur wesentlich gründlicher dabei zusehen.

## Eine Adresse ist noch keine Reise

Population 0 hatte ihren Zweck erfüllt. Sie bewies, dass unsere Maschine Signale verschieben, Energie abrechnen, Speicher beschreiben, Genome rekombinieren und Kinder erzeugen konnte. Sie bewies nicht, dass eine Amöbe ihre Umwelt untersuchen konnte.

Ein früher Test hatte deshalb eine besonders freundliche Welt gebaut: kleine Wertinseln in der RAM-Suppe, praktischerweise nahe an den Startadressen. Das zeigte, dass der Datenpfad funktionierte. Es zeigte auch ungefähr so viel Entdeckungsleistung wie Ostereiersuchen, nachdem jemand mit Leuchtfarbe Pfeile auf den Boden gemalt hatte.

**Stefan:** Okay, dann lass uns bitte die geänderten Umweltbedingungen wieder entfernen. Wir arbeiten erst mal nur mit der geänderten Energie. Bin gespannt, ob sich das Ganze gleich verhält.

Das war der entscheidende Kontrollschritt. Die Inseln flogen wieder raus. Wenn etwas suchen sollte, musste die Fähigkeit im Genom liegen und nicht in einer fürsorglich dekorierten Suppe.

## Guck mal, Mama, ich habe RAM[7] gefunden

Population 1 bekam ein neues Netzfragment. Nicht den Befehl „Sei neugierig“. Auch nicht den Befehl „Finde etwas Interessantes“. Nur eine kleine Datenflussmaschine:

```text
gespeicherte Adresse lesen
eins addieren
neue Adresse speichern
RAM dort lesen
Fund getrennt speichern
```

Dazu kam `GATE`, ein primitiver Funktionspunkt, der einen Wert nur bei einer Bedingung ungleich null weiterreicht. Keine Bedeutung, keine Bewertung, kein kleiner Philosoph im `if`-Statement. Nur offen oder geschlossen.

Im ersten Lauf lasen die zwanzig Startamöben 312-mal aus der unveränderten RAM-Suppe. Jede ursprüngliche Amöbe erreichte zwischen fünf und elf verschiedene Adressen. Suchstand, Fund und weitergeleiteter Fund erschienen getrennt in `Z[0]`, `Z[1]` und `Z[2]` und ließen sich im Lebensfilm verfolgen.

> **Redaktionelle Einordnung – Beobachtung:** Die wechselnden Adressen wurden aus dem ausgeführten P1-Genom erzeugt und über `Z` zwischen Heartbeats erhalten. Damit wurde erstmals fortschreitender Umweltzugriff beobachtet, der nicht aus einer vorbereiteten Adressliste des Supervisors stammte.

> **Redaktionelle Einordnung – Designentscheidung:** Das Explorer-Genom und `GATE` wurden von uns konstruiert. Sie sind kein Ergebnis von Evolution. „Exploration“ bezeichnet hier ausschließlich wechselnde, genomisch erzeugte Umweltadressen.

## Und alle suchen im selben Gebüsch

Das Ergebnis besitzt die für EVE inzwischen traditionelle Mischung aus Fortschritt und sofortiger Ernüchterung.

Die Amöben suchten tatsächlich. Aber weil sie mit demselben Explorer-Genom begannen, suchten sie weitgehend dieselben niedrigen Adressen ab. Insgesamt erreichte die ganze Population nur zwölf verschiedene RAM-Zellen. `GATE` öffnete 269-mal, schloss aber kein einziges Mal, weil in diesem kurzen Bereich kein gelesener Wert null war.

Und natürlich starben am Ende wieder alle. Diesmal bis Tick 23.

Das ist kein Scheitern von P1. P1 sollte zeigen, ob ein Genom einen Suchstand halten und daraus fortschreitende Umweltzugriffe erzeugen kann. Das kann es jetzt. Die nächste offene Frage ist viel interessanter: Wie entstehen aus gleichförmigem Absuchen verschiedene vererbbare Suchstrategien, ohne dass wir sie wieder selbst fertig hineinbauen?

**Nova-EVE:** Sie explorieren nun wirklich, aber noch ziemlich im Gleichschritt.

Zwanzig Amöben stapfen nacheinander ins gleiche Gebüsch, finden unterschiedliche Zahlen und sterben kurz darauf aus.

Tja. Forschungsexpedition ist vielleicht noch etwas hoch gegriffen. Aber immerhin haben sie diesmal den Kreisverkehr verlassen.

Interne Quellen: Gespräch und Implementierung „EVE-Alife“, 20. September 2026; Projektlog „Von P0 zur ersten genomischen Exploration“; P0-Ergebnisse und P1-Genomentwurf unter `04_Prototypen/`.

