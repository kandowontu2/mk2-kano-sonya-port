"""Bounded single-track native cluck tails; not production overlap-mix approval."""
import hashlib
import math
import json
from pathlib import Path
import sys
import wave
import numpy as np
from scipy.signal import correlate
from chicken_evidence_names import event_filename

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()

def reference(samples,phase):
    step=31250/48000
    edges=phase+np.arange(int((len(samples)-phase)//step)+1)*step
    indices=np.minimum(edges.astype(np.int64),len(samples)-1)
    integral=np.concatenate(([0.],np.cumsum(samples)))
    return np.diff(integral[indices]+(edges-indices)*samples[indices])/step

def correlation(a,b):
    denominator=np.linalg.norm(a)*np.linalg.norm(b)
    return float(abs(np.dot(a,b))/denominator) if denominator else None

def held_out_bounds(template_length,at,search_stop,next_command_sample=None):
    """Exclude every sample inspected by alignment search, not just winner prefix."""
    start=min(template_length,max(4096,search_stop-at))
    stop=template_length
    if next_command_sample is not None:
        stop=min(stop,max(0,next_command_sample-at))
    return start,max(start,stop)

def inspect(track,mirror=False):
    assert track in (1,2,3)
    proof_path=PORT/'generated_dcs'/event_filename(matched=True,track=track,mirror=mirror)
    proof=json.loads(proof_path.read_text())
    assert proof['diagnosticSoundBank'] and proof['audibleTrack']==track
    assert proof['physicalSide']==(2 if mirror else 1)
    manifest_path=PORT/'generated_dcs/DCS_CHICKEN_INPUTS.json'
    manifest=json.loads(manifest_path.read_text())
    paths=[BASE/proof[key]/'native_dcs.wav' for key in ('nativeRun','controlRun')]
    assert all(sha(path)==proof['pins'][str(path)] for path in paths)
    sources=[]
    source_paths=[]
    for clip in manifest['clips']:
        path=BASE/f'mk2-rebuild-main/soundp/SNDS/{clip["region"]}.AUD'
        assert path.stat().st_size==clip['samples']*2
        sources.append(np.frombuffer(path.read_bytes(),dtype='<i2').astype(float))
        source_paths.append(path)
    events=[e for e in proof['events'] if e['track']==track]
    cases=[]
    for index,event in enumerate(events):
        begin=round((event['seconds']-.05)*48000)
        count=round((len(sources[event['variant']])/31250+.2)*48000)
        assert 0<count<48000
        windows=[]
        for path in paths:
            with wave.open(str(path)) as wav:
                assert (wav.getframerate(),wav.getnchannels(),wav.getsampwidth())==(48000,1,2)
                assert begin+count<=wav.getnframes()
                wav.setpos(begin)
                windows.append(np.frombuffer(wav.readframes(count),dtype='<i2').astype(float))
        observed=windows[0]-windows[1]
        low=round(event['seconds']*48000)-begin
        best=None
        for phase in np.arange(64)/64:
            template=reference(sources[event['variant']],phase)
            prefix=template[:4096]
            cross=correlate(observed[low:low+4800+4095],prefix,mode='valid',method='fft')
            local=int(np.argmax(np.abs(cross)));at=low+local
            score=correlation(observed[at:at+4096],prefix)
            if best is None or (score or 0)>best[0]:best=(score or 0,at,phase,template)
        score,at,phase,template=best
        assert at+len(template)<=len(observed)
        gain=float(np.dot(observed[at:at+4096],template[:4096])/np.dot(template[:4096],template[:4096]))
        actual=observed[at:at+len(template)]
        tail=correlation(actual[4096:],template[4096:])
        end_seconds=(begin+at+len(template))/48000
        next_cue=events[index+1]['seconds'] if index+1<len(events) else None
        preempted=next_cue is not None and next_cue<end_seconds
        held_start,held_stop=held_out_bounds(len(template),at,low+4800+4095,
            math.floor(next_cue*48000)-begin if next_cue is not None else None)
        held_actual=actual[held_start:held_stop]
        held_reference=template[held_start:held_stop]
        safe_tail=correlation(held_actual,held_reference) if len(held_actual)>=1024 else None
        cases.append(dict(frame=event['frame'],seconds=event['seconds'],variant=event['variant'],
            sourcePhase=float(phase),latencySeconds=(begin+at)/48000-event['seconds'],
            prefixCorrelation=score,heldOutTailCorrelation=tail,
            tailResidualRMS=float(np.sqrt(np.mean((actual[4096:]-gain*template[4096:])**2))),
            fittedPrefixSamples=4096,heldOutTailSamples=len(template)-4096,
            legacyTailIncludesAlignmentSearchSamples=True,
            disjointPreCommandTailSamples=len(held_actual),
            disjointPreCommandTailCorrelation=safe_tail,
            disjointPreCommandTailAbove098=safe_tail is not None and safe_tail>.98,
            nextSameTrackCommandBeforeReferenceEnd=preempted,
            heldOutTailAbove098=tail is not None and tail>.98 and not preempted))
    report=dict(scope='Diagnostic single-track native playback, independently prefix-fitted clips and held-out tails',
        track=track,physicalSide=proof['physicalSide'],nativeRun=proof['nativeRun'],controlRun=proof['controlRun'],cases=cases,
        cues=len(cases),tailsAbove098=sum(c['heldOutTailAbove098'] for c in cases),
        sourceVariantsObserved=sorted({c['variant'] for c in cases}),
        productionOverlapMixVerified=False,fullPortVerified=False,releaseReady=False,
        limitation='Use disjointPreCommandTail metrics for independent validation: legacy tail metrics include alignment-search samples. Other native voices may preempt a cluck; single-track diagnostics do not certify the production three-track mix.')
    uninterrupted=[c for c in cases if not c['nextSameTrackCommandBeforeReferenceEnd']]
    report.update(uninterruptedCues=len(uninterrupted),sameTrackCommandOverlapCases=len(cases)-len(uninterrupted),
        allUninterruptedTailsAbove098=bool(uninterrupted) and all(c['heldOutTailAbove098'] for c in uninterrupted),
        uninterruptedVariantsObserved=sorted({c['variant'] for c in uninterrupted}))
    report.update(disjointPreCommandTailsEvaluable=sum(c['disjointPreCommandTailCorrelation'] is not None for c in cases),
        disjointPreCommandTailsAbove098=sum(c['disjointPreCommandTailAbove098'] for c in cases))
    evidence=[Path(__file__),PORT/'chicken_evidence_names.py',proof_path,manifest_path,*paths,*source_paths,
              BASE/f'chicken_track{track}_control/QUALIFICATION.json']
    report['pins']={str(p):sha(p) for p in evidence}
    output=f'DCS_CHICKEN_TRACK{track}'+('_MIRROR' if mirror else '')+'_ISOLATED_DIAGNOSTIC.json'
    (PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return {k:v for k,v in report.items() if k not in ('pins','cases')}

if __name__=='__main__':
    assert len(sys.argv) in (2,3) and (len(sys.argv)==2 or sys.argv[2]=='--mirror')
    print(json.dumps(inspect(int(sys.argv[1]),len(sys.argv)==3),indent=2))
