"""Full641-field native CPU blade/blocked knife/KO/reset on repaired candidate.

Whole original physical/AI/state/damage/pool/raster criteria stay unchanged.
The old collector's known numeric-word digest serialization is explicitly
matched to all original records before comparison, not a dropped field.
"""
import hashlib,inspect,json,re,traceback
from pathlib import Path
from types import SimpleNamespace
import capture_current_cpu_effect_render_v6348 as original
import native_projectile_identifiers_context_v6509 as candidate
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
FOLDER=ROOT/'audit_v6541_repaired_kano_effects_ram'

def init_model():
 source=inspect.getsource(original.init_model)
 scope=dict(original.init_model.__globals__,terminal=SimpleNamespace(current=candidate))
 exec(compile(source,__file__+'::whole_original_Kano_effect_model_repaired_guest','exec'),scope)
 return scope['init_model']()

def word_to_digest(line):
 word=re.search(r'\bdata=([0-9A-F]{4})(?=\s)',line)
 if not word:return line
 digest=hashlib.sha256(bytes.fromhex(word[1])).hexdigest().upper()
 return line[:word.start()]+'data_sha256='+digest+line[word.end():]

def prepare():
 factory=inspect.getsource(original.main)
 a="return scope['capture']()";need(factory.count(a)==1,'Only prepare whole original terminal-first capture without dispatch')
 factory=factory.replace(a,'return source,scope',1)
 scope=dict(original.__dict__,__file__=__file__,FOLDER=FOLDER,init_model=init_model)
 exec(compile(factory,__file__+'::whole_original_capture_factory','exec'),scope)
 source,bindings=scope['main']()
 a='previous=reader.read()';b="previous='\\n'.join(word_to_digest(l) for l in reader.read().splitlines())"
 need(source.count(a)==1,'Only exact numeric-word/digest baseline representation correction')
 source=source.replace(a,b,1)
 bindings.update(current=candidate,init_model=init_model,word_to_digest=word_to_digest)
 bindings['extra_pins'].update({Path(__file__).resolve(),Path(candidate.__file__).resolve(),Path(original.__file__).resolve(),
                               ROOT/'tools/verify_current_cpu_effect_render_v6354.py',ROOT/'audit_v6535_repaired_candidate_progress/report.json'})
 exec(compile(source,__file__+'::whole_actual_repaired_Kano_effect_capture','exec'),bindings)
 return bindings['capture']

def main(preflight=False):
 need(not FOLDER.exists() and not original.terminal.process_tools.census(),'Fresh native capture, no existing emulator job')
 function=prepare()
 if preflight:
  guest,build,scene,_,_=init_model();need(build==ROOT/candidate.NAME and guest==candidate.expected(),'Exact newly repaired guest/model')
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,candidate=candidate.NAME)),flush=True);return
 return function()

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');a=p.parse_args()
 try:main(a.preflight)
 except Exception as e:
  report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if FOLDER.exists():(FOLDER/'host_failure.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report,indent=2),flush=True);raise SystemExit(1)
