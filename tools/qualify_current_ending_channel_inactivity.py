"""Existing sparse ending observations: sentinel is not a playing predicate."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
case=root/'audit_current_kano_earned_ending_sound_events_runtime'
prior=root/'audit_current_kano_earned_ending_sound_events_v2_checked/report.json'
old=json.loads(prior.read_text());assert old['logSHA256']==sync.sha(case/'run.log')
rows=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in(case/'run.log').read_text().splitlines()if s.startswith('MK2_NAT_CAMPAIGN_ENDING_SOUND_CHANNEL ')]
def gate(rows):
    selected=[r for r in rows if 72376<=int(r['frame'])<80232]
    answer=[]
    for n in range(19):
        group=[r for r in selected if int(r['channel'])==n]
        assert len(group)==65 and [int(r['frame'])for r in group]==list(range(72480,80161,120))
        assert all(r['paused']==r['loop']=='0'for r in group)
        assert len({r['pos']for r in group})==len({r['length']for r in group})==1
        pos=float(group[0]['pos']);length=int(group[0]['length'])
        classification='never initialized'if length==0 else 'observed terminal position'if pos>=length else 'observed stopped midclip position; pointer not saved'
        if length==0:assert pos==0
        answer.append(dict(channel=n,records=65,firstFrame=72480,lastFrame=80160,position=pos,length=length,classification=classification))
    return answer
channels=gate(rows);faults=[]
for label in ('position advancement','paused channel','loop channel','missing observation'):
    bad=copy.deepcopy(rows);i=next(i for i,r in enumerate(bad)if int(r['frame'])==72600 and r['channel']=='10')
    if label=='position advancement':bad[i]['pos']=str(float(bad[i]['pos'])+1)
    elif label=='paused channel':bad[i]['paused']='1'
    elif label=='loop channel':bad[i]['loop']='1'
    else:bad.pop(i)
    try:gate(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Fault admitted:'+label)
backend=root/'mame-mkp/src/devices/sound/samples.cpp';source=backend.read_text()
assert source.index('chan.source_num = (chan.source_len > 0) ? samplenum : -1;')<source.index('chan.source_len = sample.data.size();')
out=root/'audit_current_ending_channel_inactivity_checked';assert not out.exists();out.mkdir()
report=dict(passed=True,channelObservations=channels,all19ChannelsObservedNonadvancingAt65SparseFields=True,effectiveFaultsRejected=faults,sentinelNotUsedAsPlaybackPredicate=True,priorBroadIdleClaimSuperseded=True,sourcePointerSaved=False,nativeBattleOwnerOrCleanupSaved=False,continuousIntervalSilenceProven=False,heardMixAccepted=False,fullEndingAudioAccepted=False,scope='Existing scalar position/length/nonpaused/nonloop observations every120fields72480..80160 only. No advancing source at those samples; channel10 retains a stopped midclip position. Source pointer/playing predicate and native battle cleanup ownership were not saved, so this does not independently prove continuous silence between snapshots. Historical accepted whole PCM quiet remains separate finite evidence.',logSHA256=sync.sha(case/'run.log'),priorReportSHA256=sync.sha(prior),samplesBackendSHA256=sync.sha(backend))
(out/'report.json').write_text(json.dumps(report,indent=2));print(out)
