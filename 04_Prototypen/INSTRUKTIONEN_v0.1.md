# EVE-Alife – Instruktionen für Prototyp v0.1 und Lupe

## 1. Verbindliche Grundlage

Für die fachliche Ausgestaltung des Experiments gilt ausschließlich das vorhandene **EVE-Alife-Konzept**.

Dieses Konzept ist die maßgebliche Quelle für alle inhaltlichen Regeln und Definitionen, insbesondere für:

- Weltmodell
- Organismen
- Genom
- Mutation
- Reproduktion
- Energiehaushalt
- Wahrnehmung
- Aktionen
- Ressourcen
- Lebenszyklus
- Tod
- Abstammung
- Simulationsregeln
- weitere biologische oder evolutionäre Mechanismen

Diese Instruktion ersetzt das Konzept nicht und soll keine davon abweichenden Regeln definieren.

Falls diese Instruktion und das EVE-Alife-Konzept inhaltlich unterschiedlich interpretiert werden könnten, hat das **EVE-Alife-Konzept Vorrang**.

Keine fachlichen Details ergänzen oder erfinden, nur weil sie technisch naheliegend erscheinen.

---

# 2. Ziel des ersten Prototypen

Der erste Prototyp soll eine möglichst kleine, verständliche und funktionsfähige Umsetzung des bereits definierten EVE-Alife-Konzepts darstellen.

Ziel ist nicht, möglichst viele Funktionen einzubauen.

Ziel ist:

**Die im Konzept beschriebene Kernidee in einer minimalen, beobachtbaren und reproduzierbaren Simulation lauffähig zu machen.**

Nur das implementieren, was für diesen ersten sinnvollen Lauf tatsächlich notwendig ist.

---

# 3. Experimentkern

Der eigentliche EVE-Alife-Experimentkern bleibt selbst kontrolliert, nachvollziehbar und offen.

Zum Experimentkern gehören alle Komponenten, die direkten Einfluss auf den Verlauf des Experiments haben.

Dazu zählen insbesondere:

- Simulationszustand
- Simulationszeit
- Organismen
- Umwelt
- Regeln
- Evolution
- Zufallsmechanismen
- Supervisor des Experiments
- Speicherung und Wiederherstellung des Simulationszustands

Die konkrete fachliche Ausgestaltung richtet sich jeweils nach dem **EVE-Alife-Konzept**.

Für den Experimentkern keine fertigen Frameworks verwenden, die wesentliche Teile der Evolutions-, Agenten- oder Artificial-Life-Logik übernehmen.

Der experimentrelevante Code soll original, offen und nachvollziehbar bleiben.

Allgemeine technische Standardbibliotheken dürfen selbstverständlich verwendet werden.

---

# 4. Die Lupe

Die Beobachtungs- und Visualisierungsschicht heißt:

**Lupe**

Die Lupe ist ausdrücklich **nicht Teil des biologischen Experiments**.

Sie darf deshalb geeignete bestehende Open-Source-Bibliotheken und Frameworks verwenden, zum Beispiel für:

- Benutzeroberfläche
- Visualisierung
- Diagramme
- Rendering
- Datenanalyse
- Datenhaltung
- Netzwerkkommunikation

Hier besteht kein Zwang, alles selbst zu implementieren.

---

# 5. Zentrale Regel der Lupe

Die Lupe darf:

**beobachten, darstellen und analysieren.**

Sie darf das Experiment nicht beeinflussen.

Die Simulation muss vollständig ohne laufende Lupe funktionieren.

Wird die Lupe beendet oder getrennt, darf sich der weitere Verlauf des Experiments dadurch nicht ändern.

---

# 6. Informationsfluss

Der fachliche Informationsfluss soll grundsätzlich nur in eine Richtung gehen:

**EVE-Core → Lupe**

Die Lupe erhält ausschließlich Beobachtungsdaten.

Sie darf keine Entscheidungen innerhalb des Experiments treffen und keine biologischen oder evolutionären Parameter verändern.

Falls Bedienfunktionen wie:

