"""Classify existing exact action changes, with no additional emulator run."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_mirror_confirmed_jump_runtime'
rows=chronology.load(folder/'run.log')
events=rows['MIRROR_ACTION_CHANGE']
own=[r for r in events if r['slot']=='1']
cpu=[r for r in events if r['slot']=='2']
counts={s:dict(Counter(r['action'] for r in events if r['slot']==s)) for s in ('1','2')}
windows=[]
for jump in rows['MIRROR_JUMP_ACCEPTED']:
    frame=int(jump['frame'])
    after=[r for r in own if frame<=int(r['frame'])<frame+30]
    windows.append(dict(frame=frame,startAction=jump['action'],gap=int(jump['gap']),
                        subsequentActions=[int(r['action']) for r in after],
                        airAttackCandidates=[r for r in after if r['action'] in ('1024','1025')],
                        hurtObserved=any(r['action'] in ('1283','1286') for r in after)))
assert len(windows)==49
report=dict(logSHA256=sync.sha(folder/'run.log'),actionChangesBySlot=counts,
 jumpWindows=len(windows),windowsWithAirAttackCandidate=sum(bool(r['airAttackCandidates']) for r in windows),
 windowsWithHurt=sum(r['hurtObserved'] for r in windows),
 cpuThrowEntries=sum(r['action']=='1287' for r in cpu),
 airAttackCandidateEntries=[r for r in own if r['action'] in ('1024','1025')],
 windows=windows,exactDamageCauseProven=False,
 currentCampaignClear=False,fullPortAccepted=False,
 scope='Native action transitions.776 counts startup, not proof of completed airborne jump.1024/1025 remain candidate codes pending native dispatcher identification.')
out=sync.ROOT/'audit_current_confirmed_jump_outcomes'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ('windows','airAttackCandidateEntries')},indent=2))
