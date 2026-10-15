"""Finite true-ID cannonball launch; do not credit absent incoming hit."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_twohuman_kano_ball_counter_observed';assert not out.exists();results={}
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_twohuman_kano_ball_p{side}_counter_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip();rows={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_HSPECIAL_'):
                    tag=line.split(' ',1)[0].removeprefix('MK2_HSPECIAL_');r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    assert r['writes']=='0' and r['assistance']=='none';rows.setdefault(tag,[]).append(r)
        fields=rows['FIELD'];assert len(fields)==842
        assert all(r['id']==r['roster']==('17' if int(r['slot'])==side else '18') and r['actor']==r['owner'] for r in fields)
        cues=rows['CUE'];assert len(cues)==1 and cues[0]['value']=='6B03' and cues[0]['frame']=='1459'
        hits=rows['HEALTH'];assert len(hits)==2 and all(int(r['slot'])==3-side and r['pc']=='FF836700' for r in hits)
        assert [(r['before'],r['after']) for r in hits]==[('161','141'),('141','117')]
        owners=[r for r in rows['VOICE_OWNER'] if int(r['slot'])==side and r['actor']!='00000000']
        assert owners and all(r['id']=='17' for r in owners)
        results[f'p{side}']=dict(actualLiveVoice=cues[0],actualOutgoingHits=hits,trueActorFields=842,
            incomingHitObserved=False,interruptionAccepted=False,terminal=t,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,contexts=2,incomingHitObserved=False)))

if __name__=='__main__':main()
