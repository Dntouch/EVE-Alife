# EVE-Alife – Laufergebnisse nach Prototypversion

Laufnummern gelten immer nur innerhalb einer Prototypversion. Ein Lauf wird durch das Paar aus Version und Nummer bezeichnet, zum Beispiel `v0.1/Lauf 41` oder `v0.2/Lauf 4`. Die Run-ID bleibt die technisch eindeutige Identität.

## Versionen

- [v0.4 – aktive Genomrevision](v0.4/README.md): homologe Genomplätze,
  evolvierbare Kantengewichte, der dokumentierte erste OOM-Abbruch und der
  anschließend vollständig erreichte 5.000-Tick-Populationsdurchbruch.
- [v0.3 – abgeschlossene Analyse- und Beobachtungsreihe](v0.3/README.md): reproduzierte 5.000-Tick-Standardläufe, 10.000-Tick-Lauf mit halbierter Altersrate und dokumentierte v0.3-Technikläufe.
- [v0.2 – konservierte Versuchsreihe](v0.2/README.md): SQLite-Format 2, variable genomische Partnersuche, grafische Live-Lupe, RAM-Habitate, gemeinsame Elternfinanzierung und Versuche mit reduziertem Genomkostentarif.
- [v0.1 – konservierte P0/P1-Läufe](v0.1/README.md): 41 historische Läufe sowie die damaligen Reihen-Auswertungen.

Die großen Rohdaten liegen jeweils beim zugehörigen Prototyp unter `04_Prototypen/<Version>/runs/` und werden nicht ungeprüft versioniert. Die Markdown-Berichte hier sind die kompakte, dauerhaft lesbare Ergebnisebene.

## Ablageregel

Neue Berichte werden ausschließlich unter der Version abgelegt, mit der der Run tatsächlich erzeugt wurde. Versionsübergreifende Vergleiche nennen beide vollständigen Laufbezeichnungen und dürfen Nummern nicht stillschweigend fortschreiben.
