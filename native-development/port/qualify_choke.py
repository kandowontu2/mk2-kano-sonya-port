"""Bounded native choke command/trajectory/four-pulse/release checks."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from verify_finisher_roms import verify

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def signed16(n):return (int(n)+32768)%65536-32768

def stock_victim_pose(read,table,victim):
    assert victim in (*range(12),14,15,16)
    anitab=read(table+victim*32)
    return read(read(anitab+16*32)+32)

def qualify(name,side,victim):
    run=BASE/name
    execution=json.loads((run/'execution.json').read_text())
    arguments=execution['testArguments']
    selected_victim=next((int(arg.split('=',1)[1]) for arg in arguments if arg.startswith('--choke-victim=')),1 if '--stock-victim' in arguments else 18)
    assert victim==selected_victim, 'Victim must match the physical selector profile'
    assert side==(2 if '--mirror' in execution['testArguments'] else 1),'Kano side must match the physical test profile'
    assert execution['exitCode']==0 and not execution['timedOut']
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    assert execution['controllerSHA256']==sha(run/'autoboot.lua')
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:
        verify(archive,execution)
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    rows=list(csv.DictReader((run/'choke.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(int(r['missing'])==0 for r in rows)
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    other=3-side
    fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']=='17' and r[f'p{other}char']==str(victim)]
    action=f'p{side}action';vaction=f'p{other}action'
    groups=[]
    for r in fight:
        if r[action]!='535':continue
        if not groups or int(r['frame'])!=int(groups[-1][-1]['frame'])+1:groups.append([])
        groups[-1].append(r)
    assert len(groups)>=5 and all(len(g)==69 for g in groups)
    crouch_entry='--choke-crouch-entry' in arguments
    crouch_fields=0
    if crouch_entry:
        assert '--choke-fast-command' in arguments
        first_hold=int(groups[0][0]['frame'])
        startup=[r for r in fight if first_hold-16<=int(r['frame'])<first_hold and r[action]=='534']
        assert startup
        first_seek=int(startup[0]['frame'])
        duck=[r for r in fight if first_seek-16<=int(r['frame'])<first_seek and r[action]=='770']
        assert len(duck)>=6, 'Crouch entry must observe sustained native duck before Choke'
        assert not any(r[action]=='771' for r in fight if int(duck[-1]['frame'])<=int(r['frame'])<first_seek), 'Returned to stance before Choke'
        crouch_fields=len(duck)
    held=[r for g in groups for r in g]
    assert all(r[vaction]=='536' for r in held)
    assert all(r[f'p{i}{axis}vel']=='00000000' for r in held for i in (1,2) for axis in ('x','y'))
    assets=json.loads((HERE/'generated_choke/CHOKE_ASSETS.json').read_text())
    records=assets['victims'][str(victim)]['records']
    expected_offsets={(abs(x),y) for x,y,_ in records}
    actual_offsets={(abs(int(r[f'p{other}x'])-int(r[f'p{side}x'])),signed16(int(r[f'p{other}y'])-int(r[f'p{side}y']))) for r in held}
    assert actual_offsets==expected_offsets
    drops=[(int(r['frame']),int(prev[f'p{other}hp'])-int(r[f'p{other}hp']))
           for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>int(r[f'p{other}hp'])]
    first=int(groups[0][0]['frame'])
    first_drops=[(frame,amount) for frame,amount in drops if first<=frame<first+69]
    assert first_drops==[(first+t,8) for t in (27,39,51,63)]
    assert any(r[action]=='771' and r[vaction]=='771' and first+69<int(r['frame'])<first+200 for r in fight)
    # Early far whiff; standing block; later far miss; held duck.
    for start,end in [(1,400),(800,1200),(1200,1600),(1600,2000)]:
        case=[r for i,r in enumerate(fight,1) if start<=i<end]
        assert case and not any(r[action]=='535' for r in case)
        assert len({r[f'p{other}hp'] for r in case})==1
        assert any(r[action]=='771' for r in case)
    block=[r for i,r in enumerate(fight,1) if 800<=i<1200]
    assert any(r[action]=='534' and r[vaction]=='1792' for r in block)
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    expected_body={symbols[f'ks_kano_pose_{int(a,16):08x}'] for poses in assets['phases'].values() for a in poses}
    assert expected_body<={int(r[f'p{side}shape'],16) for r in fight}
    if victim==18:
        expected_victim={symbols[pose] for _,_,pose in records}
    else:
        with zipfile.ZipFile(run/'roms/mk3.zip') as z:
            lo=z.read('mk321u54.bin');hi=z.read('mk321u63.bin')
        rom=bytearray(len(lo)*2);rom[::2]=lo;rom[1::2]=hi
        def read(address):return struct.unpack_from('<I',rom,(address-0xff800000)//8)[0]
        # Match get_char_ani: index this victim's linked animation table,
        # then high-hit animation10h, pose2. Never assume every stock victim
        # is Liu Kang merely because he was the original fixture opponent.
        expected_victim={stock_victim_pose(read,symbols['character_anitabs1'],victim)}
    assert {int(r[f'p{other}shape'],16) for r in held}==expected_victim
    paths=[run/'execution.json',run/'choke.csv',run/'autoboot.lua',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
           SRC/'KSCHOKE.ASM',SRC/'KSCANI.ASM',SRC/'KSCMD.ASM',SRC/'MOVES.ASM',SRC/'MKREACT.ASM',SRC/'MKSOUND.ASM',SRC/'KSPAIR.ASM',SRC/'MKGUYS.ASM',
           HERE/'generated_choke/CHOKE_ASSETS.json',HERE/'generate_choke_assets.py',
           HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',HERE/'verify_finisher_roms.py',Path(__file__)]
    paths+=sorted((run/'snap').glob('*.png'))
    report=dict(scope='finite physical choke hit/block/duck/far/paired-pulse/release cases',
                side=side,victimID=victim,frames=9000,completedHolds=len(groups),heldFields=len(held),
                crouchEntryWithoutStanceVerified=crouch_entry,sustainedDuckFieldsBeforeFirstSeek=crouch_fields,
                currentFull26ROMBytesVerified=True,
                holdLength=69,firstHoldDamagePulses=first_drops,firstHoldTotalDamage=32,
                originalGripTrajectoryAndOwnVictimArt=victim==18,selectedVictimTrajectoryAndArtVerified=True,allEightOwnBodyPosesObserved=True,
                blockDuckFarRejections=True,bothRecoveredAfterFirstHold=True,missingRootMarkers=0,
                allOtherVictimsBossesStageEdgesAndAIQualified=False,audioMixQualified=False,
                fullMoveSetVerified=False,releaseReady=False,pins={str(p):sha(p) for p in paths})
    (run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    assert len(sys.argv)==4, 'Usage: qualify_choke.py RUN SIDE VICTIM_ID'
    print(json.dumps(qualify(sys.argv[1],int(sys.argv[2]),int(sys.argv[3])),indent=2))
