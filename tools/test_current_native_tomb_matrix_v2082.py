"""In-memory adversarial evidence checks for all current native Tomb slots.

No gameplay, ROM, executable, control or captured artifact is changed. Raw
source reconstruction can be reused for copy-only counterexamples only after
preflight hashes are verified; the final positive recheck uses no source mocks.
"""
import argparse,json,re
from pathlib import Path
from unittest.mock import patch
import verify_current_native_tomb_matrix_v2080 as model
ROOT=model.ROOT

def run(case_name):
 fighter,side,leaf=model.CASES[case_name];CASE=ROOT/leaf
 proofpath=ROOT/f'audit_v2080_current_{case_name}_tomb_matrix_checked/report.json'
 proof=json.loads(proofpath.read_text());assert proof['passed']and not proof['fullPortAcceptance']
 pins=dict(proof['inputHashes'])
 for file,wanted in pins.items():assert model.launch.sha(file)==wanted
 pins[str(proofpath)]=model.launch.sha(proofpath)
 groups,buffers,a,b,owners=model.raster.data(CASE)
 queue=next(q for q in groups['FLOOR_QUEUE']if q['slot']==side and q['part']==0)
 key={k:queue[k]for k in('frame','cursor')}
 dispatched=next(d for d in groups['FLOOR_QUEUE_DISPATCH']if d['cursor']==key['cursor']and d['queue_frame']==key['frame'])
 event=dispatched['event'];shadow_event=groups['SHADOW_COMPONENT'][0]['event'];tests=[]
 origin=groups['FLOOR_BEGIN'][0]['origin'];end=groups['FLOOR_RETIRED'][0]['frame']
 transition=min(r['frame']for r in groups['FLOOR_STATE']if r['mode']==3)
 victim_id=17 if fighter=='sonya'else 18
 def row(g,tag,where):
  found=[r for r in g[tag]if all(r.get(k)==v for k,v in where.items())]
  assert len(found)==1,(tag,where,len(found));return found[0]
 q=lambda g:row(g,'FLOOR_QUEUE',key)
 t=lambda g:row(g,'FLOOR_QUEUE_TRANSFORM',key)
 inv=lambda g:row(g,'FLOOR_ALL_QUEUE',key)
 d=lambda g:row(g,'FLOOR_DMA',{'event':event})
 sh=lambda g:row(g,'FLOOR_DMA',{'event':shadow_event})
 # Actual immutable source bytes, graphics and their pins are preflighted
 # once. These mocks only avoid rebuilding the same unchanged source for
 # every in-memory counterexample; native contracts and all capture checks
 # execute normally. No source mutation is among these tests.
 source_pins=model.launch.source_pins()
 expected=model.launch.current.expected()
 graphics_pins={};image=model.graphics.graphics(graphics_pins)
 def graphics(p):p.update(graphics_pins);return image
 def reject(name,change):
  mutated={tag:[dict(r)for r in rows]for tag,rows in groups.items()}
  change(mutated);variant=(mutated,buffers,a,b,owners)
  with patch.object(model.raster,'data',return_value=variant),patch.object(model.raster.base,'data',return_value=variant),patch.object(model.shadow,'data',return_value=variant),\
       patch.object(model.launch,'source_pins',side_effect=lambda:dict(source_pins)),patch.object(model.launch.current,'expected',return_value=expected),patch.object(model.graphics,'graphics',side_effect=graphics):
   try:model.verify(case_name)
   except(AssertionError,ValueError,KeyError,IndexError)as error:
    tests.append(dict(name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
   else:raise AssertionError('Accepted corrupted native Tomb evidence '+case_name+': '+name)
  print(case_name+' rejected '+name+' ('+str(len(tests))+')',flush=True)
 reject('proxy_performer_ID',lambda g:q(g).update(id=1))
 reject('detached_performer_owner',lambda g:q(g).update(owner=queue['actor']^16))
 reject('invented_floor_anchor',lambda g:row(g,'FLOOR_BODY',{'frame':origin+1,'slot':3-side}).update(floor=999))
 reject('wrong_postfight_loser_state',lambda g:row(g,'FLOOR_STATE',{'frame':transition}).update({f'state{3-side}':1}))
 reject('Main_global_cleared_before_native_code',lambda g:row(g,'FLOOR_STATE',{'frame':end}).update(main1=0))
 reject('proxy_native_pointer_clear_PC',lambda g:g['FLOOR_POINTER_STORE'][0].update(pc=0xffffde00))
 reject('pointer_clear_delayed',lambda g:g['FLOOR_POINTER_STORE'][0].update(frame=end+1))
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
 reject('retirement_origin_moved',lambda g:g['FLOOR_RESULT'][0].update(retired=end+1))
 reject('held_native_controls_not_released',lambda g:row(g,'FLOOR_PHASE',{'frame':proof['nativeTombBranch']['frame']}).update(io0=0xfffffffe))
 def surviving_body(g):
  item=dict(next(r for r in g['FLOOR_BODY']if r['slot']==side))
  item['frame']=end;g['FLOOR_BODY'].append(item)
 reject('physical_actor_survives_original_retirement',surviving_body)
 log=(CASE/'run.log').read_text(encoding='utf-8-sig')
 real_read=Path.read_text
 def reject_log(name,altered):
  assert altered!=log
  def read(path,*args,**kwargs):
   if path.resolve()==(CASE/'run.log').resolve():return altered
   return real_read(path,*args,**kwargs)
  with patch.object(Path,'read_text',read),patch.object(model.launch,'source_pins',side_effect=lambda:dict(source_pins)),patch.object(model.launch.current,'expected',return_value=expected),patch.object(model.graphics,'graphics',side_effect=graphics):
   try:model.verify(case_name)
   except(AssertionError,ValueError,KeyError,IndexError)as error:
    tests.append(dict(name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
   else:raise AssertionError('Accepted corrupted original Tomb record '+case_name+': '+name)
  print(case_name+' rejected '+name+' ('+str(len(tests))+')',flush=True)
 branch_frame=proof['nativeTombBranch']['frame']
 branch=next(r for r in log.splitlines()if r.startswith(f'MK2_STAGE_PROVENANCE_BRANCH frame={branch_frame} ')and 'entry=FF8EB1A0 'in r)
 altered=re.sub(r'\ba0=[0-9A-F]+','a0=00000032'if proof['nativeTombBranch']['dropped']else'a0=00000019',branch)
 reject_log('wrong_original_RNG_branch_value',log.replace(branch,altered))
 motion=next(r for r in log.splitlines()if r.startswith(f'MK2_STAGE_PROVENANCE_FIELD frame={branch_frame+1} '))
 y=int(dict(re.findall(r'(\w+)=([^\s]+)',motion))['y'])
 reject_log('victim_ceiling_hold_one_pixel_wrong',log.replace(motion,re.sub(r'\by=-?\d+','y='+str(y+1),motion)))
 reject_log('missing_native_motion_field',log.replace(motion+'\n',''))
 reject_log('wrong_native_victim_identity',log.replace(motion,re.sub(r'\bid=\d+','id=1',motion)))
 ko=next(r for r in log.splitlines()if r.startswith('MK2_STAGE_WINDOW ')and 'match=2 'in r)
 reject_log('unearned_Tomb_finish_window',log.replace(ko,ko.replace('damage=322','damage=321')))
 fall_arg=next((r for r in log.splitlines()if r.startswith('MK2_STAGE_PROVENANCE_BRANCH ')and 'entry=FF876650 'in r and int(dict(re.findall(r'(\w+)=([^\s]+)',r))['frame'])>=origin),None)
 if fall_arg:
  reject_log('original_drop_gravity_argument_changed',log.replace(fall_arg,fall_arg.replace('a2=00008000','a2=00009000')))
 else:
  reject_log('held_branch_invents_drop_task',log.replace(branch,branch.replace('entry=FF8EB1A0','entry=FF876650')))
 assert len(tests)==28 and all(r['rejected']for r in tests)
 print(case_name+' all 28 corruptions rejected; rechecking full unmodified scene without source mocks',flush=True)
 good=model.verify(case_name);assert good['passed']
 assert all(good[k]==proof[k]for k in('nativeTombBranch','sampledFrames','exactReplayedFrames','exactScreenPixels','exactOwnedPixels',
  'sourceBoundProjections','fullPhysicalPaletteChecks','nativeShadowCopies','continuousErase','audioInventory'))
 pins.update(good['inputHashes']);model.launch.module_pins(pins)
 return dict(passed=True,case=case_name,rejectedCounterexamples=len(tests),tests=tests,unmodifiedFullSceneRechecked=True,
  immutableSourceReconstructionReuseForCopyOnlyCounterexamples=True,inputHashes=pins,gameOrCaptureBytesChanged=False,
  audioAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('case',choices=tuple(model.CASES));parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args();OUT=args.output
 assert not OUT.exists(),'Never overwrite evidence'
 try:report=run(args.case)
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('passed','case','error','rejectedCounterexamples','unmodifiedFullSceneRechecked')if k in report}),flush=True)
 raise SystemExit(0 if report['passed']else 1)
