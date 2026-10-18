"""Prove object-list removal, not arbitrary timer-based visual disappearance."""
import csv
import json
import re
import sys
import zipfile
from pathlib import Path
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
runtime=json.loads((PORT/'LAO_SPLIT_RUNTIME_QUALIFICATION.json').read_text())
cases=[]
names=sys.argv[1:]
assert len(names) in (2,4,6) and len(set(names))==len(names), 'Supply explicit distinct current runs'
assert runtime['currentFull26ROMBytesVerified']
assert all(sha(Path(path).read_bytes())==digest for path,digest in runtime['pins'].items())
qualified_names={c['run'] for c in runtime['cases']+runtime['originalControls']}
for name in names:
    assert name in qualified_names and Path(name).name==name
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    actor=18 if '--sonya' in receipt['testArguments'] else 17
    control=next((arg for arg in receipt['testArguments'] if arg.startswith('--lao-split-control=')),None)
    if control:actor=int(control.split('=',1)[1])
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert receipt['replacementChips'][chip]==runtime['programLaneSHA256'][lane]
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify(archive,receipt)
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert sha(archive.read(chip))==runtime['programLaneSHA256'][lane]
        verify_archive_sockets(archive)
    with (folder/'split_lifecycle.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert len(rows)==6000 and [int(r['frame']) for r in rows]==list(range(3001,9001))
    present=[r for r in rows if int(r['matchingObjects'])>0]
    assert present and max(int(r['matchingObjects']) for r in present)==2
    last=int(present[-1]['frame'])
    after=[r for r in rows if int(r['frame'])>last]
    assert after and all(r['matchingObjects']=='0' for r in after)
    assert any(r['death']=='65535' for r in present)
    with (folder/'laosplit_victim.csv').open() as stream:victims=list(csv.DictReader(stream))
    assert victims and all(int(r['character'])==actor for r in victims)
    assert victims[-1]['death']=='65535'
    captures=list((folder/'snap').glob(f'split_objects_cleared_{last+1:05d}.png'))
    assert len(captures)==1
    late={}
    for age in (3,12,30,60,120,240):
        matches=list((folder/'snap').glob(f'split_after_clear_{age:02d}_{last+1+age:05d}.png'))
        assert len(matches)==1
        late[matches[0].name]=sha(matches[0].read_bytes())
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=folder.name,lastObjectField=last,
        firstClearField=last+1,absentThroughField=9000,
        capture=captures[0].name,captureSHA256=sha(captures[0].read_bytes()),lateCaptures=late))
report=dict(programLaneSHA256=runtime['programLaneSHA256'],cases=cases,
    removalFromNativeObjectListVerified=True,observerHasNoGameMemoryWrites=True,
    finalGroundAlignmentAccepted=False,allTransitionVisualsAccepted=False,releaseReady=False)
paths=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'LAO_SPLIT_RUNTIME_QUALIFICATION.json']
for name in names:
    folder=BASE/name
    paths.extend(folder/item for item in ('execution.json','autoboot.lua','split_lifecycle.csv','laosplit_victim.csv','mame.log'))
    paths.extend(sorted((folder/'snap').glob('split*.png')))
report['currentFull26ROMBytesVerified']=True
report['pins']={str(path):sha(path.read_bytes()) for path in paths}
(PORT/'SPLIT_CLEANUP_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
