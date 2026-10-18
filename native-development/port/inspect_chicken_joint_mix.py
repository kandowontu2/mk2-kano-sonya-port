"""Joint prefix-only fit with a disjoint held-out timeline; diagnostic only."""
import json
from pathlib import Path
import wave
import argparse
import csv
import hashlib
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import lsqr

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main'
parser=argparse.ArgumentParser()
parser.add_argument('--full-dance',action='store_true')
parser.add_argument('--model-announcer',action='store_true')
parser.add_argument('--matched-control',action='store_true')
parser.add_argument('--shared-filter',action='store_true',help='Diagnostic nine-tap shared output filter, trained on prefixes only')
parser.add_argument('--track-preemption',action='store_true',help='Diagnostic replacement at next same-track frozen prefix onset')
args=parser.parse_args()
assert not args.model_announcer or args.full_dance
assert not (args.model_announcer and args.matched_control)
assert not args.shared_filter or (args.full_dance and args.matched_control)
assert not args.track_preemption or (args.full_dance and args.matched_control)
event_name='DCS_CHICKEN_MATCHED_EVENTS.json' if args.matched_control else 'DCS_CHICKEN_EVENTS.json'
events=json.loads((PORT/'generated_dcs'/event_name).read_text())
prior_name='DCS_CHICKEN_FULL_BOUNDARY_DIAGNOSTIC.json' if args.full_dance else 'DCS_CHICKEN_BOUNDARY_DIAGNOSTIC.json'
if args.model_announcer: prior_name='DCS_CHICKEN_ANNOUNCER_BOUNDARY_DIAGNOSTIC.json'
if args.matched_control: prior_name=prior_name.replace('DCS_CHICKEN_','DCS_CHICKEN_MATCHED_')
prior=json.loads((PORT/'generated_dcs'/prior_name).read_text())
manifest=json.loads((PORT/'generated_dcs/DCS_CHICKEN_INPUTS.json').read_text())
assert (events['nativeRun'],events['controlRun'])==(prior['nativeRun'],prior['controlRun'])
fits=prior['events']
assert len(fits)==(events['totalCues']+int(args.model_announcer) if args.full_dance else 7)
if args.model_announcer:
    announcer=json.loads((PORT/'generated_dcs/DCS_ANNOUNCER_INPUTS.json').read_text())
    for fit in fits:
        if fit.get('kind')=='announcer':
            assert fit['variant']==len(manifest['clips'])
            manifest['clips'].append(next(clip for clip in announcer['clips'] if fit['command'] in clip['calls']))
rate=48000
begin=round((fits[0]['seconds']-.05)*rate)
# Stop BEFORE the eighth command, not merely before its inferred sound onset.
end=(round((fits[-1]['seconds']+1)*rate) if args.full_dance
     else int(events['events'][7]['seconds']*rate))
count=end-begin
assert 0<count<rate*15
with wave.open(str(BASE/events['nativeRun']/'native_dcs.wav'),'rb') as a, wave.open(str(BASE/events['controlRun']/'native_dcs.wav'),'rb') as b:
    assert a.getparams()==b.getparams() and a.getframerate()==rate and a.getnchannels()==1
    a.setpos(begin);b.setpos(begin)
    observed=np.frombuffer(a.readframes(count),dtype='<i2').astype(float)-np.frombuffer(b.readframes(count),dtype='<i2').astype(float)
