"""Actual post-hit walk/jump response; no unexecuted punch credited."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    states=[];command=None;inputs=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if line.startswith('MK2_HSPECIAL_FIELD '):states.append(r)
            elif line.startswith('MK2_HSPECIAL_COMMAND '):assert command is None;command=int(r['frame'])
            elif line.startswith('MK2_HSPECIAL_INPUT '):inputs.append(r)
    assert command is not None
    return states,command,inputs

def main():
    out=sync.ROOT/'audit_bounded_interrupted_walk_jump_checked';assert not out.exists();results={}
    for move in ('bicycle','square','ball'):
        for side in (1,2):
            folder=sync.ROOT/f'audit_bounded_interrupted_{move}_p{side}_followup_runtime'
            if move=='bicycle':base=sync.ROOT/('audit_bounded_twohuman_hit_voice_state_runtime' if side==1 else 'audit_bounded_twohuman_p2_hit_voice_runtime')
            elif move=='square':base=sync.ROOT/f'audit_bounded_twohuman_square_p{side}_rise_counter_runtime'
            else:base=sync.ROOT/f'audit_bounded_kano_ball_p{side}_guard_counter_runtime'
            terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            states,command,inputs=load(folder);old,oldcommand,_=load(base);assert command==oldcommand
            assert [r for r in states if int(r['frame'])<=command+260]==[r for r in old if int(r['frame'])<=command+260]
            own=[r for r in states if int(r['slot'])==side];assert len(own)==421
            identity='17' if move=='ball' else '18'
            assert all(r['id']==r['roster']==identity and r['actor']==r['owner'] and r['hp']=='121' for r in own if int(r['frame'])>=command+260)
            walk=[r for r in own if command+260<=int(r['frame'])<=command+280]
            assert max(int(r['x']) for r in walk)>min(int(r['x']) for r in walk)
            assert any(int(r['vx'],16)!=0 and r['y']==r['floor'] for r in walk)
            jump=[r for r in own if int(r['frame'])>=command+290]
            assert any(int(r['y'])<int(r['floor']) and int(r['vy'],16)!=0 for r in jump)
            assert all(int(r['frame'])<command+360 for r in states)
            assert not any(int(r['frame'])>=command+360 for r in inputs)
            results[f'{move}P{side}']=dict(prefixPhysicalStateUnchanged=True,postHitWalkAndJumpObserved=True,
                punchExecuted=False,settledFinalRecoveryAccepted=False,terminal=terminal,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,contexts=6,walkAndJumpObserved=True,punchExecuted=False)))

if __name__=='__main__':main()
