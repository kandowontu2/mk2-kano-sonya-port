"""Record real baseline/module evidence, without claiming port completion."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import zipfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ZIP=Path('C:/Users/kando/Downloads/mk2-rebuild-main.zip')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def main():
    module=HERE/'mk2-rebuild-main/srcw'
    linked=(module/'PORT.MAP').read_text()
    assert 'PORT.OUT' in linked and 'KSCMD.OBJ' in linked
    pins={}
    for name in ('KANOASM.LOG','SONYAASM.LOG','CMDASM.LOG','KANOART.LOG','SONYAART.LOG','ANIMASM.LOG','KANOANI.LOG','SONYAANI.LOG','UIASM.LOG','NAVASM.LOG'):
        p=HERE/'mk2-rebuild-main'/name
        assert 'No Errors,  No Warnings' in p.read_text()
        pins[str(p.relative_to(ROOT))]=sha(p)
    assert 'undefined' not in (HERE/'mk2-rebuild-main/PORTLINK.LOG').read_text().lower()
    art=json.loads((HERE.parent/'port/generated_packed/ART_IMPORT.json').read_text())
    for fighter in ('kano','sonya'):
        name=fighter.upper()+'ART.OBJ'
        match=re.search(r'([0-9a-f]+)\s+'+re.escape(name)+r' \(\.data\)',linked,re.I)
        assert match and int(match[1],16)//8==art['fighters'][fighter]['expectedDataBytes']
    with zipfile.ZipFile(ZIP) as z:
        name='mk2-rebuild-main/src/DIAGDTST.ASM'
        original=z.read(name).decode('cp437').splitlines(keepends=True)
        current=(HERE/name).read_text().splitlines(keepends=True)
        # Normalize newlines before diff; only actual diagnostic guards matter.
        diff=''.join(difflib.unified_diff([x.rstrip('\r\n')+'\n' for x in original],
                       [x.rstrip('\r\n')+'\n' for x in current],fromfile='original/DIAGDTST.ASM',tofile='repaired/DIAGDTST.ASM'))
        (HERE/'tunit_diagnostic_guards.patch').write_text(diff)
    tests={}
    for name in ('stock_mame_input_test','stock_wolf_correct_lanes_test','stock_wolf_native_audio_test'):
        p=HERE/name/'execution.json'
        if p.exists():
            record=json.loads(p.read_text()); assert record['exitCode']==0 and not record['timedOut']
            tests[name]=record; pins[str(p.relative_to(ROOT))]=sha(p)
            csv=HERE/name/'probe.csv'; rows=csv.read_text().splitlines()
            assert len(rows)==201 and rows[-1].startswith('12000,')
            pins[str(csv.relative_to(ROOT))]=sha(csv)
    for path in list((HERE.parent/'port/asm').glob('*.ASM'))+list((HERE.parent/'port/generated_packed').glob('*.ASM'))+list((HERE.parent/'port/generated_templates_throws').glob('*.ASM'))+list((HERE.parent/'port/generated_ui_packed').glob('*.ASM'))+[module/'PORT.OUT',module/'PORT.MAP']:
        pins[str(path.relative_to(ROOT))]=sha(path)
        if path.suffix.upper()=='.ASM':
            assert path.read_bytes()==(module/path.name).read_bytes(), f'Assembler input differs: {path.name}'
            assert (module/path.with_suffix('.OBJ').name).stat().st_mtime >= (module/path.name).stat().st_mtime-3
    result=dict(inputZIP=str(ZIP),inputZIPSHA256=sha(ZIP),baselineSmokeTests=tests,
                firstAssemblyModulesLink=True,typedArtByteCountsMatchLinkMap=True,
                portPlayable=False,portComplete=False,releaseReady=False,files=pins)
    (HERE/'EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(tests=list(tests),moduleLink=True,portPlayable=False,releaseReady=False),indent=2))
if __name__=='__main__': main()
