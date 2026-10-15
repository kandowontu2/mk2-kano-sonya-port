"""Actual roster fixtures and corruption rejection, not artwork/CPU acceptance."""
import re
import unittest
import verify_human_special_contacts_v635 as v
import verify_human_special_matrix as old


def log(move='leg',side=2,victim='sonya',air=False):
    return(v.case_folder(move,side,victim,air)/'run.log').read_text(encoding='utf-8-sig')


class Contacts(unittest.TestCase):
    def reject(self,text,move='leg',side=2,victim='sonya',air=False):
        with self.assertRaises(ValueError):v.verify_log(text,move,side,air,victim)

    def test_all_actual_roster_cases(self):
        proof=v.verify()
        self.assertEqual(proof['cases_count'],252)
        self.assertTrue(proof['passed'],proof['failures'])
        self.assertFalse(proof['fullPortAcceptance'])

    def test_unchanged_sub_zero_controls(self):
        # The only observer changes are selectable victim routes and a log
        # label. The complete existing eighteen-case timeline must stay exact.
        for move in v.SPECS:
            for side in(1,2):
                for air in((False,True)if move=='square'else(False,)):
                    with self.subTest(move=move,side=side,air=air):
                        actual=log(move,side,'sub_zero',air)
                        suffix=move+'_air'if air else move
                        prior=(v.ROOT/f'audit_v652_positive_{suffix}_p{side}/run.log').read_text(encoding='utf-8-sig')
                        strip=lambda text:[re.sub(r' victim=sub_zero','',line)for line in text.splitlines()
                                           if line.startswith('MK2_HSPECIAL_')]
                        self.assertEqual(strip(actual),strip(prior))
                        contract=old.verify_log(actual,move,side,air)
                        general=v.verify_log(actual,move,side,air,'sub_zero')
                        self.assertEqual(contract,{key:general[key]for key in contract})

    def test_wrong_opponent_identity(self):
        text=log('choke',1,'kano')
        line=next(line for line in text.splitlines()if line.startswith('MK2_HSPECIAL_FIELD ')and 'slot=2 'in line)
        self.reject(text.replace(line,line.replace('id=17 roster=17','id=1 roster=1'),1),'choke',1,'kano')

    def test_proxy_own_identity(self):
        text=log()
        line=next(line for line in text.splitlines()if line.startswith('MK2_HSPECIAL_FIELD ')and 'slot=2 'in line)
        self.reject(text.replace(line,line.replace('id=18 roster=18','id=1 roster=1'),1))

    def test_wrong_mirror_main_owner(self):
        self.reject(re.sub(r'owner=[0-9A-F]+','owner=00000000',log(),count=1))

    def test_missing_paired_field(self):
        self.reject(re.sub(r'^MK2_HSPECIAL_FIELD .*\n','',log(),count=1,flags=re.M))

    def test_missing_actual_native_entry(self):
        self.reject(re.sub(r'^MK2_HSPECIAL_EVENT .*entry=FFF80800 .*\n','',log(),count=1,flags=re.M))

    def test_missing_collision_store(self):
        text=log()
        # The leg fixture first emits a zero-damage store. Removing that cannot
        # contradict adjacent HP, so target an actual damaging collision.
        health=next(h for h in v.rows(text,'HEALTH')if h['before']!=h['after'])
        line=next(line for line in text.splitlines()if line.startswith('MK2_HSPECIAL_HEALTH ')
                  and f'frame={health["frame"]} 'in line and
                  f'before={health["before"]} after={health["after"]} 'in line)
        self.reject(text.replace(line+'\n','',1))

    def test_non_native_collision_writer(self):
        self.reject(log().replace('pc=FF836700','pc=00000000',1))

    def test_persistent_mirror_victim_lock(self):
        text=log();result=v.rows(text,'RESULT')[0]
        line=next(line for line in text.splitlines()if line.startswith('MK2_HSPECIAL_FIELD ')
                  and f'frame={result["recovered"]} 'in line and 'slot=1 'in line)
        altered=re.sub(r'flags=[0-9A-F]+','flags=0000001D',line)
        self.assertNotEqual(line,altered)
        self.reject(text.replace(line,altered,1))

    def test_missing_native_ready_return(self):
        self.reject(re.sub(r'^MK2_HSPECIAL_EVENT .*entry=FF861350 .*\n','',log(),flags=re.M))

    def test_missing_followup_jump_input(self):
        self.reject(re.sub(r'^MK2_HSPECIAL_INPUT .*button=Up\s*\n','',log(),flags=re.M))

    def test_ground_square_cannot_prove_air_contact(self):
        self.reject(log('square',1,'kitana'),'square',1,'kitana',True)

    def test_wrong_declared_opponent(self):
        self.reject(log(),victim='kitana')

    def test_runtime_failure_cannot_pass(self):
        self.reject(log()+'\n[LUA ERROR] in execute_function: failed observer\n')


if __name__=='__main__':unittest.main()
