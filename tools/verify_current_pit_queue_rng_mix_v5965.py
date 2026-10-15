"""Whole5948 matrix for actual5964 passive queue/RNG native captures."""
import json,traceback
from pathlib import Path
from types import SimpleNamespace
import verify_current_subzero_pit_mix_v5948 as prior_matrix
import run_current_pit_queue_rng_v5961 as native_host
ROOT,need,sha=native_host.ROOT,native_host.need,native_host.sha
OUT=ROOT/'audit_v5966_current_pit_queue_rng_mix_checked'
observed=SimpleNamespace(**vars(native_host))
observed.runtime=SimpleNamespace(state=native_host.state)
observed.source=SimpleNamespace(OUT=native_host.source.OUT,previous=prior_matrix.observed.source.previous)
channel_scope=dict(prior_matrix.channel_gate.__globals__,observed=observed)
exec(compile(prior_matrix.predecessor.channel_source,__file__+'::entire14channel_clock','exec'),channel_scope)
channel_gate=channel_scope['channel_gate']
gate_scope=dict(prior_matrix.gate.__globals__,observed=observed,channel_gate=channel_gate)
exec(compile(prior_matrix.gate.source,__file__+'::whole5948_native_window','exec'),gate_scope)
gate=gate_scope['gate'];gate.source=prior_matrix.gate.source
run_source=native_host.once(prior_matrix.run.source,'audit_v5947_current_subzero_pit_mix_','audit_v5964_current_pit_queue_rng_')
run_scope=dict(prior_matrix.run.__globals__,__file__=__file__,__doc__=__doc__,observed=observed,OUT=OUT,gate=gate)
exec(compile(run_source,__file__+'::whole5948_full_audio_and_faults','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable full actual queue/RNG capture audio matrix')
 try:
  report=run();report.update(actualOriginalVictimID=8,whole5948NativeAudioContractRetained=True,
                            actualNativePriorityRNGAccepted=False,fullPortAcceptance=False)
  report['inputHashes'][str(Path(prior_matrix.__file__).resolve())]=sha(prior_matrix.__file__)
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Whole compiled/previous/executed/native proof bytes unchanged')
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
