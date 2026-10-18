import unittest
from pathlib import Path

class NormalStrikeTraceTests(unittest.TestCase):
    def test_observer_is_passive_bounded_and_uses_supported_existing_hooks(self):
        port=Path(__file__).parent
        source=(port/'diagnostics/normal_strike_trace.lua').read_text()
        self.assertIn(':install_read_tap(',source)
        self.assertNotIn(':write_u',source)
        self.assertNotIn('register_stop',source)
        self.assertIn('count<=10000',source)
        self.assertIn('cpu.state[\'A8\'].value',source)
        self.assertNotRegex(source,r'\.value\s*=(?!=)')
        wrapper=(port.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("assert '--normal-moves' in sys.argv",wrapper)
        for name in ('qualify_normal_contact.py','inspect_normal_runtime.py'):
            self.assertIn("'Fatal error:' not in log",(port/name).read_text())
