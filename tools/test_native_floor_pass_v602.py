"""Actual capture baselines and independently rejected pixel/event corruption."""
import copy
import unittest
from unittest.mock import patch
import numpy as np
import inspect_natural_arena_floor_v602_v3 as model
import verify_native_floor_pass_v602 as v


class NativeFloorPassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=v.ROOT/'audit_v630_floor_pass_sonya_p2'
        cls.data=model.data(cls.folder)
        cls.proof=model.inspect(cls.folder)

    def test_actual_kano_passes(self):
        proof=v.verify(v.ROOT/'audit_v630_floor_pass_kano_p2','kano',v.ROOT/'audit_v620_floor_kano_p2')
        self.assertEqual(proof['indexed_vram_words'],3932160)
        self.assertFalse(proof['floorAcceptance'])

    def test_actual_sonya_passes(self):
        proof=v.verify(self.folder,'sonya',v.ROOT/'audit_v620_floor_sonya_p2')
        self.assertEqual(proof['display_pixels'],1524000)
        self.assertFalse(proof['desired_grounding_proven'])

    def reject_stats(self,change):
        proof=copy.deepcopy(self.proof);change(proof['records'][0])
        with self.assertRaises(ValueError):v.verify_contract(self.data[0],proof,'sonya')

    def test_reject_missing_shadow(self):self.reject_stats(lambda r:r.update(shadow_pixels=0))
    def test_reject_wrong_shadow_pixel(self):self.reject_stats(lambda r:r.update(shadow_mismatches=1))
    def test_reject_one_wrong_vram_word(self):self.reject_stats(lambda r:r.update(vram_mismatches=1))
    def test_reject_wrong_displayed_pixel(self):self.reject_stats(lambda r:r.update(displayed_mismatches=1))
    def test_reject_proxy(self):self.reject_stats(lambda r:r['body'][2].update(id=0))
    def test_reject_erased_body(self):self.reject_stats(lambda r:r['body'][2].update(pixels=0))
    def test_reject_wrong_native_body_pixel(self):self.reject_stats(lambda r:r['body'][1].update(mismatches=1))

    def reject_groups(self,change):
        data=copy.deepcopy(self.data);change(data[0])
        with self.assertRaises((AssertionError,ValueError,KeyError)):
            with patch.object(model,'data',return_value=data):
                proof=model.inspect(self.folder)
                v.verify_contract(data[0],proof,'sonya')

    def test_reject_prepass_after_first_draw(self):
        self.reject_groups(lambda g:g['FLOOR_PRE_FRAME'][0].update(event=g['FLOOR_DMA'][0]['event']+1))

    def test_reject_dropped_command(self):self.reject_groups(lambda g:g['FLOOR_DMA'].pop(0))

    def test_reject_wrong_native_trigger_mask(self):
        self.reject_groups(lambda g:g['FLOOR_COMMAND'][0].update(mask=0xff))

    def test_reject_wrong_imported_pose_position(self):
        def change(g):
            d=next(r for r in g['FLOOR_DMA']if r['frame']==1911 and r['slot']==2)
            d['x']+=1
        self.reject_groups(change)

    def test_reject_wrong_imported_palette(self):
        def change(g):
            d=next(r for r in g['FLOOR_DMA']if r['frame']==1911 and r['slot']==2)
            d['palette']=0x200
        self.reject_groups(change)

    def test_reject_wrong_shadow_ground(self):
        def change(g):
            for r in g['FLOOR_OWNER']:
                if r['frame']==1911 and r['slot']==2:r['stageY']+=1
        self.reject_groups(change)

    def test_reject_native_foreground_omission(self):
        def change(g):
            d=next(r for r in g['FLOOR_DMA']if r['frame']==1911 and r['source']==0x05721a92)
            g['FLOOR_DMA'].remove(d)
        self.reject_groups(change)

    def test_reject_one_actual_vram_pixel(self):
        target=self.folder/'floor_vram_snap1912_flip1912_4.bin'
        # fromfile is also used for the tested latch: corrupt its returned words
        original=np.fromfile
        def corrupt_words(path,*args,**kwargs):
            result=original(path,*args,**kwargs)
            if path==target:result[365*512+420]^=1
            return result
        with patch.object(np,'fromfile',side_effect=corrupt_words),self.assertRaises(ValueError):
            proof=model.inspect(self.folder);v.verify_contract(self.data[0],proof,'sonya')


if __name__=='__main__':unittest.main()
