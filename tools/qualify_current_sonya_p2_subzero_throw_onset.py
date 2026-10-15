"""Verify observer neutrality and native ownership of throw initiations."""
from pathlib import Path
import collections
source=Path(__file__).with_name('qualify_current_sonya_p2_subzero_contact_trace.py').read_text()
source=source.replace('audit_current_sonya_p2_subzero_contact_trace','audit_current_sonya_p2_subzero_throw_onset')
source=source.replace("'SONYA_SUBZERO_DAMAGE','HOST_BOUND'","'SUBZERO_THROW_START','SONYA_SUBZERO_DAMAGE','HOST_BOUND'")
exec(compile(source,__file__+'::contact_gate','exec'))
reference=chronology.load(sync.ROOT/'audit_current_sonya_p2_subzero_contact_trace_runtime/run.log')
cutoff=min(last(rows),last(reference))
for tag in set(rows)|set(reference):
    if tag not in ('SUBZERO_THROW_START','HOST_BOUND','RESULT','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in reference.get(tag,[]) if int(r['frame'])<cutoff],tag
starts=rows['SUBZERO_THROW_START'];assert starts
def valid(r):
    return r['a8']==r['cpu_actor'] and r['a13']==r['cpu_main'] and int(r['at'],16)==int(r['cpu_main'],16)+0x1f0 and r['pc']=='FF8B6FA0'
assert all(valid(r) for r in starts)
for key in ('a8','a13','at','pc'):
    fault=dict(starts[0]);fault[key]='00000000';assert not valid(fault)
plans=rows.get('SONYA_SUBZERO_RING_PLAN',[])
detail=dict(passed=True,neutralBefore=cutoff,throwStarts=len(starts),
    gaps=[int(r['gap']) for r in starts],
    actionHardwareCounts=dict(collections.Counter(r['action']+':'+r['hardware'] for r in starts)),
    within64FieldsAfterRingPlan=sum(any(0<=int(r['frame'])-int(p['frame'])<64 for p in plans) for r in starts),
    faultCasesRejected=4,fullCampaignAccepted=False,fullPortAccepted=False)
(out/'throw-onset.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
