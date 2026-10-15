"""Bounded P2 native task return/sprite reuse and exact scene-render boundary.
The old sprite address can legitimately be allocated by the next screen.
Neither a stale parent attachment nor an individual-delete observer flag is
a universal leak test. Do not accept palette lifetime, P1 child lifecycle,
every auxiliary effect, all finishers, arenas, victims, or the full port.
"""
import copy,json,re
from pathlib import Path
import numpy as np
import inspect_current_friendship_lifecycle_v2722 as life
ROOT=life.ROOT
need=life.need
OUT=ROOT/'audit_v2728_current_friendship_p2_lifecycle_boundary_checked'
def teardown(rows,control,result):
 task,object=result['task'],result['object'];cache=task+0x100
 phases=result['phases'];by_frame={row['frame']:row for row in phases}
 returned=life.select(rows,'RETURN_TASK')
 need(len(returned)==1,'One actual native auxiliary task return')
 row=returned[0];frame=life.number(row,'frame')
 need(life.pointer(row,'entry')==0xff80e5d0 and life.pointer(row,'pc')==0xff80e5e0 and life.pointer(row,'target')==life.pointer(row,'head')==life.pointer(row,'a2')==task,'Actual original masked-task sweep returns the allocated auxiliary task')
 stores=life.select(rows,'FREE_TASK_STORE')
 need(any(life.number(r,'frame')==frame and life.pointer(r,'pc')==0xff80e5d0 and life.pointer(r,'merged')==life.pointer(r,'target')==life.pointer(r,'a2')==task for r in stores),'Actual native task free-head store, not observer flag only')
 snapshot=life.select(rows,'RETURN_TASK_LISTS')
 need(len(snapshot)==1 and task not in life.nodes(snapshot[0],'tasks') and life.nodes(snapshot[0],'freeTasks')[0]==task,'Actual task removed from active list and inserted into native free chain')
 need(all(row['taskActive'] and not row['taskFree'] for row in phases if row['frame']<frame) and all(not row['taskActive'] and row['taskFree'] for row in phases if row['frame']>=frame),'Continuous native task allocation through return and terminal free membership')
 retire=control['actualPointerRetirement'];prior=by_frame[retire-1];after=by_frame[retire]
 need(frame<retire and prior['objectActive'] and prior['objectCache']==cache and 0xfe9d2610<=prior['objectPose']<=0xfe9d2790,'Actual original bubble remains a native sprite after its task return, until scene retirement')
 reuse=life.select(rows,'FREE_OBJECT_STORE')
 need(any(life.number(r,'frame')==retire and life.pointer(r,'pc')==0xff809150 and life.pointer(r,'before')==life.pointer(r,'a0')==object and life.pointer(r,'merged')==life.pointer(r,'a2')==object+life.POOL_STRIDE and life.pointer(r,'at')==0x01060130 for r in reuse),'Actual original sprite allocator consumes reclaimed bubble address at next-screen transition')
 need(all(row['objectCache']!=cache and not 0xfe9d2610<=row['objectPose']<=0xfe9d2790 for row in phases if row['frame']>=retire),'Every later use of reclaimed address belongs to new non-bubble allocation')
 need(after['physical']==0 and prior['physical']==result['parent'],'Actual owning fighter retires at the observed sprite reuse')
 return dict(actualAllocatedTask=task,actualAllocatedSprite=object,actualAuxiliaryCache=cache,taskReturnFrame=frame,spriteReuseFrame=retire,taskReturnRoute='original masked task sweep FF80E450 / free-head store FF80E5A0',spriteReclaimEvidence='original next-screen allocator consumes same fixed-pool address and resets old pose/cache',individualSpriteDeleteObserved=False,nativeTaskReturnAndSpriteReuseAccepted=True,continuousTerminalTaskFreeMembership=True,paletteLifetimeAccepted=False,fullChildLifecycleBothSlotsAccepted=False)
