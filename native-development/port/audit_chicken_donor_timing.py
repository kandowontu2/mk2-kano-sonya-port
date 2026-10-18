"""Read original donor ROM animation commands, not custom-driver behavior."""
import hashlib
import json
from pathlib import Path
import struct
import zipfile
import subprocess

PORT=Path(__file__).resolve().parent;ROOT=PORT.parents[1]
raw=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
with zipfile.ZipFile(ROOT/'mk3.zip') as archive:
    assert raw[0::2]==archive.read('mk321u54.bin')
    assert raw[1::2]==archive.read('mk321u63.bin')
offset=lambda address:(address-0xff800000)//8
poses=(0xff9d2f70,0xff9d2ff0,0xff9d3070,0xff9d30f0,0xff9d3070,
       0xff9d2ff0,0xff9d2f70,0xff9d2ef0,0xff9d2e50,0xff9d2db0,
       0xff9d2d10,0xff9d2db0,0xff9d2e50,0xff9d2ef0)
start=0xff9d28d0
callback=struct.unpack_from('<I',raw,offset(start)+12)[0]
expected=[]
for index,pose in enumerate(poses):
    if index in (2,4,6):expected.extend((6,callback))
    expected.append(pose)
expected.extend((1,start))
actual=struct.unpack_from('<'+'I'*len(expected),raw,offset(start))
assert actual==tuple(expected)
sound=struct.unpack_from('<4I',raw,offset(0xffaa6ad0))
assert sound==(0x00a51010,0x00aa1017,0x00af1014,0x00961012)
disassembler=ROOT/'mame-mkp/unidasm.exe'
def disassemble(address,bits):
    return subprocess.run([str(disassembler),str(ROOT/'mk3/mk3-maincpu.bin'),
        '-arch','tms34010','-skip',str(offset(address)),'-count',str(bits),
        '-basepc',f'{address:X}'],check=True,capture_output=True,text=True,
        timeout=10,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)).stdout
callback_code=disassemble(callback,48)
helper_code=disassemble(0xffaa6c00,640)
assert 'MOVK   4h,A0' in callback_code and 'CALLR  FFAA6C00h' in callback_code
for instruction in ('CALLA  FF927780h','DEC    A0','SLL    5h,A0','ADD    A1,A0',
                    'MOVE   *A0+,A1,0','SRL    8h,A1'):
    assert instruction in helper_code,instruction
report=dict(scope='Original donor program chip bytes and animation cue locations',
    donorSHA256=hashlib.sha256(raw).hexdigest().upper(),archiveProgramLanesMatch=True,
    animationAddress=f'{start:08X}',callbackAddress=f'{callback:08X}',
    poseCount=14,cueBeforePoseIndices=[2,4,6],
    soundRecords=[f'{value:08X}' for value in sound],
    originalCommands=[0xa5,0xaa,0xaf,0x96],holdFields=[16,23,20,18],
    disassemblerSHA256=hashlib.sha256(disassembler.read_bytes()).hexdigest().upper(),
    callbackDisassembly=callback_code,recordSelectionDisassembly=helper_code,
    nativeMK2CallerImplemented=False,callbackRecordSelectionInstructionsAudited=True,
    completeDonorAllocatorAudited=False,
    runtimeVerified=False,releaseReady=False)
(PORT/'CHICKEN_DONOR_TIMING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
