"""Mutate real four-slot native finisher records, preserving art gaps."""
import argparse
import io
import json
import re
import unittest
from pathlib import Path
import verify_reptile_victims_v890 as proof

class VictimTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.texts={case:(proof.ROOT/case/'run.log').read_text(encoding='utf-8-sig')for case in proof.CASES}
 def report(self,texts=None):return proof.verify(texts=self.texts if texts is None else texts,check_files=False)
 def changed(self,fn):
  texts=dict(self.texts);case=proof.CASES[0];texts[case]=fn(texts[case]);self.assertNotEqual(texts[case],self.texts[case]);return texts
 def reject(self,label,fn):
  r=self.report(self.changed(fn));self.assertFalse(r['passed']);self.assertTrue(any(label in e for e in r['errors']),r['errors'])
 def test_baseline_is_runtime_repair_not_complete_art(self):
  r=self.report();self.assertTrue(r['passed'],r['errors']);self.assertEqual(len(r['cases']),4)
  self.assertFalse(r['fullPortAcceptance']);self.assertFalse(r['fullNativeDeathArtAcceptance'])
  self.assertTrue(all(v['remainingHeadIsLiu']for v in r['cases'].values()))
 def test_missing_action(self):self.reject('one complete original fatality',lambda t:re.sub(r'^MK2_REPTILE_V879_ACTION .*\n','',t,flags=re.M))
 def test_proxy_selection(self):self.reject('actual Reptile and true victim',lambda t:t.replace('ids=9,18','ids=9,1',1))
 def test_illegal_health_writer(self):self.reject('original physical health writers only',lambda t:t.replace('pc=FF836700','pc=FF838860',1))
 def test_insufficient_real_damage(self):
  self.reject('observed 322 damage',lambda t:re.sub(r'^MK2_REPTILE_V879_HEALTH .*before=161 after=121 pc=FF836700\n','',t,count=1,flags=re.M))
 def test_missing_command(self):
  self.reject('real Back Back Down LP',lambda t:re.sub(r'^MK2_REPTILE_V879_INPUT .*button=Low_Punch\n','',t,flags=re.M))
 def test_wrong_native_row_pc(self):self.reject('exact original four-field',lambda t:t.replace('pc=FF8C8AA0','pc=FFA59F10',1))
 def test_wrong_victim_animation(self):self.reject('exact original four-field',lambda t:t.replace('data=0010 mask=FFFF pc=FF8C8AF0','data=2710 mask=FFFF pc=FF8C8AF0',1))
 def test_wrong_actual_palette(self):self.reject('real independent normal palette',lambda t:t.replace('pointer=FFFED800','pointer=FFADD0D0',1))
 def test_body_palette_cannot_be_effect_only(self):
  self.reject('physical body palette',lambda t:t.replace('actor=010350A0 main=0106B150 id=18 flags=001E','actor=01000000 main=0106B150 id=18 flags=001E',1))
 def test_missing_native_wrap(self):self.reject('one complete original fatality',lambda t:re.sub(r'^MK2_REPTILE_V879_WRAP .*\n','',t,flags=re.M))
 def test_wrong_native_completion_age(self):self.reject('native completion 90 fields',lambda t:t.replace('age=187 pc=FF8C9690','age=79435 pc=FF8C9690',1))
 def test_missing_runtime_head_gap(self):self.reject('one complete original fatality',lambda t:re.sub(r'^MK2_REPTILE_V879_HEAD .*\n','',t,flags=re.M))
 def test_boot_picture_is_not_finisher(self):self.reject('actual full finisher snapshot chronology',lambda t:t.replace('DISPLAY frame=3135','DISPLAY frame=1',1))
 def test_cache_overrun_cannot_be_ignored(self):
  self.reject('no body-cache overrun',lambda t:t+'\nMK2_REPTILE_V879_CACHE_OVERWRITE frame=3265 victim=sonya side=2 writes=0 assistance=none at=01060130 data=7E7F mask=FFFF\n')
 def test_both_slots_required(self):
  texts=dict(self.texts);del texts[proof.CASES[1]];r=self.report(texts)
  self.assertFalse(r['passed']);self.assertIn('Both true victims in both physical slots',r['errors'])

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 if args.output.exists():raise ValueError('Preserve unit evidence')
 args.output.mkdir();stream=io.StringIO()
 result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(VictimTests))
 (args.output/'run.log').write_text(stream.getvalue())
 report={'passed':result.wasSuccessful(),'methods':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
         'scope':'four true-ID native victim runtime gate, not death art acceptance'}
 (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
 raise SystemExit(0 if result.wasSuccessful()else 1)
if __name__=='__main__':main()
