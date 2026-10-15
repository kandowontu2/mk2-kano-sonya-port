import re
import unittest
from pathlib import Path
from verify_unassisted_finish import verify

ROOT=Path(__file__).resolve().parents[1]


class NativeUnassistedFinishTests(unittest.TestCase):
    def setUp(self):
        self.kano=(ROOT/'audit_v273_unassisted_kano_sonya/run.log').read_text(encoding='utf-8-sig')
        self.sonya=(ROOT/'audit_v273_unassisted_sonya_kano/run.log').read_text(encoding='utf-8-sig')

    def test_actual_both_native_finishes(self):
        for fighter,victim,log in (('kano','sonya',self.kano),('sonya','kano',self.sonya)):
            result=verify(log,fighter,victim)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual(result['total_native_damage'],322)

    def test_wrong_native_writer_rejected(self):
        self.assertFalse(verify(self.kano.replace('pc=FF836700','pc=FF807F80',1),'kano','sonya')['passed'])

    def test_missing_damage_event_rejected(self):
        log=re.sub(r'^MK2_UNASSISTED_DAMAGE[^\r\n]*\r?\n','',self.kano,count=1,flags=re.M)
        self.assertFalse(verify(log,'kano','sonya')['passed'])

    def test_health_reset_without_native_constructor_rejected(self):
        log=re.sub(r'^MK2KS_NATIVE_P2_HUD[^\r\n]*\r?\n','',self.kano,flags=re.M)
        self.assertFalse(verify(log,'kano','sonya')['passed'])

    def test_wrong_victim_rejected(self):
        self.assertFalse(verify(self.kano,'kano','sub_zero')['passed'])

    def test_wrong_fatality_owner_rejected(self):
        log=self.kano.replace('fighter=kano side=1 actor=','fighter=kano side=2 actor=',1)
        self.assertFalse(verify(log,'kano','sonya')['passed'])

    def test_wrong_range_rejected(self):
        log=re.sub(r'(MK2_RANGE_GATE[^\r\n]* distance=)\d+',r'\g<1>81',self.kano,count=1)
        self.assertFalse(verify(log,'kano','sonya')['passed'])

    def test_position_assistance_rejected(self):
        self.assertFalse(verify(self.kano+'\nMK2_FINISH_POSITION_ASSIST','kano','sonya')['passed'])

    def test_false_totals_rejected(self):
        self.assertFalse(verify(self.kano.replace('total_damage=322','total_damage=323'),'kano','sonya')['passed'])


if __name__=='__main__': unittest.main()
