"""Entire original shatter matrix, current cold build, actual native panels.

Retain every original state/opcode/command/park/lifecycle and52 fault checks.
Add original inter-round refill, continuous observed-state corruptions and
sixteen actual RGB panels. Compare the whole protected older native trace and
all four RGB events, not selected passing rows. This is sparse raster review,
not continuous native scene replay, whole finisher audio or full-port proof.
"""
import copy,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
import current_payload_metadata_context_v5229 as current
import verify_native_subzero_legs_matrix_v5004 as original
import qualify_current_kitana_scene_v6116 as refill_source
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6167_current_subzero_shatter_checked'

def panels(sheet,scenes):
 a=np.asarray(Image.open(sheet).convert('RGB'))
 need(a.shape==(556,800,3),'Four whole400x254 native panels, no crop/reposition')
 for index,scene in enumerate(scenes):
  x,y=index%2*400,index//2*278
  need(hashlib.sha256(a[y+24:y+278,x:x+400].tobytes()).hexdigest().upper()==scene['actualRGBSHA256'],
       'Every complete review panel equals actual native displayed RGB')
 return a

def check_panel_array(a,scenes):
 for index,scene in enumerate(scenes):
  x,y=index%2*400,index//2*278
  need(hashlib.sha256(a[y+24:y+278,x:x+400].tobytes()).hexdigest().upper()==scene['actualRGBSHA256'],
       'Altered or swapped native RGB panel rejected')

