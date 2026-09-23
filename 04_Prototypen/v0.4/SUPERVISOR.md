# Lokaler Supervisor v0.4

Die Lupe bleibt read-only. Start-, Stopp- und Fortsetzungsaufträge gehen direkt
vom lokalen Browser an den getrennten Supervisor auf `127.0.0.1:8767`.

```bash
python3 supervisor.py
python3 lupe.py runs/DEINE-RUN-ID --port 8766
```

Der Supervisor akzeptiert ausschließlich strukturierte, anhand von
`run_parameters.py` validierte Werte. Er verwendet keine Shell und akzeptiert
weder freie Kommandozeilen noch frei wählbare Ausgabepfade.

## Kontrollierter Stopp

Ein Stoppsignal wird als `SIGTERM` an den von diesem Supervisor gestarteten
Prozess gegeben. `run.py` beendet den aktuellen konsistenten Simulationsschritt,
schreibt Beobachtung und Abschlusscheckpoint und finalisiert den Run mit
`status = stopped` und `end_reason = user_requested`.

## Fortsetzung

Ein gestoppter Run wird niemals wieder geöffnet. Die Fortsetzung verwendet den
letzten Checkpoint, erzeugt eine neue Run-ID und hält `resumed_from` sowie
`resumed_from_run` im Manifest fest.

## Presets und Parameter

Eingebaute Referenzpresets sind unveränderlich. Eigene Presets werden getrennt
in `user_presets.json` gespeichert. Beschriftung, Typ, Wertebereich,
Standardwert und Tooltipbeschreibung stammen für Oberfläche und Validierung aus
dem zentralen Parameterschema `run_parameters.py`.
