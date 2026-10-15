"""Actual native two-KO/selector/return proof and batched transport fidelity."""
import ast
import copy
import json
import re
import verify_native_source_sync as sync
sync.verify()
tree=ast.parse((sync.ROOT/'tools/qualify_current_sonya_natural_smoke.py').read_text())
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='load']
assert len(defs)==1
exec(compile(ast.Module(body=defs,type_ignores=[]),__file__+'::read_only_records','exec'))
folder=sync.ROOT/'audit_current_sonya_smoke_transition_batched_runtime'
prior_path=sync.ROOT/'audit_current_sonya_smoke_transition_batched_checked/report.json'
out=sync.ROOT/'audit_current_sonya_smoke_return_faults_checked'
assert not out.exists()
prior=json.loads(prior_path.read_text())
assert prior['completedRunAccepted'] and prior['normalTwoHumanReturnAccepted']
assert prior['logSHA256']==sync.sha(folder/'run.log')
rows=load(folder/'run.log')
old=load(sync.ROOT/'audit_current_sonya_smoke_transition_runtime/run.log')
through=max(int(r['frame']) for group in old.values() for r in group)
for tag in set(rows)|set(old):
    if tag!='RESULT':
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<=through]==old.get(tag,[]),tag
def gate(records):
    arrival=records['SECRET_RETURN'][0];tail=records['SECRET_RETURN_COMPLETE'][0]
    assert len(records['SECRET_RETURN'])==len(records['SECRET_RETURN_COMPLETE'])==1
    assert arrival['ids']==arrival['rosters']=='18,4' and arrival['states']=='1,1' and arrival['hp']=='161,161'
    assert arrival['mode']=='2' and arrival['arena']=='8' and arrival['actors']==arrival['owners']
    begin,last=int(arrival['frame']),int(tail['frame'])
    assert last-begin>=180 and not records.get('SECRET_NATIVE_RESET')
    fields=[r for r in records['SECRET_FIELD'] if begin<=int(r['frame'])<=last]
    assert [int(r['frame']) for r in fields]==list(range(begin,last+1))
    assert all(r['ids']==r['rosters']=='18,4' and r['states']=='1,1' and r['mode']=='2' and r['arena']=='8' and r['actors']==r['owners'] and r['hp']=='161,161' for r in fields)
    fight=int(records['SECRET_FIGHT'][0]['frame'])
    damage=[r for r in records['SECRET_HEALTH'] if fight<=int(r['frame'])<begin and r['slot']=='1' and r['pc']=='FF836700']
    assert sum(int(r['before'])-int(r['after']) for r in damage)==322
    assert len([r for r in damage if int(r['before'])>0 and r['after']=='0'])==2
    selected=[r for r in records['SELECT_ID'] if int(r['frame'])>fight]
    assert len(selected)==2 and {r['slot']:r['actual'] for r in selected}=={'1':'18','2':'4'}
    assert all(r['actual']==r['target'] for r in selected)
    return dict(nativeIncomingDamage=322,nativeLethalCollisions=2,realPostSecretReselection=True,returnFields=len(fields))
positive=gate(rows)
faults=[]
for label in ('proxy return','lost return owner','missing return field','native lethal omitted','wrong reselected fighter','unfinished tail','native reset substituted'):
    bad=copy.deepcopy(rows)
    begin=int(bad['SECRET_RETURN'][0]['frame'])
    if label=='proxy return':bad['SECRET_RETURN'][0]['ids']='1,4'
    elif label=='lost return owner':bad['SECRET_RETURN'][0]['owners']='00000000,00000000'
    elif label=='missing return field':bad['SECRET_FIELD']=[r for r in bad['SECRET_FIELD'] if int(r['frame'])!=begin+1]
    elif label=='native lethal omitted':
        target=next(r for r in bad['SECRET_HEALTH'] if r['pc']=='FF836700' and r['slot']=='1' and r['after']=='0')
        bad['SECRET_HEALTH'].remove(target)
    elif label=='wrong reselected fighter':
        next(r for r in bad['SELECT_ID'] if int(r['frame'])>23797 and r['slot']=='1')['actual']='1'
    elif label=='unfinished tail':bad['SECRET_RETURN_COMPLETE'][0]['frame']=str(begin+127)
    else:bad['SECRET_NATIVE_RESET']=[dict(frame=str(begin+1))]
    try:gate(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Corruption accepted: '+label)
assert gate(rows)==positive and len(faults)==7
out.mkdir()
(out/'report.json').write_text(json.dumps(dict(currentNaturalSonyaSmokeReturnPassed=True,
    positive=positive,actualRecordFaultsRejected=faults,
    batchingPreservesEveryPriorRecordThrough=through,priorReportSHA256=sync.sha(prior_path),
    logSHA256=sync.sha(folder/'run.log'),newEmulatorRuns=0,newMedia=0,
    secretVisualAudioAccepted=False,historicalLateResetFixed=False,allSecretContextsAccepted=False,fullPortAccepted=False),indent=2))
print(json.dumps(dict(passed=True,proof=positive,rejectedFaults=len(faults))))
