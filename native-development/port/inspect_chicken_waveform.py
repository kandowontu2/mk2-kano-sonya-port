"""Bounded sequential overlap diagnostic; prefixes are not full-tail proof."""
import hashlib
import json
from pathlib import Path
import wave
import argparse
import csv
import numpy as np
from scipy.signal import correlate,resample_poly

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
parser=argparse.ArgumentParser()
parser.add_argument('--boundary-reference',action='store_true',
    help='Experimental piecewise-constant boundary averaging; preserves original report')
parser.add_argument('--full-dance',action='store_true',help='Analyze every recorded cue, bounded to fifteen seconds')
parser.add_argument('--model-announcer',action='store_true',help='Include custom announcer differences in full-dance model')
parser.add_argument('--matched-control',action='store_true')
args=parser.parse_args()
assert not args.full_dance or args.boundary_reference
assert not args.model_announcer or args.full_dance
assert not (args.model_announcer and args.matched_control)
def boundary_reference(samples,phase):
    """Average a zero-order-held source over each output sample interval."""
    step=31250/48000
    count=int((len(samples)-phase)//step)
    edges=phase+np.arange(count+1)*step
    indices=np.minimum(edges.astype(np.int64),len(samples)-1)
    integral=np.concatenate(([0.],np.cumsum(samples)))
    values=integral[indices]+(edges-indices)*samples[indices]
    return np.diff(values)/step
event_name='DCS_CHICKEN_MATCHED_EVENTS.json' if args.matched_control else 'DCS_CHICKEN_EVENTS.json'
proof=json.loads((PORT/'generated_dcs'/event_name).read_text())
assert not proof['skippedOrExtraCuesDuringAction']
events=proof['events'] if args.full_dance else [event for event in proof['events'] if event['age']<176]
assert len(events)==(proof['totalCues'] if args.full_dance else 7)
manifest=json.loads((PORT/'generated_dcs/DCS_CHICKEN_INPUTS.json').read_text())
if args.model_announcer:
    events=[dict(event,kind='chicken') for event in events]
    announcer=json.loads((PORT/'generated_dcs/DCS_ANNOUNCER_INPUTS.json').read_text())
    calls={call:clip for clip in announcer['clips'] for call in clip['calls']}
    writes=list(csv.DictReader((BASE/proof['nativeRun']/'native_sound_writes.csv').open()))
    for high,low in zip(writes,writes[1:]):
        code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
        seconds=float(high['seconds'])
        if code in calls and events[0]['seconds']<=seconds<=events[-1]['seconds']:
            variant=len(manifest['clips']);manifest['clips'].append(calls[code])
            events.append(dict(age=int(high['frame'])-proof['events'][0]['frame']+88,
                frame=int(high['frame']),seconds=seconds,variant=variant,kind='announcer',command=code))
    events.sort(key=lambda event:event['seconds'])
references=[]
for clip in manifest['clips']:
    pcm=(BUILD/f'soundp/SNDS/{clip["region"]}.SND').read_bytes()
    assert sha(pcm)==clip['pcmSHA256']
    decoded=(BUILD/f'soundp/SNDS/{clip["region"]}.AUD').read_bytes()
    assert len(decoded)==clip['samples']*2
    samples=np.frombuffer(decoded,dtype='<i2').astype(float)
    references.append(samples if args.boundary_reference else resample_poly(samples,192,125))
begin=round((events[0]['seconds']-.05)*48000)
folders=[BASE/proof[key] for key in ('nativeRun','controlRun')]
with wave.open(str(folders[0]/'native_dcs.wav'),'rb') as native,wave.open(str(folders[1]/'native_dcs.wav'),'rb') as control:
    assert native.getparams()==control.getparams() and native.getframerate()==48000 and native.getnchannels()==1
    native.setpos(begin);control.setpos(begin)
    count=round((events[-1]['seconds']-events[0]['seconds']+1)*48000) if args.full_dance else 144000
    assert count<=15*48000
    # Bounded scene only, never full-match floating point arrays.
    observed=np.frombuffer(native.readframes(count),dtype='<i2').astype(float)-np.frombuffer(control.readframes(count),dtype='<i2').astype(float)
    assert len(observed)==count
residual=observed.copy();results=[];fits=[]
for event in events:
    prefix_length=8192 if event.get('kind')=='announcer' else 4096
    low=max(0,round(event['seconds']*48000)-begin);high=low+4800
    best=None
    for phase in (np.arange(64)/64 if args.boundary_reference else [None]):
        reference=(boundary_reference(references[event['variant']],phase)
                   if phase is not None else references[event['variant']])
        template=reference[:prefix_length]
        # Only the prefix and bounded latency window participate in fitting.
        cross=correlate(residual[low:high+len(template)-1],template,mode='valid',method='fft')
        local=int(np.argmax(np.abs(cross)))
        at=low+local
        segment=residual[at:at+len(template)]
        denominator=np.linalg.norm(template)*np.linalg.norm(segment)
        score=float(abs(cross[local])/denominator) if denominator else 0
        if best is None or score>best[0]:
            best=(score,at,reference,phase)
    score,at,reference,phase=best
    template=reference[:prefix_length]
    segment=residual[at:at+len(template)]
    gain=float(np.dot(segment,template)/np.dot(template,template))
    latency=(begin+at)/48000-event['seconds']
    end=min(len(residual),at+len(reference))
    residual[at:end]-=gain*reference[:end-at]
    fits.append((at,gain,reference))
    results.append(dict(**event,prefixSamples=len(template),prefixCorrelation=score,
                        latencySeconds=latency,gain=gain,sourcePhase=phase))
for index,(at,gain,reference) in enumerate(fits[:6]):
    # Held-out whole reference: gains/alignment were fitted only on4096 samples.
    clean=residual[at:at+len(reference)]+gain*reference
    score=float(abs(np.dot(clean,reference))/(np.linalg.norm(clean)*np.linalg.norm(reference)))
    results[index]['heldOutFullReferenceCorrelation']=score
    assert at+len(reference)<=len(observed)
    results[index]['heldOutFullReferenceMatched']=score>.98
    # Diagnostic only: test whether sub-sample-prefix alignment error explains
    # tails; preserve the original fixed-prefix score and acceptance flag.
    cleaned=residual.copy()
    cleaned[at:at+len(reference)]+=gain*reference
    shifts=[]
    for shift in range(-4,5):
        segment=cleaned[at+shift:at+shift+len(reference)]
        shifts.append((float(abs(np.dot(segment,reference))/(np.linalg.norm(segment)*np.linalg.norm(reference))),shift))
    aligned,shift=max(shifts)
    results[index]['localAlignmentFullCorrelation']=aligned
    results[index]['localAlignmentSamples']=shift
assert all(0<=event['latencySeconds']<.1 for event in results)
report=dict(scope='All recorded dance cue prefixes' if args.full_dance else 'Seven action-phase cluck prefixes after sequential independent prefix fitting',
    nativeRun=proof['nativeRun'],controlRun=proof['controlRun'],events=results,
    allPrefixesAbove098=all(event['prefixCorrelation']>.98 for event in results),
    referenceModel='boundary-average-phase-grid64' if args.boundary_reference else 'scipy-resample-poly',
    actionPrefixMatches=sum(event['prefixCorrelation']>.98 for event in results),
    heldOutFullReferenceMatches=sum(event.get('heldOutFullReferenceMatched',False) for event in results),
    fullClipTailsVerified=False,wholeSceneMixVerified=False,releaseReady=False)
output=('DCS_CHICKEN_FULL_BOUNDARY_DIAGNOSTIC.json' if args.full_dance else
        'DCS_CHICKEN_BOUNDARY_DIAGNOSTIC.json' if args.boundary_reference else 'DCS_CHICKEN_WAVEFORM_DIAGNOSTIC.json')
if args.model_announcer: output='DCS_CHICKEN_ANNOUNCER_BOUNDARY_DIAGNOSTIC.json'
if args.matched_control: output=output.replace('DCS_CHICKEN_','DCS_CHICKEN_MATCHED_')
(PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
