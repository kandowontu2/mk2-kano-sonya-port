"""Fresh full bounded 52-case native move regression against current v1340."""
import json,re
from pathlib import Path
from PIL import Image
import verify_native_grab_audio_v1415 as source
import verify_sonya_launch_audio_v1489 as launch
import verify_human_special_matrix as positive
import verify_human_special_negative_v6 as negative
ROOT=source.ROOT;NAME=launch.NAME;OUT=ROOT/'audit_v1502_launch_audio_human_matrix_checked'

def verify():
 pins={};cases=[];images=0
 def pin(path,wanted=None):
  path=Path(path);key=str(path)
  if key not in pins:pins[key]=source.prior.digest(path)
  source.need(wanted is None or pins[key]==wanted,'Changed evidence '+key)
 proofpath=launch.OUT/'report.json';proof=json.loads(proofpath.read_text());pin(proofpath)
 source.need(proof['passed'] and proof['candidate']==NAME and proof['wholeGuestIndependentlyReconstructed'],'Complete current native source/guest proof')
 for p,h in proof['inputHashes'].items():pin(p,h)
 buildpath=ROOT/NAME/'build-info.json';compiled=json.loads(buildpath.read_text(encoding='utf-8-sig'));pin(buildpath)
 priorpath=ROOT/'audit_v1435_grab_audio_human_matrix_checked/report.json';prior=json.loads(priorpath.read_text());pin(priorpath)
 source.need(prior['passed'] and prior['candidate']==source.NAME and prior['current52CaseHumanStateMatrixAccepted'],'Current baseline native matrix accepted')
 for p,h in prior['inputHashes'].items():pin(p,h)
 fixtures=[(m,s,None,False)for m in positive.SPECS for s in (1,2)]+[('square',s,None,True)for s in (1,2)]+[(m,s,k,False)for m in positive.SPECS for s in (1,2)for k in ('block','miss')]+[('leg',s,'duck_block',False)for s in (1,2)]
 for move,side,scenario,air in fixtures:
  suffix=move+('_air'if air else '_'+scenario if scenario else '')
  folder=ROOT/f'audit_v1499_human_{suffix}_p{side}';baseline=ROOT/f'audit_v1430_human_{suffix}_p{side}'
  launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
  source.need(launch['exit_code']==0 and launch['candidate']==NAME and launch['executable_sha256']==compiled['executable_sha256'] and launch['payload_sha256']==compiled['payload_sha256'] and launch['move']==move and launch['side']==side and launch['victim']=='sub_zero' and launch['cheats_enabled'] is False and launch['assistance']=='none','Actual matched current native fixture')
  source.need(launch['scenario']==scenario if scenario else launch['air']==air,'Actual declared defense/air fixture')
  source.need(before==launch['input_hashes'] and all(before.get(p)==h for p,h in compiled['input_hashes'].items()),'Complete executed source manifest')
  for p,h in before.items():
   pin(p,h)
   if Path(p).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(p).name,h)
  observer='mk2ks_human_special_negative_v9.lua'if scenario else'mk2ks_human_special_matrix_v3.lua'
  text=(folder/'input_sources'/observer).read_text()
  source.need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',text),'Read-only actual physical input observer')
  log=(folder/'run.log').read_text(encoding='utf-8-sig');old=(baseline/'run.log').read_text(encoding='utf-8-sig')
  source.need(not re.search('WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation',log,re.I),'No emulator/ROM runtime error')
  events=lambda value:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line)for line in value.splitlines()if line.startswith('MK2_HSPECIAL_')]
  source.need(events(log)==events(old),'Every actual native input/identity/pose/contact/health/recovery event remains exact: '+folder.name)
  result=negative.verify_log(log,move,side,scenario)if scenario else positive.verify_log(log,move,side,air)
  if move=='ball' and scenario:
   negative.verify_repel(log,side)
   if scenario=='block':result.update(negative.verify_rebound(log,side,True))
  result['case']=folder.name;cases.append(result)
  for filename in ('special_before.png','special_recovered.png','special_final.png'):
   path=folder/'snap'/filename;oldpath=baseline/'snap'/filename
   source.need(Image.open(path).size==(400,254),'Complete native snapshot dimensions')
   source.need(path.read_bytes()==oldpath.read_bytes(),'Unexpected complete-scene regression: '+str(path))
   images+=1;pin(oldpath)
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
 for name in ('tools/verify_launch_audio_human_matrix_v1502.py','tools/verify_human_special_matrix.py','tools/verify_human_special_negative_v6.py','tools/run_launch_audio_regression_v1498.py','tools/run_current_human_special_v820.ps1','tools/run_current_human_negative_v1240.ps1'):pin(ROOT/name)
 source.need(len(cases)==52 and images==156,'Complete unchanged broad matrix')
 return dict(passed=True,candidate=NAME,cases=cases,positiveCases=18,negativeCases=34,pairedFields=sum(c['fields']for c in cases),everyPriorNativeHumanEventMatched=True,
  exactPriorActualFullScreensMatched=images,current52CaseHumanStateMatrixAccepted=True,inputHashes=pins,
  allMoveChoreographyAccepted=False,audioAccepted=False,CPUAccepted=False,allArenasAccepted=False,fullPortAccepted=False,
  scope='Full current 52 bounded human moves/contact/blocks/misses/recovery matrix and byte-exact complete before/recovered/final screens; not all-victim, repeated/KO/CPU/full move choreography/audio/full-game integration')

if __name__=='__main__':
 source.need(not OUT.exists(),'Never overwrite evidence')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),cases=len(report.get('cases',[])),exactScreens=report.get('exactPriorActualFullScreensMatched')),indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
