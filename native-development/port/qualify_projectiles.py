"""Qualify bounded native knife/ring scenarios, not full move-set acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import graphics_metadata
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
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:
        verify(archive,execution)
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        data=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        assert hashlib.sha256(data).hexdigest().upper()==execution['replacementChips'][chip]
    graphics=graphics_metadata()
    for chip,digest in graphics['sockets'].items():assert execution['replacementChips'][chip]==digest
    rows=list(csv.DictReader((run/'projectiles.csv').open()))
    assert int(rows[-1]['frame'])==9000
    assert all(int(r['missing'])==0 for r in rows)
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    ids=('18','17') if mirror else ('17','18')
    fight=[r for r in rows if r['mode']=='2' and (r['p1char'],r['p2char'])==ids]
    assert len(fight)>4000
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    moves={}
    for side,fighter,action,latency in [(2 if mirror else 1,'kano',0x211,3),(1 if mirror else 2,'sonya',0x212,15)]:
        key=f'p{side}action';victim=3-side
        starts=[r for i,r in enumerate(fight) if int(r[key])==action and (i==0 or int(fight[i-1][key])!=action)]
        assert len(starts)>=3
        assert not any(int(r[key])==action for r in fight[:200])
        first=int(starts[0]['frame'])
        child=[r for r in fight if int(r[f'p{side}projectiles'])>0]
        assert int(child[0]['frame'])-first==latency
        assert all(int(r[f'p{side}projectiles'])<=1 for r in rows)
        assert all(r[f'p{side}projectileID']==str(17 if fighter=='kano' else 18) for r in child)
        own={v for n,v in symbols.items() if n.startswith(f'ks_{fighter}_pose_')}
        own.update(v for n,v in symbols.items() if n.startswith(f'ks_pp_{fighter}_'))
        seen={int(r[f'p{side}projectileShape'],16) for r in child}
        assert seen and seen<=own
        assert any(r[key]=='771' and first<int(r['frame'])<first+100 for r in fight)
        drops=[(int(r['frame']),int(prev[f'p{victim}hp'])-int(r[f'p{victim}hp']),int(r[f'p{victim}action']))
               for prev,r in zip(fight,fight[1:]) if int(prev[f'p{victim}hp'])>int(r[f'p{victim}hp'])]
        assert any(amount==22 for _,amount,_ in drops)
        assert any(amount==5 and reaction==0x700 for _,amount,reaction in drops)
        assert any(r[f'p{side}projectiles']=='0' and r[key]=='771' and first<int(r['frame'])<first+150 for r in fight)
        moves[fighter]=dict(side=side,nativeAction=action,activationEpisodes=len(starts),
                           firstChildSpawnLatency=latency,projectileShapeCount=len(seen),
                           ownProjectileIdentityAndArt=True,firstWrongDirectionRejected=True,
                           unblockedDamage=22,observedBlockDamage=5,recoveryAndCleanupObserved=True)
    paths=[run/'execution.json',run/'projectiles.csv',run/'autoboot.lua',HERE/'diagnostics/projectile_probe.lua',
           BASE/'test_wolf_baseline.py',SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'KSCMD.ASM',
           SRC/'KSPROJ.ASM',SRC/'KSPJANI.ASM',SRC/'KSPJROOT.ASM',SRC/'MKZAP.ASM',SRC/'MKSTK.ASM',SRC/'MOVES.ASM',
           HERE/'generate_projectile_animations.py',HERE/'generated_projectiles/PROJECTILE_ANIMATIONS.json',
           HERE/'verify_finisher_roms.py',Path(__file__)]
    paths+=sorted((run/'snap').glob('*.png'))
    report=dict(scope='physical command, native projectile identity/art, hit/block and cleanup smoke tests',
                swappedPlayers=mirror,frames=9000,moves=moves,missingRootMarkers=0,
                currentFull26ROMBytesVerified=True,
                nativeLaunchAudioQualifiedByThisTest=False,allWhiffSpacingAndInterruptedCasesVerified=False,
                fullMoveSetVerified=False,releaseReady=False,pins={str(p):sha(p) for p in paths})
    (run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    assert len(sys.argv)>1,'Pass current-ROM test directory names explicitly'
    print(json.dumps([qualify(name,'--mirror' in json.loads((BASE/name/'execution.json').read_text())['testArguments']) for name in sys.argv[1:]],indent=2))
