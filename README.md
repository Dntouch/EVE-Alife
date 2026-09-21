# EVE-Alife

**EVE-Alife** steht für *Emergent Virtual Evolution* und ist ein experimentelles Artificial-Life-Projekt – intern auch Schlammeimer™ oder KI-Biotop genannt.

Untersucht wird, was aus sehr einfachen digitalen Entitäten entstehen kann, wenn Genom, Energie, Umweltkontakt, Vererbung und Selektion möglichst wenig fertiges Verhalten vorgeben. Beobachtung, Interpretation und Designentscheidung werden dabei ausdrücklich getrennt.

> Isolation ist eine Eigenschaft der Umgebung, keine Verhaltensregel ihrer Bewohner.

## Aktueller Prototyp

Der aktive Entwicklungsstand ist [Prototyp v0.2](04_Prototypen/v0.2/README.md). Er startet vom konservierten P1-Endstand und ergänzt:

- begrenzte und offene Runs mit eindeutigem Status und Endgrund;
- skalierbare SQLite-Datenhaltung, Checkpoints und portable Run-Archive;
- eine read-only Lupe mit Chronik, Zeitfilter, Lebensfilm und Genomdiagramm;
- Genom- und Abstammungshistorie;
- experimentelle erbliche Partnersuche und genomischen Rückzug;
- einen ausdrücklich vorläufigen, reduzierten Genomkostentarif.

Der jüngste dokumentierte Versuch ist [v0.2/Lauf 4](07_Laufergebnisse/v0.2/Lauf_004.md): 500 Ticks, 27 lebende Amöben und sieben Nachkommen, davon keiner ohne `MEM_WRITE`. Das ist ein einzelnes Versuchsergebnis und keine allgemeine Aussage über das Modell.

Der erste ausführbare Stand [v0.1](04_Prototypen/v0.1/README.md) und die Ergebnisse von P0/P1 bleiben als abgeschlossene historische Prototypstände erhalten; die genaue Grenze steht in der [Konservierungsnotiz](04_Prototypen/KONSERVIERUNG_P0_P1.md).

## Neues aus dem Schlammeimer

| Prototyp | Dokumentierte Läufe | Massenaussterben | Nachkommen | Gewonnene RAM-Energie |
| :--- | ---: | ---: | ---: | ---: |
| [v0.2](07_Laufergebnisse/v0.2/README.md) | 4 | **0** | 13 | 181.340 |
| [v0.1](07_Laufergebnisse/v0.1/README.md) | 41 | **17** | 2.478 | 14.070.529,67 |

Als Massenaussterben zählt ein Lauf, an dessen Ende keine Amöbe mehr lebt. Die Zahlen werden nicht versionsübergreifend zu einer scheinbar einheitlichen Versuchsreihe verrechnet – aber selbstverständlich vergessen wir kein einziges ordentlich dokumentiertes Aussterben. :-)

## Schnellstart

Voraussetzung ist Python 3. Es werden keine externen Python-Pakete benötigt.

```bash
cd 04_Prototypen/v0.2
python3 run.py --ticks 500
python3 lupe.py runs/DEINE-RUN-ID
```

Die Lupe ist danach standardmäßig unter `http://127.0.0.1:8080/` erreichbar. Ein Testlauf des Codes:

```bash
cd 04_Prototypen/v0.2
python3 -m unittest -v
```

Run-Rohdaten können groß werden und bleiben deshalb lokal unter `04_Prototypen/<Version>/runs/`. Dauerhaft versioniert werden Code, Spezifikationen und kompakte Laufberichte.

## Orientierung

| Einstieg | Inhalt |
| :--- | :--- |
| [Das Genom verstehen](02_Konzept/Genom_verstehen.md) | Einführung in `G`, Funktionspunkte, Kanten, Datenfluss, Vererbung und Mutation |
| [v0.2-Spezifikation](04_Prototypen/v0.2/SPEZIFIKATION.md) | ausführbare Regeln und Abgrenzung zum Fachkonzept |
| [v0.2-Architektur](04_Prototypen/v0.2/ARCHITEKTUR.md) | Run-Lebenszyklus, Datenmodell, Skalierung und Beobachtung |
| [Laufergebnisse](07_Laufergebnisse/README.md) | nach Prototypversion getrennte Versuchsberichte |
| [Projektlog](05_Projektlog/README.md) | chronologische Entstehung einschließlich Irrwegen und Entscheidungen |
| [Blog](06_Blog/README.md) | lesbare Gesprächserzählungen und Lab Notes; derzeit interne Entwürfe |

## Versionen

| Stand | Status | Schwerpunkt |
| :--- | :--- | :--- |
| `v0.2` | aktiv und experimentell | langfristige Runs, neue Datenhaltung und Lupe sowie klar markierte Modellversuche |
| `v0.1` | konserviert | ausführbarer gemeinsamer P0/P1-Stand und historische Läufe 1–41 |
| P0/P1 | abgeschlossen | technische Machbarkeit und erste genomische Exploration |

Laufnummern gelten innerhalb einer Version. Deshalb sind beispielsweise `v0.1/Lauf 4` und `v0.2/Lauf 4` unterschiedliche Versuche; die jeweilige Run-ID ist die technisch eindeutige Identität.

## Repository

- `00_Archiv`: unveränderte historische Ausgangsdokumente
- `01_Phase_0`: Bestandsaufnahme, Begriffe, Thesen, Fragen und Entscheidungen
- `02_Konzept`: aktueller Konzeptstand und Übernahmeregeln
- `03_Experimente`: Gedankenversuche und Untersuchungen einzelner Thesen
- `04_Prototypen`: konkrete technische Umsetzungen und Spezifikationen
- `05_Projektlog`: chronologische Entstehungsgeschichte
- `06_Blog`: redaktionelle Gesprächserzählungen und Lab Notes
- `07_Laufergebnisse`: nach Prototypversion getrennte Ergebnisberichte

## Arbeitsgrundsatz

> Das Archiv bewahrt, Phase 0 denkt, das Konzept verdichtet, Experimente prüfen und Prototypen verkörpern.

Das Projektlog trennt Spekulation, Hypothese, Beobachtung und Interpretation. Dokumente im Archiv werden nicht redaktionell verändert. Neue Gedanken werden erst nach bewusster Prüfung in das Konzept übernommen.
