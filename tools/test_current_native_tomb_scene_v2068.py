"""False-evidence tests for the current native P2 Sonya Tomb recording.

All mutations are in memory only. No ROM, executable, captured file, physical
controls or emulated gameplay state is changed. Full-port acceptance stays open.
"""
import json
from pathlib import Path
from unittest.mock import patch
import verify_current_native_tomb_scene_v2067 as model

ROOT=model.ROOT
OUT=ROOT/'audit_v2068_current_sonya_p2_tomb_counterexamples'

def run():
 proofpath=ROOT/'audit_v2067_current_sonya_p2_tomb_scene_checked/report.json'
 proof=json.loads(proofpath.read_text());assert proof['passed']and not proof['fullPortAcceptance']
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():assert model.launch.sha(file)==wanted
 pins[str(proofpath)]=model.launch.sha(proofpath)
 groups,buffers,a,b,owners=model.raster.data(model.CASE)
 queue=next(q for q in groups['FLOOR_QUEUE']if q['slot']==2 and q['part']==0)
 key={k:queue[k]for k in('frame','cursor')}
 dispatched=next(d for d in groups['FLOOR_QUEUE_DISPATCH']if d['cursor']==key['cursor']and d['queue_frame']==key['frame'])
 event=dispatched['event'];shadow_event=groups['SHADOW_COMPONENT'][0]['event'];tests=[]
 def row(g,tag,where):
  rows=[r for r in g[tag]if all(r.get(k)==v for k,v in where.items())]
  assert len(rows)==1,(tag,where,len(rows));return rows[0]
 q=lambda g:row(g,'FLOOR_QUEUE',key)
 t=lambda g:row(g,'FLOOR_QUEUE_TRANSFORM',key)
 inv=lambda g:row(g,'FLOOR_ALL_QUEUE',key)
 d=lambda g:row(g,'FLOOR_DMA',{'event':event})
 sh=lambda g:row(g,'FLOOR_DMA',{'event':shadow_event})
 def reject(name,change):
  mutated={tag:[dict(r)for r in rows]for tag,rows in groups.items()}
  change(mutated);variant=(mutated,buffers,a,b,owners)
  with patch.object(model.raster,'data',return_value=variant),patch.object(model.raster.base,'data',return_value=variant),patch.object(model.shadow,'data',return_value=variant):
   try:model.verify()
   except(AssertionError,ValueError,KeyError,IndexError)as error:
    tests.append(dict(name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
   else:raise AssertionError('Accepted corrupted native Tomb evidence '+name)
  print('Rejected '+name+' ('+str(len(tests))+')',flush=True)
 reject('proxy_performer_ID',lambda g:q(g).update(id=1))
 reject('detached_performer_owner',lambda g:q(g).update(owner=queue['actor']^16))
 reject('invented_floor_anchor',lambda g:row(g,'FLOOR_BODY',{'frame':7757,'slot':1}).update(floor=87))
 reject('wrong_postfight_player_state',lambda g:row(g,'FLOOR_STATE',{'frame':8255}).update(state1=1))
 reject('Main_global_cleared_before_native_code',lambda g:row(g,'FLOOR_STATE',{'frame':8263}).update(main1=0))
 reject('proxy_native_pointer_clear_PC',lambda g:g['FLOOR_POINTER_STORE'][0].update(pc=0xffffde00))
 reject('pointer_clear_delayed',lambda g:g['FLOOR_POINTER_STORE'][0].update(frame=8264))
 def missing_inventory(g):
  g['FLOOR_ALL_QUEUE']=[r for r in g['FLOOR_ALL_QUEUE']if not all(r.get(k)==v for k,v in key.items())]
 reject('missing_physical_FIFO_inventory',missing_inventory)
 reject('body_source_changed',lambda g:inv(g).update(source=queue['source']+8))
 reject('camera_owned_by_wrong_actor',lambda g:t(g).update(actor=queue['actor']^16))
 reject('camera_Y_shifted_one_pixel',lambda g:t(g).update(camera=t(g)['camera']+65536))
 reject('display_Y_shifted_one_pixel',lambda g:t(g).update(display=t(g)['display']+65536))
 reject('native_body_DMA_Y_shifted_one_pixel',lambda g:d(g).update(y=d(g)['y']+1))
 reject('native_body_DMA_X_shifted_one_pixel',lambda g:d(g).update(x=d(g)['x']+1))
 reject('original_cached_part_offset_shifted',lambda g:row(g,'FLOOR_QUEUE_PART',{**key,'part':0}).update(dy=999))
 reject('native_shadow_palette_not_black_bank',lambda g:sh(g).update(palette=0x100))
 reject('native_shadow_colour_not_black_pen',lambda g:sh(g).update(color=14))
 def missing_shadow(g):
  g['SHADOW_COMPONENT']=[r for r in g['SHADOW_COMPONENT']if r['event']!=shadow_event]
 reject('native_shadow_missing_owner',missing_shadow)
 reject('missing_last_completed_postteardown_frame',lambda g:g['FLOOR_SNAP'].pop())
 reject('retirement_origin_moved',lambda g:g['FLOOR_RESULT'][0].update(retired=8264))
 # Mutating original records must be rejected before visual replay. Files and
 # hashes stay unchanged; only the verifier's one in-memory log read differs.
 log=(model.CASE/'run.log').read_text(encoding='utf-8-sig')
 real_read=Path.read_text
 def reject_log(name,altered):
  assert altered!=log
  def read(path,*args,**kwargs):
   if path.resolve()==(model.CASE/'run.log').resolve():return altered
   return real_read(path,*args,**kwargs)
  with patch.object(Path,'read_text',read):
   try:model.verify()
   except(AssertionError,ValueError,KeyError,IndexError)as error:
    tests.append(dict(name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
   else:raise AssertionError('Accepted corrupted original Tomb record '+name)
  print('Rejected '+name+' ('+str(len(tests))+')',flush=True)
 branch=next(r for r in log.splitlines()if r.startswith('MK2_STAGE_PROVENANCE_BRANCH frame=7799 ')and 'entry=FF8EB1A0 'in r)
 reject_log('wrong_original_RNG_branch_value',log.replace(branch,branch.replace('a0=00000019','a0=00000032')))
 motion=next(r for r in log.splitlines()if r.startswith('MK2_STAGE_PROVENANCE_FIELD frame=7800 '))
 reject_log('victim_ceiling_hold_one_pixel_wrong',log.replace(motion,motion.replace('y=-173','y=-172')))
 reject_log('missing_native_motion_field',log.replace(motion+'\n',''))
 ko=next(r for r in log.splitlines()if r.startswith('MK2_STAGE_WINDOW ')and 'match=2 'in r)
 reject_log('unearned_Tomb_finish_window',log.replace(ko,ko.replace('damage=322','damage=321')))
 assert len(tests)==24 and all(t['rejected']for t in tests)
 print('All 24 corruptions rejected; rechecking unmodified full Tomb recording',flush=True)
 good=model.verify();assert good['passed']
 assert all(good[k]==proof[k]for k in('sampledFrames','exactReplayedFrames','exactScreenPixels','exactOwnedPixels','sourceBoundProjections','fullPhysicalPaletteChecks','nativeShadowCopies','continuousErase','audioInventory'))
 pins.update(good['inputHashes']);model.launch.module_pins(pins)
 return dict(passed=True,rejectedCounterexamples=len(tests),tests=tests,unmodifiedFullSceneRechecked=True,inputHashes=pins,
  gameOrCaptureBytesChanged=False,audioAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 assert not OUT.exists(),'Preserve executed evidence'
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('passed','error','rejectedCounterexamples','unmodifiedFullSceneRechecked')if k in report}),flush=True)
 raise SystemExit(0 if report['passed']else 1)
