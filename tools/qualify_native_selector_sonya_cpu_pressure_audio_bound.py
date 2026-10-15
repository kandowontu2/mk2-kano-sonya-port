"""Preserve actual packet-constructor binding rejection; whole packet body.

The original helper constructs its gate from old.gate; marker assertions are
in that extracted body, not in the helper definition. Bind that entire original
body explicitly. Already exact waveform and actual failure remain immutable.
"""
import json
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_audio as original

original_source=Path(original.__file__)
original_failure=original.OUT/'failure.json'
original_waveform=original.OUT/'waveform.json'
need=original.need
need(json.loads(original_failure.read_text())['error']==
     "ValueError('Only actual true-ID/two-winner packet inventory boundary')" and
     json.loads(original_waveform.read_text())['passed'],
     'Actual full waveform positive and real host constructor-boundary rejection preserved')
source=original_source.read_text()
before='    source=inspect.getsource(startup.packets.packet_gate)'
after='''    source=inspect.getsource(startup.packets.old.gate)
    first=source.index(" packets=audio('PACKET');")
    last=source.index(' return dict(passed=True,',first)
    prefix="def packet_gate(text):\\n records=old.inventory(text)\\n audio=lambda tag:records.get('MK2_MAUDIO_'+tag,[])\\n identity=17\\n ends=audio('RESULT');need(len(ends)==1,'Single original audio terminal');end=ends[0]\\n"
    source=prefix+source[first:last]+" return dict(packets=len(packets),portWrites=len(sounds),nativeDSPReads=len(delivery),trueWinnerMarkers=len(markers))\\n"'''
for before,after in (
    (before,after),
    ('scope=dict(vars(startup.packets),__file__=__file__)',
     'scope=dict(startup.packets.old.gate.__globals__,old=startup.packets.old,__file__=__file__)'),
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_audio_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_audio_bound_checked'"),
    ('Path(__file__),PARENT,Path(winners.__file__),',
     'Path(__file__),original_source,original_failure,original_waveform,PARENT,Path(winners.__file__),')):
    need(source.count(before)==1,'Only exact actual packet-body constructor/source preservation boundary')
    source=source.replace(before,after,1)
exec(compile(source,str(original_source)+'::whole_original_packet_body_explicit_binding','exec'))
