"""Emit the eight physical Wolf graphics sockets for staged own arm-rip data."""
import hashlib
import json
from pathlib import Path

PORT=Path(__file__).resolve().parent;OUT=PORT/'generated_arm_rip'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
path=OUT/'ARM_RIP_DATA.json';report=json.loads(path.read_text())
packed=(OUT/'fighter_ui_finish_arm_graphics.bin').read_bytes()
assert sha(packed)==report['packedSHA256'] and len(packed)<0x600000
prefix=(PORT/'generated_impale/fighter_ui_finish_impale_graphics.bin').read_bytes()
assert packed.startswith(prefix) and sha(prefix)==report['prefixSHA256']
assert not report['socketsEmitted']
region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(len(region));sockets={}
for bank,size in ((0,0x100000),(1,0x80000)):
    for lane in range(4):
        name=f'l1_mortal_kombat_3_u{121-bank*4-lane}_game_rom.u{121-bank*4-lane}'
        assert not (OUT/name).exists()
        start=bank*0x400000+lane;data=region[start:start+size*4:4]
        assert len(data)==size
        (OUT/name).write_bytes(data);sockets[name]=sha(data)
        rebuilt[start:start+size*4:4]=data
assert rebuilt==region
report.update(sockets=sockets,socketsEmitted=True,stockSocketRoundTripVerified=True)
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(sockets=len(sockets),stockSocketRoundTripVerified=True,releaseReady=False)))
