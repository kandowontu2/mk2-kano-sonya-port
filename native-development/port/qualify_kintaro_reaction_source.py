"""Check exact original Kintaro choreography and emitted ROM data, not gameplay."""
import hashlib
import json
from pathlib import Path
import re
import struct

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline/mk2-rebuild-main'
native=(BASE/'srcw/MKLK.ASM').read_text()
body=native.split('\na_fb_goro\n',1)[1].split(';***************************************************************************',1)[0]
def typed(body):
    return [(kind.lower(),value.strip().lower()) for kind,expr in re.findall(r'\.(long|word)\s+([^;\r\n]+)',body) for value in expr.split(',')]
original=typed(body)
source=(PORT/'asm/KSREACT.ASM').read_text()
assert source==(BASE/'srcp/KSREACT.ASM').read_text()
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BASE/'srcp/MK2P.MAP').read_text())}
program=bytearray(0x100000)
for lane in (0,1):
    program[lane::2]=b''.join((BASE/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
report={}
for actor,poses in [('kano',('ff8294a0','ff829940','ff8299a0')),('sonya',('ff836860','ff837060','ff8370c0'))]:
    mapping=dict(zip(('lkstumble1','lkknockdown5','lkknockdown6'),(f'ks_{actor}_pose_{pose}' for pose in poses)))
    label=f'ks_{actor}_kintaro_thrown'
    emitted=source.split('\n'+label+'\n',1)[1]
    if actor=='kano':emitted=emitted.split('\nks_sonya_kintaro_thrown\n',1)[0]
    expected=[(kind,mapping.get(value,value)) for kind,value in original]
    assert typed(emitted)==expected
    payload=bytearray()
    for kind,value in expected:
        number=4 if value=='ani_adjustxy' else symbols[value] if value in symbols else int(value[:-1],16) if value.endswith('h') else int(value)
        payload+=struct.pack('<H' if kind=='word' else '<I',number & (65535 if kind=='word' else 0xffffffff))
    offset=(symbols[label]-0xff800000)//8
    assert program[offset:offset+len(payload)]==payload
    table=(symbols[f'ks_{actor}_anitab1']-0xff800000)//8+62*4
    assert struct.unpack_from('<I',program,table)[0]==symbols[label]
    report[actor]={'nativeTypedItemsPreserved':len(expected),'coordinateAdjustments':6,'poseSteps':6,'linkedBytes':len(payload),'runtimeVerified':False}
result={'sourceAndROMVerified':True,'programSHA256':hashlib.sha256(program).hexdigest().upper(),'actors':report,'fullPortVerified':False}
(PORT/'generated_roster_roots/KINTARO_SOURCE_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
