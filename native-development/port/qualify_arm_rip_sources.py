"""Independent staged payload/header checks, not a runtime qualification."""
import hashlib
import json
from pathlib import Path
import re
from build_arm_rip_assets import read_pgm

PORT=Path(__file__).resolve().parent;OUT=PORT/'generated_arm_rip';SOURCE=PORT/'assets/arm_rip'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
report=json.loads((OUT/'ARM_RIP_DATA.json').read_text())
packed=(OUT/'fighter_ui_finish_arm_graphics.bin').read_bytes()
assembly=(OUT/'KSARART.ASM').read_bytes();text=assembly.decode('ascii')
assert sha(packed)==report['packedSHA256'] and sha(assembly)==report['assemblySHA256']
prefix=(PORT/'generated_impale/fighter_ui_finish_impale_graphics.bin').read_bytes()
assert packed[:len(prefix)]==prefix and sha(prefix)==report['prefixSHA256']
assert sha((SOURCE/'ARM_RIP_SOURCES.json').read_bytes())==report['sourceManifestSHA256']
end=len(prefix)
for frame in report['frames']:
    path=SOURCE/frame['file'];assert sha(path.read_bytes())==frame['SHA256']
    w,h,pixels=read_pgm(path);assert (w,h)==(frame['width'],frame['height'])
    assert frame['packedByteOffset']==end
    payload=packed[end:end+frame['packedBytes']];end+=len(payload)
    assert sha(payload)==frame['packedSHA256']
    # Decode crossing bytes independently of the generator's scalar reader.
    decoded=[]
    for index in range(w*h):
        byte,shift=divmod(index*6,8)
        word=payload[byte]|((payload[byte+1]<<8) if byte+1<len(payload) else 0)
        decoded.append(word>>shift&63)
    assert decoded==pixels and sha(bytes(decoded))==frame['indexSHA256']
    expected=f"{frame['imageLabel']}\n        .word {w},{h},{frame['xOffset']},{frame['yOffset']}\n"
    assert expected in text
    assert f'        .long 0{(0xc00000+frame["packedByteOffset"])*8:08x}h\n        .word 06000h' in text
    if frame['role']=='body':
        assert h-frame['yOffset']==frame['ground']
        assert f"{frame['poseLabel']}\n        .long {frame['imageLabel']},0" in text
assert end==len(packed) and len(report['frames'])==20
for actor in ('kano','sonya'):
    for role,label in (('body',f'ks_{actor}_arms_ripped'),('arm',f'ks_{actor}_arm_fly')):
        script=text.split(label+'\n',1)[1]
        values=re.findall(r'^        \.long ([^\n]+)',script,re.M)[:6]
        expected=[f'ks_ar_{actor}_body_pose{phase}' if role=='body' else f'ks_ar_{actor}_arm_frame{phase}' for phase in range(5)]+['0']
        assert values==expected
result=dict(scope='Own source indices, six-bit packed pixels, typed headers and animation format only',
    framesVerified=20,prefixPreserved=True,bytewisePixelRoundTripVerified=True,
    bodyScriptIsMultipart=True,detachedArmScriptIsSingleImages=True,
    appendedBytes=len(packed)-len(prefix),packedSHA256=sha(packed),assemblySHA256=sha(assembly),
    gameCodeChanged=False,activeNativeLinkChanged=False,calibratedInGame=False,
    runtimeVerified=False,releaseReady=False,fullPortVerified=False)
(PORT/'ARM_RIP_SOURCE_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
