"""Emit stock Wolf sockets for corrected own inflation art, without emulation."""
import json
from pathlib import Path
from build_inflation_assets import sha

PORT = Path(__file__).resolve().parent
OUT = PORT/'generated_inflation_v3'
path = OUT/'INFLATION_DATA.json'
report = json.loads(path.read_text())
assert not report['artBoundaryIssues'] and not report['socketsEmitted']
packed = (OUT/'fighter_ui_finish_inflate_graphics.bin').read_bytes()
prefix = (PORT/'generated_arm_rip/fighter_ui_finish_arm_graphics.bin').read_bytes()
assert sha(packed) == report['packedSHA256'] and len(packed) < 0x600000
assert packed.startswith(prefix) and sha(prefix) == report['prefixSHA256']
region = packed+bytes(0x600000-len(packed))
rebuilt = bytearray(len(region))
sockets = {}
for bank, size in ((0, 0x100000), (1, 0x80000)):
    for lane in range(4):
        chip = 121-bank*4-lane
        name = f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        assert not (OUT/name).exists()
        start = bank*0x400000+lane
        data = region[start:start+size*4:4]
        assert len(data) == size
        (OUT/name).write_bytes(data)
        sockets[name] = sha(data)
        rebuilt[start:start+size*4:4] = data
assert rebuilt == region
report.update(sockets=sockets, socketsEmitted=True, stockSocketRoundTripVerified=True)
path.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(dict(sockets=len(sockets), stockSocketRoundTripVerified=True,
                      runtimeVerified=False)))
