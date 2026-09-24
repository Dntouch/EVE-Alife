# Entscheidungen

Dieses Dokument hält bewusste konzeptionelle Entscheidungen fest.

Eine Entscheidung sollte mindestens Datum, Gegenstand, Entscheidung, Begründung und mögliche Folgen enthalten. Gesprächsideen und Arbeitshypothesen sind noch keine Entscheidungen.

## 2026-09-24: `Z -> G` wird Evolutionsachse von v0.5

Gegenstand: Einfluss individuell erfahrener Umwelt auf das vererbbare Genom.

Entscheidung: **v0.5 führt einen begrenzten, evolvierbaren und energetisch
kostenpflichtigen Rückkanal `Umwelt -> K -> Z -> G -> Nachkommen` ein.** Die
Umwelt schreibt nicht selbst und nicht zielgerichtet in `G`. Ein Genom muss die
Disposition und ausführbare Strategie hervorbringen, ausgewählte Erfahrung aus
`Z` in eine vererbbare Form zu überführen. Neue Entitäten erben nicht
automatisch den vollständigen Lebensspeicher ihrer Eltern.

Begründung: In v0.4 startet jedes Kind mit leerem Umweltgedächtnis und kann
bereits bekannte Umweltwerte erneut als subjektive Neuheit energetisch nutzen.
Zugleich endet der gegenwärtige Erfahrungspfad bei `Z`; die Umwelt selektiert
Genome nur indirekt und kann keine im Leben erworbene Information genomisch
wirksam machen. Der bereits am 6. September vorgesehene seltene Pfad `A_ZG`
soll diese Lücke öffnen, ohne festzulegen, welches Wissen nützlich ist.

Mögliche Folgen: v0.5 benötigt eine eigene Spezifikation für Schreiboperation,
Kapazitätsgrenze, Energiekosten, Kodierung, Rekombination, Mutation,
Beobachtbarkeit und Sicherheitsgrenzen. Zu prüfen ist insbesondere, ob der
Mechanismus als genetische Assimilation, epigenetische Vererbung oder eigene
EVE-Kategorie beschrieben wird. v0.4 bleibt ohne aktiven `Z -> G`-Pfad
konserviert.

Herkunft: Auswertung der v0.4-Populationsexplosion und des spielzeugfreien
Kontrolllaufs am 24. September 2026; Konkretisierung der Entscheidung
„Anschlussfähigkeit für seltenes `A_ZG`“ vom 6. September 2026.

## 2026-09-20: Eindeutige Projektbezeichnung EVE-Alife

Gegenstand: Abgrenzung des Artificial-Life-Projekts von EVE, der Home-Assistant-Assistentin.

Entscheidung: Das Projekt wird in neuen Texten **EVE-Alife** genannt. Die Bezeichnung kombiniert **Emergent Virtual Evolution** und **Artificial Life**; „EVE alive“ ist ein beabsichtigter sprachlicher Nebeneffekt. Historische Bezeichnungen bleiben als Teil der Entstehungsgeschichte erhalten.

Begründung: Beide Projekte trugen im Gespräch denselben Namen und wurden dadurch wiederholt vermischt.

Mögliche Folgen: Neue Dokumente und spätere öffentliche Repositories verwenden EVE-Alife als eindeutigen Namen. Der EVE-Assistant, Home Assistant und seine Werkzeuge gehören nicht zu EVE-Alife.

Herkunft: Gespräch „EVE Identität Beibringen“, 20. September 2026.

## 2026-09-20: Isolation wird durch die Umgebung erzwungen

Gegenstand: Sicherheitsgrenze des experimentellen Kerns.

Entscheidung: **Isolation ist eine Eigenschaft der Umgebung, keine Verhaltensregel ihrer Bewohner.** Für eine nicht erreichbare Fähigkeit oder Ressource darf keine technisch nutzbare Schnittstelle existieren. Die erste Grenze bleibt bewusst langweilig: definierter Input hinein, Beobachtungsdaten hinaus, sonst nichts. Kein Internet, kein frei zugängliches Host-Dateisystem, keine Shell und keine erreichbaren Netzwerkdienste für evolvierende Entitäten.

Begründung: Prompts, Konventionen und gewünschtes Verhalten sind keine belastbaren Sicherheitsgrenzen. Fehlverhalten und überraschende Strategien sind gerade in einem Evolutionsexperiment zu erwarten.

Mögliche Folgen: Die Isolation muss außerhalb der Kontrolle von Entitäten und Evolution implementiert und getestet werden. Spätere Erweiterungen der Umweltfläche benötigen jeweils eine neue bewusste Entscheidung und ein Threat Model.

