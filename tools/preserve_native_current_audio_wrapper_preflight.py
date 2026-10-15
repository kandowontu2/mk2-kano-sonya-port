"""Preserve actual new wrapper guard failure; original native run is untouched."""
import gzip,json
from pathlib import Path
import native_cpu_finisher_spacing_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    out=ROOT/'audit_native_attract_kano_spacing_phase484'
    path=out/'replacement_wrapper_preflight_failure.json'
    source=ROOT/'tools/qualify_native_current_attract_phase484_v2.py'
    need(not path.exists() and not (out/'current_native_audio_checked_v2.json').exists(),'Actual failed wrapper before prediction, never rewrite native result')
    with gzip.open(out/'replacement_wrapper_preflight_executed_source.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(path=str(source),sha256=sha(source),text=source.read_text()),f)
    path.write_text(json.dumps(dict(passed=False,checkerPreflightFailure=True,nativeGameFailure=False,
        observedError='ValueError: Whole original qualification adaptation executed_current_audio_sources.json.gz',
        cause='Whole original qualification references this output name twice, once for write and once for dependency pinning; guard expected one.',
        failedExecutedSourceSHA256=sha(source),newNativeRuns=0,fullPortAcceptance=False),indent=2)+'\n')
    print('Original wrapper preflight failure source preserved; no new game run.')
