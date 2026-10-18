"""Typed own projectile roots, preserving native body/effect palette ownership."""
import json
from pathlib import Path
from inventory_character_tables import source_tables
PORT=Path(__file__).resolve().parent
OUT=PORT/'generated_projectiles'
def values(table):
    return [v for row in table['rows'] for v in row['values']]
def poses(table):
    result=[]
    for v in values(table):
        if v in ('0','ani_jump'):break
        result.append(v)
    return result
def main():
    animations=source_tables((OUT/'KSPJANI.ASM').read_text())
    lines=['; Own native main26/main27 typed roots. No executable binary arrays.',
           '        .include mainequ.asm','        .ref ks_knife_palette,ks_ring_palette,ks_ring_charge_palette',
           '        .data']
    report={}
    for actor,effect in (('kano','knife'),('sonya','ring')):
        art=source_tables((PORT/'generated_packed'/f'{actor.upper()}ART.ASM').read_text())
        release=poses(animations[f'ks_{effect}_release'])
        charge=poses(animations['ks_ring_charge']) if actor=='sonya' else []
        for name in charge+release:lines += [f'        .ref {name}']
        root=f'ks_{actor}_projectile_release'
        lines += [f'        .def {root}',root]
        if charge:lines += ['        .long ani_calla,ks_ring_root_palette_on']
        lines += [f'        .long {name}' for name in charge]
        if charge:lines += ['        .long ani_calla,player_normpal']
        lines += [f'        .long {name}' for name in release]+['        .long 0']
        intro=poses(animations[f'ks_{effect}_intro']) if actor=='kano' else poses(animations['ks_ring_flight'])
        flight=poses(animations[f'ks_{effect}_flight'])
        aliases={};frames={}
        for pose in dict.fromkeys(intro+flight):
            composite=[]
            for frame in values(art[pose]):
                if frame=='0':break
                if frame not in frames:
                    label=f'ks_pe_{actor}_{len(frames)}';frames[frame]=label
                    rows=art[frame]['rows']
                    assert [r['type'] for r in rows]==['word','long','word','long']
                    assert len(rows[0]['values'])==4 and rows[-1]['values']==[f'ks_{actor}_primary_palette']
                    lines += [f'        .def {label}',label]
                    for row in rows[:-1]:lines += ['        .'+row['type']+' '+','.join(row['values'])]
                    lines += [f'        .long ks_{effect}_palette']
                composite.append(frames[frame])
            assert composite
            label=f'ks_pp_{actor}_{len(aliases)}';aliases[pose]=label
            lines += [f'        .def {label}',label,'        .long '+','.join(composite+['0'])]
        root=f'ks_{actor}_projectile_effect'
        lines += [f'        .def {root}',root]
        for section in (intro,flight):
            lines += [f'        .long {aliases[p]}' for p in section]+['        .long 0']
        report[actor]=dict(release=release,charge=charge,intro=intro,flight=flight,
            descriptorAliases=frames,compositeAliases=aliases,phaseTerminators=2,runtimeVerified=False)
    lines += ['        .text','ks_ring_root_palette_on','        movi ks_ring_charge_palette,a0',
              '        jauc player_swpal']
    (OUT/'KSPJROOT.ASM').write_text('\n'.join(lines)+'\n')
    (OUT/'PROJECTILE_ROOTS.json').write_text(json.dumps(dict(actors=report,linked=False,fullPortVerified=False),indent=2)+'\n')
    print(json.dumps({a:dict(imageAliases=len(r['descriptorAliases']),introFrames=len(r['intro']),flightFrames=len(r['flight'])) for a,r in report.items()}))
if __name__=='__main__':main()
