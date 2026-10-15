"""Actual Square hit and early stopped playback on both human slots."""
import json,re,copy,wave
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync

def gate(rows,side,length):
    fields=rows['FIELD'];assert len(fields)==842
    assert all(r['id']==r['roster']==('18' if int(r['slot'])==side else '17') and r['actor']==r['owner'] for r in fields)
    cues=rows['CUE'];assert len(cues)==1 and cues[0]['value']=='6B00' and cues[0]['frame']=='1381'
    hits=rows['HEALTH'];assert len(hits)==1
    h=hits[0];assert int(h['slot'])==side and h['before']=='161' and h['after']=='121' and h['frame']=='1387' and h['pc']=='FF836700'
    owners=[r for r in rows['VOICE_OWNER'] if int(r['slot'])==side]
    active=[r for r in owners if r['actor']!='00000000'];assert active and all(r['id']=='18' and r['health']=='161' for r in active)
    cleared=[r for r in owners if int(r['frame'])>=1388];assert len(cleared)>200
    assert all(all(int(r[k],16 if k in ('actor','main') else 10)==0 for k in ('actor','main','health','id','mode')) for r in cleared)
    assert 0<Decimal(cleared[0]['seconds'])-Decimal(h['seconds'])<Decimal(1)/60
    channels=[r for r in rows['VOICE_CHANNEL'] if int(r['channel'])==10+(side-1)*2 and int(r['length'])>0]
    assert channels and all(int(r['length'])==length and r['paused']==r['loop']=='0' for r in channels)
    before=[r for r in channels if int(r['frame'])<1388];after=[r for r in channels if int(r['frame'])>=1388]
    assert max(Decimal(r['pos']) for r in before)>min(Decimal(r['pos']) for r in before)
    assert all(r['pos']=='5464.00000000' for r in after) and 0<5464<length
    assert Decimal(after[-1]['seconds'])>Decimal(h['seconds'])+Decimal('1.5')
    return dict(hitSeconds=h['seconds'],firstClearedSeconds=cleared[0]['seconds'],stoppedSample=5464,unplayedSamples=length-5464)

def main():
    out=sync.ROOT/'audit_bounded_twohuman_square_rise_cleanup_checked';assert not out.exists()
    clip=sync.ROOT/'samples/mk2ks/sonya_square_launch.wav'
    with wave.open(str(clip)) as wav:length=wav.getnframes();assert wav.getframerate()==48000
    results={}
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_twohuman_square_p{side}_rise_counter_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip();rows={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_HSPECIAL_'):
                    tag=line.split(' ',1)[0].removeprefix('MK2_HSPECIAL_');r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    assert r['writes']=='0' and r['assistance']=='none';rows.setdefault(tag,[]).append(r)
        positive=gate(rows,side,length);faults=[]
        for label in ('lingering_owner','advancing_playback'):
            bad=copy.deepcopy(rows)
            if label=='lingering_owner':next(r for r in bad['VOICE_OWNER'] if int(r['slot'])==side and int(r['frame'])>=1388)['id']='18'
            else:next(r for r in bad['VOICE_CHANNEL'] if int(r['channel'])==10+(side-1)*2 and int(r['frame'])>=1388)['pos']='5465.00000000'
            try:gate(bad,side,length)
            except AssertionError:faults.append(label)
            else:raise AssertionError('Cleanup fault accepted')
        results[f'p{side}']=dict(**positive,rejectedFaults=faults,terminal=t,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),clipSHA256=sync.sha(clip),mixedOutputAccepted=False,heardQualityAccepted=False,fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,contexts=2,unplayedSamples=length-5464)))

if __name__=='__main__':main()
