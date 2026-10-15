"""Current successful bounded fixtures and in-memory falsification checks."""
import re
import unittest
import verify_human_special_negative_v3 as v
import verify_current_special_matrix_v500 as audit
import verify_original_ball_v1 as original

def log(move='ball',scenario='miss',side=1):
    return(v.ROOT/f'audit_v503_negative_{move}_{scenario}_p{side}_sub_zero/run.log').read_text(encoding='utf-8-sig')

class CurrentMatrix(unittest.TestCase):
    def reject(self,text,move='ball',scenario='miss'):
        with self.assertRaises(ValueError):v.verify_log(text,move,1,scenario)
    def test_all_current_positive_negative_and_original_cases(self):
        report=audit.verify();self.assertEqual(len(report['positiveCases']),18)
        self.assertEqual(len(report['negativeCases']),34);self.assertEqual(len(report['originalCases']),6)
        self.assertTrue(report['boundedMatrixPassed']);self.assertFalse(report['passed'])
        self.assertEqual(len(report['originalDuckPhaseCases']),8)
        contacts={(c['victim'],c['side'])for c in report['widerDuckObservations']if c['status']=='duck_contact_needs_fidelity_review'}
        self.assertEqual(contacts,{('baraka',1),('baraka',2),('kitana',1),('kitana',2),
                                   ('mileena',1),('mileena',2),('liu_kang',1),('raiden',1)})
        self.assertEqual(sum(c['status']=='duck_miss_kinematics_unproven'for c in report['widerDuckObservations']),4)
        self.assertFalse(report['fullPortAcceptance'])
    def test_lua_error_not_terminal_success(self):self.reject(log()+'[LUA ERROR] invalid field\n')
    def test_proxy_identity(self):self.reject(log().replace('id=17 roster=17','id=1 roster=1',1))
    def test_wrong_victim_identity(self):self.reject(log().replace('id=8 roster=8','id=1 roster=1',1))
    def test_wrong_owner(self):self.reject(re.sub(r'owner=[0-9A-F]+','owner=00000000',log(),count=1))
    def test_missing_paired_field(self):self.reject(re.sub(r'^MK2_HSPECIAL_FIELD .*\n','',log(),count=1,flags=re.M))
    def test_missing_entry(self):self.reject(re.sub(r'^MK2_HSPECIAL_EVENT .*entry=FFFFDE00 .*\n','',log(),flags=re.M))
    def test_missing_native_ready(self):self.reject(re.sub(r'^MK2_HSPECIAL_EVENT .*entry=FF861350 .*\n','',log(),flags=re.M))
    def test_missing_lk_release_inventory(self):
        text=log();r=v.rows(text,'RESULT')[0]
        self.reject(re.sub(r'^MK2_HSPECIAL_INPUT frame='+str(r['command']+83)+r' .*button=Low_Kick\n','',text,flags=re.M))
    def test_missing_duck_input(self):
        text=log();r=v.rows(text,'RESULT')[0]
        self.reject(re.sub(r'^MK2_HSPECIAL_INPUT frame='+str(r['command']+13)+r' .*slot=2 button=Down\n','',text,flags=re.M))
    def test_missing_native_rectangle(self):self.reject(re.sub(r'^MK2_HSPECIAL_GEOMETRY .*\n','',log(),count=1,flags=re.M))
    def test_wrong_rectangle_writer(self):self.reject(log().replace('pc=FF835B80','pc=FF835B70',1))
    def test_old_lower_plane(self):self.reject(log().replace('attack_max=008A0254','attack_max=008F0254',1))
    def test_wrong_rectangle_width(self):self.reject(log().replace('attack_max=008A0254','attack_max=008A0255',1))
    def test_wrong_flight_speed(self):
        text=log();r=v.rows(text,'RESULT')[0];frame=r['entry']+10
        pattern=r'(^MK2_HSPECIAL_FIELD frame='+str(frame)+r' .*slot=1 .*vx=)[0-9A-F]+'
        changed=re.sub(pattern,r'\g<1>00000000',text,flags=re.M);self.assertNotEqual(changed,text);self.reject(changed)
    def test_block_damage_writer(self):self.reject(log(scenario='block').replace('pc=FF836700','pc=00000000',1),scenario='block')
    def test_unexplained_block_health(self):self.reject(re.sub(r'^MK2_HSPECIAL_HEALTH .*\n','',log(scenario='block'),count=1,flags=re.M),scenario='block')
    def test_wrong_crouch_block_action(self):
        text=log('leg','duck_block');r=v.rows(text,'RESULT')[0];contact=next(h for h in v.rows(text,'HEALTH')if r['entry']<=h['frame']<=r['recovered'])
        pattern=r'(^MK2_HSPECIAL_FIELD frame='+str(contact['frame'])+r' .*slot=2 .*action=)1793'
        changed=re.sub(pattern,r'\g<1>1794',text,flags=re.M);self.assertNotEqual(changed,text);self.reject(changed,'leg','duck_block')
    def test_missing_original_rectangle(self):
        text=(v.ROOT/'audit_v505_original_ball_sub_zero_duck/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):original.verify_log(re.sub(r'^MK3_BALL_GEOMETRY .*\n','',text,count=1,flags=re.M),'sub_zero','duck')
    def test_original_health_writer(self):
        text=(v.ROOT/'audit_v505_original_ball_sub_zero_ground/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):original.verify_log(text.replace('pc=FFA5D5A0','pc=00000000',1),'sub_zero','ground')

if __name__=='__main__':unittest.main()
