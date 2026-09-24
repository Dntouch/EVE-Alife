"""Aus v0.2 übernommenes P1-Fachmodell im Prototyp EVE-Alife v0.4."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from math import ceil, floor, inf, sqrt
from random import Random
from typing import Any, Iterable


MASK64 = (1 << 64) - 1
SIGN64 = 1 << 63

# Namen sind Beobachtungsidentitaeten. Ihre Vergabe verbraucht bewusst keinen
# Zufall und kann daher das Verhalten eines Laufs nicht beeinflussen.
_CLASSIC_AMOEBA_NAMES = (
    "Tom", "Erna", "Ada", "Bruno", "Clara", "Dario", "Emmi", "Fritz",
    "Greta", "Hugo", "Ida", "Juri", "Karla", "Lino", "Maja", "Nils",
    "Olga", "Piet", "Rosa", "Sam", "Tilda", "Uwe", "Vera", "Willi",
    "Xenia", "Yara", "Zeno", "Alma", "Ben", "Cleo", "Dora", "Enno",
    "Stefan", "Nova", "Elena", "Sonja", "Milo", "EVE",
)
_EVE_NAME_PREFIXES = (
    "Ae", "Al", "An", "Ar", "Ca", "Ce", "Da", "El", "En",
    "Fa", "Io", "Ka", "Le", "Ma", "Na", "Or", "Sa", "Ve",
)
_EVE_NAME_SUFFIXES = (
    "bela", "ciel", "dra", "fen", "gis", "hra", "ian", "jara", "kel",
    "lian", "mera", "niel", "ora", "pris", "quen", "riel", "sia", "tor",
    "una", "vis", "wen", "xia", "yel", "zara", "din", "mon",
)
AMOEBA_NAMES = _CLASSIC_AMOEBA_NAMES + tuple(
    f"{prefix}{suffix}" for prefix in _EVE_NAME_PREFIXES for suffix in _EVE_NAME_SUFFIXES
)[:500 - len(_CLASSIC_AMOEBA_NAMES)]
assert len(AMOEBA_NAMES) == 500 and len(set(AMOEBA_NAMES)) == 500


def amoeba_name(entity_id: int, generation: int = 0) -> str:
    """Deterministischer Basisname mit biologischer Generation als Suffix."""
    base = AMOEBA_NAMES[(entity_id - 1) % len(AMOEBA_NAMES)]
    return base if generation == 0 else f"{base} {generation}"


def i64(value: int) -> int:
    value &= MASK64
    return value - (1 << 64) if value & SIGN64 else value


def provenance(*signals: "Signal") -> tuple[str, ...]:
    return tuple(sorted({source for signal in signals for source in signal.sources}))


def originators(*signals: "Signal") -> tuple[int, ...]:
    return tuple(sorted({origin for signal in signals for origin in signal.originators}))


@dataclass(frozen=True)
class Signal:
    value: int
    sources: tuple[str, ...]
    originators: tuple[int, ...] = ()


PORTS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "CONST": ((), ("value",)),
    "S_READ": ((), ("value",)),
    "Z_READ": (("address",), ("value",)),
    "Z_WRITE": (("address", "value"), ("value",)),
    "RAM_READ": (("address",), ("value",)),
    "RAM_WRITE": (("address", "value"), ("value",)),
    "MEM_READ": (("offset", "slot"), ("value",)),
    "MEM_WRITE": (("offset", "slot", "value"), ("value",)),
    "ADD": (("a", "b"), ("value",)),
    "SUB": (("a", "b"), ("value",)),
    "XOR": (("a", "b"), ("value",)),
    "EQ": (("a", "b"), ("value",)),
    "GATE": (("value", "condition"), ("value",)),
    "PAUSE": (("value",), ()),
}


@dataclass
class Node:
    id: int
    kind: str
    constant: int | None = None
    segment: int | None = None

    def __post_init__(self) -> None:
        if self.kind not in PORTS:
            raise ValueError(f"Unbekannter Funktionspunkttyp: {self.kind}")
        if self.kind == "CONST" and self.constant is None:
            raise ValueError("CONST benötigt einen erblichen Wert")


@dataclass(frozen=True)
class Edge:
    source: int
    source_port: str
    target: int
    target_port: str
    weight: int = 0


@dataclass
class Genome:
    nodes: list[Node]
    edges: list[Edge]
    activity_base: int
    knock_capacity: int = 1
    bond_ticks: int = 1

    def __post_init__(self) -> None:
        # Altformate besitzen noch keine Segmentangabe. Ein einzelner Punkt je
        # Segment ist die neutralste verlustfreie Migration: Es wird keine
        # funktionale Zusammengehörigkeit erfunden.
        for node in self.nodes:
            if node.segment is None:
                node.segment = node.id

    @property
    def n_p(self) -> int:
        return len(self.edges)

    @property
    def n_g(self) -> int:
        return len(self.nodes) + len(self.edges)

    def validate(self) -> None:
        by_id = {node.id: node for node in self.nodes}
        if len(by_id) != len(self.nodes):
            raise ValueError("Instanz-IDs müssen innerhalb eines Genoms eindeutig sein")
        if self.activity_base < 1:
            raise ValueError("A₀ muss mindestens 1 sein")
        if not 1 <= self.knock_capacity <= 16:
            raise ValueError("Nₖ muss zwischen 1 und 16 liegen")
        if self.bond_ticks < 1:
            raise ValueError("Tₚ muss mindestens 1 sein")
        if any(node.segment is None or node.segment < 1 for node in self.nodes):
            raise ValueError("Jeder Funktionspunkt benötigt ein positives Segment")
        for edge in self.edges:
            if edge.source not in by_id or edge.target not in by_id:
                raise ValueError("Kante referenziert eine fehlende Instanz")
            if edge.source_port not in PORTS[by_id[edge.source].kind][1]:
                raise ValueError("Ungültiger Ausgangsport")
            if edge.target_port not in PORTS[by_id[edge.target].kind][0]:
                raise ValueError("Ungültiger Eingangsport")


@dataclass
class Entity:
    id: int
    name: str
    genome: Genome
    energy: float
    start_energy: float
    born_at: int
    generation: int = 0
    ram_position: int = 0
    parents: tuple[int, ...] = ()
    k: dict[str, Signal] = field(default_factory=dict)
    z: list[Signal | None] = field(default_factory=list)
    partner_ids: list[int | None] = field(default_factory=lambda: [None, None])
    knocker_ids: list[int] = field(default_factory=list)
    value_history: dict[str, int] = field(default_factory=dict)
    source_history: dict[str, int] = field(default_factory=dict)
    ram_last_seen: dict[int, int] = field(default_factory=dict)
    ram_seen_count: dict[str, int] = field(default_factory=dict)
    alive: bool = True
    corpse_available: bool = False

    @staticmethod
    def key(node_id: int, port: str) -> str:
        return f"{node_id}:{port}"


@dataclass
class Config:
    seed: int = 1
    ram_size: int = 65_536
    z_size: int = 64
    birth_energy: float = 50.0
    birth_energy_fraction: float | None = None
    birth_min_heartbeats: int = 0
    genome_size_sigma: float = 2.0
    mutation_probability: float = 0.001
    standby_cost: float = 1.0
    aging_cost_rate: float = 0.01
    genome_node_cost: float = 0.05
    genome_edge_cost: float = 0.01
    execution_cost: float = 0.0
    edge_cost: float = 0.0
    novelty_base: float = 10.0
    entity_discovery_base: float = 10.0
    invitation_discovery_base: float = 20.0
    life_state_discovery_base: float = 10.0
    membrane_base: int = 1_000_000
    toy_stones: int = 0
    toy_bubbles: int = 0
    toy_switches: int = 0
    toy_habitats: int = 0
    local_ram_coordinates: bool = False
    birth_position_radius: int = 32


class Simulation:
    version = "0.4"

    def __init__(self, config: Config, ram: list[int] | None = None) -> None:
        self.config = config
        self.rng = Random(config.seed)
        self.tick = 0
        self.ram = ram if ram is not None else [self.rng.randint(-(1 << 15), (1 << 15) - 1) for _ in range(config.ram_size)]
        self.ram_originators: list[tuple[int, ...]] = [()] * config.ram_size
        if len(self.ram) != config.ram_size:
            raise ValueError("RAM-Größe stimmt nicht mit der Konfiguration überein")
        self.entities: dict[int, Entity] = {}
        self.next_entity_id = 1
        self.events: list[dict[str, Any]] = []
        self._last_genome_trace: dict[str, Any] | None = None
        self.group_stability: dict[tuple[int, ...], int] = {}
        self.environment_toys: dict[str, list[dict[str, Any]]] = {
            "stones": [], "bubbles": [], "switches": [],
        }
        self._initialize_environment_toys()

    def _toy_addresses(self, rng: Random, count: int, width: int, occupied: set[int]) -> list[int]:
        """Reproduzierbare Mischung aus gut erreichbaren und globalen Positionen."""
        starts: list[int] = []
        immediate_limit = max(width, min(self.config.ram_size, 128))
        near_limit = max(width, min(self.config.ram_size, 4096))
        for index in range(count):
            limit = (immediate_limit, near_limit, self.config.ram_size)[index % 3]
            for _ in range(self.config.ram_size):
                start = rng.randrange(max(1, limit - width + 1))
                cells = {(start + offset) % self.config.ram_size for offset in range(width)}
                if not cells & occupied:
                    occupied.update(cells)
                    starts.append(start)
                    break
            else:
                raise ValueError("RAM ist für die gewünschte Spielzeugdichte zu klein")
        return starts

    def _initialize_environment_toys(self) -> None:
        if not any((self.config.toy_stones, self.config.toy_bubbles, self.config.toy_switches, self.config.toy_habitats)):
            return
        rng = Random(self.config.seed ^ 0x70A5)
        if self.config.toy_habitats:
            self._initialize_toy_habitats(rng)
            return
        occupied: set[int] = set()
        for index, start in enumerate(self._toy_addresses(rng, self.config.toy_stones, 8, occupied)):
            values = [i64(0x53544F4E45 + index * 257 + offset) for offset in range(8)]
            for offset, value in enumerate(values):
                self.ram[start + offset] = value
            self.environment_toys["stones"].append({"start": start, "length": 8, "values": values})
        for index, address in enumerate(self._toy_addresses(rng, self.config.toy_bubbles, 1, occupied)):
            low = i64(rng.randint(-(1 << 15), (1 << 15) - 1))
            high = i64(low ^ (0xB00B + index * 17))
            period = rng.randint(17, 97)
            self.ram[address] = low
            self.environment_toys["bubbles"].append({
                "address": address, "period": period, "low": low, "high": high,
            })
        starts = self._toy_addresses(rng, self.config.toy_switches, 2, occupied)
        for index, trigger in enumerate(starts):
            output = trigger + 1
            self.ram[trigger] = i64(0x53574954 + index)
            self.ram[output] = i64(0x4F555450 + index)
            self.environment_toys["switches"].append({
                "trigger": trigger, "output": output, "salt": i64(0x51A7 + index * 131),
            })

    def _initialize_toy_habitats(self, rng: Random) -> None:
        """Seedvariierte Inseln in gleich großen Sektoren des RAM-Rings."""
        count = self.config.toy_habitats
        if count < 1 or self.config.ram_size < count * 32:
            raise ValueError("RAM ist für die gewünschte Zahl Spielzeuginseln zu klein")
        sector = self.config.ram_size / count
        for index in range(count):
            sector_start = floor(index * sector)
            sector_end = floor((index + 1) * sector)
            room = sector_end - sector_start
            base = sector_start + rng.randrange(max(1, room - 31))
            stone_start = base
            values = [i64(0x53544F4E45 + index * 257 + offset) for offset in range(8)]
            for offset, value in enumerate(values):
                self.ram[stone_start + offset] = value
            self.environment_toys["stones"].append({
                "start": stone_start, "length": 8, "values": values, "habitat": index,
            })
            for bubble_index, address in enumerate((base + 12, base + 20)):
                low = i64(rng.randint(-(1 << 15), (1 << 15) - 1))
                high = i64(low ^ (0xB00B + index * 17 + bubble_index))
                period = rng.randint(17, 97)
                self.ram[address] = low
                self.environment_toys["bubbles"].append({
                    "address": address, "period": period, "low": low, "high": high,
                    "habitat": index,
                })
            trigger, output = base + 24, base + 25
            self.ram[trigger] = i64(0x53574954 + index)
            self.ram[output] = i64(0x4F555450 + index)
            self.environment_toys["switches"].append({
                "trigger": trigger, "output": output,
                "salt": i64(0x51A7 + index * 131), "habitat": index,
            })

    def _advance_environment(self) -> None:
        for bubble in self.environment_toys["bubbles"]:
            if self.tick % bubble["period"]:
                continue
            address = bubble["address"]
            before = self.ram[address]
            after = bubble["high"] if before == bubble["low"] else bubble["low"]
            self.ram[address] = after
            self.ram_originators[address] = ()
            self.emit(
                "environment_change", toy_kind="bubble", address=address,
                value_before=before, value=after,
            )

    def emit(self, kind: str, **data: Any) -> None:
        self.events.append({"tick": self.tick, "kind": kind, **data})

    def add_entity(
        self, genome: Genome, energy: float, parents: tuple[int, ...] = (),
        ram_position: int | None = None,
    ) -> Entity:
        genome.validate()
        if ram_position is None:
            ram_position = self.rng.randrange(len(self.ram)) if self.config.local_ram_coordinates else 0
        generation = 0 if not parents else 1 + max(self.entities[parent].generation for parent in parents)
        entity = Entity(
            id=self.next_entity_id,
            name=amoeba_name(self.next_entity_id, generation),
            genome=genome,
            energy=energy,
            start_energy=energy,
            born_at=self.tick,
            generation=generation,
            ram_position=ram_position % len(self.ram),
            parents=parents,
            z=[None] * self.config.z_size,
        )
        self.next_entity_id += 1
        self.entities[entity.id] = entity
        self.emit(
            "birth", entity_id=entity.id, entity_name=entity.name,
            parents=list(parents), energy=energy, n_g=genome.n_g,
            ram_position=entity.ram_position,
        )
        return entity

    def heartbeat(self) -> None:
        self.tick += 1
        self._advance_environment()
        for entity_id in sorted(tuple(self.entities)):
            entity = self.entities[entity_id]
            if not entity.alive:
                continue
            age = self.tick - entity.born_at
            aging_cost = age * self.config.aging_cost_rate
            genome_cost = (
                self.config.genome_node_cost * sqrt(len(entity.genome.nodes))
                + self.config.genome_edge_cost * sqrt(len(entity.genome.edges))
            )
            standby_cost = self.config.standby_cost + aging_cost + genome_cost
            if entity.energy < standby_cost:
                self._kill(entity, "standby_unaffordable")
                continue
            energy_before = entity.energy
            entity.energy -= standby_cost
            self.emit(
                "standby", entity_id=entity.id, cost=standby_cost,
                base_cost=self.config.standby_cost, aging_cost=aging_cost,
                genome_cost=genome_cost, age=age,
                energy_before=energy_before, energy_after=entity.energy,
            )
            self._execute_entity(entity)
        self._reproduce()
        self.emit("heartbeat", population=sum(e.alive for e in self.entities.values()))

    def _ready(self, entity: Entity) -> list[Node]:
        ready: list[Node] = []
        for node in entity.genome.nodes:
            inputs = PORTS[node.kind][0]
            if not inputs or all(Entity.key(node.id, port) in entity.k for port in inputs):
                ready.append(node)
        return ready

    def _execute_entity(self, entity: Entity) -> None:
        n_p = max(1, entity.genome.n_p)
        budget = max(1, floor(entity.genome.activity_base / sqrt(n_p)))
        outgoing: dict[int, list[Edge]] = {}
        for edge in entity.genome.edges:
            outgoing.setdefault(edge.source, []).append(edge)
        for _ in range(budget):
            ready = self._ready(entity)
            affordable = [n for n in ready if entity.energy >= self.config.execution_cost + self.config.edge_cost * len(outgoing.get(n.id, []))]
            if not affordable:
                break
            node = self.rng.choice(affordable)
            edges = outgoing.get(node.id, [])
            inputs = {
                port: self._signal_state(entity.k[Entity.key(node.id, port)])
                for port in PORTS[node.kind][0]
            }
            energy_before = entity.energy
            cost = self.config.execution_cost + self.config.edge_cost * len(edges)
            entity.energy -= cost
            outputs = self._fire(entity, node)
            self.emit(
                "node_fire", entity_id=entity.id, node_id=node.id, node_kind=node.kind,
                inputs=inputs,
                outputs={port: self._signal_state(signal) for port, signal in outputs.items()},
                cost=cost, energy_before=energy_before, energy_after=entity.energy,
            )
            for edge in edges:
                signal = outputs.get(edge.source_port)
                if signal is not None:
                    transported = self._transport_signal(signal, edge.weight)
                    entity.k[Entity.key(edge.target, edge.target_port)] = transported
                    self.emit(
                        "signal", entity_id=entity.id, source=node.id,
                        target=edge.target, source_value=signal.value,
                        value=transported.value, edge_weight=edge.weight,
                    )

    @staticmethod
    def _transport_signal(signal: Signal, weight: int) -> Signal:
        """Wende den erblichen Kantengain deterministisch auf ein i64-Signal an.

        Gewicht 0 ist bitgenau neutral. Die ganzzahlige Division rundet wie die
        übrigen Maschinenoperationen gegen null; anschließend gilt weiterhin
        die bestehende vorzeichenbehaftete 64-Bit-Semantik.
        """
        numerator = signal.value * (100 + weight)
        value = abs(numerator) // 100
        if numerator < 0:
            value = -value
        return Signal(i64(value), signal.sources, signal.originators)

    def _take_inputs(self, entity: Entity, node: Node) -> dict[str, Signal]:
        result: dict[str, Signal] = {}
        for port in PORTS[node.kind][0]:
            result[port] = entity.k.pop(Entity.key(node.id, port))
        return result

    def _fire(self, entity: Entity, node: Node) -> dict[str, Signal]:
        inputs = self._take_inputs(entity, node)
        kind = node.kind
        if kind == "CONST":
            return {"value": Signal(i64(node.constant or 0), ("G",))}
        if kind == "S_READ":
            return {"value": Signal(i64(round(entity.energy)), ("S",))}
        if kind == "PAUSE":
            return {}
        if kind == "GATE":
            signal = inputs["value"]
            condition = inputs["condition"]
            opened = condition.value != 0
            self.emit(
                "gate", entity_id=entity.id, node_id=node.id, opened=opened,
                condition=condition.value, value=signal.value,
            )
            if not opened:
                return {}
            return {"value": Signal(
                signal.value, provenance(signal, condition),
                originators(signal, condition),
            )}
        if kind in {"ADD", "SUB", "XOR", "EQ"}:
            a, b = inputs["a"].value, inputs["b"].value
            value = {"ADD": a + b, "SUB": a - b, "XOR": a ^ b, "EQ": int(a == b)}[kind]
            return {"value": Signal(
                i64(value), provenance(inputs["a"], inputs["b"]),
                originators(inputs["a"], inputs["b"]),
            )}
        if kind == "RAM_READ":
            raw_address = inputs["address"].value
            if raw_address >= self.config.membrane_base:
                membrane = self._decode_membrane_address(raw_address)
                if membrane is None:
                    self.emit(
                        "ram_read", entity_id=entity.id, address=raw_address,
                        value=0, virtual=True, reward=0.0, discovery_type=None,
                    )
                    return {"value": Signal(0, (f"MEM_VOID[{raw_address}]",))}
                target, offset, slot = membrane
                value = self._mem_read(target, offset, slot)
                source = f"MEM[{target.id},{offset},{slot}]"
                previous = entity.value_history.get(source)
                changed = previous is None or previous != value
                reward = 0.0
                discovery_type = None
                alive_foreign = target.alive and target.id != entity.id
                if not target.alive and target.corpse_available and offset == 2 and slot == 0:
                    reward = max(0.0, target.energy)
                    target.energy = 0.0
                    target.corpse_available = False
                    entity.energy += reward
                    discovery_type = "corpse"
                    self.emit(
                        "corpse_scavenged", entity_id=entity.id, target_id=target.id,
                        corpse_id=target.id, corpse_name=target.name,
                        ram_position=target.ram_position, reward=reward,
                    )
                elif alive_foreign and offset == 0 and slot == 0 and changed:
                    discovery_type = "entity"
                    count_key = f"{source}:{value}"
                    count = entity.source_history.get(count_key, 0)
                    reward = self.config.entity_discovery_base / (1 + count)
                    entity.source_history[count_key] = count + 1
                elif alive_foreign and offset == 1 and value == entity.id and changed:
                    discovery_type = "invitation"
                    count_key = f"{source}:{value}"
                    count = entity.source_history.get(count_key, 0)
                    reward = self.config.invitation_discovery_base / (1 + count)
                    entity.source_history[count_key] = count + 1
                elif target.id != entity.id and offset == 2 and slot == 0 and changed:
                    discovery_type = "life_state"
                    count_key = f"{source}:{value}"
                    count = entity.source_history.get(count_key, 0)
                    reward = self.config.life_state_discovery_base / (1 + count)
                    entity.source_history[count_key] = count + 1
                entity.value_history[source] = value
                if discovery_type != "corpse":
                    entity.energy += reward
                self.emit(
                    "ram_read", entity_id=entity.id, address=raw_address, value=value,
                    virtual=True, target_id=target.id, membrane_offset=offset,
                    membrane_slot=slot, previous=previous, changed=changed,
                    discovery_type=discovery_type, reward=reward,
                )
                return {"value": Signal(value, (f"MEM[{target.id},{offset},{slot}]",))}
            address = (
                entity.ram_position + raw_address if self.config.local_ram_coordinates else raw_address
            ) % len(self.ram)
            value = self.ram[address]
            writers = self.ram_originators[address]
            previous = entity.ram_last_seen.get(address)
            changed = previous is None or previous != value
            self_origin = entity.id in writers
            reward = 0.0
            if changed and not self_origin:
                history_key = f"{address}:{value}"
                count = entity.ram_seen_count.get(history_key, 0)
                reward = self.config.novelty_base / (1 + count)
                entity.ram_seen_count[history_key] = count + 1
                entity.energy += reward
            entity.ram_last_seen[address] = value
            self.emit(
                "ram_read", entity_id=entity.id, address=address, value=value,
                address_offset=raw_address,
                virtual=False, previous=previous, changed=changed,
                self_origin=self_origin, originators=list(writers), reward=reward,
            )
            return {"value": Signal(value, (f"RAM[{address}]",), writers)}
        if kind == "RAM_WRITE":
            raw_address = inputs["address"].value
            signal = inputs["value"]
            if raw_address >= self.config.membrane_base:
                return {"value": signal}
            address = (
                entity.ram_position + raw_address if self.config.local_ram_coordinates else raw_address
            ) % len(self.ram)
            self.ram[address] = signal.value
            writers = tuple(sorted({*signal.originators, entity.id}))
            self.ram_originators[address] = writers
            self.emit(
                "ram_write", entity_id=entity.id, address=address, value=signal.value,
                address_offset=raw_address, originators=list(writers),
            )
            for switch in self.environment_toys["switches"]:
                if switch["trigger"] != address:
                    continue
                output = switch["output"]
                before = self.ram[output]
                after = i64(signal.value ^ switch["salt"] ^ before)
                self.ram[output] = after
                # Die Umweltreaktion bleibt kausal mit ihren Auslösern verbunden:
                # Der Schreiber kann sich damit nicht selbst ernähren.
                self.ram_originators[output] = writers
                self.emit(
                    "environment_change", toy_kind="switch", address=output,
                    trigger_address=address, triggered_by=entity.id,
                    value_before=before, value=after, originators=list(writers),
                )
            return {"value": signal}
        if kind == "Z_READ":
            address = inputs["address"].value % len(entity.z)
            stored = entity.z[address]
            return {"value": stored if stored is not None else Signal(0, (f"Z_EMPTY[{address}]",))}
        if kind == "Z_WRITE":
            address = inputs["address"].value % len(entity.z)
            signal = inputs["value"]
            if not signal.sources:
                raise RuntimeError("Wert ohne Provenienz")
            entity.z[address] = signal
            self.emit(
                "z_write", entity_id=entity.id, address=address, value=signal.value,
                sources=list(signal.sources), reward=0.0,
            )
            return {"value": signal}
        if kind == "MEM_READ":
            offset, slot = inputs["offset"].value, inputs["slot"].value
            value = self._mem_read(entity, offset, slot)
            source = f"KNOCK[{value}]" if offset == 3 and value else f"MEM[{offset},{slot}]"
            return {"value": Signal(value, (source,))}
        if kind == "MEM_WRITE":
            offset, slot, signal = inputs["offset"].value, inputs["slot"].value, inputs["value"]
            if offset == 1 and slot in (0, 1):
                current_partner = entity.partner_ids[slot]
                death_source = f"MEM[{current_partner},2,0]"
                observed_partner_death = (
                    signal.value == 0
                    and current_partner is not None
                    and death_source in signal.sources
                    and not self.entities[current_partner].alive
                )
                if observed_partner_death:
                    entity.partner_ids[slot] = None
                    self.emit(
                        "mem_write", entity_id=entity.id, offset=offset,
                        slot=slot, value=0, cleared_partner=current_partner,
                        discovered=True,
                    )
                    return {"value": signal}
                genomic_withdrawal = (
                    signal.value == 0
                    and current_partner is not None
                    and "G" in signal.sources
                )
                if genomic_withdrawal:
                    entity.partner_ids[slot] = None
                    self.emit(
                        "mem_write", entity_id=entity.id, offset=offset,
                        slot=slot, value=0, cleared_partner=current_partner,
                        discovered=True, reason="genome_withdrawal",
                    )
                    return {"value": signal}
                target = self.entities.get(signal.value)
                required_source = f"MEM[{signal.value},0,0]"
                knock_source = f"KNOCK[{signal.value}]"
                discovered = required_source in signal.sources or knock_source in signal.sources
                if target is not None and target.alive and target.id != entity.id and discovered:
                    entity.partner_ids[slot] = signal.value
                    self.emit(
                        "mem_write", entity_id=entity.id, offset=offset,
                        slot=slot, value=signal.value, discovered=True,
                    )
                    if entity.id not in target.knocker_ids:
                        target.knocker_ids.append(entity.id)
                        overwritten_knocker = None
                        if len(target.knocker_ids) > target.genome.knock_capacity:
                            overwritten_knocker = target.knocker_ids.pop(0)
                        self.emit(
                            "knock", entity_id=entity.id, target_id=target.id,
                            slot=slot, overwritten_knocker=overwritten_knocker,
                        )
                else:
                    self.emit(
                        "mem_write_rejected", entity_id=entity.id, offset=offset,
                        slot=slot, value=signal.value, discovered=discovered,
                        target_alive=bool(target and target.alive),
                    )
            return {"value": signal}
        raise AssertionError(kind)

    def _mem_read(self, entity: Entity, offset: int, slot: int) -> int:
        if offset == 0 and slot == 0:
            return entity.id
        if offset == 1 and slot in (0, 1):
            value = entity.partner_ids[slot]
            return 0 if value is None else value
        if offset == 2 and slot == 0:
            if not entity.alive:
                return 0
            threshold = self._reproductive_energy_threshold(entity)
            if entity.energy > threshold and self._has_operational_mem_write(entity.genome):
                return 10
            if threshold == inf:
                return 9
            return max(1, min(9, ceil(9 * max(0.0, entity.energy) / threshold)))
        if offset == 3 and slot >= 0:
            entity.knocker_ids[:] = [
                proposer_id for proposer_id in entity.knocker_ids
                if (proposer := self.entities.get(proposer_id)) is not None
                and proposer.alive and entity.id in proposer.partner_ids
            ][-entity.genome.knock_capacity:]
            return entity.knocker_ids[slot] if slot < len(entity.knocker_ids) else 0
        return 0

    @staticmethod
    def _has_operational_mem_write(genome: Genome) -> bool:
        """Mindestens ein MEM_WRITE besitzt Kanten fuer alle benoetigten Eingangsports."""
        incoming = {
            node.id: {edge.target_port for edge in genome.edges if edge.target == node.id}
            for node in genome.nodes if node.kind == "MEM_WRITE"
        }
        required = set(PORTS["MEM_WRITE"][0])
        return any(required <= ports for ports in incoming.values())

    def _reproductive_energy_threshold(self, entity: Entity) -> float:
        """Energetische 10 fuer ein symmetrisches Zweierpaar gleicher Staerke."""
        fraction = self.config.birth_energy_fraction
        minimum = self._minimum_birth_energy(entity.genome)
        if fraction is not None:
            surplus_threshold = entity.start_energy / (1 - fraction / 2)
            child_threshold = minimum / fraction if fraction else inf
            return max(surplus_threshold, child_threshold)
        if self.config.birth_energy < minimum:
            return inf
        return entity.start_energy + self.config.birth_energy / 2

    def _decode_membrane_address(self, address: int) -> tuple[Entity, int, int] | None:
        relative = address - self.config.membrane_base
        if relative < 0:
            return None
        entity_id, cell = divmod(relative, 4)
        entity = self.entities.get(entity_id + 1)
        if entity is None or (not entity.alive and not entity.corpse_available):
            return None
        if cell == 0:
            return entity, 0, 0
        if cell in (1, 2):
            return entity, 1, cell - 1
        return entity, 2, 0

    def _kill(self, entity: Entity, reason: str) -> None:
        entity.alive = False
        entity.corpse_available = True
        entity.k.clear()
        self.emit(
            "death", entity_id=entity.id, reason=reason,
            remaining_energy=max(0.0, entity.energy), ram_position=entity.ram_position,
        )

    def _valid_groups(self) -> list[tuple[int, ...]]:
        groups: set[tuple[int, ...]] = set()
        living = {e.id: e for e in self.entities.values() if e.alive}
        for entity in living.values():
            partners = {p for p in entity.partner_ids if p in living and p != entity.id}
            candidate = tuple(sorted({entity.id, *partners}))
            if len(candidate) not in (2, 3):
                continue
            expected = set(candidate)
            if all({p for p in living[eid].partner_ids if p in living and p != eid} == expected - {eid} for eid in candidate):
                groups.add(candidate)
        return sorted(groups)

    @staticmethod
    def _birth_contributions(parents: list[Entity], child_energy: float) -> list[float] | None:
        """Verteilt Geburtsenergie gleichmaessig, begrenzt durch den S0-Sockel."""
        available = [max(0.0, parent.energy - parent.start_energy) for parent in parents]
        if sum(available) + 1e-12 < child_energy:
            return None
        contributions = [0.0] * len(parents)
        active = set(range(len(parents)))
        remaining = child_energy
        while active:
            share = remaining / len(active)
            limited = [index for index in active if available[index] < share]
            if not limited:
                for index in active:
                    contributions[index] = share
                break
            for index in limited:
                contributions[index] = available[index]
                remaining -= available[index]
                active.remove(index)
        return contributions

    def _reproduce(self) -> None:
        valid_groups = self._valid_groups()
        valid_set = set(valid_groups)
        self.group_stability = {
            group: age for group, age in self.group_stability.items() if group in valid_set
        }
        for group in valid_groups:
            self.group_stability[group] = self.group_stability.get(group, 0) + 1
            parents = [self.entities[eid] for eid in group]
            required_bond_ticks = max(parent.genome.bond_ticks for parent in parents)
            if self.group_stability[group] < required_bond_ticks:
                continue
            if self.config.birth_energy_fraction is None:
                child_energy = self.config.birth_energy
            else:
                mean_parent_energy = sum(parent.energy for parent in parents) / len(parents)
                child_energy = self.config.birth_energy_fraction * mean_parent_energy
            genome = self._recombine(parents)
            minimum = self._minimum_birth_energy(genome)
            if child_energy < minimum:
                for parent in parents:
                    self.emit(
                        "birth_rejected", entity_id=parent.id, group=list(group),
                        offered_energy=child_energy, required_energy=minimum,
                        reason="minimum_heartbeats_unaffordable",
                    )
                continue
            contributions = self._birth_contributions(parents, child_energy)
            if contributions is None:
                for parent in parents:
                    self.emit(
                        "birth_rejected", entity_id=parent.id, group=list(group),
                        offered_energy=child_energy, required_energy=minimum,
                        pooled_surplus=sum(max(0.0, item.energy - item.start_energy) for item in parents),
                        energy=parent.energy,
                        start_energy=parent.start_energy,
                        reason="parent_surplus_required",
                    )
                continue
            for parent, contribution in zip(parents, contributions):
                energy_before = parent.energy
                parent.energy -= contribution
                parent.partner_ids[:] = [None, None]
                self.emit(
                    "reproduction_cost", entity_id=parent.id, child_id=self.next_entity_id,
                    cost=contribution, energy_before=energy_before, energy_after=parent.energy,
                )
            if self.config.local_ram_coordinates:
                anchor = self.rng.choice(parents)
                child_position = (
                    anchor.ram_position
                    + self.rng.randint(-self.config.birth_position_radius, self.config.birth_position_radius)
                ) % len(self.ram)
            else:
                child_position = 0
            child = self.add_entity(genome, child_energy, group, child_position)
            self.emit(
                "genome_created", entity_id=child.id, parents=list(group),
                trace=self._last_genome_trace,
            )
            self.group_stability.pop(group, None)

    def _minimum_birth_energy(self, genome: Genome) -> float:
        """Konservative Energie für konfigurierte volle Heartbeats ohne Belohnungen."""
        if self.config.birth_min_heartbeats <= 0:
            return 0.0
        budget = max(1, floor(genome.activity_base / sqrt(max(1, genome.n_p))))
        outgoing = Counter(edge.source for edge in genome.edges)
        maximum_edges = max(outgoing.values(), default=0)
        genome_cost = (
            self.config.genome_node_cost * sqrt(len(genome.nodes))
            + self.config.genome_edge_cost * sqrt(len(genome.edges))
        )
        fixed_cost = self.config.standby_cost + genome_cost
        execution_cost = budget * (
            self.config.execution_cost + self.config.edge_cost * maximum_edges
        )
        heartbeats = self.config.birth_min_heartbeats
        aging_cost = self.config.aging_cost_rate * heartbeats * (heartbeats + 1) / 2
        return heartbeats * (fixed_cost + execution_cost) + aging_cost

    @staticmethod
    def _slot_homology(left: Genome, left_slot: int, right: Genome, right_slot: int) -> float:
        """Strukturelle Homologie zweier Vererbungsplätze, ohne Nutzenwissen."""
        left_nodes = [node for node in left.nodes if node.segment == left_slot]
        right_nodes = [node for node in right.nodes if node.segment == right_slot]
        left_ids = {node.id for node in left_nodes}
        right_ids = {node.id for node in right_nodes}
        left_kinds = Counter(node.kind for node in left_nodes)
        right_kinds = Counter(node.kind for node in right_nodes)

        def multiset_similarity(a: Counter, b: Counter) -> float:
            total = max(sum(a.values()), sum(b.values()), 1)
            return sum((a & b).values()) / total

        left_by_id = {node.id: node.kind for node in left.nodes}
        right_by_id = {node.id: node.kind for node in right.nodes}
        left_edges = Counter(
            (left_by_id[edge.source], edge.source_port,
             left_by_id[edge.target], edge.target_port)
            for edge in left.edges if edge.source in left_ids
        )
        right_edges = Counter(
            (right_by_id[edge.source], edge.source_port,
             right_by_id[edge.target], edge.target_port)
            for edge in right.edges if edge.source in right_ids
        )
        size_left = len(left_nodes) + sum(left_edges.values())
        size_right = len(right_nodes) + sum(right_edges.values())
        size_similarity = min(size_left, size_right) / max(size_left, size_right, 1)
        return (
            0.45 * multiset_similarity(left_kinds, right_kinds)
            + 0.45 * multiset_similarity(left_edges, right_edges)
            + 0.10 * size_similarity
        )

    def _recombine(self, parents: list[Entity]) -> Genome:
        """Vererbt homologe Plätze; die Gesamtgröße entsteht erst danach."""
        architecture_parent = self.rng.choice(parents)
        activity_parent = self.rng.choice(parents)
        knock_parent = self.rng.choice(parents)
        bond_parent = self.rng.choice(parents)
        slots_by_parent = {
            parent.id: sorted({node.segment for node in parent.genome.nodes})
            for parent in parents
        }
        used: dict[int, set[int]] = {parent.id: set() for parent in parents}
        chosen_slots: list[tuple[Entity, int, list[dict[str, Any]]]] = []
        homology_threshold = 0.55

        for architecture_slot in slots_by_parent[architecture_parent.id]:
            alleles: list[tuple[Entity, int, float]] = [
                (architecture_parent, architecture_slot, 1.0)
            ]
            matches: list[dict[str, Any]] = []
            for parent in parents:
                if parent.id == architecture_parent.id:
                    continue
                candidates = [
                    (self._slot_homology(
                        architecture_parent.genome, architecture_slot,
                        parent.genome, candidate,
                    ), candidate)
                    for candidate in slots_by_parent[parent.id]
                    if candidate not in used[parent.id]
                ]
                if not candidates:
                    continue
                score, candidate = max(candidates)
                if score < homology_threshold:
                    continue
                used[parent.id].add(candidate)
                alleles.append((parent, candidate, score))
                matches.append({
                    "parent_id": parent.id, "slot_id": candidate,
                    "homology": round(score, 6),
                })
            donor, donor_slot, _score = self.rng.choice(alleles)
            chosen_slots.append((donor, donor_slot, matches))

        child_nodes: list[Node] = []
        child_edges: list[Edge] = []
        node_mapping: dict[tuple[int, int], int] = {}
        inherited_fragments: list[dict[str, Any]] = []
        next_id = 1
        for child_slot, (donor, donor_slot, matches) in enumerate(chosen_slots, start=1):
            selected_nodes = sorted(
                (node for node in donor.genome.nodes if node.segment == donor_slot),
                key=lambda node: node.id,
            )
            mapping: dict[int, int] = {}
            for original in selected_nodes:
                mapping[original.id] = next_id
                node_mapping[(donor.id, original.id)] = next_id
                child_nodes.append(Node(
                    next_id, original.kind, original.constant, child_slot,
                ))
                next_id += 1
            inherited_fragments.append({
                "parent_id": donor.id,
                "segment_id": donor_slot,
                "child_segment_id": child_slot,
                "homologous_matches": matches,
                "trimmed": False,
                "node_mapping": {str(source): target for source, target in sorted(mapping.items())},
                "edges": [], "resolved_edges": [], "dropped_edges": [],
                "edge_resolutions": [],
            })

        # Anschlusskanten gehören weiterhin zum Platz ihres Quellpunkts.
        pending: list[tuple[dict[str, Any], Edge, int, Node | None]] = []
        fragment_by_donor_slot = {
            (fragment["parent_id"], fragment["segment_id"]): fragment
            for fragment in inherited_fragments
        }
        for donor, donor_slot, _matches in chosen_slots:
            fragment = fragment_by_donor_slot[(donor.id, donor_slot)]
            source_ids = {
                node.id for node in donor.genome.nodes if node.segment == donor_slot
            }
            donor_by_id = {node.id: node for node in donor.genome.nodes}
            for edge in donor.genome.edges:
                if edge.source not in source_ids:
                    continue
                fragment["edges"].append(asdict(edge))
                source = node_mapping[(donor.id, edge.source)]
                target = node_mapping.get((donor.id, edge.target))
                if target is not None:
                    resolved = Edge(
                        source, edge.source_port, target, edge.target_port, edge.weight,
                    )
                    child_edges.append(resolved)
                    fragment["resolved_edges"].append(asdict(resolved))
                    fragment["edge_resolutions"].append({
                        "status": "preserved", "original": asdict(edge),
                        "resolved": asdict(resolved),
                    })
                else:
                    pending.append((fragment, edge, source, donor_by_id.get(edge.target)))

        def semantic_role(port: str) -> str:
            return "operand" if port in {"a", "b"} else port

        occupied = {(edge.target, edge.target_port) for edge in child_edges}
        for fragment, edge, source, target_spec in pending:
            exact: list[tuple[int, str]] = []
            compatible: list[tuple[int, str]] = []
            if target_spec is not None:
                wanted_role = semantic_role(edge.target_port)
                for node in child_nodes:
                    for port in PORTS[node.kind][0]:
                        if node.id == source or (node.id, port) in occupied:
                            continue
                        if node.kind == target_spec.kind and port == edge.target_port:
                            exact.append((node.id, port))
                        elif semantic_role(port) == wanted_role:
                            compatible.append((node.id, port))
            candidates = exact or compatible
            if not candidates:
                fragment["dropped_edges"].append(asdict(edge))
                fragment["edge_resolutions"].append({
                    "status": "dropped", "reason": "no_semantic_target",
                    "original": asdict(edge), "resolved": None,
                })
                continue
            target, target_port = self.rng.choice(candidates)
            resolved = Edge(source, edge.source_port, target, target_port, edge.weight)
            child_edges.append(resolved)
            occupied.add((target, target_port))
            fragment["resolved_edges"].append(asdict(resolved))
            fragment["edge_resolutions"].append({
                "status": "reconnected", "match": "exact" if exact else "role",
                "original": asdict(edge), "resolved": asdict(resolved),
            })

        genome = Genome(
            child_nodes, child_edges, activity_parent.genome.activity_base,
            knock_parent.genome.knock_capacity, bond_parent.genome.bond_ticks,
        )
        mutation = self._mutate(genome)
        genome.validate()
        self._last_genome_trace = {
            "target_n_g": None,
            "architecture_parent_id": architecture_parent.id,
            "size_parent_id": None,
            "activity_parent_id": activity_parent.id,
            "knock_capacity_parent_id": knock_parent.id,
            "bond_ticks_parent_id": bond_parent.id,
            "selection_rule": "homologous_slot_inheritance",
            "homology_threshold": homology_threshold,
            "inherited_fragments": inherited_fragments,
            "mutation": mutation,
        }
        return genome

    def _recombine_capacity_legacy(self, parents: list[Entity]) -> Genome:
        chosen_size_parent = self.rng.choice(parents)
        target = round(self.rng.gauss(chosen_size_parent.genome.n_g, self.config.genome_size_sigma))
        target = max(1, min(target, sum(p.genome.n_g for p in parents)))
        activity_parent = self.rng.choice(parents)
        activity_base = activity_parent.genome.activity_base
        knock_parent = self.rng.choice(parents)
        knock_capacity = knock_parent.genome.knock_capacity
        bond_parent = self.rng.choice(parents)
        bond_ticks = bond_parent.genome.bond_ticks
        segments: list[tuple[int, int, list[Node], list[Edge]]] = []
        for parent in parents:
            by_segment: dict[int, list[Node]] = {}
            for node in parent.genome.nodes:
                assert node.segment is not None
                by_segment.setdefault(node.segment, []).append(node)
            for segment_id, segment_nodes in sorted(by_segment.items()):
                node_ids = {node.id for node in segment_nodes}
                # Eine Kante gehört erblich zum Segment ihres Quellpunkts.
                outgoing_edges = [
                    edge for edge in parent.genome.edges if edge.source in node_ids
                ]
                segments.append((parent.id, segment_id, segment_nodes, outgoing_edges))
        # Elterliches Material wird fortlaufend bis zur gezogenen Kapazität
        # eingefüllt. Vollständige Segmente bleiben intakt; nur das letzte
        # Segment darf an der Kapazitätsgrenze abgeschnitten werden. Dadurch
        # kann ein größeres Kind zusätzliches Material beider Eltern aufnehmen,
        # ohne dass die Zielgröße selbst neue Geninformation erfindet.
        segment_order = list(range(len(segments)))
        self.rng.shuffle(segment_order)
        selected_parts: list[tuple[int, int, list[Node], list[Edge], bool]] = []
        remaining = target
        for segment_index in segment_order:
            parent_id, segment_id, segment_nodes, segment_edges = segments[segment_index]
            segment_size = len(segment_nodes) + len(segment_edges)
            if segment_size <= remaining:
                selected_parts.append((
                    parent_id, segment_id, list(segment_nodes), list(segment_edges), False,
                ))
                remaining -= segment_size
                if remaining == 0:
                    break
                continue

            # Das letzte Segment wird in stabiler Punktreihenfolge angeschnitten.
            # Ein übernommener Punkt bringt seine ausgehenden Kanten mit, soweit
            # die Restkapazität reicht; danach endet die Vererbung.
            partial_nodes: list[Node] = []
            partial_edges: list[Edge] = []
            outgoing: dict[int, list[Edge]] = {}
            for edge in segment_edges:
                outgoing.setdefault(edge.source, []).append(edge)
            for node in sorted(segment_nodes, key=lambda item: item.id):
                if remaining <= 0:
                    break
                partial_nodes.append(node)
                remaining -= 1
                for edge in outgoing.get(node.id, []):
                    if remaining <= 0:
                        break
                    partial_edges.append(edge)
                    remaining -= 1
                if remaining <= 0:
                    break
            if partial_nodes:
                selected_parts.append((
                    parent_id, segment_id, partial_nodes, partial_edges, True,
                ))
            break

        child_nodes: list[Node] = []
        child_edges: list[Edge] = []
        inherited_fragments: list[dict[str, Any]] = []
        next_id = 1
        node_mapping: dict[tuple[int, int], int] = {}
        child_segment_by_node: dict[int, int] = {}
        segment_mapping: dict[tuple[int, int], int] = {}
        for child_segment, part in enumerate(selected_parts, start=1):
            parent_id, segment_id, selected_nodes, _selected_edges, _trimmed = part
            segment_mapping[(parent_id, segment_id)] = child_segment
            for original in selected_nodes:
                node_mapping[(parent_id, original.id)] = next_id
                child_segment_by_node[next_id] = child_segment
                child_nodes.append(Node(
                    next_id, original.kind, original.constant, child_segment,
                ))
                next_id += 1

        # Zuerst werden alle noch vollständig vorhandenen Originalziele
        # reserviert. Semantisch reparierte Schnittkanten dürfen keine dieser
        # Eingaben verdrängen.
        resolutions: list[tuple[dict[str, Any], Edge, int, Node | None]] = []
        for parent_id, segment_id, selected_nodes, selected_edges, trimmed in selected_parts:
            mapping = {
                node.id: node_mapping[(parent_id, node.id)] for node in selected_nodes
            }
            resolved_edges: list[Edge] = []
            dropped_edges: list[dict[str, Any]] = []
            edge_resolutions: list[dict[str, Any]] = []
            fragment = {
                "parent_id": parent_id,
                "segment_id": segment_id,
                "child_segment_id": segment_mapping[(parent_id, segment_id)],
                "trimmed": trimmed,
                "node_mapping": {str(source): target for source, target in sorted(mapping.items())},
                "edges": [asdict(edge) for edge in selected_edges],
                "resolved_edges": resolved_edges,
                "dropped_edges": dropped_edges,
                "edge_resolutions": edge_resolutions,
            }
            inherited_fragments.append(fragment)
            for edge in selected_edges:
                source = node_mapping[(parent_id, edge.source)]
                original_target = node_mapping.get((parent_id, edge.target))
                if original_target is not None:
                    resolved = Edge(
                        source, edge.source_port, original_target,
                        edge.target_port, edge.weight,
                    )
                    child_edges.append(resolved)
                    resolved_edges.append(asdict(resolved))
                    edge_resolutions.append({
                        "status": "preserved", "original": asdict(edge),
                        "resolved": asdict(resolved),
                    })
                    continue
                parent_genome = self.entities[parent_id].genome
                target_spec = next(
                    (node for node in parent_genome.nodes if node.id == edge.target), None
                )
                resolutions.append((fragment, edge, source, target_spec))

        def semantic_role(port: str) -> str:
            if port in {"a", "b"}:
                return "operand"
            return port

        occupied = {(edge.target, edge.target_port) for edge in child_edges}
        for fragment, edge, source, target_spec in resolutions:
            exact: list[tuple[int, str]] = []
            compatible: list[tuple[int, str]] = []
            if target_spec is not None:
                wanted_role = semantic_role(edge.target_port)
                for node in child_nodes:
                    for port in PORTS[node.kind][0]:
                        if (node.id, port) in occupied or node.id == source:
                            continue
                        if node.kind == target_spec.kind and port == edge.target_port:
                            exact.append((node.id, port))
                        elif semantic_role(port) == wanted_role:
                            compatible.append((node.id, port))
            candidates = exact or compatible
            if not candidates:
                fragment["dropped_edges"].append(asdict(edge))
                fragment["edge_resolutions"].append({
                    "status": "dropped", "reason": "no_semantic_target",
                    "original": asdict(edge), "resolved": None,
                })
                continue
            target_node, target_port = self.rng.choice(candidates)
            resolved = Edge(
                source, edge.source_port, target_node, target_port, edge.weight,
            )
            child_edges.append(resolved)
            occupied.add((target_node, target_port))
            fragment["resolved_edges"].append(asdict(resolved))
            fragment["edge_resolutions"].append({
                "status": "reconnected", "match": "exact" if exact else "role",
                "original": asdict(edge), "resolved": asdict(resolved),
            })
        genome = Genome(child_nodes, child_edges, activity_base, knock_capacity, bond_ticks)
        mutation = self._mutate(genome)
        genome.validate()
        self._last_genome_trace = {
            "target_n_g": target,
            "size_parent_id": chosen_size_parent.id,
            "activity_parent_id": activity_parent.id,
            "knock_capacity_parent_id": knock_parent.id,
            "bond_ticks_parent_id": bond_parent.id,
            "selection_rule": "ordered_segment_fill_with_semantic_trim",
            "inherited_fragments": inherited_fragments,
            "mutation": mutation,
        }
        return genome

    def _mutate(self, genome: Genome) -> dict[str, Any] | None:
        if self.rng.random() >= self.config.mutation_probability:
            return None
        slots = sorted({node.segment for node in genome.nodes})
        structural = ["slot_duplicate"] if slots else []
        if len(slots) > 1:
            structural.extend(("slot_delete", "slot_fuse"))
        if any(sum(node.segment == slot for node in genome.nodes) > 1 for slot in slots):
            structural.append("slot_split")
        if structural and self.rng.random() < 0.10:
            mutation = self.rng.choice(structural)
        else:
            classes = ["activity", "knock_capacity", "bond_ticks"]
            if genome.nodes:
                classes.append("node")
            if genome.edges:
                classes.extend(("edge", "edge_weight"))
            mutation = self.rng.choice(classes)
        detail: dict[str, Any] = {"class": mutation}
        if mutation == "slot_duplicate":
            source_slot = self.rng.choice(slots)
            new_slot = max(slots, default=0) + 1
            originals = [node for node in genome.nodes if node.segment == source_slot]
            next_id = max((node.id for node in genome.nodes), default=0) + 1
            mapping: dict[int, int] = {}
            copies: list[Node] = []
            for original in originals:
                mapping[original.id] = next_id
                copies.append(Node(next_id, original.kind, original.constant, new_slot))
                next_id += 1
            copied_edges: list[Edge] = []
            for edge in list(genome.edges):
                if edge.source not in mapping:
                    continue
                copied_edges.append(Edge(
                    mapping[edge.source], edge.source_port,
                    mapping.get(edge.target, edge.target), edge.target_port, edge.weight,
                ))
            genome.nodes.extend(copies)
            genome.edges.extend(copied_edges)
            detail.update({
                "source_slot": source_slot, "new_slot": new_slot,
                "nodes_added": len(copies), "edges_added": len(copied_edges),
            })
        elif mutation == "slot_delete":
            removed_slot = self.rng.choice(slots)
            removed = {node.id for node in genome.nodes if node.segment == removed_slot}
            before_edges = len(genome.edges)
            genome.nodes[:] = [node for node in genome.nodes if node.id not in removed]
            genome.edges[:] = [
                edge for edge in genome.edges
                if edge.source not in removed and edge.target not in removed
            ]
            detail.update({
                "removed_slot": removed_slot, "nodes_removed": len(removed),
                "edges_removed": before_edges - len(genome.edges),
            })
        elif mutation == "slot_split":
            candidates = [
                slot for slot in slots
                if sum(node.segment == slot for node in genome.nodes) > 1
            ]
            source_slot = self.rng.choice(candidates)
            members = [node for node in genome.nodes if node.segment == source_slot]
            self.rng.shuffle(members)
            moved = members[len(members) // 2:]
            new_slot = max(slots, default=0) + 1
            for node in moved:
                node.segment = new_slot
            detail.update({
                "source_slot": source_slot, "new_slot": new_slot,
                "nodes_moved": len(moved),
            })
        elif mutation == "slot_fuse":
            target_slot, removed_slot = self.rng.sample(slots, 2)
            moved = 0
            for node in genome.nodes:
                if node.segment == removed_slot:
                    node.segment = target_slot
                    moved += 1
            detail.update({
                "target_slot": target_slot, "removed_slot": removed_slot,
                "nodes_moved": moved,
            })
        elif mutation == "activity":
            detail["before"] = genome.activity_base
            genome.activity_base = max(1, genome.activity_base + self.rng.choice((-1, 1)))
            detail["after"] = genome.activity_base
        elif mutation == "knock_capacity":
            detail["before"] = genome.knock_capacity
            genome.knock_capacity = max(1, min(16, genome.knock_capacity + self.rng.choice((-1, 1))))
            detail["after"] = genome.knock_capacity
        elif mutation == "bond_ticks":
            detail["before"] = genome.bond_ticks
            genome.bond_ticks = max(1, genome.bond_ticks + self.rng.choice((-1, 1)))
            detail["after"] = genome.bond_ticks
        elif mutation == "node":
            node = self.rng.choice(genome.nodes)
            detail.update({"node_id": node.id, "before": asdict(node)})
            if node.kind == "CONST" and self.rng.random() < 0.5:
                node.constant = i64((node.constant or 0) + self.rng.choice((-1, 1)))
            else:
                signature = PORTS[node.kind]
                choices = [kind for kind, ports in PORTS.items() if ports == signature and kind != node.kind]
                if choices:
                    node.kind = self.rng.choice(choices)
                    node.constant = 0 if node.kind == "CONST" else None
            detail["after"] = asdict(node)
        elif mutation == "edge":
            edge_index = self.rng.randrange(len(genome.edges))
            edge = genome.edges[edge_index]
            detail.update({"edge_index": edge_index, "before": asdict(edge)})
            if self.rng.random() < 0.5:
                candidates = [(n.id, p) for n in genome.nodes for p in PORTS[n.kind][1]]
                source, port = self.rng.choice(candidates)
                genome.edges[edge_index] = Edge(
                    source, port, edge.target, edge.target_port, edge.weight,
                )
            else:
                candidates = [(n.id, p) for n in genome.nodes for p in PORTS[n.kind][0]]
                target, port = self.rng.choice(candidates)
                genome.edges[edge_index] = Edge(
                    edge.source, edge.source_port, target, port, edge.weight,
                )
            detail["after"] = asdict(genome.edges[edge_index])
        else:
            edge_index = self.rng.randrange(len(genome.edges))
            edge = genome.edges[edge_index]
            magnitude = self._weight_mutation_magnitude()
            delta = magnitude if self.rng.random() < 0.5 else -magnitude
            detail.update({
                "edge_index": edge_index,
                "before": asdict(edge),
                "delta": delta,
            })
            genome.edges[edge_index] = Edge(
                edge.source, edge.source_port, edge.target, edge.target_port,
                edge.weight + delta,
            )
            detail["after"] = asdict(genome.edges[edge_index])
        return detail

    def _weight_mutation_magnitude(self) -> int:
        """Ziehe exakt proportional zu 1/k², k >= 1, ohne feste Obergrenze.

        1/(k(k+1)) dient als leicht ziehbare Vorschlagsverteilung. Eine
        Akzeptanzwahrscheinlichkeit von (k+1)/(2k) korrigiert sie auf 1/k².
        """
        while True:
            draw = self.rng.random()
            if draw == 0.0:
                continue
            magnitude = int(1.0 / draw)
            if self.rng.random() < (magnitude + 1) / (2 * magnitude):
                return magnitude

    def observation(self) -> dict[str, Any]:
        return {
            "schema": 1,
            "version": self.version,
            "tick": self.tick,
            "config": asdict(self.config),
            "ram": list(self.ram),
            "environment_toys": self.environment_toys,
            "entities": [
                {
                    "id": e.id,
                    "name": e.name,
                    "alive": e.alive,
                    "corpse_available": e.corpse_available,
                    "energy": e.energy,
                    "start_energy": e.start_energy,
                    "born_at": e.born_at,
                    "generation": e.generation,
                    "ram_position": e.ram_position,
                    "parents": list(e.parents),
                    "partners": list(e.partner_ids),
                    "knockers": [self._mem_read(e, 3, slot) for slot in range(e.genome.knock_capacity)],
                    "n_f": len(e.genome.nodes),
                    "n_p": e.genome.n_p,
                    "n_g": e.genome.n_g,
                    "activity_base": e.genome.activity_base,
                    "knock_capacity": e.genome.knock_capacity,
                    "bond_ticks": e.genome.bond_ticks,
                    "k_slots": len(e.k),
                    "z_used": sum(value is not None for value in e.z),
                    "genome": {
                        "nodes": [asdict(node) for node in e.genome.nodes],
                        "edges": [asdict(edge) for edge in e.genome.edges],
                    },
                    "k": {
                        key: self._signal_state(signal)
                        for key, signal in sorted(e.k.items())
                    },
                    "z": [self._signal_state(value) for value in e.z],
                    "value_history": dict(sorted(e.value_history.items())),
                    "source_history": dict(sorted(e.source_history.items())),
                    "ram_last_seen": {str(key): value for key, value in sorted(e.ram_last_seen.items())},
                    "ram_seen_count": dict(sorted(e.ram_seen_count.items())),
                }
                for e in sorted(self.entities.values(), key=lambda item: item.id)
            ],
        }

    def live_observation(self) -> dict[str, Any]:
        """Small read-only state for the live desk.

        Unlike :meth:`observation`, this deliberately contains no RAM copy,
        signal stores, histories, or repeated genome topology.  Those remain
        available through periodic observations and the normalized genome
        tables.  Building the live view must not scale with the amount of
        historical knowledge accumulated by every amoeba.
        """
        return {
            "schema": 1,
            "version": self.version,
            "tick": self.tick,
            "config": asdict(self.config),
            "ram_size": len(self.ram),
            "environment_toys": self.environment_toys,
            "entities": [
                {
                    "id": entity.id,
                    "name": entity.name,
                    "alive": entity.alive,
                    "corpse_available": entity.corpse_available,
                    "energy": entity.energy,
                    "start_energy": entity.start_energy,
                    "born_at": entity.born_at,
                    "generation": entity.generation,
                    "ram_position": entity.ram_position,
                    "parents": list(entity.parents),
                    "partners": list(entity.partner_ids),
                    "n_f": len(entity.genome.nodes),
                    "n_p": entity.genome.n_p,
                    "n_g": entity.genome.n_g,
                    "activity_base": entity.genome.activity_base,
                    "knock_capacity": entity.genome.knock_capacity,
                    "bond_ticks": entity.genome.bond_ticks,
                    "k_slots": len(entity.k),
                    "z_used": sum(value is not None for value in entity.z),
                }
                for entity in sorted(self.entities.values(), key=lambda item: item.id)
            ],
        }

    def checkpoint(self) -> dict[str, Any]:
        """Vollständiger, versionsfähiger Zustand für deterministisches Fortsetzen."""
        return {
            "schema": 1,
            "version": self.version,
            "tick": self.tick,
            "config": asdict(self.config),
            "ram": list(self.ram),
            "ram_originators": [list(items) for items in self.ram_originators],
            "environment_toys": self.environment_toys,
            "next_entity_id": self.next_entity_id,
            "rng_state": self._json_state(self.rng.getstate()),
            "group_stability": {",".join(map(str, group)): age for group, age in self.group_stability.items()},
            "entities": [self._entity_state(e) for e in sorted(self.entities.values(), key=lambda item: item.id)],
        }

    @staticmethod
    def _json_state(value: Any) -> Any:
        if isinstance(value, tuple):
            return [Simulation._json_state(item) for item in value]
        return value

    @staticmethod
    def _tuple_state(value: Any) -> Any:
        if isinstance(value, list):
            return tuple(Simulation._tuple_state(item) for item in value)
        return value

    @staticmethod
    def _signal_state(signal: Signal | None) -> dict[str, Any] | None:
        return None if signal is None else {
            "value": signal.value, "sources": list(signal.sources),
            "originators": list(signal.originators),
        }

    def _entity_state(self, entity: Entity) -> dict[str, Any]:
        return {
            "id": entity.id, "name": entity.name,
            "energy": entity.energy, "start_energy": entity.start_energy,
            "born_at": entity.born_at,
            "generation": entity.generation,
            "ram_position": entity.ram_position,
            "parents": list(entity.parents), "alive": entity.alive,
            "corpse_available": entity.corpse_available,
            "partner_ids": list(entity.partner_ids),
            "knocker_ids": list(entity.knocker_ids),
            "genome": {
                "activity_base": entity.genome.activity_base,
                "knock_capacity": entity.genome.knock_capacity,
                "bond_ticks": entity.genome.bond_ticks,
                "nodes": [asdict(node) for node in entity.genome.nodes],
                "edges": [asdict(edge) for edge in entity.genome.edges],
            },
            "k": {key: self._signal_state(signal) for key, signal in entity.k.items()},
            "z": [self._signal_state(signal) for signal in entity.z],
            "value_history": dict(entity.value_history),
            "source_history": dict(entity.source_history),
            "ram_last_seen": {str(key): value for key, value in entity.ram_last_seen.items()},
            "ram_seen_count": dict(entity.ram_seen_count),
        }

    @classmethod
    def from_checkpoint(cls, state: dict[str, Any]) -> "Simulation":
        if state.get("schema") != 1 or state.get("version") not in {"0.1", cls.version}:
            raise ValueError("Nicht unterstütztes Checkpoint-Format")
        sim = cls(Config(**state["config"]), ram=list(state["ram"]))
        sim.ram = list(state["ram"])
        sim.tick = state["tick"]
        sim.ram_originators = [
            tuple(items) for items in state.get("ram_originators", [[] for _ in sim.ram])
        ]
        sim.next_entity_id = state["next_entity_id"]
        sim.rng.setstate(cls._tuple_state(state["rng_state"]))
        sim.entities.clear()
        for raw in state["entities"]:
            genome = Genome(
                [Node(**node) for node in raw["genome"]["nodes"]],
                [Edge(**edge) for edge in raw["genome"]["edges"]],
                raw["genome"]["activity_base"],
                raw["genome"].get("knock_capacity", 1),
                raw["genome"].get("bond_ticks", 1),
            )
            parents = tuple(raw["parents"])
            generation = raw.get(
                "generation",
                0 if not parents else 1 + max(sim.entities[parent].generation for parent in parents),
            )
            entity = Entity(
                id=raw["id"], name=raw.get("name", amoeba_name(raw["id"], generation)),
                genome=genome, energy=raw["energy"],
                start_energy=raw.get("start_energy", raw["energy"]), born_at=raw["born_at"],
                ram_position=raw.get("ram_position", 0),
                parents=parents, generation=generation, alive=raw["alive"],
                corpse_available=raw.get("corpse_available", not raw["alive"]),
                partner_ids=list(raw["partner_ids"]),
                knocker_ids=list(raw.get("knocker_ids", [raw["knocker_id"]] if raw.get("knocker_id") else [])),
                k={
                    key: Signal(item["value"], tuple(item["sources"]), tuple(item.get("originators", ())))
                    for key, item in raw["k"].items()
                },
                z=[
                    None if item is None else Signal(
                        item["value"], tuple(item["sources"]), tuple(item.get("originators", ()))
                    )
                    for item in raw["z"]
                ],
                value_history=dict(raw["value_history"]), source_history=dict(raw["source_history"]),
                ram_last_seen={int(key): value for key, value in raw.get("ram_last_seen", {}).items()},
                ram_seen_count=dict(raw.get("ram_seen_count", {})),
            )
            sim.entities[entity.id] = entity
        sim.events.clear()
        sim.group_stability = {
            tuple(int(item) for item in key.split(",")): age
            for key, age in state.get("group_stability", {}).items()
        }
        sim.environment_toys = state.get("environment_toys", {
            "stones": [], "bubbles": [], "switches": [],
        })
        return sim


def _segment_nodes(nodes: list[Node], groups: Iterable[Iterable[int]]) -> None:
    """Vergib explizite erbliche Segmente und prüfe vollständige Abdeckung."""
    assignments: dict[int, int] = {}
    for segment, node_ids in enumerate(groups, start=1):
        for node_id in node_ids:
            if node_id in assignments:
                raise ValueError("Funktionspunkt steht in mehreren Segmenten")
            assignments[node_id] = segment
    if set(assignments) != {node.id for node in nodes}:
        raise ValueError("Segmentdefinition muss jeden Funktionspunkt genau einmal abdecken")
    for node in nodes:
        node.segment = assignments[node.id]


def demo_genome(partner_id: int, ram_start: int = 0) -> Genome:
    nodes = [
        Node(1, "CONST", 1), Node(2, "CONST", 0), Node(3, "CONST", partner_id), Node(4, "MEM_WRITE"),
        Node(5, "CONST", ram_start), Node(6, "RAM_READ"), Node(7, "CONST", 0), Node(8, "Z_WRITE"),
    ]
    _segment_nodes(nodes, (range(1, 5), range(5, 9)))
    edges = [
        Edge(1, "value", 4, "offset"), Edge(2, "value", 4, "slot"), Edge(3, "value", 4, "value"),
        Edge(5, "value", 6, "address"), Edge(6, "value", 8, "value"), Edge(7, "value", 8, "address"),
    ]
    return Genome(nodes, edges, activity_base=32)


def explorer_demo_genome(partner_id: int, ram_start: int = 0) -> Genome:
    """Technisches Testgenom: Partnersignal plus rückgekoppelter RAM-Adresszähler."""
    nodes = [
        Node(1, "CONST", 1), Node(2, "CONST", 0), Node(3, "CONST", partner_id), Node(4, "MEM_WRITE"),
        Node(5, "CONST", ram_start), Node(6, "CONST", 1), Node(7, "ADD"), Node(8, "RAM_READ"),
        Node(9, "CONST", 0), Node(10, "Z_WRITE"),
    ]
    _segment_nodes(nodes, (range(1, 5), range(5, 11)))
    edges = [
        Edge(1, "value", 4, "offset"), Edge(2, "value", 4, "slot"), Edge(3, "value", 4, "value"),
        Edge(5, "value", 7, "a"), Edge(6, "value", 7, "b"),
        Edge(7, "value", 7, "a"), Edge(7, "value", 8, "address"), Edge(7, "value", 10, "address"),
        Edge(8, "value", 10, "value"), Edge(9, "value", 10, "address"),
    ]
    return Genome(nodes, edges, activity_base=48)


def p1_explorer_genome(
    partner_id: int | None = None,
    *,
    search_offset: int = -1,
    search_step: int = 1,
    search_patience: int = 64,
    activity_base: int = 100,
    knock_capacity: int = 2,
    bond_ticks: int = 5,
) -> Genome:
    """P1: Membransuche/Handshake, RAM-Exploration und neutrales Schreiben."""
    if search_step == 0:
        raise ValueError("Die Partnersuch-Schrittweite darf nicht 0 sein")
    if search_patience < 1:
        raise ValueError("Die Partnersuch-Geduld muss positiv sein")
    nodes = [
        # Fragment A: Z[3] durchlaeuft Membran-IDs. Eine reale fremde ID wird
        # vorgeschlagen; eine gelesene Einladung an die eigene ID wird erwidert.
        Node(1, "CONST", 0), Node(2, "CONST", 1), Node(3, "CONST", 3),
        Node(4, "CONST", 999_996), Node(5, "Z_READ"), Node(6, "ADD"),
        Node(7, "ADD"), Node(8, "ADD"), Node(9, "ADD"), Node(10, "RAM_READ"),
        Node(11, "EQ"), Node(12, "EQ"), Node(13, "GATE"), Node(14, "GATE"),
        Node(15, "Z_WRITE"), Node(16, "GATE"), Node(17, "MEM_WRITE"),
        Node(18, "ADD"), Node(19, "RAM_READ"), Node(20, "MEM_READ"),
        Node(21, "EQ"), Node(22, "GATE"), Node(23, "MEM_WRITE"),
        # Fragment B: persistente Exploration der normalen RAM-Suppe.
        Node(24, "CONST", 0), Node(25, "Z_READ"), Node(26, "CONST", 1),
        Node(27, "ADD"), Node(28, "Z_WRITE"), Node(29, "RAM_READ"),
        Node(30, "CONST", 1), Node(31, "Z_WRITE"), Node(32, "CONST", 2),
        Node(33, "GATE"), Node(34, "Z_WRITE"),
        # Fragment C: neutrale Markierung RAM[eigene ID] = eigene ID.
        Node(35, "CONST", 0), Node(36, "MEM_READ"), Node(37, "RAM_WRITE"),
        # Der erste Vorschlag bleibt stehen, solange der eigene Slot belegt ist.
        Node(38, "MEM_READ"), Node(39, "EQ"), Node(40, "GATE"),
        # Der Lebenszustand der gefundenen Amöbe ist eine eigene Beobachtung.
        Node(41, "ADD"), Node(42, "ADD"), Node(43, "RAM_READ"),
        # Die Membransuche beginnt bei der vorherigen ID der eigenen Nachbarschaft.
        Node(44, "MEM_READ"), Node(45, "CONST", search_offset), Node(46, "ADD"),
        Node(47, "ADD"),
        # Ein nachweislich verstorbener eingetragener Partner gibt den Slot frei.
        Node(48, "EQ"), Node(49, "EQ"), Node(50, "GATE"),
        Node(51, "GATE"), Node(52, "MEM_WRITE"),
        # Erbliche Suchgeometrie: Offset und vorzeichenbehafteter Schritt sind
        # gewöhnliche CONST-Punkte, keine Supervisorstrategie.
        Node(53, "CONST", search_step),
        # Experimenteller genomischer Rückzug: Solange der eigene Vorschlagsslot
        # belegt ist, zählt Z[4] erfolgreiche Prüfzyklen. Bei der erblichen
        # Geduldsschwelle schreibt das Genom selbst 0 in Slot und Zähler.
        Node(54, "CONST", 4), Node(55, "Z_READ"), Node(56, "CONST", 1),
        Node(57, "ADD"), Node(58, "Z_WRITE"), Node(59, "CONST", search_patience),
        Node(60, "EQ"), Node(61, "MEM_READ"), Node(62, "EQ"), Node(63, "EQ"),
        Node(64, "GATE"), Node(65, "GATE"), Node(66, "MEM_WRITE"),
        Node(67, "Z_WRITE"),
        # Experimentelle Klingel: Der erste wartende lebende Vorschlag ist in
        # der eigenen Membran unter Offset 3 lesbar. Bei freiem Partnerslot
        # wird er genomisch erwidert; die technische Schicht paart nicht selbst.
        Node(68, "CONST", 3), Node(69, "MEM_READ"), Node(70, "GATE"),
        Node(71, "MEM_WRITE"),
        # Zweiter Partnerslot und zweiter Klopfer erlauben, aber erzwingen
        # keine vollständig gegenseitige Dreierbeziehung.
        Node(72, "MEM_READ"), Node(73, "EQ"), Node(74, "MEM_READ"),
        Node(75, "GATE"), Node(76, "MEM_WRITE"),
    ]
    # Die Rumpfamöbe beginnt mit drei evolvierbaren Vererbungsplätzen.
    # Ihre Größe ist nicht begrenzt; die Gruppierung ist Verpackung, keine
    # Aussage über erwünschte Funktion oder späteren Nutzen.
    _segment_nodes(nodes, (
        (*range(1, 18), *range(41, 48), 53),
        (*range(18, 41), *range(48, 53), *range(54, 68)),
        range(68, 77),
    ))
    edges = [
        Edge(3, "value", 5, "address"), Edge(5, "value", 6, "a"),
        Edge(53, "value", 6, "b"), Edge(47, "value", 7, "a"),
        Edge(47, "value", 7, "b"), Edge(7, "value", 8, "a"),
        Edge(47, "value", 8, "b"), Edge(8, "value", 41, "a"),
        Edge(47, "value", 41, "b"), Edge(41, "value", 9, "a"),
        Edge(4, "value", 9, "b"), Edge(9, "value", 10, "address"),
        Edge(10, "value", 11, "a"), Edge(1, "value", 11, "b"),
        Edge(11, "value", 12, "a"), Edge(1, "value", 12, "b"),
        Edge(6, "value", 13, "value"), Edge(12, "value", 13, "condition"),
        Edge(1, "value", 14, "value"), Edge(11, "value", 14, "condition"),
        Edge(13, "value", 15, "value"), Edge(14, "value", 15, "value"),
        Edge(3, "value", 15, "address"), Edge(10, "value", 16, "value"),
        Edge(12, "value", 16, "condition"), Edge(16, "value", 40, "value"),
        Edge(2, "value", 17, "offset"), Edge(1, "value", 17, "slot"),
        Edge(9, "value", 18, "a"), Edge(2, "value", 18, "b"),
        Edge(18, "value", 19, "address"), Edge(1, "value", 20, "offset"),
        Edge(1, "value", 20, "slot"), Edge(19, "value", 21, "a"),
        Edge(20, "value", 21, "b"), Edge(10, "value", 22, "value"),
        Edge(21, "value", 22, "condition"), Edge(22, "value", 23, "value"),
        Edge(2, "value", 23, "offset"), Edge(1, "value", 23, "slot"),
        Edge(24, "value", 25, "address"), Edge(24, "value", 28, "address"),
        Edge(25, "value", 27, "a"), Edge(26, "value", 27, "b"),
        Edge(27, "value", 28, "value"), Edge(27, "value", 29, "address"),
        Edge(29, "value", 31, "value"), Edge(30, "value", 31, "address"),
        Edge(29, "value", 33, "value"), Edge(29, "value", 33, "condition"),
        Edge(32, "value", 34, "address"), Edge(33, "value", 34, "value"),
        Edge(35, "value", 36, "offset"), Edge(35, "value", 36, "slot"),
        Edge(36, "value", 37, "address"), Edge(36, "value", 37, "value"),
        Edge(2, "value", 38, "offset"), Edge(1, "value", 38, "slot"),
        Edge(38, "value", 39, "a"), Edge(1, "value", 39, "b"),
        Edge(39, "value", 40, "condition"), Edge(40, "value", 17, "value"),
        Edge(9, "value", 42, "a"), Edge(3, "value", 42, "b"),
        Edge(42, "value", 43, "address"),
        Edge(1, "value", 44, "offset"), Edge(1, "value", 44, "slot"),
        Edge(44, "value", 46, "a"), Edge(45, "value", 46, "b"),
        Edge(46, "value", 47, "a"), Edge(5, "value", 47, "b"),
        Edge(43, "value", 48, "a"), Edge(1, "value", 48, "b"),
        Edge(10, "value", 49, "a"), Edge(38, "value", 49, "b"),
        Edge(43, "value", 50, "value"), Edge(48, "value", 50, "condition"),
        Edge(50, "value", 51, "value"), Edge(49, "value", 51, "condition"),
        Edge(2, "value", 52, "offset"), Edge(1, "value", 52, "slot"),
        Edge(51, "value", 52, "value"),
        Edge(54, "value", 55, "address"), Edge(55, "value", 57, "a"),
        Edge(56, "value", 57, "b"), Edge(2, "value", 61, "offset"),
        Edge(1, "value", 61, "slot"), Edge(61, "value", 62, "a"),
        Edge(1, "value", 62, "b"), Edge(62, "value", 63, "a"),
        Edge(1, "value", 63, "b"), Edge(57, "value", 64, "value"),
        Edge(63, "value", 64, "condition"), Edge(64, "value", 58, "value"),
        Edge(54, "value", 58, "address"), Edge(64, "value", 60, "a"),
        Edge(59, "value", 60, "b"), Edge(1, "value", 65, "value"),
        Edge(60, "value", 65, "condition"), Edge(65, "value", 66, "value"),
        Edge(2, "value", 66, "offset"), Edge(1, "value", 66, "slot"),
        Edge(65, "value", 67, "value"), Edge(54, "value", 67, "address"),
        Edge(68, "value", 69, "offset"), Edge(1, "value", 69, "slot"),
        Edge(69, "value", 70, "value"), Edge(39, "value", 70, "condition"),
        Edge(70, "value", 71, "value"), Edge(2, "value", 71, "offset"),
        Edge(1, "value", 71, "slot"),
        Edge(2, "value", 72, "offset"), Edge(2, "value", 72, "slot"),
        Edge(72, "value", 73, "a"), Edge(1, "value", 73, "b"),
        Edge(68, "value", 74, "offset"), Edge(2, "value", 74, "slot"),
        Edge(74, "value", 75, "value"), Edge(73, "value", 75, "condition"),
        Edge(75, "value", 76, "value"), Edge(2, "value", 76, "offset"),
        Edge(2, "value", 76, "slot"),
    ]
    return Genome(
        nodes, edges, activity_base=activity_base,
        knock_capacity=knock_capacity, bond_ticks=bond_ticks,
    )
