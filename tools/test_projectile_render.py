"""Current real-input pixel evidence and deliberately broken native traces."""
import re
import unittest
from unittest.mock import patch

import verify_projectile_render as render

ROOT=render.ROOT


def case_folder(target,scenario,side):
    newer=ROOT/f'audit_v303_render_shadow_{target}_{scenario}_p{side}'
    return newer if (newer/'result.json').exists() else ROOT/f'audit_v302_render_{target}_{scenario}_p{side}'


class CurrentRenderEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=case_folder('kano','hit',1)
        cls.log=(cls.folder/'run.log').read_text(encoding='utf-8-sig')

    def reject(self,tag,field=None,value=None,predicate=lambda line:True):
        lines=self.log.splitlines()
        index=next(i for i,line in enumerate(lines) if line.startswith(tag+' ') and predicate(line))
        if field is None:del lines[index]
        else:lines[index],count=re.subn(r'\b'+field+r'=\S+',field+'='+value,lines[index]);self.assertEqual(count,1)
        try:result=render.verify_render_log('\n'.join(lines),self.folder,'kano',1,False)
        except (KeyError,ValueError,IndexError,StopIteration):return
        self.assertFalse(result['passed'],result)

    def test_twelve_current_native_render_cases(self):
        for target in ('kano','sonya'):
            for side in (1,2):
                for scenario in ('hit','block','miss'):
                    with self.subTest(target=target,side=side,scenario=scenario):
                        result=render.verify(case_folder(target,scenario,side),target,side)
                        self.assertTrue(result['passed'],result['errors'])
                        self.assertGreater(result['native_component_draws'],200)
                        self.assertTrue(result['visual'])
                        self.assertTrue(all(v['score']>=.98 for v in result['visual'] if v['visible']))

    def test_missing_body_field(self):self.reject('MK2_RENDER_BODY')
    def test_wrong_body_identity(self):self.reject('MK2_RENDER_BODY','id','0')
    def test_missing_body_component(self):self.reject('MK2_RENDER_BODY_COMPONENT')
    def test_wrong_body_bpp(self):self.reject('MK2_RENDER_BODY_COMPONENT','command','6000')
    def test_shifted_body_component_pivot(self):self.reject('MK2_RENDER_BODY_COMPONENT','dx','18')
    def test_wrong_effect_descriptor(self):self.reject('MK2_IMPACT_COMPONENT','descriptor','FF6120A0')
    def test_missing_small_raw_particle(self):self.reject('MK2_IMPACT_COMPONENT',predicate=lambda l:'index=2' in l)
    def test_missing_effect_field(self):self.reject('MK2_IMPACT_FIELD')
    def test_wrong_effect_graphic(self):self.reject('MK2_IMPACT_COMPONENT','graphic','0F300420')
    def test_observer_memory_write(self):self.reject('MK2_RENDER_DMA','writes','1')
    def test_missing_native_copy(self):self.reject('MK2_RENDER_DMA',predicate=lambda l:'graphic=0F300000' in l)
    def test_scaled_native_copy(self):self.reject('MK2_RENDER_DMA','scale_x','0080',lambda l:'graphic=0F300000' in l)
    def test_wrong_native_copy_facing(self):self.reject('MK2_RENDER_DMA','command','E012',lambda l:'graphic=0F300000' in l)
    def test_shifted_native_component(self):self.reject('MK2_RENDER_DMA','x','141',lambda l:'graphic=0F300000' in l)
    def test_missing_foreground_draw(self):self.reject('MK2_RENDER_DMA',predicate=lambda l:'ordinal=183 ' in l)
    def test_missing_actual_palette(self):self.reject('MK2_RENDER_PALETTE',predicate=lambda l:'bank=0400' in l)
    def test_wrong_used_palette(self):
        self.reject('MK2_RENDER_PALETTE','colors',','.join(['0000']*64),lambda l:'bank=0400' in l)
    def test_wrong_held_impact_pose(self):self.reject('MK2_IMPACT_FIELD','pose','FF60C040',lambda l:'pose=FF60C000' in l)
    def test_impossible_shadow_source(self):self.reject('MK2_RENDER_SHADOW_SOURCE','graphic','00000000')

    def test_blank_bitmap_rejected(self):
        with patch.object(render.Image,'open',return_value=render.Image.new('RGB',(400,254))):
            result=render.verify(self.folder,'kano',1)
        self.assertFalse(result['passed'])
        self.assertIn('Every sampled original component actually renders with decoded native foreground overdraw',result['errors'])

    def test_scaled_bitmap_rejected(self):
        with patch.object(render.Image,'open',return_value=render.Image.new('RGB',(400,300))):
            result=render.verify(self.folder,'kano',1)
        self.assertFalse(result['passed'])
        self.assertTrue(any('400x254' in error for error in result['errors']))

    def test_video_page_wrapping_is_required(self):
        # Omitting the later actual chain cannot count as invisible background.
        folder=case_folder('kano','hit',1);log=(folder/'run.log').read_text(encoding='utf-8-sig')
        draws=render.native_rows(log,'DMA');palettes=render.native_rows(log,'PALETTE')
        part=render.parts(render.PAYLOAD.read_bytes(),0xff60c160)[0]
        draw=next(d for d in draws if d['frame']==3409 and d['graphic']==part['graphic'])
        actual=[d for d in draws if d['frame']==draw['frame']]
        full=render.component_image_check(folder,draw,part,palettes,actual)
        without_wrap=[d for d in actual if (d['y']&511)+d['height']<=512]
        incomplete=render.component_image_check(folder,draw,part,palettes,without_wrap)
        self.assertGreaterEqual(full['score'],.98)
        self.assertLess(incomplete['score'],.98)

    def test_missing_actual_offscreen_reject(self):
        folder=case_folder('kano','miss',2)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        lines=log.splitlines();index=next(i for i,l in enumerate(lines) if l.startswith('MK2_IMPACT_CULL '))
        del lines[index]
        result=render.verify_render_log('\n'.join(lines),folder,'kano',2,False)
        self.assertFalse(result['passed'])
        self.assertIn('Each component reaches native copy DMA once or actual proved culling',result['errors'])

    def test_incomplete_case_launch_inventory(self):
        metadata=render.json.loads((self.folder/'result.json').read_text(encoding='utf-8-sig'))
        metadata['input_hashes']={}
        original=render.json.loads
        def changed(value,*args,**kwargs):
            parsed=original(value,*args,**kwargs)
            return metadata if isinstance(parsed,dict) and 'exit_code' in parsed else parsed
        with patch.object(render.json,'loads',side_effect=changed):
            result=render.verify(self.folder,'kano',1,False)
        self.assertFalse(result['passed'])
        self.assertIn('Complete immutable read-only render case launch inventory',result['errors'])


if __name__=='__main__':unittest.main()
