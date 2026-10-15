"""Actual current auxiliary-task/sprite lifetime diagnostic; not whole-port proof.
Bind original native allocation and full active/free-list observations. Record
the actual reclamation route without assuming individual-delete versus bulk
reset, or treating disappearance/observer flags as proof of memory teardown.
"""
import argparse,json,re,traceback
from pathlib import Path
from collections import defaultdict
import verify_current_friendship_shadow_inventory_v2696 as native
ROOT=native.ROOT
need=native.need
LISTS=('tasks','freeTasks','objects','layer1','layer2','freeObjects')
def number(row,key):return int(row[key])
def pointer(row,key):return int(row[key],16)
def nodes(row,key):return [] if row[key]=='-' else [int(value,16) for value in row[key].split(',')]
def parse(path):
 rows=[]
 with path.open(encoding='utf-8-sig') as stream:
  for line in stream:
   match=re.match(r'MK2_CHILD_LIFE_(\w+) (.*)',line)
   if match:rows.append((match[1],dict(re.findall(r'(\w+)=([^\s]+)',match[2]))))
 return rows
def select(rows,tag):return [row for kind,row in rows if kind==tag]
def check(rows,control,fighter,side):
 action=select(rows,'ACTION');final=select(rows,'RESULT');states=select(rows,'STATE')
 need(len(action)==len(final)==1 and number(action[0],'frame')==control['action']==number(final[0],'action') and number(action[0],'id')==control['actualTrueID'],'Actual true owned native Friendship lifecycle context')
 need(all(row['writes']=='0' and row['assistance']=='none' and row['fighter']==fighter and number(row,'side')==side for _,row in rows),'Every actual lifecycle record unassisted and correctly slotted')
 need(not select(rows,'INVALID'),'No invalid actual native task/sprite pointer')
 need([number(row,'frame') for row in states]==list(range(control['action'],control['window']+1601)),'Every actual lifecycle field through native transition')
 for tag,row in rows:
  if tag.endswith('_LISTS') or tag=='STATE':
   groups={key:nodes(row,key) for key in LISTS}
   for key,values in groups.items():
    need(number(row,key+'Valid')==1 and pointer(row,key+'Bad')==0 and number(row,key+'Count')==len(values)==len(set(values)) and all(0x01000000<=value<0x01100000 for value in values),'Complete original active/free linked list without missing/cyclic/out-of-range nodes')
   need(not set(groups['tasks'])&set(groups['freeTasks']),'Native task active/free lists disjoint')
   active_objects=set(groups['objects'])|set(groups['layer1'])|set(groups['layer2'])
   need(sum(len(groups[key]) for key in ('objects','layer1','layer2'))==len(active_objects) and not active_objects&set(groups['freeObjects']),'Native sprite render/free lists disjoint')
 pre=select(rows,'ALLOC_PRE');post=select(rows,'ALLOC_POST');constructed=select(rows,'CONSTRUCT')
 if fighter!='kano':
  need(not pre and not post and not constructed and pointer(final[0],'task')==pointer(final[0],'object')==0,'No tracked Kano bubble allocation in non-Kano fixture; observer does not certify every other auxiliary effect')
  return dict(action=control['action'],continuousLifecycleFields=len(states),trackedKanoBubbleAllocations=0,childObjectAndTaskTeardownAccepted=False,lifecycleAcceptanceScope='Global native list integrity only; the constructor observer intentionally targets Kano bubble allocation')
 need(len(pre)==len(post)==len(constructed)==1,'One actual native Kano bubble task and sprite allocation')
 task,object=pointer(post[0],'task'),pointer(constructed[0],'object')
 parent,parent_main=pointer(pre[0],'parent'),pointer(pre[0],'parentMain')
 need(task==pointer(pre[0],'freeHead')==pointer(constructed[0],'task')==pointer(final[0],'task') and task!=parent_main and object!=parent and object==pointer(final[0],'object'),'Original allocation consumes actual free task, not physical parent/process proxy')
 need(number(post[0],'taskID')==0x109 and pointer(post[0],'resume')==0xff83b070 and pointer(post[0],'owner')==parent and pointer(constructed[0],'cache')==task+0x100 and 0xfe9d2610<=pointer(constructed[0],'pose')<=0xfe9d2790,'Original group-task ID/resume/owner and independent cache allocation')
 before=select(rows,'ALLOC_PRE_LISTS');after=select(rows,'ALLOC_POST_LISTS');done=select(rows,'CONSTRUCT_LISTS')
 need(len(before)==len(after)==len(done)==1,'Actual native constructor boundary snapshots')
 bt,at=nodes(before[0],'tasks'),nodes(after[0],'tasks');position=bt.index(parent_main)+1
 need(at==bt[:position]+[task]+bt[position:] and nodes(after[0],'freeTasks')==nodes(before[0],'freeTasks')[1:],'Exact original task insertion and free-list pop')
 need(nodes(before[0],'freeObjects')[0]==object and nodes(done[0],'freeObjects')==nodes(before[0],'freeObjects')[1:],'Exact original independent sprite free-list pop')
 attached=select(rows,'ATTACH_STORE')
 need(any(pointer(row,'merged')==object and pointer(row,'a13')==parent_main for row in attached),'Actual native parent attachment store to allocated bubble sprite')
 phases=[]
 for row in states:
  frame=number(row,'frame')
  if frame<number(constructed[0],'frame'):continue
  phases.append(dict(frame=frame,taskActive=task in nodes(row,'tasks'),taskFree=task in nodes(row,'freeTasks'),objectActive=any(object in nodes(row,key) for key in ('objects','layer1','layer2')),objectFree=object in nodes(row,'freeObjects'),taskID=number(row,'taskID'),taskOwner=pointer(row,'taskOwner'),taskResume=pointer(row,'taskResume'),objectCache=pointer(row,'objectCache'),objectPose=pointer(row,'objectPose'),parentTrail=pointer(row,'parentTrail'),physical=pointer(row,'physical'),physicalMain=pointer(row,'physicalMain'),taskReturned=number(row,'taskReturned'),objectReturned=number(row,'objectReturned')))
 first=lambda key:next((row['frame'] for row in phases if row[key]),None)
 return dict(action=control['action'],continuousLifecycleFields=len(states),trackedKanoBubbleAllocations=1,task=task,object=object,parent=parent,parentMain=parent_main,allocationFrame=number(post[0],'frame'),constructionFrame=number(constructed[0],'frame'),initialObjectTaskPointer=pointer(constructed[0],'objectTask'),
  firstTaskFreeMembership=first('taskFree'),firstObjectFreeMembership=first('objectFree'),
  actualTaskReturnCallbacks=select(rows,'RETURN_TASK'),actualObjectReturnCallbacks=select(rows,'RETURN_OBJECT'),
  actualTaskFreeHeadStores=select(rows,'FREE_TASK_STORE'),actualObjectFreeHeadStores=select(rows,'FREE_OBJECT_STORE'),
  finalObserverTaskReturned=number(final[0],'taskReturned'),finalObserverObjectReturned=number(final[0],'objectReturned'),
  finalNativeMembership=phases[-1],phases=phases,childObjectAndTaskTeardownAccepted=False)
