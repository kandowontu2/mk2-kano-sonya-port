"""Entire5898 finite Pit audio contract, with genuine stock Sub-Zero8.

Retain every native window/channel/DAC/ROM/mixer/packet/port/ADSP predicate
and all29 actual audio plus12 earned faults per physical context. Direct
cinematic ownership is a separate gate; wider audio/RNG/port remains open.
"""
import hashlib,json,traceback
from pathlib import Path
from types import SimpleNamespace
import verify_current_cross_pit_winner_mix_v5898 as predecessor
import run_current_subzero_pit_audio_v5945 as stock_host

ROOT,need,sha=stock_host.ROOT,stock_host.need,stock_host.sha
OUT=ROOT/'audit_v5949_current_subzero_pit_mix_checked'
observed=SimpleNamespace(**vars(stock_host))
observed.runtime=SimpleNamespace(state=stock_host.state)
observed.source=SimpleNamespace(OUT=stock_host.source.OUT,previous=predecessor.observed.source.previous)
channel_scope=dict(predecessor.channel_gate.__globals__,observed=observed)
exec(compile(predecessor.channel_source,__file__+'::entire_native14channel_clock','exec'),channel_scope)
channel_gate=channel_scope['channel_gate']

gate_source=stock_host.once(predecessor.gate.source,"first['victim_id']==str(35-identity)","first['victim_id']=='8'")
gate_scope=dict(predecessor.gate.__globals__,observed=observed,channel_gate=channel_gate)
exec(compile(gate_source,__file__+'::entire5898_original_victim8','exec'),gate_scope)
gate=gate_scope['gate'];gate.source=gate_source

run_source=stock_host.once(predecessor.run.source,'audit_v5897_current_cross_pit_winner_mix_','audit_v5947_current_subzero_pit_mix_')
run_scope=dict(predecessor.run.__globals__,__file__=__file__,__doc__=__doc__,observed=observed,OUT=OUT,gate=gate)
exec(compile(run_source,__file__+'::entire5898_all_actual_faults','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable full genuine stock-victim Pit audio matrix')
 try:
  report=run()
  report.update(actualOriginalVictimID=8,addedCharacterProxy=False,
                whole5898AudioContractRetained=True,cinematicVictimAudioOwnershipAccepted=False,
                allNativePitCuePriorityAndRNGAccepted=False,fullPortAcceptance=False)
  report['inputHashes'][str(Path(predecessor.__file__).resolve())]=sha(predecessor.__file__)
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every whole executed/source/evidence byte intact')
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
