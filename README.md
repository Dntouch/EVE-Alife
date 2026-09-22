# EVE-Alife

**EVE-Alife** steht für *Emergent Virtual Evolution* und ist ein experimentelles Artificial-Life-Projekt – intern auch Schlammeimer™ oder KI-Biotop genannt.

Untersucht wird, was aus sehr einfachen digitalen Entitäten entstehen kann, wenn Genom, Energie, Umweltkontakt, Vererbung und Selektion möglichst wenig fertiges Verhalten vorgeben. Beobachtung, Interpretation und Designentscheidung werden dabei ausdrücklich getrennt.

> Isolation ist eine Eigenschaft der Umgebung, keine Verhaltensregel ihrer Bewohner.

## Aktueller Prototyp

Der aktive Entwicklungsstand ist [Prototyp v0.3](04_Prototypen/v0.3/README.md). Er basiert auf dem konservierten v0.2-Fachstand und ergänzt:

- eine EVE-Analyseoberfläche mit Leitstand, Historie, Chronik, Stammbaum und Genom;
- lineares zoombares RAM-Band, Evolutionsverlauf und Beobachtungs-Replay;
- eine evolutionäre Zeitlandschaft mit Verwandtschaftslinse und Vergleich;
- einen zoombaren Genom-Arbeitsraum mit Beziehungsfokus;
- ein versionsübergreifendes Run-Archiv samt Hall of Life;
- einen getrennten Supervisor für Presets, offene Runs und kontrollierten Stopp.

Der vollständige Fachstand von v0.2 einschließlich Genom, Energie, Umwelt,
Partnersuche und gemeinsamer Elternfinanzierung bleibt dabei erhalten. Das
Run-Datenformat bleibt kompatibel bei Version 2; v0.2 selbst wird nicht verändert.

Der jüngste abgeschlossene Versuch ist [v0.2/Lauf 16](07_Laufergebnisse/v0.2/Lauf_016.md): Die gemeinsame Elternfinanzierung trug 75 Nachkommen bis Generation 8, erzeugte aber noch keine stabile Kultur. Bei Tick 5.000 lebte allein Ada 4 mit mehr als 101.000 Energie und einem kleinen, nicht fortpflanzungsfähigen Genom weiter. Die Untersuchung ist im [Experiment Generationenwechsel](04_Prototypen/v0.2/EXPERIMENT_GENERATIONENWECHSEL.md) zusammengefasst.

Der erste ausführbare Stand [v0.1](04_Prototypen/v0.1/README.md) und die Ergebnisse von P0/P1 bleiben als abgeschlossene historische Prototypstände erhalten; die genaue Grenze steht in der [Konservierungsnotiz](04_Prototypen/KONSERVIERUNG_P0_P1.md).

## Neues aus dem Schlammeimer

| Prototyp | Dokumentierte Läufe | Massenaussterben | Nachkommen | Gewonnene RAM-Energie |
| :--- | ---: | ---: | ---: | ---: |
| [v0.2](07_Laufergebnisse/v0.2/README.md) | 16 | **5** | 536 | 6.603.400,00 |
| [v0.1](07_Laufergebnisse/v0.1/README.md) | 41 | **17** | 2.478 | 14.070.529,67 |

Als Massenaussterben zählt ein Lauf, an dessen Ende keine Amöbe mehr lebt. Die Zahlen werden nicht versionsübergreifend zu einer scheinbar einheitlichen Versuchsreihe verrechnet – aber selbstverständlich vergessen wir kein einziges ordentlich dokumentiertes Aussterben. :-)

## Schnellstart

Voraussetzung ist Python 3. Es werden keine externen Python-Pakete benötigt.

```bash
cd 04_Prototypen/v0.3
python3 run.py --ticks 500
python3 supervisor.py
python3 lupe.py runs/DEINE-RUN-ID --port 8766
```

Die Lupe ist danach unter `http://127.0.0.1:8766/` erreichbar. Ein Testlauf des Codes:

```bash
cd 04_Prototypen/v0.3
python3 -m unittest -v
```

Run-Rohdaten können groß werden und bleiben deshalb lokal unter `04_Prototypen/<Version>/runs/`. Dauerhaft versioniert werden Code, Spezifikationen und kompakte Laufberichte.

## Orientierung

| Einstieg | Inhalt |
| :--- | :--- |
| [Das Genom verstehen](02_Konzept/Genom_verstehen.md) | Einführung in `G`, Funktionspunkte, Kanten, Datenfluss, Vererbung und Mutation |
| [v0.3-Lupe](04_Prototypen/v0.3/LUPE.md) | Arbeitsbereiche, Fokusmodus, Bedienung und Beobachtungsgrenze |
| [v0.3-Spezifikation](04_Prototypen/v0.3/SPEZIFIKATION.md) | ausführbare Regeln und Abgrenzung zum Fachkonzept |
| [v0.3-Architektur](04_Prototypen/v0.3/ARCHITEKTUR.md) | Run-Lebenszyklus, Datenmodell, Skalierung und Beobachtung |
| [Laufergebnisse](07_Laufergebnisse/README.md) | nach Prototypversion getrennte Versuchsberichte |
| [Projektlog](05_Projektlog/README.md) | chronologische Entstehung einschließlich Irrwegen und Entscheidungen |
| [Blog](06_Blog/README.md) | lesbare Gesprächserzählungen und Lab Notes; derzeit interne Entwürfe |

## Versionen

| Stand | Status | Schwerpunkt |
| :--- | :--- | :--- |
| `v0.3` | aktiv und experimentell | EVE-Analysearbeitsplatz, Supervisor, Stammbaum, Genom und Chronik |
| `v0.2` | konserviert | langfristige Runs, Datenhaltung und klar markierte Modellversuche |
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
