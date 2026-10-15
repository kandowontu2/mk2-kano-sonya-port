"""Actual current ending/fresh-game/join traces, not synthetic campaign proof."""
import re
import unittest

from verify_projectile_choreography import ROOT,verify_contact
from verify_post_ending_restart import verify
from verify_restart_lifecycle import verify_projectile_join
from check_post_restart_assistance import verify as assistance
from verify_current_post_ending_choreography import verify as current

SPECS=(('kano','sonya',1,1,'hit'),('sonya','kano',1,2,'miss'),
       ('kano','sonya',2,2,'block'),('sonya','kano',2,1,'hit'))


def name(source,target,ss,ns,scenario):
    return f'audit_v310_current_end_p{ss}_{source}_p{ns}_{target}_{scenario}'


class CurrentPostEndingChoreography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={spec:(ROOT/name(*spec)/'run.log').read_text(encoding='utf-8-sig') for spec in SPECS}
        cls.first=cls.logs[SPECS[0]]

    def reject(self,tag,field=None,value=None,predicate=lambda line:True):
        lines=self.first.splitlines()
        index=next(i for i,line in enumerate(lines) if line.startswith(tag+' ') and predicate(line))
        if field is None:del lines[index]
        else:lines[index],count=re.subn(r'\b'+field+r'=\S+',field+'='+value,lines[index]);self.assertEqual(count,1)
        proof=verify('\n'.join(lines),'kano','sonya',1,1,'projectile_choreography')
        self.assertFalse(proof['passed'],proof)

    def test_four_actual_current_ending_to_fresh_join_paths(self):
        for spec,log in self.logs.items():
            source,target,ss,ns,scenario=spec
            with self.subTest(spec=spec):
                proof=verify(log,source,target,ss,ns,'projectile_choreography')
                self.assertTrue(proof['passed'],proof['errors'])
                proof=assistance(log,source,ss,all_regen=True)
                self.assertTrue(proof['passed'],proof['errors'])
                proof=current(ROOT/name(*spec),source,target,ss,ns,scenario)
                self.assertTrue(proof['passed'],proof['errors'])

    def test_cold_match_is_not_post_ending(self):
        log=(ROOT/'audit_v303_render_shadow_sonya_hit_p1'/'run.log')
        if not log.exists():log=ROOT/'audit_v302_render_sonya_hit_p1'/'run.log'
        proof=verify_projectile_join(log.read_text(encoding='utf-8-sig'),'sonya',1,True,contact_verifier=verify_contact)
        self.assertFalse(proof['passed'])

    def test_missing_own_ending_picture(self):self.reject('MK2_RESTART_PICTURE',predicate=lambda s:'page=2' in s)
    def test_wrong_ending_identity(self):self.reject('MK2_RESTART_PICTURE','id','1')
    def test_missing_native_attract(self):self.reject('MK2_RESTART_ATTRACT')
    def test_fresh_match_wrong_actor(self):self.reject('MK2_RESTART_MATCH','id','1')
    def test_fresh_game_shortened(self):self.reject('MK2_RESTART_COMPLETE','live','120')
    def test_missing_actual_challenger_attach(self):self.reject('MK2_JOIN_LIFE_ATTACH')
    def test_wrong_joined_identity(self):self.reject('MK2_PROJ_CONTACT_FIELD','id','1')
    def test_missing_release_hold(self):self.reject('MK2_CHOREO_HUMAN')
    def test_missing_complete_original_flight_pose(self):self.reject('MK2_CHOREO_GROUP',predicate=lambda s:'group=FF614AC0' in s)
    def test_native_damage_not_applied(self):self.reject('MK2_PROJ_CONTACT_HEALTH','after','161')

    def test_actual_p1_regen_events_not_baseline_counter_assumption(self):
        missing=re.sub(r'^MK2KS_DIAGNOSTIC_P1_REGEN [^\r\n]*\r?\n','',self.first,count=1,flags=re.M)
        self.assertFalse(assistance(missing,'kano',1,all_regen=True)['passed'])

    def test_post_attract_health_regen_rejected(self):
        end=int(re.search(r'MK2_RESTART_ATTRACT frame=(\d+)',self.first)[1])
        changed=re.sub(r'(MK2KS_DIAGNOSTIC_P1_REGEN frame=)\d+',lambda m:m[1]+str(end+1),self.first,count=1)
        self.assertFalse(assistance(changed,'kano',1,all_regen=True)['passed'])

    def test_invalid_regen_value_rejected(self):
        changed=re.sub(r'(MK2KS_DIAGNOSTIC_P1_REGEN frame=\d+ old=)\d+',r'\g<1>0',self.first,count=1)
        self.assertFalse(assistance(changed,'kano',1,all_regen=True)['passed'])

    def test_missing_p2_health_event_rejected(self):
        log=self.logs[SPECS[2]]
        changed=re.sub(r'^MK2_P2_TOWER_HEALTH [^\r\n]*\r?\n','',log,count=1,flags=re.M)
        self.assertFalse(assistance(changed,'kano',2,all_regen=True)['passed'])

    def test_same_frame_shang_restore_does_not_rewrite_earlier_sample(self):
        from verify_p2_tower import verify as tower
        log=(ROOT/'audit_v307_current_end_p2_kano_p2_sonya_block'/'run.log').read_text(encoding='utf-8-sig')
        self.assertIn('MK2_P2_TOWER_LIVE frame=91470',log)
        self.assertIn('MK2_NATIVE_SHANG_ID frame=91470',log)
        self.assertTrue(tower(log,'kano')['passed'])
        changed=re.sub(r'(MK2_P2_TOWER_LIVE frame=91470 [^\r\n]*cpu=6:)10',r'\g<1>9',log,count=1)
        self.assertNotEqual(changed,log)
        self.assertFalse(tower(changed,'kano')['passed'])

    def test_two_actual_current_unassisted_finish_routes(self):
        from verify_unassisted_finish import verify as finish
        for fighter,victim in (('kano','sonya'),('sonya','sub_zero')):
            folder=ROOT/f'audit_v308_current_finish_{fighter}_{victim}'
            result=finish((folder/'run.log').read_text(encoding='utf-8-sig'),fighter,victim)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual(result['total_native_damage'],322)


if __name__=='__main__':unittest.main()
