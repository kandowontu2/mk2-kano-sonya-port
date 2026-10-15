"""Native Square and uppercut activation, no collision credited when absent."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_twohuman_square_counters_observed';assert not out.exists()
    results={}
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_twohuman_square_p{side}_counter_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        data={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_HSPECIAL_'):
                    tag=line.split(' ',1)[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    assert r['writes']=='0' and r['assistance']=='none';data.setdefault(tag,[]).append(r)
        assert 'MK2_HSPECIAL_FAILED' not in data
        fields=data['MK2_HSPECIAL_FIELD'];assert len(fields)==842
        assert all(r['id']==r['roster']==('18' if int(r['slot'])==side else '17') and r['actor']==r['owner'] for r in fields)
        cues=data['MK2_HSPECIAL_CUE'];assert len(cues)==1 and cues[0]['value']=='6B00' and cues[0]['frame']=='1381'
        uppercuts=[r for r in data['MK2_HSPECIAL_ACTION_WRITE'] if r['value']=='0107']
        assert len(uppercuts)==1 and int(uppercuts[0]['slot'])==3-side and uppercuts[0]['pc']=='FF83C340'
        assert not data.get('MK2_HSPECIAL_HEALTH')
        own=[r for r in fields if int(r['slot'])==side]
        assert any(int(r['y'])<int(r['floor']) for r in own)
        results[f'p{side}']=dict(actualSquareVoice=cues[0],nativeUppercut=uppercuts[0],airborneFields=sum(int(r['y'])<int(r['floor']) for r in own),
            noCollisionObserved=True,interruptionAccepted=False,terminal=t,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,contexts=2,collisionObserved=False)))

if __name__=='__main__':main()
