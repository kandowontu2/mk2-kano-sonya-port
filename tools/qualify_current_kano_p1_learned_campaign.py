"""Current P1 native identity and same-paid-attempt stage chronology."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load,check
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p1_learned_campaign_runtime'
out=root/'audit_current_kano_p1_learned_campaign_checked';assert not out.exists()
rows=load(case/'run.log');sequence=list(range(13))+[14,15,16]
stages=check(rows,1,17,sequence)
assert all(r['human']=='17:17' and r['human_slot']=='1' and r['writes']=='0' and r['assistance']=='none' for r in rows['FIGHT'])
fights=rows['FIGHT'];same_attempt=[]
for stage in stages[:-1]:
    candidates=[]
    for f in fights:
        if int(f['stage'])!=stage:continue
        a=int(f['frame']);b=min([int(g['frame']) for g in fights if int(g['frame'])>a]+[120001])
        wins=[w for w in rows['WIN'] if int(w['stage'])==stage and w['slot']=='1' and a<=int(w['frame'])<b]
        if len(wins)>=2:candidates.append(dict(stage=stage,attemptStart=a,wins=[int(w['frame']) for w in wins]))
    assert candidates;same_attempt.append(candidates[-1])
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
report=dict(currentTrueKanoP1FiniteStageChronologyPassed=True,visitedStages=stages,
    samePaidMatchAdvances=same_attempt,lastFight=fights[-1],results=rows.get('RESULT',[]),
    terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
