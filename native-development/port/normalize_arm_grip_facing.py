"""Normalize editable grip indices into the native actor-facing convention."""
import hashlib
import json
from pathlib import Path
from build_arm_rip_assets import read_pgm

PORT=Path(__file__).resolve().parent;SOURCE=PORT/'assets/arm_rip'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
path=SOURCE/'ARM_RIP_SOURCES.json';old=path.read_bytes();manifest=json.loads(old)
assert manifest.get('gripRevision') and not manifest['gripRevision'].get('nativeFacingNormalized')
changed=[]
for frame in manifest['frames']:
    file=SOURCE/frame['file'];assert sha(file.read_bytes())==frame['SHA256']
    if frame['role']!='body' or frame['phase']!=0:continue
    w,h,pixels=read_pgm(file);normalized=[]
    for row in range(h):normalized.extend(reversed(pixels[row*w:(row+1)*w]))
    filename=f"{frame['actor']}_body0_grip_native.pgm";output=SOURCE/filename
    assert not output.exists()
    pgm=f'P2\n# Own grip indices normalized for native reaction mirroring.\n{w} {h}\n63\n'
    pgm+='\n'.join(' '.join(map(str,normalized[row*w:(row+1)*w])) for row in range(h))+'\n'
    output.write_text(pgm,encoding='ascii')
    prior={key:value for key,value in frame.items() if key!='priorFrame'}
    frame.update(priorFrame=prior,file=filename,SHA256=sha(output.read_bytes()),
        xOffset=w-1-frame['xOffset'],nativeFacingNormalized=True,
        sourcePixelTransform='horizontal reflection for native actor-facing convention')
    changed.append(frame['actor'])
assert len(changed)==2
manifest['gripRevision'].update(priorManifestSHA256=sha(old),nativeFacingNormalized=True,
    actorFootOriginPreserved=True,runtimeVisualAcceptance=False)
path.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(normalizedActors=changed,otherIndexedSourcesUnchanged=18)))
