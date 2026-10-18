from pathlib import Path
import unittest


class NormalSoakTests(unittest.TestCase):
    def test_opt_in_is_bounded_and_uses_only_physical_controls(self):
        here = Path(__file__).parent
        source = (here / 'diagnostics/normal_probe.lua').read_text()
        self.assertIn("KS_NORMAL_SOAK", source)
        self.assertIn('soak and n>=24000', source)
        self.assertIn('index=(index-1)%#cases+1', source)
        self.assertIn('mode==4 and previousMode~=4', source)
        self.assertIn('word(navigation[direction]+item[1]*16)', source)
        self.assertIn("navigate(c1,target1,'P1 ')", source)
        self.assertNotIn(':write_u', source)
        wrapper = (here.parent / 'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--normal-soak' in sys.argv: guest_limit='600'", wrapper)
        self.assertIn("if '--normal-soak' in sys.argv: wall_limit=120", wrapper)


if __name__ == '__main__':
    unittest.main()
