"""Finite real-round native Kano extraction check, not all-finisher acceptance."""
import csv
from finisher_observation_end import verify_end
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def qualify(name,side,victim):
    run=BASE/name
    execution=json.loads((run/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    assert execution['controllerSHA256']==sha(run/'autoboot.lua')
    assert side==(2 if '--mirror' in execution['testArguments'] else 1),'Performer side disagrees with the physical controller profile'
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    with zipfile.ZipFile(run/'roms/mk3.zip') as roms:
        for lane,name in [(0,'mk321u54.bin'),(1,'mk321u63.bin')]:
            assert roms.read(name)==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
        verify_archive_sockets(roms)
        verify_full_rom(roms,execution)
    rows=list(csv.DictReader((run/'extract.csv').open()))
    verify_end(run,execution,int(rows[-1]['frame']))
    assert all(r['missing']=='0' for r in rows)
    assert not (run/'extract_fault.txt').exists()
    other=3-side
    morphed='--finisher-morph' in execution['testArguments']
    selected=6 if morphed else 17
    fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==str(selected) and r[f'p{other}char']==str(victim)]
    active=[r for r in fight if r[f'p{side}action']=='540']
    assert active
    first=int(active[0]['frame'])
    running=[r for r in active if r['death']=='1']
    assert len(running)==231
    if morphed:
        identity={r['frame']:r for r in csv.DictReader((run/'morph_finish.csv').open())}
        assert all(identity[r['frame']]['selected']=='6' and identity[r['frame']]['actual']=='17' for r in running)
        assert any(r['selected']==r['actual']=='6' and r['winner']=='3' and int(r['frame'])<first for r in identity.values())
    completed=[r for r in active if r['death']=='65535']
    assert completed and int(completed[0]['frame'])==first+231
    assert all(r['winner']=='3' and r[f'p{other}hp']=='0' for r in active)
    assert all(r[f'p{other}action']=='541' for r in running[1:])
    # At least two distinct natural HP depletion events precede the fatality.
    knockouts=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0' and int(r['frame'])<first]
    assert len(knockouts)>=2
    assert any(int(r[f'p{other}hp'])>0 and int(r['frame'])>int(knockouts[0]['frame']) and int(r['frame'])<first for r in fight)
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    data=json.loads((HERE/'generated_extract/EXTRACT_DATA.json').read_text())
    body={symbols[f'ks_finish_pose_{int(g,16):08x}'] for g in data['body']}
    skeleton={symbols[f'ks_finish_pose_{int(g,16):08x}'] for g in data['skeleton']}
    victim_shapes={symbols[g] for g in data['victims'][str(victim)]}
    assert {int(r[f'p{side}shape'],16) for r in running}==body
    assert {int(r['childshape'],16) for r in running if r['child']!='00000000'}==skeleton
    assert victim_shapes<={int(r[f'p{other}shape'],16) for r in running}
    spawn=[r for r in running if r['child']!='00000000']
    assert int(spawn[0]['frame'])==first+83
    assert len({r['child'] for r in spawn})==1
    groups=[]
    for r in spawn:
        if not groups or r['childshape']!=groups[-1][-1]['childshape']:groups.append([])
        groups[-1].append(r)
    assert len(groups)==6 and all(len(g)==8 for g in groups[:5])
    assert all(r['child']==spawn[0]['child'] for r in completed)
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in running+completed)
    paths=[run/'execution.json',run/'extract.csv',run/'autoboot.lua',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
           SRC/'KSFATAL.ASM',SRC/'KSCMD.ASM',SRC/'KSEXANI.ASM',SRC/'KSFART.ASM',SRC/'MKDEATH.ASM',SRC/'MOVES.ASM',
           HERE/'generated_extract/EXTRACT_DATA.json',HERE/'generate_extract_data.py',
           HERE/'generated_finishers/FINISHER_ASSETS.json',HERE/'prepare_game_candidate.py',
           BASE/'test_wolf_baseline.py',Path(__file__)]
    paths.append(HERE/'verify_finisher_roms.py')
    paths.append(HERE/'finisher_observation_end.py')
    if morphed: paths.extend([run/'morph_finish.csv',SRC/'MKST.ASM',HERE/'diagnostics/extract_probe.lua'])
    paths+=sorted((run/'snap').glob('*.png'))
    report=dict(scope='one native Kano extraction after physically winning two rounds',
                side=side,victimID=victim,selectedCharacter=selected,activeFinisherCharacter=17,transformedFinisher=morphed,
                frames=int(rows[-1]['frame']),naturalKnockoutsBeforeFatality=len(knockouts),
                nativeActionFields=231,ownBodyPoses=9,attachedSkeletonPhases=6,
                characterOwnedVictimPhases=6,skeletonSpawnAge=83,skeletonPhaseFields=8,
                nativeCompletionObserved=True,missingRootMarkers=0,currentFull26ROMBytesVerified=True,
                allVictimsEdgesAndAIQualified=False,newMatchChildTeardownQualified=False,
                nativeAudioMixQualified=False,otherFatalitiesCoveredByThisTest=False,
                fullMoveSetVerified=False,releaseReady=False,pins={str(p):sha(p) for p in paths})
    (run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    name,side,victim=sys.argv[1:]
    print(json.dumps(qualify(name,int(side),int(victim)),indent=2))
