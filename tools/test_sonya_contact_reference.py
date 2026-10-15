import unittest
from pathlib import Path
from verify_sonya_contact_reference import verify,verify_rom

ROOT=Path(__file__).resolve().parents[1]


class SonyaContactReferenceTests(unittest.TestCase):
    def setUp(self):
        self.log=(ROOT/'audit_v266_original_sonya_native_contact/run.log').read_text(encoding='utf-8-sig')

    def test_original_rom_physics(self):
        verify_rom((ROOT/'mk3/mk3-maincpu.bin').read_bytes())

    def test_continuous_original_reference(self):
        result=verify(self.log)
        self.assertTrue(result['passed'],result['errors'])
        self.assertFalse(result['original_input_gate_validation_complete'])

    def test_missing_eighth_frame_fails(self):
        self.assertFalse(verify(self.log.replace('graphic=FFB26700','graphic=FFB26690'))['passed'])

    def test_changed_physics_fails(self):
        self.assertFalse(verify(self.log.replace('vx=00058000','vx=00060000'))['passed'])

    def test_wrong_child_fails(self):
        self.assertFalse(verify(self.log.replace('child=01036B70 x=745','child=01036750 x=745'))['passed'])

    def test_missing_contact_sample_fails(self):
        log='\n'.join(line for line in self.log.splitlines() if 'launch_age=59 ' not in line)
        self.assertFalse(verify(log)['passed'])

    def test_position_assistance_fails(self):
        self.assertFalse(verify(self.log+'\nMK3_FATALITY_CLOSE_ASSIST frame=4300')['passed'])


if __name__=='__main__':
    unittest.main()
