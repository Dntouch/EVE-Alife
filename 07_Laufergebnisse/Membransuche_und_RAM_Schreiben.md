# Membransuche, Einladung und RAM-Schreiben

## Ziel

Die mathematisch festgelegte Nachbarpaarung wurde verworfen. Eine Amöbe soll einen möglichen Partner tatsächlich in der Umwelt finden, dessen ID mit Fundherkunft behalten, eine Einladung schreiben und eine an sie gerichtete Einladung erkennen können. Zusätzlich erhält der Genpool erstmals ein neutrales `RAM_WRITE`-Fragment.

## Verbindliche Regeln

- Nur die gelesene ID einer lebenden fremden Membran darf in einen Partnerslot geschrieben werden.
- Konstante, berechnete, eigene oder zu einer toten Entität gehörende IDs werden abgewiesen.
- Ein belegter Slot verlangt weiterhin eine exakte Zweiergruppe; zwei Slots verlangen eine exakte Dreiergruppe.
- Ein neuer fremder Entitätsfund liefert 10 Energie.
- Eine neu erkannte Einladung an die eigene ID liefert 20 Energie.
- Unveränderte Wiederholungen liefern nichts.
- Schreiben in RAM oder Partnerslot erzeugt keine unmittelbare Energie.
- Zusammenhängende Netzkomponenten werden als unteilbare Fragmente vererbt.

## Läufe

| Lauf | Tarif | Ergebnis |
| ---: | ---: | :--- |
| [33](Lauf_033_f5a9e883.md) | 60 | 708 RAM-Writes und 9 Einladungen, aber flüchtige Vorschläge; keine Kinder, ausgestorben |
| [34](Lauf_034_c0390378.md) | 60 | stabile Vorschläge und 114 Geburtsprüfungen; alle an fehlendem Überschuss gescheitert |
| [35](Lauf_035_760442a6.md) | 160 | 9 Kinder, 27 von 29 Amöben lebend bei Tick 300 |

## Funktionsnachweis aus Lauf 35

- 424 neue fremde Amöbenfunde
- 20 erkannte Einladungen
- 58 erfolgreiche Partnerslot-Schreibvorgänge
- 2.546 RAM-Schreibvorgänge
- 218.080 Energie aus allen beobachteten Informationsquellen
- Tom als erster erfolgreicher Informationsproduzent: 4.160 Energie für andere Amöben

Damit sind Finden, Einladen, Erkennen, Erwiderung, Geburt und fremdnützige RAM-Information technisch nachgewiesen. Tarif 160 ist dabei ein Kontrolltarif, noch kein neues Verhandlungsergebnis. Das neue Genom ist mit 100 Bestandteilen erheblich teurer als die frühere P1-Variante; der angemessene Tarif muss deshalb neu vermessen werden.
