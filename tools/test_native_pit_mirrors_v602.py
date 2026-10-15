import unittest
from pathlib import Path
from verify_native_pit_mirrors_v602 import verify_log

ROOT=Path(__file__).resolve().parents[1]


class ActualMirrors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={f:(ROOT/f'audit_v615_{f}_p2_mirror_palette/run.log').read_text(encoding='utf-8-sig')for f in ('kano','sonya')}
        cls.references={'kano':(ROOT/'audit_v611_native_pit_kano_p2_boot604/run.log').read_text(encoding='utf-8-sig'),
                        'sonya':(ROOT/'audit_v613_sonya_p2_mirror_boot605/run.log').read_text(encoding='utf-8-sig')}

    def mutate(self,tag,selector,old,new,fighter='kano'):
        lines=self.logs[fighter].splitlines();changed=False
        for i,line in enumerate(lines):
            if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')and all(token in line for token in selector.split())and old in line:
                lines[i]=line.replace(old,new,1);changed=True;break
        self.assertTrue(changed,'Nonvacuous actual mirror mutation')
        with self.assertRaises(ValueError):verify_log('\n'.join(lines),fighter,self.references[fighter])

    def test_actual_two_kano_episodes(self):self.assertEqual(len(verify_log(self.logs['kano'],'kano',self.references['kano'])['episodes']),2)
    def test_actual_sonya_episode(self):self.assertTrue(verify_log(self.logs['sonya'],'sonya',self.references['sonya'])['passed'])
    def test_old_observer(self):self.mutate('RESULT','schema=11','schema=11','schema=10')
    def test_missing_second_exit(self):self.mutate('PIT_EXIT','episode=2','MK2_NAT_CAMPAIGN_PIT_EXIT','OMITTED')
    def test_second_wrong_id(self):self.mutate('PIT_LOOKUP','episode=2','id=17','id=1')
    def test_second_wrong_actor(self):self.mutate('PIT_LOOKUP','episode=2','a8=0102D6F0','a8=01034230')
    def test_second_wrong_constructor_argument(self):self.mutate('PIT_CONSTRUCTOR','episode=2 entry=FF906EF0','a2=00000000','a2=00000001')
    def test_sonya_wrong_constructor_identity(self):self.mutate('PIT_CONSTRUCTOR','entry=FF906EF0','a0=00000012','a0=00000000','sonya')
    def test_second_wrong_palette_variant(self):self.mutate('PIT_PALETTE','episode=2','variant=0','variant=1')
    def test_second_wrong_palette_pointer(self):self.mutate('PIT_PALETTE','episode=2','pointer=FFFED000','pointer=FFF58800')
    def test_second_wrong_palette_color(self):self.mutate('PIT_PALETTE','episode=2','0000,77BD','0000,77BC')
    def test_sonya_wrong_palette_identity(self):self.mutate('PIT_PALETTE','episode=1','id=18','id=17','sonya')
    def test_missing_palette_observation(self):self.mutate('PIT_PALETTE','episode=2','MK2_NAT_CAMPAIGN_PIT_PALETTE','MK2_NAT_CAMPAIGN_PIT_PALETTE_OMITTED')
    def test_reentrant_palette_observation(self):
        line=next(line for line in self.logs['kano'].splitlines()if line.startswith('MK2_NAT_CAMPAIGN_PIT_PALETTE '))
        with self.assertRaises(ValueError):verify_log(self.logs['kano']+'\n'+line,'kano',self.references['kano'])
    def test_missing_entire_second_episode(self):
        # A self-consistent terminal count must not conceal an episode proven
        # in the unchanged native reference, even if all its local taps vanish.
        original=self.logs['kano'];lines=[]
        for line in original.splitlines():
            if line.startswith('MK2_NAT_CAMPAIGN_PIT_LOOKUP ')and 'episode=2'in line:continue
            if line.startswith('MK2_NAT_CAMPAIGN_RESULT '):line=line.replace('pit_episodes=2','pit_episodes=1').replace('pit_lookups=4','pit_lookups=2')
            lines.append(line)
        self.assertNotEqual('\n'.join(lines),original)
        with self.assertRaises(ValueError):verify_log('\n'.join(lines),'kano',self.references['kano'])
    def test_second_missing_phase(self):self.mutate('DRAW','frame=39028 entry=FF838790','a0=FF182040','a0=FF182000')
    def test_second_wrong_cache(self):self.mutate('DRAW','frame=39025 entry=FF838790','cache=0105F230','cache=0105ED30')
    def test_second_unbounded_component(self):self.mutate('COMPONENT','frame=39025 source=FF182020','value=00000000','value=9F9F9F9F')
    def test_second_wrong_component_stride(self):self.mutate('COMPONENT','frame=39025 source=FF182020','dst=0105F2A0','dst=010602F0')
    def test_second_missing_native_completion(self):self.mutate('TRANSITION','frame=39084 at=010601D0','pc=FF820390','pc=FF80C9C0')
    def test_second_proxy_continue(self):self.mutate('FIGHT','frame=40217','human=17:17','human=1:1')
    def test_changed_actual_input_replay(self):self.mutate('INPUT','frame=604','button=Coin','button=Start')
    def test_actual_mirror_not_declared_p1(self):
        with self.assertRaises(ValueError):verify_log(self.logs['sonya'],'sonya',self.references['sonya'],side=1)
    def test_no_alternate_victim(self):
        # Keep the authentic combat/native-body flags apart: bit40 is the
        # constructor's costume flag; bit10 is also present on normal CPU.
        original=self.logs['kano'];lines=[];changed=False
        for line in original.splitlines():
            if line.startswith('MK2_NAT_CAMPAIGN_BODY '):
                import re
                match=re.search(r'bodies=([0-9A-F]+),',line)
                value=int(match[1],16)
                replacement=f'bodies={value&~0x40:04X},'
                line=line.replace(match[0],replacement,1);changed|=bool(value&0x40)
            lines.append(line)
        self.assertTrue(changed)
        with self.assertRaises(ValueError):verify_log('\n'.join(lines),'kano',self.references['kano'])


if __name__=='__main__':unittest.main(verbosity=2)
