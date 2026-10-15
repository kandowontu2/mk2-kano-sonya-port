"""Challenge actual successful Sonya/Smoke evidence, without another emulator."""
import ast
import copy
import json
import re
import verify_native_source_sync as sync
sync.verify()
for name,wanted in [('qualify_current_sonya_natural_smoke.py',{'load','gate'}),
                    ('qualify_current_sonya_toasty_decisions.py',{'decision_gate'})]:
    tree=ast.parse((sync.ROOT/'tools'/name).read_text())
    definitions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    assert len(definitions)==len(wanted)
    exec(compile(ast.Module(body=definitions,type_ignores=[]),__file__+'::'+name,'exec'))
folder=sync.ROOT/'audit_current_sonya_toasty_72_cadence_runtime'
prior_path=sync.ROOT/'audit_current_sonya_toasty_72_cadence_checked/report.json'
out=sync.ROOT/'audit_current_sonya_smoke_control_faults_checked'
assert not out.exists()
prior=json.loads(prior_path.read_text())
assert prior['finiteObservationPassed'] and prior['admission']['completeSameRoundControls']
assert sync.sha(folder/'run.log')==prior['logSHA256']
rows=load(folder/'run.log')
def full(records):
    admission=gate(records);decision=decision_gate(records)
    assert admission['actualSecretAccepted'] and admission['completeSameRoundControls']
    assert any(r['popup'] and r['value']<40 for r in decision['actualNativeDecisions'])
    jump=admission['responses'][1]
    assert int(jump['action']) in (512,776,779)
    return dict(admission=admission,decision=decision)
positive=full(rows)
faults=[]
cases=[('acceptance PC','SECRET_ACCEPT',0,'pc','FF814E90'),
       ('wrong human side','SECRET_ACCEPT',0,'taskSide','1'),
       ('Down absent','SECRET_ACCEPT',0,'in0','FFFFFFFF'),
       ('wrong hidden opponent','SECRET_ACCEPT',0,'secretID','8'),
       ('no real jump','SECRET_JUMP',-1,'y',rows['SECRET_JUMP'][-1]['floor']),
       ('hurt action substituted for jump','SECRET_JUMP',-1,'action','1548')]
for label,tag,index,key,value in cases:
    broken=copy.deepcopy(rows);assert broken[tag][index][key]!=value
    broken[tag][index][key]=value
    try:full(broken)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Corruption accepted: '+label)
first=int(positive['admission']['secretFight']['frame'])
last=int(positive['admission']['complete']['frame'])
for label in ('proxy actor','lost owner','missing live field','ordinary punch omitted','positive RNG outside threshold','Start input omitted'):
    broken=copy.deepcopy(rows)
    if label=='proxy actor':
        next(r for r in broken['SECRET_FIELD'] if int(r['frame'])==first)['ids']='1,14'
    elif label=='lost owner':
        next(r for r in broken['SECRET_FIELD'] if int(r['frame'])==first)['owners']='00000000,00000000'
    elif label=='missing live field':
        broken['SECRET_FIELD']=[r for r in broken['SECRET_FIELD'] if int(r['frame'])!=first+1]
    elif label=='ordinary punch omitted':
        at=positive['admission']['responses'][2]['frame']
        next(r for r in broken['SECRET_FIELD'] if r['frame']==at)['actions']='0,771'
    elif label=='positive RNG outside threshold':
        next(r for r in broken['TOASTY_DECISION'] if r['entry']=='FF8DF120' and int(r['a0'],16)<40)['a0']='00000028'
    else:
        at=int(broken['SECRET_ACCEPT'][0]['frame'])
        broken['INPUT']=[r for r in broken['INPUT'] if not(r['slot']=='1' and r['button']=='Start' and at-1<=int(r['frame'])<=at)]
    try:full(broken)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Corruption accepted: '+label)
assert full(rows)==positive and len(faults)==12
out.mkdir()
report=dict(currentNaturalSonyaSmokeAdmissionAndFiniteControlsPassed=True,
    actualFields=last-first+1,positive=positive,actualEvidenceFaultsRejected=faults,
    priorReportSHA256=sync.sha(prior_path),logSHA256=sync.sha(folder/'run.log'),
    newEmulatorRuns=0,newMedia=0,completeSecretTeardownAccepted=False,
    secretPixelsAudioAccepted=False,historicalLateResetFixed=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(passed=True,liveFields=last-first+1,rejectedFaults=len(faults))))
