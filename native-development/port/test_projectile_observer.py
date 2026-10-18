"""Passive observer source/ABI contracts, not projectile threat correctness."""
from pathlib import Path
import re
import unittest

PORT=Path(__file__).parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'

class ProjectileObserver(unittest.TestCase):
    def test_native_process_and_object_offsets(self):
        for file,name,value in [('MAINEQU.ASM','procid',0x20),('MAINEQU.ASM','pa8',0xc0),
                                ('DISPEQU.ASM','oxvel',0x40)]:
            match=re.search(r'^'+name+r'\s+\.set\s+([0-9a-f]+)h', (SRC/file).read_text(),re.M|re.I)
            self.assertIsNotNone(match)
            self.assertEqual(int(match[1],16),value)
        native=(SRC/'MKZAP.ASM').read_text()
        helper=native.split('\nspawn_proj_proc\n',1)[1].split('\np1p2_proj_pids\n',1)[0]
        self.assertIn('move\ta10,*a0(pa8),l',helper)

    def test_observer_is_bounded_and_passive(self):
        source=(PORT/'diagnostics/liu_projectile_observer.lua').read_text()
        self.assertIn('not seen[cursor] and count<512',source)
        self.assertIn('if not valid(own) or not valid(enemy)',source)
        self.assertIn('local good=valid(object)',source)
        self.assertNotIn('set_value',source)
        self.assertNotIn(':write_u',source)
        self.assertIsNone(re.search(r'\.value\s*=(?!=)',source))

    def test_wrapper_freezes_observer_in_scoped_run(self):
        wrapper=(PORT.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-projectile-observe' in sys.argv:",wrapper)
        self.assertIn("assert '--campaign' in sys.argv and game_candidate and '--sonya' not in sys.argv",wrapper)
        self.assertIn("'port/diagnostics/liu_projectile_observer.lua'",wrapper)

if __name__=='__main__': unittest.main()
