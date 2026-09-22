from __future__ import annotations

import unittest

from run_parameters import PARAMETERS, PRESETS
from supervisor import command_for, validate


class SupervisorTests(unittest.TestCase):
    def test_every_parameter_has_a_description(self) -> None:
        self.assertTrue(PARAMETERS)
        for name, spec in PARAMETERS.items():
            self.assertTrue(spec.get("label"), name)
            self.assertTrue(spec.get("description"), name)

    def test_builtin_presets_are_complete_and_valid(self) -> None:
        for key, preset in PRESETS.items():
            with self.subTest(key=key):
                clean = validate(preset["values"])
                self.assertEqual(set(clean), set(PARAMETERS))

    def test_open_command_has_no_tick_limit_or_shell(self) -> None:
        values = validate({**PRESETS["open-observation"]["values"], "label": "Test"})
        command = command_for("00000000-0000-0000-0000-000000000001", values)
        self.assertIn("--open", command)
        self.assertNotIn("--ticks", command)
        self.assertIsInstance(command, list)

    def test_population_must_be_even(self) -> None:
        with self.assertRaisesRegex(ValueError, "gerade"):
            validate({**PRESETS["v03-standard"]["values"], "population": 3})


if __name__ == "__main__":
    unittest.main()
