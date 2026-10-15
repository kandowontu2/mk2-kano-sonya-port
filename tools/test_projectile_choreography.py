"""Actual new-candidate field evidence and rejection of incomplete/wrong traces."""
import re
import unittest
from pathlib import Path

from verify_projectile_choreography import verify,verify_contact
from verify_restart_lifecycle import verify_projectile_join

ROOT=Path(__file__).resolve().parents[1]


class CurrentChoreographyEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=ROOT/'audit_v300_choreo_kano_hit_p1'
        cls.log=(cls.folder/'run.log').read_text(encoding='utf-8-sig')

    def reject(self,tag,field=None,value=None,predicate=lambda line:True):
        lines=self.log.splitlines()
        index=next(i for i,line in enumerate(lines) if line.startswith(tag+' ') and predicate(line))
        if field is None:del lines[index]
        else:lines[index],count=re.subn(r'\b'+field+r'=\S+',field+'='+value,lines[index]);self.assertEqual(count,1)
        result=verify_contact('\n'.join(lines),'kano',1)
        self.assertFalse(result['passed'],result)

    def test_twelve_terminal_matched_current_cases(self):
        for target in ('kano','sonya'):
            for side in (1,2):
                for scenario in ('hit','block','miss'):
                    with self.subTest(target=target,side=side,scenario=scenario):
                        result=verify(ROOT/f'audit_v300_choreo_{target}_{scenario}_p{side}',target,side)
                        self.assertTrue(result['passed'],result)

    def test_missing_actual_body_group(self):self.reject('MK2_CHOREO_GROUP',predicate=lambda s:'body=1' in s)
    def test_wrong_actual_body_pose(self):self.reject('MK2_CHOREO_GROUP','group','FE82F400',lambda s:'group=FE82F4C0' in s)
    def test_missing_held_human_field(self):self.reject('MK2_CHOREO_HUMAN')
    def test_wrong_busy_human_action(self):self.reject('MK2_CHOREO_HUMAN','action','0303',lambda s:'action=0004' in s)
    def test_wrong_human_recovery_action(self):self.reject('MK2_CHOREO_HUMAN','action','0604',lambda s:'action=0303' in s)
    def test_missing_intro_composite(self):self.reject('MK2_CHOREO_GROUP',predicate=lambda s:'group=FF6141E0' in s)
    def test_wrong_intro_origin(self):self.reject('MK2_PROJ_CONTACT_EFFECT','x','470')
    def test_repeated_instead_of_complete_travel_cycle(self):self.reject('MK2_CHOREO_GROUP','group','FF614800',lambda s:'group=FF614840' in s)
    def test_wrong_native_travel_cadence(self):self.reject('MK2_CHOREO_GROUP','frame','3175',lambda s:'group=FF614840' in s)
    def test_wrong_native_speed(self):self.reject('MK2_PROJ_CONTACT_EFFECT','vx','000C0000',lambda s:'vx=00080000' in s)
    def test_missing_child_field(self):self.reject('MK2_PROJ_CONTACT_EFFECT')
    def test_wrong_real_actor_identity(self):self.reject('MK2_PROJ_CONTACT_FIELD','id','0')
    def test_missing_input(self):self.reject('MK2_PROJ_CONTACT_CONTROL')
    def test_missing_geometry(self):self.reject('MK2_PROJ_CONTACT_GEOMETRY')
    def test_wrong_native_contact_owner(self):self.reject('MK2_PROJ_CONTACT_EVENT','a13','01068EA0',lambda s:'kind=contact' in s)
    def test_wrong_native_damage(self):self.reject('MK2_PROJ_CONTACT_HEALTH','after','161')
    def test_missing_real_join_transition(self):
        altered='\n'.join(line for line in self.log.splitlines() if not line.startswith('MK2_JOIN_LIFE_ATTACH '))
        result=verify_projectile_join(altered,'kano',1,False,contact_verifier=verify_contact)
        self.assertFalse(result['passed'],result)


if __name__=='__main__':unittest.main()
