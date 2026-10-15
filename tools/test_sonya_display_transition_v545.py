"""Nonvacuous actual-baseline and in-memory visual/provenance corruption tests."""
from __future__ import annotations
import copy
import re
import unittest

from PIL import Image
import verify_sonya_display_transition_v545 as v

class DisplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log=(v.CASE/'run.log').read_text(encoding='utf-8-sig')
        cls.payload=(v.ROOT/v.paired.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.donor=(v.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        cls.gfx=v.graphics.load_gfx(v.ROOT/'roms/mk2ks')
        cls.images={f:Image.open(v.CASE/'snap'/f'done_{f}.png').copy()for f in range(1960,1976)}
        baseline=cls.evaluate(cls.log,cls.images)
        if not baseline['passed']:raise AssertionError(baseline['errors'])

    @classmethod
    def evaluate(cls,log,images):return v.check(log,cls.payload,cls.donor,cls.gfx,images)

    def reject(self,log=None,images=None):
        proof=self.evaluate(self.log if log is None else log,self.images if images is None else images)
        self.assertFalse(proof['passed'])
        self.assertTrue(proof['errors'])

    def change(self,kind,frame,side,key,value):
        lines=self.log.splitlines()
        matches=[i for i,line in enumerate(lines)if line.startswith('MK2_VISUAL_'+kind+' ')and re.search(r'\bframe='+str(frame)+r'\b',line)and(side is None or re.search(r'\bside='+str(side)+r'\b',line))]
        self.assertTrue(matches,'Actual mutation target must exist')
        i=matches[0]
        self.assertRegex(lines[i],r'\b'+key+r'=\S+')
        lines[i]=re.sub(r'\b'+key+r'=\S+',key+'='+value,lines[i],count=1)
        return '\n'.join(lines)

    def test_actual_baseline(self):
        proof=self.evaluate(self.log,self.images)
        self.assertTrue(proof['passed']);self.assertEqual(len(proof['pixel_matches']),16)
        self.assertGreater(proof['exact_visible_body_pixels'],80000)
        self.assertFalse(proof['fullPortAcceptance'])

    def test_swap_mirror_costumes(self):
        self.reject(self.change('ACTOR',1963,1,'colors',v.parse(self.log,'ACTOR')[1]['colors']))

    def test_missing_frame_done(self):
        self.reject('\n'.join(line for line in self.log.splitlines()if not line.startswith('MK2_VISUAL_SCREEN frame=1964 ')))

    def test_missing_actor(self):
        self.reject('\n'.join(line for line in self.log.splitlines()if not line.startswith('MK2_VISUAL_ACTOR frame=1940 side=2 ')))

    def test_duplicate_actor(self):
        line=next(line for line in self.log.splitlines()if line.startswith('MK2_VISUAL_ACTOR frame=1940 side=2 '))
        self.reject(self.log+'\n'+line)

    def test_missing_dma_component(self):
        line=next(line for line in self.log.splitlines()if line.startswith('MK2_VISUAL_DMA frame=1963 '))
        self.reject(self.log.replace(line,'',1))

    def test_native_new_attack_setup_removed(self):
        self.reject('\n'.join(line for line in self.log.splitlines()if not(line.startswith('MK2_CPU_PAIR_FLAG frame=1970 ')and 'kind=flags 'in line)))

    def test_wrong_frame_snapshot(self):
        images=dict(self.images);images[1964]=self.images[1963]
        self.reject(images=images)

    def test_blank_snapshot(self):
        images=dict(self.images);images[1964]=Image.new('RGB',(400,254))
        self.reject(images=images)

    def test_wrong_snapshot_dimensions(self):
        images=dict(self.images);images[1964]=self.images[1964].resize((399,254))
        self.reject(images=images)

    def test_one_real_body_pixel_changed(self):
        actors=[a for a in v.parse(self.log,'ACTOR')if a['frame']==1963]
        dmas=[d for d in v.parse(self.log,'DMA')if d['frame']==1963]
        template=v.frame_template(dmas,actors,self.gfx)
        yy,xx=v.np.nonzero(template[:,:,3]);index=next(i for i,x in enumerate(xx)if 56<=x<456 and yy[i]<254)
        point=(int(xx[index]-56),int(yy[index]))
        images=dict(self.images);images[1964]=self.images[1964].convert('RGB').copy()
        old=images[1964].getpixel(point);images[1964].putpixel(point,(old[0]^1,old[1],old[2]))
        self.reject(images=images)

    def test_inverted_block_region(self):
        images=dict(self.images);images[1964]=self.images[1964].copy()
        box=(222,110,278,237)
        images[1964].paste(images[1964].crop(box).transpose(Image.Transpose.FLIP_TOP_BOTTOM),box)
        self.reject(images=images)

def mutation_test(kind,frame,side,key,value):
    def test(self):self.reject(self.change(kind,frame,side,key,value))
    return test

for name,params in {
    'wrong_cpu_owner':('ACTOR',1963,1,'actor','010350A0'),
    'wrong_human_main':('ACTOR',1963,2,'main','0106A370'),
    'shared_list':('ACTOR',1963,2,'list','0105ED30'),
    'shared_palette':('ACTOR',1963,2,'palette','0202'),
    'alternate_bit_cleared':('ACTOR',1963,2,'body','0012'),
    'human_y_flip':('ACTOR',1963,2,'facing','8022'),
    'human_airborne_position':('ACTOR',1963,2,'y','70'),
    'human_wrong_action':('ACTOR',1963,2,'action','1553'),
    'human_wrong_block_pose':('ACTOR',1963,2,'pose','FE83EC40'),
    'cpu_stuck_cycling':('ACTOR',1963,1,'pose','FE83EC40'),
    'cpu_late_walk_state':('ACTOR',1963,1,'action','1553'),
    'cpu_y_flip':('ACTOR',1963,1,'facing','8022'),
    'cpu_bad_landed_y':('ACTOR',1962,1,'y','70'),
    'cpu_wrong_final_cycle':('ACTOR',1961,1,'pose','FE83EC00'),
    'cpu_late_lock_missing':('ACTOR',1971,1,'body','0012'),
    'cpu_later_wrong_dispatch':('ACTOR',1971,1,'pose','FF02F240'),
    'missing_part':('PART',1963,2,'part','1'),
    'cached_source_changed':('PART',1963,2,'source','1094FA1C'),
    'cached_width_changed':('PART',1963,2,'width','23'),
    'cached_height_changed':('PART',1963,2,'height','124'),
    'cached_offset_changed':('PART',1963,2,'dy','-16'),
    'cached_y_flip':('PART',1963,2,'command','60A0'),
    'dma_wrong_palette':('DMA',1963,None,'palette','0202'),
    'dma_y_flip':('DMA',1963,None,'command','E0A2'),
    'dma_wrong_source':('DMA',1963,None,'source','1094FA1C'),
    'dma_wrong_x':('DMA',1963,None,'x','277'),
    'dma_wrong_y':('DMA',1963,None,'y','367'),
    'dma_wrong_dimensions':('DMA',1963,None,'height','124'),
    'observer_write':('ACTOR',1963,2,'writes','1'),
    'wrong_capture_phase':('SCREEN',1964,None,'phase','before'),
}.items():setattr(DisplayTests,'test_'+name,mutation_test(*params))

if __name__=='__main__':unittest.main()
