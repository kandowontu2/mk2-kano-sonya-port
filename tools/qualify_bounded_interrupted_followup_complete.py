"""Complete real post-hit walking/jumping/punching and settled native state."""
import copy,json
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_interrupted_walk_jump import load

def gate(states,command,side,identity):
    assert len(states)==1042
    own=[r for r in states if int(r['slot'])==side]
    assert len(own)==521 and all(r['id']==r['roster']==identity and r['actor']==r['owner'] for r in own)
    walk=[r for r in own if command+260<=int(r['frame'])<=command+280]
    assert max(int(r['x']) for r in walk)>min(int(r['x']) for r in walk)
    assert any(int(r['vx'],16)!=0 and r['y']==r['floor'] for r in walk)
    jump=[r for r in own if command+290<=int(r['frame'])<command+350]
    assert any(int(r['y'])<int(r['floor']) and int(r['vy'],16)!=0 for r in jump)
    punch=[r for r in own if command+360<=int(r['frame'])<=command+390]
    assert any(r['action']=='257' for r in punch)
    final=[r for r in states if int(r['frame'])>=command+420];assert len(final)>=30
    assert all(r['y']==r['floor'] and r['action']=='771' and all(int(r[k],16)==0 for k in ('vx','vy','gravity','trail'))
        and int(r['flags'],16)&0x1c==0 and int(r['body'],16)&0xc==0 and r['actor']==r['owner'] for r in final)
    assert all(r['hp']=='121' for r in own if int(r['frame'])>=command+260)
    return dict(actualPostHitWalkJumpAndPunch=True,settledFinalActorFields=len(final),nativeIdleAction='0303',staleMotionFlagsTrailOrOwnershipObserved=False)

def main():
    out=sync.ROOT/'audit_bounded_interrupted_followup_complete_checked';assert not out.exists();results={}
    proof_path=sync.ROOT/'audit_bounded_interrupted_walk_jump_checked/report.json';proof=json.loads(proof_path.read_text());assert proof['passed']
    for move in ('bicycle','square','ball'):
        for side in (1,2):
            key=f'{move}P{side}';folder=sync.ROOT/f'audit_bounded_interrupted_{move}_p{side}_complete_runtime'
            base=sync.ROOT/f'audit_bounded_interrupted_{move}_p{side}_followup_runtime'
            assert sync.sha(base/'run.log')==proof['results'][key]['logSHA256']
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            states,command,inputs=load(folder);old,oldcommand,oldinputs=load(base)
            assert command==oldcommand and states[:len(old)]==old
            assert [r for r in inputs if int(r['frame'])<=int(old[-1]['frame'])]==oldinputs
            assert len([r for r in inputs if int(r['slot'])==side and r['button']=='High_Punch' and command+360<=int(r['frame'])<command+364])==4
            identity='17' if move=='ball' else '18';positive=gate(states,command,side,identity);faults=[]
            for label in ('missing_punch','stale_trail'):
                bad=copy.deepcopy(states)
                if label=='missing_punch':
                    for r in bad:
                        if int(r['slot'])==side and command+360<=int(r['frame'])<=command+390:r['action']='771'
                else:bad[-1]['trail']='00000001'
                try:gate(bad,command,side,identity)
                except AssertionError:faults.append(label)
                else:raise AssertionError('Recovery fault accepted')
            results[key]=dict(**positive,rejectedFaults=faults,originalPrefixUnchanged=True,terminal=t,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)),priorProofSHA256=sync.sha(proof_path))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,contexts=6,completePostHitControlAndSettledState=True)))

if __name__=='__main__':main()
