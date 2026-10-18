"""Verify native shake tokens, signed XY words, own poses and loop destinations."""
import json
from pathlib import Path
import re
import struct
PORT=Path(__file__).resolve().parent;BUILD=PORT.parent/'baseline/mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def read(a,n):return struct.unpack_from('<'+'I'*n,program,(a-0xff800000)//8)
mapping=json.loads((PORT/'generated_reactions/SHRED_SOURCE.json').read_text())
for actor in ('kano','sonya'):
    root=symbols[f'ks_{actor}_shredded']
    poses=[symbols[mapping[actor]['nativeToOwnPoseMapping'][f'LKSTUMBLE{i}']] for i in (1,2,3)]
    assert read(symbols[f'ks_{actor}_anitab1']+37*32,1)==(root,)
    assert read(root,14)==(4,0x00060006,poses[0],4,0xfffafffa,poses[1],4,0x00060006,poses[2],4,0xfffafffa,poses[1],1,root)
report=dict(ownBladeFuryRoots=2,exactNativeShakeLoopVerified=True,signedXYWordsVerified=True,
            runtimeVerified=False,fullPortVerified=False)
(PORT/'generated_reactions/SHRED_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
