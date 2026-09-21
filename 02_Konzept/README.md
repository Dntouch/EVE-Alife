# Konzeptstatus und Übernahmeprozess

Dieses Verzeichnis enthält den jeweils aktuellen, konsolidierten Konzeptstand von EVE-Alife. Es ist die Brücke zwischen dem freien Denken in Gesprächen und der späteren technischen Spezifikation eines Prototyps.

## Aktueller Stand

- **Fortlaufende Arbeitsdatei:** [Grundkonzept – Arbeitsentwurf](Grundkonzept_Arbeitsentwurf.md)
- **Aktuelle Konzeptversion:** 0.7
- **Letzte abgeschlossene historische Fassung:** `00_Archiv/Grundkonzept_v0.3.1.txt`
- **Historische Prototyp-Spezifikation:** `00_Archiv/Prototyp_v0_Konsolidierte_Spezifikation.txt`

Der Arbeitsentwurf ist noch keine freigegebene Spezifikation. Die Konzeptversion 0.7 ergänzt gegenüber dem zuvor in Git dokumentierten Stand die obligatorische Genomausführung, den erblichen Basisaktivitätswert `A₀`, seine Abhängigkeit von Genomgröße und verfügbarer Energie sowie `PAUSE` als primitiven Funktionspunkt.

Eine schrittweise Einführung ohne vorausgesetzte Informatik-, Genetik- oder
ALife-Kenntnisse bietet [Das EVE-Alife-Genom verstehen](Genom_verstehen.md).
Sie erklärt Funktionspunkte, Kanten, Datenfluss, Vererbung und Mutation am
implementierten P1-Stand und kennzeichnet Abweichungen zum Arbeitsentwurf.

Die Konzeptarbeit findet ausschließlich in dieser fortlaufenden Arbeitsdatei statt. Frühere Arbeitsstände werden nicht als parallele Dateien aufbewahrt, sondern über die Git-Historie und bei wichtigen Meilensteinen über Git-Tags nachvollzogen. Das Verzeichnis `00_Archiv` bleibt historischen Dokumenten vorbehalten, die bereits vor dieser Arbeitsweise bestanden oder einen eigenständigen Dokumentcharakter besitzen.

Die historische v0-Spezifikation ist derzeit **nicht implementierungsreif**. Insbesondere ihr festes 64-Byte-Genom, Instruction Pointer, Registermodell und vorgegebener Bytecode sind durch die jüngere Konzeptarbeit wieder zur Prüfung gestellt worden.

## Wie ein Gespräch ins Konzept gelangt

1. **Quelle bewahren:** Das Projektlog dokumentiert den tatsächlichen Gedankengang, einschließlich Einwänden, Richtungswechseln und verworfenen Modellen.
2. **Status trennen:** Phase 0 verteilt Ergebnisse auf Begriffe, Thesen, Entscheidungen und offene Fragen. Ein interessanter Gedanke wird nicht allein durch gute Formulierung zur Entscheidung.
3. **Konzeptabgleich:** Neue Entscheidungen werden gegen den aktuellen Arbeitsentwurf und ältere Fassungen geprüft. Dabei werden Bestätigung, Ergänzung, Widerspruch und Ablösung ausdrücklich benannt.
4. **Konsolidieren:** Nur tragfähige Grundsätze werden in das Grundkonzept übernommen. Formeln, Bytegrößen, Opcodes und Sicherheitslimits gehören in eine Prototyp-Spezifikation, sofern sie keine Naturgesetze von EVE-Alife sein sollen.
5. **Versionieren und freigeben:** Bewusste Meilensteine erhalten eine Konzeptversionsnummer und einen Git-Tag. Die Arbeitsdatei wird fortlaufend weitergeführt; alte Arbeitskopien werden nicht parallel abgelegt. Wenn das Konzept gemeinsam als ausreichend konsistent bewertet wird, kann sein Status ohne Dateiduplikat auf freigegeben gesetzt werden.

## Kennzeichnungen im Arbeitsentwurf

- **gesetzt:** gegenwärtig bewusste konzeptionelle Entscheidung
- **Arbeitshypothese:** plausibler, später prüfbarer Zusammenhang
- **offen:** Mechanismus oder Entscheidung ist ungelöst
- **prototypspezifisch:** darf für einen Versuch festgelegt werden, ohne zum Naturgesetz zu werden
- **abgelöst:** ältere Festlegung wird im aktuellen Stand nicht mehr vorausgesetzt

## Gegenwärtige Konzeptverschiebungen gegenüber v0.3.1

| Bereich | Historischer Stand | Aktueller Arbeitsstand |
|---|---|---|
| Grundeinheit | Organismus/Agent | neutral: EVE-Entität |
| Ausführung | kleine Bytecode-Runtime als naheliegendes Modell | Netz aus vererbbaren gerichteten Datenflusskanten; Taktsemantik offen |
| Genom | mutierbare genetische Information; v0 fest 64 Byte | konkrete Funktionspunkt-Instanzen, verbindende `P`-Kanten und Metadaten; Codierung offen |
| Individualität | Genom, Register, Runtime-Wissensspeicher | `G` angeboren, `K` kurzfristiger Signalzustand, `Z` dauerhaft erworben, `S` Energie |
| Aktivität | Instruktionszyklus | Zusammenhang von Standby, Genomgröße und Aktivität gesetzt; Mathematik offen |
| Handlungsdruck | Energieverbrauch und Selektion | zusätzlich Hunger als interner Energiebedarf |
| Reproduktion | Runtime verarbeitet Bedingungen | Impuls und Inhalt aus Entitäten; geschützte Technik führt nur aus |
| Sicherheit | Sandbox und Limits | Evolution darf ihre Sicherheitsgrenze grundsätzlich nicht kontrollieren |
| erste Umweltfläche | Dateien, Prozesse und weitere Linux-Strukturen prinzipiell erreichbar | zunächst nur supervisor-reservierte RAM-Suppe; OS-Flächen später |
| Energiegewinn | neue, überprüfte Erkenntnis | zunächst syntaktisch neuer Z-Eintrag mit Inhalts- und Quellensättigung; Erkenntnisökonomie als spätere Zielrichtung |

Diese Tabelle ersetzt keine Begründung. Die Herleitung steht in den Projektlog-Einträgen „Vom Prozess zum Hunger“ und „Von der Frage ‚Was ist P?‘ zur RAM-Suppe und zum Datenflussnetz“ sowie in den Phase-0-Dokumenten.
