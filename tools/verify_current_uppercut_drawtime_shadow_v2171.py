"""All four genuine uppercuts: own shadow completeness against draw-time pose.
The native queued-body pose is not substituted for the direct shadow's actual
cache/pose. Every shadow component must match its actual read-only observed ROM
composite. Full scene, continuous erase, native row cadence and physical gameplay
are independently accepted by2170. No universal move/arena/art/audio acceptance.
"""
import copy,json
from collections import defaultdict
from pathlib import Path
import verify_current_human_uppercut_full_render_v2168 as model
import verify_current_interrupt_v1870 as launch
ROOT=model.ROOT;OUT=ROOT/'audit_v2172_current_uppercut_drawtime_shadow_coverage'
def need(ok,message):
 if not ok:raise ValueError(message)
def coverage(groups,side,identity,guest,payload):
 queues=[q for q in groups['FLOOR_QUEUE']if q['slot']==side]
 need(queues,'Actual own physical publication inventory')
 physical=queues[0];frames={q['frame']for q in queues}
 byframe=defaultdict(list)
 for r in groups['SHADOW_COMPONENT']:
  need(r['slot']==side and r['id']==identity,'Only declared own imported character supplies these shadows')
  byframe[r['frame']].append(r)
 need(set(byframe)==frames,'Every own body draw field has its own direct shadow draw, not an opponent substitute')
 components=copies=0;pose_set=set();different=[]
 for frame,rows in sorted(byframe.items()):
  first=rows[0];pose_set.add(first['pose'])
  for r in rows:
   need(r['actor']==r['owner']==physical['actor']and r['main']==physical['main'],'Every own shadow copy has the genuine physical actor/Main owner')
   need(all(r[k]==first[k]for k in ('pose','body','facing','cache','x','y','floor','stageY','cameraY','displayY')),'Shadow composite pose and native physical context stable during this original direct draw')
   need(r['floor']==r['stageY']-{17:134,18:135}[identity],'Every own shadow retains its actual character-owned native floor')
  expected=model.group(first,payload,guest);parts=defaultdict(list)
  for r in rows:parts[r['component']].append(r)
  need(set(parts)==set(range(len(expected))),'Every part of the actual direct-shadow pose is projected exactly, including transition frames')
  for number,e in enumerate(expected):
   for r in parts[number]:
    need(r['row']==r['cache']+112*number,'Every own shadow uses the actual current cache component')
    need((r['first_source'],r['width'],r['height'],r['xoff'],r['yoff'],r['command'])==
         (e['source'],e['width'],e['height'],e['dx'],e['dy'],e['command']),'Every own shadow source/shape/offset/command equals its actual draw-time ROM pose')
   components+=1;copies+=len(parts[number])
  queued={q['pose']for q in queues if q['frame']==frame}
  if queued!={first['pose']}:different.append(dict(frame=frame,queuedBodyPoses=sorted(queued),actualDirectShadowPose=first['pose']))
 return dict(ownShadowDrawFields=len(frames),ownShadowComponents=components,ownShadowCopies=copies,
  actualDirectShadowPoses=len(pose_set),queuedBodyAndDirectShadowPoseDifferences=different,
  everyActualOwnShadowPoseComponentProjected=True)
def verify():
 pins={};cases={};guest,_,payload=model.current.expected()
 for case in ('kano_p1','kano_p2','sonya_p1','sonya_p2'):
  side=int(case[-1]);identity=17 if case.startswith('kano')else 18
  folder=ROOT/f'audit_v2169_current_uppercut_{case}_shadow_pose'
  path=ROOT/f'audit_v2170_current_uppercut_{case}_shadow_pose_checked/report.json'
  positive=json.loads(path.read_text())
  need(positive['passed']and positive['interPassEraseAcceptance'],'Full independent source-exact current scene and continuous clear')
  for file,wanted in positive['inputHashes'].items():
   need(launch.sha(file)==wanted,'Changed independent render input '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);groups=model.raster.data(folder)[0]
  actual=coverage(groups,side,identity,guest,payload);outcomes=[]
  for kind,message in (
   ('missing_field','Every own body draw field'),
   ('missing_component','Every part of the actual direct-shadow pose'),
   ('wrong_owner','genuine physical actor/Main owner'),
   ('wrong_cache','actual current cache component'),
   ('wrong_source','actual draw-time ROM pose'),
   ('shifted_floor','character-owned native floor')):
   changed=copy.deepcopy(groups);row=changed['SHADOW_COMPONENT'][0]
   if kind=='missing_field':changed['SHADOW_COMPONENT']=[r for r in changed['SHADOW_COMPONENT']if r['frame']!=row['frame']]
   elif kind=='missing_component':
    key=(row['frame'],row['component']);changed['SHADOW_COMPONENT']=[r for r in changed['SHADOW_COMPONENT']if (r['frame'],r['component'])!=key]
   elif kind=='wrong_owner':row['owner']+=16
   elif kind=='wrong_cache':row['row']+=112
   elif kind=='wrong_source':row['first_source']+=16
   else:
    for r in changed['SHADOW_COMPONENT']:
     if r['frame']==row['frame']:r['floor']+=1
   try:coverage(changed,side,identity,guest,payload)
   except ValueError as error:
    need(message in str(error),'Specific intended shadow invariant failed, not incidental exception '+str(error));outcomes.append(dict(name=kind,rejectedBy=str(error)))
   else:raise ValueError('Malformed own shadow accepted '+kind)
  need(coverage(groups,side,identity,guest,payload)==actual,'Unchanged actual draw-time shadow control passes')
  cases[case]=dict(passed=True,side=side,identity=identity,fullSceneReport=str(path),**actual,
   rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes)
  print(case+' all actual draw-time ROM shadow components, six specific corruptions rejected',flush=True)
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,totalOwnShadowCopies=sum(c['ownShadowCopies']for c in cases.values()),
  rejectedSpecificCounterexamples=sum(c['rejectedSpecificCounterexamples']for c in cases.values()),inputHashes=pins,
  supersededInvalidSameFieldQueueShadowAssumption=str(ROOT/'audit_v2164_current_uppercut_owned_shadow_coverage/report.json'),
  allMoveArenaGroundShadowAccepted=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Immutable draw-time shadow coverage')
 try:report=verify()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
