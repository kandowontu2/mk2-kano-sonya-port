"""Native upper-state/recovery health pairs and observed cue age only."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;log=root/'audit_current_kano_p2_shao_charge_settled_counter_runtime/run.log'
out=root/'audit_current_shao_counter_health_windows_checked';assert not out.exists()
rows=load(log);actions=[r for r in rows['BOSS_ACTION'] if r['stage']=='16']
entries=[r for r in actions if r['after']=='263']
contacts=[r for r in rows['SHAO_CHARGE_TRACE'] if r['entry']=='FF9D24C0']
windows=[]
for e in entries:
    f=int(e['frame']);same=[r for r in actions if r['main']==e['main'] and f<int(r['frame'])<=f+12 and r['before']=='263' and r['after']!='263']
    transition=min(same,key=lambda r:int(r['frame'])) if same else None
    before=[int(v) for v in e['health'].split(',')]
    after=[int(v) for v in transition['health'].split(',')] if transition else None
    cues=[r for r in contacts if r['human_main']==e['main'] and 0<=f-int(r['frame'])<=64]
    cue=max(cues,key=lambda r:int(r['frame'])) if cues else None
    windows.append(dict(entry=f,transitionFrame=int(transition['frame']) if transition else None,
        transitionAction=int(transition['after']) if transition else None,cpuHealthBefore=before[1],cpuHealthAfter=after[1] if after else None,
        humanHealthBefore=before[0],humanHealthAfter=after[0] if after else None,
        chargeContactToUpperEntry=f-int(cue['frame']) if cue else None,contactGap=int(cue['gap']) if cue else None))
assert len(windows)==46
complete=[r for r in windows if r['transitionAction']==1539]
report=dict(ownedUpperEntries=len(windows),observedRecovery1539Transitions=len(complete),
    cpuHealthDecreasesAtRecoveryTransition=dict(Counter(r['cpuHealthBefore']-r['cpuHealthAfter'] for r in complete)),
    chargeCueToUpperEntryFields=dict(Counter(r['chargeContactToUpperEntry'] for r in windows)),
    windows=windows,logSHA256=sync.sha(log),
    caveat='Paired native state-write health samples, not direct HP collision taps. No exact damage source or guaranteed safe recovery window claimed.',
    winningControllerProved=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='windows'}))
