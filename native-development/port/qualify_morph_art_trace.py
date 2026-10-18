"""Pin forward/reverse native frame cadence and measure, not assume, grounding."""
import csv
import json
from pathlib import Path
import re
import sys
import zipfile
from build_arm_rip_assets import sha
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
data=json.loads((PORT/'generated_morph/MORPH_DATA.json').read_text())
lookup={symbols[f['poseLabel']]:f for f in data['frames']}
expected=[(actor,phase) for actor in ('kano','sonya','sonya') for phase in (0,1,2,2,1,0)]
cases=[]
names=[f'stock_wolf_game{value}' if value.isdecimal() else value for value in sys.argv[1:]]
assert len(names)==2 and len(set(names))==2,'Supply two explicit completed current morph runs'
for name in names:
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        verify_archive_sockets(archive)
    with (folder/'morph_art.csv').open() as stream:rows=list(csv.DictReader(stream))
    groups=[]
    for row in rows:
        if not groups or row['shape']!=groups[-1][-1]['shape'] or int(row['frame'])!=int(groups[-1][-1]['frame'])+1:groups.append([])
        groups[-1].append(row)
    assert [(lookup[int(g[0]['shape'],16)]['actor'],lookup[int(g[0]['shape'],16)]['phase']) for g in groups]==expected
    entries=[]
    for group in groups:
        frame=lookup[int(group[0]['shape'],16)]
        assert len(group)==4 and all(r['action']=='1028' for r in group)
        deltas={int(r['y'])+frame['height']-frame['yOffset']-int(r['ground']) for r in group}
        assert len(deltas)==1
        delta=next(iter(deltas))
        assert delta==0,(folder.name,frame['actor'],frame['phase'],group[0]['character'],delta)
        first=int(group[0]['frame'])
        captures=list((folder/'snap').glob(f'morph_pose_{group[0]["shape"]}_{first+2:05d}.png'))
        assert len(captures)==1
        entries.append(dict(actor=frame['actor'],phase=frame['phase'],character=int(group[0]['character']),
            fields=4,groundDelta=deltas.pop(),paletteSelector=int(group[0]['palette']),
            capture=captures[0].name,captureSHA256=sha(captures[0].read_bytes())))
    cases.append(dict(run=folder.name,entries=entries))
report=dict(cases=cases,forwardAndReversePoseOrderVerified=True,nativeFourFieldCadenceVerified=True,
    entryGroundingMeasuredCorrect=True,reverseGroundingMeasuredCorrect=True,finalVisualAcceptance=False,releaseReady=False)
(PORT/'MORPH_ART_TRACE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
