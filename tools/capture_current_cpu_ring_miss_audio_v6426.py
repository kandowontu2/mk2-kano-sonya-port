"""Keep entire6423 collector; executed6422 startup failure remains rejected."""
import argparse,code,inspect,json,traceback
from pathlib import Path
import capture_current_cpu_ring_miss_audio_v6423 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6427_current_cpu_ring_miss_audio_ram'
LUA='mk2ks_current_cpu_ring_miss_audio_v6425.lua'
CHAIN=(LUA,*original.CHAIN)
SCOPE=None


def prepare():
 source=inspect.getsource(original.prepare)
 need(source.count('audit_v6424_current_cpu_ring_miss_audio_ram')==1,'Only actual successor evidence destination differs')
 source=source.replace('audit_v6424_current_cpu_ring_miss_audio_ram','audit_v6427_current_cpu_ring_miss_audio_ram',1)
 scope=dict(original.__dict__,__file__=__file__,OUT=OUT,LUA=LUA,CHAIN=CHAIN)
 exec(compile(source,__file__+'::whole6423_terminal_first_miss_audio','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 global SCOPE
 failed=json.loads((original.OUT/'native_terminal.json').read_text());failure=json.loads((original.OUT/'failure.json').read_text())
 need(failed['nativeExit']==3 and not failed['hostDecodeErrors'] and not failure['passed'] and
      'attempt to call a nil value'in(original.OUT/'stderr.log').read_text(),'Actual original failed startup preserved, not a replay after timeout')
 source=inspect.getsource(original.main)
 scope=dict(original.__dict__,__file__=__file__,OUT=OUT,LUA=LUA,CHAIN=CHAIN,prepare=prepare)
 exec(compile(source,__file__+'::whole6423_preflight_and_native_dispatch','exec'),scope)
 try:return scope['main'](preflight)
 finally:SCOPE=scope.get('SCOPE')


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():original.prior.original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Same naturally terminal native miss capture; full RAM retained, no rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=original.prior.mix))
  raise SystemExit(1)
