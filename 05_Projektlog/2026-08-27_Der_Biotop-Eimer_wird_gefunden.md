# Der Biotop-Eimer wird gefunden

Datum: 27. August 2026

Primärquelle: gemeinsamer Chat „PC für lokale KI geeignet“

Quell-ID: `6a8ff6e2-f678-83eb-8a8b-d662238507ad`

Ergänzende Gespräche:

- „RTX Vergleich 3060 3070 3080“ – `6a907f11-d67c-83eb-86b8-e8604b0f9c10`
- „VR Mods unter Linux“ – `6a9141d7-0054-83ed-b0ba-5641c0eb7a8a`
- „Lexar NM710 Einschätzung“ – `6a916104-c0ec-83eb-ad2e-2ac0970f6348`
- „GPU Upgrade Empfehlung“ – `6a9178de-e064-83eb-a5ad-1c9ffb802657`

## Vom kleinen Mint-Rechner zum eigenen Habitat

Am Ende des Ursprungsgesprächs war für das KI-Biotop noch ein kleiner vorhandener Linux-Mint-Rechner vorgesehen. Eine Woche später erschien auf Kleinanzeigen ein gebrauchter Gaming-PC, der ursprünglich vor allem als lokaler KI-Rechner und Steam-Maschine geprüft wurde.

Die Anzeige versprach:

- AMD Ryzen 7 5700X
- NVIDIA GeForce RTX 3060 mit 12 GB VRAM
- 64 GB DDR4
- MSI B450M PRO-VDH MAX
- 2 TB SSD und 2 TB HDD
- 27-Zoll-Monitor mit 100 Hz
- Maus und Tastatur

Der Angebotspreis betrug zunächst 850 Euro.

## Der historische RAM-Zwischenfall

Die erste Preiseinschätzung fiel zu skeptisch aus. Nova bewertete 64 GB DDR4 zunächst nach einem deutlich älteren Preisgefühl und hielt 850 Euro für überzogen. Stefan wies zurecht auf die aktuellen DDR4-Preise hin.

Nach tatsächlicher Prüfung musste die Einschätzung korrigiert werden. Die Bestückung mit zwei 32-GB-Modulen und die stark gestiegenen damaligen DDR4-Preise machten das Gesamtpaket erheblich interessanter.

Das Projektlog hält deshalb nicht nur das Ergebnis fest, sondern auch den Irrtum:

> Nova bewertet 64 GB DDR4 nach historischen Preisen.

Punkt an Stefan. Nova hatte gepennt.

## Warum die Maschine zu EVE passte

Für den ersten primitiven Prototyp war der Rechner deutlich überdimensioniert. Gerade das machte ihn als langfristige Projektbasis attraktiv:

- Die 8 Kerne und 16 Threads des 5700X erlauben viele parallele primitive Agenten.
- 64 GB RAM schaffen Spielraum für Populationen, Messdaten und spätere lokale Modelle.
- Die RTX 3060 ist für v0 nicht erforderlich, bietet mit 12 GB VRAM aber CUDA- und Auswertungsspielraum.
- 2 TB NVMe und 2 TB HDD trennen schnelles System von großen Daten, Archiven und Backups.
- Der Rechner kann neben EVE auch als Linux-Gaming-, PCVR- und lokaler KI-Spielplatz dienen.

Damit musste das Projekt nicht von Anfang an um knappe Hardware herum entworfen werden. Falls später CPU, RAM oder GPU begrenzen, lässt sich wenigstens beobachten, warum eine Aufrüstung nötig wird.

## Windows muss weg

Die Frage nach einem SteamOS-artigen System führte zu Bazzite. Das offizielle SteamOS war für die NVIDIA-Karte nicht die bevorzugte Wahl; Bazzite bot dagegen eine passende NVIDIA-Variante, Steam-Integration und eine Atomic-Systembasis.

Eine zwischenzeitlich vorgeschlagene Dual-Boot-Lösung für bequemeres Quest-3-PCVR wurde von Stefan unmissverständlich beendet:

> Ne, nix. Windows muss weg.

Bazzite wurde damit zum geplanten Betriebssystem. Wireless-PCVR über WiVRn, normales Steam-Gaming und lokale KI waren willkommene Nebenrollen. EVE blieb der zunehmend wichtigere Langzeitgrund für die Maschine.

## Kaufentscheidung

Der Preis wurde auf 800 Euro inklusive Monitor, Maus und Tastatur geeinigt. Vor der endgültigen Übergabe sollte der Rechner mindestens einmal booten und die wesentliche Hardware unter Windows verifiziert werden. Netzteil, Temperaturen, SSD-Zustand und ungewöhnliche Geräusche blieben Prüfpunkte.

Die Anzeige und Fotos lieferten vorab weitere Hinweise:

- zwei 32-GB-TeamGroup-DDR4-3200-Module
- RTX 3060 LHR mit 12 GB; die Mining-Drossel war für CUDA und Inferenz unerheblich
- Lexar-NVMe, später als NM710 identifiziert
- BIOS-Version aus dem Jahr 2023, passend zum Ryzen 7 5700X

## Der Plan für den nächsten Tag

Für den 28. August um 18 Uhr wurde die Abholung vereinbart. Der Schreibtisch sollte umgebaut, das vorhandene Ultrawide aufgestellt und der mitgelieferte Monitor dem Sohn zur Verfügung gestellt werden.

Aus einem abstrakten Evolutionsgedanken war damit eine Einkaufsliste, aus der Einkaufsliste ein Kleinanzeigenangebot und aus dem Angebot ein reservierter Rechner geworden.

Der digitale Urschlamm hatte noch keinen einzigen Zyklus erlebt. Aber sein Eimer war gefunden.
