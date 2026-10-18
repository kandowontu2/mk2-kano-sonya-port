"""Finite native blade whiff/hit/block/interruption checks on both player sides."""
import csv
import hashlib
import json
from pathlib import Path
import re
import zipfile
import sys
from verify_finisher_roms import verify

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def qualify(name,mirror):
    run=BASE/name
    execution=json.loads((run/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    assert execution['controllerSHA256']==sha(run/'autoboot.lua')
    assert mirror==('--mirror' in execution['testArguments'])
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:
        verify(archive,execution)
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    rows=list(csv.DictReader((run/'blade.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(int(r['missing'])==0 for r in rows)
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    ids=('18','17') if mirror else ('17','18')
    fight=[r for r in rows if r['mode']=='2' and (r['p1char'],r['p2char'])==ids]
    side=2 if mirror else 1;victim=3-side
    action=f'p{side}action';slave=f'p{side}slave'
    starts=[r for i,r in enumerate(fight) if r[action]=='279' and (i==0 or fight[i-1][action]!='279')]
    assert len(starts)>=5
    # First action deliberately whiffs. Every complete action owns an attached trail.
    launch=int(starts[0]['frame'])
    first=[r for r in fight if launch<=int(r['frame'])<launch+120]
    assert all(r['p1hp']=='161' and r['p2hp']=='161' for r in first)
    assert any(r[slave]!='00000000' for r in first)
    assert any(r[slave]=='00000000' and r[action]=='771' for r in first)
    drops=[(int(r['frame']),int(prev[f'p{victim}hp'])-int(r[f'p{victim}hp']),int(r[f'p{victim}action']))
           for prev,r in zip(fight,fight[1:]) if int(prev[f'p{victim}hp'])>int(r[f'p{victim}hp'])]
    assert any(amount==26 for _,amount,_ in drops)
    assert any(amount==3 and state==0x700 for _,amount,state in drops)
    interrupted=[(prev,r) for prev,r in zip(fight,fight[1:])
                 if int(prev[f'p{side}hp'])>int(r[f'p{side}hp'])]
    assert len(interrupted)==1
    before,hit=interrupted[0]
    frame=int(hit['frame'])
    assert int(before[f'p{side}hp'])-int(hit[f'p{side}hp'])==11
    assert before[slave]!='00000000'
    assert any(r[slave]=='00000000' for r in fight if frame<=int(r['frame'])<=frame+2)
    assert all(r[slave]=='00000000' for r in fight if frame+2<=int(r['frame'])<frame+100)
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    own={v for n,v in symbols.items() if n.startswith('ks_kano_pose_')}
    body={int(r[f'p{side}shape'],16) for r in fight if r[action]=='279'}
    assert body and body<=own
    assets=json.loads((HERE/'generated_blade/BLADE_ASSETS.json').read_text())
    expected={symbols[f'ks_kano_pose_{int(a,16):08x}'] for a in assets['bodyPoses']}
    observed={int(r[f'p{side}shape'],16) for r in fight}
    assert expected<=observed
    paths=[run/'execution.json',run/'blade.csv',run/'autoboot.lua',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
           SRC/'KSBLADE.ASM',SRC/'KSBANI.ASM',SRC/'KSCMD.ASM',SRC/'JOY.ASM',SRC/'MKREACT.ASM',
           HERE/'generated_blade/BLADE_ASSETS.json',HERE/'generate_blade_assets.py',
           HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',HERE/'verify_finisher_roms.py',Path(__file__)]
    paths+=sorted((run/'snap').glob('*.png'))
    result=dict(scope='bounded physical Blade Swipe whiff/hit/block/interruption',side=side,
                frames=9000,activations=len(starts),ownBladePosesObserved=len(expected),whiffCleanup=True,
                currentFull26ROMBytesVerified=True,
                unblockedDamage=26,blockDamage=3,interruptionDamage=11,
                attachedTrailRetiredWithinTwoObserverFields=True,missingRootMarkers=0,
                allVictimBossAirborneAndSpacingCasesVerified=False,audioMixVerified=False,
                fullMoveSetVerified=False,releaseReady=False,pins={str(p):sha(p) for p in paths})
    (run/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k!='pins'}

if __name__=='__main__':
    assert len(sys.argv)>1,'Pass completed current-ROM run names explicitly'
    assert all(re.fullmatch(r'[A-Za-z0-9_-]+',name) for name in sys.argv[1:])
    print(json.dumps([qualify(name,'--mirror' in json.loads((BASE/name/'execution.json').read_text())['testArguments'])
                      for name in sys.argv[1:]],indent=2))
