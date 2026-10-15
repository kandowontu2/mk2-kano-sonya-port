"""Real crouch/uppercut dispatch; earlier version hits after voice launch."""
import json,re
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_twohuman_crouched_counters_checked';assert not out.exists()
    results={}
    for label in ('counter','early_punch'):
        folder=sync.ROOT/f'audit_bounded_twohuman_crouched_{label}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        data={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_HSPECIAL_'):
                    tag=line.split(' ',1)[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    assert r['writes']=='0' and r['assistance']=='none';data.setdefault(tag,[]).append(r)
        fields=data['MK2_HSPECIAL_FIELD'];assert len(fields)==842
        assert all(r['id']==r['roster']==('18' if r['slot']=='1' else '17') and r['actor']==r['owner'] and r['state']=='1' for r in fields)
        actions=data['MK2_HSPECIAL_ACTION_WRITE'];uppercuts=[r for r in actions if r['value']=='0107']
        assert len(uppercuts)==1
        u=uppercuts[0];assert u['before']=='0302' and u['pc']=='FF83C340' and u['mask']=='FFFF' and u['a8']=='010350A0' and u['a13']==u['main']
        cues=data['MK2_HSPECIAL_CUE'];assert [r['value'] for r in cues]==['6B01','6B02']
        hits=[r for r in data['MK2_HSPECIAL_HEALTH'] if int(r['after'])<int(r['before'])];assert len(hits)==1
        h=hits[0];assert h['pc']=='FF836700' and h['before']=='161'
        if label=='early_punch':
            assert h['slot']=='1' and h['after']=='121' and int(h['frame'])==1391
            assert Decimal(cues[-1]['seconds'])<Decimal(h['seconds'])<Decimal(cues[-1]['seconds'])+Decimal('.1')
        else:assert h['slot']=='2' and h['after']=='139'
        results[label]=dict(actualUppercut=u,actualVoiceLaunch=cues,actualCollision=h,
            incomingHitAfterLiveVoiceLaunch=label=='early_punch',voiceOwnerCleanupAccepted=False,
            terminal=terminal,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,nativeUppercutContexts=2,realIncomingDamageAfterLaunch=40,voiceCleanupAccepted=False)))

if __name__=='__main__':main()
