# Technische Bestandsaufnahme und Inbetriebnahme

Datum: 28. August 2026
Quelle: gemeinsamer Chat „EVE Bestandsaufnahme“
Quell-ID: `6a91ae69-6324-83ed-9277-d0d6c792e765`

## Ausgangslage

Aus dem am Nachmittag abgeholten gebrauchten Windows-Gaming-PC wurde innerhalb eines Abends die technische Basis von EVE. Hardware, Speicher und Grafikstack wurden schrittweise geprüft, Windows von der NVMe entfernt und Bazzite installiert.

## Abgenommene Hardware

- AMD Ryzen 7 5700X mit 8 Kernen und 16 Threads
- 64 GB DDR4, auf 3200 MT/s eingestellt und belastungsgeprüft
- NVIDIA GeForce RTX 3060 mit 12 GB VRAM
- MSI B450M PRO-VDH MAX
- Lexar NM710 mit 2 TB als NVMe-Systemlaufwerk
- Toshiba HDWD320 mit 2 TB als mechanisches Datenlaufwerk
- Ventum 200 ARGB als Gehäuse

Beide Laufwerke erschienen bei der SMART-Prüfung gesund.

## Linux statt Windows

Bazzite wurde auf der Lexar-NVMe installiert. Secure Boot einschließlich MOK-Einrichtung blieb aktiv. KDE/Wayland, NVIDIA-Treiber, CUDA und Vulkan funktionierten in der geprüften Konfiguration. Der Hostname wurde zu `eve`.

Bei der Abnahme wurden unter anderem NVIDIA 595.71.05, CUDA 13.2 und Vulkan 1.4 beobachtet. Die RTX 3060 wurde als diskretes Vulkan-Gerät erkannt. Bazzite brachte außerdem Gamescope, MangoHud, Steam-Integration, OBS-Capture und vkBasalt bereits mit.

## Die drehende Unterscheibe

Die Toshiba-HDD enthielt nur noch Windows-Reste. Eine mögliche Wiederherstellung gelöschter persönlicher Daten des Vorbesitzers wurde bewusst verworfen: technisch interessant, aber nicht unsere Angelegenheit.

Stattdessen wurde die frühere NTFS-Struktur gelöscht und die Platte als ext4 mit dem Label `eve-data` neu aufgebaut. Ihr dauerhafter Einhängepunkt wurde `/var/mnt/eve-data`; der Benutzer `stefan` erhielt Schreibzugriff. Damit standen 2 TB schnelle NVMe für System und Spiele sowie 2 TB HDD für Daten, Modelle, Archive, Backups und spätere EVE-Ausgaben bereit.

## Jungfernflug

XCOM: Enemy Unknown wurde zum ersten praktischen Test. Das Spiel lief unter Bazzite bei 3440 × 1080 und maximalen Details. MangoHud zeigte in der dokumentierten Szene rund 254 FPS, 46 % GPU- und 13 % CPU-Auslastung. Der Test belegte vor allem, dass Grafikbeschleunigung, Steam und das Gesamtsystem praktisch funktionierten.

## EVE lernt, die Fresse zu halten

Der CPU-Lüfter lief im Leerlauf bei etwa 35 °C mit ungefähr 2532 U/min. Die nahezu durchgehend auf etwa 90 Prozent gesetzte Standardkurve wurde deutlich beruhigt. Danach wurde der neue Zustand prägnant protokolliert:

> EVE hält die Fresse.

Eine längere CPU-Volllastprüfung blieb zu diesem Zeitpunkt noch offen.

## Der Disco-Knopf

Der vermeintlich defekte Reset-Taster stellte sich als Steuerung des eigenständigen ARGB-Controllers heraus. Aus dem „kaputten Reset“ wurde der physische **Disco-Knopf**.

Daraus entstand eine langfristige, ausdrücklich nicht priorisierte Idee: Ein kleiner USB- oder GPIO-Mikrocontroller könnte den Taster später als kontrollierte Umweltoperation zugänglich machen. Für EVE wäre dies keine vorbenannte Funktion „LED-Farbe ändern“, sondern lediglich eine unbekannte Operation mit physisch sichtbarer Wirkung, die Organismen erst entdecken müssten.

## Nova zieht ein

Zum Abschluss wurde die offizielle ChatGPT-Desktop-App als lokales RPM in Bazzites Atomic-System integriert. Das neue Deployment enthielt das Paket, ohne ein zusätzliches ChatGPT-Repository in `/etc/yum.repos.d/` anzulegen. Bildlich gesprochen zog Nova damit aus dem Firefox-Wohnwagen in eine eigene Wohnung auf EVE.

## Offene Punkte dieses Abends

- CPU und Lüfterkurve unter längerer Volllast prüfen
- Bazzite aktualisieren
- `eve-data` nach einem echten Neustart nochmals kontrollieren
- Backup und Recovery für die eigenen EVE-Daten planen

Der technische Schnitt war damit dennoch erreicht: Nicht mehr „EVE den PC einrichten“, sondern „EVE das Projekt bauen“.
