"""Finite native Cage torso-rip proof, not all torso consumers or visual QA."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from PIL import Image
from leg_ground_source import OWN_LEG_EXTENT
from verify_finisher_roms import verify as verify_full_rom
from fresh_victim_match import verify_folder as verify_fresh_match
from current_graphics import graphics_metadata
PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
names=sys.argv[1:]
assert names and len(names)==len(set(names)),'Supply distinct completed torso fixtures'
cases=[]
for argument in names:
    assert argument and Path(argument).name==argument and '/' not in argument and '\\' not in argument
    folder=BASE/argument;receipt=json.loads((folder/'execution.json').read_text())
    swipe='--swipe-victim' in receipt['testArguments']
    assert ('--torso-victim' in receipt['testArguments'] or swipe) and '--stock-victim' not in receipt['testArguments']
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    observer=(folder/'autoboot.lua').read_bytes()
    assert sha(observer)==receipt['controllerSHA256']
    assert b':write_u' not in observer and not re.search(rb'\.value\s*=(?!=)',observer)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify_full_rom(archive,receipt)
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        data=b''.join((BUILD/f'rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        assert sha(data)==receipt['replacementChips'][chip]
    graphics=json.loads((PORT/'generated_torso/TORSO_DATA.json').read_text())
    for chip,digest in graphics_metadata()['sockets'].items():assert receipt['replacementChips'][chip]==digest
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano';identity=18 if actor=='sonya' else 17
    poses=[symbols[f'ks_tr_{actor}_pose{i}'] for i in range(7)]
    if swipe:poses[5]=symbols[f'ks_sw_{actor}_pose5']
    rows=list(csv.DictReader((folder/'fan_objects.csv').open()))
    assert rows and all(int(r['character'])==identity and int(r['missing'])==0 for r in rows)
    required=list(range(7)) if swipe else [0,1,2,3,5,6]
    assert {poses[i] for i in required}<=set(int(r['shape'],16) for r in rows)
    legs=[r for r in rows if int(r['shape'],16)==poses[6]]
    upper=[r for r in rows if int(r['shape'],16)==poses[5]]
    assert len(legs)>=200 and len({(r['object'],r['x'],r['y']) for r in legs})==1
    main=list(csv.DictReader((folder/'fan.csv').open()))
    side=2 if '--mirror' in receipt['testArguments'] else 1
    performer=10 if swipe else 2
    owner=f'p{side}';victim=f'p{3-side}'
    active=min(int(row['frame']) for row in main if row['death']==('2' if swipe else '1'))
    fight=[row for row in main if row['mode']=='2' and int(row['frame'])<=active]
    assert fight and all(row[owner+'char']==str(performer) and row[victim+'char']==str(identity) for row in fight)
    kos=[int(row['frame']) for previous,row in zip(fight,fight[1:]) if int(previous[victim+'hp'])>0 and row[victim+'hp']=='0']
    assert len(kos)==2
    origin=next(r for r in main if r['frame']==legs[0]['frame']);ground=int(origin['ground'])
    leg_record=graphics['records'][actor][6]
    leg_path=PORT/'assets/torso'/leg_record['file']
    assert sha(leg_path.read_bytes())==leg_record['fileSHA256']
    with Image.open(leg_path) as image:opaque_bounds=image.getbbox()
    assert opaque_bounds is not None
    leg_extent=opaque_bounds[3]-leg_record['yOffset']
    assert leg_extent==OWN_LEG_EXTENT
    assert all(int(row['y'])+leg_extent==ground for row in legs),'Detached feet are not on the ground plane'
    bottom=graphics['records'][actor][5]['height']-graphics['records'][actor][5]['yOffset']
    if swipe:bottom+=16
    settled=[r for r in upper if int(r['y'])+bottom==ground]
    assert len(settled)>=200
    assert len({r['frame'] for r in legs}&{r['frame'] for r in upper})>=200
    assert max(int(r['missing']) for r in main)==0 and not (folder/'fan_fault.txt').exists()
    assert any(r['death']==('2' if swipe else '1') for r in main) and any(r['death']=='65535' for r in legs)
    result=dict(qualified=True,scope='One physical native torso fatality',victim=actor,
        performer='scorpion' if swipe else 'cage',performerPlayer=2 if '--mirror' in receipt['testArguments'] else 1,
        requiredOwnCompositePhases=required,stationaryLegObservations=len(legs),
        groundedFinalUpperObservations=len(settled),nativeCompletionObserved=True,missingMarkers=0,
        lowerOpaqueFootPlacementAccepted=True,lowerOpaqueExtent=leg_extent,
        lowerOpaqueGroundDelta=0,fullVisualAcceptance=False,fullPortVerified=False)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    result.update(naturalKOFrames=kos,currentFull26ROMBytesVerified=True)
    if '--finisher-rejoin' in receipt['testArguments']:result.update(verify_fresh_match(folder,main,side,performer,identity))
    evidence=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'fresh_victim_match.py',PORT/'leg_ground_source.py',leg_path,
              PORT/'generated_torso/TORSO_DATA.json',BUILD/'MKDEATH.ASM',BUILD/'MK2P.MAP']
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','fan.csv','fan_objects.csv','mame.log'))
    evidence.extend((folder/'snap').glob('fan_pose_*.png'))
    if '--finisher-rejoin' in receipt['testArguments']:evidence.extend(folder/item for item in ('finisher_rejoin_events.csv','finisher_cleanup.csv'))
    result['pins']={str(path):sha(path.read_bytes()) for path in evidence}
    (folder/'TORSO_RUNTIME_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    cases.append(dict(run=argument,victim=identity,victimSide=3-side,swipe=swipe,
                      freshCombatFields=result.get('freshCombatFields',0),qualificationSHA256=sha((folder/'TORSO_RUNTIME_QUALIFICATION.json').read_bytes())))
if len(cases)==4:
    assert len({case['swipe'] for case in cases})==1
    assert {(case['victim'],case['victimSide']) for case in cases}=={(actor,side) for actor in (17,18) for side in (1,2)}
    assert all(case['freshCombatFields']==600 for case in cases)
    (PORT/('SWIPE_MATRIX_QUALIFICATION.json' if cases[0]['swipe'] else 'TORSO_MATRIX_QUALIFICATION.json')).write_text(json.dumps(
        dict(cases=cases,allFourFiniteCasesPassed=True,fullPortVerified=False,releaseReady=False,
             verifierSHA256=sha(Path(__file__).read_bytes())),indent=2)+'\n')
