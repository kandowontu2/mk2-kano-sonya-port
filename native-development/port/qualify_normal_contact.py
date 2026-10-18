"""Finite HK-request contact: native proximity knee versus standing high kick."""
import csv
import json
import re
import sys
import zipfile
from inspect_normal_runtime import BASE,sha
from verify_finisher_roms import verify

def contact_spec(move,gap,blocking):
    action,hit,chip,reaction={
        ('hk',70):(0x10f,20,6,0x503),('hk',100):(0x103,32,8,0x503),
        ('hp',70):(0x114,24,6,0x503),('hp',100):(0x101,11,3,None),
        ('hp',90):(0x101,11,3,None),('lp',90):(0x102,8,2,None),
        ('lp',70):(0x507,34,34,0x226),('lp',100):(0x102,8,2,None),
        ('lk',100):(0x104,26,6,0x503),
        ('roundhouse',90):(0x105,32,8,None),('sweep',90):(0x106,20,5,None),
        ('uppercut',70):(0x107,40,10,None),('duckpunch',70):(0x119,6,2,None),
        ('duckhighkick',70):(0x113,12,3,None),('ducklowkick',70):(0x11a,6,2,None),
        ('jumpkick',70):(0x10e,32,6,None),('jumppunch',70):(0x118,16,5,None),
        ('flyingkick',180):(0x200,26,7,None),('flyingpunch',180):(0x201,16,5,None),
        ('flyingpunch',220):(0x201,16,5,None),
    }[(move,gap)]
    return action,chip if blocking else hit,reaction

def qualify(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text());args=receipt['testArguments']
    assert all(flag in args for flag in ('--game','--normal-moves'))
    requested=[a.split('=',1)[1] for a in args if a.startswith('--normal-case=')]
    assert len(requested)==1
    move=requested[0]
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    observer=(run/'autoboot.lua').read_text()
    assert receipt['controllerSHA256']==sha(run/'autoboot.lua')
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    log=(run/'mame.log').read_text()
    assert '[LUA ERROR]' not in log and 'Fatal error:' not in log
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
    side=int(next((a.split('=')[1] for a in args if a.startswith('--normal-attacker=')),'1'))
    gap=int(next((a.split('=')[1] for a in args if a.startswith('--normal-gap=')),'70'))
    assert side in (1,2) and gap in (70,90,100,180,220)
    other=3-side;blocking='--normal-block' in args
    guard='1793' if '--normal-low-block' in args else '1792'
    actors=(18,17) if '--mirror' in args else (17,18)
    with (run/'normals.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert rows and [int(r['frame']) for r in rows]==list(range(int(rows[0]['frame']),int(rows[-1]['frame'])+1))
    assert all(r['missing']=='0' and r['p1selected']==r['p1char']==str(actors[0]) and
               r['p2selected']==r['p2char']==str(actors[1]) for r in rows)
    window=[r for r in rows if r['case']==move]
    assert [int(r['age']) for r in window]==list(range(120))
    assert max(int(r['combat']) for r in rows)==240
    assert gap-4<=abs(int(window[0]['p1x'])-int(window[0]['p2x']))<=gap
    action,damage,reaction=contact_spec(move,gap,blocking)
    assert any(int(r[f'p{side}action'])==action for r in window)
    hitby=f'p{other}hitby'
    if hitby in window[0] and action!=0x507:
        assert any(int(r[hitby])==action for r in window),'Native hit-by tag never confirms contact'
    assert int(window[0][f'p{other}hp'])-int(rows[-1][f'p{other}hp'])==damage
    assert all(r[f'p{side}hp']=='161' for r in rows)
    assert rows[-1][f'p{side}action']=='771'
    if blocking and action!=0x507:assert all(r[f'p{other}action']==guard for r in window)
    else:
        if reaction is not None:assert any(int(r[f'p{other}action'])==reaction for r in window)
        assert rows[-1][f'p{other}action']==(guard if blocking else '771')
    report=dict(scope='One physical normal request at one spacing, actual proximity/standing action and damage',
                requestedMove=move,
                actor=actors[side-1],side=side,victim=actors[other-1],gap=gap,blocking=blocking,
                actualAction=action,damage=damage,attackerRecovered=True,
                victimContinuesHoldingBlock=blocking,currentFull26ROMBytesVerified=True,fullPortVerified=False,
                nativeHitByTagObserved=(any(int(r[f'p{other}hitby'])==action for r in window)
                    if f'p{other}hitby' in window[0] else None),
                pins={str(p):sha(p) for p in (run/'execution.json',run/'autoboot.lua',run/'normals.csv')})
    (run/'NORMAL_CONTACT_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    assert len(sys.argv)==2
    r=qualify(sys.argv[1]);print(r['actor'],r['side'],r['gap'],r['blocking'],r['damage'])
