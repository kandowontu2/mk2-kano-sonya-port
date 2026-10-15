"""Current Subzero whole native FIFO/projection/floor/shadow-disable contract.

Retain the entire3994/811 generic component/cache/cursor/DMA/projection/shadow
algorithm. Substitute only actual primary freeze task, original grounded own
groups and source-native shadow disable at56fields. Never add a frozen-corpse
shadow, proxy ID, forced clear or sliding correction. DeadPool normal contexts
only; full audio/other arenas/CPU/overlap/whole-port acceptance remains open.
"""
import argparse,copy,hashlib,inspect,json,re,struct,traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import current_payload_metadata_context_v5229 as current
import verify_kung_lao_split_native_fifo_v3994 as generic
import run_jax_clap_native_scene_v4028 as capture
import verify_native_subzero_legs_matrix_v5004 as state
ROOT,need,sha=current.ROOT,current.need,current.sha

def source_contract(guest):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();off=lambda a:(a-0xff800000)//8
 for lo,hi in ((0xff8c25c0,0xff8c2630),(0xff8c2e90,0xff8c3080),(0xff8c30b0,0xff8c3110),
               (0xff801070,0xff8017b0),(0xff841ec0,0xff841f40)):
  need(guest[off(lo):off(hi)]==stock[off(lo):off(hi)],'Whole original shadow-disable/fracture/park/direct-shadow blocks unchanged')
 need(struct.unpack_from('<7H',guest,off(0xff8c25c0))==(0xb501,0x0160,0x0b81,0x0010,0x0000,0xb028,0x0160),
      'Original actual body+160 flag AND FFFFFFEF then store; disable shadow bit4')
 need(struct.unpack_from('<I',guest,off(0xff8c26c0))[0]==0xffd62600 and
      struct.unpack_from('<I',guest,off(0xff8c3090))[0]==0xffd62a00 and
      struct.unpack_from('<2I',guest,0xac4c0+17*4)==(0xffd62400,0xffd62480)and
      struct.unpack_from('<2I',guest,0xac540+17*4)==(0xffd63400,0xffd63460),'True own whole/semantic-legs rows in actual original consumers')
 return dict(originalShadowDisableWordsBound=True,originalShadowKernelBound=True,originalFractureAndParkBlocksBound=True)

