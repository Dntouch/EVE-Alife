import unittest
import json
import tempfile
from pathlib import Path

from eve_core import Config, Edge, Genome, Node, Signal, Simulation, amoeba_name, demo_genome, p1_explorer_genome
from run_stats import README_END, README_START, dashboard_data, publish_run_reports, update_readme_dashboard


class EveCoreTests(unittest.TestCase):
    def test_amoeba_names_are_unique_and_survive_checkpoint(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        self.assertEqual((a.name, b.name), ("Tom", "Erna"))
        self.assertEqual(Simulation.from_checkpoint(sim.checkpoint()).entities[1].name, "Tom")
        self.assertNotEqual(amoeba_name(1), amoeba_name(33))

    def test_dashboard_counts_extinction_offspring_energy_and_life_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "run-a"
            run.mkdir()
            (run / "metadata.json").write_text(json.dumps({
                "run_id": "run-a", "created_at": "2026-01-01T00:00:00+00:00", "seed": 1,
            }), encoding="utf-8")
            (run / "latest.json").write_text(json.dumps({
                "tick": 9, "entities": [
                    {"id": 1, "alive": False, "born_at": 0, "energy": 0, "n_g": 3, "n_f": 2, "n_p": 1},
                    {"id": 2, "alive": False, "born_at": 3, "energy": 0, "n_g": 5, "n_f": 3, "n_p": 2, "parents": [1, 3]},
                ],
            }), encoding="utf-8")
            events = [
                {"tick": 0, "kind": "birth", "entity_id": 1, "entity_name": "Tom", "parents": []},
                {"tick": 3, "kind": "birth", "entity_id": 2, "entity_name": "Erna", "parents": [1, 3]},
                {"tick": 4, "kind": "ram_read", "entity_id": 2, "address": 7, "reward": 12.5, "originators": [1]},
                {"tick": 5, "kind": "death", "entity_id": 2},
                {"tick": 9, "kind": "death", "entity_id": 1},
            ]
            (run / "events.jsonl").write_text(
                "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
            )
            result = dashboard_data(Path(temporary))
            self.assertEqual(result["mass_extinctions"], 1)
            self.assertEqual(result["offspring"], 1)
            self.assertEqual(result["energy_gained"], 12.5)
            self.assertEqual(result["shortest_life"]["name"], "Erna")
            self.assertEqual(result["longest_life"]["name"], "Tom")
            self.assertEqual(result["records"]["largest_genome"]["name"], "Erna")
            self.assertEqual(result["records"]["deepest_generation"]["value"], 1)
            self.assertEqual(result["records"]["most_ram_addresses"]["value"], 1)
            self.assertEqual(result["records"]["best_information_producer"]["name"], "Tom")
            readme = Path(temporary) / "README.md"
            readme.write_text("# Test\n\n## Bereiche\n\nText\n", encoding="utf-8")
            update_readme_dashboard(readme, Path(temporary))
            first = readme.read_text(encoding="utf-8")
            update_readme_dashboard(readme, Path(temporary))
            self.assertEqual(readme.read_text(encoding="utf-8"), first)
            self.assertEqual(first.count(README_START), 1)
            self.assertEqual(first.count(README_END), 1)
            self.assertIn("**12,50**", first)
            reports = Path(temporary) / "results"
            written = publish_run_reports(Path(temporary), reports)
            self.assertEqual(len(written), 2)
            self.assertIn("[1](Lauf_001.md)", (reports / "README.md").read_text(encoding="utf-8"))
            report = next(reports.glob("Lauf_*.md")).read_text(encoding="utf-8")
            self.assertIn("`run-a`", report)
            self.assertIn("12,50", report)

    def test_same_seed_is_deterministic(self):
        def run():
            sim = Simulation(Config(seed=7, ram_size=32))
            sim.add_entity(demo_genome(2), 100)
            sim.add_entity(demo_genome(1), 100)
            for _ in range(10): sim.heartbeat()
            return sim.checkpoint()
        self.assertEqual(run(), run())

    def test_aging_cost_increases_standby_without_fixed_expiry(self):
        sim = Simulation(Config(
            seed=1, ram_size=8, standby_cost=1, aging_cost_rate=0.25,
            genome_node_cost=0, genome_edge_cost=0,
            execution_cost=0, edge_cost=0,
        ))
        entity = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1), 20)
        entity.k["1:value"] = Signal(0, ("G",))
        sim.heartbeat()
        standby = next(event for event in sim.events if event["kind"] == "standby")
        self.assertEqual(standby["age"], 1)
        self.assertEqual(standby["aging_cost"], 0.25)
        self.assertEqual(standby["cost"], 1.25)
        self.assertTrue(entity.alive)

    def test_genome_maintenance_cost_grows_with_square_root(self):
        genome = Genome(
            [Node(1, "CONST", 1), Node(2, "PAUSE"),
             Node(3, "CONST", 3), Node(4, "CONST", 4)],
            [Edge(1, "value", 2, "value")],
            1,
        )
        sim = Simulation(Config(
            seed=1, ram_size=8, standby_cost=1, aging_cost_rate=0,
            genome_node_cost=0.5, genome_edge_cost=0.1,
        ))
        entity = sim.add_entity(genome, 20)
        sim.heartbeat()
        standby = next(event for event in sim.events if event["kind"] == "standby")
        self.assertAlmostEqual(standby["genome_cost"], 1.1)
        self.assertAlmostEqual(standby["cost"], 2.1)

    def test_k_overwrites_and_inputs_are_consumed(self):
        genome = Genome(
            [Node(1, "CONST", 1), Node(2, "CONST", 2), Node(3, "PAUSE")],
            [Edge(1, "value", 3, "value"), Edge(2, "value", 3, "value")], 10,
        )
        sim = Simulation(Config(seed=2, ram_size=8, standby_cost=0, execution_cost=0, edge_cost=0))
        entity = sim.add_entity(genome, 10)
        entity.k[EntityKey := "3:value"] = Signal(9, ("G",))
        sim._fire(entity, genome.nodes[2])
        self.assertNotIn(EntityKey, entity.k)

    def test_ram_change_rewards_and_returning_value_decreases(self):
        genome = Genome([Node(1, "RAM_READ")], [], 1)
        sim = Simulation(Config(seed=1, ram_size=8, standby_cost=0, execution_cost=0))
        entity = sim.add_entity(genome, 0)
        node = genome.nodes[0]
        rewards = []
        for value in (17, 42, 17, 17):
            sim.ram[0] = value
            before = entity.energy
            entity.k["1:address"] = Signal(0, ("G",))
            sim._fire(entity, node)
            rewards.append(entity.energy - before)
        self.assertEqual(rewards, [10, 10, 5, 0])

    def test_ram_writer_cannot_feed_itself_but_another_entity_can(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        writer = sim.add_entity(Genome([Node(1, "RAM_WRITE")], [], 1), 0)
        reader = sim.add_entity(Genome([Node(1, "RAM_READ")], [], 1), 0)
        writer.k["1:address"] = Signal(3, ("G",))
        writer.k["1:value"] = Signal(77, ("G",))
        sim._fire(writer, writer.genome.nodes[0])
        writer.k["1:address"] = Signal(3, ("G",))
        sim._fire(writer, Node(1, "RAM_READ"))
        reader.k["1:address"] = Signal(3, ("G",))
        sim._fire(reader, reader.genome.nodes[0])
        self.assertEqual(writer.energy, 0)
        self.assertEqual(reader.energy, sim.config.novelty_base)

    def test_birth_conserves_energy_and_clears_partners(self):
        sim = Simulation(Config(seed=3, ram_size=8, birth_energy=50, mutation_probability=0))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        a.energy = b.energy = 150
        a.partner_ids[0], b.partner_ids[0] = 2, 1
        before = a.energy + b.energy
        sim._reproduce()
        child = sim.entities[3]
        self.assertAlmostEqual(a.energy + b.energy + child.energy, before)
        self.assertEqual(a.partner_ids, [None, None])
        self.assertEqual(b.partner_ids, [None, None])
        self.assertEqual(child.parents, (1, 2))

    def test_fractional_birth_energy_uses_parent_mean_and_conserves_energy(self):
        sim = Simulation(Config(
            seed=3, ram_size=8, birth_energy_fraction=0.5,
            mutation_probability=0,
        ))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        a.energy, b.energy = 300, 500
        a.partner_ids[0], b.partner_ids[0] = 2, 1
        before = a.energy + b.energy
        sim._reproduce()
        child = sim.entities[3]
        self.assertEqual(child.energy, 200)
        self.assertEqual(a.energy, 200)
        self.assertEqual(b.energy, 400)
        self.assertEqual(a.energy + b.energy + child.energy, before)

    def test_birth_is_rejected_below_genome_heartbeat_minimum_without_cost(self):
        sim = Simulation(Config(
            seed=3, ram_size=8, birth_energy_fraction=0.5,
            birth_min_heartbeats=5, mutation_probability=0,
            genome_node_cost=10,
        ))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        a.partner_ids[0], b.partner_ids[0] = 2, 1
        sim._reproduce()
        self.assertNotIn(3, sim.entities)
        self.assertEqual((a.energy, b.energy), (100, 100))
        self.assertEqual((a.partner_ids, b.partner_ids), ([2, None], [1, None]))
        rejected = [event for event in sim.events if event["kind"] == "birth_rejected"]
        self.assertEqual(len(rejected), 2)
        self.assertGreater(rejected[0]["required_energy"], rejected[0]["offered_energy"])

    def test_birth_requires_each_parent_to_keep_more_than_own_start_energy(self):
        sim = Simulation(Config(seed=3, ram_size=8, birth_energy=50, mutation_probability=0))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        a.partner_ids[0], b.partner_ids[0] = 2, 1
        sim._reproduce()
        self.assertNotIn(3, sim.entities)
        self.assertEqual((a.energy, b.energy), (100, 100))
        rejected = [event for event in sim.events if event["kind"] == "birth_rejected"]
        self.assertEqual({event["reason"] for event in rejected}, {"parent_surplus_required"})

    def test_checkpoint_resumes_exactly(self):
        config = Config(seed=11, ram_size=16)
        sim = Simulation(config); sim.add_entity(demo_genome(2), 100); sim.add_entity(demo_genome(1), 100)
        for _ in range(3): sim.heartbeat()
        resumed = Simulation.from_checkpoint(sim.checkpoint())
        sim.events.clear()
        for _ in range(4): sim.heartbeat(); resumed.heartbeat()
        self.assertEqual(sim.checkpoint(), resumed.checkpoint())

    def test_foreign_membrane_is_read_only_in_shared_address_space(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        b.partner_ids[0] = a.id
        base = sim.config.membrane_base + (b.id - 1) * 3
        self.assertEqual(sim._decode_membrane_address(base)[0].id, b.id)
        self.assertEqual(sim._mem_read(b, 0, 0), b.id)
        self.assertEqual(sim._mem_read(b, 1, 0), a.id)

    def test_partner_id_must_come_from_a_living_foreign_membrane(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        finder = sim.add_entity(Genome([Node(1, "MEM_WRITE")], [], 1), 100)
        target = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1), 100)
        write = finder.genome.nodes[0]
        finder.k.update({
            "1:offset": Signal(1, ("G",)), "1:slot": Signal(0, ("G",)),
            "1:value": Signal(target.id, ("G",)),
        })
        sim._fire(finder, write)
        self.assertEqual(finder.partner_ids, [None, None])
        finder.k.update({
            "1:offset": Signal(1, ("G",)), "1:slot": Signal(0, ("G",)),
            "1:value": Signal(target.id, (f"MEM[{target.id},0,0]",)),
        })
        sim._fire(finder, write)
        self.assertEqual(finder.partner_ids, [target.id, None])

    def test_entity_and_invitation_discovery_reward_only_new_information(self):
        sim = Simulation(Config(
            seed=1, ram_size=8, entity_discovery_base=7,
            invitation_discovery_base=13,
        ))
        finder = sim.add_entity(Genome([Node(1, "RAM_READ")], [], 1), 0)
        target = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1), 0)
        read = finder.genome.nodes[0]
        identity_address = sim.config.membrane_base + (target.id - 1) * 3
        rewards = []
        for _ in range(2):
            before = finder.energy
            finder.k["1:address"] = Signal(identity_address, ("G",))
            sim._fire(finder, read)
            rewards.append(finder.energy - before)
        target.partner_ids[0] = finder.id
        invitation_address = identity_address + 1
        for _ in range(2):
            before = finder.energy
            finder.k["1:address"] = Signal(invitation_address, ("G",))
            sim._fire(finder, read)
            rewards.append(finder.energy - before)
        self.assertEqual(rewards, [7, 0, 13, 0])

    def test_recombination_keeps_connected_fragments_atomic(self):
        genome = Genome(
            [Node(1, "CONST", 111), Node(2, "PAUSE"), Node(3, "CONST", 222), Node(4, "PAUSE")],
            [Edge(1, "value", 2, "value"), Edge(3, "value", 4, "value")], 10,
        )
        sim = Simulation(Config(seed=9, ram_size=8, mutation_probability=0, genome_size_sigma=20))
        parents = [sim.add_entity(genome, 100), sim.add_entity(genome, 100)]
        for _ in range(25):
            child = sim._recombine(parents)
            by_id = {node.id: node for node in child.nodes}
            outgoing = {edge.source for edge in child.edges}
            for node in child.nodes:
                if node.kind == "CONST" and node.constant in {111, 222}:
                    self.assertIn(node.id, outgoing)
                    self.assertTrue(any(
                        edge.source == node.id and by_id[edge.target].kind == "PAUSE"
                        for edge in child.edges
                    ))

    def test_observation_exposes_read_only_entity_internals_for_lupe(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        entity = sim.add_entity(demo_genome(2), 100)
        entity.k["6:address"] = Signal(3, ("G",))
        entity.z[0] = Signal(17, ("RAM[3]",))
        observation = sim.observation()["entities"][0]
        self.assertEqual(observation["genome"]["nodes"][0]["kind"], "CONST")
        self.assertEqual(observation["genome"]["edges"][0]["source"], 1)
        self.assertEqual(observation["k"]["6:address"]["value"], 3)
        self.assertEqual(observation["z"][0]["sources"], ["RAM[3]"])

    def test_replay_events_describe_energy_and_node_execution(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        sim.add_entity(demo_genome(2), 100)
        sim.heartbeat()
        kinds = {event["kind"] for event in sim.events if event.get("entity_id") == 1}
        self.assertIn("standby", kinds)
        self.assertIn("node_fire", kinds)
        firing = next(event for event in sim.events if event["kind"] == "node_fire")
        self.assertIn("energy_before", firing)
        self.assertIn("energy_after", firing)
        self.assertIn("outputs", firing)

    def test_gate_only_forwards_on_nonzero_condition(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        entity = sim.add_entity(Genome([Node(1, "GATE")], [], 1), 10)
        node = entity.genome.nodes[0]
        for condition, expected in ((0, set()), (1, {"value"})):
            entity.k["1:value"] = Signal(23, ("RAM[2]",))
            entity.k["1:condition"] = Signal(condition, ("G",))
            self.assertEqual(set(sim._fire(entity, node)), expected)
        self.assertEqual([e["opened"] for e in sim.events if e["kind"] == "gate"], [False, True])

    def test_p1_explorer_reaches_multiple_ram_addresses(self):
        sim = Simulation(Config(seed=42, ram_size=256))
        sim.add_entity(p1_explorer_genome(2), 500)
        sim.add_entity(p1_explorer_genome(1), 500)
        for _ in range(60):
            sim.heartbeat()
        reads = {
            event["address"] for event in sim.events
            if event["kind"] == "ram_read" and event["entity_id"] == 1 and not event["virtual"]
        }
        self.assertGreater(len(reads), 1)
        self.assertIsNotNone(sim.entities[1].z[0])
        self.assertIsNotNone(sim.entities[1].z[1])

    def test_p1_dynamic_pairing_allows_children_to_have_children(self):
        sim = Simulation(Config(
            seed=42, ram_size=256, birth_energy=10, mutation_probability=0,
            standby_cost=0, aging_cost_rate=0,
            genome_node_cost=0, genome_edge_cost=0,
            execution_cost=0, edge_cost=0,
        ))
        for _ in range(4):
            entity = sim.add_entity(p1_explorer_genome(), 100)
            entity.energy = 200
        for _ in range(500):
            sim.heartbeat()
            if any(entity.parents == (3, 4) for entity in sim.entities.values()):
                break
        self.assertTrue(any(entity.parents == (3, 4) for entity in sim.entities.values()))


if __name__ == "__main__":
    unittest.main()
