"""Unverändertes P1-Fachmodell im technischen Prototyp EVE-Alife v0.2."""

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
AMOEBA_NAMES = (
    "Tom", "Erna", "Ada", "Bruno", "Clara", "Dario", "Emmi", "Fritz",
    "Greta", "Hugo", "Ida", "Juri", "Karla", "Lino", "Maja", "Nils",
    "Olga", "Piet", "Rosa", "Sam", "Tilda", "Uwe", "Vera", "Willi",
    "Xenia", "Yara", "Zeno", "Alma", "Ben", "Cleo", "Dora", "Enno",
)


def amoeba_name(entity_id: int) -> str:
    """Deterministischer, innerhalb eines Laufs eindeutiger Anzeigename."""
    base = AMOEBA_NAMES[(entity_id - 1) % len(AMOEBA_NAMES)]
    generation = (entity_id - 1) // len(AMOEBA_NAMES) + 1
    return base if generation == 1 else f"{base} {generation}"


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


@dataclass
class Genome:
    nodes: list[Node]
    edges: list[Edge]
    activity_base: int

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
    parents: tuple[int, ...] = ()
    k: dict[str, Signal] = field(default_factory=dict)
    z: list[Signal | None] = field(default_factory=list)
    partner_ids: list[int | None] = field(default_factory=lambda: [None, None])
    value_history: dict[str, int] = field(default_factory=dict)
    source_history: dict[str, int] = field(default_factory=dict)
    ram_last_seen: dict[int, int] = field(default_factory=dict)
    ram_seen_count: dict[str, int] = field(default_factory=dict)
    alive: bool = True

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


