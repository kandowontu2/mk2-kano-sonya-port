import re
import unittest
import verify_human_special_negative_v4 as n
import verify_cannonball_velocity_v517 as audit

def log(kind='block'):
    return(n.ROOT/f'audit_v518_negative_ball_{kind}_p1_sub_zero/run.log').read_text(encoding='utf-8-sig')

class Rebound(unittest.TestCase):
    def test_nine_current_cases_and_retained_counterexample(self):
        r=audit.verify();self.assertEqual(len(r['cases']),9);self.assertTrue(r['targetedCasesPassed'])
        self.assertFalse(r['passed']);self.assertFalse(r['fullPortAcceptance'])
    def test_old_forward_rebound_rejected(self):
        text=(n.ROOT/'audit_v515_negative_ball_block_p1_sub_zero/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):n.verify_rebound(text,1,True)
    def test_old_body_push_slowdown_rejected(self):
        text=(n.ROOT/'audit_v511_cannonball_native_geometry_p1_kung_lao/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):n.verify_log(text,'ball',1,'miss','kung_lao')
    def test_missing_native_velocity_helper(self):
        text=log();hit=next(h['frame']for h in n.rows(text,'HEALTH')if h['before']-h['after']==5)
        changed=re.sub(r'^MK2_HSPECIAL_PARAMETERS frame='+str(hit)+r' .*entry=FF831AC0 .*\n','',text,flags=re.M)
        with self.assertRaises(ValueError):n.verify_rebound(changed,1,True)
    def test_wrong_native_fling_sentinel(self):
        text=log();changed=re.sub(r'(^MK2_HSPECIAL_PARAMETERS .*entry=FF876660 .*action=0602 a0=)0000000D',
                               r'\g<1>00000001',text,flags=re.M)
        self.assertNotEqual(changed,text)
        with self.assertRaises(ValueError):n.verify_rebound(changed,1,True)
    def test_missing_actual_velocity_store(self):
        text=log();hit=next(h['frame']for h in n.rows(text,'HEALTH')if h['before']-h['after']==5)
        changed=re.sub(r'^MK2_HSPECIAL_VELOCITY frame='+str(hit)+r' .*pc=FFFF[0-9A-F]+ .*\n','',text,flags=re.M)
        self.assertNotEqual(changed,text)
        with self.assertRaises(ValueError):n.verify_rebound(changed,1,True)
    def test_persistent_repel_counter(self):
        text=log();r=n.rows(text,'RESULT')[0]
        changed=re.sub(r'(^MK2_HSPECIAL_FIELD frame='+str(r['recovered'])+r' .*repel=)0',r'\g<1>2',text,flags=re.M)
        with self.assertRaises(ValueError):n.verify_repel(changed,1)
    def test_wrong_recoil_coordinates(self):
        text=log();hit=next(h['frame']for h in n.rows(text,'HEALTH')if h['before']-h['after']==5)
        changed=re.sub(r'(^MK2_HSPECIAL_FIELD frame='+str(hit+5)+r' .*slot=1 .*\bx=)-?\d+',r'\g<1>9000',text,flags=re.M)
        with self.assertRaises(ValueError):n.verify_rebound(changed,1,True)

if __name__=='__main__':unittest.main()
