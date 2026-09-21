# v0.2 – Lauf 4

## Identität

| Feld | Wert |
| :--- | :--- |
| Run-ID | `05084eec-b02a-4423-94cf-63fc460d68ab` |
| Erzeugt | 2026-09-21T12:23:14.239510+00:00 |
| EVE-Version | 0.2 |
| Einordnung | erster regulärer Lauf mit reduziertem Genomkostentarif |

## Ergebnis

| Ticks | Entitäten gesamt | Am Ende lebend | Nachkommen | davon ohne `MEM_WRITE` | RAM-Energie |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 500 | 27 | 27 | 7 | 0 | 90.825 |

- RAM-Leseereignisse: 3.422, davon 1.894 in der normalen RAM-Suppe
- 273 verschiedene normale RAM-Leseadressen
- RAM-Schreibvorgänge: 1.501 auf 24 Adressen im Bereich 1–26
- Genomkostentarif: `0,05/0,01`
- Recovery-Checkpoints: 5

Der reduzierte Tarif beseitigte in diesem Lauf den unmittelbaren Fortpflanzungsengpass. Die Konzentration der Schreibzugriffe auf den ID-nahen Bereich blieb davon unabhängig bestehen und ist als Eigenschaft des Startgenoms weiter zu untersuchen.
