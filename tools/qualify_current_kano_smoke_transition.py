"""Current Kano earned native Smoke/controls/return, never assume RNG success."""
import ast
import copy
import json
import re
import verify_native_source_sync as sync
sync.verify()
for name,wanted in [('qualify_current_sonya_natural_smoke.py',{'load','gate'}),
                    ('qualify_current_sonya_toasty_decisions.py',{'decision_gate'})]:
    source=(sync.ROOT/'tools'/name).read_text()
    tree=ast.parse(source)
    definitions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    assert len(definitions)==len(wanted)
    code='\n'.join(ast.get_source_segment(source,n) for n in definitions)
    for old,new in [("r['winner']=='sonya'","r['winner']=='kano'"),
                    ("'18,4'","'17,4'"),("'18,14'","'17,14'"),
                    ("fights[0]['human']=='18'","fights[0]['human']=='17'")]:
        code=code.replace(old,new)
    exec(compile(code,__file__+'::same_native_gate_actualKano17','exec'))
folder=sync.ROOT/'audit_current_kano_smoke_transition_runtime'
out=sync.ROOT/'audit_current_kano_smoke_transition_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
completed=terminal['exitCode']==0 and terminal['limitReason'] is None
assert completed or terminal['limitReason'] in ('wall_limit','memory_limit','log_limit')
assert terminal['peakWorkingSetBytes']<=321*1024*1024 and terminal['logBytes']<=11*1024*1024
lua=sync.ROOT/'audit_current_kano_smoke_transition_preparation/stage.lua'
assert terminal['observerSha256']==sync.sha(lua)==sync.sha(sync.ROOT/'audit_current_sonya_smoke_transition_batched_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=load(folder/'run.log')
complete=rows.get('SECRET_COMPLETE',[])
if complete:
    assert len(complete)==1
    control_end=int(complete[0]['frame'])
    controls=gate({t:[r for r in group if int(r['frame'])<=control_end] for t,group in rows.items()})
else:
    control_end=None
    controls=gate(rows)
decision=decision_gate(rows)
normal_return=False
return_fields=[]
lethals=[]
if control_end is not None:
    assert controls['completeSameRoundControls']
    assert int(controls['responses'][1]['action']) in (512,776,779)
    for r in rows.get('INPUT',[]):
        if int(r['frame'])>control_end:
            mode=next(m for m in reversed(rows['MODE']) if int(m['frame'])<=int(r['frame']))
            assert mode['mode']=='4' and mode['arena']=='8' and r['button'] in ('Left','Right','Down','High_Punch')
    fight=int(controls['secretFight']['frame'])
    damage=[r for r in rows.get('SECRET_HEALTH',[]) if int(r['frame'])>=fight and r['pc']=='FF836700']
    assert all(0<=int(r['after'])<=int(r['before'])<=161 for r in damage)
    lethals=[r for r in damage if int(r['before'])>0 and r['after']=='0']
    returns=rows.get('SECRET_RETURN',[]);tails=rows.get('SECRET_RETURN_COMPLETE',[])
    if returns:
        assert len(returns)==1
        arrival=returns[0];begin=int(arrival['frame'])
        assert arrival['ids']==arrival['rosters']=='17,4' and arrival['states']=='1,1'
        assert arrival['mode']=='2' and arrival['arena']=='8' and arrival['hp']=='161,161' and arrival['actors']==arrival['owners']
        selected=[r for r in rows['SELECT_ID'] if int(r['frame'])>control_end]
        assert len(selected)==2 and {r['slot']:r['actual'] for r in selected}=={'1':'17','2':'4'}
        own_damage=[r for r in damage if int(r['frame'])<begin and r['slot']=='1']
        assert sum(int(r['before'])-int(r['after']) for r in own_damage)==322
        assert len([r for r in lethals if r['slot']=='1' and int(r['frame'])<begin])==2
        return_fields=[r for r in rows['SECRET_FIELD'] if int(r['frame'])>=begin]
        assert [int(r['frame']) for r in return_fields]==list(range(begin,int(return_fields[-1]['frame'])+1))
        assert all(r['mode']=='2' and r['arena']=='8' and r['ids']==r['rosters']=='17,4' and r['states']=='1,1' and r['actors']==r['owners'] and r['hp']=='161,161' for r in return_fields)
        if tails:
            assert len(tails)==1 and int(tails[0]['frame'])-begin>=180 and tails[0]['frame']==return_fields[-1]['frame']
            normal_return=completed and not rows.get('SECRET_NATIVE_RESET')
    elif tails:raise AssertionError('Tail without return')
bad=copy.deepcopy(rows);bad['MATCH'][0]['ids']='1,4'
try:gate({t:[r for r in group if control_end is None or int(r['frame'])<=control_end] for t,group in bad.items()})
except AssertionError:pass
else:raise AssertionError('Proxy Kano accepted')
out.mkdir()
report=dict(finiteObservationPassed=True,completedRunAccepted=completed,controls=controls,
    decisions=decision,normalTwoHumanReturnAccepted=normal_return,
    nativeSecretLethals=lethals,returnFields=len(return_fields),sameDriverAsSonya=True,proxyFaultRejected=True,
    terminal=terminal,logSHA256=sync.sha(folder/'run.log'),
    nativeResets=rows.get('SECRET_NATIVE_RESET',[]),decoderWatchdog=rows.get('SECRET_DECODER_WATCHDOG',[]),
    secretPixelsAudioAccepted=False,historicalLateResetFixed=False,allSecretContextsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(completedRun=completed,secretAccepted=controls['actualSecretAccepted'],
    controlsPassed=controls['completeSameRoundControls'],normalReturnAccepted=normal_return,decisions=decision)))
