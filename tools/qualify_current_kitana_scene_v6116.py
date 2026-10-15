"""Four current earned Kitana inflation scenes: native pixels, FIFO and cleanup.

Keep the complete original command/table/state and source FIFO/shadow contract.
The independent continuous replay compares all actual RGB and native VRAM words;
later targets never become model anchors. This finite Dead Pool victim matrix
does not prove all arenas, other finishers, audio or the full port objective.
"""
import copy,json,re,struct
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_kitana_inflation_native_fifo_v3924 as fifo
import verify_kitana_inflation_earned_state_v3933 as earned
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6117_current_kitana_scene_checked'
CONTEXTS=(('kano',1),('kano',2),('sonya',1),('sonya',2))

def refill(rs,side,guest):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();lo,hi=0xff9dec90,0xff9def80
 need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==stock[(lo-0xff800000)//8:(hi-0xff800000)//8],
      'Whole original native FFFF sentinel/initial4/add2/final161 global refill remains exact')
 h=[r for r in rs if r['tag']=='HEALTH'];startpc='FF9DECE0'if side==1 else'FF9DED10';steppc='FF9DEF40'if side==1 else'FF9DEF70'
 starts=[(i,r)for i,r in enumerate(h)if r['pc']==startpc]
 need(len(starts)==1,'One actual complete inter-round victim lifebar refill')
 i,r=starts[0];at=int(r['frame']);need(r['before']=='161'and r['after']=='65535','Exact native161-to-FFFF sentinel')
 consumed={i};previous=65535;values=list(range(4,161,2))+[161]
 for age,value in enumerate(values):
  need(i+age+1<len(h),'No omitted original global refill store')
  r=h[i+age+1]
  need(r['pc']==steppc and int(r['frame'])==at+age and int(r['before'])==previous and int(r['after'])==value,
       'Every native refill value, previous-health chain, writer and exact field')
  consumed.add(i+age+1);previous=value
 need(all(j in consumed or 0<=int(r['before'])<=161 and 0<=int(r['after'])<=161 for j,r in enumerate(h)),
      'No arbitrary invalid health outside complete source-native sentinel/refill')
 kos=[int(r['frame'])for r in h if r['pc']=='FF836700'and r['after']=='0'and 0<int(r['before'])<=161]
 origin=int(next(r for r in rs if r['tag']=='ACTION')['frame'])
 need(len(kos)==2 and kos[0]<at<=at+79<kos[1]<origin,'Whole refill strictly between earned native KOs')
 return dict(startFrame=at,endFrame=at+79,actualStores=81,completeNativeRefillAccepted=True,
             healthTapBoundToPhysicalSlot=True,registerOwnershipNotRecordedOrClaimed=True)

def state_gate(rs,fighter,side,guest):
 positive=earned.gate(rs,fighter,side,guest);positive['nativeInterRoundRefill']=refill(rs,side,guest)
 return positive

def state_faults(rs,fighter,side,guest):
 positive=state_gate(rs,fighter,side,guest);faults=[]
 trials=[('proxy_first_live','FIRST_LIVE','ids','4,1'),('foreign_actor','ACTION','actor','01000000'),
 ('fabricated_damage','ACTION','damage','161'),('wrong_health_writer','HEALTH','pc','FF838860'),
 ('wrong_parameter_owner','PARAMETER','actor','01000000'),('wrong_pointer_half','GORE_ROW','value','FFFF'),
 ('wrong_command_parser','COMPARE','actual','999'),('wrong_completion_owner','WRAP','main','01000000'),
 ('fabricated_terminal','RESULT','wins','3')]
 def reject(name,changed):
  try:state_gate(changed,fighter,side,guest)
  except (ValueError,KeyError,AssertionError):faults.append(name)
  else:raise ValueError('Accepted actual state fault '+name)
 for label,tag,key,value in trials:
  changed=copy.deepcopy(rs);target=next(r for r in changed if r['tag']==tag and(tag!='COMPARE'or int(r['frame'])==positive['origin']))
  need(target[key]!=value,'Non-vacuous executed state corruption');target[key]=value;reject(label,changed)
 first=int(next(r for r in rs if r['tag']=='APPROACH')['frame'])+10
 changed=[r for r in rs if not(r['tag']=='INPUT'and int(r['frame'])==first and r['slot']==str(3-side)and r['button']==('Left'if side==1 else'Right'))]
 need(len(changed)<len(rs),'Remove actual native direction command');reject('missing_physical_direction',changed)
 at=positive['nativeInterRoundRefill']['startFrame']
 for label,age,value in [('wrong_refill_sentinel',0,'65534'),('wrong_refill_value',1,'7')]:
  changed=copy.deepcopy(rs)
  target=next(r for r in changed if r['tag']=='HEALTH'and int(r['frame'])==at+age and r['after']==('65535'if age==0 else'6'))
  target['after']=value;reject(label,changed)
 need(state_gate(rs,fighter,side,guest)==positive,'Whole positive command/state/refill restored')
 return faults

