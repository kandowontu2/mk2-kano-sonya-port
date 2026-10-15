"""Fresh complete bounded 52-case human matrix after source metadata rebuild."""
import json,re
from PIL import Image
import verify_ring_native_lookup_v1342 as build
import verify_human_special_matrix as positive
import verify_human_special_negative_v6 as negative
ROOT=build.ROOT;OUT=ROOT/'audit_v1389_current_human_matrix_checked'

def verify():
 pins={};cases=[];blood_proofs={};exact_images=0;blood_images=0
 def pin(path,wanted=None):
  actual=build.digest(path);assert wanted is None or actual==wanted,'Changed evidence '+str(path);pins[str(path)]=actual
 metadata_path=build.OUT/'report.json';metadata=json.loads(metadata_path.read_text());pin(metadata_path)
 assert metadata['passed'] and metadata['candidate']==build.CANDIDATE and metadata['nativeROMAuditAccepted']
 for file,wanted in metadata['inputHashes'].items():pin(file,wanted)
 build_path=ROOT/build.CANDIDATE/'build-info.json';compiled=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
 build.reconstruct()
 for side in(1,2):
  path=ROOT/f'audit_v1388_blade_native_gore_p{side}_checked/report.json'
  data=json.loads(path.read_text());pin(path)
  assert data['passed']and data['candidate']==build.CANDIDATE and data['side']==side
  assert data['allDifferencesAreOriginalNativeBlood']and data['changedPixels']>0
  for file,wanted in data['inputHashes'].items():pin(file,wanted)
  blood_proofs[side]=data
 fixtures=[(m,s,None,False) for m in positive.SPECS for s in (1,2)]
 fixtures += [('square',s,None,True) for s in (1,2)]
 fixtures += [(m,s,k,False) for m in positive.SPECS for s in (1,2) for k in ('block','miss')]
 fixtures += [('leg',s,'duck_block',False) for s in (1,2)]
 for move,side,scenario,air in fixtures:
  suffix=move+('_air' if air else '_'+scenario if scenario else '')
  folder=ROOT/f'audit_v1365_human_{suffix}_p{side}';baseline=ROOT/f'audit_v1252_human_{suffix}_p{side}'
  launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  assert launch['exit_code']==0 and launch['candidate']==build.CANDIDATE and launch['executable_sha256']==compiled['executable_sha256'] and launch['payload_sha256']==compiled['payload_sha256']
  assert launch['move']==move and launch['side']==side and launch['victim']=='sub_zero' and launch['cheats_enabled'] is False and launch['assistance']=='none'
  assert launch['scenario']==scenario if scenario else launch['air']==air
  for file,wanted in launch['input_hashes'].items():pin(file,wanted)
  filename='mk2ks_human_special_negative_v9.lua' if scenario else 'mk2ks_human_special_matrix_v3.lua'
  source=(folder/'input_sources'/filename).read_text()
  assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',source),'Read-only physical input observer'
  log=(folder/'run.log').read_text(encoding='utf-8-sig');old_log=(baseline/'run.log').read_text(encoding='utf-8-sig');pin(baseline/'run.log')
  assert not re.search('WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation',log,re.I)
  # Palette-cache banks are native allocations, not fixed actor IDs. Preserve
  # all actual identity, pose, movement, health, input and collision events.
  events=lambda text:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_PALETTE_ALLOCATION',line)for line in text.splitlines()if line.startswith('MK2_HSPECIAL_')]
  assert events(log)==events(old_log),'Every actual human input/native/collision/state event must remain identical'
  result=negative.verify_log(log,move,side,scenario) if scenario else positive.verify_log(log,move,side,air)
  if move=='ball' and scenario:
   negative.verify_repel(log,side)
   if scenario=='block':result.update(negative.verify_rebound(log,side,True))
  result['case']=folder.name;cases.append(result)
  for filename in ('special_before.png','special_recovered.png','special_final.png'):
   path=folder/'snap'/filename;old=baseline/'snap'/filename
   assert Image.open(path).size==(400,254)
   if path.read_bytes()==old.read_bytes():exact_images+=1
   else:
    assert move=='blade'and scenario is None and not air and filename=='special_recovered.png','Unexpected visual regression outside proven original blood'
    proof=blood_proofs[side]
    assert proof['inputHashes'][str(path)]==build.digest(path)
    assert proof['inputHashes'][str(old)]==build.digest(old)
    blood_images+=1
   pin(old)
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
 for filename in ('tools/verify_current_human_matrix_v1389.py','tools/verify_human_special_matrix.py','tools/verify_human_special_negative_v6.py',
  'tools/run_current_human_special_v820.ps1','tools/run_current_human_negative_v1240.ps1'):
  pin(ROOT/filename)
 assert len(cases)==52
 assert exact_images==154 and blood_images==2
 return dict(passed=True,candidate=build.CANDIDATE,cases=cases,positiveCases=18,negativeCases=34,
  pairedFields=sum(r['fields'] for r in cases),exactPriorActualImagesMatched=exact_images,sourceProvenNativeBloodVariationImages=blood_images,everyPriorHumanEventMatched=True,
  current52CaseHumanStateMatrixAccepted=True,currentKnifeRingPhysicalRegressionAccepted=True,noROMChecksumWarnings=True,
  inputHashes=pins,allMoveArtAccepted=False,allVictimsAccepted=False,CPUAccepted=False,audioAccepted=False,allArenasAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
 assert not OUT.exists()
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Fresh52 current human cases passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