def verify():
 pins=life.native.scene.launch.source_pins()
 def pin(path,wanted=None):
  path=str(path);actual=life.native.scene.launch.sha(path)
  need(wanted is None or wanted==actual,'Immutable actual lifecycle/render dependency '+path)
  need(path not in pins or pins[path]==actual,'Consistent actual dependency '+path);pins[path]=actual
 old=ROOT/'tools/inspect_current_friendship_lifecycle_v2717.py';new=ROOT/'tools/inspect_current_friendship_lifecycle_v2722.py'
 pin(old);pin(new)
 # Keep source-derived allocator/reset facts explicit and independently pinned.
 guest,_,_=life.native.scene.current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for start,end in ((0xff8087b0,0xff808a20),(0xff83f0a0,0xff83f200),(0xff8090b0,0xff809270),(0xff80e450,0xff80e620)):
  a,b=(start-0xff800000)//8,(end-0xff800000)//8
  need(guest[a:b]==stock[a:b],'Original pool initialization/reset/allocator/task-return bytes unchanged')
 need(life.POOL_END==0x0105b950 and life.POOL_COUNT==358,'Original 358 fixed 210-bit sprite records, excluding RNG storage')
 cases={};outcomes=[];same_images=0
 for fighter in ('kano','sonya'):
  folder=ROOT/f'audit_v2718_current_{fighter}_friendship_lifecycle_p2'
  def report(relative):
   path=ROOT/relative;r=json.loads(path.read_text());need(r['passed'] and not r['fullPortAcceptance'],'Actual scoped report '+relative);pin(path)
   for file,wanted in r['inputHashes'].items():pin(file,wanted)
   return r
  diagnostic=report(f'audit_v2726_current_{fighter}_friendship_bounded_lifecycle_p2_diagnostic/report.json')
  render=report(f'audit_v2719_current_{fighter}_friendship_lifecycle_render_p2_diagnostic/report.json')
  shadow=report(f'audit_v2721_current_{fighter}_friendship_shadow_rows_p2_checked/report.json')
  need(diagnostic['side']==render['side']==shadow['side']==2 and diagnostic['control']==render['control'] and diagnostic['originalFailedDiagnosticRetained'] and diagnostic['originalFixedStrideSpritePoolBounded'] and not diagnostic['unboundedSpriteFreeListIntegrityAccepted'],'Actual P2 diagnostic with retained unsupported unbounded traversal')
  need(render['actualConsecutiveScanouts']==1600 and render['actualBoundPixels']==162560000 and render['fullDrawingAndContinuousErasureAccepted'] and not render['gameChanged'],'Complete source-exact actual native P2 rendering and continuous erasure')
  need(shadow['originalSourcePoseCacheAndAllIntermediateRowsAccepted'] and shadow['rejectedSpecificCounterexamples']==6 and shadow['finalUnmodifiedControlPassed'],'Every original intermediate shadow row and six actual corruptions checked')
  black=0
  for r in render['diagnostics']['drawing']['records']:
   if r['shadow_pixels']:
    palette=np.fromfile(folder/f"display_palette_{r['frame']}.bin",dtype='<u4')
    need(palette[15]==0 and r['shadow_mismatches']==0,'Every rendered P2 native floor-shadow pen is source-exact black');black+=1
  need(black>=10,'Non-empty actual black floor-shadow raster coverage')
  prior=ROOT/f'audit_v2691_current_{fighter}_friendship_shadow_p2/snap'
  images=list(prior.glob('*.png'));need(len(images)>300,'Entire original P2 screenshot control retained')
  for image in images:
   wanted=life.native.scene.launch.sha(image);pin(image,wanted);pin(folder/'snap'/image.name,wanted);same_images+=1
  rows=life.parse(folder/'run.log');control=diagnostic['control'];positive=life.check(rows,control,fighter,2)
  need(positive['continuousLifecycleFields']==diagnostic['continuousLifecycleFields'],'Actual bounded native list check fully repeated')
  # These corrupt actual recorded pool membership, not a hand-written fixture.
  first_index=next(i for i,(tag,r) in enumerate(rows) if tag=='STATE')
  first=rows[first_index][1];values=life.nodes(first,'freeObjects')
  mutations=[('wrong_free_pool_stride','freeObjects',','.join(f'{v:08X}' for v in [values[0]+1]+values[1:]),'Actual sprite free membership'),('wrong_original_boot_tail','freeObjectsBad','00000000','Original boot free-pool terminator'),('missing_pool_tail','freeObjects',','.join(f'{v:08X}' for v in values[:-1]),'Every recorded free-pool prefix'),('duplicated_pool_record','freeObjects',','.join(f'{v:08X}' for v in [values[0]]+values[:-1]),'Every recorded free-pool prefix')]
  for name,key,value,expected in mutations:
   changed=list(rows);r=dict(first);r[key]=value;changed[first_index]=(rows[first_index][0],r)
   need(changed!=rows,'Non-vacuous actual pool counterexample')
   try:life.check(changed,control,fighter,2)
   except ValueError as error:
    need(expected in str(error),'Specific original pool invariant '+name+': '+str(error));outcomes.append(dict(fighter=fighter,name=name,rejectedBy=str(error)))
   else:raise ValueError('Corrupt actual sprite pool accepted '+name)
  publications=after=0;last=None
  with (folder/'run.log').open(encoding='utf-8-sig') as stream:
   for line in stream:
    if 'MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ' not in line:continue
    r=dict(re.findall(r'(\w+)=([^\s]+)',line));frame=int(r['frame']);pose=int(r['pose'],16)
    after+=frame>control['actualPointerRetirement']
    if 0xfe9d2610<=pose<=0xfe9d2790:
     need(frame<control['actualPointerRetirement'],'No old bubble publication after actual sprite reuse/physical retirement');publications+=1;last=frame
  need(after>1000 and (fighter!='kano' or publications>100),'Non-empty whole native renderer after retirement and actual bubble coverage')
  details={}
  if fighter=='kano':
   details=teardown(rows,control,positive)
   # Actual return/reuse events and continuous pose/cache state must matter.
   candidates=[('missing_native_task_return','RETURN_TASK','drop',None,'One actual native auxiliary task return'),('wrong_native_task_return_route','RETURN_TASK','entry','FF80E250','Actual original masked-task sweep'),('wrong_native_sprite_reuse_route','FREE_OBJECT_STORE','pc','FF8097D0','Actual original sprite allocator'),('old_bubble_cache_survives_reuse','STATE','objectCache',f'{positive["task"]+0x100:08X}','Every later use of reclaimed address')]
   for name,tag,key,value,expected in candidates:
    changed=[]
    for kind,r in rows:
     match=kind==tag and (tag!='FREE_OBJECT_STORE' or life.number(r,'frame')==control['actualPointerRetirement']) and (tag!='STATE' or life.number(r,'frame')==control['actualPointerRetirement'])
     if match and key=='drop':continue
     if match:r=dict(r);r[key]=value
     changed.append((kind,r))
    need(changed!=rows,'Non-vacuous actual native lifecycle counterexample')
    try:teardown(changed,control,life.check(changed,control,fighter,2))
    except ValueError as error:
     need(expected in str(error),'Specific actual lifecycle invariant '+name+': '+str(error));outcomes.append(dict(fighter=fighter,name=name,rejectedBy=str(error)))
    else:raise ValueError('Corrupt actual child lifecycle accepted '+name)
   need(teardown(rows,control,life.check(rows,control,fighter,2))==details,'Final unmodified native child-return/reuse control')
  else:details=dict(nativeTaskReturnAndSpriteReuseAccepted=False,scope='Global active lists and source-bounded free sprite pool only; observer targets Kano bubble constructor')
  cases[fighter]=dict(renderReport=str(ROOT/f'audit_v2719_current_{fighter}_friendship_lifecycle_render_p2_diagnostic/report.json'),shadowRowsReport=str(ROOT/f'audit_v2721_current_{fighter}_friendship_shadow_rows_p2_checked/report.json'),lifecycleDiagnostic=str(ROOT/f'audit_v2726_current_{fighter}_friendship_bounded_lifecycle_p2_diagnostic/report.json'),consecutiveScanouts=1600,sourceExactPixels=162560000,sourceExactDrawingPasses=render['diagnostics']['drawing']['frames'],heldScanouts=render['heldOriginalScanouts'],sourceExactBlackShadowFrames=black,intermediateShadowComponents=shadow['components'],intermediateShadowCopies=shadow['checkedCopies'],actualBubblePublications=publications,lastActualBubblePublication=last,allQueuePublicationsAfterRetirement=after,noBubblePublicationAfterPhysicalRetirement=True,**details)
 pin(Path(__file__).resolve());life.native.scene.launch.module_pins(pins)
 return dict(passed=True,cases=cases,entirePriorP2ScreenshotsByteIdentical=same_images,completeActualP2RenderAndContinuousErasureAccepted=True,originalP2IntermediateShadowRowsAndBlackRenderedPensAccepted=True,kanoP2NativeAuxiliaryTaskReturnAndSpriteReuseAccepted=True,rejectedActualLifecycleCounterexamples=len(outcomes),outcomes=outcomes,executedSourcesCapturesAndFailuresRetained=True,gameChanged=False,fullChildLifecycleBothSlotsAccepted=False,completeSceneRasterShadowAudioAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Immutable actual P2 render/lifecycle boundary')
 r=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('inputHashes','outcomes')},indent=2),flush=True)
