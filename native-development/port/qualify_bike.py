"""Finite two-sided bicycle seek/block/paired/recovery qualification."""
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
def signed16(n):return (int(n)+32768)%65536-32768

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
    rows=list(csv.DictReader((run/'bike.csv').open()))
    tail='--bike-audio-tail' in execution['testArguments']
    assert int(rows[-1]['frame'])==(9180 if tail else 9000)
    assert all(int(r['missing'])==0 for r in rows)
    # Tail mode adds only neutral controls after the unchanged behavior fixture.
    rows=[row for row in rows if int(row['frame'])<=9000]
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    ids=('18','17') if mirror else ('17','18')
    fight=[r for r in rows if r['mode']=='2' and (r['p1char'],r['p2char'])==ids]
    side=1 if mirror else 2;victim=3-side
    action=f'p{side}action';vaction=f'p{victim}action'
    starts=[r for i,r in enumerate(fight) if r[action]=='516' and (i==0 or fight[i-1][action]!='516')]
    assert len(starts)>=5
    assert not any(r[action]=='516' for r in fight[:350]), 'Incomplete B,D command activated bicycle'
    paired=[r for r in fight if r[action]=='532']
    assert len(paired)>250
    assert all(r[vaction]=='533' for r in paired)
    assert all(r[f'p{side}xvel']==r[f'p{victim}xvel'] and r[f'p{side}yvel']==r[f'p{victim}yvel'] for r in paired)
    assert {r[f'p{side}yvel'] for r in paired}=={'fffd0000','00008000'}
    assert {abs(int(r[f'p{side}xvel'],16) if int(r[f'p{side}xvel'],16)<0x80000000 else int(r[f'p{side}xvel'],16)-0x100000000) for r in paired}=={0x30000,0x10000}
    stable=[]
    previous=None
    for r in paired:
        frame=int(r['frame'])
        if previous==frame-1:stable.append(r)
        previous=frame
    assert all(abs(int(r[f'p{victim}x'])-int(r[f'p{side}x']))==48 and
               signed16(int(r[f'p{victim}y'])-int(r[f'p{side}y']))==-32 for r in stable)
    assert all((int(r[f'p{victim}x'])-int(r[f'p{side}x']))==
               (48 if int(r[f'p{side}xvel'],16)<0x80000000 else -48) for r in stable)
    drops=[(int(r['frame']),int(prev[f'p{victim}hp'])-int(r[f'p{victim}hp']),r[vaction],r[action])
           for prev,r in zip(fight,fight[1:]) if int(prev[f'p{victim}hp'])>int(r[f'p{victim}hp'])]
    assert any(amount==22 and own=='532' for _,amount,_,own in drops)
    assert any(amount==3 and state=='1792' for _,amount,state,_ in drops)
    first=int(starts[0]['frame'])
    assert any(r[action]=='771' and r[vaction]=='771' and first<int(r['frame'])<first+200 for r in fight)
    # Third valid attempt is a held duck: no paired capture or damage is allowed.
    begin=int(fight[0]['frame'])
    duck=[r for i,r in enumerate(fight) if 1200<=i+1<1600]
    assert duck and not any(r[action]=='532' for r in duck)
    assert len({r[f'p{victim}hp'] for r in duck})==1
    assert any(r[action]=='1553' for r in duck)
    assert any(r[action]=='771' and r[vaction]=='770' for r in duck)
    far=[r for i,r in enumerate(fight) if 1600<=i+1<2000]
    assert far and not any(r[action]=='532' for r in far)
    assert len({r[f'p{victim}hp'] for r in far})==1
    assert any(r[action]=='771' and r[vaction]=='771' for r in far if int(r['frame'])>begin+1850)
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    assets=json.loads((HERE/'generated_bike/BIKE_ASSETS.json').read_text())
    expected={symbols[f'ks_sonya_pose_{int(a,16):08x}'] for a in assets['intro']+assets['cycle']+assets['end']}
    observed={int(r[f'p{side}shape'],16) for r in fight}
    assert expected<=observed
    victim_own={v for n,v in symbols.items() if n.startswith('ks_kano_pose_')}
    assert {int(r[f'p{victim}shape'],16) for r in paired}<=victim_own
    paths=[run/'execution.json',run/'bike.csv',run/'autoboot.lua',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
           SRC/'KSBIKE.ASM',SRC/'KSBIANI.ASM',SRC/'KSCMD.ASM',SRC/'MOVES.ASM',SRC/'MKREACT.ASM',
           HERE/'generated_bike/BIKE_ASSETS.json',HERE/'generate_bike_assets.py',
           HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',HERE/'verify_finisher_roms.py',Path(__file__)]
    paths+=sorted((run/'snap').glob('*.png'))
    result=dict(scope='bounded physical bicycle command/hit/block/duck/far-miss/paired release',
                side=side,frames=9000,activationEpisodes=len(starts),pairedFields=len(paired),
                currentFull26ROMBytesVerified=True,
                pairedGeometryAfterFirstContactField=[48,-32],pairedVelocitiesBothPhasesMatched=True,
                victimInFrontOfSonya=True,victimRetainedOwnArt=True,
                ownBicyclePosesObserved=len(expected),unblockedDamage=22,blockDamage=3,
                incompleteCommandRejected=True,duckAndFarMissesRecovered=True,
                firstPairReleasedAndBothReturnedToStance=True,missingRootMarkers=0,
                bossOtherVictimsAllArenasAndAIQualified=False,nativeLaunchVoiceCoveredByThisTest=False,
                fullMoveSetVerified=False,releaseReady=False,pins={str(p):sha(p) for p in paths})
    (run/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k!='pins'}

if __name__=='__main__':
    assert len(sys.argv)>1,'Pass completed current-ROM run names explicitly'
    assert all(re.fullmatch(r'[A-Za-z0-9_-]+',name) for name in sys.argv[1:])
    print(json.dumps([qualify(name,'--mirror' in json.loads((BASE/name/'execution.json').read_text())['testArguments'])
                      for name in sys.argv[1:]],indent=2))
