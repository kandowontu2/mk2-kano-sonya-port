"""Whole native continuous KO/round replay, including actual held-buffer targets."""
import inspect,json,textwrap
from pathlib import Path
import current_cpu_scene_ram_contract_v5357 as original
import current_cpu_scene_ram_contract_v5363 as hud
ROOT,need,sha=original.ROOT,original.need,original.sha

def replay_binding(folder,ram,log):
 source=inspect.getsource(original.replay_binding)
 source=source.replace('source=inspect.getsource(raster.base.Replay.begin)','source=textwrap.dedent(inspect.getsource(raster.base.Replay.begin))',1)
 before='namespace=dict(erase.inspect.__globals__,ram=ram,raster=scoped)'
 need(source.count(before)==1,'Whole original native replay read transport binding')
 injected="""extra={
  "'FLOOR_SHIFT_FILL','FLOOR_SHIFT')for row": "'FLOOR_SHIFT_FILL','FLOOR_SHIFT','FLOOR_HELD')for row",
  'checked_pres=checked_flips=loads=fills=transfers=direct=0;shift=None;records=[]': 'checked_held=0;checked_pres=checked_flips=loads=fills=transfers=direct=0;shift=None;records=[]',
  "if kind in('FLOOR_PRE_FRAME','FLOOR_FLIP'):": "if kind in('FLOOR_PRE_FRAME','FLOOR_FLIP','FLOOR_HELD'):",
  "target=row if kind=='FLOOR_PRE_FRAME'else latches[row['event']]": "target=row if kind in('FLOOR_PRE_FRAME','FLOOR_HELD')else latches[row['event']]",
  "checked_pres+=kind=='FLOOR_PRE_FRAME';checked_flips+=kind=='FLOOR_FLIP'": "checked_held+=kind=='FLOOR_HELD';checked_pres+=kind=='FLOOR_PRE_FRAME';checked_flips+=kind=='FLOOR_FLIP'",
  "need(checked_pres==len(groups['FLOOR_PRE_FRAME'])": "need(checked_held==len(groups['FLOOR_HELD']),'Every actual held target continuously compared');need(checked_pres==len(groups['FLOOR_PRE_FRAME'])",
  'return dict(passed=True,continuousExactPreBuffers=checked_pres': 'return dict(passed=True,continuousExactHeldBuffers=checked_held,continuousExactPreBuffers=checked_pres'}
 for before,after in extra.items():
  need(source.count(before)==1,'Only add actual held comparison targets, preserve all original operations: '+before);source=source.replace(before,after,1)
 namespace=dict(erase.inspect.__globals__,ram=ram,raster=scoped)"""
 source=source.replace(before,injected,1)
 namespace=dict(original.replay_binding.__globals__,textwrap=textwrap,__file__=__file__)
 exec(compile(source,__file__+'::entire_original_native_operations_add_held_targets','exec'),namespace)
 return namespace['replay_binding'](folder,ram,log)

def verify(folder,ram,log,guest,pins):
 prior=ROOT/'audit_v5371_current_cpu_square_scene_ram_checked/report.json'
 need(json.loads(prior.read_text())['passed'],'Current whole native one-base scene and complete HUD qualification')
 source=inspect.getsource(original.verify)
 changes={
  'image=graphics.reconstruct(pins);payload=':'image=patch_hud(graphics.reconstruct(pins),pins);payload=',
  "len(snaps)==70 and [r['frame']for r in snaps]==list(range(2279,2349))":"len(snaps)==340 and [r['frame']for r in snaps]==list(range(3001,3341))",
  "for label,target in(('wrong_actual_prebuffer',first_pre),('wrong_actual_displayed_VRAM',first_flip)):":
   "for label,target in(('wrong_actual_prebuffer',first_pre),('wrong_actual_displayed_VRAM',first_flip))+( (('wrong_actual_held_VRAM',groups['FLOOR_HELD'][0]['file']),)if groups['FLOOR_HELD']else() ):"}
 for before,after in changes.items():need(source.count(before)==1,'Entire original scene gate plus explicit round window/held targets');source=source.replace(before,after,1)
 namespace=dict(original.verify.__globals__,patch_hud=hud.patch_hud,replay_binding=replay_binding,__file__=__file__)
 exec(compile(source,__file__+'::entire_original_graphics_CPU_DMA_shift_RGB_KO_round_gate','exec'),namespace)
 report=namespace['verify'](folder,ram,log,guest,pins)
 groups,_,_,_,_=original.parser(log)
 states={r['frame']:r for r in groups['FLOOR_STATE']}
 need(set(states)==set(range(3000,3341)),'Every observed transition state retained, not only combat fields')
 expected_modes={f:2 if f<=3021 or f>=3306 else 5 if f<=3207 else 6 if f==3208 else 7 for f in states}
 # FLOOR_STATE is frame_done, after CPU writes; ROUND_FIELD is the next
 # frame's pre-CPU publication. Bind exactly to that actual callback phase.
 rounds=original.erase.current.ROOT/'audit_v5378_current_cpu_square_audio_ram_samples/run.log'
 import verify_native_extended_cpu_v2946 as ledgers
 health,by=ledgers.health_ledger(log,guest,'kano')
 for f,r in states.items():
  next1,next2=by[f+1,1],by[f+1,2]
  need(r['mode']==next1['mode']==next2['mode']and r['health1']==next1['hp']and r['health2']==next2['hp']and
   r['p1']==next1['actor']and r['p2']==next2['actor']and r['main1']==next1['main']and r['main2']==next2['main']and
   (r['roster1'],r['roster2'])==(17,18)and(r['state1'],r['state2'])==(1,0),'Exact frame_done scene/next pre-CPU physical state and health binding')
 need(set(r['mode']for r in states.values())=={2,5,6,7}and any(r['p1']==r['p2']==0 for r in states.values()),'Actual KO/winner retirement/rebuild/reveal/live contexts captured')
 need(health['earnedKOs'][0]['frame']==3021 and {r['frame']for r in health['actualRoundResets']}=={3208},'Actual original collision KO and native161HP round reset')
 for p in(prior,Path(original.__file__),Path(hud.__file__),Path(__file__)):pins[str(p.resolve())]=sha(p)
 report.update(actualKOFrame=3021,actualNativeRoundResetFrame=3208,nextRoundPreCPUFirstLiveFrame=3306,
  everyFrameDoneStateBoundToNextActualNativePreCPUState=True,allModeSceneFields=len(states),actualHeldFields=len(groups['FLOOR_HELD']),
  completeKOToNextRoundNativeSceneEraseAndRGBWindowAccepted=True,allKOContextsOrArenasOrArtAccepted=False)
 return report