def physical(g,guest,payload,identity,side):
 begin=g['FLOOR_BEGIN'][0];origin=begin['origin'];end=g['FLOOR_RETIRED'][0]['frame']
 actor=g['FLOOR_STATE'][0][f'p{side}'];main=g['FLOOR_STATE'][0][f'main{side}']
 phase={r['frame']:r for r in g['FLOOR_PHASE']}
 own={r['frame']:r for r in g['FLOOR_BODY']if r['slot']==side}
 need(len(own)==len([r for r in g['FLOOR_BODY']if r['slot']==side])and set(own)==set(range(origin,end)),
      'Every actual physical victim pose/flags/world/floor field before native pointer retirement')
 whole=0xffd62400 if identity==17 else 0xffd62480;legs=0xffd63400 if identity==17 else 0xffd63460
 dizzy=0xff011f60 if identity==17 else 0xff0320c0
 fracture=[r for r in g['NATIVE_STATE']if r['tag']=='MK2_EARNED_SUBZERO_FRACTURE_ENTRY']
 need(len(fracture)==1,'Actual original native fracture invocation recorded')
 impact=int(fracture[0]['frame'])
 for frame,r in own.items():
  need(r['actor']==r['owner']==actor and r['main']==main and r['id']==r['roster']==identity and
       r['floor']==phase[frame]['stageY']-(134 if identity==17 else 135)and r['y']==r['floor']and
       r['vx']==r['vy']==r['gravity']==0,'All real own frozen physical states stay on source-native floor without motion or actor substitution')
  expected=dizzy if frame<origin+56 else whole if frame<impact else legs
  need(r['pose']==expected and bool(r['body']&16)==(frame<origin+56),'Complete exact dizzy/whole/leg lifecycle and native shadow-eligibility transition')
  if frame>=origin+56:need(r['bank']==0x0404,'Original native ice palette bank throughout whole/legs')
 owned_shadows=[r for r in g['SHADOW_COMPONENT']if r['slot']==side]
 need(owned_shadows and all(r['frame']<=origin+56 for r in owned_shadows),
      'Native own compressed shadows present before freeze and no post-disable imported shadow publication')
 # Own frozen streams are original raw6 uploads outside the imported range
 # used by the generic shadow observer. Account for their complete extents too.
 spans=[(0x1fa0000*8,(0x1fa0000+11944)*8),(0x1fa4000*8,(0x1fa4000+7032)*8)]
 need(not any(d['command']&15==8 and any(lo<=d['source']<hi for lo,hi in spans)for d in g['FLOOR_DMA']),
      'No hidden raw-six-bit whole/leg shadow DMA after original stock flag disable')
 # Native drawing precedes animation tasks in the field. Derive phase
 # publication from the previous complete physical state and ALL real body
 # passes; preserve actual no-render impact fields rather than fabricating them.
 body_frames={q['frame']for q in g['FLOOR_QUEUE']if q['slot']in(1,2)}
 expected={p:{f for f in body_frames if f-1 in own and own[f-1]['pose']==p}for p in(whole,legs)}
 actual={p:{q['frame']for q in g['FLOOR_QUEUE']if q['slot']==side and q['pose']==p}for p in(whole,legs)}
 need(actual==expected and all(expected.values()),'All real native whole/leg body passes correspond to complete preceding pose states, including native paused fields')
 return dict(origin=origin,fracture=impact,retirement=end,actualVictimFields=len(own),
             nativeShadowDisableFrame=origin+56,lastPreFreezeShadowDraw=max(r['frame']for r in owned_shadows),
             actualPreFreezeOwnedShadowCopies=len(owned_shadows),frozenWholeAndLegShadowCopies=0,
             phaseFields={f'{p:08X}':sorted(v)for p,v in actual.items()},
             sourceNativeGroundingAndShadowDisableAccepted=True)