def fifo_faults(g,guest,payload,identity,side,positive):
 faults=[];oi=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==side and 0xfffd8c00<=r['pose']<0xfffd8f00)
 q=g['FLOOR_QUEUE'][oi];key=q['frame'],q['cursor']
 trials=[('proxy_id','FLOOR_QUEUE',oi,'id',1),('wrong_owner','FLOOR_QUEUE',oi,'owner',0),
 ('wrong_cached_row','FLOOR_QUEUE',oi,'row',0),('wrong_source','FLOOR_QUEUE',oi,'source',0),
 ('wrong_native_xy','FLOOR_QUEUE',oi,'xy',q['xy']^1)]
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_TRANSFORM'])if(r['frame'],r['cursor'])==key)
 trials.append(('shifted_backdrop_projection','FLOOR_QUEUE_TRANSFORM',i,'camera',g['FLOOR_QUEUE_TRANSFORM'][i]['camera']^1))
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_PART'])if(r['frame'],r['cursor'])==key)
 trials.append(('wrong_art_width','FLOOR_QUEUE_PART',i,'width',g['FLOOR_QUEUE_PART'][i]['width']+1))
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_DISPATCH'])if r['slot']==side)
 trials.append(('wrong_consumer_slot','FLOOR_QUEUE_DISPATCH',i,'slot',3-side))
 trials.extend([('wrong_teardown_pointer','FLOOR_RETIRED',0,'p1',1),('wrong_live_identity','FLOOR_STATE',0,f'roster{side}',1)])
 component=g['SHADOW_COMPONENT'][0]
 trials.extend([('wrong_shadow_owner','SHADOW_COMPONENT',0,'owner',0),
                ('wrong_shadow_row_source','SHADOW_COMPONENT',0,'first_source',component['first_source']^1)])
 i=next(i for i,r in enumerate(g['FLOOR_DMA'])if r['event']==component['event'])
 trials.append(('wrong_shadow_caller','FLOOR_DMA',i,'pc',0))
 for label,tag,index,key,value in trials:
  changed=copy.deepcopy(g);changed[tag][index][key]=value
  try:fifo.contract(changed,guest,payload,identity,side)
  except (ValueError,KeyError,AssertionError):faults.append(label)
  else:raise ValueError('Accepted actual FIFO fault '+label)
 need(fifo.contract(g,guest,payload,identity,side)==positive,'Complete actual native FIFO restored')
 return faults

