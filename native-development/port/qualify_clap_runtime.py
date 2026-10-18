"""Finite earned Jax head-clap against an own victim; no broad acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()

names=sys.argv[1:]
assert names and len(names)==len(set(names)),'Supply distinct completed clap fixtures'
cases=[]
for name in names:
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '--clap-victim' in receipt['testArguments']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano'
    identity=18 if actor=='sonya' else 17
    mirror='--mirror' in receipt['testArguments']
    performer,victim=('p2','p1') if mirror else ('p1','p2')
    rows=list(csv.DictReader((folder/'fan.csv').open()))
    objects=list(csv.DictReader((folder/'fan_objects.csv').open()))
    assert objects and all(int(r['character'])==identity and int(r['missing'])==0 for r in objects)
    assert all(int(r['missing'])==0 for r in rows)
    poses=[symbols[f'ks_dc_{actor}_pose{i}'] for i in range(7)]
    observed={int(r['shape'],16) for r in objects}
    assert set(poses)<=observed
    first=[min(int(r['frame']) for r in objects if int(r['shape'],16)==pose) for pose in poses]
    assert first==sorted(first) and len(set(first))==7
    byframe={int(r['frame']):r for r in rows}
    active=next(int(r['frame']) for r in rows if int(r['death'])==1)
    complete=next(int(r['frame']) for r in rows if int(r['frame'])>active and int(r['death'])==65535)
    selection=next(int(r['frame']) for r in rows if int(r['frame'])>complete and int(r['mode']) in (3,4))
    # Native performer completion can precede the parallel victim collapse.
    # Exact same-field scene samples certify ground; sparse intervals and
    # corpse objects across the next screen are deliberately not inferred.
    body=[r for r in objects if int(r['shape'],16) in poses and
          active<=int(r['frame'])<selection and int(r['frame']) in byframe]
    assert len(body)>=50
    ground=131 if actor=='kano' else 132
    for r in body:
        frame=int(r['frame'])
        sample=byframe[frame]
        assert int(r['y'])+ground==int(sample['ground'])
        assert int(sample[performer+'char'])==11 and int(sample[victim+'char'])==identity
    previous=0;kos=[]
    for r in rows:
        hp=int(r[victim+'hp'])
        if int(r['mode'])==2 and int(r[victim+'char'])==identity and int(r[performer+'char'])==11:
            if previous>0 and hp==0 and int(r['frame'])<=active:kos.append(int(r['frame']))
            previous=hp
    assert len(kos)==2,kos
    assert selection>first[-1] and complete>active
    assert any(int(r['frame'])>selection and int(r['mode'])==2 and
               int(r[performer+'char'])==11 and int(r[performer+'hp'])>0 for r in rows)
    assert not (folder/'fan_fault.txt').exists()
    log=(folder/'mame.log').read_text(errors='replace').lower()
    assert 'lua error' not in log and 'error in emu' not in log
    report=dict(scope='One earned native Jax head-clap against one own victim',
                victim=actor,performerPlayer=2 if mirror else 1,
                naturalKOFrames=kos,nativeStart=active,nativeComplete=complete,
                ownBodyPoses=7,firstPoseFrames=first,groundedBodyObservations=len(body),
                postFinishTransitionObserved=True,postFinishMode=int(byframe[selection]['mode']),currentAll26ChipsVerified=True,
                fullVisualAcceptance=False,allEffectCleanupVerified=False,fullPortVerified=False,
                evidenceSHA256={p.name:sha(p) for p in (folder/'autoboot.lua',folder/'fan.csv',folder/'fan_objects.csv',folder/'execution.json')})
    fresh_fields=0;palette_colors=0
    if '--finisher-rejoin' in receipt['testArguments']:
        events=list(csv.DictReader((folder/'finisher_rejoin_events.csv').open()))
        starts=[int(row['frame']) for row in events if row['phase']=='combat']
        assert len(starts)==1
        fresh=[row for row in rows if int(row['frame'])>=starts[0]]
        assert [int(row['frame']) for row in fresh]==list(range(starts[0],starts[0]+600))
        assert all(row['mode']=='2' and row['death']==row['winner']==row['missing']=='0' and
                   row[performer+'char']=='11' and row[victim+'char']==str(identity) for row in fresh)
        assert fresh[0]['p1hp']==fresh[0]['p2hp']=='161'
        assert any(int(row[victim+'hp'])<161 for row in fresh)
        palettes=list(csv.DictReader((folder/'finisher_cleanup.csv').open()))
        assert [int(row['frame']) for row in palettes]==list(range(starts[0],starts[0]+600))
        for row in palettes:
            for side in (1,2):
                assert row[f'p{side}source']==row[f'initialP{side}source']
                assert row[f'p{side}rgbMismatch']=='0'
                colors=int(row[f'p{side}colors']);assert 1<=colors<=256
                palette_colors+=colors
        fresh_fields=600
    report.update(freshCombatFields=fresh_fields,freshHardwarePaletteColorComparisons=palette_colors)
    evidence=[Path(__file__),PORT/'verify_finisher_roms.py',SRC/'MK2P.MAP',SRC/'MKDEATH.ASM']
    evidence.extend(folder/item for item in ('autoboot.lua','fan.csv','fan_objects.csv','execution.json','mame.log'))
    evidence.extend((folder/'snap').glob('fan_pose_*.png'))
    if fresh_fields:evidence.extend([folder/'finisher_rejoin_events.csv',folder/'finisher_cleanup.csv'])
    report['pins']={str(path):sha(path) for path in evidence}
    (folder/'CLAP_RUNTIME_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='evidenceSHA256'}))
    cases.append(dict(run=name,victim=identity,victimSide=1 if mirror else 2,freshCombatFields=fresh_fields,
                      qualificationSHA256=sha(folder/'CLAP_RUNTIME_QUALIFICATION.json')))
if len(cases)==4:
    assert {(case['victim'],case['victimSide']) for case in cases}=={(actor,side) for actor in (17,18) for side in (1,2)}
    assert all(case['freshCombatFields']==600 for case in cases)
    (PORT/'CLAP_MATRIX_QUALIFICATION.json').write_text(json.dumps(dict(cases=cases,allFourFiniteCasesPassed=True,
        fullPortVerified=False,releaseReady=False,verifierSHA256=sha(Path(__file__))),indent=2)+'\n')
