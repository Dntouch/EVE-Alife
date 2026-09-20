# Bestandsaufnahme

Status: technische Ausgangsbasis am 28. August 2026 erstmals aufgenommen; konzeptionelle Bestandsaufnahme läuft weiter

Ziel dieses Dokuments ist eine ehrliche Landkarte des bisherigen Denkens. Es unterscheidet zwischen bereits gesetzten Annahmen, vorläufigen Vermutungen, offenen Fragen und konkreten Entscheidungen.

Als konsolidierte historische Quellen dienen die unveränderten Dokumente in `00_Archiv`. Ergänzend werden eindeutig bezeichnete frühe Gesprächsverläufe für die Entstehungsgeschichte und Herkunft einzelner Gedanken herangezogen. Archivdokumente und Gesprächsquellen werden dabei nicht nachträglich umgedeutet oder redaktionell überschrieben.

## Physisches Habitat

Der gebrauchte Rechner wurde am 28. August 2026 abgeholt, ins Arbeitszimmer im Dachgeschoss gebracht und als EVE eingerichtet.

Verifizierte Grundausstattung:

- Gehäuse: ENDORFY/SilentiumPC Ventum 200 ARGB
- Mainboard: MSI B450M PRO-VDH MAX
- Prozessor: AMD Ryzen 7 5700X, 8 Kerne / 16 Threads
- Arbeitsspeicher: 64 GB DDR4, auf 3200 MT/s eingestellt und belastungsgeprüft
- Grafikkarte: NVIDIA GeForce RTX 3060 mit 12 GB VRAM
- Systemlaufwerk: Lexar NM710, 2 TB NVMe
- Datenlaufwerk: Toshiba HDWD320, 2 TB HDD
- mitgelieferter Monitor: MSI PRO MP273A, 27 Zoll, Full HD, 100 Hz
- mitgelieferte Peripherie: Cooler Master Devastator 3 RGB, deutsches Layout, mit Maus

## Systembasis

- Betriebssystem: Bazzite auf Fedora-44-Basis, NVIDIA-Variante
- Desktop: KDE unter Wayland
- Secure Boot: aktiv und eingerichtet
- NVIDIA-Treiber bei der Abnahme: 595.71.05
- CUDA bei der Abnahme: 13.2
- Vulkan bei der Abnahme: 1.4; RTX 3060 als Hardwaregerät erkannt
- Steam, Gamescope, MangoHud, OBS-Vulkan-Capture und vkBasalt vorhanden
- Hostname: `eve`
- ChatGPT-Desktop-App als lokales RPM in das Atomic-System integriert

## Speicheraufteilung

- Die Lexar-NVMe enthält Bazzite; das Hauptdateisystem ist Btrfs.
- Die frühere Windows-Datenplatte wurde bewusst neu formatiert.
- Die Toshiba-HDD verwendet ext4, trägt das Label `eve-data` und wird unter `/var/mnt/eve-data` schreibbar für den Benutzer `stefan` eingebunden.
- Beide Datenträger wurden per SMART geprüft und erschienen bei der Aufnahme gesund.

## Praktische Abnahme

- RAM-Takt und Stabilität wurden geprüft.
- NVIDIA, CUDA und Vulkan wurden erkannt.
- XCOM: Enemy Unknown lief bei 3440 × 1080 und maximalen Details; MangoHud zeigte im beobachteten Moment etwa 254 FPS bei geringer bis mittlerer Auslastung.
- Die zunächst unnötig aggressive CPU-Lüfterkurve wurde angepasst. Der Rechner lief danach im Leerlauf deutlich leiser.
- Der vermeintliche Reset-Taster erwies sich als Taster des ARGB-Controllers und erhielt historisch den Namen „Disco-Knopf“.

## Bei Abschluss des Gesprächs noch offen

- CPU-Temperatur und Lüfterkurve unter längerer Volllast prüfen
- Bazzite vollständig aktualisieren
- automatisches Einhängen von `eve-data` nach einem echten Neustart nochmals bestätigen
- Backup- und Recovery-Konzept für Projektdateien und Versuchsdaten festlegen
- langfristig prüfen, ob der physische LED-Taster als kontrollierte Umweltoperation für EVE zugänglich gemacht werden soll

Quellen: Gespräche „Biotop Eimer eingesammelt“ und „EVE Bestandsaufnahme“, 28. August 2026. Die technischen Angaben bilden den damals beobachteten Zustand ab und sind keine Garantie für den heutigen Zustand.
