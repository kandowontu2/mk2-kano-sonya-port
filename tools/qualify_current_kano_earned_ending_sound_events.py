"""Seal sparse actual events, not heard mix or complete native DCS waveform."""
import json,re
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_earned_ending_sound_events_runtime'
prior=sync.ROOT/'audit_current_kano_postending_two_coin_join_runtime'
out=sync.ROOT/'audit_current_kano_earned_ending_sound_events_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert not (case/'stderr.log').read_text().strip()
def lines(folder):
    text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
    return [s for s in text.splitlines() if s.startswith('MK2_NAT_CAMPAIGN_')]
actual=lines(case);original=lines(prior)
assert [s for s in actual if not s.startswith('MK2_NAT_CAMPAIGN_ENDING_SOUND_')]==original
def rows(tag):return [dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in actual if s.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
channels=rows('ENDING_SOUND_CHANNEL');words=rows('ENDING_SOUND_WORD')
assert {int(r['channel']) for r in channels}==set(range(19))
assert all(r['writes']=='0' and r['assistance']=='none' for r in channels+words)
attract=int(rows('POST_ENDING_ATTRACT')[0]['frame'])
assert attract>int(rows('ENDING_COMPLETED')[0]['frame'])
page1=[r for r in rows('PICTURE') if r['page']=='1'];page2=[r for r in rows('PICTURE') if r['page']=='2']
assert page1 and page2 and channels and words
transitions={}
for k in range(19):
    group=[r for r in channels if int(r['channel'])==k]
    transitions[str(k)]=dict(records=len(group),activeSamples=sorted({int(r['sample']) for r in group if int(r['sample'])>=0}),lastBeforeAttract=next((r for r in reversed(group) if int(r['frame'])<attract),None))
report=dict(earnedCampaignAndFreshJoinRecordsExactlyPreserved=True,
    endingSoundWords=words,channelSummary=transitions,actualAttractFrame=attract,
    passiveFullEndingWindowObserved=True,heardMixAccepted=False,stockDCSWaveformAccepted=False,
    fullEndingAudioAccepted=False,fullPortAccepted=False,terminal=terminal,
    logSHA256=sync.sha(case/'run.log'),caveat='Scalar guest sound words and sample-channel state only; original DCS music/voices waveform and output mix not recorded or certified.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(recordsPreserved=True,soundWords=len(words),channelRecords=len(channels),attractFrame=attract,heardMixAccepted=False)))
