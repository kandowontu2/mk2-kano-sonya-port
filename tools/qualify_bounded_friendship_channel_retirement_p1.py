"""Sample channels may retain buffers after ending; pos>=length is idle."""
import json
from qualify_bounded_current_friendships import fields
from qualify_bounded_friendly_rejoin import validate_rejoin
import verify_native_source_sync as sync


def validate_channels(text):
    rows=[fields(line) for line in text.splitlines() if line.startswith('MK2_FRIEND_SAMPLE_CHANNEL')]
    assert rows
    def playing(r): return int(r['length'])>0 and float(r['pos'])<int(r['length']) and r['paused']=='0'
    assert any(playing(r) for r in rows), 'No actual sample-channel activity observed'
    css=int(fields(next(line for line in text.splitlines() if line.startswith('MK2_FRIEND_REJOIN_CSS')))['frame'])
    cleared=[r for r in rows if int(r['frame'])>=css+30]
    assert cleared and all(not playing(r) for r in cleared)
    fresh=[r for r in rows if r['rejoined']=='true']
    assert fresh and all(not playing(r) for r in fresh)
    assert {int(r['channel']) for r in fresh}==set(range(4,10))
    assert all(r['loop']=='0' and r['writes']=='0' and r['assistance']=='none' for r in rows)
    return {'observedRows':len(rows),'activeRows':sum(playing(r) for r in rows),'postSelectionIdleRows':len(cleared),'newMatchIdleRows':len(fresh)}


def run(side):
    sync.verify()
    out=sync.ROOT/f'audit_bounded_friendship_channel_retirement_p{side}_checked'
    assert not out.exists()
    reports=[]
    lua=sync.ROOT/'audit_bounded_friendship_channel_retirement_preparation/channels.lua'
    for fighter in ('kano','sonya'):
        case=sync.ROOT/f'audit_bounded_friendship_channel_retirement_{fighter}_p{side}_runtime'
        baseline=sync.ROOT/f'audit_bounded_rejoin_both_selectors_friendship_{fighter}_p{side}_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<=320*1024**2
        assert terminal['observerSha256'].lower()==sync.sha(lua).lower()
        assert not (case/'stderr.log').read_text().strip()
        text=(case/'run.log').read_text()
        core=[line for line in text.splitlines() if line.startswith('MK2_FRIEND_') and not line.startswith('MK2_FRIEND_SAMPLE_CHANNEL')]
        expected=[line for line in (baseline/'run.log').read_text().splitlines() if line.startswith('MK2_FRIEND_')]
        assert core==expected
        validate_rejoin(text,'MK2_FRIEND_',17 if fighter=='kano' else 18,side)
        result=validate_channels(text)
        broken=text.replace('rejoined=true','rejoined=false')
        try: validate_channels(broken)
        except AssertionError: pass
        else: raise AssertionError('Missing new-match observations accepted')
        reports.append({'fighter':fighter,'side':side,'channelObservations':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finiteChannelRetirementPassed':True,'everyAudioSampleAcceptance':False,'waveformAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print(f'PASS: P{side} real friendship sample-channel activity, idle selection/new match')


if __name__=='__main__': run(1)
