"""Finite stock-MAME, physical-input Leg Grab evidence; not release acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from verify_finisher_roms import verify

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def qualify(name, side, victim):
    run=BASE/name
    execution=json.loads((run/'execution.json').read_text())
    assert side==(1 if '--mirror' in execution['testArguments'] else 2),'Sonya side must match the physical test profile'
    assert execution['exitCode']==0 and not execution['timedOut']
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    assert execution['controllerSHA256']==sha(run/'autoboot.lua')
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    # Do not associate a newer link map with a historical test binary.
    with zipfile.ZipFile(run/'roms/mk3.zip') as roms:
        verify(roms,execution)
    rows=list(csv.DictReader((run/'leg.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(int(r['missing'])==0 for r in rows)
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    other=3-side
    fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']=='18' and r[f'p{other}char']==str(victim)]
    action=f'p{side}action'
    groups=[]
    for r in fight:
        if r[action]!='538':continue
        if not groups or int(r['frame'])!=int(groups[-1][-1]['frame'])+1:groups.append([])
        groups[-1].append(r)
    assert len(groups)>=4 and all(len(g)==46 for g in groups)
    held=[r for g in groups for r in g]
    assert all(r[f'p{other}action']=='539' for r in held)
    assert all(r[f'p{i}{axis}vel']=='00000000' for r in held for i in (1,2) for axis in ('x','y'))
    drops=[(int(r['frame']),int(prev[f'p{other}hp'])-int(r[f'p{other}hp']))
           for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>int(r[f'p{other}hp'])]
    for g in groups:
        first=int(g[0]['frame'])
        # Physical process order makes P2's victim transfer visible one field later.
        release=first+46+(side==1)
        assert [(frame,amount) for frame,amount in drops if first<=frame<=release]==[(release,35)]
        if first+220<=int(fight[-1]['frame']):
            assert any(r[action]=='771' and r[f'p{other}action']=='771' and release<int(r['frame'])<first+220 for r in fight)
    # Missing Block, low Block, far miss, missing LP, and missing Down.
    for case in [0,2,4,7,8]:
        samples=fight[case*400:(case+1)*400]
        assert samples and not any(r[action]=='538' for r in samples)
        # A natural round restart may refill health; no negative delta is allowed.
        assert all(int(r[f'p{other}hp'])>=int(prev[f'p{other}hp']) for prev,r in zip(samples,samples[1:]))
    for case in [3,5,6,9]:
        assert any(r[action]=='538' for r in fight[case*400:(case+1)*400])
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    assert 'ks_leg_gate' not in symbols
    assets=json.loads((HERE/'generated_leg/LEG_ASSETS.json').read_text())
    expected_body={symbols[f'ks_sonya_pose_{int(a,16):08x}'] for a in assets['body']}
    assert expected_body<={int(r[f'p{side}shape'],16) for r in fight}
    records=assets['victims'][str(victim)]['records']
    assert {int(r[f'p{other}shape'],16) for r in held}=={symbols[label] for _,_,label in records}
    offsets={(abs(int(r[f'p{other}x'])-int(r[f'p{side}x'])),int(r[f'p{other}y'])-int(r[f'p{side}y'])) for r in held}
    expected_offsets={(abs(x),y) for x,y,_ in records}
    expected_offsets.add((abs(records[0][0]),records[0][1]+3))
    assert offsets==expected_offsets,(offsets,expected_offsets)
    paths=[run/'execution.json',run/'leg.csv',run/'autoboot.lua',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
           SRC/'KSLEG.ASM',SRC/'KSLANI.ASM',SRC/'KSPAIR.ASM',SRC/'KSCMD.ASM',SRC/'MOVES.ASM',SRC/'MKDISP.ASM',
           HERE/'generated_leg/LEG_ASSETS.json',HERE/'generate_leg_assets.py',HERE/'prepare_game_candidate.py',
           Path(__file__),BASE/'test_wolf_baseline.py',HERE/'verify_finisher_roms.py']
    report=dict(scope='finite Leg Grab physical chord, block, miss, paired throw and recovery cases',
                side=side,victimID=victim,frames=9000,completedHolds=len(groups),holdLength=46,
                currentFull26ROMBytesVerified=True,
                damagePerRelease=35,sevenOwnBodyPosesAndFiveOwnVictimPosesObserved=True,
                releaseDamageFieldOffset=46+(side==1),
                holdsWithFullRecoveryObservation=sum(int(g[0]['frame'])+220<=int(fight[-1]['frame']) for g in groups),
                exactGripTrajectory=True,lowBlockFarAndIncompleteChordRejected=True,
                standingBlockCaught=True,blockFirstAndSimultaneousChord=True,redundantBlockInput=True,
                earlyLPFirstChordAccepted=any(r[action]=='538' for r in fight[400:800]),
                missingRootMarkers=0,diagnosticGateRemoved=True,
                allVictimsBossesStageEdgesAndAIQualified=False,audioMixQualified=False,
                fullMoveSetVerified=False,releaseReady=False,pins={str(p):sha(p) for p in paths})
    (run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    name,side,victim=sys.argv[1:]
    print(json.dumps(qualify(name,int(side),int(victim)),indent=2))