def run():
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for source,dest,stride in ((0xff8cd3b0,0xfd680,2),(0xff8cd2f0,0xfd6c0,2),(0xff9ed0f0,0xfac40,4),(0xff9eca40,0xfac90,4),(0xff9ecc30,0xface0,4)):
  lo=(source-0xff800000)//8;need(guest[dest:dest+17*stride]==stock[lo:lo+17*stride],'All17original stock parameter/animation/palette rows preserved')
 pins={str(Path(__file__).resolve()):sha(__file__)}
 for module in (current,fifo,earned,fifo.shadow):pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
 legacy_path=ROOT/'audit_v3925_kitana_inflation_native_fifo_checked/report.json'
 legacy=json.loads(legacy_path.read_text());need(legacy['passed']and legacy['actualContexts']==4,'Retained whole source/FIFO/pixel reference qualified in all four contexts')
 pins[str(legacy_path)]=sha(legacy_path);cases=[]
 for fighter,side in CONTEXTS:
  folder=ROOT/f'audit_v6114_current_kitana_{fighter}_p{side}_native_scene_ram'
  reportpath=ROOT/f'audit_v6115_current_kitana_{fighter}_p{side}_scene_observed/report.json'
  observed=json.loads(reportpath.read_text());meta=json.loads((folder/'result.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
  need(not observed['passed']and observed['error']=="ValueError('Actual true Kitana winner, own victim and native both-pointer teardown')"and
       meta['candidate']==current.NAME and meta['exit_code']==terminal['nativeExit']==0 and
       meta['ramGuestSHA256']==current.GUEST_SHA and not meta['modelErrors']and
       meta['observedRGBFields']==meta['modelExactFields']==737,
       'Actual current native terminal and complete unweakened continuous scene model')
  # Capture host used identity for both the integer fighter ID and the CIM
  # process dictionary. Its postassertion fails without a native/model fault.
  # Reparse authoritative rows with distinct values; never restart or forge IDs.
  process=json.loads((folder/'process.json').read_text());windows_identity=terminal['actualWindowsIdentity']
  need(process['actualWindowsIdentity']==windows_identity and process['pid']==terminal['pid']==windows_identity['ProcessId']and
       windows_identity['Name']=='mkport_candidate.exe'and
       Path(windows_identity['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
       str(folder)in windows_identity['CommandLine'],'Actual creation/executable/full-command native terminal identity')
  for p,h in meta['input_hashes'].items():need(sha(p)==h,'Actual executed input unchanged');pins[p]=h
  need(meta['input_hashes']==json.loads((folder/'input_hashes_before.json').read_text()),'Whole executed preboot pin ledger retained')
  text=(folder/'run.log').read_text();need((folder/'stderr.log').read_text()==''and not re.search('LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS',text,re.I),'Fault-free actual native replay')
  rs=earned.rows(text);state=state_gate(rs,fighter,side,guest);g=defaultdict(list)
  for index,line in enumerate(text.splitlines()):
   parsed=fifo.model.parse(line)
   if parsed and parsed[0]!='FLOOR_CPU':parsed[1]['_observed_line']=index;g[parsed[0]].append(parsed[1])
  identity=17 if fighter=='kano'else 18;projection=fifo.contract(g,guest,payload,identity,side)
  records=json.loads((folder/'continuous_scene_records.json').read_text());later=[r for r in records if r['frame']>=projection['disappearance']+3]
  need(len(records)==meta['observedRGBFields']==meta['modelExactFields']==737 and
       [r['frame']for r in records]==list(range(projection['origin']+1,projection['disappearance']+31))and later and
       all(r['body'][str(side)]['pixels']==0 and r['shadowPixels']==0 for r in later),
       'Every consecutive actual native scene field, complete erased victim/body/shadow after teardown')
  native_rgb=json.loads((folder/'visible_digests.json').read_text())
  need(len(native_rgb)==len(records)and all(v['file']==f"display_{r['frame']}.png"and v['rgbSHA256']==r['rgbSHA256']for v,r in zip(native_rgb,records)),
       'Every actual RAM-decoded native RGB target digest agrees with the independent replay record')
  oldrecords_path=ROOT/f'audit_v3921_kitana_{fighter}_p{side}_native_scene_ram/continuous_scene_records.json'
  need(sha(oldrecords_path)==legacy['inputHashes'][str(oldrecords_path)],'Protected source-qualified original complete pixel reference')
  oldrecords=json.loads(oldrecords_path.read_text())
  need([(r['frame'],r['rgbSHA256'])for r in records]==[(r['frame'],r['rgbSHA256'])for r in oldrecords],
       'All737current native screens exactly match entire retained native reference, no crop/mask/tolerance')
  review=ROOT/f'art_review_inflation_v3923/{fighter}-p{side}-native-inflation-review.png'
  need(review.is_file(),'Existing six-phase/post-removal native review; current whole-scene hashes exact')
  pins[str(oldrecords_path)]=sha(oldrecords_path);pins[str(review)]=sha(review)
  faults=state_faults(rs,fighter,side,guest)+fifo_faults(g,guest,payload,identity,side,projection)
  need(not list(folder.glob('*.bin'))and not list(folder.glob('*.wav'))and not(folder/'input_sources').exists(),
       'No raw native media or duplicate source directory')
  for p in folder.rglob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
  pins[str(reportpath)]=sha(reportpath)
  cases.append(dict(fighter=fighter,side=side,exactFields=len(records),actualEarnedNativeState=state,
       nativeFIFO=projection,actualSemanticFaultsRejected=faults,actualWindowsTerminal=terminal,
       nativeReview=str(review),all737CurrentNativeRGBFieldsEqualReference=True,
       hostVariableCollisionQualifiedWithoutGameChanges=True,postRemovalPixels=0))
 need(all(sha(p)==h for p,h in pins.items()),'All source/terminal/scene evidence unchanged')
 return dict(passed=True,candidate=current.NAME,cases=cases,inputHashes=pins,actualContexts=4,
     exactNativeFields=sum(c['exactFields']for c in cases),exactRGBPixels=sum(c['exactFields']for c in cases)*400*254,
     actualSemanticFaultsRejected=sum(len(c['actualSemanticFaultsRejected'])for c in cases),
     currentEarnedInflationSceneFIFOProjectionGroundingShadowAndEraseAccepted=True,
     finiteSixPhaseAndPostRemovalNativeReviewAccepted=True,allCurrentNativeRGBFieldsEqualProtectedReference=True,
     fullAudioAcceptance=False,fullPortAcceptance=False,
     rawMediaFilesWritten=0,newSourceDirectoryCopies=0,newBuildCopies=0,nativeGameChanges=0,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh complete current native inflation matrix')
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
