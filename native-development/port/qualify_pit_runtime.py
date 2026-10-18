"""Finite physical versus progression into the native Pit II cinematic."""
import csv
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from qualify_bubble import BASE,HERE,SRC,sha
from verify_finisher_roms import verify

run=BASE/sys.argv[1];actor=int(sys.argv[2]);victim=18 if actor==17 else 17
execution=json.loads((run/'execution.json').read_text());args=execution['testArguments']
assert all(flag in args for flag in ['--stage','--stage-rematch','--own-victim','--pit-progress'])
assert ('--sonya' in args)==(actor==18)
side=2 if '--mirror' in args else 1;other=3-side
fall_delay=148 if side==1 else 147
duration=fall_delay+58
assert execution['exitCode']==0 and not execution['timedOut']
assert not execution['customDriver'] and not execution['gameMemoryWrites']
assert execution['controllerSHA256']==sha(run/'autoboot.lua')
observer=(run/'autoboot.lua').read_text()
assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert '[LUA ERROR]' not in (run/'mame.log').read_text()
assert not (run/'stage_fault.txt').exists()
with zipfile.ZipFile(run/'roms/mk3.zip') as z:
    lanes=[z.read(f'mk321u{chip}.bin') for chip in [54,63]]
    verify(z,execution)
rom=bytearray(1048576);rom[::2]=lanes[0];rom[1::2]=lanes[1]
def read(address):return struct.unpack_from('<I',rom,(address-0xff800000)//8)[0]
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
rows=list(csv.DictReader((run/'stage.csv').open()))
assert all(r['missing']=='0' for r in rows)
environment={r['frame']:r for r in csv.DictReader((run/'stage_environment.csv').open())}
fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==str(actor) and r[f'p{other}char']==str(victim)]
if '--pit-rejoin' in args:
    launch_frame=next(int(r['frame']) for r in fight if environment[r['frame']]['background']=='6' and r['death']=='6')
    fight=[r for r in fight if int(r['frame'])<=launch_frame+duration+240]
assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in fight)
visits=[]
for r in fight:
    background=int(environment[r['frame']]['background'])
    if not visits or visits[-1]!=background:visits.append(background)
assert visits==list(range(7)),visits
ko=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0']
assert len(ko)==14
launch=[r for r in fight if environment[r['frame']]['background']=='6' and r['death']=='6']
assert launch and launch[0]['winner']=='3' and launch[0][f'p{other}hp']=='0'
first=int(launch[0]['frame'])
objects=list(csv.DictReader((run/'pit_objects.csv').open()))
if '--pit-rejoin' in args:
    # Preserve this verifier's original cinematic +240-field observation scope.
    # The separate cleanup verifier checks the subsequent match, not this slice.
    objects=objects[:299]
assert objects and len({r['object'] for r in objects})==1
assert all(r['character']==str(victim) and r['x']=='192' and r['y']=='64' for r in objects)
name='kano' if victim==17 else 'sonya';sequence=symbols[f'ks_pit_{name}_sequence']
loop=[read(sequence+i*32) for i in range(5)];impact=read(sequence+8*32)
fall=[r for r in objects if r['death']=='6'];done=[r for r in objects if r['death']=='65535']
assert len(fall)==58 and len(done)==241
assert int(fall[0]['frame'])==first+fall_delay
assert [int(r['ground']) for r in fall]==list(range(1,59))
assert [int(r['shape'],16) for r in fall]==[loop[(i//3)%5] for i in range(58)]
assert all(int(r['shape'],16)==impact and r['ground']=='59' for r in done)
assert int(done[0]['frame'])==first+duration
assert [int(r['frame']) for r in objects]==list(range(first+fall_delay,first+fall_delay+299))
assert int(objects[-1]['frame'])==int(done[0]['frame'])+240
captures=sorted((run/'snap').glob('pit_*.png'))
assert captures and any(int(p.stem.split('_')[-1])>=int(done[0]['frame']) for p in captures)
report=dict(scope='physical seven-versus-match progression, native Pit fall/impact of the other added actor',
            actorID=actor,physicalActorSide=side,victimID=victim,observedThroughFrame=int(objects[-1]['frame']),
            naturalRoundKnockouts=14,backgroundVisits=visits,nativePitActionFields=duration,
            nativeLaunchToFallFields=fall_delay,
            ownFallFields=58,ownImpactObservedFields=241,nativeCompletionObserved=True,
            allFiveOwnFallPosesAndImpactObserved=True,missingRootMarkers=0,
            currentFull26ROMBytesVerified=True,
            exactVisualStyleAndAudioQualified=False,mirrorAndSubsequentMatchCleanupQualified=False,
            fullSinglePlayerCampaignQualified=False,fullPortVerified=False,releaseReady=False)
paths=[run/'execution.json',run/'autoboot.lua',run/'stage.csv',run/'stage_environment.csv',run/'stage_inputs.csv',
       run/'pit_objects.csv',SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'MKFALL.ASM',SRC/'KSPITART.ASM',
       SRC/'KSCMD.ASM',SRC/'MOVES.ASM',HERE/'generated_pit/PIT_DATA.json',HERE/'PIT_SOURCE_ROUNDTRIP.json',
       BASE/'test_wolf_baseline.py',HERE/'verify_finisher_roms.py',Path(__file__)]+captures
report['pins']={str(p):sha(p) for p in paths}
(run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
