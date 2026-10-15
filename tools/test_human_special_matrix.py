"""Actual-current-log references and in-memory corrupted-trace rejections."""
import re
import unittest
import verify_human_special_matrix as v

def read(move='knife',side=1,air=False):
    suffix=move+'_air'if air else move
    return (v.ROOT/f'audit_v482_human_special_{suffix}_p{side}'/'run.log').read_text(encoding='utf-8-sig')

class Matrix(unittest.TestCase):
    def test_all_eighteen_actual_cases(self):
        for move,side,air in [(m,s,False)for m in v.SPECS for s in (1,2)]+[('square',s,True)for s in (1,2)]:
            with self.subTest(move=move,side=side,air=air):
                v.verify_log(read(move,side,air),move,side,air)
    def rejected(self,log,move='knife',side=1,air=False):
        with self.assertRaises(ValueError):v.verify_log(log,move,side,air)
    def test_missing_special_instruction(self):
        self.rejected(re.sub(r'^MK2_HSPECIAL_EVENT .*entry=FFFFB000 .*\n','',read(),flags=re.M))
    def test_proxy_actor(self):
        self.rejected(read().replace('id=17 roster=17','id=0 roster=0',1))
    def test_ownership_corruption(self):
        self.rejected(re.sub(r'owner=[0-9A-F]+','owner=00000000',read(),count=1))
    def test_missing_callback(self):
        self.rejected(re.sub(r'^MK2_HSPECIAL_FIELD .*\n','',read(),count=1,flags=re.M))
    def test_non_native_damage(self):
        self.rejected(read().replace('pc=FF836700','pc=00000000',1))
    def test_missing_damage_store(self):
        self.rejected(re.sub(r'^MK2_HSPECIAL_HEALTH .*\n','',read(),count=1,flags=re.M))
    def test_missing_native_ready_handoff(self):
        self.rejected(re.sub(r'^MK2_HSPECIAL_EVENT .*entry=FF861350 .*\n','',read(),flags=re.M))
    def test_wrong_button(self):
        result=v.rows(read(),'RESULT')[0];frame=result['command']+6
        line=next(s for s in read().splitlines()if s.startswith('MK2_HSPECIAL_INPUT frame='+str(frame)+' ')and'button=High_Punch'in s)
        self.rejected(read().replace(line,line.replace('High_Punch','Low_Punch')))
    def test_charged_release_input_omitted(self):
        log=read('ball');result=v.rows(log,'RESULT')[0];frame=result['command']+83
        self.rejected(re.sub(r'^MK2_HSPECIAL_INPUT frame='+str(frame)+r' .*button=Low_Kick\n','',log,flags=re.M),'ball')
    def test_stationary_target_cannot_count_as_air_hit(self):
        self.rejected(read('square'), 'square',air=True)
    def test_missing_genuine_target_jump_input(self):
        log=read('square',air=True)
        self.rejected(re.sub(r'^MK2_HSPECIAL_INPUT .*slot=2 button=Up\n','',log,flags=re.M),'square',air=True)
    def mutate_window(self,log,first,last,change):
        result=v.rows(log,'RESULT')[0];output=[]
        for line in log.splitlines():
            if line.startswith('MK2_HSPECIAL_FIELD '):
                field=v.rows(line,'FIELD')[0]
                if field['slot']==1 and result['followup']+first<=field['frame']<=result['followup']+last:
                    line=change(line,field)
            output.append(line)
        return '\n'.join(output)+'\n'
    def test_walk_stall(self):
        self.rejected(self.mutate_window(read(),2,9,lambda line,f:re.sub(r'vx=[0-9A-F]+','vx=00000000',line)))
    def test_walk_teleport(self):
        self.rejected(self.mutate_window(read(),3,8,lambda line,f:re.sub(r'\bx=-?\d+', 'x='+str(f['x']+100*f['frame']),line)))
    def test_jump_stall(self):
        def ground(line,f):
            return re.sub(r'\by=-?\d+','y='+str(f['floor']),line)
        self.rejected(self.mutate_window(read(),42,65,ground))
    def test_punch_stall(self):
        self.rejected(self.mutate_window(read(),114,140,lambda line,f:re.sub(r'action=\d+','action=771',line)))
    def test_frozen_special_pose(self):
        log=read();result=v.rows(log,'RESULT')[0];out=[]
        for line in log.splitlines():
            if line.startswith('MK2_HSPECIAL_FIELD '):
                f=v.rows(line,'FIELD')[0]
                if f['slot']==1 and result['entry']<f['frame']<=result['recovered']:
                    line=re.sub(r'pose=[0-9A-F]+','pose=FF00DB20',line)
            out.append(line)
        self.rejected('\n'.join(out)+'\n')
    def test_result_cannot_override_actual_phase(self):
        log=read();r=v.rows(log,'RESULT')[0]
        self.rejected(log.replace('recovered='+str(r['recovered']),'recovered='+str(r['entry'])))

if __name__=='__main__':unittest.main()
