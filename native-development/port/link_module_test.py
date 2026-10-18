"""Resolve first assembly modules against actual rebuilt engine symbols.

This only tests assembly/linking; it does not install/select the new fighters.
No guessed retail helper addresses or emulated memory modifications.
"""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'baseline/mk2-rebuild-main/srcw'
def main():
    symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_][A-Za-z0-9_]*)', (SRC/'MK2NEW.MAP').read_text())}
    refs=set(); definitions=set()
    for file in list((HERE/'asm').glob('*.ASM'))+list((HERE/'generated_packed').glob('*.ASM'))+list((HERE/'generated_templates_throws').glob('*.ASM'))+list((HERE/'generated_ui_packed').glob('*.ASM')):
        for row in file.read_text().splitlines():
            if row.strip().startswith('.ref '): refs.update(row.split('.ref',1)[1].strip().split(','))
            if row.strip().startswith('.def '): definitions.update(row.split('.def',1)[1].strip().split(','))
    refs-=definitions
    missing=refs-symbols.keys()
    assert not missing, f'Unresolved native engine symbols: {sorted(missing)}'
    cmd=['-o PORT.OUT','-m PORT.MAP','KANOMOV.OBJ','SONYAMOV.OBJ','KSCMD.OBJ','KANOART.OBJ','SONYAART.OBJ','KSANIM.OBJ','KANOANI.OBJ','SONYAANI.OBJ','KSUI.OBJ','KSNAV.OBJ']
    cmd += [f'{name} = 0x{symbols[name]:08x};' for name in sorted(refs)]
    cmd += ['f_norepell = 0x%08x;'%symbols['f_norepell'],
            'MEMORY { ROM: org=0xffe00000, len=0x80000 }',
            'SECTIONS { .text: {} > ROM .data: {} > ROM }']
    (SRC/'PORT.CMD').write_text('\n'.join(cmd)+'\n')
    print(f'Resolved {len(refs)} engine symbols from actual Wolf link map')
if __name__=='__main__': main()
