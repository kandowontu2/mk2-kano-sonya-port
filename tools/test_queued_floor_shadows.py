"""Real captures plus in-memory counterexamples; never rewrite evidence."""
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
import verify_queued_floor_shadows as v
import inspect_ground_presentation as p

def rgb(path):return np.asarray(Image.open(path).convert('RGB')).copy()

def first_mask():
    folder=v.ROOT/'audit_v438_ground_kano_p1'
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    snap=p.rows(log,'SNAP')[0];frame=snap['frame']-2
    buffers={r['key']:r for r in p.rows(log,'GFX')}
    palettes={r['bank']:np.array([[int(c[i:i+2],16) for i in (0,2,4)] for c in r['colors'].split(',')],dtype=np.uint8) for r in p.rows(log,'PALETTE')}
    draw=[r for r in p.rows(log,'DMA') if r['frame']==frame]
    body,bodymask,slots,stock,native=p.render(draw,buffers,palettes,p.rows(log,'FIELD'),p.rows(log,'PART'),
        p.rows(log,'DMA_CACHE'),p.descriptor_geometry((v.ROOT/'diagnostic_v323_native_shang_morph_payload/roms/mk2ks/mk2ks.mdata').read_bytes()))
    mask=native[:254,56:456]&~bodymask[:254,56:456];mask[:44]=False
    return folder/'snap'/snap['file'],mask

class Counterexamples(unittest.TestCase):
    def test_restore_old_missing_shadow_rejected(self):
        path,mask=first_mask()
        previous=v.ROOT/'audit_v427_ground_kano_p1/snap'/path.name
        self.assertGreater(mask.sum(),500)
        self.assertTrue(np.all(rgb(path)[mask]==0))
        self.assertFalse(np.all(rgb(previous)[mask]==0))
        with self.assertRaisesRegex(ValueError,'floor-shadow pixel'):
            v.verify_case('kano',1,lambda item:rgb(previous if item==path else item))

    def test_non_native_shadow_color_rejected(self):
        path,mask=first_mask();changed=rgb(path);changed[mask]=[8,0,0]
        with self.assertRaisesRegex(ValueError,'floor-shadow pixel'):
            v.verify_case('kano',1,lambda item:changed if item==path else rgb(item))

    def test_one_frame_shadow_flicker_rejected(self):
        path,mask=first_mask();changed=rgb(path)
        changed[mask]=rgb(v.ROOT/'audit_v427_ground_kano_p1/snap'/path.name)[mask]
        with self.assertRaisesRegex(ValueError,'floor-shadow pixel'):
            v.verify_case('kano',1,lambda item:changed if item==path else rgb(item))

    def test_shifted_shadow_rejected(self):
        path,mask=first_mask();changed=rgb(path)
        changed[mask]=rgb(v.ROOT/'audit_v427_ground_kano_p1/snap'/path.name)[mask]
        shifted=np.roll(mask,1,axis=0);changed[shifted]=0
        with self.assertRaises(ValueError):v.verify_case('kano',1,lambda item:changed if item==path else rgb(item))

    def test_fighter_recolor_rejected(self):
        path,mask=first_mask();changed=rgb(path);changed[120,100]=[255,0,255]
        with self.assertRaises(ValueError):v.verify_case('kano',1,lambda item:changed if item==path else rgb(item))

    def test_stock_frame_change_rejected(self):
        folder=v.ROOT/'audit_v438_ground_sub_zero_p1'
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        path=folder/'snap'/p.rows(log,'SNAP')[0]['file'];changed=rgb(path);changed[240,140]=[255,0,255]
        with self.assertRaisesRegex(ValueError,'Stock control frame'):
            v.verify_case('sub_zero',1,lambda item:changed if item==path else rgb(item))

    def test_selection_presentation_change_rejected(self):
        folder=v.ROOT/'audit_v439_shadow_ui_sonya_p2'
        data=(folder/'run.log').read_text(encoding='utf-8-sig').replace('MK2_UI_','MK2_GROUND_')
        path=folder/'snap'/p.rows(data,'SNAP')[0]['file'];changed=rgb(path);changed[24,323]=[255,0,255]
        with self.assertRaisesRegex(ValueError,'Selection/ladder'):
            v.verify_ui('sonya',2,lambda item:changed if item==path else rgb(item))

    def test_name_shadow_change_rejected(self):
        folder=v.ROOT/'audit_v439_shadow_ui_kano_p1'
        data=(folder/'run.log').read_text(encoding='utf-8-sig').replace('MK2_UI_','MK2_GROUND_')
        live=p.rows(data,'LIVE')[0]['frame']
        snap=next(r for r in p.rows(data,'SNAP') if r['frame']>=live)
        path=folder/'snap'/snap['file'];changed=rgb(path)
        ys,xs=np.where(np.all(changed[27:44]==[66,0,0],axis=2))
        self.assertGreater(len(xs),20);changed[ys[0]+27,xs[0]]=[0,0,0]
        with self.assertRaisesRegex(ValueError,'Lifebar names'):
            v.verify_ui('kano',1,lambda item:changed if item==path else rgb(item))

    def test_mode7_ladder_cannot_be_treated_as_arena(self):
        folder=v.ROOT/'audit_v439_shadow_ui_kano_p1'
        data=(folder/'run.log').read_text(encoding='utf-8-sig').replace('MK2_UI_','MK2_GROUND_')
        modes={r['frame']:r['mode'] for r in p.rows(data,'OUTSIDE')}
        candidates=[r for r in p.rows(data,'SNAP') if r['scene']=='transition' and 120<r['age']<300 and modes.get(r['frame'])==7]
        self.assertTrue(candidates)
        path=folder/'snap'/candidates[0]['file'];changed=rgb(path)
        ys,xs=np.where(changed[180:240,40:360].max(2)>64)
        self.assertGreater(len(xs),20);changed[ys[0]+180,xs[0]+40]=0
        with self.assertRaisesRegex(ValueError,'Selection/ladder'):
            v.verify_ui('kano',1,lambda item:changed if item==path else rgb(item))

    def test_arena_intro_cannot_acquire_selection_overlay(self):
        folder=v.ROOT/'audit_v439_shadow_ui_kano_p1'
        path=folder/'snap/ui_1730.png';changed=rgb(path);changed[100,100]=[255,0,255]
        with self.assertRaisesRegex(ValueError,'Arena intro'):
            v.verify_ui('kano',1,lambda item:changed if item==path else rgb(item))

    def test_initial_bad_observer_remains_rejected(self):
        log=(v.ROOT/'audit_v426_ground_kano_p1/run.log').read_text(encoding='utf-8-sig')
        self.assertIn('ready=-1 terminalAge=-1',log)

    def test_original_video_header_restored(self):
        self.assertEqual(v.digest(v.ROOT/'mame-mkp/src/mame/midway/midtunit_v.h'),
                         '8BA30B7AA635EA1FD68CF46697560E58BA7E3FC7A2C760C0881414836FBFD4D5')

class Baselines(unittest.TestCase):pass
for fighter,side in v.CASES:
    def case(self,f=fighter,s=side):self.assertEqual(v.verify_case(f,s)['snapshots'],117)
    setattr(Baselines,f'test_ground_{fighter}_p{side}',case)
for side in (1,2):
    for fighter in ('kano','sonya'):
        def case(self,f=fighter,s=side):self.assertTrue(v.verify_ui(f,s)['allNativeUiRecordsBitExact'])
        setattr(Baselines,f'test_ui_{fighter}_p{side}',case)

if __name__=='__main__':unittest.main()
