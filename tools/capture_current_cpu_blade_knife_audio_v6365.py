"""Retain complete6363 collector; fix its prelaunch module/local name collision."""
import argparse,code,inspect,json,traceback
from pathlib import Path
import capture_current_cpu_blade_knife_audio_v6363 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6366_current_cpu_blade_knife_audio_ram'
SCOPE=None


def prepare():
 source=inspect.getsource(original.prepare)
 changes={
  'Path(phase.__file__)':'Path(phase_source.__file__)',
  'phase=phase,mix=mix,sys=sys,':'phase_source=phase,mix=mix,sys=sys,',
  'audit_v6364_current_cpu_blade_knife_audio_ram':'audit_v6366_current_cpu_blade_knife_audio_ram',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'One exact collector namespace/path repair')
  source=source.replace(before,after,1)
 scope=dict(original.__dict__,__file__=__file__)
 exec(compile(source,__file__+'::whole6363_namespace_repair','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 global SCOPE
 failed=ROOT/'audit_v6364_current_cpu_blade_knife_audio_ram/failure.json'
 failure=json.loads(failed.read_text())
 need(not failure['passed'] and failure['nativeBoots']==0 and failure['hostExitCode']==1,'Preserve actual prelaunch collision')
 parent=json.loads(original.PARENT.read_text())
 need(parent['passed'] and all(sha(p)==h for p,h in parent['inputHashes'].items()),'Whole current renderer proof unchanged')
 need(not OUT.exists() and not original.process_tools.census(),'Fresh observer job and empty actual native process census')
 SCOPE=prepare()
 # The generated function now pins the module under a name distinct from its
 # unchanged local ROM phase; inspect rather than execute a redundant boot.
 need('phase_source'in SCOPE and 'phase_source'in SCOPE['run'].__code__.co_names and
      'phase_source'not in SCOPE['run'].__code__.co_varnames,'No module/local shadowing remains')
 if preflight:
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,modulePinNamespaceChecked=True)),flush=True);return
 return SCOPE['run']('kano',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():original.original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Native terminal; actual PCM/DAC retained in RAM, no native rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=original.mix))
  raise SystemExit(1)
