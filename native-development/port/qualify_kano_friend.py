"""Finite native Kano Friendship body/bubble/retirement evidence."""
import csv
from finisher_observation_end import verify_end
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom
from qualify_bubble import BASE,HERE,SRC,sha

run=BASE/sys.argv[1]
execution=json.loads((run/'execution.json').read_text());args=execution['testArguments']
side=2 if '--mirror' in args else 1;other=3-side
victim=1 if '--stock-victim' in args else 18;negative='--punch-wins' in args
morphed='--finisher-morph' in args
if morphed:assert not negative
assert '--kano' in args and '--friend' in args
assert execution['exitCode']==0 and not execution['timedOut']
assert not execution['customDriver'] and not execution['gameMemoryWrites']
assert execution['controllerSHA256']==sha(run/'autoboot.lua')
observer=(run/'autoboot.lua').read_text()
assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert '[LUA ERROR]' not in (run/'mame.log').read_text()
assert not (run/'friend_fault.txt').exists()
with zipfile.ZipFile(run/'roms/mk3.zip') as z:
    verify_full_rom(z,execution)
    for lane,chip in enumerate([54,63]):
        assert z.read(f'mk321u{chip}.bin')==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
    verify_archive_sockets(z)
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
assert 'ks_kano_friend_gate' not in symbols
rows=list(csv.DictReader((run/'friend.csv').open()))
verify_end(run,execution,int(rows[-1]['frame']))
assert all(r['missing']=='0' for r in rows)
fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==('6' if morphed else '17') and r[f'p{other}char']==str(victim)]
ko=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0']
assert len(ko)>=2
assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in fight)
inputs=list(csv.DictReader((run/'friend_inputs.csv').open()))
window={r['frame'] for r in fight if r['winner']=='3' and r['death'] in ('0','7')}
command=[r for r in inputs if r['frame'] in window and [int(r[f'q{i}'],16)>>16 for i in range(4)]==[3,2,2,4]]
assert command
running=[r for r in fight if r['death']=='7']
completed=[r for r in fight if r['death']=='65535' and r['death2']=='2']
if negative:
    assert all(int(r['hpTimestamp'])>0 for r in command)
    assert not running and not completed
else:
    if morphed:
        from finisher_morph_identity import verify as verify_morph
        verify_morph(run,running,17)
    assert all(r['hpTimestamp']=='0' and r['lpTimestamp']=='0' for r in command)
    assert len(running)==193
    first=int(running[0]['frame'])
    assert [int(r['frame']) for r in running]==list(range(first,first+193))
    assert completed and int(completed[0]['frame'])==first+193
    assert all(r[f'p{side}action']=='551' and r[f'p{other}hp']=='0' for r in running)
    data=json.loads((HERE/'generated_friendship/FRIEND_DATA.json').read_text())
    def poses(key):return [symbols[f'ks_friend_pose_{int(g,16):08x}'] for g in data['groups'][key]]
    body=poses('kanoBody');bubble=poses('kanoBubble')
    assert [int(r[f'p{side}shape'],16) for r in running[48:]]==[g for g in body for _ in range(5)]+[body[-1]]*55
    expected=[g for index in [0,1,2,3,4,4,4,4,4,5,6] for g in [bubble[index]] for _ in range(5)]
    assert [int(r['childshape'],16) for r in running[138:]]==expected
    assert all(r['child']=='00000000' for r in running[:138])
    assert len({r['child'] for r in running[138:]})==1 and running[138]['child']!='00000000'
    assert all(r['childx']==r[f'p{side}x'] and r['childy']==r[f'p{side}y'] for r in running[138:])
    assert len({(r[f'p{side}x'],r[f'p{side}y']) for r in running})==1
    life={int(r['frame']):r for r in csv.DictReader((run/'friend_lifetime.csv').open())}
    assert all(life[first+i]['childActive']=='1' and life[first+i]['processActive']=='1' for i in range(138,193))
    assert life[first+193]['childActive']=='0' and life[first+193]['processActive']=='0'
report=dict(scope='finite physical Kano Friendship, own body/bubble poses and native retirement',
            actorID=17,physicalActorSide=side,victimID=victim,frames=int(rows[-1]['frame']),naturalKnockouts=len(ko),
            nativeActionFields=len(running),nativeCompletionObserved=not negative,
            ownBodyBubbleTimingAndRetirementObserved=not negative,punchEligibilityRejected=negative,
            rapidInputDuringKickRecoveryQualified=False,exactPopAudioQualified=False,
            allVictimsEdgesAIAndFreshMatchCleanupQualified=False,fullPortVerified=False,releaseReady=False)
paths=[run/'execution.json',run/'autoboot.lua',run/'friend.csv',run/'friend_inputs.csv',run/'friend_lifetime.csv',
       SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'KSFRIEND.ASM',SRC/'KSCMD.ASM',SRC/'MOVES.ASM',SRC/'MKFRIEND.ASM',
       HERE/'generated_friendship/FRIEND_DATA.json',BASE/'test_wolf_baseline.py',Path(__file__)]
paths+=sorted((run/'snap').glob('*.png'))
if morphed:
    report.update(selectedCharacter=6,activeFinisherCharacter=17,transformedFinisher=True)
    paths.extend([run/'morph_finish.csv',HERE/'finisher_morph_identity.py',SRC/'MKST.ASM'])
report['pins']={str(p):sha(p) for p in paths}
report['pins'][str(HERE/'finisher_observation_end.py')]=sha(HERE/'finisher_observation_end.py')
report['pins'][str(HERE/'verify_finisher_roms.py')]=sha(HERE/'verify_finisher_roms.py')
report['currentFull26ROMBytesVerified']=True
if negative:
    report['nativeIneligibleCommandObservedFrames']=[int(row['frame']) for row in command]
(run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
