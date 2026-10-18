"""Declare own main38 lead-in with the native typed adjustment grammar."""
from pathlib import Path
import re
PORT=Path(__file__).resolve().parent
lines=['; Native soul-drain lead-in DATA using own recoil/dizzy composites.',
       '        .include mainequ.asm','        .data']
for actor in ('kano','sonya'):
    source=(PORT/'generated_templates_candidate'/f'{actor.upper()}ANI.ASM').read_text()
    def first(index):
        match=re.search(r'(?m)^ks_'+actor+'_main_'+index+r'\s*\n\s*\.long\s+(\w+)',source)
        assert match
        return match[1]
    recoil,dizzy=first('10'),first('28')
    root=f'ks_{actor}_drain_reaction'
    lines += [f'        .ref {recoil},{dizzy}',f'        .def {root}',root,
              '        .long ani_adjustxy','        .word -048h,-013h',
              f'        .long {recoil},0']
    for x,y in ((-10,26),(19,-8),(8,-20),(0,0)):
        lines += ['        .long ani_adjustxy',f'        .word {x},{y}',f'        .long {dizzy}']
    lines += ['        .long 0']
(PORT/'generated_drain/KSDRAIN.ASM').write_text('\n'.join(lines)+'\n')
print('Generated two own native main38 reaction scripts; runtime alignment pending.')
