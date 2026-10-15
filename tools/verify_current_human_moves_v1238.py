"""Fresh actual-input positive moves and recovery on the corrected build.

Eighteen cases: all eight authored specials in both slots, plus real airborne
square-wave contact. This does not assert final art/audio/CPU/negative scope.
"""
import json,re
from PIL import Image
import verify_stock_secondary_display_v1234 as current
import verify_human_special_matrix as positive
ROOT=current.ROOT;OUT=ROOT/'audit_v1238_current_human_moves_checked'

def verify():
 pins={};cases=[]
 def pin(path,wanted=None):
  actual=current.util.digest(path);assert wanted is None or actual==wanted,'Changed input '+str(path);pins[str(path)]=actual
 candidate=current.physical.headed.CANDIDATE
 build_path=ROOT/candidate/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
 _,_,_,payload=current.physical.headed.reconstruct()
 assert payload==(ROOT/candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
 for file,wanted in build['input_hashes'].items():pin(file,wanted)
 for move,side,air in [(m,s,False) for m in positive.SPECS for s in (1,2)]+[('square',s,True) for s in (1,2)]:
  suffix=move+'_air' if air else move;folder=ROOT/f'audit_v1236_human_{suffix}_p{side}'
  launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  assert launch['candidate']==candidate and launch['exit_code']==0 and launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
  assert launch['move']==move and launch['side']==side and launch['air']==air and launch['victim']=='sub_zero' and launch['assistance']=='none' and launch['cheats_enabled'] is False
  for file,wanted in launch['input_hashes'].items():pin(file,wanted)
  observer=(folder/'input_sources/mk2ks_human_special_matrix_v3.lua').read_text()
  assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Standalone physical inputs and read-only observation'
  log=(folder/'run.log').read_text(encoding='utf-8-sig');result=positive.verify_log(log,move,side,air);result['case']=folder.name;cases.append(result)
  for filename in ('special_before.png','special_recovered.png','special_final.png'):
   path=folder/'snap'/filename;assert Image.open(path).size==(400,254)
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
 for filename in ('tools/verify_current_human_moves_v1238.py','tools/verify_human_special_matrix.py','tools/run_current_human_special_v820.ps1','mk2ks_human_special_matrix_v3.lua','tools/verify_native_headed_reaction_v1221.py'):
  pin(ROOT/filename)
 assert len(cases)==18
 return dict(passed=True,candidate=candidate,executableSHA256=build['executable_sha256'],payloadSHA256=build['payload_sha256'],
  cases=cases,pairedFields=sum(r['fields'] for r in cases),currentAllEightHumanPositiveCommandContactRecoveryAccepted=True,
  currentKnifeRingPhysicalRegressionAccepted=True,wholePayloadIndependentlyReconstructed=True,inputHashes=pins,
  allMoveArtAccepted=False,negativeCasesAccepted=False,allVictimsAccepted=False,CPUAccepted=False,audioAccepted=False,
  allArenasAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists(),'Keep executed evidence immutable'
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Current human positive moves passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
