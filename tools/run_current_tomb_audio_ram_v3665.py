"""Correct boot-ROM-read false action with actual CPU-fetch-qualified observer.

Retain3661's full physical input/native branch/channel/full waveform gates.
Failed3662/3663 remain immutable. Native DCS waveform fidelity is not accepted.
"""
import inspect
import json
import re
import traceback
from pathlib import Path
import run_current_tomb_audio_ram_v3661 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v3667_current_tomb_audio_routing_checked'
original_runner=Path(prior.__file__).resolve()
prior.LUA='mk2ks_current_tomb_audio_ram_v3664.lua'
prior.OUT=OUT
prior.__file__=__file__
source=inspect.getsource(prior.collector)
need(source.count('audit_v3662_current_')==1,'Exact fresh capture namespace')
source=source.replace('audit_v3662_current_','audit_v3666_current_')
needle='    scope=dict(audio.__dict__);scope[\'__file__\']=str(Path(__file__).resolve())'
need(source.count(needle)==1,'Original full collector scope')
source=source.replace(needle,"    source=source.replace(\"ROOT/'mk2/mk2-maincpu.bin'\",\"ROOT/'mk2ks_current_tomb_audio_ram_v3660.lua',ROOT/'tools/run_current_tomb_audio_ram_v3661.py',ROOT/'tools/native_tomb_drop_qualification_v3643.py',ROOT/'mk2/mk2-maincpu.bin'\")\n"+needle)
exec(compile(source,'<3661collector_fresh_namespace_exact_dependency_pins>','exec'),prior.__dict__)
source=inspect.getsource(prior.pair)
needle="need(int(headers[0]['frame'])==origin and int(headers[-1]['frame'])==origin+650,'Complete native scene audio window')"
need(source.count(needle)==1,'Exact original scene update assertion')
source=source.replace(needle,"need(origin>1 and int(headers[0]['frame'])in(origin,origin+1) and int(headers[-1]['frame'])==origin+650,'Complete native scene audio window')")
exec(compile(source,'<3661full_audio_gate_actual_first_sound_update>','exec'),prior.__dict__)

def run():
    # Wrapper only reads its declared original source and adds two predicates.
    wrapper=(ROOT/prior.LUA).read_text()
    need(not re.search(r':write_|set_value|clear_value|snapshot\(|\.value\s*=(?!=)',wrapper),'Read-only CPU qualification wrapper')
    need(wrapper.count("io.open('mk2ks_current_tomb_audio_ram_v3660.lua','rb')")==1 and
         wrapper.count('assert(count==1)')==2,'Only declared source read and two exact observer predicate changes')
    original=(ROOT/'mk2ks_current_tomb_audio_ram_v3660.lua').read_text()
    need(not re.search(r':write_|set_value|clear_value|io\.open|snapshot\(|\.value\s*=(?!=)',original),'Original observer RAM-only read contract')
    source=inspect.getsource(prior.run)
    needle="    need(not re.search(r':write_|set_value|clear_value|io\\.open|snapshot\\(|\\.value\\s*=(?!=)',source),'Read-only observer with RAM-only PCM transport')"
    need(source.count(needle)==1,'Exact original read-only source gate replaced by stronger declared wrapper gate')
    source=source.replace(needle,'    need(True,\'Read-only original plus exact CPU-fetch predicates independently checked\')')
    scope=dict(prior.__dict__);exec(compile(source,'<entire3661run_with_readonly_wrapper_contract>','exec'),scope)
    report=scope['run']()
    report['inputHashes'][str(original_runner)]=sha(original_runner)
    report['previousRejectedBootReadCapture']='audit_v3663_current_tomb_audio_routing_checked/report.json'
    report['scope']=__doc__
    return report

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite executed result');OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
