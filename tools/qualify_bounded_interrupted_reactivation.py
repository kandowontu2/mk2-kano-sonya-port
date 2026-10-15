"""Physical special reactivation after proven real interruption and recovery."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_interrupted_walk_jump import load

def gate(states,command,side,move,cues):
    assert len(states)==1602
    identity='17' if move=='ball' else '18'
    assert all(r['id']==r['roster']==(identity if int(r['slot'])==side else ('18' if identity=='17' else '17')) and r['actor']==r['owner'] and r['state']=='1' and r['mode']=='2' for r in states)
    own=[r for r in states if int(r['slot'])==side]
    assert all(r['hp']=='121' for r in own if int(r['frame'])>=command+260)
    action={'bicycle':'516','square':'519','ball':'523'}[move]
    assert any(r['action']==action for r in own if command+460<=int(r['frame'])<command+600)
    expected={'bicycle':['6B01','6B02'],'square':['6B00'],'ball':['6B03']}[move]
    assert [r['value'] for r in cues if int(r['frame'])>=command+460]==expected
    final=[r for r in states if int(r['frame'])>=command+680]
    assert len(final)>=60
    assert all(r['action']=='771' and r['y']==r['floor'] and all(int(r[k],16)==0 for k in ('vx','vy','gravity','trail')) and int(r['flags'],16)&0x1c==0 and int(r['body'],16)&0xc==0 for r in final)
    return dict(secondSpecialAction=action,secondVoiceCues=expected,settledFinalActorFields=len(final))

def main():
    out=sync.ROOT/'audit_bounded_interrupted_reactivation_checked';assert not out.exists()
    proof_path=sync.ROOT/'audit_bounded_interrupted_followup_complete_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
    for move in ('bicycle','square','ball'):
        for side in (1,2):
            key=f'{move}P{side}';folder=sync.ROOT/f'audit_bounded_interrupted_{move}_p{side}_reactivation_runtime'
            base=sync.ROOT/f'audit_bounded_interrupted_{move}_p{side}_complete_runtime'
            assert sync.sha(base/'run.log')==proof['results'][key]['logSHA256']
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
            assert not (folder/'stderr.log').read_text().strip()
            states,command,inputs=load(folder);old,oldcommand,oldinputs=load(base)
            assert command==oldcommand and states[:len(old)]==old
            assert [r for r in inputs if int(r['frame'])<=int(old[-1]['frame'])]==oldinputs
            repeat=[r for r in inputs if int(r['slot'])==side and int(r['frame'])>=command+460]
            expected_count={'bicycle':15,'square':9,'ball':84}[move]
            assert len(repeat)==expected_count
            cues=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in (folder/'run.log').read_text().splitlines() if line.startswith('MK2_HSPECIAL_CUE ')]
            positive=gate(states,command,side,move,cues);faults=[]
            for fault in ('missing_reactivation','stale_trail'):
                bad=copy.deepcopy(states)
                if fault=='missing_reactivation':
                    for r in bad:
                        if int(r['slot'])==side and command+460<=int(r['frame'])<command+600:r['action']='771'
                else:bad[-1]['trail']='00000001'
                try:gate(bad,command,side,move,cues)
                except AssertionError:faults.append(fault)
                else:raise AssertionError('Fault accepted')
            results[key]=dict(**positive,rejectedFaults=faults,priorHitAndRecoveryPrefixUnchanged=True,physicalRepeatInputCount=len(repeat),terminal=terminal,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),priorProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),fullGoalComplete=False,scope='Six physical reactivations and scalar recovery, not whole-scene, all arenas or finished release acceptance')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=6)))

if __name__=='__main__':main()