def make_contract():
 source=inspect.getsource(generic.contract)
 def replace(before,after,count=1):
  nonlocal source
  need(source.count(before)==count,'Exact whole generic native FIFO adaptation '+before)
  source=source.replace(before,after)
 replace('    ids={side:identity,3-side:0};anchors={0:140,17:134,18:135}',
         '    ids={side:identity,3-side:8};anchors={8:131,17:134,18:135}')
 first=source.index("    secondary={q['actor']")
 last=source.index("    for r in g['FLOOR_STATE']:",first)
 source=source[:first]+"""    phase_targets={0xffd62400,0xffd63400}if identity==17 else{0xffd62480,0xffd63460}
    source_contract(guest)
    need(not any(q['slot']==3 for q in g['FLOOR_QUEUE']),'No proxy/secondary physical frozen victim')
    need(begin['id']==identity and begin['entry']==0xff8c2320 and begin['actor']==actors[side]and begin['main']==mains[side]and
         retired['p1']==retired['p2']==0 and retired['victim_health']==0 and retired['mode']in(3,5),'True native own deep-freeze task and actual both-pointer teardown')
    need(result['origin']==origin and result['retired']==end and result['snapshots']==end-origin+30 and
         [r['frame']for r in g['FLOOR_STATE']]==list(range(origin,end+31)),'All physical states through natural disappearance plus30')
"""+source[last:]
 changes={
  "active=q['actor']in(actors[1],actors[2])or(q['actor']==actors[3]and q['frame']>=creation)":"active=q['actor']in(actors[1],actors[2])",
  "s=q['slot'];owner=actors[side]if s==3 else actors.get(s)":"s=q['slot'];owner=actors.get(s)",
  "allowed_owner=hat if s==3-side and hat_owner_first<=q['frame']<hat_owner_first+12 else owner":"allowed_owner=owner",
  "s in(1,2,3)":"s in(1,2)","q['kind']==(1 if s==3 else 0)":"q['kind']==0 ",
  "s in(side,3)and 0xfffdf100<=q['pose']<0xfffdf600":"s==side and q['pose']in phase_targets",
  "q['slot']in(side,3)and 0xfffdf100<=q['pose']<0xfffdf600":"q['slot']==side and q['pose']in phase_targets",
 }
 for before,after in changes.items():replace(before,after,2 if before=='s in(1,2,3)'else 1)
 replace("            need(q['y']==q['floor']and(d['y']&255)+d['height']-1==ground,'Every true primary and mirrored split phase genuinely contacts native raster floor')",
         "            union_bottom=max(q['y']-p['dy']+p['height']-1 for p in group(q,payload,guest))+t['displayY']-t['cameraY']-(t['displayY']&256)\n            need(q['y']==q['floor']and union_bottom==ground,'Whole native multipart frozen/leg union contacts actual source-native floor; never force every upper part to be a foot')")
 first=source.index('    phase_start=')
 last=source.index('    own_shadows=shadow_contract(g)',first)
 source=source[:first]+"""    need(set(phases)=={(side,p)for p in phase_targets}and all(phases[side,p]for p in phase_targets),'Both own frozen/semantic-leg groups genuinely publish')
    need(all(draws[s]>0 for s in(1,2)),'Both true physical fighters publish and draw')
    native_physical=physical(g,guest,payload,identity,side)
"""+source[last:]
 replace('actualOwnedCompressedShadowRows=own_shadows,allArenaFloorShadowsAccepted=False)',
         'actualOwnedCompressedShadowRows=own_shadows,nativePhysicalFreeze=native_physical,allArenaFloorShadowsAccepted=False)')
 namespace=dict(vars(generic),source_contract=source_contract,physical=physical)
 exec(compile(source,__file__+'::complete_native_frozen_FIFO_projection_shadow','exec'),namespace)
 return namespace['contract']

def parsed(log):
 groups=defaultdict(list)
 for index,line in enumerate(log.splitlines()):
  row=capture.model.parse(line)
  if row and row[0]!='FLOOR_CPU':row[1]['_observed_line']=index;groups[row[0]].append(row[1])
 groups['NATIVE_STATE']=[r for r in state.parser.parse(log)if '_DIGEST'not in r['tag']]
 return groups

