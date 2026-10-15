import re
import unittest
from pathlib import Path
from verify_native_pit_scene_v602_v4 import verify_log

ROOT=Path(__file__).resolve().parents[1]


class PitScene(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={f:(ROOT/f'audit_v603_native_pit_{f}_p1/run.log').read_text(encoding='utf-8-sig')for f in ('kano','sonya')}
        cls.references={'kano':(ROOT/'audit_v592_pit_actual_lookup_kano_p1/run.log').read_text(encoding='utf-8-sig'),
                        'sonya':(ROOT/'audit_v599_native_pit_sonya_p1_uppercut/run.log').read_text(encoding='utf-8-sig')}

    def change(self,tag,selector,old,new,fighter='kano'):
        original=self.logs[fighter];lines=original.splitlines();changed=False
        for i,line in enumerate(lines):
            if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ') and selector in line and old in line:
                lines[i]=line.replace(old,new,1);changed=True;break
        self.assertTrue(changed,'Nonvacuous mutation')
        with self.assertRaises(ValueError):verify_log('\n'.join(lines),fighter,self.references[fighter])

    def test_actual_kano(self):self.assertTrue(verify_log(self.logs['kano'],'kano',self.references['kano'])['passed'])
    def test_actual_sonya(self):self.assertTrue(verify_log(self.logs['sonya'],'sonya',self.references['sonya'])['passed'])
    def test_missing_second_lookup(self):self.change('PIT_LOOKUP','frame=16843','MK2_NAT_CAMPAIGN_PIT_LOOKUP','OMITTED')
    def test_wrong_actual_id(self):self.change('PIT_LOOKUP','frame=16784',' id=17 ',' id=1 ')
    def test_sonya_alias(self):self.change('PIT_ROM','id=18','value=FF181200','value=FF85E830',fighter='sonya')
    def test_wrong_coordinates(self):self.change('PIT_COORDINATES','operand=','kano=004000C0','kano=00B00080')
    def test_kano_clipped(self):self.change('DRAW','a0=FF182000',' y=64 ',' y=176 ')
    def test_sonya_sideways(self):self.change('DRAW','a0=FF182180',' x=192 ',' x=224 ',fighter='sonya')
    def test_wrong_phase(self):self.change('DRAW','a0=FF182040','a0=FF182040','a0=FF182000')
    def test_wrong_cadence(self):self.change('DRAW','a0=FF182040','frame=16788','frame=16789')
    def test_wrong_component(self):self.change('COMPONENT','source=FF182000','value=FF184000','value=FF184300')
    def test_unbounded_component(self):self.change('COMPONENT','source=FF182020','value=00000000','value=9F9F9F9F')
    def test_overrun_stride(self):self.change('COMPONENT','source=FF182020','dst=0105EDA0','dst=010602F0')
    def test_health_corruption(self):self.change('HEALTH','frame=16584','after=0','after=32382')
    def test_false_stock_sentinel(self):self.change('HEALTH','after=65535','pc=FF9DECE0','pc=FF838A10')
    def test_lost_stock_sentinel_recovery(self):self.change('HEALTH','before=65535','after=4','after=5')
    def test_skipped_scene_completion(self):self.change('TRANSITION','before=9 after=5','pc=FF820390','pc=FF80C9C0')
    def test_proxy_after_continue(self):self.change('FIGHT','selection=8','human=17:17','human=1:1')
    def test_no_paid_coin(self):
        original=self.logs['kano'];lines=[line for line in original.splitlines()if not(line.startswith('MK2_NAT_CAMPAIGN_INPUT ')and 'button=Coin 'in line and 17143<int(re.search(r'frame=(\d+)',line)[1])<17457)]
        self.assertNotEqual('\n'.join(lines),original)
        with self.assertRaises(ValueError):verify_log('\n'.join(lines),'kano',self.references['kano'])
    def test_truncated_terminal(self):self.change('RESULT','schema=9','frame=21883','frame=18000')
    def test_observed_reset(self):self.change('RESULT','schema=9','reset=-1','reset=16955')
    def test_observer_failure(self):
        with self.assertRaises(ValueError):verify_log(self.logs['kano']+'\n[LUA ERROR] failed','kano')
    def test_wrong_slot(self):self.change('PIT_LOOKUP','frame=16784','human_slot=1','human_slot=2')


class PitPhysicalSlots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={f:(ROOT/f'audit_v610_native_pit_{f}_p2/run.log').read_text(encoding='utf-8-sig')for f in ('kano','sonya')}

    def mutate(self,fighter,tag,old,new,selector=''):
        lines=self.logs[fighter].splitlines();changed=False
        for i,line in enumerate(lines):
            if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')and old in line and selector in line:
                lines[i]=line.replace(old,new,1);changed=True;break
        self.assertTrue(changed,'Nonvacuous actual P2 mutation')
        with self.assertRaises(ValueError):verify_log('\n'.join(lines),fighter,side=2)

    def test_actual_kano_p2(self):self.assertTrue(verify_log(self.logs['kano'],'kano',side=2)['passed'])
    def test_actual_sonya_p2(self):self.assertTrue(verify_log(self.logs['sonya'],'sonya',side=2)['passed'])
    def test_wrong_kano_cache(self):self.mutate('kano','DRAW','cache=0105F230','cache=0105ED30','a0=FF182000')
    def test_wrong_sonya_cache(self):self.mutate('sonya','DRAW','cache=0105F230','cache=0105ED30','a0=FF182180')
    def test_wrong_p2_destination(self):self.mutate('kano','COMPONENT','dst=0105F230','dst=0105ED30','source=FF182000')
    def test_wrong_p2_zero_terminator(self):self.mutate('sonya','COMPONENT','source=FF1821A0 value=00000000','source=FF1821A0 value=FF184300')
    def test_wrong_declared_side(self):
        with self.assertRaises(ValueError):verify_log(self.logs['sonya'],'sonya',side=1)
    def test_wrong_p1_cache(self):
        original=(ROOT/'audit_v603_native_pit_kano_p1/run.log').read_text(encoding='utf-8-sig')
        lines=original.splitlines()
        for i,line in enumerate(lines):
            if line.startswith('MK2_NAT_CAMPAIGN_DRAW ')and 'a0=FF182000 'in line:
                lines[i]=line.replace('cache=0105ED30','cache=0105F230',1);break
        changed='\n'.join(lines)
        self.assertNotEqual(changed,original)
        with self.assertRaises(ValueError):verify_log(changed,'kano',side=1)


if __name__=='__main__':unittest.main(verbosity=2)
