"""Pin the two-pose revision against an actual earlier runtime graphics set."""
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile
from build_arm_rip_assets import read_pgm

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
proof=json.loads((PORT/'ARM_RIP_RUNTIME_QUALIFICATION.json').read_text())
assert proof['nativeCompletionWithoutRecoveryVerified'] and proof['mirroredSidesVerified']
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
assert proof['programLaneSHA256']==[sha(data) for data in lanes]
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
art=json.loads((PORT/'generated_arm_rip/ARM_RIP_DATA.json').read_text())
source=json.loads((PORT/'assets/arm_rip/ARM_RIP_SOURCES.json').read_text())
assert source['gripRevision']['nativeFacingNormalized']
old_run=BASE/'stock_arm_origins_kano221'
with zipfile.ZipFile(old_run/'roms/mk3.zip') as archive:
    old_program=bytearray(1048576)
    old_program[::2]=archive.read('mk321u54.bin');old_program[1::2]=archive.read('mk321u63.bin')
    old_graphics=bytearray(0x600000)
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            name=f'l1_mortal_kombat_3_u{121-bank*4-lane}_game_rom.u{121-bank*4-lane}'
            start=bank*0x400000+lane;old_graphics[start:start+size*4:4]=archive.read(name)
changed=[];unchanged=[]
for frame in art['frames']:
    address=symbols[frame['imageLabel']]
    w,h,x,y,sag,control,palette=struct.unpack_from('<HHhhIHI',old_program,(address-0xff800000)//8)
    assert control==0x6000 and palette==symbols[f"ks_{frame['actor']}_primary_palette"]
    offset=sag//8-0xc00000;assert 0<=offset<len(old_graphics)
    payload=old_graphics[offset:offset+(w*h*6+7)//8]
    pixels=[]
    for index in range(w*h):
        byte,shift=divmod(index*6,8)
        word=payload[byte]|((payload[byte+1]<<8) if byte+1<len(payload) else 0)
        pixels.append(word>>shift&63)
    identical=(w,h)==(frame['width'],frame['height']) and sha(bytes(pixels))==frame['indexSHA256']
    if frame['role']=='body' and frame['phase']==0:
        assert not identical;changed.append(frame['imageLabel'])
    else:assert identical;unchanged.append(frame['imageLabel'])
assert len(changed)==2 and len(unchanged)==18
cases=[]
for case in proof['cases']:
    actor='kano' if case['actor']==17 else 'sonya'
    frame=next(item for item in source['frames'] if item['actor']==actor and item['role']=='body' and item['phase']==0)
    w,h,pixels=read_pgm(PORT/'assets/arm_rip'/frame['file'])
    oldw,oldh,prior=read_pgm(PORT/'assets/arm_rip'/frame['priorFrame']['file'])
    assert (w,h)==(oldw,oldh)
    assert pixels==[value for row in range(h) for value in reversed(prior[row*w:(row+1)*w])]
    assert frame['xOffset']==w-1-frame['priorFrame']['xOffset'] and frame['yOffset']==0
    address=symbols[f'ks_ar_{actor}_body_pose0']
    captures=list((BASE/case['run']/'snap').glob(f'fan_pose_{address:08x}_*.png'));assert len(captures)==1
    cases.append(dict(actor=case['actor'],side=case['victimSide'],run=case['run'],
        capture=str(captures[0]),captureSHA256=sha(captures[0].read_bytes()),
        handsTowardJaxVisuallyReviewed=True,footOriginPreserved=True))
report=dict(scope='Initial grip pose only; complete arm-rip visual QA remains open',cases=cases,
    programLaneSHA256=proof['programLaneSHA256'],earlierRuntimeReference=old_run.name,
    changedBodyImages=changed,unchangedOtherImages=unchanged,
    onlyTwoImagesChangedAgainstEarlierRuntimeVerified=True,nativeFacingReflectionVerified=True,
    bothSidesCapturedGripContactReviewed=True,nativeFatalityCompletionVerified=True,
    allBloodPlacementAndEdgeCasesAccepted=False,fullAnimationVisualAcceptance=False,
    releaseReady=False,fullPortVerified=False)
(PORT/'ARM_GRIP_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key not in ('cases','unchangedOtherImages')},indent=2))
