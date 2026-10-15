"""Current-candidate Babality runtime/pixel corruption tests, in memory only."""
import copy
import json
from pathlib import Path
import unittest
import numpy as np
from PIL import Image
import verify_native_babality_performers_v739 as own

ROOT = Path(__file__).resolve().parents[1]
v = own.v

class CurrentBabalityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = json.loads((ROOT / 'audit_v726_original_baby_reference/reference.json').read_text())
        cls.rows = v.records((ROOT / 'audit_v793_kano_babality_p1/run.log').read_text(encoding='utf-8-sig'))

    def positive(self, rows):
        v.runtime_check(rows, 'sonya', 1, self.reference, winner_id=17)
        own.command_check(rows, 'kano', 1, 'positive')

    def test_all_ten_current_runtime_baselines(self):
        cases = [(winner, victim, f'{winner}_babality', side, 'positive')
                 for winner, victim in (('kano', 'sonya'), ('sonya', 'kano')) for side in (1, 2)]
        cases += [(winner, victim, f'{winner}_wrong', 1, 'wrong_direction')
                  for winner, victim in (('kano', 'sonya'), ('sonya', 'kano'))]
        cases += [(winner, victim, f'{winner}_punch', 2, 'punch_used')
                  for winner, victim in (('kano', 'sonya'), ('sonya', 'kano'))]
        cases += [('kitana', 'liu_kang', 'stock_liu', side, 'positive') for side in (1, 2)]
        for winner, victim, label, side, command in cases:
            with self.subTest(winner=winner, side=side, command=command):
                rows = v.records((ROOT / f'audit_v793_{label}_p{side}/run.log').read_text(encoding='utf-8-sig'))
                if command == 'positive':
                    v.runtime_check(rows, victim, side, self.reference, winner_id=own.WINNERS[winner])
                    own.command_check(rows, winner, side, command)
                else:
                    own.negative_check(rows, winner, victim, side, command)

    def test_current_positive_corruptions_rejected(self):
        edits = (
            ('unearned rounds', 'RESULT', 'wins', '1', lambda r: True),
            ('assistance', 'RESULT', 'writes', '1', lambda r: True),
            ('winner proxy', 'SELECT_ID', 'actual', '1', lambda r: r['slot'] == '1'),
            ('victim proxy', 'SELECT_ID', 'actual', '1', lambda r: r['slot'] == '2'),
            ('non-native damage', 'DAMAGE', 'pc', 'FF80DE20', lambda r: True),
            ('punch eligibility', 'FINISH_WINDOW', 'hp_counters', '1,0', lambda r: True),
            ('wrong infant', 'CONSTRUCT', 'frame_pointer', 'FFB1C960', lambda r: True),
            ('wrong victim ID', 'CONSTRUCT', 'victim_id', '1', lambda r: True),
            ('wrong lookup', 'LOOKUP', 'value', '002C', lambda r: True),
            ('wrong lookup ID', 'LOOKUP', 'live_id', '1', lambda r: True),
            ('wrong owner', 'FIELD', 'owner', '01031D10', lambda r: r['age'] == '0' and r['slot'] == '1'),
            ('lost ID', 'FIELD', 'id', '1', lambda r: r['age'] == '144' and r['slot'] == '2'),
            ('floor shifted', 'BABY', 'y', '173', lambda r: r['age'] == '160'),
            ('wrong palette', 'BABY', 'colors', 'FFFF,' + ','.join(v.entries(self.rows, 'BABY')[0]['colors'].split(',')[1:]), lambda r: r['age'] == '160'),
            ('wrong retirement', 'RETIRE', 'pc', 'FF80DE20', lambda r: r['entry'] == '01060220'),
            ('wrong case', 'RESULT', 'case', 'wrong_direction', lambda r: True),
            ('wrong activation', 'RESULT', 'action', str(int(v.entries(self.rows, 'RESULT')[0]['action']) + 1), lambda r: True),
        )
        for label, tag, key, value, predicate in edits:
            with self.subTest(label=label):
                changed = copy.deepcopy(self.rows)
                next(r for t, r in changed if t == tag and predicate(r))[key] = value
                with self.assertRaises(ValueError):
                    self.positive(changed)

    def test_missing_native_handoff_and_cleanup_rejected(self):
        edits = (
            ('action', 'ENTRY', lambda r: r['entry'] == 'FF87E520'),
            ('half retirement', 'RETIRE', lambda r: r['entry'] == '01060230'),
            ('object reuse', 'BABY_REUSED', lambda r: True),
            ('first command direction', 'INPUT', lambda r: r['button'] == 'Right' and int(r['frame']) == int(v.entries(self.rows, 'RESULT')[0]['window']) + 20),
        )
        for label, tag, predicate in edits:
            with self.subTest(label=label):
                changed = [(t, r) for t, r in self.rows if not(t == tag and predicate(r))]
                with self.assertRaises(ValueError):
                    self.positive(changed)

    def test_watchdog_reboot_rejected(self):
        with self.assertRaises(ValueError):
            self.positive(self.rows + [('BOOT', copy.deepcopy(v.entries(self.rows, 'BOOT')[0]))])

    def test_current_exact_original_pixels_and_one_pixel_corruption(self):
        sprite = np.asarray(Image.open(ROOT / 'audit_v726_original_baby_reference/sonya_baby.png').convert('RGBA'))
        actual = np.asarray(Image.open(ROOT / 'audit_v793_kano_babality_p1/snap/babality_160.png').convert('RGB'))
        (x, y), count = v.image_match(actual, sprite)
        self.assertEqual(count, 961)
        yy, xx = np.argwhere(sprite[:, :, 3] != 0)[0]
        altered = actual.copy(); altered[y + yy, x + xx, 0] ^= 1
        with self.assertRaises(ValueError):
            v.image_match(altered, sprite)

    def test_negative_action_or_proxy_rejected(self):
        for label, winner, victim, side, command in (
            ('kano_wrong', 'kano', 'sonya', 1, 'wrong_direction'),
            ('sonya_punch', 'sonya', 'kano', 2, 'punch_used'),
        ):
            rows = v.records((ROOT / f'audit_v793_{label}_p{side}/run.log').read_text(encoding='utf-8-sig'))
            for tag, key, value in (('RESULT', 'action', '1'), ('SELECT_ID', 'actual', '1')):
                with self.subTest(label=label, tag=tag):
                    changed = copy.deepcopy(rows)
                    next(r for t, r in changed if t == tag)[key] = value
                    with self.assertRaises(ValueError):
                        own.negative_check(changed, winner, victim, side, command)

    def test_proof_does_not_claim_full_port(self):
        proof = json.loads((ROOT / 'audit_v794_current_babality_regression_checked/verification.json').read_text())
        self.assertTrue(proof['boundedCurrentHumanBabalityRegressionAcceptance'])
        self.assertFalse(proof['fullFinisherAcceptance'])
        self.assertFalse(proof['fullPortAcceptance'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
