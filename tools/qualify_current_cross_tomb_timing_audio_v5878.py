"""Whole5839 current audio source preflight, actual ordinary cross timings."""
import ast,hashlib,inspect,json,re,traceback
from pathlib import Path
import qualify_current_cross_tomb_audio_v5839 as original
import find_current_cross_tomb_native_branches_v5872 as search
ROOT,need,sha=original.ROOT,original.need,original.sha
current=original.current
OUT=ROOT/'audit_v5879_current_cross_tomb_timing_audio_source_checked'
previous=original

def once(code,before,after):
 need(code.count(before)==1,'Exactly declared whole source preflight adaptation: '+before)
 return code.replace(before,after,1)

run_source=inspect.getsource(original.run)
run_source=once(run_source,'import run_current_cross_tomb_audio_v5838 as host','import run_current_cross_tomb_timing_audio_v5877 as host')
run_source=once(run_source,'audit_v5832_current_pressed_tomb_full_scene_matrix_progress/progress.json',
 'audit_v5875_current_cross_tomb_native_timing_progress/progress.json')
run_source=once(run_source,"parent['actualCurrentHeldPressedAndRandomMirrorFullScenesRetained']",
 "parent['actualMissingCrossP1HeldAndP2RandomDropStatesAccepted']and parent['priorCurrentCrossObservedPressedAudioAndFullScenesAndAllMirrorBranchesRetained']")
start=run_source.index(" olddriver=(ROOT/'mk2ks_tomb_mirror_driver_ram_v4340.lua')")
end=run_source.index(' need((ROOT/host.LUA)',start)
run_source=run_source[:start]+""" timing=search.preflight()
 need(timing['passed']and timing['physicalCommandWaitOnlyChanged']and timing['nativeRNGStateUntouched'],
  'Whole4453 original cold cross driver and complete PC-qualified provenance source retained')
 prior_cross=ROOT/'audit_v5840_current_cross_tomb_audio_source_checked/report.json'
 prior_cross_report=json.loads(prior_cross.read_text())
 need(prior_cross_report['passed']and all(sha(p)==h for p,h in prior_cross_report['inputHashes'].items()),
  'Whole original5839 actual cross controller, mixer and source gate still intact')
 pins[str(prior_cross)]=sha(prior_cross)
 for p in parent['selectedActualMissingBranchProfiles']:
  need(host.physical_delay(p['fighter'],p['physicalSlot'])==p['physicalCommandDelay']and
   p['nativeBranch']['nativeDrop']==(p['physicalSlot']==2),
   'Four genuine independently earned missing native outcomes, no guessed delay acceptance')
"""+run_source[end:]
run_source=once(run_source,
 "'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_provenance_v5834.lua'),",
 "'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_timing_provenance_v5871.lua'),")
start=run_source.index(' fn,digest=host.collector();base_fn,_=host.base.collector()')
end=run_source.index(' need(fn.source==expected',start)
run_source=run_source[:start]+""" fn,digest=host.collector();base_fn,_=host.original.collector()
 expected=base_fn.source
 changes=(
  ('audit_v5841_current_cross_tomb_winner_mix_','audit_v5880_current_cross_tomb_timing_winner_mix_'),
  (host.original.LUA,host.LUA),
  ("controller='mk2ks_current_cross_tomb_driver_v5833.lua'","controller='mk2ks_current_cross_tomb_timing_driver_v5870.lua'"),
  ("ROOT/'mk2ks_current_cross_tomb_provenance_v5834.lua'","ROOT/'mk2ks_current_cross_tomb_timing_provenance_v5871.lua'"),
  ('    files.update(ROOT/p for p in '+repr(host.original.EXTRA_INPUTS)+')',
   '    files.update(ROOT/p for p in '+repr(host.EXTRA_INPUTS)+')'),
  ("MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder))",
   "MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder),MK2KS_TOMB_COMMAND_DELAY=str(physical_delay(fighter,side)))"),
  ("                if line.startswith(('MK2_NATIVE_DAC_RAM ','MK2_NATIVE_DCS_ROM ')):",
   "                if line.startswith('MK2_TOMB_TIMING_GUEST '):\\n"
   "                    h=fields(line);raw=bytes.fromhex(h.pop('hex'))\\n"
   "                    need(h==dict(frame='1',bytes='1048576')and raw==guest,'Whole additional initialized timing guest independently verified in RAM')\\n"
   "                    log.write('MK2_TOMB_TIMING_GUEST_DIGEST frame=1 bytes=1048576 sha256='+hashlib.sha256(raw).hexdigest().upper()+'\\\\n')\\n"
   "                elif line.startswith(('MK2_NATIVE_DAC_RAM ','MK2_NATIVE_DCS_ROM ')):"),
 )
 for before,after in changes:
  need(expected.count(before)==1,'One independent declared original cold-capture source substitution')
  expected=expected.replace(before,after,1)
"""+run_source[end:]
run_source=once(run_source,"fn.__globals__['model']is host.model and fn.__globals__['source'].__file__==__file__,",
 "fn.__globals__['model']is host.model and fn.__globals__['source'].__file__==__file__ and\n  fn.__globals__['physical_delay']is host.physical_delay and fn.__globals__['__doc__']==host.__doc__,")
run_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,OUT=OUT,search=search)
exec(compile(run_source,__file__+'::whole5839_actual_cross_timing_audio_source','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable timing/source preflight')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
