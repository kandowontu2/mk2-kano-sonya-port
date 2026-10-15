"""Keep complete6404 verifier; resolve the actual physical-contract import."""
import inspect,json
from pathlib import Path
import verify_current_cpu_ring_mirror_audio_v6404 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6407_current_cpu_ring_mirror_audio_checked'
FAILURE=ROOT/'audit_v6406_preserved_verifier_import_failure'


def main():
 need(not FAILURE.exists() and not prior.OUT.exists(),'Actual failed6404 output was not created; preserve checker')
 FAILURE.mkdir()
 prior.model.original.prior.original.prior.original.save(FAILURE/'failure.json',dict(passed=False,
  error="AttributeError: module 'capture_current_cpu_ring_mirror_render_v6389' has no attribute 'physical'",
  executedChecker=str(Path(prior.__file__).resolve()),checkerSHA256=sha(prior.__file__),nativeReruns=0))
 source=inspect.getsource(prior.cue_gate)
 before='phase=capture.physical.physical.phase'
 need(source.count(before)==1,'Only physical-contract import reference differs')
 source=source.replace(before,'phase=capture.prior.physical.phase',1)
 scope=dict(prior.__dict__)
 exec(compile(source,__file__+'::whole_mirror_cue_source_gate','exec'),scope)
 scope.update(OUT=OUT,__file__=__file__)
 source=inspect.getsource(prior.main)
 before="Path(original.__file__),ROOT/'samples/mk2ks/sonya_select.wav'"
 after="Path(original.__file__),Path(prior_checker),preserved_failure,ROOT/'samples/mk2ks/sonya_select.wav'"
 need(source.count(before)==1,'Pin executed6404 and actual import failure')
 source=source.replace(before,after,1)
 scope.update(prior_checker=prior.__file__,preserved_failure=FAILURE/'failure.json')
 exec(compile(source,__file__+'::whole_mirror_audio_records_and_faults','exec'),scope)
 return scope['main']()


if __name__=='__main__':main()
