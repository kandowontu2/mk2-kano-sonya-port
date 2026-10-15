"""Native checkpoints identify floor-gate rejection, without inferring carry."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_leg_attack_guard.py').read_text().replace('audit_current_sonya_p2_kunglao_leg_attack_guard','audit_current_sonya_p2_leg_native_gate_trace')
exec(compile(source,__file__+'::campaign_context','exec'))
import collections
gates=rows.get('SONYA_NATIVE_GATE',[])
assert gates
assert all(r['a8']==r['human_actor'] and r['task_link']==r['human_main'] and int(r['pc'],16)==int(r['checkpoint'],16)+16 for r in gates)
groups=collections.defaultdict(list)
for r in gates:
    if r['a7']=='FFF80800':groups[(r['frame'],r['a13'])].append(r)
floor_reject=[];flag_reject=[];accepted=[]
for (frame,task),sequence in groups.items():
    checks=[r['checkpoint'] for r in sequence]
    if 'FF8771F0' not in checks:continue
    if 'FF877270' in checks and 'FF877420' in checks and 'FF8772F0' not in checks:
        floor_reject.append(dict(frame=int(frame),task=task,heights=[int(r['height']) for r in sequence],checkpoints=checks))
    elif 'FF8772F0' in checks and 'FF877340' not in checks:flag_reject.append(dict(frame=int(frame),task=task,checkpoints=checks))
    elif 'FF877350' in checks:accepted.append(dict(frame=int(frame),task=task,checkpoints=checks))
detail=dict(passedFiniteChecks=True,nativeCheckpointRows=len(gates),floorGateRejections=len(floor_reject),flagGateRejections=len(flag_reject),passedAliveGate=len(accepted),floorRejectionExamples=floor_reject[:12],flagsRejectionExamples=flag_reject[:12],carryRegisterNotRead=True,floorGateRequiresZeroVerticalVelocityAndExactFloor=True,fullPortAccepted=False)
assert floor_reject
(out/'native-gates.json').write_text(json.dumps(detail,indent=2)+'\n')
print(json.dumps(detail))
