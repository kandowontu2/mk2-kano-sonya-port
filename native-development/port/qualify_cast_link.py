"""Actual linked cast rows and own animation roots, not credits runtime proof."""
import hashlib
import json
from pathlib import Path
import re
import struct
from native_roster import verified_names

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
listing=(SRC/'MKEND.LST').read_text()
def local(name):return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+'+name+r'\s*$',listing,re.M)[1],16)
base=symbols['cast_of_characters']-local('cast_of_characters')
rom=bytearray(1048576)
for lane in (0,1):rom[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
def read(address,count):
    assert address>=0xff800000 and address+count*8<=0x100000000 and address%8==0
    at=(address-0xff800000)//8
    return bytes(rom[at:at+count])
def pointer(address):return struct.unpack('<I',read(address,4))[0]
names=verified_names();rows=[]
table=base+local('cast_table')
for index,expected in enumerate(((3,1),(7,2),(4,0),(6,11),(5,8),(9,10),(17,18))):
    left,x1,right,x2,text1,text2=struct.unpack('<HHHHII',read(table+index*128,16))
    assert (left,right)==expected
    credits=[read(address,80).split(b'\0',1)[0].decode('ascii') for address in (text1,text2)]
    if index==6:
        assert (x1,x2)==(0x70,0x120)
        assert credits==['RICHARD DIVIZIO\\nAS\\nKANO','KERRI HOSKINS\\nAS\\nSONYA']
    rows.append(dict(identities=[left,right],names=[names[left],names[right]],x=[x1,x2],credits=credits))
assert read(table+7*128,2)==b'\0\0'
roots=[]
for identity,actor in ((17,'kano'),(18,'sonya')):
    root=pointer(symbols['character_anitabs1']+identity*32)
    assert root==symbols[f'ks_{actor}_anitab1']
    for index,label in ((6,f'ks_{actor}_vertical_jump'),(0x29,f'ks_{actor}_main_29')):
        actual=pointer(root+index*32)
        assert actual==symbols[label]
        roots.append(dict(actor=actor,animation=index,label=label,address=f'{actual:08X}'))
report=dict(programSHA256=sha(rom),castRows=rows,ownAnimationRoots=roots,
    originalSixPairsPreserved=True,ownSeventhPairAndTerminatorVerified=True,
    ownBowAnimationRuntimeVerified=False,creditsRuntimeVerified=False,releaseReady=False)
report['sourceSHA256']={name:sha((SRC/name).read_bytes()) for name in ('MKEND.ASM','MKEND.LST','MK2P.MAP','KSROOT.ASM')}
(PORT/'CAST_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