def run():
 need(not OUT.exists(),'Fresh complete current native shatter matrix')
 source=Path(original.__file__).read_text()
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'One exact whole original matrix current adaptation')
  source=source.replace(before,after,1)
 replace('import native_subzero_legs_context_v4993 as native','import current_payload_metadata_context_v5229 as native')
 replace("OUT=ROOT/'audit_v5005_native_subzero_legs_matrix_checked'","OUT=ROOT/'audit_v6167_current_subzero_shatter_checked'")
 replace('audit_v5002_subzero_','audit_v6164_current_subzero_')
 replace('audit_v5003_subzero_','audit_v6165_current_subzero_')
 replace('cases.append(verify(guest,rows,log,identity,side,scenes))',
         'cases.append(extend(guest,rows,log,identity,side,scenes,folder,report,pins))')
 replace('Path(__file__),Path(native.__file__),Path(parser.__file__)',
         'Path(__file__),Path(original.__file__),Path(refill_source.__file__),Path(native.__file__),Path(parser.__file__)')
 extra_faults=[];pixel_faults=[]
 legacy_path=ROOT/'audit_v5005_native_subzero_legs_matrix_checked/report.json'
 legacy=json.loads(legacy_path.read_text())
 need(legacy['passed']and legacy['guestSHA256']==current.GUEST_SHA and len(legacy['cases'])==4,
      'Protected semantic-leg native baseline, exactly same initialized whole guest')
 need(all(sha(p)==h for p,h in legacy['inputHashes'].items()),'Every actually executed protected baseline input unchanged')
 def extend(guest,rows,log,identity,side,scenes,folder,report,pins):
  positive=original.verify(guest,rows,log,identity,side,scenes)
  fighter='kano'if identity==17 else'sonya'
  terminal=json.loads((folder/'native_terminal.json').read_text());process=json.loads((folder/'process.json').read_text())
  need(terminal==report['actualWindowsTerminal']and terminal['nativeExit']==report['nativeExit']==0 and
       terminal['pid']==process['pid']==terminal['actualWindowsIdentity']['ProcessId']and
       process['actualWindowsIdentity']==terminal['actualWindowsIdentity']and terminal['actualWindowsIdentity']['CreationDate']and
       Path(terminal['actualWindowsIdentity']['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
       str(ROOT/'mk2ks_native_subzero_legs_nextmatch_v5000.lua')in terminal['actualWindowsIdentity']['CommandLine'],
       'Actual current native Windows creation/full-command identity and terminal')
  health=[dict(r,tag=r['tag'].removeprefix('MK2_STOCK_HEAD_V921_'))for r in rows if r['tag'].startswith('MK2_STOCK_HEAD_V921_')]
  positive['nativeInterRoundRefill']=refill_source.refill(health,side,guest)
  for label,tag,key,value in [('proxy_field_roster','FIELD','roster','1'),('wrong_field_owner','FIELD','owner','00000000'),
                            ('fake_frozen_health','FIELD','hp','161'),('wrong_field_state','FIELD','state','3')]:
   changed=copy.deepcopy(rows);target=next(r for r in changed if r['tag']=='MK2_EARNED_SUBZERO_'+tag);need(target[key]!=value,'Non-vacuous actual native field corruption');target[key]=value
   try:original.verify(guest,changed,log,identity,side,scenes)
   except ValueError as e:extra_faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(e)))
   else:raise ValueError('Accepted actual victim field corruption')
  first=positive['nativeFreezeFrame']
  changed=[r for r in rows if not(r['tag']=='MK2_EARNED_SUBZERO_FIELD'and int(r['frame'])==first+80)]
  need(len(changed)<len(rows),'Remove actual continuous physical field')
  try:original.verify(guest,changed,log,identity,side,scenes)
  except ValueError as e:extra_faults.append(dict(case=f'{fighter}_p{side}',fault='missing_actual_victim_field',rejectedBy=str(e)))
  else:raise ValueError('Accepted missing physical field')
  at=positive['nativeInterRoundRefill']['startFrame']
  for label,age,value in [('wrong_native_refill_sentinel',0,'65534'),('wrong_native_refill_step',1,'7')]:
   changed=copy.deepcopy(health)
   target=next(r for r in changed if r['tag']=='HEALTH'and int(r['frame'])==at+age and r['after']==('65535'if age==0 else'6'));target['after']=value
   try:refill_source.refill(changed,side,guest)
   except ValueError as e:extra_faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(e)))
   else:raise ValueError('Accepted native refill corruption')
  need(original.verify(guest,rows,log,identity,side,scenes)=={k:v for k,v in positive.items()if k!='nativeInterRoundRefill'},'Complete positive native grammar restored')
  old=ROOT/f'audit_v5002_subzero_{fighter}_p{side}_lifecycle'
  old_log=(old/'run.log').read_text();old_rows=original.parser.parse(old_log)
  old_scenes=json.loads((old/'rgb_memory_proofs.json').read_text())
  old_positive=original.verify(guest,old_rows,old_log,identity,side,old_scenes)
  need(rows==old_rows,'Every actual native state/input/branch/effect/lifecycle record equals protected baseline')
  need([{k:v for k,v in r.items()if k!='actualRGBSHA256'}for r in scenes]==old_scenes,
       'All four complete actual RGB events exactly equal protected native reference, including subsequent match')
  need(old_positive=={k:v for k,v in positive.items()if k!='nativeInterRoundRefill'and k!='actualRGBFields'}|dict(actualRGBFields=old_scenes),
       'Whole original baseline/current proof, no omitted checks')
  atlas=panels(report['nativeReview'],scenes)
  changed=atlas.copy();changed[24,0,0]^=1
  try:check_panel_array(changed,scenes)
  except ValueError as e:pixel_faults.append(dict(case=f'{fighter}_p{side}',fault='one_actual_native_pixel_changed',rejectedBy=str(e)))
  else:raise ValueError('Accepted native panel pixel mutation')
  changed=atlas.copy();changed[24:278,0:400]=atlas[24:278,400:800]
  try:check_panel_array(changed,scenes)
  except ValueError as e:pixel_faults.append(dict(case=f'{fighter}_p{side}',fault='wrong_actual_native_phase_substituted',rejectedBy=str(e)))
  else:raise ValueError('Accepted wrong native panel phase')
  need(refill_source.refill(health,side,guest)==positive['nativeInterRoundRefill'],'Complete original refill positive restored')
  positive.update(fighter=fighter,actualWindowsTerminal=terminal,nativeReview=report['nativeReview'],
                  allOriginalNativeRowsAndFourRGBEventsEqualProtectedBaseline=True,actualNativeReviewPanels=4,
                  continuousNativeSceneReplayAccepted=False,nativeFloorShadowCoverageAccepted=False)
  pins[str(legacy_path)]=sha(legacy_path);pins.update(legacy['inputHashes'])
  for p in(old/'run.log',old/'rgb_memory_proofs.json'):pins[str(p.resolve())]=sha(p)
  return positive
 scope=dict(original.__dict__,__name__='current_native_shatter_matrix',__file__=__file__,original=original,refill_source=refill_source,extend=extend)
 exec(compile(source,__file__+'::whole_original_shatter_matrix','exec'),scope)
 scope['main']()
 report=json.loads((OUT/'report.json').read_text())
 need(len(extra_faults)==28 and len(pixel_faults)==8 and len(report['actualFaultsRejected'])==52,'All original52 plus28state/refill plus8native panel faults')
 report.update(actualAdditionalStateRefillFaultsRejected=extra_faults,actualNativePixelFaultsRejected=pixel_faults,
               actualSemanticFaultsRejected=80,actualNativePanelFaultsRejected=8,actualNativeReviewPanels=16,
               actualEventRGBPixels=16*400*254,actualConsecutiveVictimFields=sum(c['actualConsecutiveVictimFields']for c in report['cases']),
               actualNativeRefillStores=324,completeOriginalStateMatrixRetained=True,allNativeReviewPanelsActualPixelBound=True,
               continuousNativeSceneReplayAccepted=False,nativeFloorShadowCoverageAccepted=False,
               normalHealthFreezeAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
               originalScopeRemaining='Full finisher scene/FIFO/ground/shadow/audio, other cinematic consumers, broader arenas/CPU/overlap and integrated release')
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All executed complete native evidence unchanged at final report')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('passed','actualConsecutiveVictimFields','actualNativeRefillStores','actualSemanticFaultsRejected','actualNativePanelFaultsRejected','actualEventRGBPixels','fullPortAcceptance')},indent=2),flush=True)

if __name__=='__main__':run()
