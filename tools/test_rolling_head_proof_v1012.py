"""Corruption-rejection tests with unchanged real runtime evidence as fixtures.

Cache only exact immutable pixel-match inputs for repeated trace mutations.
The explicit blank-picture mock bypasses that cache and runs the real image
matcher. No source/ROM/evidence files or artwork are modified.
"""
import copy
import hashlib
import json
import re
import struct
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import verify_rolling_heads_v1010 as proof

ROOT=proof.ROOT
OUT=ROOT/'audit_v1012_rolling_head_corruption_units'
CASE=proof.CASES[0]
BASE={case:(ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in proof.CASES}
ORIGINAL_MATCH=proof.pixel_match
CACHE={}
CHECKS=[]
BLANK_PATH=None


def cached_match(path,indices,palette,flip):
    if path==BLANK_PATH:return ORIGINAL_MATCH(path,indices,palette,flip)
    key=(str(path),proof.digest(path),indices.shape,indices.tobytes(),palette.tobytes(),flip)
    if key not in CACHE:CACHE[key]=ORIGINAL_MATCH(path,indices,palette,flip)
    return CACHE[key].copy()


def replace_field(tag,key,value,filter_text=None):
    text=BASE[CASE]
    for line in text.splitlines():
        if line.startswith(tag+' ') and (filter_text is None or filter_text in line):
            changed=re.sub(r'(?<=\s)'+re.escape(key)+r'=[^\s]+',key+'='+str(value),line,count=1)
            assert changed!=line,(tag,key,value)
            return text.replace(line,changed,1)
    raise AssertionError('Missing immutable mutation fixture: '+tag)


class CorruptionTests(unittest.TestCase):
    def test_original_matrix(self):
        report=proof.verify(BASE,check_files=False)
        self.assertTrue(report['passed'],report['errors']);CHECKS.append('unchanged real matrix passes')

    def test_trace_corruptions(self):
        art='MK2_ROLLING_HEAD_V1003_';stock='MK2_STOCK_HEAD_V921_'
        mutations={
            'proxy live identity':replace_field(stock+'FIRST_LIVE','ids','3,1'),
            'wrong original health writer':replace_field(stock+'HEALTH','pc','FF836710',filter_text='pc=FF836700'),
            'unearned damage':replace_field(stock+'ACTION','damage','321'),
            'wrong accepted back token':replace_field(stock+'COMPARE','actual','7',filter_text='table=FF87AA00'),
            'wrong parser comparison timing':replace_field(stock+'COMPARE','tick','999',filter_text='table=FF87AA00'),
            'native timing drift':replace_field(stock+'WRAP','age','175'),
            'no real continuation':replace_field(stock+'MODE','mode','0',filter_text='mode=3'),
            'false terminal wins':replace_field(stock+'RESULT','wins','1'),
            'wrong native head identity':replace_field(art+'QUEUE','id','1',filter_text='source=0F62B0A0'),
            'wrong independent head descriptor':replace_field(art+'QUEUE','cache','FFB4A4B0',filter_text='source=0F62B0A0'),
            'head actor substituted for physical body':replace_field(art+'QUEUE','actor','01034E90',filter_text='source=0F62B0A0'),
            'wrong native body floor':replace_field(art+'QUEUE','floor','81',filter_text='source=0F600000'),
            'wrong measured camera projection':replace_field(art+'QUEUE','cameraY','-7',filter_text='source=0F600000'),
            'FIFO DMA mismatch':replace_field(art+'DMA','queue_match','0',filter_text='source=0F600000'),
            'wrong actual DMA dimensions':replace_field(art+'DMA','width','1',filter_text='source=0F600000'),
            'foreign physical owner':replace_field(art+'QUEUE','physical','010350A0',filter_text='source=0F600000'),
            'wrong actual palette bank':replace_field(art+'DMA','palette','0300',filter_text='source=0F600000'),
            'observer claims assistance':replace_field(art+'DMA','assistance','hidden_write',filter_text='source=0F600000'),
            'previous-page snapshot':replace_field(art+'POSE_SNAPSHOT','queued_frame','1',filter_text='source=0F62B0A0'),
        }
        for label,text in mutations.items():
            with self.subTest(label=label):
                modified=BASE.copy();modified[CASE]=text
                report=proof.verify(modified,check_files=False)
                self.assertFalse(report['passed'],label);CHECKS.append(label)

    def test_actual_binary_corruptions(self):
        directory=ROOT/CASE
        palette=next(directory.glob('death_palette_0F62B0A0_*.bin'))
        original=Path.read_bytes
        for filename in (directory/'guest_maincpu.bin',directory/'native_death_gfx.bin',palette):
            with self.subTest(filename=filename.name):
                def altered(path):
                    data=original(path)
                    if path==filename:
                        data=bytearray(data);data[4 if filename==palette else 0]^=1;return bytes(data)
                    return data
                with patch.object(Path,'read_bytes',altered):
                    report=proof.verify(BASE,check_files=False)
                self.assertFalse(report['passed'],filename.name);CHECKS.append('reject corrupt actual '+filename.name)

    def test_payload_corruptions(self):
        payload=(ROOT/proof.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
        for offset,label in ((0x160008,'header graphics length'),(0x160400+7*20,'tested upright head'),
                             (0x160400+9*20,'rotating head geometry'),(0x164000,'existing body pixels'),
                             (0x17004c,'new diagonal pixels'),(death_offset:=((0xff00b910-0xfe800000)//8),'native main61 grammar'),
                             (0xfda00,'native palette record')):
            with self.subTest(label=label):
                data=bytearray(payload);data[offset]^=1
                with self.assertRaises(AssertionError):proof.verify_payload(bytes(data))
                CHECKS.append('reject corrupt '+label)

    def test_blank_actual_picture(self):
        global BLANK_PATH
        report=json.loads((ROOT/'audit_v1010_owned_rolling_head_runtime_checked/verification.json').read_text())
        item=next(r for r in report['cases'][CASE]['pixelMatches'] if r['kind']=='head' and r['pose']==2)
        BLANK_PATH=Path(item['snapshot']);original=Image.open
        def blank(path,*args,**kwargs):
            if Path(path)==BLANK_PATH:return Image.new('RGB',(400,254),(0,0,0))
            return original(path,*args,**kwargs)
        try:
            with patch.object(Image,'open',blank):report=proof.verify(BASE,check_files=False)
            self.assertFalse(report['passed']);CHECKS.append('reject absent head pixels in presented PNG')
        finally:BLANK_PATH=None


if __name__=='__main__':
    if OUT.exists():raise ValueError('Preserve corruption test evidence')
    proof.pixel_match=cached_match
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(CorruptionTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    OUT.mkdir();data=dict(passed=result.wasSuccessful(),testMethods=result.testsRun,
                         fixtureAndCorruptionChecks=len(CHECKS),checks=CHECKS,
                         errors=[str(r) for r in result.errors],failures=[str(r) for r in result.failures],
                         sourceOrEvidenceFileWrites=0,fullPortAccepted=False)
    (OUT/'unit-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2));raise SystemExit(0 if data['passed'] else 1)
