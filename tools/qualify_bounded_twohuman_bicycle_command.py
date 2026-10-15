"""Prove live physical command, true actors and real outgoing collision."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    folder=sync.ROOT/'audit_bounded_twohuman_bicycle_counter_runtime'
    out=folder/'command_check.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    rows={}
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if line.startswith('MK2_HSPECIAL_'):
                tag=line.split(' ',1)[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                assert r['writes']=='0' and r['assistance']=='none'
                rows.setdefault(tag,[]).append(r)
    assert 'MK2_HSPECIAL_FAILED' not in rows
    assert len(rows['MK2_HSPECIAL_COMMAND'])==len(rows['MK2_HSPECIAL_READY'])==len(rows['MK2_HSPECIAL_COUNTER_TERMINAL'])==1
    fields=rows['MK2_HSPECIAL_FIELD'];assert len(fields)==840
    assert all(r['id']==r['roster']==('18' if r['slot']=='1' else '17') and r['actor']==r['owner'] and r['state']=='1' for r in fields)
    cues=rows['MK2_HSPECIAL_CUE'];assert [r['value'] for r in cues]==['6B01','6B02']
    assert all(int(r['frame'])>int(rows['MK2_HSPECIAL_COMMAND'][0]['frame']) for r in cues)
    hits=[r for r in rows['MK2_HSPECIAL_HEALTH'] if int(r['after'])<int(r['before'])]
    assert len(hits)==1 and hits[0]['slot']=='2' and hits[0]['before']=='161' and hits[0]['after']=='139'
    report=dict(passed=True,trueSonyaP1KanoP2PhysicalFields=840,actualLiveBicycleVoiceLaunch=cues,
        actualOutgoingDamage=hits,incomingInterruptionObserved=False,fullGoalComplete=False,
        terminal=terminal,sourceSync=sync.verify(),logSHA256=sync.sha(folder/'run.log'),checkerSHA256=sync.sha(Path(__file__)))
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,fields=840,outgoingDamage=22,incomingInterruptionObserved=False)))

if __name__=='__main__':main()
