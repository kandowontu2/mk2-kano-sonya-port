"""Finite natural rematch into Kombat Tomb, native uppercut/spike completion."""
import csv
import json
from pathlib import Path
import re
import sys
import zipfile
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom
from qualify_bubble import BASE,HERE,SRC,sha
from stage_sides import performer_first,signed_word,tomb_command

run=BASE/sys.argv[1];actor=int(sys.argv[2])
execution=json.loads((run/'execution.json').read_text());args=execution['testArguments']
assert '--stage-rematch' in args and '--stage' in args
assert ('--sonya' in args)==(actor==18)
mirror='--mirror' in args
victim=(17 if actor==18 else 18) if '--own-victim' in args else 1
assert execution['exitCode']==0 and not execution['timedOut']
assert not execution['customDriver'] and not execution['gameMemoryWrites']
assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert execution['controllerSHA256']==sha(run/'autoboot.lua')
observer=(run/'autoboot.lua').read_text()
assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
assert '[LUA ERROR]' not in (run/'mame.log').read_text()
assert not (run/'stage_fault.txt').exists()
with zipfile.ZipFile(run/'roms/mk3.zip') as z:
    verify_full_rom(z,execution)
    for lane,chip in enumerate([54,63]):
        assert z.read(f'mk321u{chip}.bin')==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
    verify_archive_sockets(z)
rows=list(csv.DictReader((run/'stage.csv').open()))
rows=performer_first(rows,mirror)
assert int(rows[-1]['frame'])==18000
assert all(r['missing']=='0' for r in rows)
environment={r['frame']:int(r['background']) for r in csv.DictReader((run/'stage_environment.csv').open())}
fight=[r for r in rows if r['mode']=='2' and r['p1char']==str(actor) and r['p2char']==str(victim)]
ko=[r for prev,r in zip(fight,fight[1:]) if int(prev['p2hp'])>0 and r['p2hp']=='0']
assert len(ko)>=4
assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in fight)
deadpool=[r for r in fight if environment[r['frame']]==0]
assert deadpool and not any(r['death'] in ('6','8') for r in deadpool)
tomb=[r for r in fight if environment[r['frame']]==1]
running=[r for r in tomb if r['death']=='8']
assert len(running)==64
first=int(running[0]['frame'])
assert [int(r['frame']) for r in running]==list(range(first,first+64))
assert all(r['winner']=='3' and r['p1hp']!='0' and r['p2hp']=='0' for r in running)
assert abs(signed_word(running[0]['p1x'])-signed_word(running[0]['p2x']))<=72
completed=[r for r in tomb if r['death']=='65535' and int(r['frame'])>=first]
assert completed and int(completed[0]['frame'])==first+64
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
own={v for k,v in symbols.items() if k.startswith('ks_'+('kano' if actor==17 else 'sonya')+'_pose_')}
assert all(int(r['p1shape'],16) in own for r in running)
def signed_y(row):
    value=int(row['p2y'])
    return value-65536 if value>=32768 else value
assert min(signed_y(r) for r in running)<0
if victim in (17,18):
    own_victim={v for k,v in symbols.items() if k.startswith('ks_'+('kano' if victim==17 else 'sonya')+'_pose_')}
    assert all(int(r['p2shape'],16) in own_victim for r in running)
    flat='ks_kano_pose_ff8299e0' if victim==17 else 'ks_sonya_pose_ff837100'
    assert int(running[-1]['p2shape'],16)==symbols[flat]
inputs=list(csv.DictReader((run/'stage_inputs.csv').open()))
expected=tomb_command(actor,running[0]['p1x'],running[0]['p2x'])
near=[r for r in inputs if first-4<=int(r['frame'])<=first+4]
assert any([int(r[f'q{i}'],16)>>16 for i in range(3)]==expected for r in near)
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
    original=z.read('mk2-rebuild-main/src/MOVES.ASM').decode('cp437').replace('\r\n','\n')
current=(SRC/'MOVES.ASM').read_text()
def native_gate(text):return re.search(r'^check_dtp\n(.*?)^fatality_xfer_close\n',text,re.M|re.S).group(1)
assert native_gate(original)==native_gate(current)
report=dict(scope='Physical commands after native versus rematch, own performer and selected spike victim',
            actorID=actor,physicalActorSide=2 if mirror else 1,victimID=victim,frames=18000,naturalKnockouts=len(ko),nativeSpikeFields=64,
            nativeCompletionObserved=True,ownPerformerPosesObserved=True,originalStageGatePreserved=True,
            initialDeadPoolStageCommandRejected=True,ownVictimPosesObserved=victim in (17,18),pitAndMirrorQualified=False,
            exactStageAudioAndFreshMatchCleanupQualified=False,fullPortVerified=False,releaseReady=False)
paths=[run/'execution.json',run/'autoboot.lua',run/'stage.csv',run/'stage_environment.csv',run/'stage_inputs.csv',
       SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'KSCMD.ASM',SRC/'MOVES.ASM',SRC/'MKDEATH.ASM',
       HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',Path(__file__)]
paths+=sorted((run/'snap').glob('*.png'))
paths.append(HERE/'verify_finisher_roms.py')
paths.append(HERE/'stage_sides.py')
report['currentFull26ROMBytesVerified']=True
report['pins']={str(p):sha(p) for p in paths}
(run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
