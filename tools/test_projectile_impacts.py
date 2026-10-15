"""Reject missing or falsified impact evidence, not just observer pass flags."""
import re
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import verify_projectile_impacts as v

ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=ROOT/'diagnostic_v293_native_projectile_impacts/roms/mk2ks/mk2ks.mdata'


class ImpactEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(t,s,c):(ROOT/f'audit_v295_impact_{t}_{c}_p{s}/run.log').read_text(encoding='utf-8-sig')
                  for t in ('kano','sonya') for s in (1,2) for c in ('hit','block','miss')}

    def reject(self,log,target='sonya'):
        with tempfile.TemporaryDirectory(prefix='mk2-impact-rejection-') as directory:
            folder=Path(directory);(folder/'run.log').write_text(log,encoding='utf-8')
            result=v.verify(folder,target,1,PAYLOAD,False)
            self.assertFalse(result['passed'],result)

    def mutate(self,tag,key,value,where='',target='sonya'):
        log=self.logs[target,1,'hit'];changed=False
        def replace(m):
            nonlocal changed
            if changed or where not in m[0]:return m[0]
            new=re.sub(r'(\b'+key+r'=)[^\s]+',lambda n:n[1]+value,m[0],count=1)
            changed=new!=m[0];return new
        altered=re.sub(r'^MK2_IMPACT_'+tag+r' [^\r\n]*',replace,log,flags=re.M)
        self.assertTrue(changed)
        return altered

    def test_all_twelve_actual_cold_runtime_paths(self):
        for t,s,c in self.logs:
            with self.subTest(target=t,side=s,scenario=c):
                result=v.verify(ROOT/f'audit_v295_impact_{t}_{c}_p{s}',t,s,PAYLOAD,False)
                self.assertTrue(result['passed'],result)
                self.assertFalse(result['startup_fidelity_proven'])

    def test_wrong_impact_id(self):self.reject(self.mutate('FIELD','id','0','action=0500'))
    def test_wrong_facing(self):self.reject(self.mutate('FIELD','flags','E012','action=0500'))
    def test_wrong_pose_order(self):self.reject(self.mutate('FIELD','pose','FF60C000','action=0500'))
    def test_wrong_hold(self):self.reject(self.mutate('FIELD','frame','9999','action=0500'))
    def test_wrong_x(self):self.reject(self.mutate('FIELD','x','0','action=0500'))
    def test_wrong_y(self):self.reject(self.mutate('FIELD','y','0','action=0500'))
    def test_wrong_drift(self):self.reject(self.mutate('FIELD','vx','000C0000','action=0500'))
    def test_wrong_component_count(self):self.reject(self.mutate('FIELD','components','1','components=5'))
    def test_wrong_component_source(self):self.reject(self.mutate('COMPONENT','graphic','0F020000','pose=FF60C'))
    def test_wrong_component_descriptor(self):self.reject(self.mutate('COMPONENT','descriptor','FF602000','pose=FF60C'))
    def test_wrong_component_pivot(self):self.reject(self.mutate('COMPONENT','dx','0','pose=FF60C'))
    def test_wrong_component_size(self):self.reject(self.mutate('COMPONENT','width','1','pose=FF60C'))
    def test_wrong_component_command(self):self.reject(self.mutate('COMPONENT','command','6010','pose=FF60C'))
    def test_wrong_dma_size(self):self.reject(self.mutate('DMA','height','1','graphic=0F2D'))
    def test_wrong_dma_facing(self):self.reject(self.mutate('DMA','command','E012','graphic=0F2D'))
    def test_wrong_dma_scale(self):self.reject(self.mutate('DMA','scale_x','0200','graphic=0F2D'))
    def test_wrong_dma_pc(self):self.reject(self.mutate('DMA','pc','FF804630','graphic=0F2D'))
    def test_wrong_cull_pc(self):self.reject(self.mutate('CULL','pc','FF804570'))
    def test_false_cull_for_on_screen_position(self):self.reject(self.mutate('CULL','position','00500050'))
    def test_missing_cull(self):self.reject(re.sub(r'^MK2_IMPACT_CULL [^\r\n]*\r?\n','',self.logs['sonya',1,'hit'],flags=re.M))
    def test_missing_components(self):self.reject(re.sub(r'^MK2_IMPACT_COMPONENT [^\r\n]*\r?\n','',self.logs['sonya',1,'hit'],flags=re.M))
    def test_missing_dma(self):self.reject(re.sub(r'^MK2_IMPACT_DMA [^\r\n]*\r?\n','',self.logs['sonya',1,'hit'],flags=re.M))
    def test_missing_effect_field(self):self.reject(re.sub(r'^MK2_IMPACT_FIELD [^\r\n]*\r?\n','',self.logs['sonya',1,'hit'],count=1,flags=re.M))
    def test_extra_effect_field(self):
        log=self.logs['sonya',1,'hit'];line=next(l for l in log.splitlines() if l.startswith('MK2_IMPACT_FIELD '))
        self.reject(log+'\n'+line+'\n')
    def test_observer_gameplay_write(self):self.reject(self.mutate('FIELD','writes','1','action=0500'))

    def test_blank_snapshot_cannot_pass_original_art_match(self):
        payload=PAYLOAD.read_bytes()
        with tempfile.TemporaryDirectory(prefix='mk2-impact-render-rejection-') as directory:
            path=Path(directory)/'blank.png';Image.new('RGB',(400,254),'black').save(path)
            for group in (0xff60c000,0xff60c1c0):
                rgb,mask=v.composite(payload,group)
                self.assertEqual(v.match_image(path,rgb,mask)['score'],0)

    def test_wrong_snapshot_resolution_rejected(self):
        with tempfile.TemporaryDirectory(prefix='mk2-impact-size-rejection-') as directory:
            path=Path(directory)/'scaled.png';Image.new('RGB',(400,300),'black').save(path)
            rgb,mask=v.composite(PAYLOAD.read_bytes(),0xff60c000)
            with self.assertRaisesRegex(ValueError,'unscaled'):v.match_image(path,rgb,mask)


if __name__=='__main__':unittest.main()
