"""Bind actual mode7->2 within-frame launch to genuine CPU instruction tap.

Preserve both prior checker rejections; no global mode-check waiver. The
physical frame sample precedes the real Bicycle choice in round two. Its
independent instruction-time mode and next physical field must both equal2.
"""
import json
from pathlib import Path
import qualify_native_selector_sonya_voice_owner_eof_errors as prior

original=prior.original
failure=prior.failure
phase_failure=prior.OUT/'failure.json'
original.need(json.loads(phase_failure.read_text())['error']==
    "AssertionError('Actual quiet owner identity/health/mode unchanged during each real clip')",
    'Actual within-frame native mode-boundary rejection retained')


def mode_boundary(data,actual,frame):
    mode=actual[frame]['mode']
    if mode=='2':return mode
    original.need(frame==2490 and mode=='7' and actual[frame+1]['mode']=='2',
                  'Only real second-round frame7->2 boundary')
    taps=[r for r in data['MK2_SONYA_CHOICE_EVENT'] if r['frame']==str(frame) and r['kind']=='bicycle']
    original.need(len(taps)==1 and
        tuple(taps[0][k] for k in ('mode','pc','opcode','actor','main','owner','id','roster','state','human_state'))==
        ('2','FFFBC330','C080','010350A0','0106BF30','010350A0','18','18','0','1'),
        'Independent actual instruction-time mode/owners and next physical mode, not synthesized mode2')
    return taps[0]['mode']


source=prior.source
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_voice_owner_eof_errors_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_voice_owner_eof_boundary_checked'"),
    ("'MK2_CPU_ROUND_FIELD ','MK2_CPU_ROUND_HEALTH ')",
     "'MK2_CPU_ROUND_FIELD ','MK2_CPU_ROUND_HEALTH ','MK2_SONYA_CHOICE_EVENT ')") ,
    ("actual[f]['id'],actual[f]['hp'],actual[f]['mode'])==",
     "actual[f]['id'],actual[f]['hp'],mode_boundary(data,actual,f))=="),
    ("for p in (Path(__file__),Path(original.__file__),failure,CAPTURE,",
     "for p in (Path(__file__),Path(prior.__file__),phase_failure,Path(original.__file__),failure,CAPTURE,")):
    original.need(source.count(before)==1,'Only exact within-frame observation/source provenance boundary')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_owner_history_actual_instruction_mode_boundary','exec'))
