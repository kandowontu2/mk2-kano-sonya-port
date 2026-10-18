"""Check all146 own dispatch cells in linked ROM bytes; not animation QA."""
import hashlib
import json
from pathlib import Path
import re
import struct

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def pointers(source,label,count):
    match=re.search(r'^'+re.escape(label)+r'\s*\n((?:[ \t]+\.long[^\n]*\n)+)',source,re.M)
    assert match,('Missing dispatch table',label)
    values=[]
    for line in match[1].splitlines():
        entry=re.fullmatch(r'\s*\.long\s+(\w+)\s*;.*',line)
        assert entry,('Unexpected dispatch expression',label,line)
        values.append(entry[1])
    assert len(values)==count,(label,len(values),count)
    assert not any(value.startswith('ks_missing_') for value in values)
    return values

def read_long(program,address):
    assert 0xff800000<=address<=0xffffffe0 and (address-0xff800000)%8==0
    offset=(address-0xff800000)//8
    assert offset+4<=len(program)
    return struct.unpack_from('<I',program,offset)[0]

def main():
    root=PORT/'generated_roster_roots/KSROOT.ASM'
    coverage_path=PORT/'generated_roster_roots/ROOT_COVERAGE.json'
    coverage=json.loads(coverage_path.read_text())
    assert coverage['sourceSHA256']==sha(root)==sha(SRC/'KSROOT.ASM')
    assert coverage['complete'] and not coverage['actorIDSubstitution']
    source=root.read_text()
    native_source=(SRC/'MKGUYS.ASM').read_text()
    symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in (0,1)]
    program=bytearray(1048576)
    assert all(len(lane)==524288 for lane in lanes)
    program[::2]=lanes[0];program[1::2]=lanes[1]
    records=[]
    for family,getter,count in ((1,'get_char_ani',66),(2,'get_char_ani2',7)):
        address=symbols[getter]
        assert read_long(program,address)&0xffff==0x09ee,'Expected native MOVI table address into A14'
        native=read_long(program,address+16)
        native_label=f'character_anitabs{family}'
        assert re.search(r'^'+getter+r'\s+movi\s+'+native_label+r',a14',native_source,re.M|re.I)
        # Follow the actual getter immediate even for non-exported table labels.
        if native_label in symbols:assert native==symbols[native_label]
        for actor,identity in (('kano',17),('sonya',18)):
            label=f'ks_{actor}_anitab{family}'
            table=symbols[label]
            assert read_long(program,native+identity*32)==table
            targets=pointers(source,label,count)
            if family==1:
                assert targets[0]==targets[64]==f'ks_{actor}_stance'
                assert coverage['fighters'][actor]['missingMainEntries']==[]
            else:assert coverage['fighters'][actor]['missingSpecialEntries']==[]
            for slot,target in enumerate(targets):
                pointer=read_long(program,table+slot*32)
                assert pointer==symbols[target],(actor,family,slot,target)
                # This unexported helper may be absent from the linker map.
                # Source target checks above independently forbid missing roots.
                if 'ks_missing_animation_mark' in symbols:
                    assert pointer!=symbols['ks_missing_animation_mark']
                assert read_long(program,pointer)!=0,('Empty root',target)
                records.append(dict(actor=actor,identity=identity,family=family,slot=slot,
                                    root=target,address=f'{pointer:08X}'))
    assert len(records)==146
    evidence=[Path(__file__),root,coverage_path,SRC/'KSROOT.ASM',SRC/'MKGUYS.ASM',SRC/'MK2P.MAP']
    evidence.extend(SRC/f'rom/P12{part}.{lane}' for part in ('F8','FC') for lane in (0,1))
    report=dict(scope='All own main/special dispatch pointers in the current linked program',
        cells=146,mainCells=132,specialCells=14,records=records,
        programSHA256=hashlib.sha256(program).hexdigest().upper(),
        allLinkedDispatchCellsMatchOwnASM=True,noMissingDispatchTargets=True,
        allRootBehaviorAndArtVerified=False,fullPortVerified=False,releaseReady=False,
        pins={str(path):sha(path) for path in evidence})
    (PORT/'ALL_ROSTER_ROOTS_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in ('records','pins')},indent=2))

if __name__=='__main__':main()
