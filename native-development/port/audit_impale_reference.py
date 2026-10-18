"""Read-only original-victim impalement ABI/choreography reference audit."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
from current_graphics import graphics_metadata
PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main/srcp'
folder=BASE/'stock_impale_liu_reference86'
receipt=json.loads((folder/'execution.json').read_text())
assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
    assert hashlib.sha256(lanes[lane]).hexdigest().upper()==receipt['replacementChips'][chip]
for name,digest in graphics_metadata()['sockets'].items():assert receipt['replacementChips'][name]==digest
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def read(a,fmt):return struct.unpack_from('<'+fmt,program,(a-0xff800000)//8)
root=read(symbols['lk_anitab1']+59*32,'I')[0];script=read(root,'21I')
poses=[script[2],script[14],script[15]]
assert script==(4,0x0010ffa0,poses[0],4,0xffe80000,poses[0],4,0xffe80000,poses[0],4,0xffe80010,poses[0],0,
                poses[0],poses[1],poses[2],poses[1],poses[0],poses[1],poses[2],0)
records=[]
for phase,pose in enumerate(poses):
    parts=[]
    for i in range(8):
        pointer=read(pose+i*32,'I')[0]
        if pointer==0:break
        # Original tables omit optional trailing palette fields on many images;
        # do not misread the following image's dimensions as a palette pointer.
        parts.append(list(read(pointer,'HHhhIH')))
    assert len(parts)==(1,2,1)[phase]
    records.append(dict(phase=phase,composite=f'{pose:08x}',descriptors=parts))
rows=list(csv.DictReader((folder/'fan_objects.csv').open()))
assert rows and all(r['character']=='1' and r['missing']=='0' for r in rows)
assert set(poses)=={int(r['shape'],16) for r in rows}
assert any(r['death']=='65535' for r in rows)
for phase,pose in enumerate(poses):
    observed=[r for r in rows if int(r['shape'],16)==pose]
    records[phase].update(observations=len(observed),observedY=sorted({int(r['y']) for r in observed}))
report=dict(scope='Original Liu victim reference only, not added-character acceptance',
    nativeTwoPartScriptVerified=True,poses=records,nativeCompletionObserved=True,
    missingMarkers=0,ownImpalementImplemented=False,fullPortVerified=False)
(PORT/'IMPALE_REFERENCE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
