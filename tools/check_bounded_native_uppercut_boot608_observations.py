"""Preserve failed no-cue assumption: actual owner snapshots are nonzero.

No claim of launch-port coverage or hit-during-voice qualification.
"""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync
BASE=sync.ROOT/'audit_bounded_native_uppercut_boot608_runtime'
RX=re.compile(r'(\w+)=([^\s]+)')
def main():
    terminal=json.loads((BASE/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    fields={};owners={};actions=collections.Counter();selection=None;cue_count=0
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip();r=dict(RX.findall(line))
            if tag=='MK2_BOUNDED_FIELD':
                assert r['p1id']=='17' and r['p2id']=='18' and r['writes']=='0'
                fields[int(r['frame'])]=r;actions[r['action1']]+=1
                assert len(fields)<=1800
            elif tag=='MK2_VOICE_OWNER' and r['slot']=='2' and r['actor']!='00000000':
                owners[int(r['frame'])]=r
            elif tag=='MK2_BOUNDED_CUE':cue_count+=1
            elif tag=='MK2_P2CPU_SELECT_RESULT':selection=r
    assert selection and selection['errors']=='0' and owners
    hits=[];previous=None
    for frame,r in sorted(fields.items()):
        hp=int(r['hp2'])
        if previous and 0<previous[1]<=166 and hp<previous[1]:
            hits.append(dict(frame=frame,before=previous[1],after=hp,
                activeOwnerSameFrame=frame in owners,activeOwnerPreviousFrame=frame-1 in owners))
        previous=(frame,hp)
    result=dict(nativeExit=terminal['exitCode'],peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        scalarFields=len(fields),observedHumanActions=dict(actions),
        activeSonyaOwnerFrames=len(owners),firstActiveFrame=min(owners),lastActiveFrame=max(owners),
        incomingSonyaDamageTransitions=hits,privatePortCueCount=cue_count,
        privateInterruptionAccepted=False,fullGoalComplete=False,
        limitation='Saved owner became active but port tap emitted no cue; tap retention and launch provenance require correction before acceptance',
        logSha256=sync.sha(BASE/'run.log'),sourceSync=sync.verify())
    out=BASE/'scalar_observations.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sourceSync','logSha256')}))
if __name__=='__main__':main()
