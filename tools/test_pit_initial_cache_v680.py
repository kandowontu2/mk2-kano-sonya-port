"""Nonvacuous current native-initialization/render/sound regressions."""
import copy
import re
import struct
import unittest
import numpy as np
import inspect_current_pit_raster_v680_v3 as inspection
import verify_pit_initial_cache_v680_v2 as initial
import verify_native_pit_scene_v680_v1 as scene
import inspect_natural_pit_saved_passes_v680_v2 as raster

class Pit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures=[]
        for name,(fighter,side,_)in inspection.CASES.items():
            folder=scene.ROOT/name
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            compact='\n'.join(line for line in log.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and
                              not line.startswith(('MK2_NAT_CAMPAIGN_FLOOR_','MK2_NAT_CAMPAIGN_SHADOW_')))
            proof=scene.verify_log(compact,fighter,side=side)
            initlog='\n'.join(line for line in log.splitlines()if line.startswith(('MK2_NAT_CAMPAIGN_PIT_INITIAL ','MK2_NAT_CAMPAIGN_FLOOR_QUEUE ')))
            groups=inspection.data(folder)[0]
            cls.fixtures.append((folder,fighter,side,compact,initlog,proof,groups))
        cls.original=(scene.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        cls.payload=(scene.ROOT/scene.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()

    def test_both_actual_current_preloads_and_first_body_queues(self):
        for folder,_,_,_,_,proof,_ in self.fixtures:
            self.assertTrue(initial.verify(folder,proof)['passed'])

    def test_all_19_exact_native_branch_and_register_masks(self):
        for identity in range(19):
            with self.subTest(identity=identity):self.assertEqual(initial.execute(identity)['id'],identity)

    def test_runtime_stub_and_unused_tail(self):
        for folder,*_ in self.fixtures:
            code=initial.guest_bytes((folder/'pit_initial_guest_code.bin').read_bytes())
            hook=initial.guest_bytes((folder/'pit_initial_guest_hook.bin').read_bytes())
            self.assertTrue(initial.stub(code,hook))
            for byte in (0,2,12,22,28,34,40,46,52,56,63,64,127):
                mutated=bytearray(code);mutated[byte]^=1
                with self.subTest(byte=byte),self.assertRaises(ValueError):initial.stub(mutated,hook)
            with self.assertRaises(ValueError):initial.stub(code,b'\0'*6)

    def test_redundant_native_bit_address_reads_cannot_hide_corruption(self):
        raw=b''.join(bytes((i,))*8 for i in range(128))
        self.assertEqual(initial.guest_bytes(raw),bytes(range(128)))
        bad=bytearray(raw);bad[7]^=1
        with self.assertRaises(ValueError):initial.guest_bytes(bad)
        with self.assertRaises(ValueError):initial.guest_bytes(raw[:-1])

    def test_actual_own_rom_composites_and_native_fifo_dispatch(self):
        for *_,proof,groups in self.fixtures:
            self.assertEqual(len(inspection.body_queues(groups,self.payload,self.original,proof)['poses']),6)

    def test_actual_impact_camera_and_serialized_native_voice(self):
        for *_,proof,groups in self.fixtures:
            result=inspection.native_impact(groups,proof,self.original)
            self.assertEqual(result['native_DCS_commands'][0],0x254)
            self.assertEqual(result['native_DCS_commands'][1],0x348 if proof['actual_id']==17 else 0x2e7)

    def change(self,log,tag,field,value,predicate=lambda r:True,remove=False):
        lines=log.splitlines();changed=0
        for i,line in enumerate(lines):
            if not line.startswith('MK2_NAT_CAMPAIGN_'+tag+' '):continue
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if field not in row or not predicate(row):continue
            replacement=''if remove else re.sub(r'\b'+field+r'=\S+',field+'='+str(value),line,count=1)
            changed=int(replacement!=line);lines[i]=replacement;break
        self.assertEqual(changed,1,'Mutation must alter an actual recorded target')
        return '\n'.join(lines)

def initial_corruption(tag,field,value,predicate=lambda r:True,remove=False):
    def test(self):
        for _,_,_,_,log,proof,_ in self.fixtures:
            broken=self.change(log,tag,field,value,predicate,remove)
            with self.assertRaises(ValueError):initial.verify_log(broken,proof)
    return test

for label,tag,field,value,predicate,remove in (
    ('missing_constructor','PIT_INITIAL','frame','0',lambda r:True,True),
    ('wrong_entry','PIT_INITIAL','entry','00000000',lambda r:True,False),
    ('wrong_pc','PIT_INITIAL','pc','00000000',lambda r:True,False),
    ('wrong_field','PIT_INITIAL','frame','0',lambda r:True,False),
    ('proxy_id','PIT_INITIAL','id','1',lambda r:True,False),
    ('stack_imbalance','PIT_INITIAL','sp','01000000',lambda r:r['entry']=='FFFC9DF0',False),
    ('wrong_main','PIT_INITIAL','a13','00000000',lambda r:True,False),
    ('stale_cache','PIT_INITIAL','pose','00000000',lambda r:r['entry']=='FFFC9DF0',False),
    ('wrong_coordinate_MOVI','PIT_INITIAL','a0','FF85CB40',lambda r:r['entry']=='FFFC9DF0',False),
    ('stale_first_fifo','FLOOR_QUEUE','pose','00000000',lambda r:True,False),
    ('late_first_fifo','FLOOR_QUEUE','frame','0',lambda r:True,False),
    ('wrong_first_part','FLOOR_QUEUE','part','1',lambda r:True,False),
):setattr(Pit,'test_reject_'+label,initial_corruption(tag,field,value,predicate,remove))
for register in range(1,8):
    setattr(Pit,'test_reject_clobbered_a'+str(register),initial_corruption('PIT_INITIAL','a'+str(register),'76543210',lambda r:r['entry']=='FFFC9DF0'))

def scene_corruption(tag,field,value,remove=False):
    def test(self):
        for _,fighter,side,log,_,proof,_ in self.fixtures:
            first=0xff182000+(proof['actual_id']-17)*384
            def target(row):
                if tag=='DRAW':return row['entry']=='FF838790' and first<=int(row['a0'],16)<=first+320
                if tag=='COMPONENT':return first<=int(row['source'],16)<=first+352
                return True
            broken=self.change(log,tag,field,value,target,remove)
            with self.assertRaises((ValueError,KeyError)):scene.verify_log(broken,fighter,side=side)
    return test
for label,tag,field,value,remove in (
    ('missing_preload_copy','DRAW','frame','0',True),
    ('proxy_preload_group','DRAW','actor_id','1',False),
    ('preload_cache','DRAW','cache','00000000',False),
    ('preload_component','COMPONENT','value','00000000',False),
    ('component_stride','COMPONENT','dst','00000000',False),
    ('wrong_native_impact','PIT_LOOKUP','frame','0',False),
    ('missing_episode_exit','PIT_EXIT','frame','0',True),
    ('wrong_total_episodes','RESULT','pit_episodes','99',False),
    ('reset','RESULT','reset','1',False),
):setattr(Pit,'test_reject_scene_'+label,scene_corruption(tag,field,value,remove))

def impact_corruption(tag,field,value,predicate):
    def test(self):
        for *_,proof,original_groups in self.fixtures:
            groups=copy.deepcopy(original_groups)
            targets=[row for row in groups[tag]if predicate(row,proof)]
            self.assertTrue(targets,'Actual native impact target exists')
            self.assertNotEqual(targets[0][field],value);targets[0][field]=value
            with self.assertRaises(ValueError):inspection.native_impact(groups,proof,self.original)
    return test
for label,tag,field,value,predicate in (
    ('shake_argument','PIT_NATIVE','a11',0,lambda r,p:r['frame']==p['pit_impact']and r['entry']==0xff9e1290),
    ('male_female_group','PIT_NATIVE','a0',0,lambda r,p:r['frame']==p['pit_impact']and r['entry']==0xffa12530 and r['a0']==(0xcc if p['actual_id']==17 else 0xce)),
    ('voice_owner','PIT_NATIVE','a8',0,lambda r,p:r['frame']==p['pit_impact']and r['entry']==0xffa12530 and r['a0']==0xcf),
    ('wrong_DCS_byte','PIT_SOUND_PORT','data',0,lambda r,p:r['frame']==p['pit_impact']and r['pc']==0xffa13d60),
    ('wrong_DCS_pc','PIT_SOUND_PORT','pc',0,lambda r,p:r['frame']==p['pit_impact']),
    ('camera_cadence','FLOOR_SNAP','cameraY',99,lambda r,p:r['frame']==p['pit_impact']+4),
):setattr(Pit,'test_reject_impact_'+label,impact_corruption(tag,field,value,predicate))

class ScaledNativePass(unittest.TestCase):
    def test_source_step_not_busy_time_floor_or_sprite_stretch(self):
        replay=raster.Replay.__new__(raster.Replay)
        replay.words=np.zeros((512,512),dtype=np.uint16)
        replay.body=np.zeros((512,512),dtype=np.uint8)
        replay.shadow=np.zeros((512,512),dtype=bool)
        replay.decode=lambda *args:np.arange(1,13,dtype=np.uint8).reshape(3,4)
        d=dict(scaleX=384,scaleY=384,source=0,command=0x8002,width=4,height=3,skip=0,x=10,y=20,
               left=0,right=511,top=0,bottom=511,palette=0x300,color=0,slot=0)
        replay.dma(d)
        self.assertEqual(replay.words[20:22,10:13].tolist(),[[0x301,0x302,0x304],[0x305,0x306,0x308]])
        self.assertEqual(np.count_nonzero(replay.words),6)
        replay.words[:]=0;d['command']|=0x30
        replay.dma(d)
        self.assertEqual(replay.words[19:21,8:11].tolist(),[[0x308,0x306,0x305],[0x304,0x302,0x301]])
        self.assertEqual(np.count_nonzero(replay.words),6)
        d['command']|=128
        with self.assertRaises(AssertionError):replay.dma(d)

if __name__=='__main__':unittest.main(verbosity=2)
