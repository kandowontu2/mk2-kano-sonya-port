"""Actual paid native join cuts a progressing CPU clip before EOF."""
import copy,json,wave
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_cpu_sonya_active_voice_join_runtime'
out=sync.ROOT/'audit_current_cpu_sonya_active_voice_join_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<=320*1024*1024
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
with wave.open(str(sync.ROOT/'samples/mk2ks/sonya_bicycle_cry.wav')) as wav:length=wav.getnframes()
def gate(records):
    trigger=records['JOIN_TRIGGER'];assert len(trigger)==1 and trigger[0]['id']=='18' and trigger[0]['cue']=='6B01'
    assert all(r['writes']=='0' and r['assistance']=='none' for group in records.values() for r in group)
    assert [(r['button'],int(r['age'])) for r in records['JOIN_INPUT']]==[('Coin_1',n) for n in list(range(1,5))+list(range(41,45))]+[('Start_1',n) for n in range(64,68)]
    cry=[r for r in records['JOIN_CHANNEL'] if r['channel']=='11']
    before=[r for r in cry if r['mode']=='2' and int(r['age'])>=60]
    assert before and all(float(b['pos'])>float(a['pos']) for a,b in zip(before,before[1:]))
    cut=next(r for r in cry if r['mode']=='14')
    assert int(cut['age'])==int(before[-1]['age'])+1
    assert int(cut['length'])==length and 0<float(cut['pos'])<length and cut['pos']==before[-1]['pos']
    tail=[r for r in cry if int(r['age'])>=int(cut['age'])]
    assert len({r['pos'] for r in tail})==1
    for n in (1,2):
        owners=[r for r in records['JOIN_OWNER'] if r['slot']==str(n) and int(r['age'])>=int(cut['age'])]
        assert owners and all(r['actor']==r['main']=='00000000' and r['id']=='0' for r in owners)
    selection=records['JOIN_SELECTION'];done=records['JOIN_COMPLETE'];assert len(selection)==len(done)==1
    assert int(done[0]['frame'])-int(selection[0]['frame'])==160 and not records.get('LOSS')
    assert any(r['mode']=='4' and r['states']=='3,3' for r in records['STATE'] if int(r['frame'])>=int(selection[0]['frame']))
    return dict(trigger=trigger[0],lastActive=before[-1],firstCut=cut,selection=selection[0],completion=done[0],stationaryCryFields=len(tail))
proof=gate(rows)
bad=copy.deepcopy(rows);next(r for r in bad['JOIN_CHANNEL'] if r['channel']=='11' and r['mode']=='14')['pos']=str(length)
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Already completed clip accepted as active cut')
out.mkdir();report=dict(activeCpuCryCutByNativePaidJoinProven=True,
    bothBattleOwnersCleared=True,selectorContinuedFields=160,noGameLossUsed=True,
    proof=proof,alreadyEOFSubstitutionRejected=True,clipLength=length,terminal=terminal,
    logSHA256=sync.sha(folder/'run.log'),heardMixAccepted=False,damageInterruptionAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(passed=True,cutAge=proof['firstCut']['age'],cutPosition=proof['firstCut']['pos'],clipLength=length)))
