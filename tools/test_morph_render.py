"""Native original-art morph pixels and fail-closed palette/buffer mutations."""
import re
import unittest
from unittest.mock import patch
from pathlib import Path
import numpy as np
from PIL import Image
import verify_morph_render as check

ROOT=Path(__file__).resolve().parents[1]


class MorphRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=ROOT/'audit_v358_fixed_morph_render_sonya_p2'
        cls.log=(cls.folder/'run.log').read_text(encoding='utf-8-sig')

    def rejects(self,log):self.assertFalse(check.verify_log(log,self.folder,'sonya',2,False)['passed'])

    def test_all_four_actual_native_pixel_cases(self):
        for target in ('kano','sonya'):
            for side in (1,2):
                folder=ROOT/f'audit_v358_fixed_morph_render_{target}_p{side}'
                with self.subTest(target=target,side=side):
                    proof=check.verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),folder,target,side)
                    self.assertTrue(proof['passed'],proof['errors'])
                    self.assertEqual(proof['transition_fields'],24)
                    self.assertEqual(proof['native_component_fields'],80)
                    self.assertEqual(proof['restored_handoff_fields'],8)
                    self.assertTrue(all(v['score']==1.0 for v in proof['visual']))

    def test_pre_fix_native_palette_substitution_is_rejected(self):
        for target in ('kano','sonya'):
            for side in (1,2):
                folder=ROOT/f'audit_v356_native_morph_render_{target}_p{side}'
                proof=check.verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),folder,target,side,False)
                self.assertFalse(proof['passed'])
                self.assertIn('All used original morph/body colors reach actual DMA palette',proof['errors'])

    def test_render_scope_does_not_claim_full_game(self):
        proof=check.verify_log(self.log,self.folder,'sonya',2,False)
        self.assertEqual(proof['scope'],check.SCOPE)
        self.assertFalse(proof['whole_character_integration_complete'])

    def test_no_observer_memory_assistance(self):self.rejects(self.log.replace('writes=0','writes=1'))
    def test_missing_hold(self):
        self.rejects(re.sub(r'^MK2_MORPH_RENDER_BODY.*pose=FF0C4120.*\n','',self.log,count=1,flags=re.M))
    def test_wrong_pose_order(self):self.rejects(self.log.replace('pose=FF0C4180','pose=FF0C41E0'))
    def test_missing_reverse(self):self.rejects(re.sub(r'^MK2_MORPH_RENDER_WINDOW.*phase=reverse.*\n','',self.log,flags=re.M))
    def test_missing_normal_body_handoff(self):self.rejects(re.sub(r'^MK2_MORPH_RENDER_BODY.*id=18.*\n','',self.log,flags=re.M))
    def test_missing_restored_shang_handoff(self):self.rejects(re.sub(r'^MK2_MORPH_RENDER_BODY.*phase=reverse.*id=6.*\n','',self.log,flags=re.M))
    def test_wrong_opaque_palette(self):
        log=re.sub(r'(MK2_MORPH_RENDER_PALETTE[^\n]*colors=)[0-9A-F,]+',lambda m:m[1]+','.join(['0000']*64),self.log)
        self.rejects(log)
    def test_wrong_palette_bank(self):self.rejects(self.log.replace('palette=0404','palette=0303'))
    def test_wrong_flip(self):self.rejects(self.log.replace('command=6010','command=6000'))
    def test_wrong_component_descriptor(self):self.rejects(self.log.replace('descriptor=FF0C2640','descriptor=FF0C26E0'))
    def test_wrong_scale(self):self.rejects(self.log.replace('scale_x=0100','scale_x=0080'))
    def test_wrong_native_copy_writer(self):self.rejects(self.log.replace('pc=FF804640','pc=00000000'))
    def test_omitted_draw_ordinal(self):self.rejects(self.log.replace('ordinal=2 ','ordinal=1 '))
    def test_displaced_part_pivot(self):self.rejects(self.log.replace('dx=6 ','dx=7 '))
    def test_transparent_proxy_body(self):self.rejects(self.log.replace('components=2','components=0'))
    def test_mirror_palette_handoff_not_primary(self):
        folder=ROOT/'audit_v358_fixed_morph_render_kano_p2'
        log=(folder/'run.log').read_text(encoding='utf-8-sig').replace('body=0052','body=0012')
        self.assertFalse(check.verify_log(log,folder,'kano',2,False)['passed'])
    def test_cannot_claim_success_from_png_alone(self):self.rejects(re.sub(r'^MK2_MORPH_RENDER_DMA.*\n','',self.log,flags=re.M))

    def test_corrupted_native_bitmap_pixels_fail(self):
        original=Image.open
        def corrupt(path,*args,**kwargs):
            bitmap=original(path,*args,**kwargs)
            if Path(path).name.startswith('choreo_'):
                pixels=np.array(bitmap.convert('RGB'))^255
                return Image.fromarray(pixels)
            return bitmap
        with patch.object(check.Image,'open',side_effect=corrupt):
            proof=check.verify_log(self.log,self.folder,'sonya',2)
            self.assertFalse(proof['passed'])


if __name__=='__main__':unittest.main()