- Start
- Stop
- Pause
- Fortsetzen
- Speichern
- Laden
- Simulationsgeschwindigkeit

benötigt werden, gehören diese zu einer klar getrennten **Supervisor-/Control-Schnittstelle** und nicht zur Beobachtungsschnittstelle der Lupe.

Diese Trennung soll auch im Code eindeutig sichtbar sein.

---

# 7. Observation Interface

Zwischen Core und Lupe soll eine klar definierte read-only Beobachtungsschnittstelle existieren.

Diese Schnittstelle darf unter anderem liefern:

- aktuellen Simulationszustand
- relevante Ereignisse
- Snapshots
- statistische Daten
- Abstammungsinformationen

Welche konkreten Zustände, Ereignisse und Eigenschaften existieren, richtet sich nach dem **EVE-Alife-Konzept**.

Die Lupe soll nicht direkt auf interne veränderbare Datenstrukturen des Core zugreifen.

---

# 8. Ereignisse und Snapshots

Der Core soll ausreichend Informationen bereitstellen, damit ein Simulationslauf später nachvollzogen werden kann.

Dafür sollen zwei Arten von Daten vorgesehen werden:

**Events**

für relevante Veränderungen innerhalb des Experiments.

**Snapshots**

für vollständige oder hinreichend vollständige Zustandsabbilder zu bestimmten Simulationszeitpunkten.

Welche Events und welche Zustandsdaten konkret sinnvoll sind, aus dem bestehenden Konzept und der tatsächlichen Implementierung ableiten.

Keine zusätzlichen biologischen Konzepte nur für die Beobachtung erfinden.

---

# 9. Reproduzierbarkeit

Jeder Simulationslauf soll eindeutig identifizierbar sein.

Mindestens vorzusehen:

- Run-ID
- verwendeter Random Seed
- verwendete Konfiguration
- EVE-Alife-Version
- Codeversion beziehungsweise Git-Commit

Soweit technisch möglich, sollen identische Ausgangsbedingungen reproduzierbare Läufe ermöglichen.

Die Lupe darf niemals den Zufallszustand des Experimentkerns beeinflussen.

---

# 10. Zeitmodell

Das Zeitmodell des Experiments richtet sich nach dem EVE-Alife-Konzept.

Die Lupe soll zwischen:

- Simulationszeit
- realer Laufzeit

klar unterscheiden.

Die reale Laufzeit darf keinen Einfluss auf die fachliche Evolution haben.

---

# 11. Anforderungen an die erste Lupe

Die erste Version der Lupe soll bewusst funktional und schlicht bleiben.

Sie soll vor allem ermöglichen:

- den aktuellen Weltzustand zu sehen
- einzelne Organismen zu untersuchen
- wichtige Zustände und Eigenschaften sichtbar zu machen
- Populationsentwicklungen zu verfolgen
- evolutionäre Veränderungen über Zeit sichtbar zu machen
- Abstammungsinformationen nachvollziehen zu können
- vergangene Zustände beziehungsweise Snapshots betrachten zu können

Welche Werte konkret angezeigt werden, ergibt sich aus dem EVE-Alife-Konzept und den tatsächlich vorhandenen Daten.

---

# 12. Keine Interpretation erzwingen

Die Lupe soll nicht selbst entscheiden, ob etwas:

- intelligent
- erfolgreich
- optimal
- emergent
- fortschrittlich
- überlegen

ist.

Sie soll Beobachtungsdaten darstellen und Analyse ermöglichen.

Interpretation erfolgt durch den Beobachter.

Keine künstlichen Scores oder Klassifikationen einführen, sofern sie nicht ausdrücklich Bestandteil des EVE-Alife-Konzepts sind.

---

# 13. Abstammung

Falls das EVE-Alife-Konzept Abstammungsinformationen vorsieht, müssen diese so gespeichert werden, dass die Lupe sie später auswerten kann.

Die erste Version muss daraus noch keine aufwendige Stammbaumdarstellung erzeugen.

Wichtig ist zunächst:

