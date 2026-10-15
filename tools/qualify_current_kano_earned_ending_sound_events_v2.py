"""Normalize unsigned idle sentinel; seal external silence separately from DCS."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_earned_ending_sound_events_runtime'
prior=sync.ROOT/'audit_current_kano_earned_ending_sound_events_checked/report.json'
out=sync.ROOT/'audit_current_kano_earned_ending_sound_events_v2_checked'
assert not out.exists()
old=json.loads(prior.read_text());assert old['logSHA256']==sync.sha(case/'run.log')
rows=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in (case/'run.log').read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_ENDING_SOUND_CHANNEL ')]
def sample(r):
    n=int(r['sample']);return n-0x100000000 if n>=0x80000000 else n
def gate(rows):
    window=[r for r in rows if 72376<=int(r['frame'])<80232]
    assert {int(r['channel']) for r in window}==set(range(19))
    assert all(sample(r)==-1 and r['loop']=='0' for r in window)
    return len(window)
count=gate(rows)
bad=copy.deepcopy(rows)
next(r for r in bad if 72376<=int(r['frame'])<80232)['sample']='0'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Stale external playback accepted')
summary={str(k):sorted({sample(r) for r in rows if int(r['channel'])==k and sample(r)>=0}) for k in range(19)}
report=dict(earnedPrefixPreserved=old['earnedCampaignAndFreshJoinRecordsExactlyPreserved'],
    unsignedIdleSentinelNormalized=True,originalSummaryActiveSamplesSuperseded=True,
    endingThroughCreditsExternalChannelsIdle=True,observedIdleChannelRecords=count,
    activeSamplesByChannel=summary,stalePlaybackFaultRejected=True,
    nativeSoundWordsObserved=len(old['endingSoundWords']),fullEndingAudioAccepted=False,
    heardMixAccepted=False,stockDCSWaveformAccepted=False,fullPortAccepted=False,
    logSHA256=old['logSHA256'],priorReportSHA256=sync.sha(prior),terminal=old['terminal'])
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
