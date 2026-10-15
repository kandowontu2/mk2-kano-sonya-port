"""The shared real-input driver must release the same controls for both sides."""
from pathlib import Path
import re
import unittest


class SelectorInputDriverTests(unittest.TestCase):
    def test_both_players_have_all_combat_fields_in_the_clear_list(self):
        source = (Path(__file__).resolve().parent.parent / "mk2ks_selector_exit_test.lua").read_text()
        start = source.index("        fields = {")
        end = source.index("        screen =", start)
        setup = source[start:end]
        expected = {"High Punch", "High Kick", "Block", "Low Punch", "Low Kick", "Block 2",
                    "Left", "Right", "Up", "Down"}
        for side in (1, 2):
            with self.subTest(side=side):
                controls = set(re.findall(rf'(?:high|low)\["P{side} ([^"]+)"\]', setup))
                self.assertEqual(controls, expected)
        self.assertIn("for _, field in pairs(fields) do field:clear_value() end", source)


if __name__ == "__main__":
    unittest.main()