**Datenverlust vermeiden.**

Informationen, die später experimentell interessant sein könnten, sollten nicht deshalb fehlen, weil die erste Lupe sie noch nicht darstellen kann.

---

# 14. Debugging und Lupe

Debugging und Beobachtung sind getrennte Bereiche.

Debugging dient der Entwicklung des Programms.

Die Lupe dient der Beobachtung des Experiments.

Debug-Ausgaben dürfen daher nicht als langfristige Beobachtungsschnittstelle missbraucht werden.

---

# 15. Performance

Für den ersten Prototypen gilt folgende Priorität:

1. korrekte Umsetzung des Konzepts
2. Verständlichkeit
3. Reproduzierbarkeit
4. Beobachtbarkeit
5. Performance

Keine unnötige Parallelisierung oder technische Optimierung einbauen.

Erst reale Engpässe messen und anschließend gezielt optimieren.

---

# 16. Persistenz

Ein Simulationslauf soll gespeichert und später untersucht werden können.

Das konkrete Speicherformat soll:

- offen
- einfach
- nachvollziehbar
- versionsfähig

sein.

Die technische Lösung darf pragmatisch gewählt werden.

Keine komplexe Infrastruktur aufbauen, solange sie nicht notwendig ist.

---

# 17. Architektur

Bevorzugte grobe Struktur:

**EVE-Core**

führt das Experiment gemäß EVE-Alife-Konzept aus.

↓

**Observation Interface**

stellt read-only Beobachtungsdaten bereit.

↓

**Lupe**

visualisiert und analysiert diese Daten.

Zusätzlich getrennt:

**Supervisor / Control**

für technische Steuerung des Simulationsprozesses.

Die Lupe darf nicht Bestandteil der Simulationslogik werden.

---

# 18. Keine Konzept-Erweiterung während der Implementierung

Besonders wichtig:

Wenn bei der Umsetzung eine fachliche Frage auftaucht, die das vorhandene EVE-Alife-Konzept nicht eindeutig beantwortet, nicht stillschweigend eine eigene Lösung erfinden.

Stattdessen:

1. offene Frage kennzeichnen
2. technisch neutrale Stelle vorbereiten
3. Entscheidung im Konzept ergänzen lassen
4. anschließend implementieren

Technische Detailentscheidungen dürfen selbstverständlich selbst getroffen werden, solange sie das Experiment fachlich nicht verändern.

---

# 19. Nicht überbauen

Der erste Prototyp ist ein Experiment, kein fertiges Produkt.

Deshalb zunächst vermeiden:

- Microservices
- Cloud-Infrastruktur
- verteilte Systeme
- komplexe Authentifizierung
- Plugin-Systeme
- umfangreiche Framework-Abstraktionen
- unnötige Datenbankarchitektur
- große UI-Designsysteme
- hypothetische Erweiterungspunkte ohne aktuellen Bedarf

Ein einfacher sauberer Aufbau ist ausdrücklich erwünscht.

---

# 20. Leitlinie

Bei jeder Designentscheidung prüfen:

**Gehört diese Entscheidung zur Technik oder verändert sie das Experiment?**

Wenn sie nur Technik betrifft:

pragmatisch entscheiden.

Wenn sie das Experiment beeinflusst:

im EVE-Alife-Konzept nachsehen.

Wenn das Konzept dazu nichts sagt:

nicht erfinden.

---

# 21. Zielzustand von v0.1

Am Ende soll vorhanden sein:

- ein lauffähiger EVE-Alife-Core gemäß Konzept
- ein reproduzierbarer Simulationslauf
- persistierbare Runs
- eine klar getrennte Beobachtungsschnittstelle
- eine erste funktionierende Lupe
- grundlegende Live- und Verlaufsvisualisierung
- Möglichkeit, einzelne Organismen und relevante Experimentdaten zu untersuchen
- saubere Grundlage für weitere Experimente

Der erste Prototyp muss nicht schön sein.

Er muss verständlich genug sein, dass wir ihm beim Leben zusehen können.
