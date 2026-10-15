"""Nonvacuous original-grab plus full owned follow-up regression checks."""
import re
import unittest
import verify_cpu_followup_v545 as check

CASES={'sonya':(602,'bicycle'),'sub_zero':(605,'square'),'liu_kang':(604,'blade')}


class NativeFollowup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={}
        for player,(boot,move) in CASES.items():
            folder=check.ROOT/f'audit_v568_cpu_followup_{player}_boot{boot}'
            proof=check.verify(folder,player,move)
            if not proof['passed']:raise AssertionError('Actual passing matched baseline required: '+str(proof))
            cls.logs[player]=(folder/'run.log').read_text(encoding='utf-8-sig')

    def mutate(self,player,tag,key,value,contains=(),remove=False,mirrored=False):
        lines=self.logs[player].splitlines(keepends=True);changed=0
        tags=(tag,'FOLLOW_FIELD')if mirrored else(tag,)
        for index,line in enumerate(lines):
            if any(line.startswith('MK2_CPU_PAIR_'+name+' ')for name in tags) and all(s in line for s in contains):
                if not re.search(r'\b'+key+r'=',line):continue
                lines[index]=''if remove else re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
                changed+=1
        self.assertGreater(changed,0,'Mutation must hit actual observer evidence')
        return ''.join(lines)

    def reject(self,player,text):
        proof=check.verify_log(text,player,CASES[player][1])
        self.assertFalse(proof['passed'],proof)

    def test_full_current_matched_baselines(self):
        for player,(boot,move) in CASES.items():
            proof=check.verify(check.ROOT/f'audit_v568_cpu_followup_{player}_boot{boot}',player,move)
            self.assertTrue(proof['passed'],proof)
            self.assertEqual(proof['native_followup']['move'],move)
            self.assertEqual(proof['damage'],32 if player=='liu_kang' else 35)
            self.assertEqual(proof['held_fields'],70 if player=='liu_kang' else 46)
            self.assertFalse(proof['whole_character_integration_complete'])

    def test_generic_state_cannot_relabel_actual_move_entry(self):
        for player,wrong in (('sonya','square'),('sub_zero','bicycle'),('liu_kang','square')):
            self.assertFalse(check.verify_log(self.logs[player],player,wrong)['passed'])


MUTATIONS=[
 ('bike_startup_pose','sonya','FIELD','pose','FE83EB40',('frame=1903 ',),False,False),
 ('bike_startup_x','sonya','FIELD','xraw','024F8000',('frame=1903 ',),False,False),
 ('bike_startup_y','sonya','FIELD','yraw','00660000',('frame=1903 ',),False,False),
 ('bike_seek_initial_vy','sonya','FIELD','vy','FFFF0000',('frame=1907 ',),False,False),
 ('bike_seek_negative_gravity','sonya','FIELD','gravity','00008000',('frame=1910 ',),False,False),
 ('bike_seek_cycle_pose','sonya','FIELD','pose','FE83EC00',('frame=1910 ',),False,False),
 ('bike_seek_stage_ground','sonya','FIELD','stage_floor','240',('frame=1919 ',),False,False),
 ('bike_fall_args','sonya','FOLLOW_INSTRUCTION','a2','00008000',('kind=fall ',),False,False),
 ('bike_fall_actual_callback','sonya','FOLLOW_INSTRUCTION','a6','00000000',('kind=fall ',),False,False),
 ('bike_fall_entry','sonya','FOLLOW_INSTRUCTION','entry','FF876650',('kind=fall ',),False,False),
 ('bike_fall_loop_pose','sonya','FIELD','pose','FE83EB40',('frame=1940 ',),False,True),
 ('bike_fall_y','sonya','FIELD','yraw','FFAA0000',('frame=1940 ',),False,True),
 ('bike_fall_vy','sonya','FIELD','vy','00010000',('frame=1940 ',),False,True),
 ('bike_fall_gravity','sonya','FIELD','gravity','00008000',('frame=1940 ',),False,True),
 ('bike_landing_fraction','sonya','FOLLOW_REGAIN','yraw','00510000',(),False,False),
 ('bike_effect_must_be_absent','sonya','FIELD','trail','01036540',('frame=1940 ',),False,True),
 ('square_rise_pose','sub_zero','FIELD','pose','FE835C20',('frame=1972 ',),False,False),
 ('square_rise_speed','sub_zero','FIELD','vy','FFF60000',('frame=1972 ',),False,False),
 ('square_rise_height','sub_zero','FIELD','yraw','00380000',('frame=1972 ',),False,False),
 ('square_flight_speed','sub_zero','FIELD','vx','FFFB0000',('frame=1990 ',),False,False),
 ('square_flight_height','sub_zero','FIELD','yraw','FFF20000',('frame=1990 ',),False,False),
 ('square_flight_pose','sub_zero','FIELD','pose','FE835C80',('frame=1990 ',),False,False),
 ('square_all_flight_checks','sub_zero','FOLLOW_INSTRUCTION','frame','2002',('kind=fling ',),False,False),
 ('square_drop_args','sub_zero','FOLLOW_INSTRUCTION','a1','00030000',('kind=fling ',),False,False),
 ('square_drop_y','sub_zero','FIELD','yraw','00200000',('frame=2010 ',),False,True),
 ('square_drop_pose','sub_zero','FIELD','pose','FE835C80',('frame=2010 ',),False,True),
 ('square_drop_gravity','sub_zero','FIELD','gravity','0000A000',('frame=2010 ',),False,True),
 ('square_landing_state','sub_zero','FIELD','action','771',('frame=2021 ',),False,True),
 ('square_full_landing_holds','sub_zero','FOLLOW_INSTRUCTION','frame','2018',('kind=landing ',),False,False),
 ('blade_first_pose','liu_kang','FIELD','pose','FE82FCA0',('frame=1871 ',),False,False),
 ('blade_startup_advance','liu_kang','FIELD','xraw','025B0000',('frame=1873 ',),False,False),
 ('blade_complete_hold','liu_kang','FIELD','pose','FE82FF40',('frame=1900 ',),False,False),
 ('blade_grounding','liu_kang','FIELD','y','81',('frame=1873 ',),False,False),
 ('blade_no_gravity','liu_kang','FIELD','gravity','00008000',('frame=1873 ',),False,False),
 ('blade_owned_trail','liu_kang','FIELD','trail','00000000',('frame=1873 ',),False,False),
 ('blade_trail_cleanup_entry','liu_kang','FOLLOW_INSTRUCTION','entry','FF83EE90',('kind=trail_cleanup ','frame=1908 '),False,False),
 ('blade_trail_cleanup_pointer','liu_kang','FOLLOW_INSTRUCTION','trail','00000000',('kind=trail_cleanup ','frame=1908 '),False,False),
 ('blade_missing_trail_cleanup','liu_kang','FOLLOW_INSTRUCTION','entry','',('kind=trail_cleanup ','frame=1908 '),True,False),
]

