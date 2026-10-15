"""Same-paid-match boss defeat and natural ending pages; no pixel/audio claim."""
import copy,json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load,check
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_shao_backjump_charge_counter_runtime'
out=root/'audit_current_kano_p2_earned_ending_checked';assert not out.exists()
rows=load(case/'run.log');sequence=list(range(13))+[14,15,16]
def gate(r):
    assert check(r,2,17,sequence)==sequence
    fights=r['FIGHT']
    for stage in sequence[:-1]:
        attempts=[f for f in fights if int(f['stage'])==stage]
        passed=False
        for f in attempts:
            a=int(f['frame']);b=min([int(g['frame']) for g in fights if int(g['frame'])>a]+[75417])
            wins=[w for w in r['WIN'] if w['stage']==str(stage) and w['slot']=='2' and a<=int(w['frame'])<b]
            if len(wins)>=2:passed=True
        assert passed
    boss=[f for f in fights if f['stage']=='16'];assert len(boss)==1 and boss[0]['frame']=='69699'
    wins=[w for w in r['WIN'] if w['stage']=='16'];assert len(wins)==1 and wins[0]['slot']=='2' and wins[0]['frame']=='70715' and wins[0]['health']=='0,17'
    assert not any(int(s['frame'])>=69699 for s in r['LOSS'])
    assert any(s['frame']=='72050' and s['stage']=='16' and s['mode']=='11' and s['winner']=='2' and s['health']=='0,17' for s in r['STATE'])
    assert any(s['frame']=='72044' and s['after']=='263' and s['id']==s['roster']=='17' and s['actor']==s['owner']==s['a8'] and s['main']==s['a13'] and s['health']=='17,11' for s in r['BOSS_ACTION'])
    assert any(s['frame']=='72376' and s['winner']=='2' and s['roster']=='17' and s['health']=='0,17' for s in r['ENDING_START'])
    assert len(r['PICTURE'])==2 and {s['page'] for s in r['PICTURE']}=={'1','2'}
    assert all(s['roster']=='17' and s['pc']=='FF8447E0' for s in r['PICTURE'])
    assert len(r['TEXT'])==6 and all(s['roster']=='17' for s in r['TEXT'])
    assert len(r['ENDING_COMPLETED'])==1 and r['ENDING_COMPLETED'][0]['frame']=='75116'
gate(rows)
faults=[]
for name,mutate in [
 ('remove_final_round_state',lambda r:r.update(STATE=[s for s in r['STATE'] if s['frame']!='72050'])),
 ('wrong_picture_identity',lambda r:r['PICTURE'][0].update(roster='1')),
 ('continued_between_boss_rounds',lambda r:r['LOSS'].append(dict(frame='71000',stage='16'))),
 ('missing_ending_page',lambda r:r['PICTURE'].pop())]:
    bad=copy.deepcopy(rows);mutate(bad)
    try:gate(bad)
    except AssertionError:faults.append(name)
    else:raise AssertionError('Fault accepted:'+name)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
report=dict(currentKanoP2NaturalCampaignRuntimeClear=True,visitedStages=sequence,
    samePaidShaoAttemptStart=69699,firstRoundWin=70715,finalBossDefeatState=72050,
    endingStart=72376,ownNativePicturePages=2,ownNativeTextRecords=6,endingCompletion=75116,
    faultCasesRejected=faults,terminal=terminal,logSHA256=sync.sha(case/'run.log'),
    endingPixelsReviewed=False,endingAudioAccepted=False,postEndingFreshJoinAccepted=False,
    otherThreeCurrentCampaignsAccepted=False,fullPortAccepted=False,
    caveat='Final Shao defeat enters ending mode directly; require same attempt, native upper/KO state and own ending pages, not two WIN-table reads. This seals runtime chronology, not rendered ending acceptance.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
