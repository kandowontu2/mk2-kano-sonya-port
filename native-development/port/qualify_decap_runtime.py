"""Finite physical Kitana decapitation evidence, not whole-port acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import graphics_metadata
from inventory_character_tables import source_tables
PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
for argument in sys.argv[1:]:
    folder=BASE/argument
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        program=b''.join((BUILD/f'rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        assert sha(program)==receipt['replacementChips'][chip]
    graphics=graphics_metadata()
    for name,digest in graphics['sockets'].items():
        assert receipt['replacementChips'][name]==digest
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano'
    tongue='--tongue-victim' in receipt['testArguments']
    if tongue:
        tables=source_tables((BUILD/'MKDEATH.ASM').read_text())
        lineup=tables['head_lineups']
        values=[v.lower() for row in lineup['rows'] for v in row['values']]
        assert all(row['type']=='word' for row in lineup['rows']) and len(values)==19*4
        with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
            original=source_tables(z.read('mk2-rebuild-main/src/MKDEATH.ASM').decode('cp437'))['head_lineups']
        assert values[:64]==[v.lower() for row in original['rows'] for v in row['values']]
        assert values[-8:]==['-0bbh','0','010h','020h','-0bbh','-1','010h','020h']
    identity=18 if actor=='sonya' else 17
    rows=list(csv.DictReader((folder/'fan_objects.csv').open()))
    assert rows and all(int(r['missing'])==0 and int(r['character'])==identity for r in rows)
    body=[symbols[f'ks_dc_{actor}_pose{i}'] for i in range(7)]
    heads=[symbols[f'ks_hd_{actor}_frame{i}'] for i in range(1 if tongue else 7)]
    assert set(body)<=set(int(r['shape'],16) for r in rows)
    assert set(heads)<=set(int(r['image'],16) for r in rows)
    first=[min(int(r['frame']) for r in rows if int(r['shape'],16)==pose) for pose in body]
    assert first==sorted(first) and len(set(first))==7
    main=list(csv.DictReader((folder/'fan.csv').open()))
    origin=next(r for r in main if int(r['frame'])==first[0])
    ground=int(origin['ground'])
    offset=131 if actor=='kano' else 132
    body_rows=[r for r in rows if int(r['shape'],16) in body]
    assert all(int(r['y'])+offset==ground for r in body_rows)
    tongue_path=None
    if tongue:
        head_rows=[r for r in rows if int(r['image'],16)==heads[0]]
        assert len(head_rows)>=20
        xs=[int(r['x']) for r in head_rows]
        direction=1 if '--mirror' in receipt['testArguments'] else -1
        # tproc9 explicitly relocates the head into the mouth after tongue
        # retraction. Verify the tongue phase separately from that native snap.
        initial_y=int(head_rows[0]['y'])
        mouth=next((i for i,r in enumerate(head_rows) if int(r['y'])!=initial_y),len(head_rows))
        assert mouth>=12 and mouth<len(head_rows)
        assert all((b-a)*direction>=0 for a,b in zip(xs[:mouth],xs[1:mouth]))
        assert len({(r['x'],r['y']) for r in head_rows[mouth:]})==1
        assert (xs[-1]-xs[0])*direction>=100
        assert max(int(r['frame']) for r in head_rows)<max(int(r['frame']) for r in body_rows)
        tongue_path=dict(observations=len(head_rows),startX=xs[0],endX=xs[-1],
                         tonguePhaseObservations=mouth,nativeMouthPlacementObserved=True,
                         retractsTowardPerformer=True,headRemovedWhileBodyRemains=True)
    assert max(int(r['missing']) for r in main)==0
    assert any(r['death']==('1' if tongue else '2') for r in rows) and any(r['death']=='65535' for r in rows)
    assert not (folder/'fan_fault.txt').exists()
    result=dict(qualified=True,scope='One physical native decapitation against an added victim',
                performer='reptile' if tongue else 'kitana',
                victim=actor,performerPlayer=2 if '--mirror' in receipt['testArguments'] else 1,
                ownBodyPosesObserved=7,ownHeadFramesObserved=len(heads),bodyFirstFrames=first,
                bodyGroundPlane=ground,bodyGroundAlignedObservations=len(body_rows),
                nativeCompletionObserved=True,missingMarkers=0,
                tongueHeadPath=tongue_path,
                fullVisualAcceptance=False,fullPortVerified=False)
    (folder/'DECAP_RUNTIME_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
