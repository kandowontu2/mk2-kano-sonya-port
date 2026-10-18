"""Finite native Sonya Friendship command, own poses, timing and completion."""
import csv
from finisher_observation_end import verify_end
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom
from qualify_bubble import BASE,HERE,SRC,sha

run=BASE/sys.argv[1]
execution=json.loads((run/'execution.json').read_text())
args=execution['testArguments'];side=2 if '--mirror' in args else 1;other=3-side
victim=1 if '--stock-victim' in args else 17
morphed='--finisher-morph' in args
negative='--punch-wins' in args or morphed
assert execution['exitCode']==0 and not execution['timedOut']
assert not execution['customDriver'] and not execution['gameMemoryWrites']
assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert execution['controllerSHA256']==sha(run/'autoboot.lua')
observer=(run/'autoboot.lua').read_text()
assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
assert '[LUA ERROR]' not in (run/'mame.log').read_text()
assert not (run/'friend_fault.txt').exists()
with zipfile.ZipFile(run/'roms/mk3.zip') as z:
    verify_full_rom(z,execution)
    lanes=[z.read(f'mk321u{chip}.bin') for chip in [54,63]]
    for lane,raw in enumerate(lanes):
        assert raw==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
    verify_archive_sockets(z)
rom=bytearray(1048576);rom[::2]=lanes[0];rom[1::2]=lanes[1]
def read(address):return struct.unpack_from('<I',rom,(address-0xff800000)//8)[0]
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
rows=list(csv.DictReader((run/'friend.csv').open()))
verify_end(run,execution,int(rows[-1]['frame']))
assert all(r['missing']=='0' for r in rows)
fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==('6' if morphed else '18') and r[f'p{other}char']==str(victim)]
assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in fight)
ko=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0']
assert len(ko)>=2
running=[r for r in fight if r['death']=='7']
completed=[r for r in fight if r['death']=='65535' and r['death2']=='2']
if negative:
    from finisher_eligibility import verify_punch_rejection
    eligibility_path,command_frames=verify_punch_rejection(run,18,'friend',{r['frame'] for r in fight if r['winner']=='3' and r['death']=='0'})
    if morphed:
        from finisher_morph_identity import verify as verify_morph
        verify_morph(run,[dict(frame=str(frame)) for frame in command_frames],18)
        assert '--punch-wins' not in args
        eligibility=list(csv.DictReader(eligibility_path.open()))
        command_set=set(command_frames)
        assert all(r['hpTimestamp']=='0' and int(r['lpTimestamp'])>0 for r in eligibility if int(r['frame']) in command_set)
        assert any(r['hpTimestamp']==r['lpTimestamp']=='0' and int(r['frame'])<command_frames[0] for r in eligibility)
    assert not running and not completed
    assert len([r for r in fight if r['winner']=='3'])>=150
else:
    assert len(running)==176
    first=int(running[0]['frame'])
    assert [int(r['frame']) for r in running]==list(range(first,first+176))
    assert completed and int(completed[0]['frame'])==first+176
    assert all(r[f'p{side}action']=='550' and r['winner']=='3' and r[f'p{other}hp']=='0' for r in running)
    intro=[read(symbols['ks_friend_sonya_intro']+i*32) for i in range(7)]
    groups=[int(g,16) for g in json.loads((HERE/'generated_friendship/FRIEND_DATA.json').read_text())['groups']['sonyaBody']]
    poses=[symbols[f'ks_friend_pose_{g:08x}'] for g in groups]
    loop=[poses[i] for i in [7,8,9,10,9,8,7,6,5,4,3,4,5,6]]
    expected=[v for v in intro for _ in range(5)]
    expected += [loop[(i//3)%14] for i in range(93)]
    assert [int(r[f'p{side}shape'],16) for r in running[48:]]==expected
    assert len({(r[f'p{side}x'],r[f'p{side}y']) for r in running})==1
report=dict(scope='finite physical Sonya Friendship against stationary selected victim',
            actorID=18,physicalActorSide=side,victimID=victim,frames=int(rows[-1]['frame']),naturalKnockouts=len(ko),
            nativeActionFields=len(running),nativeCompletionObserved=not negative,
            allIntroAndLoopPosesWithTimingObserved=not negative,punchEligibilityRejected=negative,
            exactCluckAudioQualified=False,allVictimsEdgesAndCleanupQualified=False,
            kanoFriendshipImplemented=True,fullPortVerified=False,releaseReady=False)
paths=[run/'execution.json',run/'autoboot.lua',run/'friend.csv',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
       SRC/'KSFRIEND.ASM',SRC/'KSFRART.ASM',SRC/'KSCMD.ASM',SRC/'MOVES.ASM',SRC/'MKFRIEND.ASM',
       HERE/'generate_friendship_data.py',HERE/'generated_friendship/FRIEND_DATA.json',
       HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',Path(__file__)]
paths+=sorted((run/'snap').glob('*.png'))
if negative:
    paths += [eligibility_path,HERE/'finisher_eligibility.py']
    report['nativeIneligibleCommandObservedFrames']=command_frames
if morphed:
    report.update(selectedCharacter=6,activeCommandCharacter=18,morphLPPunchEligibilityRejected=True)
    paths.extend([run/'morph_finish.csv',HERE/'finisher_morph_identity.py',SRC/'MKST.ASM'])
report['pins']={str(p):sha(p) for p in paths}
report['pins'][str(HERE/'finisher_observation_end.py')]=sha(HERE/'finisher_observation_end.py')
report['pins'][str(HERE/'verify_finisher_roms.py')]=sha(HERE/'verify_finisher_roms.py')
report['currentFull26ROMBytesVerified']=True
(run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
