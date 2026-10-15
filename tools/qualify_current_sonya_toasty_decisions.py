"""Actual current RNG outcomes; missing decision path never relabelled a miss."""
import ast
import copy
import json
import verify_native_source_sync as sync
sync.verify()
tree=ast.parse((sync.ROOT/'tools/qualify_current_sonya_natural_smoke.py').read_text())
functions=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('load','gate')]
assert len(functions)==2
import re
exec(compile(ast.Module(body=functions,type_ignores=[]),__file__+'::original_admission_control_gate','exec'))
folder=sync.ROOT/'audit_current_sonya_toasty_decisions_runtime'
out=sync.ROOT/'audit_current_sonya_toasty_decisions_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_toasty_decisions_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=load(folder/'run.log')
old=load(sync.ROOT/'audit_current_sonya_natural_smoke_close_runtime/run.log')
new={'TOASTY_DECISION','TOASTY_STOCK_CODE'}
assert {t:r for t,r in rows.items() if t not in new}==old
proof=gate(rows)
def decision_gate(records):
    code=records['TOASTY_STOCK_CODE']
    expected={'FF8DE9F0':str((0xff8df2b0-0xff8de9f0)//16),
              'FF81E740':str((0xff81e820-0xff81e740)//16),
              'FF80E980':str((0xff80ecf0-0xff80e980)//16)}
    assert len(code)==3 and {r['at']:r['words'] for r in code}==expected
    assert all(r['frame']=='600' and r['mismatches']=='0' and r['writes']=='0' and r['assistance']=='none' for r in code)
    decisions=records.get('TOASTY_DECISION',[])
    products=[r for r in decisions if r['entry']=='FF8DF120']
    observations=[]
    for product in products:
        args=[r for r in decisions if r['entry']=='FF8DF0F0' and r['frame']==product['frame'] and r['task']==product['task']]
        assert len(args)==1 and args[0]['a0']=='00000028'
        value=int(product['a0'],16)
        assert product['pc']=='FF8DF130' and 0<=value<1000
        assert product['actor']==product['victim'] and product['ids']=='18,4' and product['states']=='1,1'
        popup=any(r['frame']==product['frame'] for r in records.get('SECRET_TOASTY',[]))
        assert popup==(value<40)
        observations.append(dict(frame=product['frame'],task=product['task'],value=value,popup=popup))
    counts={entry:sum(r['entry']==entry for r in decisions) for entry in
            ('FF8DEBF0','FF8DEF20','FF8DF070','FF8DF0F0','FF8DF120','FFA0BA10')}
    return dict(actualNativeDecisions=observations,callChainCounts=counts,
                randomMissesProven=bool(products) and all(not r['popup'] for r in observations),
                missingDecisionPath=not bool(products))
decision=decision_gate(rows)
bad=copy.deepcopy(rows);bad['TOASTY_STOCK_CODE'][0]['mismatches']='1'
try:decision_gate(bad)
except AssertionError:pass
else:raise AssertionError('Changed native code accepted')
faults=['changed native code']
if decision['actualNativeDecisions']:
    bad=copy.deepcopy(rows);next(r for r in bad['TOASTY_DECISION'] if r['entry']=='FF8DF120')['a0']='FFFFFFFF'
    try:decision_gate(bad)
    except AssertionError:faults.append('unbounded random product')
    else:raise AssertionError('Invalid RNG value accepted')
out.mkdir()
report=dict(finiteObservationPassed=True,allPreviousPhysicalAndGameplayRecordsUnchanged=True,
            admission=proof,decision=decision,corruptionsRejected=faults,terminal=terminal,
            stockSHA256=sync.sha(sync.ROOT/'mk2/mk2-maincpu.bin'),logSHA256=sync.sha(folder/'run.log'),
            actualSecretLifecycleAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(decision))
