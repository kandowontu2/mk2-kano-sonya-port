"""Actual captures and in-memory regressions; no frozen evidence is rewritten."""
import unittest
import numpy as np
import verify_ko_round_floor_shadows as v
import inspect_ground_presentation as p

class Counterexamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=v.ROOT/'audit_v458_ko_round_kano_p1/snap/ground_3072.png'
        cls.old=v.ROOT/'audit_v457_ko_round_kano_p1/snap/ground_3072.png'
        cls.original=v.rgb(cls.path).copy();cls.before=v.rgb(cls.old).copy()
        cls.restored=np.any(cls.original!=cls.before,axis=2)
        if int(cls.restored.sum())<50:raise AssertionError('Real held corpse has restored shadow pixels')

    def reject_image(self,changed,label=None):
        load=lambda path:changed if path==self.path else v.rgb(path)
        with self.assertRaises(ValueError) if label is None else self.assertRaisesRegex(ValueError,label):
            v.verify_case('kano',1,load)

    def test_old_missing_KO_shadow_rejected(self):
        self.reject_image(self.before,'KO floor-shadow pixel')

    def test_single_held_frame_flicker_rejected(self):
        changed=self.original.copy();changed[self.restored]=self.before[self.restored]
        self.reject_image(changed,'KO floor-shadow pixel')

    def test_miscolored_shadow_rejected(self):
        changed=self.original.copy();changed[self.restored]=[8,0,0]
        self.reject_image(changed,'KO floor-shadow pixel')

    def test_shifted_shadow_rejected(self):
        changed=self.before.copy();changed[np.roll(self.restored,1,axis=0)]=0
        self.reject_image(changed)

    def test_high_screen_selection_overlay_rejected(self):
        changed=self.original.copy();changed[80,80]=[255,0,255]
        self.reject_image(changed,'High-screen')

    def test_foreground_chain_overwrite_rejected(self):
        folder=v.ROOT/'audit_v458_ko_round_kano_p1'
        fg=v.foreground(v.ROOT/'audit_v462_ko_foreground_kano_p1',v.read(folder))
        record=next(r for r in v.original_report('kano',1)['records'] if r['file']==self.path.name)
        colors,mask=fg(record['dmaFrame']);visible=mask&np.all(self.before==colors,axis=2)
        visible[:140]=False
        ys,xs=np.where(visible&np.any(colors!=0,axis=2));self.assertGreater(len(xs),30)
        changed=self.original.copy();changed[ys[-1],xs[-1]]=0
        self.reject_image(changed)

    def test_proxy_character_state_rejected(self):
        log=v.read(v.ROOT/'audit_v458_ko_round_kano_p1')
        with self.assertRaisesRegex(ValueError,'True identity'):
            v.lifecycle(log.replace('id=17 roster=17','id=0 roster=0',1),'kano',1)

    def test_assisted_damage_ledger_rejected(self):
        log=v.read(v.ROOT/'audit_v458_ko_round_kano_p1')
        altered=log.replace('before=161 after=121 pc=FF836700','before=161 after=121 pc=00000000',1)
        self.assertNotEqual(altered,log)
        with self.assertRaisesRegex(ValueError,'genuine native uppercut'):
            v.lifecycle(altered,'kano',1)

    def test_missing_round_two_rejected(self):
        log=v.read(v.ROOT/'audit_v458_ko_round_kano_p1')
        altered='\n'.join(line for line in log.splitlines() if not line.startswith('MK2_GROUND_NEXT_READY '))
        with self.assertRaisesRegex(ValueError,'next-round readiness'):
            v.lifecycle(altered,'kano',1)

    def test_stock_KO_pixel_change_rejected(self):
        folder=v.ROOT/'audit_v458_ko_round_sub_zero_p2'
        snap=next(r for r in p.rows(v.read(folder),'SNAP') if r['age']==1600)
        path=folder/'snap'/snap['file']
        changed=v.rgb(path).copy();changed[245,140]=[255,0,255]
        with self.assertRaisesRegex(ValueError,'Stock KO'):
            v.verify_case('sub_zero',2,lambda item:changed if item==path else v.rgb(item))

    def test_selection_ladder_change_rejected(self):
        folder=v.ROOT/'audit_v459_ko_shadow_ui_sonya_p2'
        snap=p.rows(v.read(folder).replace('MK2_UI_','MK2_GROUND_'),'SNAP')[0]
        path=folder/'snap'/snap['file'];changed=v.rgb(path).copy();changed[24,323]=[255,0,255]
        with self.assertRaisesRegex(ValueError,'Whole selection/ladder'):
            v.verify_ui('sonya',2,lambda item:changed if item==path else v.rgb(item))

    def test_lifebar_name_shadow_change_rejected(self):
        folder=v.ROOT/'audit_v459_ko_shadow_ui_kano_p1';log=v.read(folder).replace('MK2_UI_','MK2_GROUND_')
        live=p.rows(log,'LIVE')[0]['frame'];snap=next(r for r in p.rows(log,'SNAP') if r['frame']>=live)
        path=folder/'snap'/snap['file'];changed=v.rgb(path).copy()
        ys,xs=np.where(np.all(changed[27:44]==[66,0,0],axis=2));self.assertGreater(len(xs),20)
        changed[ys[0]+27,xs[0]]=0
        with self.assertRaisesRegex(ValueError,'Whole selection/ladder'):
            v.verify_ui('kano',1,lambda item:changed if item==path else v.rgb(item))

class ActualCases(unittest.TestCase):pass
for fighter,side in v.CASES:
    def case(self,f=fighter,s=side):self.assertEqual(v.verify_case(f,s)['roundTwoGroundedFields'],61)
    setattr(ActualCases,f'test_KO_round_two_{fighter}_p{side}',case)
for side in (1,2):
    for fighter in ('kano','sonya'):
        def case(self,f=fighter,s=side):self.assertTrue(v.verify_ui(f,s)['allNativeRecordsBitExact'])
        setattr(ActualCases,f'test_UI_{fighter}_p{side}',case)

if __name__=='__main__':unittest.main()
