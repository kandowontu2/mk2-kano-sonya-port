"""Finite physical Sonya flame-kiss motion/burn/completion evidence."""
import csv
from finisher_observation_end import verify_end
import hashlib
import json
from pathlib import Path
import re
import struct
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
        lo=roms.read('mk321u54.bin');hi=roms.read('mk321u63.bin')
        for lane,raw in enumerate([lo,hi]):
            assert raw==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
        verify_archive_sockets(roms)
        verify_full_rom(roms,execution)
    rom=bytearray(1048576);rom[::2]=lo;rom[1::2]=hi
    def read(address):return struct.unpack_from('<I',rom,(address-0xff800000)//8)[0]
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    rows=list(csv.DictReader((run/'kiss.csv').open()))
    verify_end(run,execution,int(rows[-1]['frame']))
    assert all(r['missing']=='0' for r in rows)
    assert not (run/'kiss_fault.txt').exists()
    other=3-side
    morphed='--finisher-morph' in execution['testArguments']
    fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==('6' if morphed else '18') and r[f'p{other}char']==str(victim)]
    action=[r for r in fight if r[f'p{side}action']=='542']
    assert action
    first=int(action[0]['frame'])
    running=[r for r in action if r['death']=='1']
    if morphed:
        from finisher_morph_identity import verify as verify_morph
        verify_morph(run,running,18)
    assert len(running)==231 and all(int(r['frame'])==first+i for i,r in enumerate(running))
    completed=[r for r in action if r['death']=='65535']
    assert completed and int(completed[0]['frame'])==first+231
    assert all(r['winner']=='3' and r[f'p{other}hp']=='0' for r in running)
    assert all(r[f'p{other}action']=='543' for r in running[1:])
    assert len({r[f'p{other}y'] for r in running})==1, 'Burn must not ground the torso-only flash'
    knockouts=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0' and int(r['frame'])<first]
    assert len(knockouts)>=2
    orb=[r for r in running if r['child']!='00000000']
    assert len(orb)==60 and int(orb[0]['frame'])==first+55 and int(orb[-1]['frame'])==first+114
    assert len({r['child'] for r in orb})==1
    assert all(r['child']=='00000000' for r in running[115:]+completed)
    frames=[read(symbols['ks_kiss_orb_frames']+i*32) for i in range(8)]
    assert {int(r['childshape'],16) for r in orb[1:]}==set(frames)
    for age,r in enumerate(orb[1:],1):
        index=age//6 if age<=42 else (age-43)//3
        assert int(r['childshape'],16)==frames[index]
    # Independently evaluate every fixed-point point of the native arc.
    flip=bool(int(orb[0]['childflags'])&16)
    direction=-1 if flip else 1
    start=orb[0]
    assert int(start['childx'])==int(start[f'p{side}x'])+(-60 if flip else 30)
    assert int(start['childy'])==int(start[f'p{side}y'])+24
    x=int(start['childxval'],16);y=int(start['childyval'],16)
    expected=[(x,y)];vx=direction*6*65536;vy=0;ax=-direction*32768
    def step():
        nonlocal x,y
        x+=vx;y+=vy;expected.append((x,y))
    for _ in range(5):step()
    vy=-7*65536
    for _ in range(28):step();vx+=ax;vy+=16384
    for _ in range(10):step();vx-=ax;vy+=32768
    target_x=int(orb[-1][f'p{other}x'])
    target_y=int(orb[-1]['ground'])-88
    vx=((target_x-(x>>16))<<16)>>4
    vy=((target_y-(y>>16))<<16)>>4
    for _ in range(16):step()
    assert [(int(r['childxval'],16),int(r['childyval'],16)) for r in orb]==expected
    assert (int(orb[-1]['childx']),int(orb[-1]['childy']))==(target_x,target_y)
    data=json.loads((HERE/'generated_kiss/KISS_DATA.json').read_text())
    burn=[symbols[g] for g in data['burn']]
    assert [int(r[f'p{other}shape'],16) for r in running[115:]]==[g for g in burn for _ in range(4)]
    performer=[read(symbols['ks_finish_sonya_kiss']+i*32) for i in range(11)]
    outro=[symbols[f'ks_sonya_pose_{int(g,16):08x}'] for g in data['outro']]
    expected_body=[g for g in performer for _ in range(5)]+[performer[-1]]*132
    expected_body += [g for g,count in zip(outro,[1,1,4,1,1,1,1,1]) for _ in range(count*4)]
    assert [int(r[f'p{side}shape'],16) for r in running]==expected_body
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in running+completed)
    paths=[run/'execution.json',run/'kiss.csv',run/'autoboot.lua',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
           SRC/'KSKISS.ASM',SRC/'KSCMD.ASM',SRC/'KSKSANI.ASM',SRC/'KSFART.ASM',SRC/'KSFANI.ASM',
           SRC/'MKDEATH.ASM',SRC/'MOVES.ASM',HERE/'generate_kiss_data.py',HERE/'generated_kiss/KISS_DATA.json',
           HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',Path(__file__)]
    paths.append(HERE/'verify_finisher_roms.py')
    paths.append(HERE/'finisher_observation_end.py')
    paths+=sorted((run/'snap').glob('*.png'))
    if morphed: paths.extend([run/'morph_finish.csv',HERE/'finisher_morph_identity.py',SRC/'MKST.ASM'])
    report=dict(scope='finite native flame-kiss after physically winning two rounds',
                selectedCharacter=6 if morphed else 18,activeFinisherCharacter=18,transformedFinisher=morphed,
                side=side,victimID=victim,frames=int(rows[-1]['frame']),naturalKnockoutsBeforeFatality=len(knockouts),
                nativeActionFields=231,performerPoses=11,salutePoses=8,orbFrames=8,
                orbFields=60,everyFixedPointMotionStepVerified=True,stageRelativeHomingTarget=[target_x,target_y],
                orbDeletedBeforeBurn=True,burnFields=116,burnUniquePoses=15,victimStandingOriginPreserved=True,
                nativeCompletionObserved=True,missingRootMarkers=0,currentFull26ROMBytesVerified=True,
                allVictimsEdgesAndAIQualified=False,freshMatchCleanupQualified=False,
                exactNativeLaunchAudioAndMixQualified=False,otherFatalitiesCoveredByThisTest=False,
                fullMoveSetVerified=False,releaseReady=False,pins={str(p):sha(p) for p in paths})
    (run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    name,side,victim=sys.argv[1:]
    print(json.dumps(qualify(name,int(side),int(victim)),indent=2))
