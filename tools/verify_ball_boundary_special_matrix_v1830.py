"""Fresh 52-case physical special regression for the native ball boundary fix.

50 fixtures must preserve all previous native events and full endpoint scenes.
Two positive ball fixtures instead prove the intentional native boundary delta,
with exact full raster, native shadows and continuous erase for both slots.
This is not universal victim, arena, CPU, repeat, audio or whole-port acceptance.
"""
import json,re
from pathlib import Path
from PIL import Image
import verify_native_grab_audio_v1415 as source
import verify_ball_boundary_source_v1817 as audio_source
import verify_ball_boundary_runtime_v1825 as boundary
import verify_human_special_matrix as positive
import verify_human_special_negative_v6 as negative
ROOT=source.ROOT;NAME=audio_source.NAME;OUT=ROOT/'audit_v1830_ball_boundary_special_matrix_checked'

def verify():
 pins={};cases=[];images=0
 def pin(path,wanted=None):
  path=Path(path);key=str(path)
  if key not in pins:pins[key]=source.prior.digest(path)
  source.need(wanted is None or pins[key]==wanted,'Changed evidence '+key)
 proofpath=audio_source.OUT/'report.json';proof=json.loads(proofpath.read_text());pin(proofpath)
 source.need(proof['passed'] and proof['candidate']==NAME and proof['wholeActualGuestExactlyCallbackDelta'],'Complete current native source/guest proof')
 for p,h in proof['inputHashes'].items():pin(p,h)
 buildpath=ROOT/NAME/'build-info.json';compiled=json.loads(buildpath.read_text(encoding='utf-8-sig'));pin(buildpath)
 priorpath=ROOT/'audit_v1623_ground_throw_special_matrix_checked/report.json';prior=json.loads(priorpath.read_text());pin(priorpath)
 source.need(prior['passed'] and prior['candidate']=='diagnostic_v1597_native_ground_throw' and prior['current52CaseHumanStateMatrixAccepted'],'Current baseline native matrix accepted')
 for p,h in prior['inputHashes'].items():pin(p,h)
 fixtures=[(m,s,None,False)for m in positive.SPECS for s in (1,2)]+[('square',s,None,True)for s in (1,2)]+[(m,s,k,False)for m in positive.SPECS for s in (1,2)for k in ('block','miss')]+[('leg',s,'duck_block',False)for s in (1,2)]
 for move,side,scenario,air in fixtures:
  suffix=move+('_air'if air else '_'+scenario if scenario else '')
  revised_ball=move=='ball'and scenario is None
  folder=ROOT/(f'audit_v1824_human_ball_p{side}_boundary'if revised_ball else f'audit_v1829_human_{suffix}_p{side}');baseline=ROOT/f'audit_v1620_human_{suffix}_p{side}'
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
  if not revised_ball:source.need(events(log)==events(old),'Every actual native input/identity/pose/contact/health/recovery event remains exact: '+folder.name)
  else:
   causal=boundary.verify(log,side);source.need(causal['passed'],'Actual native ball clamp preserves true identity/damage/choreography')
   for kind,version in (('render',1826),('erase',1827)):
    rp=ROOT/f'audit_v{version}_human_ball_p{side}_{kind}_checked/report.json';rr=json.loads(rp.read_text());pin(rp)
    source.need(rr['passed'],'Full consecutive native ball '+kind)
    for p,h in rr['inputHashes'].items():pin(p,h)
   source.need(rr['oneInitialBaseOnly']and not rr['laterBuffersUsedAsAnchors'],'No later buffer anchor conceals erasure')
  result=negative.verify_log(log,move,side,scenario)if scenario else positive.verify_log(log,move,side,air)
  if move=='ball' and scenario:
   negative.verify_repel(log,side)
   if scenario=='block':result.update(negative.verify_rebound(log,side,True))
  result['case']=folder.name;cases.append(result)
  for filename in ('special_before.png','special_recovered.png','special_final.png'):
   path=folder/'snap'/filename;oldpath=baseline/'snap'/filename
   source.need(Image.open(path).size==(400,254),'Complete native snapshot dimensions')
   if not revised_ball or filename=='special_before.png':
    source.need(path.read_bytes()==oldpath.read_bytes(),'Unexpected complete-scene regression: '+str(path));images+=1;pin(oldpath)
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
 for name in ('tools/verify_ball_boundary_special_matrix_v1830.py','tools/verify_human_special_matrix.py','tools/verify_human_special_negative_v6.py','tools/run_ground_throw_special_matrix_v1619.py','tools/run_current_human_special_v820.ps1','tools/run_current_human_negative_v1240.ps1'):pin(ROOT/name)
 source.need(len(cases)==52 and images==152,'Complete unchanged broad matrix')
 return dict(passed=True,candidate=NAME,cases=cases,positiveCases=18,negativeCases=34,pairedFields=sum(c['fields']for c in cases),fiftyUnaffectedFixturesEveryPriorNativeHumanEventMatched=True,bothPositiveBallBoundaryAndFullRasterShadowEraseAccepted=True,
  exactPriorActualFullScreensMatched=images,current52CaseHumanStateMatrixAccepted=True,inputHashes=pins,
  allMoveChoreographyAccepted=False,audioAccepted=False,CPUAccepted=False,allArenasAccepted=False,fullPortAccepted=False,
  scope='Full current 52 bounded physical move/contact/blocks/misses/recovery matrix. Fifty cases retain every native event and all endpoint screens; positive ball cases retain pre-command screens and prove intentional native boundary correction with full consecutive raster/shadows/erase. Not all victims, repeated, KO, CPU, audio, all arenas or whole game.')

if __name__=='__main__':
 source.need(not OUT.exists(),'Never overwrite evidence')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),cases=len(report.get('cases',[])),exactScreens=report.get('exactPriorActualFullScreensMatched')),indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
