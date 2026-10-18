"""Finite natural Dead Pool chord/uppercut, own victim art and native completion."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom
from deadpool_source import OLD,NEW,integrate,WAIT_OLD,WAIT_NEW,integrate_wait

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
current=(BUILD/'MOVES.ASM').read_text()
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as original_zip:
    original=original_zip.read('mk2-rebuild-main/src/MOVES.ASM').decode('cp437').replace('\r\n','\n')
    original_background=original_zip.read('mk2-rebuild-main/src/BGND.ASM').decode('cp437').replace('\r\n','\n')
assert integrate(original).count(NEW)==1 and current.count(NEW)==1
background=(BUILD/'BGND.ASM').read_text()
assert integrate_wait(original_background).rstrip('\r\n')==background.rstrip('\r\n')
def gate(text):
    start=text.index('\tmove\t@curback,a0,w',text.index('\ndo_uppercut\n'))
    end=text.index('\nucut2 ',start)
    return text[start:end]
assert gate(current.replace(NEW,OLD))==gate(original)
for bits in range(16):
    pressed=((bits&3)<<16)|((bits>>2)<<20)
    for side in (1,2):
        observed=(pressed>>16>>(4 if side==2 else 0))&3
        assert observed==((bits>>(2 if side==2 else 0))&3)
for name in sys.argv[1:]:
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    args=receipt['testArguments']
    assert '--stage' in args and '--deadpool' in args
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert receipt['controllerSHA256']==sha((folder/'autoboot.lua').read_bytes())
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        verify_full_rom(archive,receipt)
        lanes=[archive.read(chip) for chip in ('mk321u54.bin','mk321u63.bin')]
        for lane in (0,1): assert lanes[lane]==b''.join((BUILD/f'rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        verify_archive_sockets(archive)
    program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
    # Actual linked uppercut must read Wolf's main port then shift16, not DIP/switch2.
    start=(symbols['do_uppercut']-0xff800000)//8
    native=program[start:start+512]
    assert struct.pack('<HIHH',0x07a3,0x0187ff80,0x03e3,0x2e03) in native
    actor=18 if '--sonya' in args else 17
    victim=(17 if actor==18 else 18) if '--own-victim' in args else 1
    mirror='--mirror' in args
    performer,other=('p2','p1') if mirror else ('p1','p2')
    main=list(csv.DictReader((folder/'stage.csv').open()))
    fight=[r for r in main if r['mode']=='2' and int(r[performer+'char'])==actor and int(r[other+'char'])==victim]
    assert fight and all(r['missing']=='0' for r in main)
    ko=[r for prev,r in zip(fight,fight[1:]) if int(prev[other+'hp'])>0 and r[other+'hp']=='0']
    assert len(ko)>=2
    environment={r['frame']:int(r['background']) for r in csv.DictReader((folder/'stage_environment.csv').open())}
    rows=list(csv.DictReader((folder/'deadpool_victim.csv').open()))
    assert rows and all(int(r['character'])==victim and environment[r['frame']]==0 for r in rows)
    assert not (folder/'stage_fault.txt').exists() and '[LUA ERROR]' not in (folder/'mame.log').read_text()
    assert any(r[performer+'action']=='263' for r in fight)
    negative='--deadpool-no-chord' in args
    falling=[r for r in rows if int(r['action'])==0x50a]
    if negative:
        # An earlier combat uppercut is not evidence that the final command
        # was actually delivered while stage-fatality eligibility was active.
        finish_uppercuts=[r for r in fight if r[performer+'action']=='263' and
                         r['winner']=='3' and r[other+'hp']=='0' and
                         int(r[performer+'hp'])>0 and environment[r['frame']]==0]
        assert finish_uppercuts, 'No native uppercut in the Finish Him window'
        uppercut_frame=int(finish_uppercuts[0]['frame'])
        contact=[r for r in rows if uppercut_frame<=int(r['frame'])<=uppercut_frame+12
                 and r['action']=='1283']
        assert contact, 'Uppercut did not produce the native victim hit reaction'
        ordinary_result=[r for r in main if r['mode']=='5' and
                         uppercut_frame<int(r['frame'])<=uppercut_frame+80 and
                         r[performer+'char']==str(actor) and r[other+'char']==str(victim) and
                         r['winner']==('2' if mirror else '1') and
                         r[other+'hp']=='0' and int(r[performer+'hp'])>0]
        assert ordinary_result, 'No ordinary round result after the rejected stage fatality'
        assert all(r['heldChord']=='0' for r in rows) and not falling
        assert not any(r['death']=='65535' for r in rows)
    else:
        assert falling and all(r['heldChord']=='3' for r in falling)
        assert any(r['death']=='65535' for r in rows)
        assert any(r['masterCountdown']=='256' and r['thatsAll']=='0' for r in falling)
        visible=[r for r in falling if not int(r['flags'])&0x20]
        hidden=[r for r in falling if int(r['flags'])&0x20]
        assert len(visible)>20 and len(hidden)>50
        assert max(int(r['y']) for r in visible)-min(int(r['y']) for r in visible)>60
        if victim in (17,18):
            own={v for k,v in symbols.items() if k.startswith('ks_'+('kano' if victim==17 else 'sonya')+'_pose_')}
            own|={symbols[f'ks_{"kano" if victim==17 else "sonya"}_banged']}
            assert all(int(r['shape'],16) in own for r in visible)
    report=dict(scope='One physical Dead Pool uppercut',actor=actor,victim=victim,
        performerPlayer=2 if mirror else 1,naturalKnockouts=len(ko),
        nativeWolfInputReadVerified=True,otherNativeStageGatesPreserved=True,
        nativeSkeletonDeclaresCompletion=not negative,finiteMasterWait=256,
        chordNegativeRejected=negative,nativeSlimeFallObserved=bool(falling),
        nativeCompletionObserved=not negative,ownVisibleVictimArtVerified=victim in (17,18) and not negative,
        missingMarkers=0,fullVisualAcceptance=False,fullPortVerified=False)
    report['currentFull26ROMBytesVerified']=True
    if negative:
        report['finishWindowUppercutFrames']=[int(r['frame']) for r in finish_uppercuts]
        report['nativeVictimHitReactionObserved']=True
        report['ordinaryRoundResultObserved']=True
    paths=[folder/'execution.json',folder/'autoboot.lua',folder/'stage.csv',
           folder/'stage_environment.csv',folder/'deadpool_victim.csv',
           BUILD/'MK2P.MAP',BUILD/'MOVES.ASM',BUILD/'BGND.ASM',
           PORT/'verify_finisher_roms.py',PORT/'deadpool_source.py',Path(__file__)]
    paths+=sorted((folder/'snap').glob('*.png'))
    report['pins']={str(path):sha(path.read_bytes()) for path in paths}
    (folder/'DEADPOOL_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
