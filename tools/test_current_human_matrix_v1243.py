"""Current 52-case state contracts reject altered records, in memory only."""
import json,re,unittest
import verify_current_human_negative_v1241 as audit
OUT=audit.ROOT/'audit_v1243_current_human_matrix_corruption_checks';assert not OUT.exists()

def check(log,move,side,scenario=None,air=False):
 if scenario is None:return audit.positive.positive.verify_log(log,move,side,air)
 result=audit.negative.verify_log(log,move,side,scenario)
 if move=='ball':
  audit.negative.verify_repel(log,side)
  if scenario=='block':audit.negative.verify_rebound(log,side,True)
 return result

class CurrentMatrix(unittest.TestCase):
 def log(self,move,side,scenario=None):
  name=f'audit_v1236_human_{move}_p{side}' if scenario is None else f'audit_v1240_human_{move}_{scenario}_p{side}'
  return (audit.ROOT/name/'run.log').read_text(encoding='utf-8-sig')
 def reject(self,log,move,side,scenario=None,air=False):
  with self.assertRaises(ValueError):check(log,move,side,scenario,air)
 def test_all_52_actual_cases(self):
  report=audit.verify();self.assertTrue(report['passed']);self.assertEqual(report['positiveCases']+report['negativeCases'],52)
 def test_missing_field(self):
  log=self.log('ring',1);changed=re.sub(r'^MK2_HSPECIAL_FIELD[^\n]+\n','',log,count=1,flags=re.M)
  self.assertNotEqual(log,changed);self.reject(changed,'ring',1)
 def test_wrong_identity(self):
  log=self.log('ring',2);changed=log.replace('id=18','id=1',1)
  self.assertNotEqual(log,changed);self.reject(changed,'ring',2)
 def test_missing_native_entry(self):
  log=self.log('blade',1);changed=re.sub(r'^MK2_HSPECIAL_EVENT[^\n]*entry=FFF8CC00[^\n]+\n','',log,flags=re.M)
  self.assertNotEqual(log,changed);self.reject(changed,'blade',1)
 def test_missing_health_store(self):
  log=self.log('leg',2);changed=re.sub(r'^MK2_HSPECIAL_HEALTH[^\n]+\n','',log,flags=re.M)
  self.assertNotEqual(log,changed);self.reject(changed,'leg',2)
 def test_ball_forward_rebound(self):
  log=self.log('ball',1,'block');changed=re.sub(r'(MK2_HSPECIAL_FIELD[^\n]*slot=1[^\n]*vx=)[0-9A-F]+([^\n]*action=1538)',r'\g<1>000A0000\2',log)
  self.assertNotEqual(log,changed);self.reject(changed,'ball',1,'block')
 def test_ball_missing_geometry(self):
  log=self.log('ball',2,'miss');changed=re.sub(r'^MK2_HSPECIAL_GEOMETRY[^\n]+\n','',log,count=1,flags=re.M)
  self.assertNotEqual(log,changed);self.reject(changed,'ball',2,'miss')
 def test_ground_square_not_air_contact(self):self.reject(self.log('square',1),'square',1,air=True)
 def test_leg_standing_block_not_duck(self):self.reject(self.log('leg',2,'block'),'leg',2,'duck_block')

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CurrentMatrix))
 report=dict(passed=result.wasSuccessful(),testsRun=result.testsRun,failures=[(str(t),s) for t,s in result.failures],
  errors=[(str(t),s) for t,s in result.errors],inMemoryOnly=True,actualRuntimeEvidenceChanged=False,fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit(0 if report['passed'] else 1)
