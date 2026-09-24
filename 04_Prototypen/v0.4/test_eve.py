import unittest
import json
import tempfile
from pathlib import Path

from eve_core import AMOEBA_NAMES, Config, Edge, Genome, Node, Signal, Simulation, amoeba_name, demo_genome, p1_explorer_genome
from run_stats import README_END, README_START, dashboard_data, publish_run_reports, update_readme_dashboard


class EveCoreTests(unittest.TestCase):
    def test_edge_weight_scales_signal_and_preserves_provenance(self):
        signal = Signal(200, ("RAM[7]",), (3,))
        cases = {
            0: 200,
            1: 202,
            50: 300,
            -50: 100,
            -100: 0,
            -150: -100,
        }
        for weight, expected in cases.items():
            with self.subTest(weight=weight):
                transported = Simulation._transport_signal(signal, weight)
                self.assertEqual(transported.value, expected)
                self.assertEqual(transported.sources, signal.sources)
                self.assertEqual(transported.originators, signal.originators)
        self.assertEqual(Simulation._transport_signal(Signal(-101, ("G",)), 1).value, -102)

    def test_edge_weight_defaults_to_zero_and_survives_checkpoint(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        genome = Genome(
            [Node(1, "CONST", 20), Node(2, "PAUSE")],
            [Edge(1, "value", 2, "value", 25)], 1,
        )
        sim.add_entity(genome, 100)
        restored = Simulation.from_checkpoint(sim.checkpoint())
        self.assertEqual(restored.entities[1].genome.edges[0].weight, 25)
        self.assertEqual([node.segment for node in restored.entities[1].genome.nodes], [1, 2])
        self.assertEqual(Edge(1, "value", 2, "value").weight, 0)

    def test_weight_mutation_magnitude_uses_unbounded_inverse_square_draw(self):
        class Draws:
            def __init__(self):
                self.values = iter((0.75, 0.99, 0.4, 0.7, 0.2, 0.9, 0.3, 0.1))

            def random(self):
                return next(self.values)

        sim = Simulation(Config())
        sim.rng = Draws()
        self.assertEqual(sim._weight_mutation_magnitude(), 1)
        self.assertEqual(sim._weight_mutation_magnitude(), 2)
        self.assertEqual(sim._weight_mutation_magnitude(), 3)

    def test_weight_mutation_changes_one_edge_only_at_genome_creation(self):
        class MutationDraws:
            def __init__(self):
                self.random_values = iter((0.0, 0.75, 0.75, 0.25, 0.25))

            def random(self):
                return next(self.random_values)

            def choice(self, values):
                return "edge_weight"

            def randrange(self, stop):
                return 0

        genome = Genome(
            [Node(1, "CONST", 20), Node(2, "PAUSE")],
            [Edge(1, "value", 2, "value")], 1,
        )
        sim = Simulation(Config(mutation_probability=1.0))
        sim.rng = MutationDraws()
        mutation = sim._mutate(genome)
        self.assertEqual(mutation["class"], "edge_weight")
        self.assertEqual(mutation["delta"], 1)
        self.assertEqual(genome.edges[0].weight, 1)
        self.assertEqual(mutation["before"]["weight"], 0)
        self.assertEqual(mutation["after"]["weight"], 1)

    def test_amoeba_names_encode_generation_and_survive_checkpoint(self):
        self.assertEqual(len(AMOEBA_NAMES), 500)
        self.assertEqual(len(set(AMOEBA_NAMES)), 500)
        self.assertTrue({"Stefan", "Nova", "Sam", "Elena", "Sonja", "Milo", "EVE"} <= set(AMOEBA_NAMES))
        sim = Simulation(Config(seed=1, ram_size=8))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        self.assertEqual((a.name, b.name), ("Tom", "Erna"))
        child = sim.add_entity(demo_genome(2), 100, (a.id, b.id))
        grandchild = sim.add_entity(demo_genome(2), 100, (child.id,))
        self.assertEqual((child.name, child.generation), ("Ada 1", 1))
        self.assertEqual((grandchild.name, grandchild.generation), ("Bruno 2", 2))
        self.assertEqual(Simulation.from_checkpoint(sim.checkpoint()).entities[1].name, "Tom")
        resumed = Simulation.from_checkpoint(sim.checkpoint())
        self.assertEqual((resumed.entities[3].name, resumed.entities[3].generation), ("Ada 1", 1))
        self.assertEqual(amoeba_name(501, 4), "Tom 4")

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
                {"tick": 4, "kind": "ram_read", "entity_id": 2, "virtual": True, "reward": 10, "discovery_type": "entity"},
                {"tick": 4, "kind": "ram_read", "entity_id": 2, "virtual": True, "reward": 20, "discovery_type": "invitation"},
                {"tick": 4, "kind": "ram_read", "entity_id": 2, "virtual": True, "reward": 10, "discovery_type": "life_state", "value": 0},
                {"tick": 4, "kind": "ram_write", "entity_id": 2, "address": 2, "value": 2},
                {"tick": 5, "kind": "death", "entity_id": 2},
                {"tick": 9, "kind": "death", "entity_id": 1},
            ]
            (run / "events.jsonl").write_text(
                "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
            )
            result = dashboard_data(Path(temporary))
            self.assertEqual(result["mass_extinctions"], 1)
            self.assertEqual(result["offspring"], 1)
            self.assertEqual(result["energy_gained"], 52.5)
            self.assertEqual(result["history"][0]["death_discoveries"], 1)
            self.assertEqual(result["shortest_life"]["name"], "Erna")
            self.assertEqual(result["longest_life"]["name"], "Tom")
            self.assertEqual(result["records"]["largest_genome"]["name"], "Erna")
            self.assertEqual(result["records"]["deepest_generation"]["value"], 1)
            self.assertEqual(result["records"]["most_ram_addresses"]["value"], 1)
            self.assertEqual(result["records"]["best_information_producer"]["name"], "Tom")
            self.assertEqual(result["records"]["most_descendants"]["value"], 1)
            self.assertEqual(result["records"]["most_entity_discoveries"]["name"], "Erna")
            self.assertEqual(result["records"]["most_invitations"]["value"], 1)
            self.assertEqual(result["records"]["most_ram_writes"]["value"], 1)
            readme = Path(temporary) / "README.md"
            readme.write_text("# Test\n\n## Bereiche\n\nText\n", encoding="utf-8")
            update_readme_dashboard(readme, Path(temporary))
            first = readme.read_text(encoding="utf-8")
            update_readme_dashboard(readme, Path(temporary))
            self.assertEqual(readme.read_text(encoding="utf-8"), first)
            self.assertEqual(first.count(README_START), 1)
            self.assertEqual(first.count(README_END), 1)
            self.assertIn("**52,50**", first)
            reports = Path(temporary) / "results"
            written = publish_run_reports(Path(temporary), reports)
            self.assertEqual(len(written), 2)
            self.assertIn("[1](Lauf_001.md)", (reports / "README.md").read_text(encoding="utf-8"))
            report = next(reports.glob("Lauf_*.md")).read_text(encoding="utf-8")
            self.assertIn("`run-a`", report)
            self.assertIn("52,50", report)

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

    def test_external_bubble_changes_are_rewardable_and_persisted_as_events(self):
        sim = Simulation(Config(seed=1, ram_size=128, toy_bubbles=1))
        bubble = sim.environment_toys["bubbles"][0]
        address = bubble["address"]
        before = sim.ram[address]
        sim.tick = bubble["period"] - 1
        sim.heartbeat()
        self.assertNotEqual(sim.ram[address], before)
        event = next(event for event in sim.events if event["kind"] == "environment_change")
        self.assertEqual((event["toy_kind"], event["address"]), ("bubble", address))
        reader = sim.add_entity(Genome([Node(1, "RAM_READ")], [], 1), 0)
        reader.k["1:address"] = Signal(address, ("G",))
        sim._fire(reader, reader.genome.nodes[0])
        self.assertEqual(reader.energy, sim.config.novelty_base)

    def test_toy_habitats_cover_every_sector_without_following_entities(self):
        sim = Simulation(Config(seed=4, ram_size=4096, toy_habitats=8))
        self.assertEqual(len(sim.environment_toys["stones"]), 8)
        self.assertEqual(len(sim.environment_toys["bubbles"]), 16)
        self.assertEqual(len(sim.environment_toys["switches"]), 8)
        for index, stone in enumerate(sim.environment_toys["stones"]):
            self.assertLessEqual(index * 512, stone["start"])
            self.assertLess(stone["start"], (index + 1) * 512)

    def test_switch_preserves_trigger_origin_and_cannot_feed_its_writer(self):
        sim = Simulation(Config(seed=2, ram_size=128, toy_switches=1))
        switch = sim.environment_toys["switches"][0]
        writer = sim.add_entity(Genome([Node(1, "RAM_WRITE")], [], 1), 0)
        reader = sim.add_entity(Genome([Node(1, "RAM_READ")], [], 1), 0)
        writer.k["1:address"] = Signal(switch["trigger"], ("G",))
        writer.k["1:value"] = Signal(77, ("G",))
        sim._fire(writer, writer.genome.nodes[0])
        self.assertEqual(sim.ram_originators[switch["output"]], (writer.id,))
        writer.k["1:address"] = Signal(switch["output"], ("G",))
        sim._fire(writer, Node(1, "RAM_READ"))
        reader.k["1:address"] = Signal(switch["output"], ("G",))
        sim._fire(reader, reader.genome.nodes[0])
        self.assertEqual(writer.energy, 0)
        self.assertEqual(reader.energy, sim.config.novelty_base)

    def test_local_ram_coordinates_translate_offsets_around_entity_position(self):
        sim = Simulation(Config(seed=3, ram_size=16, local_ram_coordinates=True))
        genome = Genome([Node(1, "RAM_READ"), Node(2, "RAM_WRITE")], [], 1)
        entity = sim.add_entity(genome, 0, ram_position=10)
        sim.ram[13] = 77
        entity.k["1:address"] = Signal(3, ("G",))
        self.assertEqual(sim._fire(entity, genome.nodes[0])["value"].value, 77)
        entity.k["2:address"] = Signal(-2, ("G",))
        entity.k["2:value"] = Signal(91, ("G",))
        sim._fire(entity, genome.nodes[1])
        self.assertEqual(sim.ram[8], 91)
        events = [event for event in sim.events if event["kind"] in {"ram_read", "ram_write"}]
        self.assertEqual([(event["address_offset"], event["address"]) for event in events], [(3, 13), (-2, 8)])

    def test_child_is_born_at_a_parent_position_when_birth_radius_is_zero(self):
        sim = Simulation(Config(
            seed=3, ram_size=128, local_ram_coordinates=True, birth_position_radius=0,
            birth_energy=50, mutation_probability=0,
        ))
        first = sim.add_entity(demo_genome(2), 100, ram_position=11)
        second = sim.add_entity(demo_genome(1), 100, ram_position=99)
        first.energy = second.energy = 150
        first.partner_ids[0], second.partner_ids[0] = 2, 1
        sim._reproduce()
        self.assertIn(sim.entities[3].ram_position, {11, 99})

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

    def test_birth_requires_pooled_surplus_above_parent_start_energy(self):
        sim = Simulation(Config(seed=3, ram_size=8, birth_energy=50, mutation_probability=0))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        a.partner_ids[0], b.partner_ids[0] = 2, 1
        sim._reproduce()
        self.assertNotIn(3, sim.entities)
        self.assertEqual((a.energy, b.energy), (100, 100))
        rejected = [event for event in sim.events if event["kind"] == "birth_rejected"]
        self.assertEqual({event["reason"] for event in rejected}, {"parent_surplus_required"})

    def test_one_parent_can_fund_the_complete_birth_from_its_surplus(self):
        sim = Simulation(Config(seed=3, ram_size=8, birth_energy=50, mutation_probability=0))
        rich = sim.add_entity(demo_genome(2), 100)
        poor = sim.add_entity(demo_genome(1), 100)
        rich.energy = 400
        rich.partner_ids[0], poor.partner_ids[0] = 2, 1
        sim._reproduce()
        self.assertEqual(sim.entities[3].energy, 50)
        self.assertEqual((rich.energy, poor.energy), (350, 100))
        costs = [event for event in sim.events if event["kind"] == "reproduction_cost"]
        self.assertEqual([event["cost"] for event in costs], [50, 0])

    def test_checkpoint_resumes_exactly(self):
        config = Config(seed=11, ram_size=64, toy_stones=1, toy_bubbles=1, toy_switches=1)
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
        base = sim.config.membrane_base + (b.id - 1) * 4
        self.assertEqual(sim._decode_membrane_address(base)[0].id, b.id)
        self.assertEqual(sim._mem_read(b, 0, 0), b.id)
        self.assertEqual(sim._mem_read(b, 1, 0), a.id)
        self.assertEqual(sim._mem_read(b, 2, 0), 8)
        b.alive = False
        self.assertEqual(sim._mem_read(b, 2, 0), 0)

    def test_first_corpse_finder_receives_remaining_energy_and_removes_membrane(self):
        sim = Simulation(Config(
            seed=1, ram_size=8, life_state_discovery_base=99,
        ))
        finder = sim.add_entity(Genome([Node(1, "RAM_READ")], [], 1), 10)
        corpse = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1), 2)
        sim._kill(corpse, "test_death")
        vitality_address = sim.config.membrane_base + (corpse.id - 1) * 4 + 3
        finder.k["1:address"] = Signal(vitality_address, ("G",))
        result = sim._fire(finder, finder.genome.nodes[0])
        self.assertEqual(result["value"].value, 0)
        self.assertEqual(finder.energy, 12)
        self.assertEqual(corpse.energy, 0)
        self.assertFalse(corpse.corpse_available)
        self.assertIsNone(sim._decode_membrane_address(vitality_address))
        scavenged = [event for event in sim.events if event["kind"] == "corpse_scavenged"]
        self.assertEqual(len(scavenged), 1)
        self.assertEqual(scavenged[0]["reward"], 2)
        self.assertEqual(scavenged[0]["target_id"], corpse.id)
        self.assertIn(corpse.id, [item["id"] for item in sim.observation()["entities"]])

        finder.k["1:address"] = Signal(vitality_address, ("G",))
        sim._fire(finder, finder.genome.nodes[0])
        self.assertEqual(finder.energy, 12)
        self.assertEqual(len([event for event in sim.events if event["kind"] == "corpse_scavenged"]), 1)

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

    def test_knock_is_delivered_but_requires_genomic_reply(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        proposer = sim.add_entity(Genome([Node(1, "MEM_WRITE")], [], 1), 100)
        receiver = sim.add_entity(Genome(
            [Node(1, "MEM_READ"), Node(2, "MEM_WRITE")],
            [Edge(1, "value", 2, "value")], 1,
        ), 100)
        proposer.k.update({
            "1:offset": Signal(1, ("G",)), "1:slot": Signal(0, ("G",)),
            "1:value": Signal(receiver.id, (f"MEM[{receiver.id},0,0]",)),
        })
        sim._fire(proposer, proposer.genome.nodes[0])
        self.assertEqual(proposer.partner_ids[0], receiver.id)
        self.assertEqual(receiver.knocker_ids, [proposer.id])
        self.assertIsNone(receiver.partner_ids[0])

        receiver.k.update({
            "1:offset": Signal(3, ("G",)), "1:slot": Signal(0, ("G",)),
        })
        knock_signal = sim._fire(receiver, receiver.genome.nodes[0])["value"]
        receiver.k["2:value"] = knock_signal
        self.assertEqual(knock_signal.value, proposer.id)
        self.assertIn(f"KNOCK[{proposer.id}]", knock_signal.sources)
        receiver.k.update({
            "2:offset": Signal(1, ("G",)), "2:slot": Signal(0, ("G",)),
        })
        sim._fire(receiver, receiver.genome.nodes[1])
        self.assertEqual(receiver.partner_ids[0], proposer.id)
        self.assertIn((proposer.id, receiver.id), sim._valid_groups())

    def test_withdrawn_or_dead_knocker_is_no_longer_readable(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        proposer = sim.add_entity(demo_genome(2), 100)
        receiver = sim.add_entity(demo_genome(1), 100)
        proposer.partner_ids[0] = receiver.id
        receiver.knocker_ids = [proposer.id]
        self.assertEqual(sim._mem_read(receiver, 3, 0), proposer.id)
        proposer.partner_ids[0] = None
        self.assertEqual(sim._mem_read(receiver, 3, 0), 0)
        proposer.partner_ids[0] = receiver.id
        proposer.alive = False
        self.assertEqual(sim._mem_read(receiver, 3, 0), 0)

    def test_knock_capacity_keeps_distinct_proposers_in_fifo_order(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        proposers = [sim.add_entity(Genome([Node(1, "MEM_WRITE")], [], 1), 100) for _ in range(3)]
        receiver = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1, knock_capacity=2), 100)
        for proposer in proposers:
            proposer.k.update({
                "1:offset": Signal(1, ("G",)), "1:slot": Signal(0, ("G",)),
                "1:value": Signal(receiver.id, (f"MEM[{receiver.id},0,0]",)),
            })
            sim._fire(proposer, proposer.genome.nodes[0])
        self.assertEqual(receiver.knocker_ids, [proposers[1].id, proposers[2].id])
        self.assertEqual(sim._mem_read(receiver, 3, 0), proposers[1].id)
        self.assertEqual(sim._mem_read(receiver, 3, 1), proposers[2].id)

    def test_group_must_remain_mutual_for_heritable_bond_time(self):
        sim = Simulation(Config(
            seed=1, ram_size=8, birth_energy_fraction=0.1,
            birth_min_heartbeats=0, mutation_probability=0,
        ))
        genome = demo_genome(2)
        genome.bond_ticks = 3
        first = sim.add_entity(genome, 10_000)
        second = sim.add_entity(demo_genome(1), 10_000)
        second.genome.bond_ticks = 2
        first.start_energy = second.start_energy = 100
        first.partner_ids[0] = second.id
        second.partner_ids[0] = first.id
        sim._reproduce()
        sim._reproduce()
        self.assertEqual(len(sim.entities), 2)
        sim._reproduce()
        self.assertEqual(len(sim.entities), 3)
        self.assertEqual(sim.entities[3].parents, (1, 2))

    def test_three_mutual_partner_lists_form_a_reproductive_group(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        entities = [sim.add_entity(demo_genome(1), 100) for _ in range(3)]
        for entity in entities:
            entity.partner_ids = [other.id for other in entities if other.id != entity.id]
        self.assertEqual(sim._valid_groups(), [(1, 2, 3)])

    def test_partner_can_be_cleared_by_observed_death_or_genomic_withdrawal(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        finder = sim.add_entity(Genome([Node(1, "MEM_WRITE")], [], 1), 100)
        target = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1), 100)
        write = finder.genome.nodes[0]
        finder.partner_ids[0] = target.id
        for sources, expected in ((('RAM[0]',), target.id), (('G',), None)):
            finder.k.update({
                "1:offset": Signal(1, ("G",)), "1:slot": Signal(0, ("G",)),
                "1:value": Signal(0, sources),
            })
            sim._fire(finder, write)
            self.assertEqual(finder.partner_ids[0], expected)
        finder.partner_ids[0] = target.id
        target.alive = False
        finder.k.update({
            "1:offset": Signal(1, ("G",)), "1:slot": Signal(0, ("G",)),
            "1:value": Signal(0, (f"MEM[{target.id},2,0]",)),
        })
        sim._fire(finder, write)
        self.assertIsNone(finder.partner_ids[0])

    def test_entity_and_invitation_discovery_reward_only_new_information(self):
        sim = Simulation(Config(
            seed=1, ram_size=8, entity_discovery_base=7,
            invitation_discovery_base=13,
        ))
        finder = sim.add_entity(Genome([Node(1, "RAM_READ")], [], 1), 0)
        target = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1), 0)
        read = finder.genome.nodes[0]
        identity_address = sim.config.membrane_base + (target.id - 1) * 4
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

    def test_dead_life_state_becomes_single_use_corpse_instead_of_bonus_information(self):
        sim = Simulation(Config(
            seed=1, ram_size=8, life_state_discovery_base=11,
        ))
        finder = sim.add_entity(Genome([Node(1, "RAM_READ")], [], 1), 0)
        target = sim.add_entity(Genome([Node(1, "PAUSE")], [], 1), 0)
        read = finder.genome.nodes[0]
        status_address = sim.config.membrane_base + (target.id - 1) * 4 + 3
        rewards = []
        for index in range(4):
            if index == 2:
                sim._kill(target, "test_death")
            before = finder.energy
            finder.k["1:address"] = Signal(status_address, ("G",))
            sim._fire(finder, read)
            rewards.append(finder.energy - before)
        self.assertEqual(rewards, [11, 0, 0, 0])
        discoveries = [
            event for event in sim.events
            if event.get("discovery_type") == "life_state"
        ]
        self.assertEqual([event["value"] for event in discoveries], [1])
        scavenged = [event for event in sim.events if event["kind"] == "corpse_scavenged"]
        self.assertEqual(len(scavenged), 1)
        self.assertEqual(scavenged[0]["reward"], 0)

    def test_membrane_vitality_reaches_ten_only_above_reproductive_threshold(self):
        sim = Simulation(Config(
            seed=1, ram_size=8, birth_energy_fraction=0.5,
            birth_min_heartbeats=0,
        ))
        genome = Genome(
            [Node(1, "CONST", 1), Node(2, "CONST", 0), Node(3, "MEM_WRITE")],
            [Edge(1, "value", 3, "offset"), Edge(2, "value", 3, "slot"),
             Edge(1, "value", 3, "value")], 1,
        )
        entity = sim.add_entity(genome, 500)
        self.assertAlmostEqual(sim._reproductive_energy_threshold(entity), 500 / 0.75)
        self.assertEqual(sim._mem_read(entity, 2, 0), 7)
        entity.energy = 500 / 0.75
        self.assertEqual(sim._mem_read(entity, 2, 0), 9)
        entity.energy += 0.01
        self.assertEqual(sim._mem_read(entity, 2, 0), 10)
        entity.alive = False
        self.assertEqual(sim._mem_read(entity, 2, 0), 0)

    def test_membrane_vitality_without_operational_mem_write_is_capped_at_nine(self):
        sim = Simulation(Config(seed=1, ram_size=8, birth_energy_fraction=0.5, birth_min_heartbeats=0))
        incomplete = Genome([Node(1, "MEM_WRITE")], [], 1)
        entity = sim.add_entity(incomplete, 500)
        entity.energy = 10_000
        self.assertEqual(sim._mem_read(entity, 2, 0), 9)

    def test_recombination_inherits_one_homologous_allele_per_architecture_slot(self):
        left = Genome(
            [Node(1, "CONST", 111, 1), Node(2, "PAUSE", segment=1),
             Node(3, "CONST", 222, 2), Node(4, "PAUSE", segment=2)],
            [Edge(1, "value", 2, "value", 7), Edge(3, "value", 4, "value", -9)], 10,
        )
        right = Genome(
            [Node(1, "CONST", 333, 1), Node(2, "PAUSE", segment=1),
             Node(3, "CONST", 444, 2), Node(4, "PAUSE", segment=2)],
            [Edge(1, "value", 2, "value", 8), Edge(3, "value", 4, "value", -10)], 10,
        )
        sim = Simulation(Config(seed=9, ram_size=8, mutation_probability=0))
        parents = [sim.add_entity(left, 100), sim.add_entity(right, 100)]
        child = sim._recombine(parents)
        fragments = sim._last_genome_trace["inherited_fragments"]
        self.assertEqual(sim._last_genome_trace["selection_rule"], "homologous_slot_inheritance")
        self.assertIsNone(sim._last_genome_trace["target_n_g"])
        self.assertEqual(len(fragments), 2)
        self.assertEqual({node.segment for node in child.nodes}, {1, 2})
        self.assertEqual(child.n_g, left.n_g)
        self.assertTrue(all(fragment["homologous_matches"] for fragment in fragments))
        self.assertTrue(all(not fragment["trimmed"] for fragment in fragments))

    def test_cross_slot_edge_reconnects_semantically_when_alleles_come_from_different_parents(self):
        left = Genome(
            [Node(1, "GATE", segment=1), Node(2, "CONST", 9, 2)],
            [Edge(2, "value", 1, "condition", 17)], 4,
        )
        right = Genome(
            [Node(1, "GATE", segment=1), Node(2, "CONST", 10, 2)],
            [Edge(2, "value", 1, "condition", 19)], 4,
        )
        witnessed = False
        for seed in range(30):
            sim = Simulation(Config(seed=seed, mutation_probability=0))
            parents = [sim.add_entity(left, 100), sim.add_entity(right, 100)]
            child = sim._recombine(parents)
            repaired = [
                item for fragment in sim._last_genome_trace["inherited_fragments"]
                for item in fragment["edge_resolutions"] if item["status"] == "reconnected"
            ]
            if repaired:
                self.assertEqual(repaired[0]["match"], "exact")
                self.assertEqual(repaired[0]["resolved"]["target_port"], "condition")
                self.assertIn(repaired[0]["resolved"]["weight"], (17, 19))
                self.assertTrue(any(edge.target_port == "condition" for edge in child.edges))
                witnessed = True
                break
        self.assertTrue(witnessed)

    def test_p1_starts_with_three_unbounded_inheritance_slots(self):
        sim = Simulation(Config(
            seed=9, ram_size=8, mutation_probability=0, genome_size_sigma=2,
        ))
        parents = [
            sim.add_entity(p1_explorer_genome(), 500),
            sim.add_entity(p1_explorer_genome(), 500),
        ]
        for _ in range(40):
            child = sim._recombine(parents)
            self.assertEqual(sim._last_genome_trace["selection_rule"], "homologous_slot_inheritance")
            self.assertEqual(len({node.segment for node in child.nodes}), 3)
            self.assertIsNone(sim._last_genome_trace["target_n_g"])

    def test_all_four_slot_structure_mutations_are_reachable(self):
        seen = set()
        for seed in range(2000):
            genome = Genome(
                [Node(1, "CONST", 1, 1), Node(2, "PAUSE", segment=1),
                 Node(3, "CONST", 2, 2), Node(4, "PAUSE", segment=2)],
                [Edge(1, "value", 2, "value"), Edge(3, "value", 4, "value")], 4,
            )
            sim = Simulation(Config(seed=seed, mutation_probability=1))
            mutation = sim._mutate(genome)
            if mutation["class"].startswith("slot_"):
                seen.add(mutation["class"])
                genome.validate()
            if seen == {"slot_duplicate", "slot_delete", "slot_split", "slot_fuse"}:
                break
        self.assertEqual(seen, {"slot_duplicate", "slot_delete", "slot_split", "slot_fuse"})

    def test_observation_exposes_read_only_entity_internals_for_lupe(self):
        sim = Simulation(Config(seed=1, ram_size=8))
        entity = sim.add_entity(demo_genome(2), 100)
        entity.k["6:address"] = Signal(3, ("G",))
        entity.z[0] = Signal(17, ("RAM[3]",))
        observation = sim.observation()["entities"][0]
        self.assertEqual(observation["ram_position"], 0)
        self.assertEqual(observation["genome"]["nodes"][0]["kind"], "CONST")
        self.assertEqual(observation["genome"]["nodes"][0]["segment"], 1)
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

    def test_p1_partner_search_starts_near_own_id(self):
        sim = Simulation(Config(
            seed=42, ram_size=256, standby_cost=0, aging_cost_rate=0,
            genome_node_cost=0, genome_edge_cost=0,
        ))
        for _ in range(4):
            sim.add_entity(p1_explorer_genome(), 500)
        for _ in range(300):
            sim.heartbeat()
        first_find = {}
        for event in sim.events:
            if event["kind"] == "ram_read" and event.get("discovery_type") == "entity":
                first_find.setdefault(event["entity_id"], event["target_id"])
        self.assertIn(first_find[1], {2, 3, 4})
        self.assertEqual({key: first_find[key] for key in range(2, 5)}, {2: 1, 3: 2, 4: 3})
        self.assertEqual(first_find.get(5), 4)

    def test_p1_search_parameters_are_heritable_genome_constants(self):
        genome = p1_explorer_genome(
            search_offset=3, search_step=-2, search_patience=7, activity_base=103,
        )
        nodes = {node.id: node for node in genome.nodes}
        self.assertEqual(nodes[45].constant, 3)
        self.assertEqual(nodes[53].constant, -2)
        self.assertEqual(nodes[59].constant, 7)
        self.assertEqual(genome.activity_base, 103)
        self.assertTrue(any(node.kind == "MEM_WRITE" and node.id == 66 for node in genome.nodes))

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
