# 20. September 2026: Von der Partnersuche zum beobachtbaren Biotop

## Ausgangslage

Das erste P1-Genom konnte RAM erkunden, schrieb Partner-IDs aber noch aus einer berechneten Nachbarschaft. Das war technisch dynamischer als eine fest verdrahtete ID, blieb inhaltlich jedoch eine versteckte Zwangspaarung. Gleichzeitig zeigte die Lupe Zustände und Lebensfilme, aber noch keinen frei wählbaren zeitlichen Ausschnitt des gesamten Biotops.

## Partner müssen gefunden werden

Die berechnete Paarbildung wurde durch ein genomisches Such-und-Handshake-Fragment ersetzt. Eine Amöbe durchläuft den virtuellen Membranraum und darf eine fremde ID nur dann in ihren Partnerslot schreiben, wenn ihr Signal tatsächlich aus der gelesenen ID-Zelle einer lebenden fremden Amöbe stammt. Erkennt sie die eigene ID im Partnerslot einer gefundenen Amöbe, kann sie diese Einladung erwidern.

Beide Informationsereignisse sind energetisch relevant:

- das erstmalige beziehungsweise veränderte Finden einer lebenden Amöbe,
- das Erkennen einer neuen Einladung an die eigene ID.

Zusätzlich schreibt ein getrenntes Genomfragment die eigene ID neutral in die RAM-Suppe. Das Schreiben erzeugt für die schreibende Amöbe keine Energie. Andere Amöben können den veränderten Wert nach der bestehenden Herkunftsregel entdecken und daraus Energie gewinnen.

Zusammenhängende Netzkomponenten werden bei der Rekombination nun atomar behandelt. Eine vererbbare Funktionseinheit wird nicht länger mitten im Netzfragment abgeschnitten.

## Der Preis der Komplexität

Das neue P1-Startgenom umfasst 40 Funktionspunkte und 60 Kanten. Unter der bisherigen linearen Abrechnung kostete seine Ausführung ungefähr 47 Energie je Heartbeat. Bei einem Neuheitstarif von 60 funktionierten Suche und Handshake, sämtliche Geburten scheiterten aber korrekt an der Bedingung, dass Eltern nach ihrem Beitrag über ihrer eigenen Geburtsenergie bleiben müssen.

Ein Kontrolllauf mit Tarif 160 erzeugte neun Kinder und bestätigte die vollständige Kausalkette. Er zeigte zugleich, dass nicht die Reproduktionsmechanik defekt war, sondern das Verhältnis aus Genomkosten und Umweltvergütung.

Die Lebenshaltung wurde deshalb auf ein unterlineares Modell umgestellt:

```text
1 + Alter × 0,01 + 0,5 × √N_f + 0,1 × √N_p
```

Die Genomgröße bleibt ein Selektionsfaktor, verdoppelt ihre Kosten bei einer Verdoppelung aber nicht mehr automatisch.

Der anschließende 1.000-Tick-Lauf mit dem unveränderten Tarif 60 ergab 49 Amöben insgesamt, 29 Nachkommen, 38 Überlebende und erstmals Generation 4. Beobachtet wurden außerdem 1.460 Amöbenfunde, 64 erkannte Einladungen und 9.845 RAM-Schreibvorgänge. Damit war die lineare Besteuerung komplexer Genome als wesentliche Ursache der vorherigen wirtschaftlichen Sackgasse isoliert.

Maßgebliche Run-ID: `157811c6-aee4-4418-8cb8-6eef05fd6c5a` (Lauf 36).

## Die Lupe wird zum Untersuchungsinstrument

Der Populationsgraph dient nun zugleich als Zeitfilter:

- Klick wählt einen gespeicherten Tick,
- Ziehen wählt einen Zeitraum,
- die Gesamtansicht hebt den Filter auf.

Auswahlbilanz, verständliche Ereignisse, Umweltkontakte und Amöbenkarten folgen demselben Ausschnitt. Für Zeiträume zeigt die Lupe alle Amöben, deren Leben den Bereich berührt, mit ihrem Zustand am Ende der Auswahl. Die Chronik erhielt zusätzlich genealogische und verhaltensbezogene Rekorde, darunter gesamte Nachkommenschaft, Amöbenfunde, erkannte Einladungen und RAM-Schreibvorgänge.

## Einordnung

- **Beobachtung:** Echte Membranfunde können genomisch zu Einladung, Erwiderung und Geburt führen.
- **Beobachtung:** Tarif 60 trägt unter unterlinearen Genomkosten eine Population über 1.000 Ticks und vier Generationen.
- **Designentscheidung:** Suchfragment, Belohnungssätze und Kostenformel wurden von uns gesetzt.
- **Offene Frage:** Die gegenwärtige lineare Suche im Membranraum bevorzugt frühe IDs und kann soziale Zentren erzeugen.
- **Keine Beobachtung:** Freie Partnerwahl im menschlichen Sinn, Absicht, Sympathie oder entwickelte Kommunikation.

Der Prototyp ist damit nicht nur komplexer geworden. Er ist erstmals so beobachtbar, dass zeitliche Ursachenketten im gesamten Biotop untersucht werden können, ohne den Lauf zu verändern.
