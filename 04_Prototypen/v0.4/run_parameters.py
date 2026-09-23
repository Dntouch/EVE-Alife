"""Zentrales Parameterschema und unveränderliche Startpresets für v0.4."""

PARAMETERS = {
    "label": {"label": "Bezeichnung", "type": "text", "default": "", "description": "Frei gewählter Anzeigename. Die unveränderliche Run-ID wird zusätzlich automatisch erzeugt."},
    "mode": {"label": "Laufmodus", "type": "choice", "default": "limited", "choices": ["limited", "open"], "description": "Begrenzt endet am Ticklimit. Offen läuft bis zur Extinktion oder einem kontrollierten Stoppsignal des Supervisors."},
    "ticks": {"label": "Ticklimit", "type": "int", "default": 2000, "min": 1, "max": 100000000, "description": "Maximale Zahl der Heartbeats eines begrenzten Runs. Bei offenen Runs wird dieser Wert nicht verwendet."},
    "seed": {"label": "Seed", "type": "int", "default": 42, "min": 0, "max": 2147483647, "description": "Startwert aller reproduzierbaren Zufallsquellen. Gleiche Konfiguration und gleicher Seed erzeugen denselben Verlauf."},
    "population": {"label": "Startpopulation", "type": "int", "default": 20, "min": 2, "max": 10000, "step": 2, "description": "Gerade Zahl der Gründeramöben. Größere Populationen erhöhen Rechenlast und Begegnungsmöglichkeiten."},
    "start_energy": {"label": "Startenergie", "type": "float", "default": 500, "min": 0.01, "max": 1000000000, "description": "Energie S jeder Gründeramöbe zu Beginn."},
    "birth_energy": {"label": "Basis-Geburtsenergie", "type": "float", "default": 50, "min": 0.01, "max": 1000000000, "description": "Fallback-Energie eines Kindes. Bei aktivem relativen Anteil wird die konkrete Geburtsenergie aus der Elternenergie berechnet."},
    "birth_energy_fraction": {"label": "Relativer Geburtsanteil", "type": "float", "default": 0.5, "min": 0.0001, "max": 1, "step": 0.01, "description": "Anteil der mittleren aktuellen Elternenergie für das Kind. Die gemeinsame Finanzierung darf kein Elternteil unter sein S₀ senken."},
    "birth_min_heartbeats": {"label": "Mindest-Heartbeats", "type": "int", "default": 5, "min": 0, "max": 1000000, "description": "Zusätzliche Untergrenze: Das Kind muss bei der Geburt mindestens diese Zahl eigener Heartbeats finanzieren können."},
    "novelty_base": {"label": "Neuheitsenergie", "type": "float", "default": 60, "min": 0, "max": 1000000000, "description": "Basisertrag für eine neue externe RAM-Veränderung. Größere Werte machen Umwelterkundung energetisch attraktiver."},
    "aging_cost_rate": {"label": "Altersrate", "type": "float", "default": 0.01, "min": 0, "max": 1000000, "step": 0.001, "description": "Zusätzliche Standby-Kosten pro bereits gelebtem Heartbeat. Null deaktiviert die altersabhängige Mehrbelastung."},
    "genome_node_cost": {"label": "Funktionspunktkosten", "type": "float", "default": 0.05, "min": 0, "max": 1000000, "step": 0.01, "description": "Faktor der unterlinear wachsenden laufenden Kosten für Genom-Funktionspunkte."},
    "genome_edge_cost": {"label": "Kantenkosten", "type": "float", "default": 0.01, "min": 0, "max": 1000000, "step": 0.01, "description": "Faktor der unterlinear wachsenden laufenden Kosten für Genom-Verbindungen."},
    "entity_discovery_base": {"label": "Amöbenfund-Energie", "type": "float", "default": 10, "min": 0, "max": 1000000000, "description": "Energie für den neuen Fund einer lebenden fremden Amöbe."},
    "invitation_discovery_base": {"label": "Einladungsenergie", "type": "float", "default": 20, "min": 0, "max": 1000000000, "description": "Energie für eine neu erkannte Einladung in einem fremden Partnerslot."},
    "life_state_discovery_base": {"label": "Lebenszustandsenergie", "type": "float", "default": 10, "min": 0, "max": 1000000000, "description": "Energie für einen neu erkannten fremden Lebenszustand."},
    "ram_world": {"label": "RAM-Welt", "type": "choice", "default": "toys", "choices": ["random", "islands", "toys"], "description": "Toys erzeugt 128 verteilte Habitate und echte lokale Amöbenpositionen. Random und Islands sind historische Modi mit absoluter Adressierung; ihre Gründer erscheinen räumlich gemeinsam bei RAM 0."},
    "population_model": {"label": "Populationsmodell", "type": "choice", "default": "p1", "choices": ["p1", "demo", "technical-explorer"], "description": "P1 ist die wissenschaftliche Ausgangspopulation. Demo und Technical Explorer sind technische Prüfkulturen."},
    "uniform_p1": {"label": "Uniforme P1-Gründer", "type": "bool", "default": False, "description": "Verwendet identische P1-Gründergenome statt seedabhängiger Suchparameter. Dient als Kontrollfall."},
    "sample_every": {"label": "Messintervall", "type": "int", "default": 10, "min": 1, "max": 1000000, "description": "Abstand dauerhaft gespeicherter Beobachtungspunkte in Ticks. Kleiner ist flüssiger im Replay, benötigt aber mehr Speicher. Diskrete Ereignisse bleiben unabhängig davon erhalten."},
    "checkpoint_every": {"label": "Checkpointintervall", "type": "int", "default": 10000, "min": 0, "max": 100000000, "description": "Abstand vollständiger Recovery-Checkpoints. Null deaktiviert regelmäßige Checkpoints; kontrolliertes Stoppen erzeugt trotzdem einen Abschlusscheckpoint."},
}

