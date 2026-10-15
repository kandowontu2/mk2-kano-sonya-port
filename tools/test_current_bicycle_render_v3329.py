"""All original16 real raster/shadow/palette corruptions on current hit capture."""
import builtins
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import verify_current_bicycle_render_erase_v3322 as current
import test_native_cpu_bicycle_round_render_v3136 as tests
ROOT=current.ROOT;OUT=ROOT/'audit_v3330_current_cpu_bicycle_hit_render_counterexamples';need=current.need

def run():
    expected=current.current.expected_current()
    current.current.assembly.NAME=current.current.current.CANDIDATE;current.current.assembly.expected=lambda:expected
    source=inspect.getsource(tests.run)
    substitutions=[
        ("checked=ROOT/f'audit_v3131_native_cpu_bicycle_round_render_{player}_checked/report.json'", "checked=ROOT/'audit_v3323_current_cpu_bicycle_hit_render_erase_checked/report.json'"),
        ("proof=json.loads(checked.read_text());", "proof=json.loads(checked.read_text())['scene'];"),
        ("condition=lines[-1].line or ''", "condition=model.render_condition(lines[-1])"),
    ]
    for before,after in substitutions:
        need(source.count(before)==1,'One declared proof/source-line addressing adaptation')
        source=source.replace(before,after)
    compiled={}
    def compile_capture(text,filename,*args,**kwargs):
        compiled[filename]=text.splitlines()
        return builtins.compile(text,filename,*args,**kwargs)
    def condition(frame):
        if frame.filename in compiled:return compiled[frame.filename][frame.lineno-1]
        return frame.line or ''
    bridge=SimpleNamespace(**vars(current.render.original))
    bridge.CASES={'current_kano':(current.state.CASE,'new','kano')}
    bridge.bicycle=current.state.phase;bridge.model=current.state
    bridge.verify=lambda key:current.render.verify()
    bridge.render_condition=condition
    namespace=dict(vars(tests));namespace['model']=bridge
    exec(compile(source,__file__+'::original16_counterexamples','exec'),namespace)
    with patch.object(current.render,'compile',side_effect=compile_capture,create=True):
        result=namespace['run']()
    need(result['actualCounterexamplesRejected']==16 and result['sameMockedPathPositiveControlAccepted'] and
         result['unrelatedMissingEventExceptionsNeverAccepted'] and result['originalCapturesUnchanged'],'All original actual raster corruptions with same-path positive controls')
    result['inputHashes'][str(Path(__file__).resolve())]=current.current.assembly.sha(__file__)
    result['phaseHorizontalPushAndAudioAccepted']=False
    return result

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite actual counterexamples')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('counterexamples','inputHashes','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
