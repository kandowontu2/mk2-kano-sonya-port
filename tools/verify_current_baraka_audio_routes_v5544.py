"""Entire5540 source/voice/packet/fault gate with exact owner-field binding.

Retain5541's observed unrelated-background-packet counterexample. Select
actual queue descendants by actor/task/field as well as time; every original
table/register/word/port/ADSP and effective fault criterion remains intact.
"""
import inspect,json,traceback
from pathlib import Path
import verify_current_baraka_audio_routes_v5540 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FAILURE=ROOT/'audit_v5541_current_baraka_audio_routes_progress/progress.json'
PARENT=prior.OBSERVED
OUT=ROOT/'audit_v5545_current_baraka_audio_routes_qualified'
failure=json.loads(FAILURE.read_text())
need(not failure['passed']and failure['error']=="ValueError('Actual selected native queue reaches one complete packet')",
     'Preserve actual unrelated-background native packet association failure')
source=inspect.getsource(prior.gate)
edits={
 "after=[p for p in packets if float(queue['seconds'])<=float(p['seconds'])<end]":
 "after=[p for p in packets if float(queue['seconds'])<=float(p['seconds'])<end and all(p[k]==call[k]for k in('a8','a13','frame'))]",
 "port=[w for w in writes if float(packet['seconds'])<=float(w['seconds'])<end]":
 "port=[w for w in writes if float(packet['seconds'])<=float(w['seconds'])<end and all(w[k]==call[k]for k in('a8','a13','frame'))]",
}
for before,after in edits.items():
    need(source.count(before)==1,'Only exact actual native actor/task/field descendants, no dropped source criteria')
    source=source.replace(before,after,1)
scope=dict(prior.__dict__)
exec(compile(source,__file__+'.whole5540_source_voice_table_and_native_packet_owner_field_binding','exec'),scope)
gate=scope['gate']
run_source=inspect.getsource(prior.run)
before='for p in(PARENT,OBSERVED,Path(__file__)):'
after='for p in(PARENT,OBSERVED,Path(prior.__file__),FAILURE,Path(__file__)):'
need(run_source.count(before)==1,'Entire original actual pair/fault/storage qualification, executed failed model pinned')
run_source=run_source.replace(before,after,1)
run_scope=dict(prior.__dict__,prior=prior,gate=gate,PARENT=PARENT,OUT=OUT,FAILURE=FAILURE,__file__=__file__)
exec(compile(run_source,__file__+'.entire5540_actual_record_fault_and_storage_qualification','exec'),run_scope)
run=run_scope['run']


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable current original native packet association qualification')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();prior.capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','remaining','newInputHashes','persistentNativeAutomaticExitPNGs')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
