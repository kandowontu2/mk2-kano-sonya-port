"""Measure late gush anchors relative to the actual collapsed victim pose."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
from build_arm_rip_assets import read_pgm

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
proof=json.loads((PORT/'ARM_RIP_RUNTIME_QUALIFICATION.json').read_text())
assert proof['nativeCompletionWithoutRecoveryVerified'] and proof['mirroredSidesVerified']
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
assert proof['programLaneSHA256']==[sha(data) for data in lanes]
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
gw,gh,gx,gy=struct.unpack_from('<HHhh',program,(symbols['GUSHER1']-0xff800000)//8)
source=json.loads((PORT/'assets/arm_rip/ARM_RIP_SOURCES.json').read_text())
points={'kano':((36,10),(4,20)),'sonya':((38,20),(12,25))}
cases=[]
for case in proof['cases']:
    actor='kano' if case['actor']==17 else 'sonya'
    frame=next(frame for frame in source['frames'] if frame['actor']==actor and frame['role']=='body' and frame['phase']==4)
    w,h,pixels=read_pgm(PORT/'assets/arm_rip'/frame['file'])
    assert sha((PORT/'assets/arm_rip'/frame['file']).read_bytes())==frame['SHA256']
    colors=source['palettesRGB15'][actor]
    for x,y in points[actor]:
        assert pixels[y*w+x]!=0
        # Authored wound centers can contain highlight/skin pixels; require
        # adjacent dark-red cap pixels within a two-pixel neighborhood.
        nearby=[colors[pixels[yy*w+xx]] for yy in range(max(0,y-2),min(h,y+3)) for xx in range(max(0,x-2),min(w,x+3))]
        assert any((v>>10&31)>8 and (v>>10&31)>2*(v>>5&31) and (v>>10&31)>2*(v&31) for v in nearby)
    expected={(x-frame['xOffset'],y-frame['yOffset']) for x,y in points[actor]}
    folder=BASE/case['run'];rows=list(csv.DictReader((folder/'fan_objects.csv').open()))
    bodies={row['frame']:row for row in rows if int(row['shape'],16)==symbols[f'ks_ar_{actor}_body_pose4']}
    gush=[row for row in rows if int(row['image'],16)==symbols['GUSHER1']]
    assert len(gush)==24
    measured=collections.Counter()
    for row in gush:
        victim=bodies[row['frame']]
        # A single-part object's x/y are image-corner coordinates. Restore
        # its compiled animation point before comparing to the multi body.
        anchor_x=int(row['x'])+(gw-gx if int(row['flags'])&16 else gx)
        anchor_y=int(row['y'])+gy
        dx=(anchor_x-int(victim['x']))*(-1 if int(victim['flags'])&16 else 1)
        dy=anchor_y-int(victim['y']);measured[dx,dy]+=1
    assert set(measured)==expected and set(measured.values())=={12}
    ticks=sorted({int(row['frame']) for row in gush});waves=[]
    for tick in ticks:
        if not waves or tick!=waves[-1][-1]+1:waves.append([])
        waves[-1].append(tick)
    assert len(waves)==3 and all(len(wave)==4 for wave in waves)
    captures=list((folder/'snap').glob(f"fan_pose_{symbols['GUSHER1']:08x}_*.png"));assert len(captures)==1
    cases.append(dict(actor=case['actor'],side=case['victimSide'],run=case['run'],
        collapsedPoseWoundPixels=points[actor],normalizedWorldAnchors=[list(point) for point in sorted(measured)],
        matchedGushRows=24,nativeGushPairs=3,captureSHA256=sha(captures[0].read_bytes())))
report=dict(scope='Late arm-rip gushes on own collapsed-body shoulder wounds only',cases=cases,
    programLaneSHA256=proof['programLaneSHA256'],compiledGusherHeader=[gw,gh,gx,gy],
    exactLateGushAnchorsVerified=True,mirroredSidesVerified=True,nativeCompletionVerified=True,
    earlyDripPlacementVerified=False,allAnimationVisualQAComplete=False,
    originalRosterRuntimeRegressionVerified=False,releaseReady=False,fullPortVerified=False)
(PORT/'ARM_BLOOD_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
