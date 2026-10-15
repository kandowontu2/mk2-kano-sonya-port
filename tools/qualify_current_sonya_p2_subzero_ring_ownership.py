"""Supplement current test with exact real-ID special owner and fault checks."""
import copy,json
import verify_native_source_sync as sync
sync.verify()
prior=sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_checked/report.json'
report=json.loads(prior.read_text())
assert report['finiteEvidenceVerified']
assert report['logSHA256']==sync.sha(sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_runtime/run.log')
def gate(data):
    rings=data['nativeRingEntries'];assert rings
    assert all(r['id']==r['roster']=='18' and r['actor']==r['a8'] and r['main']==r['a13'] and r['entry']=='FFFFB400' and r['stage']=='1' for r in rings)
    assert all(r['slot']=='2' and r['id']=='18' and r['entry']=='FFFEFA40' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in data['subzeroOwnWins'])
    return len(rings)
count=gate(report)
for fault in ('proxy','owner','winner'):
    bad=copy.deepcopy(report)
    if fault=='proxy':bad['nativeRingEntries'][0]['id']='1'
    elif fault=='owner':bad['nativeRingEntries'][0]['a8']='DEADBEEF'
    else:bad['subzeroOwnWins'][0]['slot']='1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Invalid proof accepted: '+fault)
out=sync.ROOT/'audit_current_sonya_p2_subzero_ring_ownership_checked';assert not out.exists();out.mkdir()
result=dict(passed=True,ownedNativeRingEntries=count,proxyFaultRejected=True,ownerFaultRejected=True,wrongWinnerFaultRejected=True,
            subzeroMatchCleared=False,fullCampaignAccepted=False,fullPortAccepted=False,priorReportSHA256=sync.sha(prior))
(out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
