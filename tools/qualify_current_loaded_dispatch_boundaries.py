"""Loaded table bytes must preserve originals and real-ID/action extensions."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
prep=sync.ROOT/'audit_current_loaded_dispatch_boundaries_preparation'
case=sync.ROOT/'audit_current_loaded_dispatch_boundaries_runtime'
out=sync.ROOT/'audit_current_loaded_dispatch_boundaries_checked';assert not out.exists()
expected=json.loads((prep/'expected.json').read_text())
assert expected['stockSHA256']==sync.sha(sync.ROOT/'mk2/mk2-maincpu.bin')
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['elapsedSeconds']<92
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(prep/'tables.lua') and not (case/'stderr.log').read_bytes()
text=(case/'run.log').read_text();assert 'LUA ERROR' not in text
records=[(line.split()[0],dict(re.findall(r'(\w+)=([^\s]+)',line))) for line in text.splitlines() if line.startswith('MK2_DISPATCH_')]
def gate(records):
    assert all(r['writes']=='0' and r['assistance']=='none' for _,r in records)
    for name,t in expected['tables'].items():
        actual=[r for tag,r in records if tag=='MK2_DISPATCH_ROW' and r['table']==name]
        assert [int(r['index']) for r in actual]==list(range(len(t['values'])))
        assert [int(r['value'],16) for r in actual]==t['values'],name
    operands=[r for tag,r in records if tag=='MK2_DISPATCH_OPERAND']
    assert len(operands)==len(expected['operands'])
    assert {r['at']:int(r['value'],16) for r in operands}==expected['operands']
    fallback=[r for tag,r in records if tag=='MK2_DISPATCH_FALLBACK']
    assert [int(r['index']) for r in fallback]==list(range(5))
    assert [int(r['value'],16) for r in fallback]==expected['closeFallback']['words']
gate(records)
faults=[]
for name in expected['tables']:
    bad=copy.deepcopy(records)
    next(r for tag,r in bad if tag=='MK2_DISPATCH_ROW' and r['table']==name)['value']='00000000'
    try:gate(bad)
    except AssertionError:faults.append(name)
    else:raise AssertionError('Loaded table corruption accepted')
report=dict(passed=True,loadedTableRows=sum(len(t['values']) for t in expected['tables'].values()),loadedOperands=len(expected['operands']),stockRowsComparedToOriginalROM=True,
    addedIdRowsVerified=True,ownedSpecialRoutersVerified=True,stockCloseFallbackVerified=True,effectiveLoadedFaultsRejected=faults,terminal=terminal,
    allOriginalAiEnemyIdLookupsAudited=False,gameplayAcceptance=False,fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
