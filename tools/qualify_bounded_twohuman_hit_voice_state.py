"""True P1 voice owner retires and loaded cry stops early after real hit."""
import copy,json,re,wave
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    rows=[];states=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if line.startswith(('MK2_HSPECIAL_FIELD ','MK2_HSPECIAL_INPUT ')):states.append(line.strip())
            if line.startswith('MK2_HSPECIAL_'):rows.append((line.split(' ',1)[0],dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows,states

def gate(rows,length):
    owners=[r for tag,r in rows if tag=='MK2_HSPECIAL_VOICE_OWNER' and r['slot']=='1']
    active=[r for r in owners if r['actor']!='00000000'];assert active
    assert all(r['actor']=='01034E90' and r['main']=='0106A370' and r['health']=='161' and r['id']=='18' and r['mode']=='2' for r in active)
    after=[r for r in owners if int(r['frame'])>=1392];assert len(after)>200
    assert all(all(int(r[k],16 if k in ('actor','main') else 10)==0 for k in ('actor','main','health','id','mode')) for r in after)
    hits=[r for tag,r in rows if tag=='MK2_HSPECIAL_HEALTH' and r['slot']=='1' and r['before']=='161' and r['after']=='121'];assert len(hits)==1
    assert hits[0]['frame']=='1391' and hits[0]['pc']=='FF836700'
    assert 0<Decimal(after[0]['seconds'])-Decimal(hits[0]['seconds'])<Decimal(1)/60
    cry=[r for tag,r in rows if tag=='MK2_HSPECIAL_VOICE_CHANNEL' and r['channel']=='11' and int(r['length'])>0]
    assert all(int(r['length'])==length and r['paused']==r['loop']=='0' for r in cry)
    pre=[r for r in cry if int(r['frame'])<1392];post=[r for r in cry if int(r['frame'])>=1392]
    assert pre and post and max(Decimal(r['pos']) for r in pre)>min(Decimal(r['pos']) for r in pre)
    assert all(r['pos']=='3174.00000000' for r in post) and 0<3174<length
    assert Decimal(post[-1]['seconds'])>Decimal(hits[0]['seconds'])+Decimal('1.5')
    return dict(hitSeconds=hits[0]['seconds'],firstClearedOwnerSeconds=after[0]['seconds'],stoppedCrySample=3174,unplayedCrySamples=length-3174,postStopObservations=len(post))

def main():
    folder=sync.ROOT/'audit_bounded_twohuman_hit_voice_state_runtime'
    base=sync.ROOT/'audit_bounded_twohuman_crouched_early_punch_runtime'
    out=folder/'voice_state_check.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    proof=sync.ROOT/'audit_bounded_twohuman_crouched_counters_checked/report.json'
    checked=json.loads(proof.read_text());assert checked['passed'] and sync.sha(base/'run.log')==checked['results']['early_punch']['logSHA256']
    rows,states=load(folder);_,old=load(base);assert states==old
    clip=sync.ROOT/'samples/mk2ks/sonya_bicycle_cry.wav'
    with wave.open(str(clip)) as wav:length=wav.getnframes();assert wav.getframerate()==48000
    positive=gate(rows,length);faults=[]
    for label in ('lingering_owner','advancing_cry'):
        bad=copy.deepcopy(rows)
        if label=='lingering_owner':next(r for tag,r in bad if tag=='MK2_HSPECIAL_VOICE_OWNER' and r['slot']=='1' and int(r['frame'])>=1392)['actor']='01034E90'
        else:next(r for tag,r in bad if tag=='MK2_HSPECIAL_VOICE_CHANNEL' and r['channel']=='11' and int(r['frame'])>=1392)['pos']='3175.00000000'
        try:gate(bad,length)
        except AssertionError:faults.append(label)
        else:raise AssertionError('Retirement fault accepted')
    report=dict(passed=True,**positive,unchangedActualPhysicalInputsAndActors=True,rejectedFaults=faults,
        terminal=terminal,sourceSync=sync.verify(),mixedOutputCleanupAccepted=False,heardCutoffAccepted=False,fullGoalComplete=False,
        pins={str(p):sync.sha(p) for p in (folder/'run.log',base/'run.log',clip,proof,Path(__file__))})
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,**positive)))

if __name__=='__main__':main()
