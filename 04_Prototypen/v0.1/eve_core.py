"""Minimaler, standardbibliotheksbasierter Experimentkern von EVE-Alife P0.1."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import floor, sqrt
from random import Random
from typing import Any, Iterable


MASK64 = (1 << 64) - 1
SIGN64 = 1 << 63


def i64(value: int) -> int:
    value &= MASK64
    return value - (1 << 64) if value & SIGN64 else value


def provenance(*signals: "Signal") -> tuple[str, ...]:
    return tuple(sorted({source for signal in signals for source in signal.sources}))


@dataclass(frozen=True)
class Signal:
    value: int
    sources: tuple[str, ...]


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
    genome: Genome
    energy: float
    born_at: int
    parents: tuple[int, ...] = ()
    k: dict[str, Signal] = field(default_factory=dict)
    z: list[Signal | None] = field(default_factory=list)
    partner_ids: list[int | None] = field(default_factory=lambda: [None, None])
    value_history: dict[str, int] = field(default_factory=dict)
    source_history: dict[str, int] = field(default_factory=dict)
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
    genome_size_sigma: float = 2.0
    mutation_probability: float = 0.001
    standby_cost: float = 1.0
    execution_cost: float = 1.0
    edge_cost: float = 0.1
    novelty_base: float = 10.0
    membrane_base: int = 1_000_000


class Simulation:
    version = "0.1"

    def __init__(self, config: Config, ram: list[int] | None = None) -> None:
        self.config = config
        self.rng = Random(config.seed)
        self.tick = 0
        self.ram = ram if ram is not None else [self.rng.randint(-(1 << 15), (1 << 15) - 1) for _ in range(config.ram_size)]
        if len(self.ram) != config.ram_size:
            raise ValueError("RAM-Größe stimmt nicht mit der Konfiguration überein")
        self.entities: dict[int, Entity] = {}
        self.next_entity_id = 1
        self.events: list[dict[str, Any]] = []

    def emit(self, kind: str, **data: Any) -> None:
        self.events.append({"tick": self.tick, "kind": kind, **data})

    def add_entity(self, genome: Genome, energy: float, parents: tuple[int, ...] = ()) -> Entity:
        genome.validate()
        entity = Entity(
            id=self.next_entity_id,
            genome=genome,
            energy=energy,
            born_at=self.tick,
            parents=parents,
            z=[None] * self.config.z_size,
        )
        self.next_entity_id += 1
        self.entities[entity.id] = entity
        self.emit("birth", entity_id=entity.id, parents=list(parents), energy=energy, n_g=genome.n_g)
        return entity

    def heartbeat(self) -> None:
        self.tick += 1
        for entity_id in sorted(tuple(self.entities)):
            entity = self.entities[entity_id]
            if not entity.alive:
                continue
            if entity.energy < self.config.standby_cost:
                self._kill(entity, "standby_unaffordable")
                continue
            entity.energy -= self.config.standby_cost
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
            entity.energy -= self.config.execution_cost + self.config.edge_cost * len(edges)
            outputs = self._fire(entity, node)
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
        if kind in {"ADD", "SUB", "XOR", "EQ"}:
            a, b = inputs["a"].value, inputs["b"].value
            value = {"ADD": a + b, "SUB": a - b, "XOR": a ^ b, "EQ": int(a == b)}[kind]
            return {"value": Signal(i64(value), provenance(inputs["a"], inputs["b"]))}
        if kind == "RAM_READ":
            raw_address = inputs["address"].value
            if raw_address >= self.config.membrane_base:
                membrane = self._decode_membrane_address(raw_address)
                if membrane is None:
                    return {"value": Signal(0, (f"MEM_VOID[{raw_address}]",))}
                target, offset, slot = membrane
                value = self._mem_read(target, offset, slot)
                return {"value": Signal(value, (f"MEM[{target.id},{offset},{slot}]",))}
            address = raw_address % len(self.ram)
            return {"value": Signal(self.ram[address], (f"RAM[{address}]",))}
        if kind == "RAM_WRITE":
            raw_address = inputs["address"].value
            signal = inputs["value"]
            if raw_address >= self.config.membrane_base:
                return {"value": signal}
            address = raw_address % len(self.ram)
            self.ram[address] = signal.value
            self.emit("ram_write", entity_id=entity.id, address=address, value=signal.value)
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
            value_key = str(signal.value)
            source_key = "|".join(signal.sources)
            k = entity.value_history.get(value_key, 0)
            r = entity.source_history.get(source_key, 0)
            reward = self.config.novelty_base / ((1 + k) * (1 + r))
            entity.value_history[value_key] = k + 1
            entity.source_history[source_key] = r + 1
            entity.energy += reward
            self.emit("z_write", entity_id=entity.id, address=address, value=signal.value, sources=list(signal.sources), reward=reward)
            return {"value": signal}
        if kind == "MEM_READ":
            offset, slot = inputs["offset"].value, inputs["slot"].value
            value = self._mem_read(entity, offset, slot)
            return {"value": Signal(value, (f"MEM[{offset},{slot}]",))}
        if kind == "MEM_WRITE":
            offset, slot, signal = inputs["offset"].value, inputs["slot"].value, inputs["value"]
            if offset == 1 and slot in (0, 1):
                entity.partner_ids[slot] = signal.value
                self.emit("mem_write", entity_id=entity.id, offset=offset, slot=slot, value=signal.value)
            return {"value": signal}
        raise AssertionError(kind)

    @staticmethod
    def _mem_read(entity: Entity, offset: int, slot: int) -> int:
        if offset == 0 and slot == 0:
            return entity.id
        if offset == 1 and slot in (0, 1):
            value = entity.partner_ids[slot]
            return 0 if value is None else value
        return 0

    def _decode_membrane_address(self, address: int) -> tuple[Entity, int, int] | None:
        relative = address - self.config.membrane_base
        if relative < 0:
            return None
        entity_id, cell = divmod(relative, 3)
        entity = self.entities.get(entity_id + 1)
        if entity is None:
            return None
        if cell == 0:
            return entity, 0, 0
        return entity, 1, cell - 1

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
            contribution = self.config.birth_energy / len(parents)
            if any(parent.energy < contribution for parent in parents):
                continue
            genome = self._recombine(parents)
            for parent in parents:
                parent.energy -= contribution
                parent.partner_ids[:] = [None, None]
            self.add_entity(genome, self.config.birth_energy, group)

    def _recombine(self, parents: list[Entity]) -> Genome:
        chosen_size_parent = self.rng.choice(parents)
        target = round(self.rng.gauss(chosen_size_parent.genome.n_g, self.config.genome_size_sigma))
        target = max(1, min(target, sum(p.genome.n_g for p in parents)))
        activity_base = self.rng.choice(parents).genome.activity_base
        pool: dict[tuple[int, int], Node] = {(p.id, n.id): n for p in parents for n in p.genome.nodes}
        parent_edges: dict[int, list[Edge]] = {p.id: list(p.genome.edges) for p in parents}
        child_nodes: list[Node] = []
        child_edges: list[Edge] = []
        next_id = 1
        attempts = 0
        while pool and len(child_nodes) + len(child_edges) < target and attempts < 1000:
            attempts += 1
            seed = self.rng.choice(list(pool))
            parent_id, _ = seed
            selected = {seed}
            desired_nodes = self.rng.randint(1, max(1, target - len(child_nodes) - len(child_edges)))
            while len(selected) < desired_nodes:
                frontier: list[tuple[int, int]] = []
                selected_ids = {nid for pid, nid in selected if pid == parent_id}
                for edge in parent_edges[parent_id]:
                    if edge.source in selected_ids and (parent_id, edge.target) in pool and (parent_id, edge.target) not in selected:
                        frontier.append((parent_id, edge.target))
                    if edge.target in selected_ids and (parent_id, edge.source) in pool and (parent_id, edge.source) not in selected:
                        frontier.append((parent_id, edge.source))
                if not frontier:
                    break
                selected.add(self.rng.choice(frontier))
            selected_ids = {nid for _, nid in selected}
            internal = [e for e in parent_edges[parent_id] if e.source in selected_ids and e.target in selected_ids]
            fragment_size = len(selected) + len(internal)
            remaining = target - len(child_nodes) - len(child_edges)
            if fragment_size > remaining:
                continue
            mapping: dict[int, int] = {}
            for key in sorted(selected):
                original = pool.pop(key)
                mapping[original.id] = next_id
                child_nodes.append(Node(next_id, original.kind, original.constant))
                next_id += 1
            for edge in internal:
                child_edges.append(Edge(mapping[edge.source], edge.source_port, mapping[edge.target], edge.target_port))
        genome = Genome(child_nodes, child_edges, activity_base)
        self._mutate(genome)
        genome.validate()
        return genome

    def _mutate(self, genome: Genome) -> None:
        if self.rng.random() >= self.config.mutation_probability:
            return
        classes = ["activity"]
        if genome.nodes:
            classes.append("node")
        if genome.edges:
            classes.append("edge")
        mutation = self.rng.choice(classes)
        if mutation == "activity":
            genome.activity_base = max(1, genome.activity_base + self.rng.choice((-1, 1)))
        elif mutation == "node":
            node = self.rng.choice(genome.nodes)
            if node.kind == "CONST" and self.rng.random() < 0.5:
                node.constant = i64((node.constant or 0) + self.rng.choice((-1, 1)))
            else:
                signature = PORTS[node.kind]
                choices = [kind for kind, ports in PORTS.items() if ports == signature and kind != node.kind]
                if choices:
                    node.kind = self.rng.choice(choices)
                    node.constant = 0 if node.kind == "CONST" else None
        else:
            edge_index = self.rng.randrange(len(genome.edges))
            edge = genome.edges[edge_index]
            if self.rng.random() < 0.5:
                candidates = [(n.id, p) for n in genome.nodes for p in PORTS[n.kind][1]]
                source, port = self.rng.choice(candidates)
                genome.edges[edge_index] = Edge(source, port, edge.target, edge.target_port)
            else:
                candidates = [(n.id, p) for n in genome.nodes for p in PORTS[n.kind][0]]
                target, port = self.rng.choice(candidates)
                genome.edges[edge_index] = Edge(edge.source, edge.source_port, target, port)

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
                    "alive": e.alive,
                    "energy": e.energy,
                    "born_at": e.born_at,
                    "parents": list(e.parents),
                    "partners": list(e.partner_ids),
                    "n_f": len(e.genome.nodes),
                    "n_p": e.genome.n_p,
                    "n_g": e.genome.n_g,
                    "activity_base": e.genome.activity_base,
                    "k_slots": len(e.k),
                    "z_used": sum(value is not None for value in e.z),
                    "z": [None if value is None else {"value": value.value, "sources": list(value.sources)} for value in e.z],
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
        return None if signal is None else {"value": signal.value, "sources": list(signal.sources)}

    def _entity_state(self, entity: Entity) -> dict[str, Any]:
        return {
            "id": entity.id, "energy": entity.energy, "born_at": entity.born_at,
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
        }

    @classmethod
    def from_checkpoint(cls, state: dict[str, Any]) -> "Simulation":
        if state.get("schema") != 1 or state.get("version") != cls.version:
            raise ValueError("Nicht unterstütztes Checkpoint-Format")
        sim = cls(Config(**state["config"]), ram=list(state["ram"]))
        sim.tick = state["tick"]
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
                id=raw["id"], genome=genome, energy=raw["energy"], born_at=raw["born_at"],
                parents=tuple(raw["parents"]), alive=raw["alive"],
                partner_ids=list(raw["partner_ids"]),
                k={key: Signal(item["value"], tuple(item["sources"])) for key, item in raw["k"].items()},
                z=[None if item is None else Signal(item["value"], tuple(item["sources"])) for item in raw["z"]],
                value_history=dict(raw["value_history"]), source_history=dict(raw["source_history"]),
            )
            sim.entities[entity.id] = entity
        sim.events.clear()
        return sim


def demo_genome(partner_id: int) -> Genome:
    nodes = [
        Node(1, "CONST", 1), Node(2, "CONST", 0), Node(3, "CONST", partner_id), Node(4, "MEM_WRITE"),
        Node(5, "CONST", 0), Node(6, "RAM_READ"), Node(7, "CONST", 0), Node(8, "Z_WRITE"),
    ]
    edges = [
        Edge(1, "value", 4, "offset"), Edge(2, "value", 4, "slot"), Edge(3, "value", 4, "value"),
        Edge(5, "value", 6, "address"), Edge(6, "value", 8, "value"), Edge(7, "value", 8, "address"),
    ]
    return Genome(nodes, edges, activity_base=32)
