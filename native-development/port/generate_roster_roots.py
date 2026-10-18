"""Declare independent native roster roots; explicitly mark unfinished states.

Development candidate only. Missing states are observable and cannot be counted
as implemented just because their dispatch cell has a safe, non-random pointer.
"""
import hashlib
import argparse
import json
from special_root_contract import ROOTS, ROLES
from pathlib import Path
HERE=Path(__file__).resolve().parent
TEMPLATES=HERE/'generated_templates_candidate'
OUT=HERE/'generated_roster_roots'
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--refresh-generated',action='store_true')
    args=parser.parse_args()
    assert not OUT.exists() or args.refresh_generated
    coverage=json.loads((TEMPLATES/'TRANSLATION.json').read_text())
    assert coverage['nativeMainEntries']==66 and coverage['nativeSpecialEntries']==7
    lines=['; DEVELOPMENT roster roots. Missing-state markers are NOT move implementations.',
           '        .include dispequ.asm','        .include sysequ.asm',
           '        .include mainequ.asm',
           '        .def ks_missing_animation_count,ks_missing_animation_tag,ks_missing_animation_actor',
           '        .bss ks_missing_animation_count,32',
           '        .bss ks_missing_animation_tag,16',
           '        .bss ks_missing_animation_actor,16','        .data']
    refs=set();missing=set();report={}
    for fighter in ('kano','sonya'):
        actor=coverage['fighters'][fighter]
        assert '37' not in actor['entries'] and '30' in actor['entries']
        entries={int(i):entry['label'] for i,entry in actor['entries'].items()}
        # Native DUMMY is an explicit alias of the stance, not a fallback for
        # unknown animations. Keep it as the new actor's own stance as well.
        entries[64]=f'ks_{fighter}_stance'
        entries[55]=f'ks_{fighter}_bike_victim'
        entries[58]=f'ks_{fighter}_banged'
        entries[62]=f'ks_{fighter}_kintaro_thrown'
        # Ordinary throw queries must expose the actual own three-phase body
        # script, not the superseded Liu-template phase translation.
        entries[36]=f'ks_{fighter}_throw_phase0'
        entries[63]=f'ks_{fighter}_back_broke'
        entries[61]=f'ks_{fighter}_head'
        entries[60]=f'ks_{fighter}_decapfall'
        entries[56]=f'ks_{fighter}_drain_reaction'
        entries[57]=f'ks_{fighter}_torso_ripped'
        entries[65]=f'ks_{fighter}_swipe_torso'
        entries[38]=f'ks_{fighter}_projectile_release'
        entries[39]=f'ks_{fighter}_projectile_effect'
        entries[37]=f'ks_{fighter}_shredded'
        entries[59]=f'ks_{fighter}_impaled'
        # Native MKFN's empty a_nutcrunched label aliases a_bike_kicked.
        # Female immunity prevents this from being a male nut-punch reaction.
        if fighter=='sonya':entries[54]='ks_sonya_bike_victim'
        else:entries[54]='ks_kano_nutcrunched'
        overrides={0:'stance',1:'walk_forward',3:'walk_backward',5:'crouch',6:'vertical_jump',7:'forward_flip',8:'backward_flip'}
        for i,role in overrides.items():entries[i]=f'ks_{fighter}_{role}'
        main=f'ks_{fighter}_anitab1';special=f'ks_{fighter}_anitab2'
        lines += [f'        .def {main},{special}',main]
        for i in range(66):
            target=entries.get(i,f'ks_missing_main_{i:02x}')
            if i not in entries:missing.add(('main',i))
            else:refs.add(target)
            lines.append(f'        .long {target} ; main {i:02x}')
        lines.append(special)
        for i,target in enumerate(ROOTS[fighter]):
            refs.add(target)
            lines.append(f'        .long {target} ; own special {i:02x}: {ROLES[i]}')
        report[fighter]=dict(nativeMainEntries=66,nativeSpecialEntries=7,
            implementedMainEntries=len(entries),missingMainEntries=sorted(set(range(66))-entries.keys()),
            missingSpecialEntries=[],implementedSpecialEntries=7,
            ownSpecialRootRoles=dict(enumerate(ROLES)),nativeDummyAliasOwnStance=True,playable=False)
    for label in sorted(refs):lines.insert(1,f'        .ref {label}')
    for kind,i in sorted(missing):
        tag=i+(0x100 if kind=='special' else 0)
        lines += [f'ks_missing_{kind}_{i:02x}',f'        .long ani_calla,ks_mark_{kind}_{i:02x}','        .long 0']
    lines += ['        .text']
    for kind,i in sorted(missing):
        tag=i+(0x100 if kind=='special' else 0)
        lines += [f'ks_mark_{kind}_{i:02x}',f'        movi {tag},a0','        jauc ks_missing_animation_mark']
    lines += ['ks_missing_animation_mark',
              '        move a0,@ks_missing_animation_tag,w',
              '        move *a8(ochar),a0,w',
              '        move a0,@ks_missing_animation_actor,w',
              '        move @ks_missing_animation_count,a0,l',
              '        addk 1,a0',
              '        move a0,@ks_missing_animation_count,l','        rets']
    OUT.mkdir(exist_ok=True);content=('\n'.join(lines)+'\n').encode();(OUT/'KSROOT.ASM').write_bytes(content)
    result=dict(sourceSHA256=hashlib.sha256(content).hexdigest().upper(),fighters=report,
                complete=not missing,fullPortVerified=False,
                releaseGate='Root coverage alone does not prove gameplay; any nonzero missing-state counter rejects final acceptance',
                actorIDSubstitution=False,ordinaryJumpKickIndependentOfSpecialMoves=True,
                rejectedPrototypeMapping=dict(mainIndex=37,sourceRole='a_shredded',incorrectPrototypeRole='short stumble'))
    (OUT/'ROOT_COVERAGE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
