"""Inspect actual linked instructions; not execution or boss gameplay proof."""
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

PORT=Path(__file__).resolve().parent;ROOT=PORT.parents[1]
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
target=symbols['ks_boss_category']
program=bytearray(1048576)
for lane in (0,1):program[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
calls=[]
for offset in range(0,len(program)-4,2):
    opcode,relative=struct.unpack_from('<Hh',program,offset)
    if opcode==0x0d3f and ((0xff800000+offset*8+32+relative*16)&0xffffffff)==target:
        calls.append(0xff800000+offset*8)
assert len(calls)==2,calls
out=PORT/'generated_boss_category';out.mkdir(exist_ok=True)
binary=out/'linked_helper.bin'
offset=(target-0xff800000)//8
binary.write_bytes(program[offset:offset+256])
result=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
    '-basepc',f'{target:X}','-count','2048'],capture_output=True,text=True,check=True,
    timeout=10,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
helper=result.stdout.split('RETS',1)[0]+'RETS\n'
for operand in ('211h,A1','212h,A1','11h,A0','12h,A0'):
    assert operand in helper,operand
assert 'SRL    8h,A1' in helper
assert 'MOVE   A0,-*SP,1' in helper and 'MMFM   SP,A0' in helper
(out/'linked_helper.txt').write_text(helper)
report=dict(scope='Linked native boss-category helper calls and disassembly',
    programSHA256=hashlib.sha256(program).hexdigest().upper(),
    helperAddress=f'{target:08X}',callSites=[f'{address:08X}' for address in calls],
    helperBinarySHA256=hashlib.sha256(binary.read_bytes()).hexdigest().upper(),
    identityAndActionComparisonsPresent=True,originalShiftFallbackPresent=True,
    disassembly=helper,targetExecutionVerified=False,bossRuntimeVerified=False,releaseReady=False)
(PORT/'BOSS_CATEGORY_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
