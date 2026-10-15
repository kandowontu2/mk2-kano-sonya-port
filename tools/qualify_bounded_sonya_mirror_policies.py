"""Do not mistake losses from simple controllers for failed special activation."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    groups={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            groups.setdefault(line.split()[0][17:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return groups

out=sync.ROOT/'audit_bounded_sonya_mirror_policies_checked';assert not out.exists()
proof_path=sync.ROOT/'audit_bounded_campaign_progress_checked/report.json';proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
for policy,name in (('defensive_leg','audit_bounded_campaign_progress_core_sonya_p2_runtime'),('zoning','audit_bounded_sonya_mirror_zoning_runtime')):
    folder=sync.ROOT/name
    if policy=='defensive_leg':assert sync.sha(folder/'run.log')==proof['results']['sonyaP2']['logSHA256']
    t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and t['rawMedia']=='none'
    rows=load(folder);assert rows['RESULT'][0]['frame']=='12000'
    assert all(r['human']=='18:18' and r['cpu']=='18:18' and r['stage']=='0' and r['schedule']=='FFFA3180' for r in rows['LIVE'])
    assert all(r['roster']=='18' for r in rows['SELECT_ID'])
    losses=rows.get('LOSS',[]);assert losses
    assert all(r['slot']=='1' and r['id']=='18' and r['pc']=='FF8296B0' and r['health'].split(',')[1]=='0' for r in rows['WIN'])
    special=rows.get('SPECIAL',[])
    if policy=='defensive_leg':
        assert len(special)==36
        assert all(r['move']=='leg' and r['id']==r['roster']=='18' and r['actor']==r['a8'] and r['main']==r['a13'] for r in special)
    results[policy]=dict(terminal=t,firstOpponentWasNaturalSonyaMirror=True,paidMatchLosses=len(losses),actualOwnedLegEntries=len(special) if policy=='defensive_leg' else None,identityPreserved=True,firstOpponentCleared=False,lossCauseProven=False,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),priorProofSHA256=sync.sha(proof_path),scope='Both existing physical policies fail natural Sonya mirror; defensive leg activates36 times with true owners. Evidence does not prove a gameplay defect or campaign clear. No game/AI/difficulty change justified.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,ownedLegActivationVerified=True,bothControllerPoliciesFailed=True)))
