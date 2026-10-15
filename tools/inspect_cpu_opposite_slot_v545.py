"""Four independently checked actual opposite-slot grabs, never full-port acceptance."""
import hashlib
import json
import sys
from pathlib import Path
import verify_cpu_recovery_v545_v3 as c

CASES=(('audit_v578_p2cpu_sonya_boot600','sonya','bicycle'),
       ('audit_v578_p2cpu_kano_boot602','kano','ordinary'),
       ('audit_v578_p2cpu_kano_boot600','kano','ordinary'),
       ('audit_v578_p2cpu_cage_boot600','cage','ordinary'))

def verify():
    inputs={};proofs=[];errors=[];scouts=[]
    for name,player,move in CASES:
        folder=c.ROOT/name;proof=c.verify(folder,player,move);proof['capture']=name
        if not proof['passed']:errors.extend(proof['errors'])
        c.matched(folder,inputs);proofs.append(proof)
    accepted={name for name,_,_ in CASES}
    folders=sorted([*c.ROOT.glob('audit_v577_*'),*c.ROOT.glob('audit_v578_*')])
    for folder in folders:
        c.matched(folder,inputs)
        if folder.name not in accepted:
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            cold=c.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ')
            results=c.rows(log,'RESULT')
            if len(cold)!=1 or len(results)!=1 or cold[0]['writes']!=0 or results[0]['assistance']!='none':
                errors.append('One real input-only cold scout required: '+folder.name)
            scouts.append(dict(capture=folder.name,accepted=False,cpu_id=cold[0]['cpu_id'],
                               completed_frame=results[0]['complete'],cycles=results[0]['cycles'],
                               scope='preserved_natural_scout_not_full_grab_and_continuation_acceptance'))
        for path in folder.rglob('*'):
            if path.is_file():inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    return dict(passed=not errors,errors=errors,fullPortAcceptance=False,cases=proofs,scouts=scouts,
                paired_fields=sum(p['paired_fields']for p in proofs),
                held_fields=sum(p['held_fields']for p in proofs),
                victim_flight_fields=sum(p['victim_flight_fields']for p in proofs),inputHashes=inputs,
                scope='four_actual_P2_CPU_full_grabs_one_complete_bicycle_miss_three_original_next_action_lock_cleanups_not_universal_move_or_art_audio_campaign_acceptance')

if __name__=='__main__':
    proof=verify();print(json.dumps(proof,indent=2));sys.exit(0 if proof['passed']else 1)
