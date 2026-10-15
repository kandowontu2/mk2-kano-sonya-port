"""Exact current native defensive states/full screens after bounded audio fix."""
import json,re
from pathlib import Path
import verify_native_grab_audio_v1415 as source
import verify_human_special_negative_v6 as negative
ROOT=source.ROOT;OUT=ROOT/'audit_v1421_grab_defense_checked'
FIXTURES=[(m,s,k)for m in ('choke','leg')for s in (1,2)for k in ('block','miss')]+[('leg',s,'duck_block')for s in (1,2)]

def verify():
 pins={};cases=[]
 def pin(path,wanted=None):
  path=Path(path);key=str(path)
  if key not in pins:pins[key]=source.prior.digest(path)
  source.need(wanted is None or pins[key]==wanted,'Changed source/evidence '+key)
 proof_path=source.OUT/'report.json';proof=json.loads(proof_path.read_text());pin(proof_path)
 source.need(proof['passed'] and proof['candidate']==source.NAME and proof['wholeGuestIndependentlyReconstructed'],'Whole rebuilt native source contract')
 for p,h in proof['inputHashes'].items():pin(p,h)
 compiled=json.loads((ROOT/source.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 for move,side,scenario in FIXTURES:
  folder=ROOT/f'audit_v1417_human_{move}_{scenario}_p{side}';old=ROOT/f'audit_v1365_human_{move}_{scenario}_p{side}'
  launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
  source.need(launch['exit_code']==0 and launch['candidate']==source.NAME and launch['executable_sha256']==compiled['executable_sha256'] and launch['payload_sha256']==compiled['payload_sha256'] and launch['move']==move and launch['side']==side and launch['scenario']==scenario and launch['victim']=='sub_zero' and not launch['cheats_enabled'] and launch['assistance']=='none','Actual current native defensive case')
  source.need(before==launch['input_hashes'] and all(before.get(p)==h for p,h in compiled['input_hashes'].items()),'Executed complete source manifest')
  for p,h in before.items():
   pin(p,h)
   if Path(p).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(p).name,h)
  log=(folder/'run.log').read_text(encoding='utf-8-sig');result=negative.verify_log(log,move,side,scenario)
  events=lambda text:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line)for line in text.splitlines()if line.startswith('MK2_HSPECIAL_')]
  source.need(events(log)==events((old/'run.log').read_text(encoding='utf-8-sig')),'All real input/character/action/contact/recovery events remain exact')
  for name in ('special_before.png','special_recovered.png','special_final.png'):
   pin(old/'snap'/name)
   source.need((folder/'snap'/name).read_bytes()==(old/'snap'/name).read_bytes(),'Original complete actual defensive screens remain byte-exact')
  result.update(case=folder.name,everyPriorNativeHumanEventMatched=True,exactPriorActualFullScreensMatched=3);cases.append(result)
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
 for name in ('tools/verify_grab_defense_regression_v1421.py','tools/verify_human_special_negative_v6.py','tools/run_grab_audio_defense_batch_v1416.py'):pin(ROOT/name)
 return dict(passed=True,candidate=source.NAME,cases=cases,everyPriorNativeHumanEventMatched=True,exactPriorActualFullScreensMatched=30,inputHashes=pins,
  scope='Ten genuine choke/leg block/miss/leg duck-block native event/full-screen regressions after native grab cues; no all-victim/CPU/KO/audio/full-port claim',audioAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 source.need(not OUT.exists(),'Never overwrite evidence')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),cases=len(report.get('cases',[]))),indent=2),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
