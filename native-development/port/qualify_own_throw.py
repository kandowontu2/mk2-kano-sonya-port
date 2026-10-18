"""Finite physical ordinary-throw proof, not broad victim/edge acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import struct
import zipfile
from verify_finisher_roms import verify as verify_full_rom

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
art=json.loads((PORT/'generated_throw/THROW_DATA.json').read_text())['actors']
names=sys.argv[1:]
assert names and len(names)==len(set(names)),'Supply distinct completed throw fixtures'
for argument in names:
    assert argument and Path(argument).name==argument and '/' not in argument and '\\' not in argument
    folder=BASE/argument
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--own-throw' in receipt['testArguments']
    observer=(folder/'autoboot.lua').read_bytes()
    assert hashlib.sha256(observer).hexdigest().upper()==receipt['controllerSHA256']
    assert b':write_u' not in observer and not re.search(rb'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify_full_rom(archive,receipt)
    program=bytearray(0x100000)
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        data=b''.join((BUILD/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        assert hashlib.sha256(data).hexdigest().upper()==receipt['replacementChips'][chip]
        program[lane::2]=data
    rows=list(csv.DictReader((folder/'throw.csv').open()))
    assert len(rows)==9000 and all(int(r['missing'])==0 for r in rows)
    combat=[r for r in rows if r['mode']=='2' and int(r['fight'])>0]
    assert all(int(r['pc'],16)>=0xff800000 and int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in combat)
    actor='sonya' if '--sonya' in receipt['testArguments'] else 'kano'
    identity=18 if actor=='sonya' else 17
    rootOffset=(symbols[f'ks_{actor}_anitab1']-0xff800000)//8+36*4
    assert struct.unpack_from('<I',program,rootOffset)[0]==symbols[f'ks_{actor}_throw_phase0']
    victim=1 if '--stock-victim' in receipt['testArguments'] else (17 if identity==18 else 18)
    victimOption=next((arg for arg in receipt['testArguments'] if arg.startswith('--throw-victim=')),None)
    if victimOption:victim=int(victimOption.split('=',1)[1])
    assert all(int(r['p1char'])==identity and int(r['p2char'])==victim for r in combat)
    held=[r for r in combat if int(r['action'])==0x507]
    assert held
    expected={symbols[p] for phase in art[actor]['bodyPhases'] for p in phase['poses']}
    observed={int(r['ownerShape'],16) for r in held}
    assert expected<=observed
    assert any(int(r['victimAction'])==0x226 for r in held)
    first=int(held[0]['fight']);last=int(held[-1]['fight'])
    window=[r for r in combat if first<=int(r['fight'])<=last+180]
    damage=int(held[0]['victimHP'])-min(int(r['victimHP']) for r in window)
    assert damage==34,damage
    assert any(int(r['fight'])>last+180 and int(r['action'])!=0x507 and int(r['victimAction'])!=0x226 for r in combat)
    grounded=None
    if 'ownerGround' in combat[0]:
        settled=[r for r in combat if last+180<=int(r['fight'])<=last+400]
        assert len(settled)>=200
        assert all(r['ownerY']==r['ownerGround'] and r['victimY']==r['victimGround'] for r in settled)
        assert all(r['action']==r['victimAction']=='771' for r in settled)
        grounded=len(settled)
    edgeProof=None
    if '--throw-front-edge' in receipt['testArguments']:
        setup=json.loads((folder/'throw_edge_setup.json').read_text())
        assert setup['stationaryFieldsWhileAwayHeld']>=30 and not setup['guestWrites']
        assert first>setup['fight'] and held[0]['edgeReady']=='1'
        settled=[r for r in combat if last+180<=int(r['fight'])<=last+400]
        assert len(settled)>=200
        assert all(r['ownerY']==r['ownerGround'] and r['victimY']==r['victimGround'] for r in settled)
        right=setup['ownerX']<setup['victimX']
        assert all((int(r['p2x'])<=setup['victimX'] if right else int(r['p2x'])>=setup['victimX']) for r in settled)
        edgeProof={'physicalSetup':setup,'settledGroundedObservations':len(settled),'releasedWithinObservedFrontBoundary':True}
    result={'qualified':True,'scope':'One physical ordinary throw; damage, own poses and recovery only','victimID':victim,
            'actor':actor,'actorPlayer':2 if '--mirror' in receipt['testArguments'] else 1,
            'frames':len(rows),'ownerActionFields':len(held),'ownBodyPosesObserved':len(expected),
            'damage':damage,'missingMarkers':0,'allVictimsOrEdgesVerified':False,'fullPortVerified':False}
    if edgeProof:result['frontEdgeProof']=edgeProof
    if grounded:result['settledGroundedObservations']=grounded
    result['currentFull26ROMBytesVerified']=True
    evidence=[Path(__file__),PORT/'verify_finisher_roms.py',PORT/'generated_throw/THROW_DATA.json',BUILD/'MK2P.MAP',BUILD/'KSTHROW.ASM']
    evidence.extend(folder/item for item in ('execution.json','autoboot.lua','throw.csv','mame.log'))
    evidence.extend((folder/'snap').glob('throw_age*.png'))
    if edgeProof:evidence.append(folder/'throw_edge_setup.json')
    result['pins']={str(path):hashlib.sha256(path.read_bytes()).hexdigest().upper() for path in evidence}
    (folder/'throw_qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
