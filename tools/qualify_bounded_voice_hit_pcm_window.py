"""Bind scalar mixed-output observations to unchanged real interruption trace."""
import json,re
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync
import check_bounded_native_retained_tap as trace

def main():
    folder=sync.ROOT/'audit_bounded_voice_hit_pcm_window_runtime'
    baseline=sync.ROOT/'audit_bounded_native_voice_channels_runtime'
    out=folder/'pcm_window_check.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    assert trace.scan(folder)['digest']==trace.scan(baseline)['digest']
    previous=json.loads((baseline/'channel_stop_check.json').read_text());assert previous['passed']
    assert sync.sha(baseline/'run.log')==previous['hashes'][str(baseline/'run.log')]
    rows=[];stops=[];channels=[];original_channels=[]
    for location,target in ((folder,channels),(baseline,original_channels)):
        with (location/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_BOUNDED_CHANNEL '):target.append(line.strip())
                if location==folder:
                    row=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if line.startswith('MK2_HIT_PCM '):rows.append(row)
                    elif line.startswith('MK2_HIT_PCM_STOP '):stops.append(row)
    assert channels==original_channels and len(stops)==1 and int(stops[0]['updates'])==len(rows)
    assert rows and all(2500<=int(r['frame'])<=2700 and int(r['bytes'])>0 and int(r['bytes'])%4==0 and re.fullmatch('[0-9A-F]{64}',r['sha256']) and r['writes']=='0' and r['raw_media']=='none' for r in rows)
    assert all(Decimal(b['seconds'])-Decimal(a['seconds'])==Decimal('.02') for a,b in zip(rows,rows[1:]))
    hit=Decimal(previous['ownerTiming']['hitSeconds'])
    assert Decimal(rows[0]['seconds'])<hit-1 and Decimal(rows[-1]['seconds'])>hit+Decimal('.5')
    assert sum(int(r['energy']) for r in rows)>0
    report=dict(passed=True,originalGameplayOwnersAndPlaybackCountersUnchanged=True,
        updates=len(rows),bytesHashed=sum(int(r['bytes']) for r in rows),hitSeconds=str(hit),
        lastUpdateSeconds=rows[-1]['seconds'],terminal=terminal,sourceSync=sync.verify(),
        outputWindowObserved=True,isolatedImportedContributionVerified=False,heardCutoffAccepted=False,
        fullGoalComplete=False,logSHA256=sync.sha(folder/'run.log'),checkerSHA256=sync.sha(Path(__file__)),
        baselineStopProofSHA256=sync.sha(baseline/'channel_stop_check.json'))
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','updates','bytesHashed','hitSeconds','heardCutoffAccepted')}))

if __name__=='__main__':main()
