"""Conserve the actual first whole-source EOF checker failure before repair."""
import gzip,json
from pathlib import Path
import native_cpu_finisher_spacing_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha

def preserve(c):
    out=c['folder'];path=out/'first_source_EOF_checker_failure.json'
    need(not path.exists(),'Fresh actual failed checker conservation')
    script=ROOT/'tools/qualify_native_current_attract_phase484.py'
    originals=json.loads((out/'report.json').read_text())['inputHashes']
    paths=[Path(p) for p in originals if Path(p).suffix in ('.lua','.py','.cpp','.h','.ps1','.cmd')]
    paths += [script,Path(__file__)]
    with gzip.open(out/'first_source_EOF_failed_executed_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump({str(p.resolve()):dict(sha256=sha(p),text=p.read_text()) for p in paths},f)
    comparison=json.loads((out/'current_native_audio_checked.json').read_text())
    need(comparison['passed'] and comparison['differentChannelSamples']==0 and c['terminal']['nativeExit']==0,
         'Whole actual PCM already exact; failure is the stronger EOF predicate, not game failure')
    report=dict(passed=False,checkerFailure=True,nativeGameFailure=False,
        actualError='ValueError: Actual Square replacement and both complete Bicycle EOFs, with all unused/muted channels idle',
        nativeTerminal=c['terminal'],wholePCMMixStillBitExact=True,comparedStereoFrames=778560,
        failedCheckerSourceSHA256=sha(script),allExecutedOriginalSourceHashes=originals,
        fullPortAcceptance=False,rawMediaFilesWritten=0)
    path.write_text(json.dumps(report,indent=2)+'\n')
    return report
