"""Preserve native blade-fury shake grammar with own corresponding stumble art."""
import json
from pathlib import Path
import re
from inventory_character_tables import source_tables
PORT=Path(__file__).resolve().parent
OUT=PORT/'generated_reactions'
def main():
    native=(PORT.parent/'baseline/mk2-rebuild-main/srcw/MKLK.ASM').read_text()
    tables=source_tables(native)
    native_poses=[v for row in tables['a_lkstumble']['rows'] for v in row['values'] if v!='0']
    assert native_poses==[f'LKSTUMBLE{i}' for i in range(1,6)]
    text=native[native.index('\na_shredded\n'):native.index('\n***********************************************',native.index('\na_shredded\n'))]
    lines=['; Own blade-fury victim DATA, exact native shake/loop controls.',
           '        .include mainequ.asm','        .data'];report={}
    for actor in ('kano','sonya'):
        candidate=source_tables((PORT/'generated_templates_candidate'/f'{actor.upper()}ANI.ASM').read_text())
        own=[v for row in candidate[f'ks_{actor}_main_23']['rows'] for v in row['values'] if v!='0']
        assert len(own)==5 and all(v.startswith(f'ks_{actor}_pose_') for v in own)
        mapping=dict(zip(native_poses,own));root=f'ks_{actor}_shredded';mapping['a_shredded']=root
        for pose in own[:3]:lines += [f'        .ref {pose}']
        lines += [f'        .def {root}',re.sub(r'\b[A-Za-z_]\w*\b',lambda m:mapping.get(m[0],m[0]),text)]
        report[actor]=dict(nativeToOwnPoseMapping=mapping,preservesNativeAdjustmentsAndLoop=True,runtimeVerified=False)
    OUT.mkdir(exist_ok=True)
    (OUT/'KSSHRED.ASM').write_text('\n'.join(lines)+'\n')
    (OUT/'SHRED_SOURCE.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Generated own blade-fury victim scripts; runtime tests pending.')
if __name__=='__main__':main()