BASE_RUN16 = {
    "label": "v0.2 Lauf 16 – Wiederholung", "mode": "limited", "ticks": 5000,
    "seed": 42, "population": 50, "start_energy": 500, "birth_energy": 50,
    "birth_energy_fraction": 0.5, "birth_min_heartbeats": 5, "novelty_base": 60,
    "aging_cost_rate": 0.01, "genome_node_cost": 0.05, "genome_edge_cost": 0.01,
    "entity_discovery_base": 10, "invitation_discovery_base": 20,
    "life_state_discovery_base": 10, "ram_world": "toys", "population_model": "p1",
    "uniform_p1": False, "sample_every": 10, "checkpoint_every": 10000,
}

PRESETS = {
    "v04-standard": {"label": "v0.4 Standard", "description": "Räumlicher Referenzlauf mit 128 Spielzeughabitaten und über den RAM verteilten Gründeramöben.", "values": {**{key: spec["default"] for key, spec in PARAMETERS.items()}, "label": "v0.4 Standard", "ram_world": "toys"}},
    "v02-run16": {"label": "v0.2 Lauf 16", "description": "Unveränderliche Referenzkonfiguration des letzten dokumentierten v0.2-Laufs.", "values": BASE_RUN16},
    "short-200": {"label": "Kurzer 200-Tick-Test", "description": "Lauf-16-Konfiguration für schnelle Oberflächen- und Datenprüfungen.", "values": {**BASE_RUN16, "label": "200-Tick-Test", "ticks": 200, "checkpoint_every": 0}},
    "open-observation": {"label": "Offener Beobachtungslauf", "description": "Lauf-16-Konfiguration ohne Ticklimit; endet durch Extinktion oder kontrollierten Stopp.", "values": {**BASE_RUN16, "label": "Offener Beobachtungslauf", "mode": "open"}},
    "uniform-control": {"label": "Uniformer Kontrolllauf", "description": "P1-Kontrollfall mit identischen Gründerparametern.", "values": {**BASE_RUN16, "label": "Uniformer Kontrolllauf", "uniform_p1": True, "ticks": 2000}},
}
