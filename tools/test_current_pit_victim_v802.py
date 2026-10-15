"""Current Pit native-state/owner/voice corruption tests; no capture edits."""
from pathlib import Path
import re
import unittest
import verify_current_pit_victim_regression_v801 as verify

ROOT = Path(__file__).resolve().parents[1]

class PitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs = {(fighter, side): (ROOT/name/'run.log').read_text(encoding='utf-8-sig')
                    for fighter, side, name in (('kano', 1, 'audit_v799_kano_pit_audio_p1'),
                                                ('sonya', 2, 'audit_v799_sonya_pit_audio_p2'))}
        cls.original = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()

    def changed(self, log, tag, key, value, condition=lambda row: True):
        lines = log.splitlines()
        for index, line in enumerate(lines):
            if not line.startswith('MK2_NAT_CAMPAIGN_' + tag + ' '):continue
            row = dict(re.findall(r'(\w+)=([^\s]+)', line))
            if condition(row):
                lines[index] = re.sub(r'\b' + key + r'=[^\s]+', key+'='+value, line, count=1)
                return '\n'.join(lines)
        self.fail('Mutation target not present: ' + tag + ':' + key)

    def test_both_current_native_baselines(self):
        for (fighter, side), log in self.logs.items():
            proof = verify.scene.verify_log(log, fighter, side=side)
            self.assertEqual(proof['terminal_frame'], 49237)
            verify.impact_commands(log, proof, self.original)

    def test_current_state_phase_identity_and_continue_mutations(self):
        for (fighter, side), log in self.logs.items():
            edits = (
                ('actual proxy victim', 'PIT_LOOKUP', 'id', '1', lambda r: True),
                ('wrong physical cache', 'DRAW', 'cache', '0105ED30' if side == 2 else '0105F230', lambda r: r['entry'] == 'FF838790'),
                ('wrong scene owner', 'PIT_LOOKUP', 'a8', '01000000', lambda r: True),
                ('missing true source', 'COMPONENT', 'value', 'FF184000' if fighter == 'sonya' else 'FF184300', lambda r: True),
                ('wrong native dispatch', 'PIT_LOOKUP', 'pc', 'FF80DE20', lambda r: True),
                ('wrong centered origin', 'DRAW', 'x', '191', lambda r: r['entry'] == 'FF838790' and r['x'] == '192'),
                ('wrong exit mode', 'PIT_EXIT', 'mode', '3', lambda r: True),
                ('wrong continued own ID', 'FIGHT', 'human', '1:1', lambda r: int(r['frame']) > int(verify.scene.rows(log, 'PIT_EXIT')[0]['frame'])),
                ('reset', 'RESULT', 'reset', '40000', lambda r: True),
                ('ending mislabeled clear', 'RESULT', 'ending', '40000', lambda r: True),
            )
            for label, tag, key, value, condition in edits:
                with self.subTest(fighter=fighter, label=label):
                    altered = self.changed(log, tag, key, value, condition)
                    with self.assertRaises(ValueError):verify.scene.verify_log(altered, fighter, side=side)

    def test_native_initial_preload_cannot_be_omitted(self):
        for (fighter, side), log in self.logs.items():
            enter = verify.scene.rows(log, 'PIT_LOOKUP')[0]['frame']
            altered = '\n'.join(line for line in log.splitlines()
                if not(line.startswith('MK2_NAT_CAMPAIGN_DRAW ') and 'entry=FF838790 ' in line and 'frame='+enter+' ' in line))
            with self.assertRaises(ValueError):verify.scene.verify_log(altered, fighter, side=side)

    def test_native_voice_command_owner_byte_and_gender(self):
        for (fighter, side), log in self.logs.items():
            proof = verify.scene.verify_log(log, fighter, side=side)
            impact, actor = str(proof['pit_impact']), f'{proof["episodes"][0]["actor"]:08X}'
            for key, value in (('data', 'FF00'), ('mask', '00FF'), ('pc', 'FF80DE20'), ('a8', '01000000'), ('a13', '01000000')):
                with self.subTest(fighter=fighter, field=key):
                    lines = log.splitlines()
                    index = next(i for i, line in enumerate(lines) if line.startswith('MK2_PIT_DISPLAY_SOUND ')
                                 and 'frame='+impact+' ' in line and 'a8='+actor+' ' in line)
                    lines[index] = re.sub(r'\b'+key+r'=[^\s]+', key+'='+value, lines[index], count=1)
                    with self.assertRaises(ValueError):verify.impact_commands('\n'.join(lines), proof, self.original)

    def test_paid_continue_buttons_cannot_be_removed(self):
        for (fighter, side), log in self.logs.items():
            for button in ('Coin', 'Start'):
                with self.subTest(fighter=fighter, button=button):
                    altered = '\n'.join(line for line in log.splitlines() if not(
                        line.startswith('MK2_NAT_CAMPAIGN_INPUT ') and 'button='+button+' ' in line))
                    with self.assertRaises(ValueError):verify.scene.verify_log(altered, fighter, side=side)

if __name__ == '__main__':
    unittest.main(verbosity=2)
