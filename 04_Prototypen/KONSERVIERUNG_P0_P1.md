# Konservierung von P0 und P1

Stand: 21. September 2026

P0 und P1 sind mit Beginn des Prototyps `v0.2` abgeschlossene historische Erkenntnisstände. Ihre fachlichen Dokumente `P0_ERGEBNISSE.md` und `P1_GENOMENTWURF.md`, der ausführbare Stand `v0.1`, dessen Spezifikation sowie die vorhandenen Laufberichte bleiben unverändert erhalten. Neue Laufverwaltung, Datenhaltung und Lupe werden ausschließlich unter `04_Prototypen/v0.2` entwickelt.

Die Versionsgrenze lautet:

- `v0.1`: gemeinsamer historischer ausführbarer Stand von P0/P1, JSON/JSONL-Runs und erste Lupe;
- `v0.2`: neuer Prototyp für offene Runs, explizite Endgründe, skalierbare Run-Daten und gemeinsame Live-/Archiv-Lupe.

Alte `v0.1`-Runverzeichnisse werden nicht automatisch migriert oder als Format 2 interpretiert. Die historische `v0.1`-Lupe bleibt ihr Leser. Ein späterer Importer muss die alte Semantik ausdrücklich als Quellformat 1 behandeln.

Die anfängliche Kopie des Fachkerns in `v0.2/eve_core.py` änderte gegenüber `v0.1` zunächst nur technische und beobachtende Aspekte. Spätere, ausdrücklich freigegebene v0.2-Experimente betreffen unter anderem Rekombinationsauswahl, erbliche Partnersuchparameter, genomischen Rückzug und den Genomkostentarif. Diese Änderungen gelten ausschließlich für v0.2; der konservierte Code und die Berichte von P0/P1 und v0.1 bleiben unverändert.
