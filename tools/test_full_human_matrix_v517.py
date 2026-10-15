"""Reject altered fresh v517 records using the same case contracts as the audit."""
import re
import unittest
import verify_full_human_matrix_v517 as audit

class FreshMatrix(unittest.TestCase):
    def log(self, name):
        return (audit.ROOT / ('audit_v523_' + name) / 'run.log').read_text(encoding='utf-8-sig')

    def reject(self, log, move, side, scenario=None, air=False):
        with self.assertRaises(ValueError):
            audit.check_case(log, move, side, scenario, air)

    def test_missing_field(self):
        log = self.log('positive_ring_p1')
        altered = re.sub(r'^MK2_HSPECIAL_FIELD[^\n]+\n', '', log, count=1, flags=re.M)
        self.assertNotEqual(log, altered)
        self.reject(altered, 'ring', 1)

    def test_wrong_identity(self):
        log = self.log('positive_ring_p2')
        altered = log.replace('id=18', 'id=1', 1)
        self.assertNotEqual(log, altered)
        self.reject(altered, 'ring', 2)

    def test_missing_native_entry(self):
        log = self.log('positive_blade_p1')
        altered = re.sub(r'^MK2_HSPECIAL_EVENT[^\n]*entry=FFF8CC00[^\n]+\n', '', log, flags=re.M)
        self.assertNotEqual(log, altered)
        self.reject(altered, 'blade', 1)

    def test_missing_health_store(self):
        log = self.log('positive_leg_p2')
        altered = re.sub(r'^MK2_HSPECIAL_HEALTH[^\n]+\n', '', log, flags=re.M)
        self.assertNotEqual(log, altered)
        self.reject(altered, 'leg', 2)

    def test_ball_forward_rebound(self):
        log = self.log('negative_ball_block_p1')
        altered = re.sub(r'(MK2_HSPECIAL_FIELD[^\n]*slot=1[^\n]*vx=)[0-9A-F]+([^\n]*action=1538)',
                         r'\g<1>000A0000\2', log)
        self.assertNotEqual(log, altered)
        self.reject(altered, 'ball', 1, 'block')

    def test_ball_missing_geometry(self):
        log = self.log('negative_ball_miss_p2')
        altered = re.sub(r'^MK2_HSPECIAL_GEOMETRY[^\n]+\n', '', log, count=1, flags=re.M)
        self.assertNotEqual(log, altered)
        self.reject(altered, 'ball', 2, 'miss')

    def test_ground_square_not_air_contact(self):
        self.reject(self.log('positive_square_p1'), 'square', 1, air=True)

    def test_leg_standing_block_not_duck_block(self):
        self.reject(self.log('negative_leg_block_p2'), 'leg', 2, 'duck_block')

if __name__ == '__main__': unittest.main()
