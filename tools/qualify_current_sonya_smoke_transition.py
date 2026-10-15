"""Whole observed secret exit; bounded incomplete outcomes never count as return."""
import ast
import copy
import json
import re
import verify_native_source_sync as sync
sync.verify()
tree=ast.parse((sync.ROOT/'tools/qualify_current_sonya_natural_smoke.py').read_text())
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('load','gate')]
assert len(defs)==2
exec(compile(ast.Module(body=defs,type_ignores=[]),__file__+'::unchanged_earned_controls_gate','exec'))
folder=sync.ROOT/'audit_current_sonya_smoke_transition_runtime'
out=sync.ROOT/'audit_current_sonya_smoke_transition_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
completed=terminal['exitCode']==0 and terminal['limitReason'] is None
assert completed or terminal['limitReason'] in ('wall_limit','memory_limit','log_limit')
assert terminal['peakWorkingSetBytes']<=321*1024*1024 and terminal['logBytes']<=11*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_smoke_transition_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=load(folder/'run.log')
old=load(sync.ROOT/'audit_current_sonya_toasty_72_cadence_runtime/run.log')
end=int(old['SECRET_COMPLETE'][0]['frame'])
added={'SECRET_DECODER_WATCHDOG','SECRET_NATIVE_RESET','SECRET_POST_STATE','SECRET_RETURN','SECRET_RETURN_COMPLETE'}
for tag in set(rows)|set(old):
    if tag not in added|{'RESULT'}:
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<=end]==[
            r for r in old.get(tag,[]) if int(r['frame'])<=end],tag
prefix={t:[r for r in group if int(r['frame'])<=end] for t,group in rows.items()}
controls=gate(prefix)
assert controls['completeSameRoundControls']
assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
assert not [r for r in rows.get('INPUT',[]) if int(r['frame'])>end]
fight=int(controls['secretFight']['frame'])
stores=[r for r in rows.get('SECRET_HEALTH',[]) if int(r['frame'])>=fight and r['pc']=='FF836700']
assert all(0<=int(r['after'])<=int(r['before'])<=161 for r in stores)
damage=[r for r in stores if int(r['after'])<int(r['before'])]
lethals=[r for r in damage if r['after']=='0']
resets=[r for r in rows.get('SECRET_HEALTH',[]) if int(r['frame'])>fight and r['pc'] in ('FF825930','FF825960')]
for r in resets:
    assert r['after']=='161'
    assert any(v['frame']==r['frame'] and v['slot']!=r['slot'] for v in resets)
for r in rows.get('SECRET_FIELD',[]):
    if int(r['frame'])>=fight and r['mode']=='2' and r['arena']=='9':
        assert r['ids']==r['rosters']=='18,14' and r['states']=='1,0' and r['actors']==r['owners']
returns=rows.get('SECRET_RETURN',[])
tails=rows.get('SECRET_RETURN_COMPLETE',[])
normal_return=False
if returns and tails:
    assert len(returns)==len(tails)==1
    arrival=returns[0];tail=tails[0]
    assert int(tail['frame'])-int(arrival['frame'])>=180
    assert arrival['mode']=='2' and arrival['arena']!='9'
    assert arrival['ids']==arrival['rosters']=='18,4' and arrival['states']=='1,1'
    assert arrival['actors']==arrival['owners']
    fields=[r for r in rows['SECRET_FIELD'] if int(arrival['frame'])<=int(r['frame'])<=int(tail['frame'])]
    assert [int(r['frame']) for r in fields]==list(range(int(arrival['frame']),int(tail['frame'])+1))
    assert all(r['mode']=='2' and r['arena']==arrival['arena'] and r['ids']==r['rosters']=='18,4' and r['actors']==r['owners'] for r in fields)
    assert len([r for r in lethals if r['slot']=='1'])>=2
    normal_return=completed and not rows.get('SECRET_NATIVE_RESET')
bad=copy.deepcopy(prefix);bad['SECRET_ACCEPT'][0]['pc']='FF814E90'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Wrong acceptance accepted')
out.mkdir()
report=dict(finiteTransitionObservationPassed=True,completedRunAccepted=completed,
    priorSuccessfulControlsPrefixUnchangedThrough=end,controls=controls,
    exactNativeSecretLethalCollisions=lethals,pairedNativeHealthResets=resets,
    observedReturn=returns,observedReturnTail=tails,normalTwoHumanReturnAccepted=normal_return,
    nativeResets=rows.get('SECRET_NATIVE_RESET',[]),decoderWatchdog=rows.get('SECRET_DECODER_WATCHDOG',[]),
    lastPostState=rows.get('SECRET_POST_STATE',[])[-1:],terminal=terminal,
    logSHA256=sync.sha(folder/'run.log'),secretPixelsAudioAccepted=False,
    historicalLateResetFixed=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(completedRun=completed,secretLethals=len(lethals),normalReturnAccepted=normal_return,lastPostState=report['lastPostState'])))
