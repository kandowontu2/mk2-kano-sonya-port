"""Current actual Pit state baselines and nonvacuous rejected corruptions."""
import re
import unittest
import inspect_current_pit_display_audio_v635 as capture

s=capture.scene


class Pit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={name:(s.ROOT/name/'run.log').read_text(encoding='utf-8-sig') for name in capture.CASES}
        for name,(fighter,side) in capture.CASES.items():
            assert s.verify_log(cls.logs[name],fighter,side=side)['passed']

    def test_two_current_native_scene_continuations(self):
        for name,(fighter,side) in capture.CASES.items():
            proof=s.verify(s.ROOT/name,fighter,side=side)
            self.assertTrue(proof['passed'])
            self.assertEqual(proof['native_falling_groups'],20)
            self.assertEqual(proof['native_impact_groups'],1)
            self.assertFalse(proof['fullPortAcceptance'])

    def test_no_pit_scout_is_not_a_scene_pass(self):
        for fighter in ('kano','sonya'):
            log=(s.ROOT/f'audit_v671_current_pit_{fighter}_p1/run.log').read_text(encoding='utf-8-sig')
            with self.assertRaises(ValueError):s.verify_log(log,fighter,side=1)

    def mutate(self,name,tag,field,value,remove=False,predicate=lambda r:True):
        lines=self.logs[name].splitlines(keepends=True);changed=0
        for i,line in enumerate(lines):
            if not line.startswith('MK2_NAT_CAMPAIGN_'+tag+' '):continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if field not in row or not predicate(row):continue
            lines[i]='' if remove else re.sub(r'\b'+field+r'=\S+',field+'='+str(value),line,count=1)
            changed+=int(lines[i]!=line)
            break
        self.assertEqual(changed,1,'Actual recorded mutation target must change')
        return ''.join(lines)


def corruption(tag,field,value,predicate=lambda r:True,remove=False):
    def test(self):
        for name,(fighter,side) in capture.CASES.items():
            # Native mode-9 intro draws precede the own falling sequence;
            # they are not the imported stream tested by this contract.
            identity=17 if fighter=='kano' else 18
            first=0xff182000+(identity-17)*6*64
            def actual_target(row):
                if tag=='PIT_ROM' and int(row['id'])!=identity:return False
                if tag=='DRAW' and not first<=int(row['a0'],16)<=first+5*64:return False
                if tag=='COMPONENT' and not first<=int(row['source'],16)<=first+5*64+32:return False
                return predicate(row)
            log=self.mutate(name,tag,field,value,remove,actual_target)
            with self.assertRaises((ValueError,KeyError)):s.verify_log(log,fighter,side=side)
    return test


for label,tag,field,value,predicate,remove in (
    ('runtime_own_pointer','PIT_ROM','value','00000000',lambda r:int(r['id']) in (17,18),False),
    ('lookup_id','PIT_LOOKUP','id','1',lambda r:True,False),
    ('lookup_table_slot','PIT_LOOKUP','table_slot','1',lambda r:True,False),
    ('lookup_pc','PIT_LOOKUP','pc','00000000',lambda r:True,False),
    ('lookup_owner','PIT_LOOKUP','a8','00000000',lambda r:True,False),
    ('lookup_main','PIT_LOOKUP','a13','00000000',lambda r:True,False),
    ('missing_impact_lookup','PIT_LOOKUP','frame','0',lambda r:True,True),
    ('group_cadence','DRAW','frame','0',lambda r:r['entry']=='FF838790',False),
    ('group_origin','DRAW','x','0',lambda r:r['entry']=='FF838790',False),
    ('group_cache','DRAW','cache','00000000',lambda r:r['entry']=='FF838790',False),
    ('group_proxy','DRAW','actor_id','1',lambda r:r['entry']=='FF838790',False),
    ('component_stride','COMPONENT','dst','00000000',lambda r:True,False),
    ('component_source','COMPONENT','value','00000000',lambda r:True,False),
    ('missing_native_completion','PIT_EXIT','frame','0',lambda r:True,True),
    ('early_native_completion','PIT_EXIT','frame','0',lambda r:True,False),
    ('old_schema','RESULT','schema','9',lambda r:True,False),
    ('reset','RESULT','reset','1',lambda r:True,False),
):
    setattr(Pit,'test_reject_'+label,corruption(tag,field,value,predicate,remove))


if __name__=='__main__':unittest.main(verbosity=2)
