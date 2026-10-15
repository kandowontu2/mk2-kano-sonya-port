"""Nonvacuous current CPU contact/recovery baselines and corruptions.

Use observed phase-relative timestamps, never old-build hardcoded frames.
Mutations of duplicated continuation fields affect both streams where requested.
"""
import re
import unittest
import inspect_current_cpu_campaign_v635 as campaign

o=campaign.ordinary;s=campaign.special;n=campaign.natural
PAIRS={
    'leg_ordinary':('audit_v661_cpu_pair_cage_boot605','cage','ordinary'),
    'choke_ordinary':('audit_v664_cpu_close_cage_boot604','cage','ordinary'),
    'square':('audit_v661_cpu_pair_liu_kang_boot605','liu_kang','square'),
    'bicycle_mirror':('audit_v663_cpu_guard_sonya_boot605','sonya','bicycle'),
}
ACCEPTED=tuple(name for name in campaign.PAIR_PROFILES if name not in {
    'audit_v663_cpu_guard_cage_boot605','audit_v663_cpu_guard_sub_zero_boot605',
    'audit_v663_cpu_guard_mileena_boot605','audit_v663_cpu_guard_kitana_boot605'})


class CurrentCPU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={key:(n.ROOT/name/'run.log').read_text(encoding='utf-8-sig')
                  for key,(name,player,profile) in PAIRS.items()}
        for key in PAIRS:
            proof=cls.verify(key,cls.logs[key])
            assert proof['passed'],('Nonvacuous current baseline',key,proof)

    @staticmethod
    def verify(key,log):
        _,player,profile=PAIRS[key]
        return o.verify_log(log,player) if profile=='ordinary' else s.verify_log(log,player,profile)

    def mutate(self,key,tags,field,value,predicate=lambda r:True,remove=False,all_matches=False):
        lines=self.logs[key].splitlines(keepends=True);count=0
        for i,line in enumerate(lines):
            if not any(line.startswith('MK2_CPU_PAIR_'+tag+' ') for tag in tags):continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if field not in row or not predicate(row):continue
            lines[i]='' if remove else re.sub(r'\b'+field+r'=\S+',field+'='+str(value),line,count=1)
            if lines[i]!=line:count+=1
            if not all_matches:break
        self.assertGreater(count,0,'Mutation must change actual recorded evidence')
        return ''.join(lines)

    def reject(self,key,log):self.assertFalse(self.verify(key,log)['passed'])

    def held(self,key):
        step=next(r for r in o.rows(self.logs[key],'EVENT') if r['kind']=='step')
        return step['frame']+1

    def test_all_nine_declared_full_pairs(self):
        self.assertEqual(len(ACCEPTED),9)
        for name in ACCEPTED:
            player,profile=campaign.PAIR_PROFILES[name]
            proof=o.verify(n.ROOT/name,player) if profile=='ordinary' else s.verify(n.ROOT/name,player,profile)
            self.assertTrue(proof['passed'],(name,proof))
            self.assertEqual(proof['held_fields'],70 if proof['target']=='kano' else 46)
            self.assertEqual(proof['damage'],32 if proof['target']=='kano' else 35)
            self.assertFalse(proof['whole_character_integration_complete'])

    def test_two_current_natural_campaign_contracts(self):
        for name in ('kano_boot605','sonya_boot601'):
            proof=n.verify(n.ROOT/('audit_v662_cpu_'+name))
            self.assertTrue(proof['passed'],proof)
            self.assertFalse(proof['whole_character_integration_complete'])

    def test_other_natural_campaigns_are_not_waived(self):
        for name in ('kano_boot606','sonya_boot604'):
            self.assertFalse(n.verify(n.ROOT/('audit_v662_cpu_'+name))['passed'])

    def test_no_target_short_capture_is_not_a_pass(self):
        self.assertFalse(n.verify(n.ROOT/'audit_v660_cpu_kano_boot605')['passed'])

    def test_specials_cannot_be_relabelled(self):
        for key,wrong in (('square','bicycle'),('bicycle_mirror','square')):
            self.assertFalse(s.verify_log(self.logs[key],PAIRS[key][1],wrong)['passed'])
            self.assertFalse(o.verify_log(self.logs[key],PAIRS[key][1])['passed'])

    def test_missing_pair_is_not_completion(self):
        self.reject('leg_ordinary',self.mutate('leg_ordinary',('COMPLETE',),'frame',0,remove=True))

    def test_summary_only_is_not_proof(self):
        log=re.sub(r'^MK2_CPU_PAIR_(FIELD|FOLLOW_FIELD|EVENT|HEALTH|FLAG) [^\r\n]*\r?\n','',self.logs['square'],flags=re.M)
        self.reject('square',log)

    def test_corrupted_mirrored_continuation_owner(self):
        done=o.rows(self.logs['leg_ordinary'],'COMPLETE')[0]['frame']
        self.reject('leg_ordinary',self.mutate('leg_ordinary',('FIELD','FOLLOW_FIELD'),'owner','00000000',
                    lambda r:int(r['frame'])==done+1,all_matches=True))

    def test_ordinary_damage_cannot_execute_as_victim(self):
        done=o.rows(self.logs['leg_ordinary'],'COMPLETE')[0]
        self.reject('leg_ordinary',self.mutate('leg_ordinary',('HEALTH',),'a8',f"{done['vactor']:08X}",
                    lambda r:int(r['frame'])>done['frame'] and r['slot']=='2' and r['before']!=r['after']))

    def test_unlogged_continuation_health_is_rejected(self):
        done=o.rows(self.logs['leg_ordinary'],'COMPLETE')[0]['frame']
        self.reject('leg_ordinary',self.mutate('leg_ordinary',('HEALTH',),'frame',0,
                    lambda r:int(r['frame'])>done and r['slot']=='2' and r['before']!=r['after'],remove=True))

    def test_later_real_cleanup_effect_required(self):
        ready=o.rows(self.logs['leg_ordinary'],'RESULT')[0]['follow_regain']
        self.reject('leg_ordinary',self.mutate('leg_ordinary',('FLAG',),'frame',0,
                    lambda r:int(r['frame'])==ready and r['slot']=='1' and r['kind']=='flags' and
                             int(r['before'],16)&0x14!=0,remove=True,all_matches=True))

    def test_ordinary_later_cleanup_opcode(self):
        ready=o.rows(self.logs['leg_ordinary'],'RESULT')[0]['follow_regain']
        self.reject('leg_ordinary',self.mutate('leg_ordinary',('FLAG',),'op0','0000',
                    lambda r:int(r['frame'])==ready and r['slot']=='1' and r['kind']=='body',all_matches=True))

    def test_first_ordinary_regain_is_not_coincidental_later_callback(self):
        self.reject('leg_ordinary',self.mutate('leg_ordinary',('FOLLOW_REGAIN',),'frame',9999))

    def test_cold_proxy_selection_rejected(self):
        self.reject('square',self.logs['square'].replace('human_id=1 ','human_id=17 '))