Herkunft: Diskussion eines fehlkonfigurierten KI-Pentests im Gespräch „EVE Identität Beibringen“, 20. September 2026.

## 2026-09-20: Eigenproduktion im experimentellen Kern

Gegenstand: Zulässige Abhängigkeiten innerhalb und außerhalb des Schlammeimers™.

Entscheidung: Alles, was Regeln oder Verhalten des Experiments unmittelbar bestimmt, wird selbst geschrieben und quelloffen veröffentlicht. Dazu zählen insbesondere Supervisor, Weltmodell, Entitäten, Evolution, Mutation, Ressourcenlogik, Interaktionen und Simulationsregeln. Externe Libraries oder Frameworks dürfen diese Funktionen nicht implementieren.

Compiler, Betriebssystem, Programmiersprache und Standardbibliothek gelten als Infrastruktur. Die **Lupe** außerhalb des experimentellen Kerns darf bestehende Frameworks für Visualisierung, Analyse, UI und Datenansicht nutzen, solange sie ausschließlich beobachtet und das Experiment nicht beeinflusst.

Begründung: Evolutionär relevante Vorgänge sollen vollständig auf nachvollziehbaren eigenen Code zurückführbar sein, ohne unnötig Compiler, Betriebssystem oder Darstellungswerkzeuge neu zu erfinden.

Mögliche Folgen: Zwischen Kern und Beobachtungsschicht ist eine schmale, einseitige und dokumentierte Schnittstelle erforderlich. Neue Abhängigkeiten müssen danach bewertet werden, ob sie kausalen Einfluss auf das Experiment besitzen.

Herkunft: Gespräch „EVE Identität Beibringen“, 20. September 2026.

## 2026-09-06: RAM-Suppe, geschütztes Inneres und Membran

Gegenstand: Erste tatsächlich erreichbare Umweltfläche der Entitäten.

Entscheidung: Die gemeinsame Umwelt ist zunächst ein vom Supervisor bereitgestellter beziehungsweise reservierter RAM-Bereich. Dateien, Pfade und höherwertige OS-Konzepte sind für Entitäten in dieser Stufe nicht erreichbar. Entitäten belegen abgegrenzte Bereiche; `G` und `Z` bleiben geschützt. `S` wird ausschließlich vom Supervisor verwaltet. Die Entität darf ihren eigenen aktuellen Wert über den primitiven Funktionspunkt `S-read` lesen, ihn aber niemals schreiben oder anderweitig manipulieren. Die Membran ist ein supervisor-kontrolliertes adressierbares Interface, das `G`, `Z` und fremde Energiezustände nicht offenlegt.

Begründung: Die RAM-Suppe schafft eine minimale gemeinsame Umwelt, ohne den Entitäten bereits die Semantik oder Komplexität eines Betriebssystems zu schenken.

Mögliche Folgen: Die Entscheidung präzisiert die reale Linux-Umwelt als spätere, nicht anfängliche Umweltfläche. Entity-ID und weitere Membranoffsets bleiben Arbeitshypothesen beziehungsweise offene Ausgestaltung.

Herkunft: Konzeptarbeit vom 6. September 2026.

## 2026-09-06: `P` als vererbbare gerichtete Datenflusskante

Gegenstand: Technische Grundbedeutung eines Genomparameters `P`.

Entscheidung: `P` bezeichnet die kleinste vererbbare gerichtete Datenflusskante von einem Ausgangsport eines elementaren Funktionspunkts zu einem Eingangsport eines anderen Funktionspunkts: `P: A.out → B.in`. Der Wert fließt nur in Pfeilrichtung. Erst mehrere `P` bilden ein funktionales Datenflussnetz. Verhalten entsteht aus Netztopologie, `Z`, RAM-Suppe und primitiven Operationen, nicht aus einem einzelnen fertigen Befehl oder benannten Verhaltensparameter.

Begründung: Das Modell gibt elementare Datenbewegung und Verknüpfung vor, ohne einen linearen Kontrollfluss oder eine fertige Verhaltensfolge in das Genom einzubauen.

Mögliche Folgen: Der frühere offene Netz-Kandidat wird konkretisiert. Die frühere allgemeine Gleichsetzung von relativer P-Häufigkeit und phänotypischer Ausprägung ist für Kanten nicht mehr gesichert. Taktung, Codierung und Portlogik bleiben offen.

Herkunft: Konzeptarbeit vom 6. September 2026.

## 2026-09-06: Leeres `Z`, lesbares `S` und doppelt sättigende Neuheitsökonomie

Gegenstand: Anfangszustand, Energiewahrnehmung und supervisorseitige Bewertung des Energiegewinns.

