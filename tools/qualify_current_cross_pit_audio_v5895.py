"""Pre-boot entire Pit audio source/namespace and original seven-match contract.
No actual waveform/voice/scene/port acceptance is given by source inspection.
"""
import ast,hashlib,inspect,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5896_current_cross_pit_audio_source_checked'

def run():
 import run_current_cross_pit_winner_mix_v5894 as host
 import qualify_current_cross_tomb_audio_v5839 as cross
 current.expected()
 parentpath=ROOT/'audit_v5890_current_cross_tomb_timing_full_scene_matrix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['allCurrentCrossHeldPressedRandomFullScenesAccepted']and
  parent['allCurrentCrossHeldPressedRandomEnabledAudioRetained'],'Prior complete cross Tomb evidence and full original scope')
 priorpath=cross.OUT/'report.json';prior=json.loads(priorpath.read_text())
 need(prior['passed'],'Whole original source/mixer/controller proof retained')
 pins=dict(prior['inputHashes']);pins[str(priorpath)]=sha(priorpath);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'All actual original passive source/mixer/current compile inputs retained')
 original_observer=(ROOT/host.original.OBSERVER).read_text()
 expected=host.once(original_observer,
  "0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'",
  "0xff8bdde0,0xff8bddef,'actual native Pit audio origin'")
 expected=host.once(expected,'at~=0xff8bdfe0','at~=0xff8bdde0')
 wrapper=(ROOT/host.OBSERVER).read_text()
 # Reconstruct the exact two declared Lua literal replacements independently.
 statements=re.findall(r'replace\((.*?)\)\n',wrapper,re.S)
 pairs=[]
 for statement in statements:
  literals=re.findall(r'([\'"])(.*?)\1',statement,re.S)
  if len(literals)==2:pairs.append(tuple(value for quote,value in literals))
 need(pairs==[("0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'",
  "0xff8bdde0,0xff8bddef,'actual native Pit audio origin'"),('at~=0xff8bdfe0','at~=0xff8bdde0')],
  'Exactly both declared origin-address replacements; no other passive algorithm edits')
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|snapshot\(|force_update|flush\(',expected),
  'Entire15tap/native DAC/wholeROM/raw PCM/14precise channel source stays passive')
 campaign=(ROOT/host.original.LUA).read_text().replace(
  '-- Whole original earned held Tomb campaign; passive full enabled audio.',
  '-- Whole original earned cross campaign; passive full enabled Pit audio.').replace(host.original.OBSERVER,host.OBSERVER)
 need((ROOT/host.LUA).read_text()==campaign,'Whole actual cross controller and failure-only890deadline unchanged')
 need(host.state.check_log is host.state.original.check_log and
  host.state.contract_source==host.state.native.source,'Entire original1731/3643 earned state contract, no narrowed Pit admission')
 expected_fault=host.state.original.fault_source
 expected_fault=expected_fault.replace("check_log('\\n'.join(altered)+'\\n',fighter,side,1,guest=guest)",
  "check_log('\\n'.join(altered)+'\\n',fighter,side,6,guest=guest)",2).replace("'FF8BDFE0'","'FF8BDDE0'",1)
 need(host.state.fault_source==expected_fault and host.state.actual_faults.__globals__['check_log']is host.state.check_log,
  'Whole actual12identity/input/health/parser/action/801cleanup counterexamples, only Pit arena/action target')
 fn,digest=host.collector();oldfn,_=host.original.collector()
 expected_capture=oldfn.source.replace('audit_v5841_current_cross_tomb_winner_mix_',
  'audit_v5897_current_cross_pit_winner_mix_',1).replace(host.original.LUA,host.LUA,1).replace(
  "MK2KS_STAGE_ARENA='1'","MK2KS_STAGE_ARENA='6'",1).replace(
  '    files.update(ROOT/p for p in '+repr(host.original.EXTRA_INPUTS)+')',
  '    files.update(ROOT/p for p in '+repr(host.EXTRA_INPUTS)+')',1)
 need(fn.source==expected_capture and fn.__globals__['state']is host.state and
  fn.__globals__['NAME']==current.NAME and fn.__globals__['model']is host.model and
  fn.__globals__['source'].__file__==__file__ and fn.__globals__['OBSERVER']==host.OBSERVER,
  'Entire canonical4212/4350/5781/5838 cold collector, RAM-only guest/DAC/ROM/PCM, exact Pit namespace')
 need(host.model.float_model().source==host.original.model.float_model().source,
  'Whole native float resampler/cache and original finite source winner mix; raw/source operation faults unchanged')
 for name in host.EXTRA_INPUTS+(host.LUA,host.OBSERVER,):
  path=ROOT/name
  if path.suffix=='.py':ast.parse(path.read_text())
  pins[str(path.resolve())]=sha(path)
 pins[str(Path(__file__).resolve())]=sha(__file__)
 need(all(sha(p)==h for p,h in pins.items()),'All independently bound exact source bytes stable before native boot')
 return dict(passed=True,sourceOnly=True,inputHashes=pins,transportSourceSHA256=digest,
  executedPassiveObserverSHA256=hashlib.sha256(expected.encode()).hexdigest().upper(),
  wholeCrossEarnedContractSHA256=host.state.CONTRACT_SHA256,wholePitEarnedFaultSHA256=host.state.FAULT_SHA256,
  originalFullGoalRemaining=parent['remaining'],actualCurrentPitAudioAccepted=False,
  fullStageArtAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete Pit-source preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
