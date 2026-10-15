"""Current actual traces plus in-memory ownership/cancel/KO/cursor regressions."""
import re
import unittest
import verify_interrupt_and_ko_v635 as v
import verify_current_lifecycle as old

def interrupt(move='blade',side=1,victim='sonya'):
    return (v.ROOT/f'audit_v653_interrupt_{move}_p{side}_{victim}/run.log').read_text(encoding='utf-8-sig')

def ko(move='bicycle',side=1,victim='sonya'):
    return (v.ROOT/f'audit_v653_ko_{move}_p{side}_{victim}/run.log').read_text(encoding='utf-8-sig')

class Interruptions(unittest.TestCase):
    def reject(self,log,move='blade',side=1,victim='sonya'):
        with self.assertRaises(ValueError):v.verify_interrupt(log,move,side,victim)
    def test_all_ten_actual_cases(self):
        for move,side,victim in v.INT_CASES:
            with self.subTest(move=move,side=side,victim=victim):
                v.verify_interrupt(interrupt(move,side,victim),move,side,victim)
    def test_proxy_identity(self):
        self.reject(interrupt().replace('id=17 roster=17','id=1 roster=1',1))
    def test_wrong_main_owner(self):
        self.reject(re.sub(r'owner=[0-9A-F]+','owner=00000000',interrupt(),count=1))
    def test_missing_actual_field(self):
        self.reject(re.sub(r'^MK2_INTERRUPT_FIELD .*\n','',interrupt(),count=1,flags=re.M))
    def test_non_native_health_writer(self):
        self.reject(interrupt().replace('pc=FF836700','pc=00000000',1))
    def test_missing_damage_store(self):
        self.reject(re.sub(r'^MK2_INTERRUPT_HEALTH .*before=161 after=121 .*\n','',interrupt(),count=1,flags=re.M))
    def test_original_damage_cannot_be_replaced_by_summary(self):
        self.reject(interrupt().replace('after=121','after=161',1))
    def test_no_actual_native_entry(self):
        self.reject(re.sub(r'^MK2_INTERRUPT_EVENT .*phase=1 .*kind=action .*\n','',interrupt(),count=1,flags=re.M))
    def test_no_actual_retry_entry(self):
        self.reject(re.sub(r'^MK2_INTERRUPT_EVENT .*phase=2 .*kind=action .*\n','',interrupt(),count=1,flags=re.M))
    def test_missing_native_ready(self):
        self.reject(re.sub(r'^MK2_INTERRUPT_EVENT .*kind=ready .*\n','',interrupt(),flags=re.M))
    def test_descriptor_is_not_an_instruction_entry(self):
        self.reject(interrupt().replace('entry=FFF8E400 pc=FF835480','entry=FFF8E400 pc=FFF8E410'))
    def test_attack_cannot_succeed_before_interruption(self):
        log=interrupt();line=next(s for s in log.splitlines()if s.startswith('MK2_INTERRUPT_EVENT ')and'kind=strike'in s)
        self.reject(log.replace(line,line.replace('phase=2','phase=1')))
    def test_cancelled_blade_cannot_remain_attached(self):
        log=interrupt();health=[h for h in v.rows(log,'HEALTH')if h['after']<h['before']][0]
        frame=health['frame']+4
        line=next(s for s in log.splitlines()if s.startswith('MK2_INTERRUPT_FIELD frame='+str(frame)+' ')and'slot=1'in s)
        self.reject(log.replace(line,line.replace('trail=00000000','trail=010352B0')))
    def test_false_cleanup_deadline(self):
        log=interrupt();hit=[h for h in v.rows(log,'HEALTH')if h['after']<h['before']][0]['frame']
        self.reject(re.sub(r'MK2KS_BLADE_INTERRUPT_CLEANUP frame=\d+',
                           'MK2KS_BLADE_INTERRUPT_CLEANUP frame='+str(hit+20),log))
    def test_wrong_original_floor(self):
        self.reject(re.sub(r'floor=-?\d+','floor=999',interrupt(),count=1))
    def test_missing_actual_counter_input(self):
        self.reject(re.sub(r'^MK2_INTERRUPT_INPUT .*slot=2 button=hp .*\n','',interrupt(),flags=re.M))
    def test_missing_paired_bicycle_update(self):
        self.reject(re.sub(r'^MK2_INTERRUPT_EVENT .*kind=tick .*\n','',interrupt('bicycle'),count=1,flags=re.M),'bicycle')
    def test_lua_error_is_not_a_game_pass(self):
        self.reject(interrupt()+'\n[LUA ERROR] in execute_function: failed observer\n')

