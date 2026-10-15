"""Real human-command traces plus fail-closed mutations; no invented successes."""
import re
import unittest
from pathlib import Path
import verify_human_shang as check

ROOT=Path(__file__).resolve().parents[1]


def cases():
    for side in (1,2):
        for target in ('kano','sonya'):
            yield f'audit_v349_human_{target}_p{side}',target,side,'native'
            for profile in sorted(check.NEGATIVE[target]):
                yield f'audit_v348_human_{target}_p{side}_{profile}',target,side,profile
        for profile in ('block2','block_first','lp_first'):
            yield f'audit_v349_human_sonya_p{side}_{profile}','sonya',side,profile
        for profile in check.STOCK:
            yield f'audit_v350_human_p{side}_{profile}','kano' if profile=='stock_lk' else 'sonya',side,profile


class HumanCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log=(ROOT/'audit_v349_human_sonya_p2/run.log').read_text(encoding='utf-8-sig')
        cls.bad=(ROOT/'audit_v348_human_sonya_p2_airborne/run.log').read_text(encoding='utf-8-sig')

    def rejects(self,log):
        self.assertFalse(check.verify_log(log,'sonya',2,'native')['passed'])

    def test_all_36_actual_input_cases(self):
        found=list(cases());self.assertEqual(len(found),36)
        for name,target,side,profile in found:
            with self.subTest(name=name):
                proof=check.verify_log((ROOT/name/'run.log').read_text(encoding='utf-8-sig'),target,side,profile)
                self.assertTrue(proof['passed'],proof)

    def test_scope_does_not_claim_full_game(self):
        proof=check.verify_log(self.log,'sonya',2,'native')
        self.assertFalse(proof['whole_character_integration_complete'])
        self.assertEqual(proof['scope'],check.SCOPE)

    def test_zero_exit_cannot_hide_lua_errors(self):self.rejects(self.log+'\n[LUA ERROR] broken driver\n')
    def test_event_table_binding(self):self.rejects(self.log.replace('lp=FFFC9000','lp=FF869E00'))
    def test_forced_state_annotation(self):self.rejects(self.log.replace('writes=0','writes=1',1))
    def test_no_match(self):self.rejects(re.sub(r'^MK2_HUMAN_SHANG_MATCH.*\n','',self.log,flags=re.M))
    def test_proxy_body(self):self.rejects(self.log.replace('id=18','id=0'))
    def test_wrong_controller(self):self.rejects(self.log.replace('state=1 roster=6','state=0 roster=6'))
    def test_missing_field(self):self.rejects(re.sub(r'^MK2_HUMAN_SHANG_FIELD.*age=300 .*\n','',self.log,flags=re.M))
    def test_missing_input(self):self.rejects(re.sub(r'^MK2_HUMAN_SHANG_INPUT.*age=100 .*\n','',self.log,flags=re.M))
    def test_wrong_chord(self):self.rejects(self.log.replace('buttons=Down,Low_Punch,Block','buttons=Down,Low_Punch'))
    def test_wrong_facing(self):self.rejects(self.log.replace('facing=left','facing=right'))
    def test_missing_eligibility_gate(self):self.rejects(self.log.replace('entry=FFFC8F00','entry=00000000'))
    def test_wrong_forward_writer(self):self.rejects(self.log.replace('pc=FF86E670','pc=00000000'))
    def test_missing_forward_store(self):self.rejects(re.sub(r'^MK2_HUMAN_SHANG_STORE.*old=6 .*\n','',self.log,flags=re.M))
    def test_wrong_reverse_writer(self):self.rejects(self.log.replace('pc=FFA16700','pc=00000000'))
    def test_wrong_sequence(self):self.rejects(self.log.replace('root=FF0C1A00','root=FF0C1800'))
    def test_missing_reverse(self):self.rejects(re.sub(r'^MK2_HUMAN_SHANG_RESTORE_BEGIN.*\n','',self.log,flags=re.M))
    def test_wrong_palette(self):self.rejects(self.log.replace('palette=FF0C1000','palette=FF0C0800'))
    def test_wrong_composite(self):self.rejects(self.log.replace('group=FF0C4180','group=FF0C4060'))
    def test_floaty_form_floor(self):self.rejects(self.log.replace('floor=81','floor=87'))
    def test_wrong_projectile(self):self.rejects(self.log.replace('entry=FFFFB400','entry=FFFFB000'))
    def test_missing_child(self):self.rejects(re.sub(r'^MK2_HUMAN_SHANG_PROJECTILE_CREATE.*\n','',self.log,flags=re.M))
    def test_missing_release_pose(self):self.rejects(self.log.replace('action=0004','action=0303'))
    def test_missing_recovery(self):self.rejects(self.log.replace('action=0604','action=0303'))
    def test_no_real_contact(self):self.rejects(self.log.replace('hp1=155','hp1=161'))
    def test_dead_game(self):self.rejects(self.log.replace('mode=2','mode=11'))
    def test_no_post_restore_jump(self):self.rejects(self.log.replace('action=030B','action=0303'))
    def test_no_post_restore_punch(self):self.rejects(self.log.replace('action=0101','action=0303'))
    def test_rejected_input_cannot_be_a_positive(self):self.rejects(self.bad)
    def test_airborne_negative_requires_airborne_evidence(self):
        log=re.sub(r'y=-?\d+ floor=87', 'y=87 floor=87',self.bad)
        self.assertFalse(check.verify_log(log,'sonya',2,'airborne')['passed'])
    def test_forged_summary_cannot_prove_morph(self):
        log=self.bad.replace('forms=0 restores=0','forms=1 restores=1')
        self.assertFalse(check.verify_log(log,'sonya',2,'airborne')['passed'])


if __name__=='__main__':unittest.main()