def run(fighter,side):
 folder=ROOT/f'audit_v6178_current_subzero_{fighter}_p{side}_native_scene_ram'
 observed=ROOT/f'audit_v6179_current_subzero_{fighter}_p{side}_scene_observed/report.json'
 report=json.loads(observed.read_text());meta=json.loads((folder/'result.json').read_text())
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();identity=17 if fighter=='kano'else 18
 need(report['passed']and report['actualContinuousNativeSceneAccepted']and report['actualWindowsTerminal']['nativeExit']==meta['exit_code']==0 and
      meta['candidate']==current.NAME and meta['ramGuestSHA256']==current.GUEST_SHA and not meta['modelErrors']and
      meta['observedRGBFields']==meta['modelExactFields']==report['exactFields'],'Actual current full cold guest/terminal/whole unweakened native pixel replay')
 pins=dict(report['inputHashes']);pins.update({str(p.resolve()):sha(p)for p in(observed,Path(__file__),Path(current.__file__),Path(generic.__file__),Path(generic.shadow.__file__),Path(capture.__file__),Path(state.__file__))})
 for p,h in pins.items():need(sha(p)==h,'Actual compiled/controller/source/evidence input unchanged')
 log=(folder/'run.log').read_text();g=parsed(log);contract=make_contract();positive=contract(g,guest,payload,identity,side)
 # The entire native command/state/effect/next-match row set must equal the
 # independently accepted current sparse run. No reference RGB is relabelled
 # as a new observation; actual native THREE overlapping stages are compared.
 reference_path=ROOT/'audit_v6175_current_subzero_shatter_checked/report.json';reference=json.loads(reference_path.read_text())
 need(reference['passed']and not reference['fullPortAcceptance']and all(sha(p)==h for p,h in reference['inputHashes'].items()),'Full retained current four-slot/state/refill/pixel matrix intact')
 old_folder=ROOT/f'audit_v6164_current_subzero_{fighter}_p{side}_lifecycle'
 old_rows=[r for r in state.parser.parse((old_folder/'run.log').read_text())if '_DIGEST'not in r['tag']]
 need(g['NATIVE_STATE']==old_rows,'Every current physical input/native/opcode/health/effect/lifecycle/next-match row unchanged under whole-render observer')
 records=json.loads((folder/'continuous_scene_records.json').read_text());visible=json.loads((folder/'visible_digests.json').read_text())
 by_frame={r['frame']:r for r in records};rgb={int(re.search(r'_(\d+)\.png$',r['file']).group(1)):r['rgbSHA256']for r in visible}
 sparse=json.loads((old_folder/'rgb_memory_proofs.json').read_text())
 for s in sparse[:3]:need(rgb[s['frame']]==s['actualRGBSHA256'],'Each of three complete overlapping current native finisher RGB stages identical, no donor/modelled substitute')
 need([r['frame']for r in records]==list(range(positive['origin']+1,positive['disappearance']+31))and
      len(records)==report['exactFields']and all(r['exactRGBPixels']==400*254 and r['exactVRAMWords']==512*512 for r in records),
      'Every actual continuous displayed pixel and full VRAM target through native removal plus30')
 atlas=np.asarray(Image.open(report['nativeReview']).convert('RGB'));need(atlas.shape==(556,800,3),'One bounded actual native three-panel review')
 frames=sorted((int(k,16),v)for k,v in report['actualPhaseFrames'].items())+[(0,records[-1]['frame'])]
 for i,(pose,frame)in enumerate(frames):
  x,y=i%2*400,i//2*278
  need(hashlib.sha256(atlas[y+24:y+278,x:x+400].tobytes()).hexdigest().upper()==rgb[frame],'Every whole new native review panel bound to actual pixels')
 faults=[]
 def reject(label,changed):
  try:contract(changed,guest,payload,identity,side)
  except(ValueError,KeyError,AssertionError)as e:faults.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Accepted actual native freeze/FIFO/ground/shadow corruption '+label)
 own_index=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==side and r['pose']in {0xffd62400,0xffd62480})
 q=g['FLOOR_QUEUE'][own_index];key=q['frame'],q['cursor']
 trials=[('proxy_frozen_id','FLOOR_QUEUE',own_index,'id',1),('wrong_actor_owner','FLOOR_QUEUE',own_index,'owner',0),
         ('wrong_physical_main','FLOOR_QUEUE',own_index,'main',0),('wrong_cache_row','FLOOR_QUEUE',own_index,'row',0),
         ('donor_art_source','FLOOR_QUEUE',own_index,'source',0),('shifted_native_xy','FLOOR_QUEUE',own_index,'xy',q['xy']^1)]
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_TRANSFORM'])if(r['frame'],r['cursor'])==key)
 trials.extend([('shifted_camera','FLOOR_QUEUE_TRANSFORM',i,'camera',g['FLOOR_QUEUE_TRANSFORM'][i]['camera']^1),
                ('floating_floor','FLOOR_QUEUE_TRANSFORM',i,'floor',q['floor']+1)])
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_PART'])if(r['frame'],r['cursor'])==key)
 trials.append(('wrong_art_width','FLOOR_QUEUE_PART',i,'width',g['FLOOR_QUEUE_PART'][i]['width']+1))
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_DISPATCH'])if r['slot']==side)
 trials.append(('wrong_physical_consumer','FLOOR_QUEUE_DISPATCH',i,'slot',3-side))
 i=next(i for i,r in enumerate(g['FLOOR_BODY'])if r['slot']==side and r['frame']==positive['origin']+56)
 trials.extend([('missing_shadow_disable','FLOOR_BODY',i,'body',g['FLOOR_BODY'][i]['body']|16),
                ('wrong_ice_palette','FLOOR_BODY',i,'bank',0x202),('floating_frozen_body','FLOOR_BODY',i,'y',g['FLOOR_BODY'][i]['y']-1)])
 i=next(i for i,r in enumerate(g['FLOOR_BODY'])if r['slot']==side and r['frame']==positive['origin']+55)
 trials.append(('premature_shadow_disable','FLOOR_BODY',i,'body',g['FLOOR_BODY'][i]['body']&~16))
 trials.extend([('wrong_pointer_retirement','FLOOR_RETIRED',0,'p1',1),('fake_native_roster','FLOOR_STATE',0,f'roster{side}',1)])
 component=g['SHADOW_COMPONENT'][0];i=next(i for i,r in enumerate(g['FLOOR_DMA'])if r['event']==component['event'])
 trials.extend([('wrong_pre_freeze_shadow_owner','SHADOW_COMPONENT',0,'owner',0),
                ('wrong_pre_freeze_shadow_source','SHADOW_COMPONENT',0,'first_source',component['first_source']^1),
                ('wrong_original_shadow_caller','FLOOR_DMA',i,'pc',0)])
 for label,tag,index,key,value in trials:
  changed=copy.deepcopy(g);need(changed[tag][index][key]!=value,'Non-vacuous actual native row corruption');changed[tag][index][key]=value;reject(label,changed)
 # A missing physical state and a fabricated raw frozen-shadow command are
 # separately exercised, including graphics outside imported shadow filtering.
 changed=copy.deepcopy(g);changed['FLOOR_BODY']=[r for r in changed['FLOOR_BODY']if not(r['slot']==side and r['frame']==positive['origin']+80)];reject('omitted_actual_frozen_field',changed)
 changed=copy.deepcopy(g);target=next(d for d in changed['FLOOR_DMA']if 0xfd00000<=d['source']<0xfd17540 and d['command']&15==2);target['command']=(target['command']&~15)|8;reject('fabricated_raw_frozen_shadow',changed)
 need(contract(g,guest,payload,identity,side)==positive,'Entire uncached positive native FIFO/floor/shadow restored after all actual corruptions')
 for p in folder.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 pins[str(reference_path)]=sha(reference_path)
 need(all(sha(p)==h for p,h in pins.items()),'All actual sources/state/palette/pixel/evidence unchanged at complete qualification')
 return dict(passed=True,fighter=fighter,side=side,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
             sourceNativeTask=source_contract(guest),nativeFIFO=positive,exactNativeFields=len(records),exactNativeRGBPixels=len(records)*400*254,
             actualSemanticFaultsRejected=len(faults),actualRecordFaults=faults,actualNativePixelFaultsRejected=report['rejectedActualPixelTargetFaults'],
             nativeReview=report['nativeReview'],actualNativeReviewPanels=3,actualWindowsTerminal=report['actualWindowsTerminal'],
             completeCurrentStateRowsEqualIndependentQualifiedReference=True,threeOverlappingNativeRGBStagesExactlyEqual=True,
             newNextCPURGBRecaptured=False,currentContinuousSceneFIFOProjectionGroundAndShadowDisableAccepted=True,
             fullArtAcrossAllArenasAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6181_current_subzero_{a.fighter}_p{a.side}_scene_checked';need(not out.exists(),'Fresh actual native FIFO/floor/shadow report')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualRecordFaults')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