Entscheidung: Eine neue Entität startet mit `G = Genom`, `Z = leer` und `S = Startenergie`. `G` erzeugt die ersten Aktionen; `Z` ist der beschreibbare erworbene interne Zustand und entsteht ausschließlich aus der eigenen Ausführungsgeschichte. Ein ungeeignetes Genom, das keine ausreichenden Energiegewinne erschließt, verbraucht die Startenergie und stirbt aus.

Nur der Supervisor verändert und bilanziert `S`. Die Entität darf ihren aktuellen eigenen Energiewert über `S-read` wahrnehmen und das Ergebnis wie andere Werte verarbeiten oder in `Z` speichern. Sie kann `S` nicht schreiben.

Ein neuer Z-Eintrag kann `ΔS` erzeugen. Sein energetischer Wert sättigt sich unabhängig entlang zweier Achsen: Wiederholungen desselben Inhalts liefern zunehmend weniger Mehrenergie (**Inhaltssättigung**), und wiederholt aus derselben Quelle gewonnene neue Inhalte liefern ebenfalls zunehmend weniger Mehrenergie (**Quellensättigung**). Der Supervisor bewertet dabei keine semantische Bedeutung, Wahrheit oder Nützlichkeit der Quelle oder des Werts.

Begründung: Ein zufälliges `Z` wäre Erfahrung vor dem Leben und verwischt die Trennung von Vererbung und Erwerb. Ein völlig verborgenes `S` könnte keinen evolvierbaren energieabhängigen Handlungsdruck vermitteln. Die Quellensättigung entschärft semantisch unbekannte, endlos variierende Datenströme, ohne Sonderregeln etwa für Uhren einzubauen.

Mögliche Folgen: Die Minimalregel ist weiterhin nur eine operative Näherung an das Forschungsziel „Information ist keine Nahrung. Erkenntnis ist Nahrung.“ Sie definiert noch keine Wahrheit, Vorhersage, Bestätigung oder Reproduzierbarkeit. Die konkreten Sättigungsfunktionen, die Identität einer Quelle und das Neuheitsgedächtnis bleiben offen.

Herkunft: Konzeptarbeit vom 6. September 2026; Korrektur und Präzisierung am selben Tag.

## 2026-09-06: Anschlussfähigkeit für seltenes `A_ZG`

Gegenstand: Möglicher Pfad vom Lebensspeicher zum Genom.

Entscheidung: Der Pfad `Z -> G` wird konzeptionell und technisch von Anfang an vorgesehen, aber nicht als globale oder zwingend aktive Lernfunktion. Er kann nur über eine seltene genomische Disposition `A_ZG` wirksam werden. Diese muss in Population 0 nicht vorkommen und kann etwa durch Mutation entstehen.

Begründung: Genetische Assimilation soll evolutionär erreichbar sein, ohne erworbene Zustände automatisch zu vererben.

Mögliche Folgen: Die konkrete Übersetzung, Aktivierung, Kosten- und Sicherheitslogik bleibt offen und zunächst inaktiv.

Herkunft: Konzeptarbeit vom 6. September 2026.

## 2026-08-29: Entität, Genom, Zustand und Energie als Grundmodell

Gegenstand: Minimale begriffliche und funktionale Ausstattung einer Einheit in EVE.

Entscheidung: Der formale Begriff lautet **EVE-Entität**. Ihr derzeitiges Minimalmodell unterscheidet das vererbte Genom `G`, den während der Existenz erworbenen internen Zustand `Z` und die aktuelle Energie `S`. Die kontrollierte Außenschnittstelle gehört zur EVE-Umwelt, nicht zur Entität.

Das Genom ist eine variable Sammlung elementarer Parameter `P`. Ein `P` ist keine benannte komplexe Fähigkeit und kein vollständiger Handlungsbefehl. Seine Häufigkeit im Elternpool beeinflusst seine Vererbungschance. Die am 29. August noch angenommene allgemeine Ausprägung über den relativen Anteil ist seit der Konkretisierung von `P` als Netzkante prüfbedürftig; siehe Entscheidung vom 6. September. Rückgabewerte primitiver Verarbeitung können in `Z` gespeichert und später wiederverwendet werden.

Begründung: Das Modell trennt angeborene Disposition, individuelle Erfahrung und verfügbaren Energiehaushalt, ohne fertige Fähigkeiten wie Lernen, Neugier oder Kooperation einzubauen. Der neutrale Begriff Entität vermeidet unbelegte biologische oder agentische Zuschreibungen.

