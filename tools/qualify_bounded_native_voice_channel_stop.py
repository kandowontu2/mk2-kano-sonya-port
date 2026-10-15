"""Read-only saved playback counters: early frozen position after actual hit.

Not a mixed-waveform or subjective listening acceptance claim.
"""
import copy,json,wave
from decimal import Decimal
from pathlib import Path
import check_bounded_native_retained_tap as trace
import qualify_bounded_native_voice_hit_timing as timing
ROOT=trace.ROOT
BASE=ROOT/'audit_bounded_native_voice_channels_runtime'
def gate(rows,length,tick):
    cry=[r for r in rows if r['channel']=='13' and int(r['length'])>0]
    assert cry and all(int(r['length'])==length and r['loop']=='0' and r['paused']=='0' for r in cry)
    before=[r for r in cry if Decimal(r['seconds'])<tick]
    after=[r for r in cry if Decimal(r['seconds'])>tick]
    assert before and len(after)>50
    positions=[Decimal(r['pos']) for r in before]
    assert max(positions)>min(positions),'Actual playback must progress before cleanup'
    stopped=positions[-1]
    assert 0<stopped<length,'Playback did not naturally reach sample EOF'
    assert all(Decimal(r['pos'])==stopped for r in after),'Stopped private channel keeps advancing'
    assert all(int(r['sample'])==0xffffffff for r in after)
    assert Decimal(after[-1]['seconds'])>tick+Decimal('0.5'),'Observe well past natural EOF'
    return dict(channel=13,clipSamples=length,frozenPosition=str(stopped),
        unplayedSourceSamples=str(Decimal(length)-stopped),
        firstPostTimerObservation=after[0]['seconds'],lastObservation=after[-1]['seconds'],
        preCleanupPlaybackAdvanced=True,postCleanupPositionFrozenBeforeEOF=True,
        afterObservations=len(after))
def main():
    out=BASE/'channel_stop_check.json';assert not out.exists()
    terminal=json.loads((BASE/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    current=trace.scan(BASE);previous=trace.scan(timing.BASE)
    assert current['digest']==previous['digest'],'Read-only playback observer changed actual gameplay/owner trace'
    data={k:[] for k in ('MK2_BOUNDED_CUE','MK2_VOICE_OWNER','MK2_BOUNDED_HEALTH_WRITE')};rows=[]
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip();r=dict(timing.RX.findall(line))
            if tag in data:data[tag].append(r);assert len(data[tag])<20000
            elif tag=='MK2_BOUNDED_CHANNEL':rows.append(r);assert len(rows)<2000
    durations={};clip_lengths={}
    for word,name in (('6B01','sonya_bicycle_launch'),('6B02','sonya_bicycle_cry')):
        with wave.open(str(ROOT/'samples/mk2ks'/f'{name}.wav')) as clip:
            assert clip.getframerate()==48000
            clip_lengths[word]=clip.getnframes();durations[word]=Decimal(clip.getnframes())/48000
    owner=timing.gate(data,durations);tick=Decimal(owner['predictedHealthTimerTickSeconds'])
    positive=gate(rows,clip_lengths['6B02'],tick);faults=[]
    for label,change in (
        ('playback_advances_after_stop',lambda r:next(x for x in r if x['channel']=='13' and Decimal(x['seconds'])>tick).update(pos='65113.00000000')),
        ('pause_instead_of_stop',lambda r:next(x for x in r if x['channel']=='13' and Decimal(x['seconds'])>tick).update(paused='1')),
        ('wrong_loaded_clip_length',lambda r:next(x for x in r if x['channel']=='13' and int(x['length'])>0).update(length='66524'))):
        bad=copy.deepcopy(rows);change(bad)
        try:gate(bad,clip_lengths['6B02'],tick)
        except AssertionError:faults.append(label)
        else:raise AssertionError('Channel fault admitted '+label)
        del bad
    assert gate(rows,clip_lengths['6B02'],tick)==positive
    report=dict(passed=True,nativeExit=0,peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        identicalActualGameplayAndOwnerTrace=True,ownerTiming=owner,playbackCounters=positive,
        rejectedFaults=faults,mixedWaveformAccepted=False,subjectiveAudioAccepted=False,
        fullGoalComplete=False,sourceSync=trace.sync.verify(),
        limitation='Saved source_num is -1 even during this first playback; early frozen position, not source_num alone, proves playback ceases',
        hashes={str(p):trace.sync.sha(p) for p in (BASE/'run.log',Path(__file__),ROOT/'samples/mk2ks/sonya_bicycle_cry.wav')})
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,playback=positive,rejectedFaults=faults,mixedWaveformAccepted=False)))
if __name__=='__main__':main()
