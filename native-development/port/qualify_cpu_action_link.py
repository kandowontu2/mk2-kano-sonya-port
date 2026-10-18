"""Actual linked sparse rows/sentinel/call audit; not target execution proof."""
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
from cpu_action_source import ROUTES

PORT=Path(__file__).resolve().parent;ROOT=PORT.parents[1]
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
locals={name:int(address,16) for address,name in re.findall(r'(?m)^\s*\d+\s+([0-9a-fA-F]{8})\s+(ks_\w+)\s*$',(SRC/'MKDRONE.LST').read_text())}
start=symbols['ks_own_counter_lookup'];base=start-locals['ks_own_counter_lookup']
addresses={name:base+offset for name,offset in locals.items()}
program=bytearray(1048576)
for lane in (0,1):program[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
rows={}
for identity,name in ((17,'kano'),(18,'sonya')):
    offset=(addresses[f'ks_{name}_counter_rows']-0xff800000)//8
    entries=[]
    for action,reaction in ROUTES[identity].items():
        emitted_action,pointer=struct.unpack_from('<HI',program,offset);offset+=6
        assert emitted_action==action
        expected=0 if reaction=='0' else addresses[reaction]
        assert pointer==expected
        entries.append((emitted_action,pointer))
    assert program[offset:offset+6]==bytes(6),'Missing zero terminator/pointer'
    rows[identity]=entries
# Scan actual emitted records with signed word semantics (the prior failure).
checks=0
for identity in range(19):
    for action in range(0x900):
        if identity not in rows:continue
        name='kano' if identity==17 else 'sonya'
        offset=(addresses[f'ks_{name}_counter_rows']-0xff800000)//8
        found=False;pointer=None
        for _ in range(len(rows[identity])+1):
            current=struct.unpack_from('<h',program,offset)[0]
            if current==0:break
            if current==action:
                found=True;pointer=struct.unpack_from('<I',program,offset+2)[0];break
            offset+=6
        assert found==(action in ROUTES[identity])
        if found:
            reaction=ROUTES[identity][action]
            assert pointer==(0 if reaction=='0' else addresses[reaction])
        checks+=1
calls=[]
for offset in range(0,len(program)-4,2):
    opcode,relative=struct.unpack_from('<Hh',program,offset)
    if opcode==0x0d3f and ((0xff800000+offset*8+32+relative*16)&0xffffffff)==start:calls.append(0xff800000+offset*8)
assert len(calls)==1
out=PORT/'generated_cpu_actions';out.mkdir(exist_ok=True)
binary=out/'lookup.bin';offset=(start-0xff800000)//8
binary.write_bytes(program[offset:offset+256])
disassembly=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
    '-basepc',f'{start:X}','-count','2048'],capture_output=True,text=True,check=True,
    timeout=10,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)).stdout
assert 'CMPI   0h,A0' in disassembly
assert 'MOVE   *A2+,A0,0' in disassembly
(out/'lookup.txt').write_text(disassembly)
report=dict(scope='Compiled 48-bit sparse action records and signed sentinel scan',
    programSHA256=hashlib.sha256(program).hexdigest().upper(),rows={str(k):len(v) for k,v in rows.items()},
    signedLookupCasesChecked=checks,zeroTerminatorsVerified=True,allPointersMatchSource=True,
    callSites=[f'{address:08X}' for address in calls],helperAddress=f'{start:08X}',
    targetExecutionVerified=False,bossRuntimeVerified=False,releaseReady=False)
(PORT/'CPU_ACTION_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