values=[];rows=[];pointers=[0];cue_spans=[]
training=np.zeros(count,dtype=bool)
for index,fit in enumerate(fits):
    clip=manifest['clips'][fit['variant']]
    decoded=(BUILD/f'soundp/SNDS/{clip["region"]}.AUD').read_bytes()
    assert len(decoded)==clip['samples']*2
    samples=np.frombuffer(decoded,dtype='<i2').astype(float)
    step=31250/rate
    phase=fit['sourcePhase']
    n=int((len(samples)-phase)//step)
    edges=phase+np.arange(n+1)*step
    indices=np.minimum(edges.astype(np.int64),len(samples)-1)
    integral=np.concatenate(([0.],np.cumsum(samples)))
    reference=np.diff(integral[indices]+(edges-indices)*samples[indices])/step
    at=round((fit['seconds']+fit['latencySeconds'])*rate)-begin
    assert 0<=at<count
    stop=min(count,at+len(reference))
    if args.track_preemption:
        for later in fits[index+1:]:
            if later['track']==fit['track']:
                next_at=round((later['seconds']+later['latencySeconds'])*rate)-begin
                assert next_at>at
                stop=min(stop,next_at)
                break
    cue_spans.append((at,stop,at+len(reference),fit['prefixSamples']))
    values.extend(reference[:stop-at]);rows.extend(range(at,stop));pointers.append(len(values))
    training[at:min(count,at+fit['prefixSamples'])]=True
# Gains only: phases and latencies stay frozen from the earlier prefix search.
# Include EVERY prefix-search sample in training, excluding it from validation.
columns=csc_matrix((values,rows,pointers),shape=(count,len(fits))).tocsr()
solution=lsqr(columns[training],observed[training],atol=1e-10,btol=1e-10,iter_lim=500)
gains=solution[0]
assert solution[1] in (1,2)
prediction=columns@gains
support=np.asarray(columns.getnnz(axis=1)).ravel()>0
validation=~training & support
assert np.count_nonzero(validation)>4096
def metrics(mask):
    actual=observed[mask];model=prediction[mask];residual=actual-model
    actual_norm=float(np.linalg.norm(actual));model_norm=float(np.linalg.norm(model))
    return dict(samples=int(mask.sum()),
        correlation=float(np.dot(actual,model)/(actual_norm*model_norm)) if actual_norm and model_norm else None,
        actualRMS=float(np.sqrt(np.mean(actual*actual))),
        residualRMS=float(np.sqrt(np.mean(residual*residual))),
        relativeResidualNorm=float(np.linalg.norm(residual)/actual_norm) if actual_norm else None)

shared_filter=None
if args.shared_filter:
    from chicken_shared_filter import fit_shared_filter
    filtered,valid,shared_filter=fit_shared_filter(observed,prediction,training)
    shared_filter['unfilteredTraining']=metrics(training & valid)
    shared_filter['unfilteredValidation']=metrics(validation & valid)
    prediction=filtered;training &= valid;validation &= valid

# No per-cue phase, latency or gain refit: inspect each frozen cue's held-out
# timeline against the existing joint prediction. Overlap cannot identify
# individual voices, and samples used by ANY prefix remain excluded.
overlap=np.asarray(columns.getnnz(axis=1)).ravel()>1
cue_tails=[]
for index,(at,stop,full_stop,prefix) in enumerate(cue_spans):
    mask=np.zeros(count,dtype=bool)
    mask[min(stop,at+prefix):stop]=True
    mask &= validation
    solo=mask & ~overlap
    cue_tails.append(dict(cue=index,variant=fits[index]['variant'],
        fullReferenceWithinObservation=full_stop<=count,
        heldOutJointTimeline=metrics(mask) if mask.any() else None,
        heldOutNonoverlappingTimeline=metrics(solo) if solo.any() else None,
        overlappedHeldOutSamples=int(np.count_nonzero(mask & overlap)),
        individualVoiceTailVerified=False))
report=dict(nativeRun=events['nativeRun'],controlRun=events['controlRun'],
    scope='All recorded cues plus final tail; disjoint timeline validation' if args.full_dance else 'First seven cues, ending before eighth command; disjoint timeline validation',
    frozenPrefixPhaseAndLatency=True,gains=gains.tolist(),solverStop=int(solution[1]),
    solverIterations=int(solution[2]),cueCount=len(fits),sparseNonzeros=int(columns.nnz),
    training=metrics(training),validation=metrics(validation),
    individualClipTailsVerified=False,
    finalReferenceWithinObservation=cue_spans[-1][2]<=count,
    everyReferenceWithinObservation=all(span[2]<=count for span in cue_spans),
    perCueHeldOutTailDiagnostics=cue_tails,
    wholeSceneMixVerified=False,releaseReady=False,
    limitation='Joint model tests overlap, not individual voices or the complete dance; reference phases were selected only on training prefixes.')
if shared_filter:
    report['sharedOutputFilter']=shared_filter
    report['limitation']+=' Optional shared FIR parameters use training prefixes only; no actual mixer/filter mechanism is established.'
announcers=json.loads((PORT/'generated_dcs/DCS_ANNOUNCER_INPUTS.json').read_text())
calls={call:clip['actor']+' '+clip['kind'] for clip in announcers['clips'] for call in clip['calls']}
writes=list(csv.DictReader((BASE/events['nativeRun']/'native_sound_writes.csv').open()))
unmodelled=[]
for high,low in zip(writes,writes[1:]):
    call=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
    seconds=float(high['seconds'])
    if call in calls and begin/rate<=seconds<end/rate and not args.model_announcer and not args.matched_control:
        unmodelled.append(dict(command=call,seconds=seconds,clip=calls[call]))
report['unmodelledCustomAnnouncements']=unmodelled
report['knownCustomAnnouncementsCovered']=not bool(unmodelled)
report['controlEquivalenceProven']=False
report['announcerExplicitlyModelled']=bool(args.model_announcer)
if unmodelled:
    report['limitation']+=' SoundW control lacks these custom announcements; full-window residual is confounded and cannot measure chicken-only correctness.'
output='DCS_CHICKEN_FULL_JOINT_MIX_DIAGNOSTIC.json' if args.full_dance else 'DCS_CHICKEN_JOINT_MIX_DIAGNOSTIC.json'
if args.model_announcer: output='DCS_CHICKEN_ANNOUNCER_JOINT_MIX_DIAGNOSTIC.json'
if args.matched_control: output=output.replace('DCS_CHICKEN_','DCS_CHICKEN_MATCHED_')
if args.shared_filter:output=output.replace('_DIAGNOSTIC.json','_SHARED_FILTER_DIAGNOSTIC.json')
if args.track_preemption:
    output=output.replace('_DIAGNOSTIC.json','_TRACK_PREEMPTION_DIAGNOSTIC.json')
    report['sameTrackReplacementAtFrozenPrefixOnset']=True
    report['limitation']+=' Same-track replacement is a hypothesis; earlier prefix alignments were not refitted, and other native commands are not modelled.'
evidence=[Path(__file__),PORT/'generated_dcs'/event_name,PORT/'generated_dcs'/prior_name,
          PORT/'generated_dcs/DCS_CHICKEN_INPUTS.json',
          BASE/events['nativeRun']/'native_dcs.wav',BASE/events['controlRun']/'native_dcs.wav']
evidence.extend(BUILD/f'soundp/SNDS/{clip["region"]}.AUD' for clip in manifest['clips'])
if args.shared_filter:evidence.append(PORT/'chicken_shared_filter.py')
report['evidenceSHA256']={str(path):hashlib.sha256(path.read_bytes()).hexdigest().upper() for path in evidence}
(PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(report,indent=2,allow_nan=False))
