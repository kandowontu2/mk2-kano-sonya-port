"""Actual P2-CPU baselines plus nonvacuous physical-slot/phase corruption tests."""
import re
import unittest
import verify_cpu_recovery_v545_v3 as c

CASES={
    'sonya':('audit_v578_p2cpu_sonya_boot600','sonya','bicycle',1720,1785),
    'kano_mirror':('audit_v578_p2cpu_kano_boot602','kano','ordinary',1720,1830),
    'sonya_kano':('audit_v578_p2cpu_kano_boot600','kano','ordinary',1820,1920),
    'sonya_cage':('audit_v578_p2cpu_cage_boot600','cage','ordinary',1860,1980),
}

class OppositeSlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={}
        for key,(folder,player,move,held,follow) in CASES.items():
            result=c.verify(c.ROOT/folder,player,move)
            if not result['passed']:raise AssertionError('Actual passing matched baseline required: '+str(result))
            cls.logs[key]=(c.ROOT/folder/'run.log').read_text(encoding='utf-8-sig')

    def mutate(self,case,tag,key,value,contains=(),remove=False,mirror=False):
        lines=self.logs[case].splitlines(keepends=True);count=0
        tags=(tag,'FOLLOW_FIELD')if mirror else(tag,)
        for index,line in enumerate(lines):
            if any(line.startswith('MK2_CPU_PAIR_'+t+' ')for t in tags) and all(x in line for x in contains):
                if not re.search(r'\b'+key+'=',line):continue
                changed=''if remove else re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
                if changed!=line:count+=1
                lines[index]=changed
        self.assertGreater(count,0,'Mutation must alter actual baseline evidence')
        return ''.join(lines)

    def reject(self,case,log):
        _,player,move,_,_=CASES[case]
        self.assertFalse(c.verify_log(log,player,move)['passed'])

    def test_actual_matched_baselines(self):
        for case,(folder,player,move,held,follow)in CASES.items():
            proof=c.verify(c.ROOT/folder,player,move)
            self.assertTrue(proof['passed'],proof)
            self.assertEqual((proof['CPU_slot'],proof['human_slot']),(2,1))
            self.assertFalse(proof['whole_character_integration_complete'])

    def test_original_P1_CPU_logs_cannot_be_relabelled_as_opposite_slot(self):
        log=(c.ROOT/'audit_v568_cpu_followup_sonya_boot602/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(c.verify_log(log,'sonya','bicycle')['passed'])

    def test_bicycle_not_an_ordinary_followup(self):
        self.assertFalse(c.verify_log(self.logs['sonya'],'sonya','ordinary')['passed'])

    def test_ordinary_not_a_bicycle_followup(self):
        self.assertFalse(c.verify_log(self.logs['kano_mirror'],'kano','bicycle')['passed'])

MUTATIONS=[]
for case,(_,player,move,held,follow) in CASES.items():
    h=('frame='+str(held)+' ',);f=('frame='+str(follow)+' ',)
    for tag,key,value,contains,remove,mirror in [
        ('BIND','actor_at','01060220',(*h,'slot=2 '),False,False),
        ('BIND','main_at','01060260',(*h,'slot=2 '),False,False),
        ('BIND','hp_at','010602F0',(*h,'slot=2 '),False,False),
        ('BIND','state_at','010601F0',(*h,'slot=2 '),False,False),
        ('BIND','id_at','01060280',(*h,'slot=2 '),False,False),
        ('BIND','slot','1',(*h,'slot=2 '),False,False),
        ('BIND','state','1',(*h,'slot=2 '),False,False),
        ('BIND','actor','010352B0',(*h,'slot=2 '),False,False),
        ('BIND','main','0106FFFF',(*h,'slot=2 '),False,False),
        ('BIND','hp','100',(*f,'slot=1 '),False,False),
        ('BIND','slot','',(*h,'slot=1 '),True,False),
        ('FIELD','owner','010352B0',h,False,False),
        ('FIELD','vowner','010352B0',h,False,False),
        ('FIELD','pose','FF030580',h,False,False),
        ('FIELD','vpose','FF030580',h,False,False),
        ('FIELD','vxpos','999',h,False,False),
        ('FIELD','vypos','999',h,False,False),
        ('FIELD','xraw','00000000',h,False,False),
        ('FIELD','vxraw','00000000',h,False,False),
        ('FIELD','flags','00000000',h,False,False),
        ('FIELD','body','00000012',h,False,False),
        ('FIELD','vflags','00000001',h,False,False),
        ('FIELD','frame','',h,True,False),
        ('FIELD','flags','00000004',f,False,True),
        ('FIELD','action','273',f,False,True),
        ('EVENT','a1','01060EA0',('kind=velocity ',),False,False),
        ('EVENT','a8','010352B0',('kind=release ',),False,False),
        ('HEALTH','slot','2',('slot=1 ',),False,False),
        ('HEALTH','pc','FF836710',(),False,False),
        ('HEALTH','a13','0106FFFF',(),False,False),
        ('OWN_REGAIN','flags','00000010',(),False,False),
        ('VICTIM_REGAIN','vtrail','01036540',(),False,False),
        ('FOLLOW_REGAIN','gravity','00008000',(),False,False),
        ('RESULT','cpu_slot','1',(),False,False),
        ('RESULT','schema','8',(),False,False),
        ('RESULT','frame','9999',(),False,False),
    ]:
        MUTATIONS.append((case,tag,key,value,contains,remove,mirror))

for case,tag,key,value,contains,remove,mirror in MUTATIONS:
    def test(self,case=case,tag=tag,key=key,value=value,contains=contains,remove=remove,mirror=mirror):
        self.reject(case,self.mutate(case,tag,key,value,contains,remove,mirror))
    setattr(OppositeSlot,'test_'+case+'_'+tag+'_'+key+'_'+str(len(OppositeSlot.__dict__)),test)

if __name__=='__main__':unittest.main()
