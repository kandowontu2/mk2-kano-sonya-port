"""Stream scalar diagnostic; never treat an absent voice target as passed."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync

BASE=sync.ROOT/'audit_bounded_native_uppercut_runtime'
RX=re.compile(r'(\w+)=([^\s]+)')
def main():
    terminal=json.loads((BASE/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['peakWorkingSetBytes']<=320*1024*1024
    counts=collections.Counter();actions=collections.Counter();cpu_ids=collections.Counter()
    hp_prev={};damage=collections.Counter();active=0;selection=None
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576
            assert 'Lua error' not in line
            tag=line.split(' ',1)[0].strip()
            row=dict(RX.findall(line));counts[tag]+=1
            if tag=='MK2_P2CPU_SELECT_RESULT':selection=row
            if tag=='MK2_BOUNDED_FIELD':
                assert row['p1id']=='17' and row['writes']=='0'
                cpu_ids[row['p2id']]+=1;actions[row['action1']]+=1
                for slot in (1,2):
                    hp=int(row[f'hp{slot}'])
                    if slot in hp_prev and 0<hp_prev[slot]<=166 and hp<hp_prev[slot]:damage[slot]+=1
                    hp_prev[slot]=hp
            if tag=='MK2_VOICE_OWNER' and row['actor']!='00000000':active+=1
    assert selection and selection['errors']=='0' and selection['human_id']=='17'
    report=dict(resourceAndSelectionChecksPassed=True,privateInterruptionAccepted=False,
        classification='target_absent',reason='Natural opponent was Baraka (3), not Sonya; no private cue launched',
        terminal=terminal,scalarFields=counts['MK2_BOUNDED_FIELD'],nativeCpuIds=dict(cpu_ids),
        observedHumanActions=dict(actions),healthDecreaseTransitions=dict(damage),
        privateCueCount=counts['MK2_BOUNDED_CUE'],activeOwnerSnapshots=active,
        fullGoalComplete=False,sourceSync=sync.verify(),
        logSha256=sync.sha(BASE/'run.log'),checkerSha256=sync.sha(Path(__file__)))
    assert report['privateCueCount']==0 and active==0 and set(cpu_ids)=={'3'}
    out=BASE/'scalar_check.json';assert not out.exists()
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('classification','scalarFields','nativeCpuIds','observedHumanActions','healthDecreaseTransitions','privateCueCount')}))
if __name__=='__main__':main()