Mögliche Folgen (Stand 29. August): Die konkrete Form von `P`, die unterste Verarbeitungsregel und die Auswahl von Instruktionen blieben zunächst zentrale offene Architekturfragen. Seit dem 6. September ist `P` als Netzkante konkretisiert; Ausführungsregel, Codierung und primitiver Funktionssatz bleiben offen. Frühere Begriffe wie Organismus oder Agent müssen in historischen Dokumenten nicht rückwirkend ersetzt werden.

Herkunft: Gespräch „Privacy nachhaken“, 29. August 2026.

## 2026-08-29: Standbyverbrauch, genetische Aktivität und Hunger

Gegenstand: Energetischer Grundmechanismus einer EVE-Entität.

Entscheidung: Existenz wird in Heartbeats abgerechnet. Ein positiver vererbbarer Standbyverbrauch ist Ausdruck laufender Existenz; kann eine Entität den nächsten Heartbeat nicht bezahlen, endet sie. Ein Standbywert von `0` entspricht dem Tod und darf als lebensunfähige Mutation auftreten.

Der Standbyverbrauch soll zugleich die Intensität begrenzen, mit der das Genom pro Heartbeat wirksam werden kann. Diese Aktivität steht im Verhältnis zur Genomgröße. Die konkrete mathematische Funktion ist nicht entschieden.

Hunger wird als interner Bedarf an Energie und damit als elementarer Handlungsdruck aufgenommen. Hunger schreibt weder eine Handlung noch die Suche nach Erkenntnis vor.

Begründung: Genomgröße erhält dadurch einen evolutionären Trade-off statt einer pauschalen Strafe. Hunger liefert der einzelnen Entität ein energetisches „Warum“, während das „Wie“ aus Genom, erworbenem Zustand und Evolution hervorgehen muss.

Mögliche Folgen: Sparsame langsame, energiehungrige aktive und große, theoretisch vielseitige, aber nur langsam wirksame Genome werden gleichermaßen möglich. Die Bewertung muss durch die Umwelt erfolgen.

Herkunft: Gespräch „Privacy nachhaken“, 29. August 2026.

## 2026-08-29: Supervisor und Evolution strikt trennen

Gegenstand: Rolle des Supervisors und Sicherheitsgrenze des Experiments.

Entscheidung: Der Supervisor liegt außerhalb der Evolution. Er startet Population 0, beobachtet, protokolliert und kann das Experiment aus Sicherheitsgründen beenden. Er wählt keine Partner, löst keine Reproduktion aus und bestimmt keine vererbten Inhalte. Eine geschützte Komponente darf ein von Entitäten hervorgebrachtes gültiges Reproduktionsereignis technisch ausführen.

Evolution erhält keinen Zugriff auf die Mechanismen, die ihre VM-, Berechtigungs- und Sicherheitsgrenzen setzen. Die Versuchs-VM wird ab Prototyp 0 als potenziell kompromittierbar behandelt.

Begründung: Selbstverändernde und replizierende Prozesse besitzen sicherheitsrelevante Eigenschaften. Zugleich wäre eine vom Supervisor ausgelöste Vermehrung keine aus den Entitäten hervorgegangene Reproduktion.

Mögliche Folgen: Reproduktion und Sicherheit benötigen getrennte technische Mechanismen. Die genaue minimale Schnittstelle bleibt offen.

Herkunft: Gespräch „Privacy nachhaken“, 29. August 2026.

## 2026-08-29: Redaktioneller Grundsatz des Projektlogs

Gegenstand: Welche Geschichte das Projektlog bewahren soll.

Entscheidung: Das Log dokumentiert nicht nur technische Änderungen und Ergebnisse, sondern auch die Entwicklung unserer Fragen, Motivation und Deutungen. Dazu gehören ausdrücklich Hypothesen, Spekulationen, Irrwege, Fehlannahmen, gescheiterte Versuche, Anekdoten und Humor.

Dabei werden Spekulation, Hypothese, Beobachtung und Interpretation klar gekennzeichnet und nicht nachträglich miteinander vermischt. Persönliche und humorvolle Notizen dürfen neben der sachlichen Analyse stehen.

Begründung: Das Projekt soll unabhängig von Erfolg oder Scheitern nachvollziehbar bleiben. Spätere Leser sollen erkennen können, welche Gedanken vor einem Experiment bestanden und welche erst aus Ergebnissen entstanden.

Leitsatz:

> Maximale Ambition bei den Fragen. Minimale Erwartung an das Ergebnis.

Mögliche Folgen: Auch ein früher Fehlschlag von Prototyp 0 ist ein dokumentierbares Ergebnis. Eine korrekte Analyse darf im Log gelegentlich von einem ehrlichen „Tja.“ begleitet werden.

