"""Actual grounded/moving display replay and rejection of wrong foot contracts."""
import copy
import json
import unittest
from unittest.mock import patch
import inspect_native_idle_feet_v635_v2 as model
import verify_native_idle_feet_v635 as v


class NativeFeet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=v.ROOT/'audit_v644_native_idle_kano_p1'
        cls.log=(cls.folder/'run.log').read_text(encoding='utf-8-sig')
        cls.rows={tag:model.rows(cls.log,tag)for tag in ('FIELD','PRE','OWNER','DMA','GFX','SNAP')}
        cls.proofs=json.loads((v.ROOT/v.NAME/'idle-foot-verification.json').read_text())['cases']

    def test_four_real_cases(self):
        for case in self.proofs.values():
            value=copy.deepcopy(case['presentation'])
            value['idle_sole_rows']={int(k):r for k,r in value['idle_sole_rows'].items()}
            value['idle_native_ground_offsets']={int(k):r for k,r in value['idle_native_ground_offsets'].items()}
            for record in value['records']:record['body']={int(k):r for k,r in record['body'].items()}
            v.check_presentation(value,case['fighter'],case['side'])
            self.assertFalse(case['fullPortAcceptance'])

    def mutate_actual(self,tag,field,delta):
        evidence=copy.deepcopy(self.rows)
        # Touch the actual pass displayed by the first retained screenshot,
        # not the earlier unsampled ready field (which cannot test rejection).
        target=evidence['SNAP'][0]['frame']-(0 if tag=='SNAP'else 1)
        row=next(r for r in evidence[tag]if r['frame']==target and
                 (tag!='DMA'or r['palette']==0x200 and r['command']&15==2)and
                 (tag!='FIELD'or r['slot']==1))
        if isinstance(row[field],str):row[field]=f'{(int(row[field],16)+delta)&65535:04X}'
        else:row[field]+=delta
        with patch.object(model,'rows',side_effect=lambda log,name:evidence[name]):
            return model.inspect(self.folder)

    def test_actual_one_pixel_body_shift(self):
        proof=self.mutate_actual('DMA','y',1)
        with self.assertRaises(ValueError):v.check_presentation(proof,'kano',1)

    def test_actual_source_corruption(self):
        with self.assertRaises((KeyError,ValueError,AssertionError)):
            proof=self.mutate_actual('DMA','source',8)
            v.check_presentation(proof,'kano',1)

    def test_actual_foreign_identity(self):
        with self.assertRaises((ValueError,AssertionError)):
            proof=self.mutate_actual('FIELD','id',-16)
            v.check_presentation(proof,'kano',1)

    def test_actual_wrong_display_latch(self):
        with self.assertRaises((ValueError,AssertionError)):
            proof=self.mutate_actual('SNAP','start',0x1000)
            v.check_presentation(proof,'kano',1)

    def test_actual_prepass_is_required(self):
        evidence=copy.deepcopy(self.rows);evidence['PRE'].pop(0)
        with patch.object(model,'rows',side_effect=lambda log,name:evidence[name]):
            with self.assertRaises(KeyError):model.inspect(self.folder)


if __name__=='__main__':unittest.main()
