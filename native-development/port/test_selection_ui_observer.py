from pathlib import Path
import unittest

class SelectionObserverTests(unittest.TestCase):
    def test_bounded_readonly_capture_and_object_guards(self):
        source=(Path(__file__).parent/'diagnostics/selection_ui_observer.lua').read_text()
        self.assertIn('frame<begin or frame>4500',source)
        self.assertIn('assert(begin==3000 or begin==3500)',source)
        self.assertIn('address+0x210>=0x01400000',source)
        self.assertIn('frame%4==0',source)
        self.assertIn('frame%10==0',source)
        for forbidden in (':write_u','set_value','.value='):
            self.assertNotIn(forbidden,source)

    def test_explicit_campaign_only_option(self):
        wrapper=(Path(__file__).parent.parent/'baseline/test_wolf_baseline.py').read_text()
        branch=wrapper.split("if '--selection-ui-observe' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert game_candidate and any(flag in sys.argv for flag in ('--campaign','--special'))",branch)
        self.assertIn('selection_ui_observer.lua',branch)
