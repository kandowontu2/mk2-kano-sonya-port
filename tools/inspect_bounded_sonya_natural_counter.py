"""Qualify actual natural selection and census, without crediting absent hits."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    folder=sync.ROOT/'audit_bounded_sonya_natural_counter_runtime'
    out=folder/'observed_context.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    fields=[];cues=[];owners=[];selected=[];physical=[]
    tags={'MK2_BOUNDED_FIELD':fields,'MK2_BOUNDED_CUE':cues,
          'MK2_VOICE_OWNER':owners,'MK2_P2CPU_SELECT_RESULT':selected,
          'MK2_BOUNDED_PHYSICAL':physical}
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip()
            if tag in tags:tags[tag].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    assert len(selected)==1;s=selected[0]
    assert s['human']=='sonya' and s['human_id']=='18' and s['errors']=='0'
    assert int(s['live'])>0 and int(s['checks'])>0
    assert len(fields)>1000 and len(fields)==len(physical)
    assert all(r['p1id']=='18' and r['p2id']==s['initial_cpu'] and r['writes']=='0' for r in fields)
    hits=[]
    for a,b in zip(fields,fields[1:]):
        for slot in (1,2):
            if 0<int(a[f'hp{slot}'])<=166 and int(b[f'hp{slot}'])<int(a[f'hp{slot}']):
                hits.append(dict(frame=int(b['frame']),slot=slot,before=int(a[f'hp{slot}']),after=int(b[f'hp{slot}'])))
    active={(int(r['frame']),int(r['slot'])) for r in owners if r['actor']!='00000000'}
    overlaps=[h for h in hits if (h['frame'],h['slot']) in active or (h['frame']-1,h['slot']) in active]
    report=dict(passed=True,actualSelection=s,observedFields=len(fields),actualDamageEvents=hits,
        privateCueLaunches=cues,observedVoiceHitCandidates=overlaps,
        targetInterruptionAccepted=False,fullGoalComplete=False,terminal=terminal,
        logSHA256=sync.sha(folder/'run.log'),sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)))
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,selection=s,fields=len(fields),damageEvents=len(hits),cues=cues,voiceHitCandidates=overlaps)))

if __name__=='__main__':main()