class Knockouts(unittest.TestCase):
    def own_cursor(self,log,cursor):
        # A Sonya mirror victim also reads this list. Mutate the attacker/Main
        # under test, not the first matching address anywhere in the trace.
        own=next(f for f in v.life.rows(log,'FIELD')if f['cycle']==1 and f['slot']==1)
        return next(line for line in log.splitlines()if
                    line.startswith('MK2_LIFE_TRACE_EVENT ')and 'cycle=1 'in line and
                    'kind=animation 'in line and f'a9={cursor:08X} 'in line and
                    f'a8={own["actor"]:08X} 'in line and f'a13={own["main"]:08X} 'in line)
    def mutate_cursor(self,cursor,replacement):
        log=ko();line=self.own_cursor(log,cursor)
        changed=line.replace(f'a9={cursor:08X}',f'a9={replacement:08X}')
        self.assertNotEqual(line,changed)
        return log.replace(line,changed,1)
    def grade(self,log,move='bicycle',side=1,victim='sonya'):
        return v.life.verify(log,move,side,victim)
    def reject(self,log,move='bicycle',side=1,victim='sonya'):
        self.assertFalse(self.grade(log,move,side,victim)['passed'])
    def test_all_four_current_ko_round_cases(self):
        for move,side,victim in v.KO_CASES:
            with self.subTest(move=move,side=side,victim=victim):
                self.assertTrue(self.grade(ko(move,side,victim),move,side,victim)['passed'])
    def test_original_fixed_phase_model_is_insufficient_for_early_contact(self):
        self.assertFalse(old.verify(ko(),'bicycle',1,'sonya')['passed'])
        self.assertTrue(self.grade(ko())['passed'])
    def test_missing_cursor_read(self):
        log=ko();self.reject(log.replace(self.own_cursor(log,0xFFF9EB00)+'\n','',1))
    def test_reordered_authored_cursor(self):
        self.reject(self.mutate_cursor(0xFFF9EB20,0xFFF9EB80))
    def test_corrupted_loop_token(self):
        self.reject(self.mutate_cursor(0xFFF9EC40,0xFFF9EB00))
    def test_corrupted_native_animation_reader(self):
        log=ko();line=self.own_cursor(log,0xFFF9EB00)
        self.reject(log.replace(line,line.replace('pc=FF83BB10','pc=00000000')))
    def test_wrong_four_field_cadence(self):
        log=ko();line=self.own_cursor(log,0xFFF9EB40)
        age=int(re.search(r'\bage=(\d+)',line)[1]);frame=int(re.search(r'frame=(\d+)',line)[1])
        changed=line.replace('frame='+str(frame),'frame='+str(frame+1)).replace('age='+str(age),'age='+str(age+1))
        self.reject(log.replace(line,changed))
    def test_shifted_body_cannot_choose_its_own_phase(self):
        log=ko();fields=v.life.rows(log,'FIELD');ticks=[e for e in v.life.rows(log,'EVENT')if e['cycle']==1 and e['kind']=='tick']
        age=ticks[0]['age']+2
        line=next(s for s in log.splitlines()if s.startswith('MK2_LIFE_TRACE_FIELD ')and
                  'cycle=1 'in s and'age='+str(age)+' 'in s and'slot=1 'in s)
        self.reject(log.replace(line,re.sub(r'pose=[0-9A-F]+','pose=FE83EC80',line)))
    def test_missing_next_round(self):
        self.reject(re.sub(r'^MK2KS_BICYCLE_LIFECYCLE_NEXT .*\n','',ko(),flags=re.M))
    def test_wrong_next_round_health(self):
        log=ko();line=next(s for s in log.splitlines()if s.startswith('MK2_LIFE_TRACE_FIELD ')and
                          'cycle=9 age=0 slot=2'in s)
        self.reject(log.replace(line,line.replace('hp=161','hp=1')))
    def test_missing_blood_cleanup(self):
        self.reject(re.sub(r'^MK2_LIFE_TRACE_EVENT .*kind=blood_cleanup .*\n','',ko('blade',1,'kano'),count=1,flags=re.M),'blade',1,'kano')
    def test_stale_paired_state(self):
        log=ko();line=next(s for s in log.splitlines()if s.startswith('MK2_LIFE_TRACE_FIELD ')and
                          'cycle=1 age=200 slot=2'in s)
        self.reject(log.replace(line,line.replace('flags=0001','flags=001D')))

if __name__=='__main__':unittest.main()
