"""Actual mirrored-slot, identity and native-palette counterexamples.

All mutations are in memory. No capture, script or game input is rewritten.
"""
import copy
import unittest
import numpy as np
import verify_finish_display_v798 as v


class Slots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload=(v.ROOT/v.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.original=(v.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        cls.guest=(v.ROOT/'audit_v790_kano_friendship_p1/guest_maincpu.bin').read_bytes()
        cls.cases=[]
        for name,ids in v.CASES.items():
            folder=v.ROOT/name
            import json
            side=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))['human_slot']
            cls.cases.append((folder,v.raster.data(folder)[0],ids,side))

    def cache(self,g,ids,side):return v.composites(g,self.payload,self.original,ids,self.guest,side)
    def retired(self,g,ids,side):return v.retirement(g,g['FLOOR_BEGIN'][0],self.guest,ids,side)

    def mutate_cache(self,index,tag,key,value,condition=lambda r:True):
        _,g,ids,side=self.cases[index];g=copy.deepcopy(g)
        r=next(r for r in g[tag] if condition(r));r[key]=value(r[key])
        with self.assertRaises(ValueError):self.cache(g,ids,side)

    def palette_case(self,index):
        folder,g,ids,side=self.cases[index]
        by_frame={q['frame']:q for q in g['FLOOR_QUEUE'] if q['slot']==3-side}
        for d in g['FLOOR_DISPLAY']:
            q=by_frame.get(d['frame']-1)
            if q:
                actual=np.fromfile(folder/d['palette_file'],dtype='<u4')
                if v.check_palette_record(q,actual,self.guest,ids,side):return q,actual,ids,side
        self.fail('No positive actual palette sample')

    def test_all_four_cache_baselines(self):
        for _,g,ids,side in self.cases:self.cache(g,ids,side)
    def test_all_four_native_retirement_baselines(self):
        for _,g,ids,side in self.cases:self.retired(g,ids,side)
    def test_actual_native_SubZero_colors_P2(self):
        self.palette_case(1)
    def test_actual_Sonya_fire_colors_stock_and_mirror(self):
        for index in (2,3):self.palette_case(index)
    def test_wrong_P2_actual_fighter_ID(self):
        self.mutate_cache(1,'FLOOR_QUEUE','id',lambda x:1,lambda r:r['slot']==2)
    def test_wrong_P2_actual_victim_ID(self):
        self.mutate_cache(1,'FLOOR_QUEUE','roster',lambda x:1,lambda r:r['slot']==1)
    def test_false_mirror_victim_ID(self):
        self.mutate_cache(3,'FLOOR_QUEUE','id',lambda x:17,lambda r:r['slot']==1)
    def test_wrong_mirrored_cache_component(self):
        self.mutate_cache(0,'FLOOR_QUEUE_PART','dx',lambda x:x+1)
    def test_wrong_native_horizontal_flip(self):
        self.mutate_cache(0,'FLOOR_QUEUE','facing',lambda x:x^16)
    def test_wrong_left_facing_orb_descriptor(self):
        self.mutate_cache(2,'FLOOR_SINGLE_DESCRIPTOR','descriptor',lambda x:x+2048)
    def test_single_effect_mistaken_for_multipart(self):
        self.mutate_cache(2,'FLOOR_QUEUE','multipart',lambda x:1,lambda r:r['multipart']==0)
    def test_single_effect_mistaken_for_victim(self):
        self.mutate_cache(2,'FLOOR_QUEUE','slot',lambda x:1,lambda r:r['slot']==3)
    def test_effect_bound_to_wrong_parent(self):
        self.mutate_cache(0,'FLOOR_QUEUE','parent',lambda x:x+16,lambda r:r['slot']==3)
    def test_effect_bound_to_wrong_Main(self):
        self.mutate_cache(0,'FLOOR_QUEUE','main',lambda x:x+16,lambda r:r['slot']==3)
    def test_effect_bound_to_wrong_roster(self):
        self.mutate_cache(0,'FLOOR_QUEUE','roster',lambda x:1,lambda r:r['slot']==3)
    def test_effect_bound_to_wrong_native_owner(self):
        self.mutate_cache(0,'FLOOR_QUEUE','owner',lambda x:x+16,lambda r:r['slot']==3)
    def test_wrong_native_RGB_entry(self):
        for index in (1,2,3):
            q,actual,ids,side=self.palette_case(index);actual=actual.copy()
            actual[(q['bank']&0x7f00)+1]^=255
            with self.assertRaises(ValueError):v.check_palette_record(q,actual,self.guest,ids,side)
    def test_incorrect_stock_alternate_palette_choice(self):
        q,actual,ids,side=self.palette_case(1);q=q.copy();q['body']^=64
        with self.assertRaises(ValueError):v.check_palette_record(q,actual,self.guest,ids,side)
    def test_wrong_palette_bank(self):
        q,actual,ids,side=self.palette_case(3);q=q.copy();q['bank']^=256
        with self.assertRaises(ValueError):v.check_palette_record(q,actual,self.guest,ids,side)
    def test_truncated_actual_palette(self):
        q,actual,ids,side=self.palette_case(1)
        with self.assertRaises(ValueError):v.check_palette_record(q,actual[:100],self.guest,ids,side)
    def test_wrong_64_color_fire_alias(self):
        q,actual,ids,side=self.palette_case(3);guest=bytearray(self.guest);guest[0xf5900]=64
        with self.assertRaises(ValueError):v.check_palette_record(q,actual,guest,ids,side)
    def test_wrong_physical_retirement_slot(self):
        _,g,ids,side=self.cases[1]
        with self.assertRaises(ValueError):self.retired(g,ids,1)
    def test_wrong_native_P2_winner(self):
        _,g,ids,side=self.cases[1];g=copy.deepcopy(g);g['FLOOR_RETIRED'][0]['winner']=1
        with self.assertRaises(ValueError):self.retired(g,ids,side)
    def test_retirement_with_live_victim(self):
        _,g,ids,side=self.cases[0];g=copy.deepcopy(g);g['FLOOR_RETIRED'][0]['victim_health']=161
        with self.assertRaises(ValueError):self.retired(g,ids,side)
    def test_missing_actual_pointer_store(self):
        _,g,ids,side=self.cases[0];g=copy.deepcopy(g);g['FLOOR_POINTER_STORE'].pop()
        with self.assertRaises(ValueError):self.retired(g,ids,side)

    def own_palette_case(self,index):
        folder,g,ids,side=self.cases[index]
        by_frame={q['frame']:q for q in g['FLOOR_QUEUE'] if q['slot']==side}
        for d in g['FLOOR_DISPLAY']:
            q=by_frame.get(d['frame']-1)
            if q:
                actual=np.fromfile(folder/d['palette_file'],dtype='<u4')
                result=v.check_owned_body_palette(q,actual,self.guest,ids,side)
                return q,actual,ids,side,result
        self.fail('Missing positively drawn own palette')

    def test_full_bright_own_normal_palette_all_four(self):
        for index in range(4):self.own_palette_case(index)

    def test_actual_own_alternate_Sonya_palette(self):
        _,_,_,_,result=self.own_palette_case(3)
        self.assertTrue(result['alternate'])

    def test_dimmed_owned_body_rejected(self):
        for index in range(4):
            q,actual,ids,side,_=self.own_palette_case(index)
            actual=actual.copy();actual[(q['bank']&0x7f00)+1]=0
            with self.assertRaises(ValueError):v.check_owned_body_palette(q,actual,self.guest,ids,side)

    def test_wrong_owned_alternate_choice_rejected(self):
        q,actual,ids,side,_=self.own_palette_case(3)
        q=q.copy();q['body']^=64
        with self.assertRaises(ValueError):v.check_owned_body_palette(q,actual,self.guest,ids,side)

    def test_wrong_owned_palette_identity_rejected(self):
        q,actual,ids,side,_=self.own_palette_case(0)
        q=q.copy();q['id']=1
        with self.assertRaises(ValueError):v.check_owned_body_palette(q,actual,self.guest,ids,side)

    def test_wrong_owned_palette_bank_rejected(self):
        q,actual,ids,side,_=self.own_palette_case(0)
        q=q.copy();q['bank']^=256
        with self.assertRaises(ValueError):v.check_owned_body_palette(q,actual,self.guest,ids,side)


if __name__=='__main__':unittest.main(verbosity=2)
