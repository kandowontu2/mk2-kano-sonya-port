"""Fresh current CPU contracts plus retained non-passing natural scouts.

Never count a missing action, KO or unrelated follow-up as a completed fixture.
Reports all attempted captures and pins the complete runtime artifact inventory.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import verify_natural_cpu_moves_v635 as natural
import verify_cpu_recovery_v635_v4 as ordinary
import verify_cpu_followup_v635_v2 as special
import verify_cpu_projectile_followup_v635 as projectile

ROOT=natural.ROOT
PAIR_PROFILES={
    'audit_v661_cpu_pair_cage_boot605':('cage','ordinary'),
    'audit_v661_cpu_pair_sub_zero_boot605':('sub_zero','ordinary'),
    'audit_v661_cpu_pair_liu_kang_boot605':('liu_kang','square'),
    'audit_v663_cpu_guard_cage_boot605':('cage','ordinary'),
    'audit_v663_cpu_guard_sub_zero_boot605':('sub_zero','ordinary'),
    'audit_v663_cpu_guard_raiden_boot605':('raiden','ordinary'),
    'audit_v663_cpu_guard_mileena_boot605':('mileena','ordinary'),
    'audit_v663_cpu_guard_kano_boot605':('kano','square'),
    'audit_v663_cpu_guard_liu_kang_boot605':('liu_kang','square'),
    'audit_v663_cpu_guard_sonya_boot605':('sonya','bicycle'),
    'audit_v663_cpu_guard_kitana_boot605':('kitana','bicycle'),
    'audit_v664_cpu_close_cage_boot604':('cage','ordinary'),
    'audit_v664_cpu_close_raiden_boot604':('raiden','ordinary'),
}


def attempt(fn,*args):
    try:return fn(*args)
    except (OSError,ValueError,KeyError,IndexError,TypeError,AssertionError) as error:
        return dict(passed=False,errors=[str(error)],whole_character_integration_complete=False)


def inventory(cases):
    inputs={}
    def add(path):
        inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    for folder in cases:
        for file in folder.rglob('*'):
            if file.is_file():add(file)
        manifest=folder/'input_hashes_before.json'
        if manifest.exists():
            for path,expected in json.loads(manifest.read_text(encoding='utf-8-sig')).items():
                file=Path(path);add(file)
                if inputs[str(file)]!=expected:raise ValueError('Launch input changed: '+path)
    # Record actual transitive verifier modules loaded, not just top-level checks.
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':add(path)
    add(Path(__file__).resolve())
    add(ROOT/'mk2/mk2-maincpu.bin')
    return inputs


def report():
    cases=sorted(p for p in ROOT.iterdir() if p.is_dir() and
                 any(p.name.startswith('audit_v'+str(v)+'_cpu_') for v in range(660,665)))
    proofs={};scouts={}
    for folder in cases:
        if not (folder/'result.json').exists():raise ValueError('Capture is not terminal: '+folder.name)
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        if 'opponent_id' in meta:
            proofs[folder.name]=attempt(natural.verify,folder)
        elif folder.name in PAIR_PROFILES:
            player,profile=PAIR_PROFILES[folder.name]
            proofs[folder.name]=attempt(ordinary.verify,folder,player) if profile=='ordinary' else \
                                attempt(special.verify,folder,player,profile)
        elif folder.name.endswith('ring_block') or folder.name.endswith('ring_duck'):
            duck=folder.name.endswith('ring_duck')
            proofs[folder.name]=attempt(projectile.verify,folder,18,'duck_miss' if duck else 'block','v3' if duck else 'v2')
        else:
            scouts[folder.name]=dict(
                terminal=ordinary.rows(log,'RESULT'),entries=len(ordinary.rows(log,'ENTRY')),
                complete=ordinary.rows(log,'COMPLETE'),
                full_contact_accepted=False,
                reason='No declared passing complete contact/follow-up contract; retained scout, not a pass')
    return dict(candidate=natural.CANDIDATE,proofs=proofs,unaccepted_scouts=scouts,
                verified_fixtures=sum(p.get('passed',False) for p in proofs.values()),
                nonpassing_contracts=[name for name,p in proofs.items() if not p.get('passed')],
                CPU_acceptance=False,whole_character_integration_complete=False,
                scope='fresh_declared_current_natural_CPU_contacts_and_retained_scouts_not_all_moves_victims_slots_pixels_KO_audio_or_full_goal',
                checked_inputs=inventory(cases))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise SystemExit('Refusing to overwrite evidence')
    proof=report();args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({k:v for k,v in proof.items() if k!='checked_inputs'},indent=2))
