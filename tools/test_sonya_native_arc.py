import unittest
from pathlib import Path
from verify_sonya_native_arc import verify

ROOT=Path(__file__).resolve().parents[1]


class NativeSonyaArcTests(unittest.TestCase):
    def setUp(self):
        self.log=(ROOT/'audit_v269_arc_acceptance_sonya_side1_gap102/run.log').read_text(encoding='utf-8-sig')

    def test_actual_near_and_far_on_both_sides(self):
        for side,gap in ((1,65),(1,102),(2,65),(2,92)):
            log=(ROOT/f'audit_v269_arc_acceptance_sonya_side{side}_gap{gap}/run.log').read_text(encoding='utf-8-sig')
            result=verify(log,side)
            self.assertTrue(result['passed'],result['errors'])

    def test_actual_register_clobber_trial_is_rejected(self):
        log=(ROOT/'audit_v267_arc_first_sonya_side1_gap102/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log,1)['passed'])

    def test_actual_undrawn_final_point_trial_is_rejected(self):
        log=(ROOT/'audit_v268_arc_owned_sonya_side1_gap102/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(verify(log,1)['passed'])

    def test_changed_velocity_is_rejected(self):
        self.assertFalse(verify(self.log.replace('vx=00058000','vx=00060000'),1)['passed'])

    def test_missing_eighth_ascent_frame_is_rejected(self):
        self.assertFalse(verify(self.log.replace('child_graphic=FFFB1F00','child_graphic=FFFB1E00'),1)['passed'])

    def test_wrong_target_is_rejected(self):
        self.assertFalse(verify(self.log.replace('target_x=1098','target_x=1128'),1)['passed'])

    def test_missing_contact_publication_is_rejected(self):
        log='\n'.join(line for line in self.log.splitlines() if not ('MK2_SONYA_CONTACT_FRAME' in line and 'action_age=115 ' in line))
        self.assertFalse(verify(log,1)['passed'])

    def test_position_assistance_is_rejected(self):
        self.assertFalse(verify(self.log+'\nMK2_FINISH_POSITION_ASSIST applied',1)['passed'])


if __name__=='__main__':
    unittest.main()
