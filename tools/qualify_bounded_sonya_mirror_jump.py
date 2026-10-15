"""Retain failed physical jump policy without claiming a port defect or clear."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

folder=sync.ROOT/'audit_bounded_sonya_mirror_jump_runtime'
out=sync.ROOT/'audit_bounded_sonya_mirror_jump_observed';assert not out.exists()
t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and t['rawMedia']=='none'
assert not (folder/'stderr.log').read_text().strip()
rows={}
for line in (folder/'run.log').read_text().splitlines():
    assert '[LUA ERROR]' not in line
    if line.startswith('MK2_NAT_CAMPAIGN_'):
        rows.setdefault(line.split()[0][17:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
assert len(rows['RESULT'])==len(rows['HOST_BOUND'])==1 and rows['RESULT'][0]['frame']=='12000'
assert rows['LIVE'] and all(r['human']==r['cpu']=='18:18' and r['stage']=='0' and r['schedule']=='FFFA3180' for r in rows['LIVE'])
assert rows['LOSS'] and all(r['roster']=='18' for r in rows['SELECT_ID'])
assert all(r['slot']=='1' and r['id']=='18' and r['health'].split(',')[1]=='0' for r in rows['WIN'])
report=dict(passed=True,terminal=t,paidLosses=len(rows['LOSS']),sampledMirrorCombatFields=len(rows['LIVE']),firstOpponentCleared=False,gameDefectProven=False,sourceSync=sync.verify(),logSHA256=sync.sha(folder/'run.log'),checkerSHA256=sync.sha(Path(__file__)),scope='Existing jump controller fails natural Sonya mirror; identities and continue flow intact. No game or difficulty changes justified.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,controllerFailed=True,identityPreserved=True)))
