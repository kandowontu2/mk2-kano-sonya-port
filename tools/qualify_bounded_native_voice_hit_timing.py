"""Small saved-log proof of early owner retirement, not audible cutoff proof."""
import copy,json,re,wave
from decimal import Decimal,ROUND_CEILING
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
BASE=ROOT/'audit_bounded_native_close_counter_runtime'
OUT=BASE/'voice_hit_timing_check.json'
RX=re.compile(r'(\w+)=([^\s]+)')
def gate(data,durations):
    cues=data['MK2_BOUNDED_CUE'];owners=[r for r in data['MK2_VOICE_OWNER'] if r['slot']=='2']
    assert [r['word'] for r in cues]==['6B01','6B02']
    hits=[r for r in data['MK2_BOUNDED_HEALTH_WRITE'] if r['slot']=='2' and r['frame']=='2666']
    assert len(hits)==1
    hit=hits[0];hit_time=Decimal(hit['seconds'])
    assert (hit['address'],hit['before'],hit['data'],hit['mask'],hit['pc'])==('01060EC0','161','0087','FFFF','FF836700')
    start=Decimal(cues[0]['seconds'])
    tick=start+((hit_time-start)*60).to_integral_value(rounding=ROUND_CEILING)/60
    active=[r for r in owners if start<Decimal(r['seconds'])<=tick]
    assert active and all(tuple(r[k] for k in ('actor','main','health','id','mode'))==
        ('010350A0','0106BF30','161','18','2') for r in active)
    after=[r for r in owners if Decimal(r['seconds'])>tick]
    assert after and all(all(r[k]=='0' if k in ('health','id','mode') else r[k]=='00000000'
        for k in ('actor','main','health','id','mode')) for r in after)
    first=Decimal(after[0]['seconds']);last=Decimal(active[-1]['seconds'])
    assert last<tick<first and first-hit_time<Decimal(1)/60
    eof={r['word']:Decimal(r['seconds'])+durations[r['word']] for r in cues}
    assert first<max(eof.values()),'Retirement must precede natural end of owned audio'
    return dict(hitSeconds=str(hit_time),predictedHealthTimerTickSeconds=str(tick),
        firstObservedZeroSeconds=str(first),normalClipEOFSeconds={k:str(v) for k,v in eof.items()},
        clearanceObservedWithinOne60HzTick=True,retiredBeforeNaturalEOF=True,
        activeOwnerSnapshotsChecked=len(active),remainingZeroSnapshotsChecked=len(after))
def main():
    assert not OUT.exists()
    terminal=json.loads((BASE/'terminal.json').read_text());assert terminal['exitCode']==0 and not terminal['limitReason']
    data={k:[] for k in ('MK2_BOUNDED_CUE','MK2_VOICE_OWNER','MK2_BOUNDED_HEALTH_WRITE')}
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip()
            if tag in data:
                data[tag].append(dict(RX.findall(line)));assert len(data[tag])<20000
    durations={};clips={}
    for word,name in (('6B01','sonya_bicycle_launch'),('6B02','sonya_bicycle_cry')):
        clip=ROOT/'samples/mk2ks'/f'{name}.wav'
        with wave.open(str(clip)) as wav:
            assert wav.getframerate()==48000
            durations[word]=Decimal(wav.getnframes())/wav.getframerate()
        clips[str(clip)]=sync.sha(clip)
    positive=gate(data,durations);faults=[]
    for label,change in (
        ('wrong_native_damage',lambda d:d['MK2_BOUNDED_HEALTH_WRITE'][next(i for i,r in enumerate(d['MK2_BOUNDED_HEALTH_WRITE']) if r['slot']=='2' and r['frame']=='2666')].update(data='00A1')),
        ('owner_id_changed',lambda d:next(r for r in d['MK2_VOICE_OWNER'] if r['slot']=='2' and r['frame']=='2666' and r['phase']=='frame').update(id='17')),
        ('owner_lingers_after_tick',lambda d:next(r for r in d['MK2_VOICE_OWNER'] if r['slot']=='2' and r['frame']=='2667' and r['phase']=='frame').update(actor='010350A0')),
        ('wrong_launch_time',lambda d:d['MK2_BOUNDED_CUE'][0].update(seconds='40.000000000000'))):
        bad=copy.deepcopy(data);change(bad)
        try:gate(bad,durations)
        except AssertionError:faults.append(label)
        else:raise AssertionError('Counterexample admitted '+label)
        del bad
    assert gate(data,durations)==positive
    report=dict(passed=True,ownerHealthInterruptionTiming=positive,rejectedFaults=faults,
        audibleCutoffAccepted=False,fullGoalComplete=False,sourceSync=sync.verify(),
        sourceClipHashes=clips,logSha256=sync.sha(BASE/'run.log'),checkerSha256=sync.sha(Path(__file__)))
    OUT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,timing=positive,rejectedFaults=faults,audibleCutoffAccepted=False)))
if __name__=='__main__':main()
