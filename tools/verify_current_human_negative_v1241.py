"""Fresh genuine blocked/missed specials and paired recovery, corrected build."""
import json,re
from PIL import Image
import verify_current_human_moves_v1238 as positive
import verify_human_special_negative_v6 as negative
ROOT=positive.ROOT;OUT=ROOT/'audit_v1241_current_human_negative_checked'

def verify():
 pins={};cases=[];candidate=positive.current.physical.headed.CANDIDATE
 def pin(path,wanted=None):
  actual=positive.current.util.digest(path);assert wanted is None or actual==wanted,'Changed input '+str(path);pins[str(path)]=actual
 build_path=ROOT/candidate/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
 positive.current.physical.headed.reconstruct()
 for file,wanted in build['input_hashes'].items():pin(file,wanted)
 fixtures=[(m,s,k) for m in positive.positive.SPECS for s in (1,2) for k in ('block','miss')]+[('leg',s,'duck_block') for s in (1,2)]
 for move,side,scenario in fixtures:
  folder=ROOT/f'audit_v1240_human_{move}_{scenario}_p{side}'
  launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  assert launch['exit_code']==0 and launch['candidate']==candidate and launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
  assert launch['move']==move and launch['side']==side and launch['scenario']==scenario and launch['victim']=='sub_zero' and launch['assistance']=='none' and launch['cheats_enabled'] is False
  for file,wanted in launch['input_hashes'].items():pin(file,wanted)
  observer=(folder/'input_sources/mk2ks_human_special_negative_v9.lua').read_text()
  assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Standalone unassisted input observer'
  log=(folder/'run.log').read_text(encoding='utf-8-sig')
  result=negative.verify_log(log,move,side,scenario)
  if move=='ball':
   negative.verify_repel(log,side)
   if scenario=='block':result.update(negative.verify_rebound(log,side,True))
  result['case']=folder.name;cases.append(result)
  for filename in ('special_before.png','special_recovered.png','special_final.png'):
   assert Image.open(folder/'snap'/filename).size==(400,254)
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
 positive_path=positive.OUT/'report.json';prior=json.loads(positive_path.read_text());pin(positive_path)
 assert prior['passed'] and prior['candidate']==candidate and len(prior['cases'])==18
 for file,wanted in prior['inputHashes'].items():pin(file,wanted)
 for filename in ('tools/verify_current_human_negative_v1241.py','tools/verify_human_special_negative_v6.py',
  'tools/run_current_human_negative_v1240.ps1','mk2ks_human_special_negative_v9.lua'):
  pin(ROOT/filename)
 assert len(cases)==34
 return dict(passed=True,candidate=candidate,cases=cases,positiveCases=18,negativeCases=34,
  current52CaseHumanStateMatrixAccepted=True,currentKnifeRingPhysicalRegressionAccepted=True,
  pairedFields=sum(r['fields'] for r in cases)+prior['pairedFields'],inputHashes=pins,
  scope='Cold actual-input specials against Sub-Zero: contact/blocked/miss, leg duck-block, true paired identity, natural recovery and walking/jumping/punch follow-up; not complete moves/art/audio/CPU/arenas acceptance.',
  allMoveArtAccepted=False,allVictimsAccepted=False,CPUAccepted=False,audioAccepted=False,allArenasAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists(),'Preserve every executed result'
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Current 34 defensive/miss +18 positive human cases passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