Herkunft: Gespräch „Sinn des Lebens in EVE“, 29. August 2026.

## 2026-08-28: Projektname EVE

Status: Am 20. September 2026 als alleinige Projektbezeichnung durch **EVE-Alife** abgelöst. Die Entscheidung bleibt als Entstehungsgeschichte erhalten.

Gegenstand: Kurzbezeichnung des Projekts.

Entscheidung: Der Projektname lautet **EVE**, die Langform **Emergent Virtual Evolution**. „Das KI-Biotop“ bleibt als beschreibender Arbeitstitel erhalten.

Begründung: Der Name ist kurz und eignet sich für Verzeichnisse, Dokumentation und visuelle Identität. Inhaltlich verweist er auf den emergenten und evolutionären Ansatz, ohne ein bestimmtes Ergebnis vorwegzunehmen.

Mögliche Folgen: Ein Logo und eine konsistente visuelle Kennzeichnung können später auf dieser Namensform aufbauen.

Herkunft: Gespräch „Biotop Eimer eingesammelt“, 28. August 2026.

## 2026-08-28: Linux-Basis und Datenträgeraufteilung

Gegenstand: Technische Basis des EVE-Rechners.

Entscheidung: EVE verwendet Bazzite auf der 2-TB-NVMe als Betriebssystembasis. Die mechanische 2-TB-Toshiba wird als ext4-Datenlaufwerk mit dem Label `eve-data` unter `/var/mnt/eve-data` eingebunden.

Begründung: Bazzite stellte NVIDIA-, Vulkan-, Steam- und Secure-Boot-Unterstützung in der geprüften Konfiguration ohne größere Reibung bereit. Die getrennte Datenplatte bietet einen einfachen Ort für Modelle, Archive, Backups und spätere EVE-Ausgaben.

Mögliche Folgen: Projektdateien und Versuchsdaten benötigen noch ein bewusstes Backup- und Recovery-Konzept. Das Atomic-System erleichtert die Wiederherstellung des Betriebssystems, ersetzt aber kein Backup der eigenen Daten.

Herkunft: Gespräch „EVE Bestandsaufnahme“, 28. August 2026.

## 2026-08-19: Reale Rechnerumwelt statt vollständig erfundener Welt

Gegenstand: Grundlegende Umwelt des KI-Biotops.

Entscheidung: Die unmittelbare Welt der Organismen soll ein realer Linux-Rechner sein. Dateien, Prozesse, Zeit, Speicher, Geräte, Berechtigungen und später möglicherweise Netzwerkschnittstellen sind Eigenschaften dieser Umwelt, werden den Organismen aber nicht semantisch erklärt. Eine minimale digitale Zellmembran vermittelt kontrollierte Umweltkontakte.

Begründung: Das Experiment soll möglichst wenig vorgeben, welche Strukturen entdeckt und wie sie genutzt werden. Reale Systemgrenzen können selbst zu entdeckbaren Naturgesetzen werden.

Mögliche Folgen: Sicherheit, Reproduzierbarkeit und die schrittweise Erweiterung erreichbarer Systemflächen müssen Teil jeder Prototypstufe sein. „Unbekannt“ und „technisch unerreichbar“ dürfen nicht verwechselt werden.

Statusabgleich 6. September 2026: Als langfristiger Rahmen bestätigt, für die erste erreichbare Umweltfläche jedoch durch die RAM-Suppe eingeschränkt. Dateien, Prozesse und andere höherwertige OS-Strukturen sind zunächst technisch unerreichbar und erst für spätere Stufen vorgesehen.

Herkunft: Gespräch „KI Biotop Konzept“, 19. August 2026.

## 2026-08-19: Grundkonzept und Prototyp-Spezifikation trennen

Gegenstand: Struktur der Projektdokumentation.

Entscheidung: Das Grundkonzept beschreibt Naturgesetze, Ziele und Forschungsphilosophie. Eine Prototyp-Spezifikation beschreibt nur die vorläufige technische Umsetzung. Konkrete Werte wie Genomlänge, Registerzahl, Bytecodes oder Channel-Anzahl werden nicht zu Naturgesetzen erklärt.

Begründung: Frühe Implementierungskompromisse sollen die langfristige Fragestellung nicht unbemerkt verengen. Die Trennung erleichtert außerdem die Prüfung von Redundanzen und Widersprüchen.

Mögliche Folgen: Erkenntnisse aus Prototypen dürfen nur dann ins Grundkonzept zurückgeführt werden, wenn sie bewusst als grundsätzlich bewertet wurden.

Herkunft: Gespräch „KI Biotop Konzept“, 19. August 2026.