def make_hold_mutation(key,field,value,remove=False):
    def test(self):
        at=self.held(key)
        self.reject(key,self.mutate(key,('FIELD',),field,value,
                    lambda r:int(r['frame'])==at,remove=remove))
    return test


for key in PAIRS:
    for field,value in (('state','1'),('vstate','0'),('roster','1'),('owner','00000000'),
                        ('pose','00000000'),('vpose','00000000'),('vxpos','-999'),
                        ('vypos','-999'),('vx','00010000'),('vaction','0'),('vhp','1')):
        setattr(CurrentCPU,'test_'+key+'_held_'+field,make_hold_mutation(key,field,value))
    setattr(CurrentCPU,'test_'+key+'_missing_held_callback',make_hold_mutation(key,'frame',0,True))


def make_native_mutation(key,tag,field,value,predicate):
    def test(self):
        completed=o.rows(self.logs[key],'COMPLETE')[0]
        started=next(r for r in o.rows(self.logs[key],'ENTRY') if r['cycle']==completed['cycle'])
        # Contract scope is the declared completed contact, not earlier ordinary
        # attacks. Keep the rejected first attempt; target its real damage store.
        def in_contact(row):
            return (tag=='RESULT' or started['frame']<=int(row['frame'])<=completed['frame']) and predicate(row)
        self.reject(key,self.mutate(key,(tag,),field,value,in_contact))
    return test


for key in PAIRS:
    for label,tag,field,value,predicate in (
        ('health_writer','HEALTH','pc','00000000',lambda r:r['before']!=r['after']),
        ('damage_register','EVENT','a10','00000001',lambda r:r['kind']=='damage'),
        ('fling_gravity','EVENT','a2','00000000',lambda r:r['kind']=='fling'),
        ('native_catch_descriptor','EVENT','word','0000',lambda r:r['kind']=='attack'),
        ('own_dirty_ready','OWN_REGAIN','flags','00000010',lambda r:True),
        ('victim_dirty_ready','VICTIM_REGAIN','vbody','0000001E',lambda r:True),
        ('terminal_schema','RESULT','schema','6',lambda r:True),
    ):
        setattr(CurrentCPU,'test_'+key+'_'+label,make_native_mutation(key,tag,field,value,predicate))


if __name__=='__main__':unittest.main()
