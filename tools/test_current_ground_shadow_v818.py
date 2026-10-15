"""Actual current body/VRAM/native shadow evidence and corruption rejection."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import inspect_current_ground_shadow_v811 as model
import verify_current_ui_ground_v816 as proof

ROOT=Path(__file__).resolve().parents[1]

class GroundShadow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=ROOT/'audit_v815_ground_shadow_kano_p1'
        cls.log=(cls.folder/'run.log').read_text(encoding='utf-8-sig')
        cls.evidence={tag:model.rows(cls.log,tag)for tag in ('FIELD','PRE','OWNER','DMA','GFX','SNAP','SHADOW_COMPONENT')}
        cls.shadow_rows={tag:cls.evidence[tag]for tag in ('DMA','SHADOW_COMPONENT')}
        cls.buffers={r['key']:r for r in cls.evidence['GFX']}
        cls.accepted=json.loads((ROOT/'audit_v816_current_ui_ground_checked/verification.json').read_text())['ground_cases']
    def test_four_actual_presentation_baselines(self):
        for name,value in self.accepted.items():
            fighter,slot=name.rsplit('_p',1);side=int(slot);value=copy.deepcopy(value)
            value['idle_sole_rows']={int(k):v for k,v in value['idle_sole_rows'].items()}
            value['idle_native_ground_offsets']={int(k):v for k,v in value['idle_native_ground_offsets'].items()}
            for r in value['records']:
                r['body']={int(k):v for k,v in r['body'].items()}
                r['owned_shadow_pixels']={int(k):v for k,v in r['owned_shadow_pixels'].items()}
            proof.check_ground(value,fighter,side)
    def mutate_shadow(self,tag,key,delta):
        # Read only actual shadow DMA rows: other draws are outside row stepping.
        data={'DMA':[r.copy()for r in self.shadow_rows['DMA']if 0x10000000<=r['source']<0x1a000000 and r['command']&15==8],
              'SHADOW_COMPONENT':[r.copy()for r in self.shadow_rows['SHADOW_COMPONENT']]}
        target=data[tag][0];target[key]+=delta
        with patch.object(model,'rows',side_effect=lambda text,name:data[name]):model.check_shadow_rows(self.log,self.buffers)
    def test_actual_native_row_baseline(self):
        value=model.check_shadow_rows(self.log,self.buffers)
        self.assertTrue(value['rowStreamVerified']);self.assertEqual(value['copies'],30440)
    def test_one_pixel_shadow_shift(self):
        with self.assertRaises(AssertionError):self.mutate_shadow('DMA','y',1)
    def test_wrong_shadow_source_bit(self):
        with self.assertRaises(AssertionError):self.mutate_shadow('DMA','source',1)
    def test_wrong_shadow_colour(self):
        with self.assertRaises(AssertionError):self.mutate_shadow('DMA','color',1)
    def test_wrong_native_shadow_caller(self):
        with self.assertRaises(AssertionError):self.mutate_shadow('DMA','pc',16)
    def test_proxy_shadow_identity(self):
        with self.assertRaises(AssertionError):self.mutate_shadow('SHADOW_COMPONENT','id',-16)
    def test_foreign_shadow_cache_row(self):
        with self.assertRaises(AssertionError):self.mutate_shadow('SHADOW_COMPONENT','row',16)
    def test_missing_native_row(self):
        data={'DMA':self.shadow_rows['DMA'],'SHADOW_COMPONENT':self.shadow_rows['SHADOW_COMPONENT'][1:]}
        with patch.object(model,'rows',side_effect=lambda text,name:data[name]):
            with self.assertRaises(AssertionError):model.check_shadow_rows(self.log,self.buffers)
    def mutate_raster(self,tag,key,delta):
        data=copy.deepcopy(self.evidence);target=data['SNAP'][0]['frame']-(0 if tag=='SNAP'else 1)
        r=next(r for r in data[tag]if r['frame']==target and
            (tag!='DMA'or r['palette']==0x200 and r['command']&15==2)and(tag!='FIELD'or r['slot']==1))
        r[key]=f'{(int(r[key],16)+delta)&65535:04X}'if isinstance(r[key],str)else r[key]+delta
        with patch.object(model,'rows',side_effect=lambda text,name:data[name]):
            value=model.inspect(self.folder);proof.check_ground(value,'kano',1)
    def test_actual_one_pixel_body_shift(self):
        with self.assertRaises(ValueError):self.mutate_raster('DMA','y',1)
    def test_wrong_actual_display_latch(self):
        with self.assertRaises(ValueError):self.mutate_raster('SNAP','start',0x1000)
    def test_actual_wrong_physical_identity(self):
        with self.assertRaises((AssertionError,ValueError)):self.mutate_raster('FIELD','id',-16)
    def test_no_visible_shadow_rejected(self):
        value=copy.deepcopy(next(iter(self.accepted.values())))
        # Normalize persisted keys before checking the actual baseline contract.
        value['idle_sole_rows']={int(k):v for k,v in value['idle_sole_rows'].items()}
        value['idle_native_ground_offsets']={int(k):v for k,v in value['idle_native_ground_offsets'].items()}
        for r in value['records']:
            r['body']={int(k):v for k,v in r['body'].items()};r['owned_shadow_pixels']={int(k):v for k,v in r['owned_shadow_pixels'].items()}
        value['records'][0]['owned_shadow_pixels'][1]=0
        with self.assertRaises(ValueError):proof.check_ground(value,'kano',1)

if __name__=='__main__':
    out=ROOT/'audit_v818_current_ground_shadow_units'
    if out.exists():raise ValueError('Do not overwrite evidence')
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(GroundShadow))
    out.mkdir();(out/'unit-tests.log').write_text(stream.getvalue())
    paths=[Path(__file__),Path(model.__file__),Path(proof.__file__),ROOT/'audit_v816_current_ui_ground_checked/verification.json',ROOT/'audit_v815_ground_shadow_kano_p1/run.log']
    (out/'verification.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
        'scope':__doc__,'fullPortAcceptance':False,'checked_inputs':{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest().upper()for p in paths}},indent=2)+'\n')
    print(stream.getvalue());sys.exit(0 if result.wasSuccessful()else 1)