COMMON=[
 ('wrong_entry_move','FOLLOW_INSTRUCTION','move','leg',('kind=action ',),False),
 ('wrong_entry_address','FOLLOW_INSTRUCTION','entry','FFF80800',('kind=action ',),False),
 ('wrong_entry_actor','FOLLOW_INSTRUCTION','a8','010350A0',('kind=action ',),False),
 ('wrong_entry_Main','FOLLOW_INSTRUCTION','a13','0106FFFF',('kind=action ',),False),
 ('missing_entry','FOLLOW_INSTRUCTION','move','',('kind=action ',),True),
 ('missing_first_follow_regain','FOLLOW_REGAIN','frame','',(),True),
 ('follow_regain_still_locked','FOLLOW_REGAIN','flags','00000010',(),False),
 ('follow_regain_still_attached','FOLLOW_REGAIN','trail','01036540',(),False),
 ('follow_regain_airborne','FOLLOW_REGAIN','vy','00008000',(),False),
 ('follow_regain_wrong_Main','FOLLOW_REGAIN','main','0106FFFF',(),False),
 ('follow_regain_original_PC','FOLLOW_READY_INSTRUCTION','pc','FF861360',('kind=regained ',),False),
 ('missing_original_follow_ready','FOLLOW_READY_INSTRUCTION','entry','',('kind=recovery ',),True),
 ('terminal_first_regain','RESULT','follow_regain','9999',(),False),
 ('terminal_observation_window','RESULT','frame','9999',(),False),
 ('old_schema','RESULT','schema','6',(),False),
]
for player in CASES:
    for name,tag,key,value,contains,remove in COMMON:
        MUTATIONS.append((player+'_'+name,player,tag,key,value,contains,remove,False))

STARTS={'sonya':1900,'sub_zero':1969,'liu_kang':1870}
RECOVERIES={'sonya':1961,'sub_zero':2023,'liu_kang':1908}
for player in CASES:
    start=('frame='+str(STARTS[player])+' ','slot=1 ','kind=action ')
    for key,value in (('op0','B00D'),('op1','0210'),('a1','00000303'),
                      ('a13','0106FFFF'),('at','010601D0'),('before','0000')):
        MUTATIONS.append((player+'_state_publication_'+key,player,'FLAG',key,value,start,False,False))
    for field in ('body','flags'):
        MUTATIONS.append((player+'_NEW_setup_'+field,player,'FLAG','pc','',
                          ('frame='+str(STARTS[player])+' ','slot=1 ','kind='+field+' '),True,False))
        MUTATIONS.append((player+'_original_cleanup_'+field,player,'FLAG','pc','',
                          ('frame='+str(RECOVERIES[player])+' ','slot=1 ','kind='+field+' '),True,False))


def mutation_test(spec):
    _,player,tag,key,value,contains,remove,mirrored=spec
    def run(self):self.reject(player,self.mutate(player,tag,key,value,contains,remove,mirrored))
    return run


for spec in MUTATIONS:
    setattr(NativeFollowup,'test_'+spec[0],mutation_test(spec))

if __name__=='__main__':unittest.main()
