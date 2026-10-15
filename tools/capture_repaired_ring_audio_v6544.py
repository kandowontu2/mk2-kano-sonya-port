"""Same complete source-native Ring DAC/PCM/ROM/winner mix on repaired build.

Full original639-field audio window, source waveform prediction and fault gates
are retained. No timing/gain fitting, guest writes, audio flushing or raw files.
"""
import argparse,code,inspect,json,sys,traceback,types
from pathlib import Path
from types import SimpleNamespace
import capture_current_cpu_ring_audio_v6384 as original
import capture_repaired_ring_render_v6536 as rendered
ROOT,need,sha=rendered.ROOT,rendered.need,rendered.sha
OUT=ROOT/'audit_v6545_repaired_ring_hit_audio_ram'
PARENT=ROOT/'audit_v6539_repaired_ring_hit_checked/report.json'
physical=SimpleNamespace(**dict(original.physical.__dict__,FOLDER=rendered.folder('hit')))
state=types.FunctionType(original.state.__code__,dict(original.state.__globals__,physical=physical),original.state.__name__)
SCOPE=None

def prepare():
 source=inspect.getsource(original.prepare)
 before='audit_v6385_current_cpu_ring_audio_ram';need(source.count(before)==1,'Only fresh immutable repaired audio destination')
 source=source.replace(before,'audit_v6545_repaired_ring_hit_audio_ram',1)
 scope=dict(original.__dict__,__file__=__file__,physical=physical,PARENT=PARENT,state=state)
 exec(compile(source,__file__+'::whole_original_native_audio_capture_factory','exec'),scope)
 result=scope['prepare']();result.update(current=rendered.candidate,physical=physical,state=state)
 return result

def main(preflight=False):
 global SCOPE
 need(not OUT.exists() and not original.process_tools.census(),'Fresh actual native audio process, no conflicting game')
 parent=json.loads(PARENT.read_text());need(parent['passed'] and all(sha(k)==h for k,h in parent['inputHashes'].items()),
                                         'Whole actual repaired physical/raster proof intact')
 SCOPE=prepare()
 if preflight:
  guest=rendered.candidate.expected();need(physical.full_phase(original.gzip.open(physical.FOLDER/'run.log.gz','rt').read(),guest)['ring']['acceptedRings'][0]==parent['phase'],
      'Exact repaired phase and whole original source-native sound capture binding')
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,candidate=rendered.candidate.NAME)),flush=True);return
 return SCOPE['run']('sonya',2)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');p.add_argument('--hold',action='store_true');a=p.parse_args()
 try:main(a.preflight)
 except Exception as e:
  failure=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():original.original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if a.hold and SCOPE and 'LAST_CAPTURE' in SCOPE:
   code.interact(banner='Same naturally terminal native game; actual PCM/DAC remain in RAM, no replay.',local=dict(capture=SCOPE['LAST_CAPTURE'],scope=SCOPE,module=__import__(__name__)))
  raise SystemExit(1)
