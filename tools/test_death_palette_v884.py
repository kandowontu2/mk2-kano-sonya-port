"""Reject corrupt native palette-table and actual-runtime evidence."""
import argparse
import io
import json
import re
import unittest
from pathlib import Path
import verify_death_palette_v882 as proof

class PaletteTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.before=proof.BEFORE.read_bytes();cls.after=proof.AFTER.read_bytes()
  cls.texts={name:(proof.ROOT/name/'run.log').read_text(encoding='utf-8-sig')for name in proof.CASES}
 def report(self,**changes):
  args=dict(before=self.before,after=self.after,texts=self.texts,check_files=False);args.update(changes)
  return proof.verify(**args)
 def reject(self,label,**changes):
  result=self.report(**changes);self.assertFalse(result['passed']);self.assertTrue(any(label in e for e in result['errors']),result['errors'])
 def text_change(self,fn):
  texts=dict(self.texts);name=proof.CASES[0];texts[name]=fn(texts[name]);self.assertNotEqual(texts[name],self.texts[name]);return texts
 def test_baseline_has_no_art_or_unobserved_runtime_promotion(self):
  r=self.report();self.assertTrue(r['passed'],r['errors']);self.assertEqual(r['guestChangedBytes'],119)
  for key in('fullPortAcceptance','nativeDeathArtAccepted','kanoPaletteRuntimeProven','alternatePaletteRuntimeProven','completeHeadBiteRuntimeProven'):
   self.assertFalse(r[key])
 def test_stock_row_change(self):
  d=bytearray(self.after);d[0xfa900+4*8]^=1;self.reject('Only full native palette table',after=d)
 def test_kano_row_change(self):
  d=bytearray(self.after);d[0xfa900+17*8]^=1;self.reject('Only full native palette table',after=d)
 def test_alternate_row_change(self):
  d=bytearray(self.after);d[0xfa900+18*8+4]^=1;self.reject('Only full native palette table',after=d)
 def test_unrelated_native_code_change(self):
  d=bytearray(self.after);d[proof.at(0xff8366c0)]^=1;self.reject('Only full native palette table',after=d)
 def test_owned_palette_color_change(self):
  d=bytearray(self.after);d[0xfdb00+12]^=1;self.reject('Owned normal/alternate costume palettes preserved',after=d)
 def test_wrong_native_halfword(self):
  texts=self.text_change(lambda t:t.replace('part=0 at=FFFD4C80 data=D800','part=0 at=FFFD4C80 data=D000',1))
  self.reject('exact native palette halfword',texts=texts)
 def test_rom_dump_cannot_impersonate_native_read(self):
  texts=self.text_change(lambda t:t.replace('mask=FFFF pc=FF90C8D0','mask=FFFF pc=FFA59F10',1))
  self.reject('exact native palette halfword',texts=texts)
 def test_wrong_actual_pointer(self):
  texts=self.text_change(lambda t:t.replace('pointer=FFFED800 pc=FF90C8E0','pointer=FFADD0D0 pc=FF90C8E0',1))
  self.reject('actual pointer after both native reads',texts=texts)
 def test_missing_halfword(self):
  texts=self.text_change(lambda t:re.sub(r'^MK2_NAT_CAMPAIGN_HEADLESS_PALETTE .*part=1 .*\n','',t,count=1,flags=re.M))
  self.reject('actual pointer after both native reads',texts=texts)
 def test_effects_cannot_stand_in_for_physical_victim(self):
  texts=self.text_change(lambda t:re.sub(r'(MK2_NAT_CAMPAIGN_LIVE .*human_actor=)[0-9A-F]+',r'\g<1>01000000',t))
  self.reject('actual physical Sonya palette uses',texts=texts)
 def test_machine_reset_is_not_waived(self):
  texts=self.text_change(lambda t:t+'\nMK2_NAT_CAMPAIGN_REENTRY writes=0 assistance=none\n')
  self.reject('no reset/cache overrun',texts=texts)
 def test_illegal_health_writer(self):
  texts=self.text_change(lambda t:t.replace('pc=FF836700 a8=','pc=FF838860 a8=',1))
  self.reject('exact physical-slot health writer',texts=texts)
 def test_prior_input_chronology(self):
  texts=self.text_change(lambda t:t.replace('button=High_Punch selection=0','button=Low_Punch selection=0',1))
  self.reject('Exact prior input/state chronology',texts=texts)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
 if args.output.exists():raise ValueError('Preserve unit evidence')
 args.output.mkdir();stream=io.StringIO()
 result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PaletteTests))
 (args.output/'run.log').write_text(stream.getvalue())
 report={'passed':result.wasSuccessful(),'methods':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),
         'scope':'native table/palette/runtime verifier mutations, not complete death art or port'}
 (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
 raise SystemExit(0 if result.wasSuccessful()else 1)
if __name__=='__main__':main()
