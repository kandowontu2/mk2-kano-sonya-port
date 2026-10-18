"""Bounded command/flight/recovery checks; not final move or release acceptance."""
import csv
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from verify_finisher_roms import verify

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def signed16(value):
    n=int(value)
    return n-65536 if n>=32768 else n

def qualify(name,actor,action):
    run=BASE/name
    execution=json.loads((run/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    assert execution['controllerSHA256']==sha(run/'autoboot.lua')
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:
        verify(archive,execution)
    rows=list(csv.DictReader((run/'special.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(int(r['missing'])==0 for r in rows)
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    mirror='--mirror' in execution['testArguments']
    assert actor==((1 if mirror else 2) if action==0x207 else (2 if mirror else 1))
    identities=('18','17') if mirror else ('17','18')
    fight=[r for r in rows if (r['mode'],r['p1char'],r['p2char'])==('2',*identities)]
    key=f'p{actor}action'
    starts=[]
    was_active=False
    for r in fight:
        active=int(r[key])==action
        if active and not was_active: starts.append(r)
        was_active=active
    assert len(starts)>=3
    # First attempt is a deliberately invalid command/prerequisite.
    first=int(fight[0]['frame'])
    assert not any(int(r[key])==action for r in fight if int(r['frame'])<first+100)
    launch=int(starts[0]['frame'])
    assert any(r[key]=='771' and launch<int(r['frame'])<launch+200 for r in fight)
    victim=2 if actor==1 else 1
    assert any(int(r[f'p{victim}hp'])<161 and launch<int(r['frame'])<launch+150 for r in fight)
    if action==0x207:
        assert all(signed16(r[f'p{victim}y'])<80 for r in starts), 'Square launched against a grounded opponent'
    paths=[run/'execution.json',run/'special.csv',run/'autoboot.lua',HERE/'diagnostics/special_probe.lua',
           BASE/'test_wolf_baseline.py',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
           SRC/'KANOMOV.ASM',SRC/'SONYAMOV.ASM',SRC/'KSCMD.ASM',HERE/'verify_finisher_roms.py',Path(__file__)]
    paths+=sorted((run/'snap').glob('*.png'))
    result=dict(scope='bounded native command, hit and recovery smoke test',
                actorID=18 if action==0x207 else 17,physicalSide=actor,nativeAction=action,activationEpisodes=len(starts),
                firstActivation=launch,negativeFirstAttemptRejected=True,
                firstActivationHitAndReturnedToStance=True,
                airborneOpponentAtEverySquareStart=True if action==0x207 else None,
                missingAnimationMarkers=0,sourceLinkedROM=True,customEmulator=False,
                currentFull26ROMBytesVerified=True,
                nativeLaunchAudioCoveredByThisTest=False,finalDamageGeometryAndTimingAccepted=False,
                blockedAndWhiffCasesFullyVerified=False,allMovesVerified=False,releaseReady=False,
                pins={str(path):sha(path) for path in paths})
    (run/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k!='pins'}

def main():
    names=sys.argv[1:]
    assert len(names)==2
    assert all(re.fullmatch(r'[A-Za-z0-9_-]+',name) for name in names)
    mirrors=['--mirror' in json.loads((BASE/name/'execution.json').read_text())['testArguments'] for name in names]
    print(json.dumps([
        qualify(names[0],2 if mirrors[0] else 1,0x20b),
        qualify(names[1],1 if mirrors[1] else 2,0x207)],indent=2))

if __name__=='__main__': main()
