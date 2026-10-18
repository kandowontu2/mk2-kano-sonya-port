"""Report observed CPU behavior and faults, never infer stability from exit0."""
import csv
import json
from pathlib import Path
import sys
import re
import hashlib
import zipfile
from collections import Counter
from verify_finisher_roms import verify
from cpu_observation import post_health_fill_observations

BASE=Path(__file__).resolve().parent.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
recovery=symbols['illegal_opcode']+0x50
for argument in sys.argv[1:]:
    folder=BASE/argument
    rows=list(csv.DictReader((folder/'cpu_attract.csv').open()))
    execution=json.loads((folder/'execution.json').read_text())
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    observer=(folder/'autoboot.lua').read_bytes()
    assert hashlib.sha256(observer).hexdigest().upper()==execution['controllerSHA256']
    assert b':write_u' not in observer
    assert not re.search(rb'\.value\s*=(?!=)',observer)
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify(archive,execution)
    actors={}
    for actor in (17,18):
        observations=[]
        for row in rows:
            for side in (1,2):
                if int(row[f'p{side}char'])==actor:
                    observations.append((row,side))
        actors[str(actor)]={'sampledObjectObservations':len(observations),
            'selectedIdentityMatches':sum(int(row[f'p{side}selected'])==actor for row,side in observations),
            'sidesObserved':sorted({side for _,side in observations}),
            'actionsObserved':sorted({int(row[f'p{side}action']) for row,side in observations})}
        # Presence during a bio/transition is not active AI combat evidence.
        combat,full_frames=post_health_fill_observations(observations,actor)
        combat_keys={(int(row['frame']),side) for row,side in combat}
        dealt=taken=events=0
        for previous,current in zip(rows,rows[1:]):
            if int(current['frame'])-int(previous['frame'])!=2:continue
            if any(current[f'p{s}char']!=previous[f'p{s}char'] for s in (1,2)):continue
            if int(previous['frame'])<=3000:continue
            for side in (1,2):
                other=3-side
                if int(previous[f'p{side}char'])!=actor or int(previous[f'p{side}selected'])!=actor:continue
                if (int(previous['frame']),side) not in combat_keys:continue
                if not all(0<int(previous[f'p{s}hp'])<=161 for s in (1,2)):continue
                if any(int(current[f'p{s}hp'])>int(previous[f'p{s}hp']) for s in (1,2)):continue
                outgoing=int(previous[f'p{other}hp'])-int(current[f'p{other}hp'])
                incoming=int(previous[f'p{side}hp'])-int(current[f'p{side}hp'])
                dealt+=outgoing;taken+=incoming;events+=int(outgoing>0 or incoming>0)
        actors[str(actor)].update(postHealthFillSampledObjectObservations=len(combat),
            observedFullStartingHealthFrames=full_frames,
            postHealthFillActionTagSamples=dict(Counter(f"{int(row[f'p{side}action']):04x}" for row,side in combat)),
            postHealthFillAnimationShapesObserved=len({row[f'p{side}shape'] for row,side in combat}),
            observedOpponentHealthLoss=dealt,observedOwnHealthLoss=taken,
            sampledDamageExchangeEvents=events,
            allOwnSpecialsExecutedVerified=False,allOpponentInteractionsVerified=False)
    fault=(folder/'cpu_fault.txt').exists()
    recoveryObserved=any(int(r['pc'],16)==recovery for r in rows)
    result={'lastRecordedFrame':int(rows[-1]['frame']),'actors':actors,
            'missingMarkers':max(int(r['missing']) for r in rows),
            'faultCapturePresent':fault,'recoveryPCObserved':recoveryObserved,
            'budgetCompleted':int(rows[-1]['frame'])==(42000 if '--cpu-long' in execution['testArguments'] else 30000),
            'exitCode':execution['exitCode'],'timedOut':execution['timedOut'],
            'currentProgramAndGraphicsPinned':True,'recoveryAddressFromCurrentLinkMap':f'{recovery:08x}',
            'currentFull26ROMBytesVerified':True,
            'scope':'Attract-mode sampled object/action observations, not exhaustive CPU gameplay or campaign proof',
            'cpuGameplayVerified':False,'fullPortVerified':False}
    evidence=[folder/'cpu_attract.csv',folder/'execution.json',folder/'autoboot.lua',
              Path(__file__),Path(__file__).parent/'verify_finisher_roms.py',SRC/'MK2P.MAP',
              Path(__file__).parent/'cpu_observation.py']
    result['evidenceSHA256']={str(path):hashlib.sha256(path.read_bytes()).hexdigest().upper() for path in evidence}
    (folder/'cpu_observation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
