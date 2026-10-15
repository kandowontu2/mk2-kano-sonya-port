"""Entire original source cue/ADSP/packet/channel-clock and actual audio faults.

Bind only the new repaired native candidate/capture path. The full DAC/PCM,
sound ROM and waveform prediction proof is required, not substituted by cues.
"""
import argparse,inspect,json,types
from pathlib import Path
from types import SimpleNamespace
import capture_repaired_ring_audio_v6544 as capture_source
import verify_current_cpu_ring_audio_v6386 as original
ROOT,need,sha=capture_source.ROOT,capture_source.need,capture_source.sha
CASE=capture_source.OUT
OUT=ROOT/'audit_v6547_repaired_ring_audio_checked'

def main(preflight=False):
 native=SimpleNamespace(**dict(capture_source.original.original.__dict__,current=capture_source.rendered.candidate))
 capture=SimpleNamespace(**dict(capture_source.original.__dict__,original=native,state=capture_source.state,
                               physical=capture_source.physical,OUT=CASE))
 cue=types.FunctionType(original.cue_gate.__code__,dict(original.cue_gate.__globals__,capture=capture),original.cue_gate.__name__)
 source=inspect.getsource(original.main)
 a='Path(packets.__file__),Path(clocks.__file__),'
 b='Path(original.__file__),Path(capture_source.__file__),Path(packets.__file__),Path(clocks.__file__),'
 need(source.count(a)==1,'Pin original whole gate and actual repaired native audio collector')
 source=source.replace(a,b,1)
 scope=dict(original.__dict__,__file__=__file__,CASE=CASE,OUT=OUT,capture=capture,capture_source=capture_source,original=original,cue_gate=cue)
 exec(compile(source,__file__+'::whole_original_source_cue_delivery_clock_fault_matrix','exec'),scope)
 return scope['main'](preflight)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');a=p.parse_args();main(a.preflight)
