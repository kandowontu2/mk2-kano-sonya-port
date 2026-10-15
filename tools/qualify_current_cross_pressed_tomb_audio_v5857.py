"""Whole source preflight: opposite victim, real32callback both-Down, exact mix."""
import ast,hashlib,inspect,json,re,traceback
from pathlib import Path
import qualify_current_pressed_tomb_winner_mix_v5792 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
held=original.held
OUT=ROOT/'audit_v5858_current_cross_pressed_tomb_audio_source_checked'

def run():
 import run_current_cross_pressed_tomb_audio_v5856 as host
 host.current.expected()
 parentpath=ROOT/'audit_v5851_current_cross_tomb_full_scene_matrix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentBothCharactersBothSlotsOppositeTombFullSceneGroundShadowEraseAccepted']and
  parent['actualCurrentHeldPressedAndRandomMirrorFullScenesRetained'],'All actual previous scenes/audio and full original objective retained')
 priorpath=original.OUT/'report.json';prior=json.loads(priorpath.read_text())
 need(prior['passed'],'Whole original pressed physical/source/controller/float carrier/14channels preflight')
 pins=dict(prior['inputHashes']);pins[str(priorpath)]=sha(priorpath);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'Entire previously qualified current/native/observer/model sources stable')
 oldlines=[l for l in (ROOT/'mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua').read_text().splitlines()if not l.startswith('--')]
 newlines=[l for l in (ROOT/'mk2ks_current_cross_pressed_tomb_driver_v5852.lua').read_text().splitlines()if not l.startswith('--')]
 oldlines.remove("replace('local victim_id=id==17 and 18 or 17','local victim_id=id')")
 newlines.remove("assert(source:find('local victim_id=id==17 and 18 or 17',1,true))")
 oldlines[-1]=oldlines[-1].replace('complete3594_true_mirror_native_both_Down_4372','complete3594_actual_cross_native_both_Down_5852')
 need(oldlines==newlines,'Entire original3594 health/input/selection/retirement and exact ordinary both-Down, only mirror selection override removed')
 oldlines=[l for l in (ROOT/'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua').read_text().splitlines()if not l.startswith('--')]
 newlines=[l for l in (ROOT/'mk2ks_current_cross_pressed_tomb_provenance_v5853.lua').read_text().splitlines()if not l.startswith('--')]
 need('\n'.join(newlines)=='\n'.join(oldlines).replace('mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua',
  'mk2ks_current_cross_pressed_tomb_driver_v5852.lua').replace('complete4341_pressed_mirror_provenance_4379',
  'complete4341_pressed_actual_cross_provenance_5853'),'Whole PC-qualified read-only branch/motion observer unchanged')
 need((ROOT/host.LUA).read_text()==(ROOT/host.base.LUA).read_text().replace('earned mirror Tomb','earned opposite Tomb').replace(
  'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_current_cross_pressed_tomb_provenance_v5853.lua'),
  'Whole earned/native controller and890failure deadline, no new controls')
 need(sha(ROOT/host.OBSERVER)==prior['inputHashes'][str(ROOT/host.OBSERVER)]and
  not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|snapshot\(|force_update|flush\(',
   (ROOT/host.OBSERVER).read_text()),'Entire original passive full DAC/ROM/PCM/14precisechannel observer unchanged')
 native=host.pressed
 need(native.qualifier_source==inspect.getsource(native.original.qualify_pressed_drop).replace(
  "own=17 if fighter=='kano'else 18","own=18 if fighter=='kano'else 17",1)and
  native.contract_source==native.cross.native.source.replace('qualify_drop(log,fighter,side,arena,case,guest)',
   'qualify_pressed_drop(log,fighter,side,arena,case,guest)',1)and
  native.check_source==inspect.getsource(native.original.check_log)and native.fault_source==native.original.fault_source and
  native.phase_fault_source==inspect.getsource(native.original.pressed_phase_faults),
  'Complete original1731/3643 cross earned/action/801cleanup and4387physical32callback/PC/IO/ceiling-writer/269phase and real negatives')
 expected_fault=inspect.getsource(native.writer_faults.actual_pressed_source_faults).replace(
  'runtime.native.qualify_pressed_drop','qualify_pressed_drop')
 need(native.source_fault_source==expected_fault,'All six original real pressed PC/actor/Main/IO/ceiling value/mask counterexamples retained')
 fn,digest=host.collector();oldfn,_=host.base.collector()
 expected=oldfn.source.replace('audit_v5794_current_pressed_tomb_winner_mix_','audit_v5859_current_cross_pressed_tomb_winner_mix_').replace(
  host.base.LUA,host.LUA).replace('mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua','mk2ks_current_cross_pressed_tomb_driver_v5852.lua').replace(
  'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_current_cross_pressed_tomb_provenance_v5853.lua')
 before='    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}'
 expected=expected.replace(before,'    files.update(ROOT/p for p in '+repr(host.EXTRA_INPUTS)+')\n'+before,1)
 need(fn.source==expected and fn.__globals__['NAME']==host.current.NAME and fn.__globals__['state']is native and
  fn.__globals__['pressed']is native and fn.__globals__['model']is host.model and fn.__globals__['source'].__file__==__file__ and
  host.collector_source==inspect.getsource(host.base.collector),
  'Entire bounded cold RAM/gzip collector retained, only exact output/cross source pins and actual cross state namespace')
 vg,vf=host.voice_models()
 need(vg.source==inspect.getsource(host.cross_voice.original_voice.qualify_scream).replace(
  "own=17 if fighter=='kano' else 18","own=18 if fighter=='kano' else 17",1).replace(
  "'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(host.current.GUEST_SHA),1)and
  vf.__globals__['qualify_scream']is vg and host.model is host.base.model,
  'Whole4394actual female/Main-role/RNG/owner/caller voice and eight original real faults; exact native mix model unchanged')
 for name in host.EXTRA_INPUTS+(host.LUA,host.OBSERVER,):
  p=ROOT/name
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 for module in (host.pressed.cross,host.pressed.native,host.pressed.native.legacy,host.cross_voice):
  pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
 need(all(sha(p)==h for p,h in pins.items()),'All source inputs stable before ordinary native boot')
 return dict(passed=True,sourceOnly=True,inputHashes=pins,transportSourceSHA256=digest,
  wholeEarnedPressedContractSHA256=native.CONTRACT_SHA256,wholeCrossPressedQualifierSHA256=native.QUALIFIER_SHA256,
  actualCrossPressedEnabledAudioAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable pressed-cross source preflight')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