def verify(folder):
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'));fighter,side=meta['winner'],meta['side']
 need(meta['exit_code']==0 and meta['candidate']==native.scene.current.NAME and meta['assistance']=='none' and meta['guest_writes']==0 and not meta['cheats_enabled'] and meta['command_case']=='positive' and meta['observation']==1600 and meta['requested_gap']==160 and before==meta['input_hashes'],'Terminal unchanged-build physical lifecycle capture')
 pins=native.scene.launch.source_pins()
 def pin(path,wanted=None):
  path=str(path);actual=native.scene.launch.sha(path);need(wanted is None or actual==wanted,'Immutable actual lifecycle dependency '+path);need(path not in pins or pins[path]==actual,'Consistent actual dependency '+path);pins[path]=actual
 for file,wanted in before.items():
  pin(file,wanted)
  if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
 observer=ROOT/'mk2ks_current_friendship_lifecycle_v2715.lua';text=observer.read_text()
 need(text.count("dofile('mk2ks_current_friendship_full_render_v2702.lua')")==1 and not re.search(r':write_|set_value|clear_value|load_?state|\.value\s*=(?!=)',text),'Lifecycle wrapper is read-only over exact existing physical/render driver')
 old_runner=(ROOT/'tools/run_current_friendship_full_render_v2703.ps1').read_text()
 expected=old_runner.replace('"$root/mk2ks_current_friendship_full_render_v2702.lua"','"$root/mk2ks_current_friendship_lifecycle_v2715.lua","$root/mk2ks_current_friendship_full_render_v2702.lua"',1)
 expected=expected.replace('-autoboot_script "$root/mk2ks_current_friendship_full_render_v2702.lua"','-autoboot_script "$root/mk2ks_current_friendship_lifecycle_v2715.lua"')
 need(expected==(ROOT/'tools/run_current_friendship_lifecycle_v2716.ps1').read_text(),'Entire launcher unchanged except new read-only wrapper and manifest pin')
 guest,_,payload=native.scene.current.expected();need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/native.scene.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual current guest/payload independently reconstructed')
 original_path=ROOT/'mk2/mk2-maincpu.bin';stock=original_path.read_bytes();pin(original_path,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
 for first,last in ((0xff83ae20,0xff83b3f0),(0xff80e0e0,0xff80e620),(0xff8090b0,0xff809270),(0xff8093e0,0xff809580),(0xff809670,0xff8099f0),(0xff82bb80,0xff82bc80)):
  a,b=(first-0xff800000)//8,(last-0xff800000)//8;need(guest[a:b]==stock[a:b],'Original native group/task/sprite allocate/register/retire implementation unchanged')
 native_rows=native.scene.previous.parse(folder/'run.log');image=native.graphics.graphics(pins);control=native.inventory(native_rows,fighter,side,guest,image)
 baseline=ROOT/f'audit_v2691_current_{fighter}_friendship_shadow_p{side}/run.log';pin(baseline)
 physical=lambda rs:[(tag,row) for tag,row in rs if not tag.startswith('SHADOW_')]
 need(physical(native_rows)==physical(native.scene.previous.parse(baseline)),'Every actual original physical input/health/pose/part/WIN/cue/transition record unchanged')
 rows=parse(folder/'run.log');result=check(rows,control,fighter,side)
 for path in folder.rglob('*'):
  if path.is_file():pin(path)
 pin(Path(__file__).resolve());native.scene.launch.module_pins(pins)
 return dict(passed=True,diagnosticCompleted=True,fighter=fighter,side=side,control=control,**result,wholeActualGuestAndPayloadReconstructed=True,originalNativeLifecycleRoutinesUnchanged=True,physicalInputAndNativeChronologyUnchanged=True,inputHashes=pins,gameChanged=False,fullFinisherAcceptance=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable actual lifecycle diagnostic')
 try:r=verify(a.folder)
 except Exception as error:r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({key:value for key,value in r.items() if key not in ('inputHashes','phases','actualTaskFreeHeadStores','actualObjectFreeHeadStores')},indent=2),flush=True);raise SystemExit(0 if r['passed'] else 1)
