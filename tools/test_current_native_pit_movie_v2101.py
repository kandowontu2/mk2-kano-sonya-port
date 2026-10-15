"""Copy-only adversarial current Pit evidence with positive controls.

Unexpected key/index/parser errors are failures, never accepted rejections.
No source, ROM, runtime input or retained capture is edited.
"""
import argparse,json,traceback
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
import verify_current_native_pit_movie_v2100 as model
ROOT=model.ROOT
def run(case):
 fighter,side,leaf=model.CASES[case];folder=ROOT/leaf
 path=ROOT/f'audit_v2100_current_{case}_pit_movie_checked/report.json';proof=json.loads(path.read_text())
 model.need(proof['passed']and not proof['fullPortAcceptance'],'Actual full positive preflight')
 pins=dict(proof['inputHashes'])
 for f,h in pins.items():model.need(model.launch.sha(f)==h,'Changed positive dependency '+f)
 pins[str(path)]=model.launch.sha(path)
 groups,buffers,other1,other2,owners=model.raster.data(folder)
 source_pins=model.launch.source_pins();expected=model.launch.current.expected()
 graphics_pins={};image=model.prior.graphics.graphics(graphics_pins)
 def graphics(p):p.update(graphics_pins);return image
 def run_copy(g):
  variant=(g,buffers,other1,other2,owners)
  with ExitStack()as stack:
   stack.enter_context(patch.object(model.raster,'data',return_value=variant))
   stack.enter_context(patch.object(model.raster.base,'data',return_value=variant))
   stack.enter_context(patch.object(model.launch,'source_pins',side_effect=lambda:dict(source_pins)))
   stack.enter_context(patch.object(model.launch.current,'expected',return_value=expected))
   stack.enter_context(patch.object(model.prior.graphics,'graphics',side_effect=graphics))
   return model.verify(case)
 def copied():return defaultdict(list,{tag:[dict(r)for r in rows]for tag,rows in groups.items()})
 positive=run_copy(copied())
 model.need(positive['passed']and all(positive[k]==proof[k]for k in('sampledFrames','exactScreenPixels','continuousErase','movie')),'Unchanged in-memory positive control')
 print(case+' unchanged in-memory full-scene control passes',flush=True)
 tests=[]
 def reject(name,change,wanted):
  g=copied();change(g)
  try:run_copy(g)
  except ValueError as error:
   model.need(wanted in str(error),'Unexpected validation failure for '+name+': '+str(error))
   tests.append(dict(name=name,rejected=True,errorType='ValueError',validation=str(error)))
  else:raise AssertionError('Accepted corrupted actual Pit '+name)
  print(case+' rejected '+name+' ('+str(len(tests))+')',flush=True)
 movie=proof['movie'];enter=movie['enter'];clear=movie['actualMovieAddressRepurposed'];a=movie['actualActor']
 q=next(q for q in groups['FLOOR_QUEUE']if q['slot']==4);key=(q['frame'],q['cursor'])
 def at(g,tag):return next(q for q in g[tag]if(q['frame'],q['cursor'])==key)
 dma=next(d for d in groups['FLOOR_QUEUE_DISPATCH']if(d['queue_frame'],d['cursor'])==key)
 event=dma['event']
 def d(g):return next(d for d in g['FLOOR_DMA']if d['event']==event)
 cine=lambda g:g['FLOOR_PIT_CONSTRUCTED'][0]
 reject('proxy_cinematic_ID',lambda g:cine(g).update(id=1),'Actual Main+140 cinematic victim')
 reject('detached_cinematic_owner',lambda g:cine(g).update(owner=a^16),'Actual Main+140 cinematic victim')
 reject('wrong_original_victim_ancestry',lambda g:cine(g).update(original=0),'Actual Main+140 cinematic victim')
 reject('wrong_original_constructor_ID',lambda g:next(q for q in g['FLOOR_PIT_NATIVE']if q['entry']==0xff906ef0).update(a0=1),'Original native constructor carries')
 reject('wrong_original_constructor_A11',lambda g:next(q for q in g['FLOOR_PIT_NATIVE']if q['entry']==0xff906ef0).update(a11=0),'Original native constructor carries')
 reject('wrong_own_stream_half',lambda g:g['FLOOR_PIT_LOOKUP'][0].update(low=0),'Actual own stream fetch')
 reject('wrong_native_exit_PC',lambda g:next(q for q in g['FLOOR_PIT_MODE_STORE']if q['before']==9 and q['value']==5).update(pc=0),'Original native movie exit')
 reject('missing_initial_return',lambda g:g['FLOOR_PIT_INITIAL'].pop(),'One actual synchronous preload')
 reject('wrong_initial_pose',lambda g:g['FLOOR_PIT_INITIAL'][1].update(pose=0),'Own cache before original registration')
 reject('clobbered_preload_register',lambda g:g['FLOOR_PIT_INITIAL'][1].update(a7=0),'Actual observed preserved preload registers')
 reject('missing_falling_group',lambda g:g['FLOOR_PIT_DRAW'].remove(next(q for q in g['FLOOR_PIT_DRAW']if q['actor']==a)),'Own initial preload plus twenty falling')
 reject('wrong_falling_cadence',lambda g:next(q for q in g['FLOOR_PIT_DRAW']if q['actor']==a and q['frame']==enter+1).update(frame=enter+2),'Original fall cadence')
 reject('wrong_component_descriptor',lambda g:next(q for q in g['FLOOR_PIT_COMPONENT']if q['actor']==a and q['frame']==enter+1).update(value=0),'Exact native component/terminator')
 reject('wrong_native_palette_ID',lambda g:g['FLOOR_PIT_PALETTE'][0].update(id=1),'Original normal true-ID movie palette')
 reject('wrong_native_palette_color',lambda g:g['FLOOR_PIT_PALETTE'][0].update(colors='0001'+g['FLOOR_PIT_PALETTE'][0]['colors'][4:]),'Every movie constructor palette source color')
 reject('missing_cinematic_completed_field',lambda g:g['FLOOR_BODY'].remove(next(q for q in g['FLOOR_BODY']if q['slot']==4)),'Every actual physical and cinematic completed body field')
 reject('wrong_completed_cinematic_ID',lambda g:next(q for q in g['FLOOR_BODY']if q['slot']==4).update(id=1),'Completed true cinematic identity')
 reject('missing_last_completed_postscreen',lambda g:g['FLOOR_SNAP'].pop(),'Every movie and thirty later fields retained')
 def persistent(g):
  rec=next(q for q in g['FLOOR_ALL_QUEUE']if q['frame']==clear and q['actor']==a)
  rec.update(id=movie['actualID'],pose=model.art.group and proof['actualMoviePoses'][-1])
 reject('persistent_private_Pit_body',persistent,'Own Pit body still published')
 reject('missing_cinematic_FIFO_inventory',lambda g:g['FLOOR_ALL_QUEUE'].remove(at(g,'FLOOR_ALL_QUEUE')),'All native publications bound')
 reject('wrong_FIFO_source',lambda g:at(g,'FLOOR_ALL_QUEUE').update(source=q['source']+8),'All native publications bound')
 reject('wrong_transform_actor',lambda g:at(g,'FLOOR_QUEUE_TRANSFORM').update(actor=0),'Actual actor-owned world transform')
 reject('shifted_native_camera_Y',lambda g:at(g,'FLOOR_QUEUE_TRANSFORM').update(camera=at(g,'FLOOR_QUEUE_TRANSFORM')['camera']+65536),'Native actual queued camera/flip/cache projection')
 reject('shifted_cache_offset',lambda g:at(g,'FLOOR_QUEUE_PART').update(dy=999),'Source descriptors equal every actual native cache')
 reject('shifted_native_DMA_Y',lambda g:d(g).update(y=d(g)['y']+1),'Exact native DMA/cache/palette')
 reject('cinematic_DMA_hidden_as_scenery',lambda g:d(g).update(slot=0),'Actual FIFO dispatch including cinematic victim')
 reject('wrong_gender_group',lambda g:next(q for q in g['FLOOR_PIT_NATIVE']if q['entry']==0xffa12530 and q['frame']==movie['impact']and q['a0']in(0xcc,0xce)).update(a0=0xcc if movie['actualID']==18 else 0xce),'Actual native impact and male/female voice groups')
 reject('wrong_native_gender_selector',lambda g:next(q for q in g['FLOOR_PIT_NATIVE']if q['entry']==0xffa12210 and q['frame']==movie['impact']).update(a1=0),'True native gender selector')
 reject('wrong_native_impact_sound_byte',lambda g:next(q for q in g['FLOOR_SOUND']if q['frame']==movie['impact']and q['a8']==a).update(value=0xff03),'Actual native serialized impact and gender-correct commands')
 reject('wrong_native_shake_arguments',lambda g:next(q for q in g['FLOOR_PIT_NATIVE']if q['entry']==0xff9e1290 and q['frame']==movie['impact']).update(a11=0),'Original five-step/five-pixel shake')
 reject('wrong_native_shake_owner',lambda g:next(q for q in g['FLOOR_PIT_NATIVE']if q['entry']==0xff9e1290 and q['frame']==movie['impact']).update(a8=0),'Original five-step/five-pixel shake')
 model.need(len(tests)==31,'Every declared counterexample executed')
 print(case+' all31specificcorruptions rejected; final full positive recheck without source mocks',flush=True)
 good=model.verify(case)
 model.need(good['passed']and all(good[k]==proof[k]for k in('sampledFrames','exactReplayedFrames','exactHeldScanouts','exactScreenPixels','continuousErase','movie','audioInventory','fullOwnPaletteChecks')),'Full unmodified independent recheck')
 pins.update(good['inputHashes']);model.launch.module_pins(pins)
 return dict(passed=True,case=case,rejectedCounterexamples=len(tests),tests=tests,unchangedInMemoryControlPassed=True,
  unmodifiedFullSceneRechecked=True,unexpectedErrorsAcceptedAsRejection=False,inputHashes=pins,gameOrCaptureBytesChanged=False,
  waveformFidelityAcceptance=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=tuple(model.CASES));p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 model.need(not args.output.exists(),'Immutable evidence only')
 try:report=run(args.case)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('passed','error','case','rejectedCounterexamples','unchangedInMemoryControlPassed')if k in report}),flush=True)
 raise SystemExit(0 if report['passed']else 1)
