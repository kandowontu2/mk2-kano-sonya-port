"""Direct same-base native prefix; do not inherit unrelated earlier trial gates."""
import json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_sonya_p2_baraka_hk_spacing90_runtime'
out=root/'audit_current_sonya_p2_baraka_hk_spacing90_v2_checked';assert not out.exists()
def load(path):
    rows=[]
    for s in path.read_text().splitlines():
        assert 'LUA ERROR' not in s
        if s.startswith('MK2_NAT_CAMPAIGN_'):rows.append((s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))))
    return rows
rows=load(case/'run.log');prior=load(root/'audit_current_sonya_p2_baraka_hk_guard_ready_runtime/run.log')
assert [(t,r) for t,r in rows if int(r['frame'])<=50237]==[(t,r) for t,r in prior if int(r['frame'])<=50237]
damage=[r for t,r in rows if t=='SONYA_BARAKA_DAMAGE'];assert damage
assert all(r['ids']=='3,18' and int(r['after'])<int(r['before'])<=161 for r in damage)
wins=[r for t,r in rows if t=='WIN' and r['stage']=='6' and r['slot']=='2']
assert all(r['id']=='18' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'));assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
report=dict(earlierNativeAndPhysicalRecordsExactlyPreservedThrough=50237,ownBarakaRounds=wins,
    stage7Observed=any(t=='STAGE' and r['stage']=='7' for t,r in rows),
    incomingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),
    outgoingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
    terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullPortAccepted=False,
    caveat='Raw HP totals across altered histories are not normalized improvement; isolated round wins are not a match clear.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
