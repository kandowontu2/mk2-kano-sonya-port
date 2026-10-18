"""Verify own anitab2 source contracts and actual linked native dispatch cells."""
import hashlib
import json
from pathlib import Path
import re
import struct
from special_root_contract import ROOTS, ROLES, CALLERS

PORT=Path(__file__).resolve().parent
BUILD=PORT.parent/'baseline/mk2-rebuild-main/srcp'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000)
program[::2]=lanes[0]
program[1::2]=lanes[1]
def read(a,fmt): return struct.unpack_from('<'+fmt,program,(a-0xff800000)//8)
getter=symbols['get_char_ani2']
assert read(getter,'H')==(0x09ee,) # Native MOVI long immediate to A14.
native_table=read(getter+16,'I')[0]
records=[]
for actor,identity in [('kano',17),('sonya',18)]:
    table=symbols[f'ks_{actor}_anitab2']
    assert read(native_table+identity*32,'I')==(table,)
    for slot,(root,module) in enumerate(zip(ROOTS[actor],CALLERS[actor])):
        pointer=symbols[root]
        assert read(table+slot*32,'I')==(pointer,)
        assert 0xff800000<=pointer<0x100000000 and read(pointer,'I')[0]!=0
        source=(PORT/'asm'/module).read_bytes()
        assert source==(BUILD/module).read_bytes(),module
        selector=r'clr\s+a9' if slot==0 else rf'movk\s+{slot},a9'
        assert re.search(selector+r'\s+(?:calla|jauc)\s+get_char_ani2',source.decode('ascii'),re.I)
        records.append(dict(actor=actor,slot=slot,role=ROLES[slot],root=root,
            rootAddress=f'{pointer:08x}',callerModule=module,callerSHA256=sha(source)))
native=(BUILD/'MKGUYS.ASM').read_text()
assert re.search(r'get_char_ani2\s+movi\s+character_anitabs2,a14',native,re.I)
allocator=(BUILD/'MKZAP.ASM').read_text()
assert re.search(r'move\s+\*a8\(ochar\),\*a10\(ochar\),w',allocator,re.I)
# Record every native lookup/wrapper consumer for review. This is an inventory,
# not a claim that regex matching proves original dispatch reachability.
inventory=[]
for path in sorted(BUILD.glob('*.ASM')):
    if path.name.startswith('KS') or path.name in ('KANOMOV.ASM','SONYAMOV.ASM'):
        continue
    lines=path.read_text(errors='replace').splitlines()
    for i,line in enumerate(lines):
        code=line.split(';',1)[0]
        if re.search(r'\b(?:calla|callr|jsrp|jauc|movi)\s+(?:get_char_ani2|get_his_char_ani2|animate2_a9|pose2_a9|striker_2)\b',code,re.I):
            inventory.append(dict(module=path.name,line=i+1,context=lines[max(0,i-5):i+2]))
report=dict(ownDispatchCellsVerified=14,records=records,programLaneSHA256=[sha(l) for l in lanes],
    originalCallerInventory=inventory,originalCallerReachabilityFullyAudited=False,
    nativeGetterVerified=True,projectileTrueIdentityInheritanceVerified=True,
    runtimeVerified=False,fullPortVerified=False)
(PORT/'SPECIAL_ROOT_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('records','originalCallerInventory')}))
