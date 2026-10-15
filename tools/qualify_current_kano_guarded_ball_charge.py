"""Require actual owned cannonball entry following84physical held-LK fields."""
import json,re
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_guarded_ball_charge_runtime'
out=sync.ROOT/'audit_current_kano_guarded_ball_charge_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
rows={}
for line in (folder/'run.log').read_text().splitlines():
    assert '[LUA ERROR]' not in line
    if line.startswith('MK2_HSPECIAL_'):
        rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
entry=rows['GUARDED_BALL_ENTRY']
assert len(entry)==1 and entry[0]['id']=='17' and entry[0]['actor']==entry[0]['owner'] and int(entry[0]['charge_age'])>=84
start=int(rows['COMMAND'][0]['frame'])
for button in ('Low_Kick','Down','Block'):
    fields={int(r['frame']) for r in rows['INPUT'] if r['slot']=='1' and r['button']==button and start<=int(r['frame'])<start+84}
    assert fields==set(range(start,start+84)),button
assert all(r['roster']==r['id']==('17' if r['slot']=='1' else '18') for r in rows['FIELD'])
report=dict(passedPhysicalGuardedCharge=True,nativeEntry=entry[0],physicalChargeFields=84,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),cpuCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(passed=True,nativeEntry=entry[0])))
