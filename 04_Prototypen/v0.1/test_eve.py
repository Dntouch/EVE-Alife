import unittest

from eve_core import Config, Edge, Genome, Node, Signal, Simulation, demo_genome


class EveCoreTests(unittest.TestCase):
    def test_same_seed_is_deterministic(self):
        def run():
            sim = Simulation(Config(seed=7, ram_size=32))
            sim.add_entity(demo_genome(2), 100)
            sim.add_entity(demo_genome(1), 100)
            for _ in range(10): sim.heartbeat()
            return sim.checkpoint()
        self.assertEqual(run(), run())

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

    def test_repeat_reward_decreases(self):
        genome = Genome([Node(1, "Z_WRITE")], [], 1)
        sim = Simulation(Config(seed=1, ram_size=8, standby_cost=0, execution_cost=0))
        entity = sim.add_entity(genome, 0)
        node = genome.nodes[0]
        rewards = []
        for _ in range(2):
            before = entity.energy
            entity.k["1:address"] = Signal(0, ("G",))
            entity.k["1:value"] = Signal(5, ("RAM[1]",))
            sim._fire(entity, node)
            rewards.append(entity.energy - before)
        self.assertGreater(rewards[0], rewards[1])

    def test_birth_conserves_energy_and_clears_partners(self):
        sim = Simulation(Config(seed=3, ram_size=8, birth_energy=50, mutation_probability=0))
        a = sim.add_entity(demo_genome(2), 100)
        b = sim.add_entity(demo_genome(1), 100)
        a.partner_ids[0], b.partner_ids[0] = 2, 1
        before = a.energy + b.energy
        sim._reproduce()
        child = sim.entities[3]
        self.assertAlmostEqual(a.energy + b.energy + child.energy, before)
        self.assertEqual(a.partner_ids, [None, None])
        self.assertEqual(b.partner_ids, [None, None])
        self.assertEqual(child.parents, (1, 2))

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


if __name__ == "__main__":
    unittest.main()
