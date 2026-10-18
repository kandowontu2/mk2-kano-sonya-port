"""Assemble the native playback test against the REAL full-game linker inputs."""
import json
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
BUILD=HERE.parent/'baseline/mk2-rebuild-main'
SRC=BUILD/'srcw'
def main():
    coverage=json.loads((HERE/'generated_templates_throws/TRANSLATION.json').read_text())
    lines=['; Generated typed playback matrix, not an action dispatch table.','        .data']
    for fighter in ('kano','sonya'):
        table=f'ks_art_{fighter}_animations'
        lines += [f'        .def {table}',table]
        for index,entry in sorted(coverage['fighters'][fighter]['entries'].items(),key=lambda kv:int(kv[0])):
            label=entry['label']
            lines += [f'        .ref {label}',f'        .word {index}',f'        .long {label}']
        lines += ['        .word -1','        .long 0']
    (SRC/'KSCYCLE.ASM').write_text('\n'.join(lines)+'\n')
    (SRC/'KSCENE.ASM').write_bytes((HERE/'diagnostics/KSCENE.ASM').read_bytes())
    link=(SRC/'ARTTEST.CMD').read_text()
    link=link.replace('ARTTEST.OUT','CYCTEST.OUT').replace('ARTTEST.MAP','CYCTEST.MAP')
    assert link.count('KSART.OBJ')==1
    link=link.replace('KSART.OBJ','KSCENE.OBJ\nKSCYCLE.OBJ')
    (SRC/'CYCLE.CMD').write_text(link)
    learn=(SRC/'rom/ART.LRN').read_text().replace('ARTTEST.OUT','CYCTEST.OUT').replace('A12','C12')
    (SRC/'rom/CYCLE.LRN').write_text(learn)
    print('Prepared native 51-script/character initial-phase playback test')
if __name__=='__main__':main()
