"""Pre-boot whole-source proof: original cross victim, unchanged native mixing."""
import ast,hashlib,inspect,json,re,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5840_current_cross_tomb_audio_source_checked'

def run():
 import run_current_cross_tomb_audio_v5838 as host
 current.expected()
 parentpath=ROOT/'audit_v5832_current_pressed_tomb_full_scene_matrix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentHeldPressedAndRandomMirrorFullScenesRetained'],'Full existing goal and actual mirror evidence retained')
 priorpath=ROOT/'audit_v5783_current_tomb_winner_mix_source_checked/report.json'
 prior=json.loads(priorpath.read_text());need(prior['passed'],'Original whole enabled model/controller preflight')
 pins=dict(prior['inputHashes']);pins[str(priorpath)]=sha(priorpath);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'Whole authoritative original/current sources intact')
 olddriver=(ROOT/'mk2ks_tomb_mirror_driver_ram_v4340.lua').read_text()
 newdriver=(ROOT/'mk2ks_current_cross_tomb_driver_v5833.lua').read_text()
 # Executable statements retain every old control except the mirror override.
 oldlines=[l for l in olddriver.splitlines()if not l.startswith('--')]
 newlines=[l for l in newdriver.splitlines()if not l.startswith('--')]
 oldlines.remove("replace('local victim_id=id==17 and 18 or 17','local victim_id=id')")
 newlines.remove("assert(source:find('local victim_id=id==17 and 18 or 17',1,true))")
 oldlines[-1]=oldlines[-1].replace('complete3594_true_mirror_ram_only_4340','complete3594_actual_cross_ram_only_5833')
 need(oldlines==newlines,'Whole original3594 controls unchanged; only actual opposite-character selection restored')
 provenance=(ROOT/'mk2ks_tomb_mirror_provenance_ram_v4341.lua').read_text()
 lines=[l for l in provenance.splitlines()if not l.startswith('--')]
 target=[l for l in (ROOT/'mk2ks_current_cross_tomb_provenance_v5834.lua').read_text().splitlines()if not l.startswith('--')]
 need('\n'.join(target)=='\n'.join(lines).replace('mk2ks_tomb_mirror_driver_ram_v4340.lua',
  'mk2ks_current_cross_tomb_driver_v5833.lua').replace('complete3595_true_mirror_pc_qualified_4341',
  'complete3595_actual_cross_pc_qualified_5834'),'Whole actual PC-qualified native provenance retained')
 need((ROOT/host.LUA).read_text()==(ROOT/host.base.LUA).read_text().replace(
  'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_provenance_v5834.lua'),
  'Complete same physical earned campaign and failure-only890 deadline, no new controls')
 observer=(ROOT/host.OBSERVER).read_text()
 need(sha(ROOT/host.OBSERVER)==prior['inputHashes'][str(ROOT/host.OBSERVER)]and
  not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|snapshot\(|force_update|flush\(',observer),
  'Entire unchanged passive native/PCM/ROM/DAC/precise14channel observer')
 need(host.state.contract_source==host.state.native.source and host.state.check_log is host.state.native.check_log and
  host.state.drop_source==inspect.getsource(host.state.native.qualify_drop)and
  host.state.fault_source==inspect.getsource(host.state.original_faults.actual_faults),
  'Entire original3643/1731 cross earned/phase801cleanup contract and real12faults, not mirror admission')
 expected_branch=inspect.getsource(host.branches.original.branch).replace('state=runtime.state','state=cross_state',1).replace(
  "own=17 if fighter=='kano'else 18","own=18 if fighter=='kano'else 17",1)
 need(host.branches.branch.source==expected_branch and host.branches.fault_source==inspect.getsource(host.branches.original.faults),
  'Whole original actual RNG/PC/IO/actor/Main/ceiling/drop/retirement and four fault gates, only victim expectation')
 voice,_=host.branches.voice_models()
 expected_voice=inspect.getsource(host.branches.original_voice.qualify_scream).replace(
  "own=17 if fighter=='kano' else 18","own=18 if fighter=='kano' else 17",1).replace(
  "'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(current.GUEST_SHA),1)
 need(voice.source==expected_voice,'Whole original late victim gender/Main-role/source/RNG/owner gate')
 fn,digest=host.collector();base_fn,_=host.base.collector()
 expected=base_fn.source.replace('audit_v5784_current_tomb_winner_mix_','audit_v5841_current_cross_tomb_winner_mix_').replace(
  host.base.LUA,host.LUA).replace('mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_current_cross_tomb_driver_v5833.lua').replace(
  'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_provenance_v5834.lua')
 before='    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}'
 expected=expected.replace(before,'    files.update(ROOT/p for p in '+repr(host.EXTRA_INPUTS)+')\n'+before,1)
 need(fn.source==expected and fn.__globals__['NAME']==current.NAME and fn.__globals__['state']is host.state and
  fn.__globals__['model']is host.model and fn.__globals__['source'].__file__==__file__,
  'Whole bounded cold4212/4350/5781RAM collector unchanged except output/cross sources and explicit hash inputs')
 need(host.model.float_model().source==host.base.model.float_model().source,
  'Whole native source float resampler/cache retained; source-operation faults added without algorithm change')
 for name in host.EXTRA_INPUTS+(host.LUA,host.OBSERVER,):
  p=ROOT/name
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 for module in (host,host.state.native,host.state.native.legacy,host.branches.original,host.branches.original_voice):
  pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
 need(all(sha(p)==h for p,h in pins.items()),'Whole source preflight stable before actual native boot')
 return dict(passed=True,sourceOnly=True,inputHashes=pins,transportSourceSHA256=digest,
  wholeCrossEarnedContractSHA256=host.state.CONTRACT_SHA256,wholeCrossDropSHA256=host.state.DROP_SHA256,
  wholeCrossBranchSHA256=hashlib.sha256(host.branches.branch.source.encode()).hexdigest().upper(),
  wholeCrossVoiceSHA256=hashlib.sha256(voice.source.encode()).hexdigest().upper(),
  originalFullGoalRemaining=parent['remaining'],actualCurrentCrossTombAccepted=False,
  completeStageVictimAudioAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable cross-source result')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
