import unittest
from pathlib import Path

from verify_mk3_input_finish_reference import verify, verify_rom

ROOT=Path(__file__).resolve().parent.parent
GOOD='audit_v265_mk3_final_input_reference_kano/run.log'


class OriginalInputReferenceTests(unittest.TestCase):
    def setUp(self):
        self.log=(ROOT/GOOD).read_text(encoding='utf-8-sig')

    def test_original_rom_rules(self):
        verify_rom((ROOT/'mk3/mk3-maincpu.bin').read_bytes())

    def test_actual_owned_input_reference(self):
        result=verify(self.log)
        self.assertTrue(result['passed'],result['errors'])
        self.assertEqual(result['accepted_input']['charge_fields'],80)
        self.assertEqual(result['accepted_input']['gap'],61)

    def test_cpu_controlled_attempt_is_rejected(self):
        log=(ROOT/'audit_v265_mk3_precharged_input_reference_kano/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log)['passed'])

    def test_missing_native_command_gate_is_rejected(self):
        log='\n'.join(line for line in self.log.splitlines() if 'a11=FF986380' not in line)
        self.assertFalse(verify(log)['passed'])

    def test_unqualified_charge_is_rejected(self):
        log='\n'.join(line.replace('a1=00000050','a1=0000003F') if 'at=FF992D50' in line else line for line in self.log.splitlines())
        self.assertFalse(verify(log)['passed'])

    def test_out_of_range_dispatch_is_rejected(self):
        log='\n'.join(line.replace('x=666,727','x=666,747') if 'at=FF993160' in line else line for line in self.log.splitlines())
        self.assertFalse(verify(log)['passed'])

    def test_position_assistance_is_rejected_even_with_good_gates(self):
        self.assertFalse(verify(self.log+'\nMK3_FATALITY_CLOSE_ASSIST frame=4498')['passed'])

    def test_old_round_actor_pointer_is_not_an_owner_proof(self):
        log='\n'.join(line for line in self.log.splitlines() if 'MK3_FATALITY_FINISH_OWNERS' not in line)
        self.assertFalse(verify(log)['passed'])


if __name__=='__main__':
    unittest.main()
