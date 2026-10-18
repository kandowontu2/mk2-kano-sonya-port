"""Local integration checks of the actual26-chip verifier; no files mutated."""
from pathlib import Path
import json
import unittest
import zipfile
from verify_finisher_roms import verify

class RuntimeROMVerifier(unittest.TestCase):
    def check(self,corrupt=None):
        # Use the explicitly verified current runtime reference, not an old
        # hardcoded smoke run or a potentially lagging development package.
        port=Path(__file__).parent
        rebuilt=json.loads((port/'REBUILT_ROM_SET_QUALIFICATION.json').read_text())
        self.assertTrue(rebuilt['allRebuiltROMBytesMatchRuntimeInput'])
        name=rebuilt['runtimeReference']
        self.assertEqual(Path(name).name,name)
        path=port.parent/'baseline'/name/'roms/mk3.zip'
        with zipfile.ZipFile(path) as original:
            # A negative test must reject its mutation, not an unrelated
            # pre-existing stale program mismatch in the baseline archive.
            verify(original,{'testArguments':['--sound-candidate']})
            if corrupt is None:return
            class ArchiveView:
                def read(self,name):
                    data=original.read(name)
                    if name==corrupt:
                        data=bytes([data[0]^1])+data[1:]
                    return data
            verify(ArchiveView(),{'testArguments':['--sound-candidate']})

    def reject_corruption(self,name):
        # Validate outside assertRaises too: stale baseline data must fail the
        # negative test rather than masquerade as the intended corruption.
        self.check()
        with self.assertRaises(AssertionError):self.check(name)

    def test_actual_current_all26_chips(self): self.check()
    def test_corrupt_program_rejected(self):
        self.reject_corruption('mk321u54.bin')
    def test_corrupt_sound_rejected(self):
        self.reject_corruption('l1_mortal_kombat_3_u2_music_spch.u2')
    def test_corrupt_original_graphics_rejected(self):
        self.reject_corruption('l1_mortal_kombat_3_u133_game_rom.u133')
    def test_corrupt_added_graphics_rejected(self):
        self.reject_corruption('l1_mortal_kombat_3_u114_game_rom.u114')

if __name__=='__main__': unittest.main()