class Simulation:
    version = "0.2"

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

    def emit(self, kind: str, **data: Any) -> None:
        self.events.append({"tick": self.tick, "kind": kind, **data})

    def add_entity(self, genome: Genome, energy: float, parents: tuple[int, ...] = ()) -> Entity:
        genome.validate()
        entity = Entity(
            id=self.next_entity_id,
            name=amoeba_name(self.next_entity_id),
            genome=genome,
            energy=energy,
            start_energy=energy,
            born_at=self.tick,
            parents=parents,
            z=[None] * self.config.z_size,
        )
        self.next_entity_id += 1
        self.entities[entity.id] = entity
        self.emit(
            "birth", entity_id=entity.id, entity_name=entity.name,
            parents=list(parents), energy=energy, n_g=genome.n_g,
        )
        return entity

    def heartbeat(self) -> None:
        self.tick += 1
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
                    entity.k[Entity.key(edge.target, edge.target_port)] = signal
                    self.emit("signal", entity_id=entity.id, source=node.id, target=edge.target, value=signal.value)

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
                if alive_foreign and offset == 0 and slot == 0 and changed:
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
                entity.energy += reward
                self.emit(
                    "ram_read", entity_id=entity.id, address=raw_address, value=value,
                    virtual=True, target_id=target.id, membrane_offset=offset,
                    membrane_slot=slot, previous=previous, changed=changed,
                    discovery_type=discovery_type, reward=reward,
                )
                return {"value": Signal(value, (f"MEM[{target.id},{offset},{slot}]",))}
            address = raw_address % len(self.ram)
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
                virtual=False, previous=previous, changed=changed,
                self_origin=self_origin, originators=list(writers), reward=reward,
            )
            return {"value": Signal(value, (f"RAM[{address}]",), writers)}
        if kind == "RAM_WRITE":
            raw_address = inputs["address"].value
            signal = inputs["value"]
            if raw_address >= self.config.membrane_base:
                return {"value": signal}
            address = raw_address % len(self.ram)
            self.ram[address] = signal.value
            writers = tuple(sorted({*signal.originators, entity.id}))
            self.ram_originators[address] = writers
            self.emit(
                "ram_write", entity_id=entity.id, address=address, value=signal.value,
                originators=list(writers),
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
            return {"value": Signal(value, (f"MEM[{offset},{slot}]",))}
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
                discovered = required_source in signal.sources
                if target is not None and target.alive and target.id != entity.id and discovered:
                    entity.partner_ids[slot] = signal.value
                    self.emit(
                        "mem_write", entity_id=entity.id, offset=offset,
                        slot=slot, value=signal.value, discovered=True,
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
        if entity is None:
            return None
        if cell == 0:
            return entity, 0, 0
        if cell in (1, 2):
            return entity, 1, cell - 1
        return entity, 2, 0

    def _kill(self, entity: Entity, reason: str) -> None:
        entity.alive = False
        entity.k.clear()
        self.emit("death", entity_id=entity.id, reason=reason)

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

    def _reproduce(self) -> None:
        for group in self._valid_groups():
            parents = [self.entities[eid] for eid in group]
            if self.config.birth_energy_fraction is None:
                child_energy = self.config.birth_energy
            else:
                mean_parent_energy = sum(parent.energy for parent in parents) / len(parents)
                child_energy = self.config.birth_energy_fraction * mean_parent_energy
            contribution = child_energy / len(parents)
            if any(parent.energy < contribution for parent in parents):
                continue
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
            if any(parent.energy - contribution <= parent.start_energy for parent in parents):
                for parent in parents:
                    self.emit(
                        "birth_rejected", entity_id=parent.id, group=list(group),
                        offered_energy=child_energy, required_energy=minimum,
                        contribution=contribution, energy=parent.energy,
                        start_energy=parent.start_energy,
                        reason="parent_surplus_required",
                    )
                continue
            for parent in parents:
                energy_before = parent.energy
                parent.energy -= contribution
                parent.partner_ids[:] = [None, None]
                self.emit(
                    "reproduction_cost", entity_id=parent.id, child_id=self.next_entity_id,
                    cost=contribution, energy_before=energy_before, energy_after=parent.energy,
                )
            child = self.add_entity(genome, child_energy, group)
            self.emit(
                "genome_created", entity_id=child.id, parents=list(group),
                trace=self._last_genome_trace,
            )

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

    def _recombine(self, parents: list[Entity]) -> Genome:
        chosen_size_parent = self.rng.choice(parents)
        target = round(self.rng.gauss(chosen_size_parent.genome.n_g, self.config.genome_size_sigma))
        target = max(1, min(target, sum(p.genome.n_g for p in parents)))
        activity_parent = self.rng.choice(parents)
        activity_base = activity_parent.genome.activity_base
        fragments: list[tuple[int, list[Node], list[Edge]]] = []
        for parent in parents:
            nodes = {node.id: node for node in parent.genome.nodes}
            neighbors: dict[int, set[int]] = {node_id: set() for node_id in nodes}
            for edge in parent.genome.edges:
                neighbors[edge.source].add(edge.target)
                neighbors[edge.target].add(edge.source)
            remaining = set(nodes)
            while remaining:
                seed = min(remaining)
                component = {seed}
                frontier = [seed]
                while frontier:
                    current = frontier.pop()
                    for neighbor in neighbors[current]:
                        if neighbor not in component:
                            component.add(neighbor)
                            frontier.append(neighbor)
                remaining -= component
                component_edges = [
                    edge for edge in parent.genome.edges
                    if edge.source in component and edge.target in component
                ]
                fragments.append((parent.id, [nodes[node_id] for node_id in sorted(component)], component_edges))
        child_nodes: list[Node] = []
        child_edges: list[Edge] = []
        inherited_fragments: list[dict[str, Any]] = []
        next_id = 1
        # Atomare 0/1-Knapsack-Auswahl: Die Kombination soll die zufällig
        # gezogene Zielgröße möglichst gut erreichen. Damit kann eine deutlich
        # schlechter passende Folge kleiner Fragmente eine große Komponente
        # nicht mehr allein durch die Reihenfolge verdrängen. Gleich gute
        # Kombinationen bleiben zufällig.
        reachable: dict[int, tuple[tuple[int, ...], int]] = {0: ((), 1)}
        for index, (_parent_id, nodes, edges) in enumerate(fragments):
            size = len(nodes) + len(edges)
            for total, (combination, _count) in list(reachable.items())[::-1]:
                candidate_total = total + size
                if candidate_total > target:
                    continue
                candidate = combination + (index,)
                existing = reachable.get(candidate_total)
                if existing is None:
                    reachable[candidate_total] = (candidate, 1)
                else:
                    previous, count = existing
                    count += 1
                    reachable[candidate_total] = (
                        candidate if self.rng.randrange(count) == 0 else previous,
                        count,
                    )
        best_size = max(reachable)
        selected_indices = reachable[best_size][0]
        if not selected_indices:
            # Ein Fragment bleibt unteilbar, auch wenn die Zielgröße kleiner ist.
            selected_indices = (min(
                range(len(fragments)),
                key=lambda index: len(fragments[index][1]) + len(fragments[index][2]),
            ),)
        for fragment_index in selected_indices:
            parent_id, selected_nodes, selected_edges = fragments[fragment_index]
            mapping: dict[int, int] = {}
            for original in selected_nodes:
                mapping[original.id] = next_id
                child_nodes.append(Node(next_id, original.kind, original.constant))
                next_id += 1
            for edge in selected_edges:
                child_edges.append(Edge(mapping[edge.source], edge.source_port, mapping[edge.target], edge.target_port))
            inherited_fragments.append({
                "parent_id": parent_id,
                "node_mapping": {str(source): target for source, target in sorted(mapping.items())},
                "edges": [asdict(edge) for edge in selected_edges],
            })
        genome = Genome(child_nodes, child_edges, activity_base)
        mutation = self._mutate(genome)
        genome.validate()
        self._last_genome_trace = {
            "target_n_g": target,
            "size_parent_id": chosen_size_parent.id,
            "activity_parent_id": activity_parent.id,
            "selection_rule": "closest_atomic_subset",
            "inherited_fragments": inherited_fragments,
            "mutation": mutation,
        }
        return genome

    def _mutate(self, genome: Genome) -> dict[str, Any] | None:
        if self.rng.random() >= self.config.mutation_probability:
            return None
        classes = ["activity"]
        if genome.nodes:
            classes.append("node")
        if genome.edges:
            classes.append("edge")
        mutation = self.rng.choice(classes)
        detail: dict[str, Any] = {"class": mutation}
        if mutation == "activity":
            detail["before"] = genome.activity_base
            genome.activity_base = max(1, genome.activity_base + self.rng.choice((-1, 1)))
            detail["after"] = genome.activity_base
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
        else:
            edge_index = self.rng.randrange(len(genome.edges))
            edge = genome.edges[edge_index]
            detail.update({"edge_index": edge_index, "before": asdict(edge)})
            if self.rng.random() < 0.5:
                candidates = [(n.id, p) for n in genome.nodes for p in PORTS[n.kind][1]]
                source, port = self.rng.choice(candidates)
                genome.edges[edge_index] = Edge(source, port, edge.target, edge.target_port)
            else:
                candidates = [(n.id, p) for n in genome.nodes for p in PORTS[n.kind][0]]
                target, port = self.rng.choice(candidates)
                genome.edges[edge_index] = Edge(edge.source, edge.source_port, target, port)
            detail["after"] = asdict(genome.edges[edge_index])
        return detail

    def observation(self) -> dict[str, Any]:
        return {
            "schema": 1,
            "version": self.version,
            "tick": self.tick,
            "config": asdict(self.config),
            "ram": list(self.ram),
            "entities": [
                {
                    "id": e.id,
                    "name": e.name,
                    "alive": e.alive,
                    "energy": e.energy,
                    "start_energy": e.start_energy,
                    "born_at": e.born_at,
                    "parents": list(e.parents),
                    "partners": list(e.partner_ids),
                    "n_f": len(e.genome.nodes),
                    "n_p": e.genome.n_p,
                    "n_g": e.genome.n_g,
                    "activity_base": e.genome.activity_base,
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

    def checkpoint(self) -> dict[str, Any]:
        """Vollständiger, versionsfähiger Zustand für deterministisches Fortsetzen."""
        return {
            "schema": 1,
            "version": self.version,
            "tick": self.tick,
            "config": asdict(self.config),
            "ram": list(self.ram),
            "ram_originators": [list(items) for items in self.ram_originators],
            "next_entity_id": self.next_entity_id,
            "rng_state": self._json_state(self.rng.getstate()),
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
            "parents": list(entity.parents), "alive": entity.alive,
            "partner_ids": list(entity.partner_ids),
            "genome": {
                "activity_base": entity.genome.activity_base,
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
            )
            entity = Entity(
                id=raw["id"], name=raw.get("name", amoeba_name(raw["id"])),
                genome=genome, energy=raw["energy"],
                start_energy=raw.get("start_energy", raw["energy"]), born_at=raw["born_at"],
                parents=tuple(raw["parents"]), alive=raw["alive"],
                partner_ids=list(raw["partner_ids"]),
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
        return sim


def demo_genome(partner_id: int, ram_start: int = 0) -> Genome:
    nodes = [
        Node(1, "CONST", 1), Node(2, "CONST", 0), Node(3, "CONST", partner_id), Node(4, "MEM_WRITE"),
        Node(5, "CONST", ram_start), Node(6, "RAM_READ"), Node(7, "CONST", 0), Node(8, "Z_WRITE"),
    ]
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
    ]
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
    ]
    return Genome(nodes, edges, activity_base=activity_base)
