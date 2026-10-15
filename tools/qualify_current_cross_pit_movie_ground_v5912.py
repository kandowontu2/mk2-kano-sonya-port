"""Whole retained current Pit movie and grounding; shadow policy remains open.

Preserve actual5907wrong-floor and5910zero-shadow failures. Full native movie,
visible six poses, actual Main+140 ancestry, source-native phase floors and
all31movie/sixfloor corruptions are independently qualified. Zero shadow draws
are inventory, not acceptance of native shadow suppression or full Pit scope.
"""
import argparse,collections,inspect,json,subprocess,traceback
from pathlib import Path
from unittest.mock import patch
import verify_current_cross_pit_retained_scene_v5909 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
contract=previous.contract

def partial_contract(scene,text,guest,payload,fighter,side,reference,ids):
 # Execute the entire unrelaxed current full-scene successor. Its open
 # shadow policy must fail explicitly, not be removed to obtain a full pass.
 try:contract.scene_contract(scene,text,guest,payload,fighter,side,reference,ids)
 except ValueError as error:
  need(str(error)=='All actual own compressed physical floor-shadow rows and identities retained',
       'Only the actual still-open native shadow policy is allowed as partial-scope evidence')
  unresolved=str(error)
 else:raise ValueError('This bounded qualifier requires explicit unresolved shadow policy')
 native=contract.native_gate(scene,text,guest,payload,fighter,side,ids)
 floor=contract.phase_ground(scene,guest,side)
 floor_faults=contract.ground_faults(scene,guest,side)
 movie_faults=contract.movie_faults(scene,text,guest,payload,fighter,side,ids,native)
 earned_faults=contract.native.actual_faults(text,fighter,side,guest)
 need(len(movie_faults)==31 and len(floor_faults)==6 and len(earned_faults)==12,
      'Entire original actual31movie, six source-native floor and12physical earned faults')
 scene_groups=scene.groups;queue={(q['frame'],q['cursor']):q for q in scene_groups['FLOOR_QUEUE']}
 draws=collections.defaultdict(set);visible=set()
 for d in scene_groups['FLOOR_QUEUE_DISPATCH']:
  q=queue[d['queue_frame'],d['cursor']]
  if q['slot']==4:draws[d['frame']].add(q['pose'])
 for r in scene.records:
  if r['body']['4']['pixels']>100:visible.update(draws[r['frame']-1])
 need(visible==set(native['actualMoviePoses']) and len(visible)==6,
      'Every actual own falling/impact pose visibly scanned out in retained full live RGB')
 shadow=contract.previous.continuous.shadow
 with patch.object(shadow,'data',return_value=(scene_groups,scene.buffers,None,None,scene.owners)):
  inventory=shadow.inspect(None)
 need(inventory['components']==inventory['checked_copies']==0 and not inventory['identities'] and
      not inventory['failures'] and not inventory['oversized_rows'] and
      not scene_groups['SHADOW_COMPONENT'] and sum(r['shadowPixels']for r in scene.records)==0 and
      not any(0x10000000<=d['source']<0x1a000000 and d['command']&15==8 for d in scene_groups['FLOOR_DMA']),
      'Actual captured zero shadow draw inventory, not a claim about native suppression correctness')
 native.update(actualNativePhaseGround=floor,actualNativePhaseGroundFaultsRejected=floor_faults,
               actualMovieFaultsRejected=movie_faults,actualEarnedFaultsRejected=earned_faults,
               visiblyRenderedMoviePoses=sorted(visible),actualShadowInventory=inventory,
               unresolvedFullSceneValidation=unresolved,wholeNativePitShadowPolicyAccepted=False,
               completeNativePitSceneAccepted=False)
 return native

source=inspect.getsource(previous.run)
before='proof=contract.scene_contract(scene,text,guest,payload,fighter,side,Path(ref[\'capture\']),ids)'
need(source.count(before)==1,'Whole actual scene proof call preserved with explicit partial native qualification')
source=source.replace(before,"proof=partial_contract(scene,text,guest,payload,fighter,side,Path(ref['capture']),ids)",1)
before='actualCurrentCrossPitCompleteRetainedNativeSceneAccepted=True,'
need(source.count(before)==1,'Whole broader scene acceptance must not be granted')
source=source.replace(before,'actualCurrentQualifiedNativePitMovieAndGroundingAccepted=True,wholeNativePitShadowPolicyAccepted=False,completeNativePitSceneAccepted=False,',1)
scope=dict(vars(previous),__file__=__file__,__doc__=__doc__,partial_contract=partial_contract)
exec(compile(source,__file__+'::whole5909_actual_movie_ground_partial_scope','exec'),scope)
run=scope['run'];run.source=source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 OUT=ROOT/f'audit_v5913_current_cross_pit_{args.fighter}_p{args.side}_movie_ground_checked'
 need(not OUT.exists(),'Immutable current native movie/ground progress, not full-scene success')
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Bounded qualified native text compressed')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','nativeScene')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
