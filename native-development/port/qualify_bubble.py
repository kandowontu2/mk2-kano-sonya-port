"""Finite native Death Orb activation, timing and explicit lifetime checks."""
import csv
from finisher_observation_end import verify_end
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
from current_graphics import verify_archive_sockets

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def qualify(name,side,victim,negative=False):
    run=BASE/name
    execution=json.loads((run/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    assert execution['controllerSHA256']==sha(run/'autoboot.lua')
    assert side==(2 if '--mirror' in execution['testArguments'] else 1),'Performer side disagrees with the physical controller profile'
    observer=(run/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert ('--bad-hold' in execution['testArguments'])==negative
    with zipfile.ZipFile(run/'roms/mk3.zip') as roms:
        lo=roms.read('mk321u54.bin');hi=roms.read('mk321u63.bin')
        for lane,raw in enumerate([lo,hi]):
            assert raw==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
        verify_archive_sockets(roms)
        sound='soundp' if '--sound-candidate' in execution['testArguments'] else 'soundw'
        for chip in range(2,6):
            assert roms.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(SRC.parent/sound/f'U{chip}.ROM').read_bytes()
        with zipfile.ZipFile(HERE.parents[1]/'roms/mk2.zip') as original:
            for bank,(first,second) in enumerate(((14,19),(16,20),(17,22))):
                for lane,(letter,socket) in enumerate((('ug',first),('uj',first),('ug',second),('uj',second))):
                    assert roms.read(f'l1_mortal_kombat_3_u{133-bank*4-lane}_game_rom.u{133-bank*4-lane}')==original.read(f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}')
    rom=bytearray(1048576);rom[::2]=lo;rom[1::2]=hi
    def read(address):return struct.unpack_from('<I',rom,(address-0xff800000)//8)[0]
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    rows=list(csv.DictReader((run/'bubble.csv').open()))
    verify_end(run,execution,int(rows[-1]['frame']))
    assert all(r['missing']=='0' for r in rows)
    assert not (run/'bubble_fault.txt').exists()
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    other=3-side
    morphed='--finisher-morph' in execution['testArguments']
    fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==('6' if morphed else '18') and r[f'p{other}char']==str(victim)]
    assert fight, 'No requested matchup observed'
    first,last=int(fight[0]['frame']),int(fight[-1]['frame'])
    assert all(r[f'p{side}char']==('6' if morphed else '18') and r[f'p{other}char']==str(victim)
               for r in rows if r['mode']=='2' and first<=int(r['frame'])<=last), 'Identity changed within tested matchup'
    knockouts=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0']
    assert len(knockouts)>=2
    running=[r for r in fight if r[f'p{side}action']=='544' and r['death']=='2']
    if morphed:
        from finisher_morph_identity import verify as verify_morph
        verify_morph(run,running,18)
    report=dict(scope='finite native Death Orb with physical round wins and linked-list lifetime observations',
                currentFull26ROMBytesVerified=True,
                side=side,victimID=victim,negativeBrokenBlockHold=negative,frames=int(rows[-1]['frame']),
                naturalKnockoutsBeforeFinish=len(knockouts),missingRootMarkers=0,
                allVictimsEdgesAndAIQualified=False,exactNativeAudioQualified=False,
                freshMatchCleanupQualified=False,eyeLaserCoveredByThisTest=False,fullMoveSetVerified=False,releaseReady=False)
    if negative:
        assert not running and not any(r['death']=='2' for r in fight)
        window=[r for r in fight if r['winner']=='3']
        assert len(window)>=150 and len({r[f'p{side}y'] for r in window})==1
        report.update(brokenContinuousHoldRejected=True,performerStayedGrounded=True,
                      finishWindowObserved=len(window),nativeCompletionObserved=False)
    else:
        assert running
        first=int(running[0]['frame']);length=len(running);travel=length-137
        assert 1<=travel<=256 and all(int(r['frame'])==first+i for i,r in enumerate(running))
        completed=[r for r in fight if r[f'p{side}action']=='544' and r['death']=='65535']
        assert completed and int(completed[0]['frame'])==first+length
        assert all(r['winner']=='3' and r[f'p{other}hp']=='0' for r in running)
        assert abs(int(running[0]['p1x'])-int(running[0]['p2x']))>=160
        data=json.loads((HERE/'generated_bubble/BUBBLE_DATA.json').read_text())
        def poses(key):return [symbols[f'ks_sonya_pose_{int(g,16):08x}'] for g in data[key]]
        intro,loop,burst=poses('intro'),poses('loop'),poses('burst')
        contact=54+travel;retire=contact+51
        child=running[33:retire]
        assert len({r['child'] for r in child})==1 and child[0]['child']!='00000000'
        assert all(r['child']=='00000000' for r in running[:33]+running[retire:]+completed)
        expected=[g for g in intro for _ in range(3)]
        expected += [loop[(i//3)%4] for i in range(travel)]
        expected += [loop[(i//3)%4] for i in range(39)]
        expected += [g for g in burst for _ in range(4)]
        assert [int(r['childshape'],16) for r in child]==expected
        travel_rows=running[54:contact]
        direction=-1 if int(travel_rows[0]['childflags'])&16 else 1
        x0=int(travel_rows[0]['childxval'],16)
        assert [int(r['childxval'],16) for r in travel_rows]==[x0+direction*131072*i for i in range(travel)]
        victim_x=int(travel_rows[-1][f'p{other}x'])
        assert abs((x0>>16)+direction*2*travel-victim_x)<=177
        assert abs((x0>>16)+direction*2*(travel-1)-victim_x)>177
        enclosure=running[contact:contact+39]
        assert len({(r['childxval'],r['childyval']) for r in enclosure})==1
        assert all(r['childy']==r[f'p{other}y'] for r in enclosure)
        assert all(r[f'p{other}action']=='545' for r in enclosure[1:])
        assert any(r[f'p{other}action']=='546' for r in running[contact+39:])
        performer=[read(symbols['ks_finish_sonya_kiss']+i*32) for i in range(11)]
        salute=[read(symbols['ks_kiss_outro']+i*32) for i in range(8)]
        expected_body=[g for g in performer for _ in range(3)]+[performer[-1]]*(retire-33)
        expected_body += [g for g in salute for _ in range(4)]
        assert [int(r[f'p{side}shape'],16) for r in running]==expected_body
        root=symbols['ks_kano_anitab1' if victim==17 else 'lk_anitab1']
        address=read(root+0x23*32);stumble=[]
        for i in range(64):
            value=read(address+i*32)
            if value==0:break
            if value>=0xff800000:stumble.append(value)
        else:raise AssertionError('Unbounded native stumble script')
        observed={int(r[f'p{other}shape'],16) for r in enclosure if r[f'p{other}action']=='545'}
        assert observed==set(stumble)
        life=list(csv.DictReader((run/'bubble_lifetime.csv').open()))
        by_frame={int(r['frame']):r for r in life}
        assert all(by_frame[first+i]['childActive']=='1' and by_frame[first+i]['processActive']=='1' for i in range(33,retire))
        assert all(by_frame[first+i]['childActive']=='0' and by_frame[first+i]['processActive']=='0' for i in range(retire,length))
        report.update(nativeActionFields=length,travelFields=travel,travelPixelsPerField=2,
                      nativeContactThreshold=177,growthFields=21,enclosureFields=39,burstFields=12,
                      saluteFields=32,allFourteenOwnBubblePosesObserved=True,
                      actualVictimNativeStumbleObserved=True,bubbleObjectAndDummyProcessRetired=True,
                      nativeCompletionObserved=True)
    paths=[run/'execution.json',run/'bubble.csv',run/'bubble_lifetime.csv',run/'autoboot.lua',
           SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'KSBUBBLE.ASM',SRC/'KSBUANI.ASM',SRC/'KSCMD.ASM',
           SRC/'MKUTIL.ASM',SRC/'MKDIE.ASM',SRC/'MKDEATH.ASM',SRC/'MOVES.ASM',
           HERE/'generate_bubble_data.py',HERE/'generated_bubble/BUBBLE_DATA.json',
           HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',Path(__file__)]
    paths+=sorted((run/'snap').glob('*.png'))
    paths.append(HERE/'finisher_observation_end.py')
    if morphed:
        report.update(selectedCharacter=6,activeFinisherCharacter=18,transformedFinisher=True)
        paths.extend([run/'morph_finish.csv',HERE/'finisher_morph_identity.py',SRC/'MKST.ASM'])
    report['pins']={str(p):sha(p) for p in paths}
    (run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    name,side,victim=sys.argv[1:4]
    print(json.dumps(qualify(name,int(side),int(victim),'--negative' in sys.argv),indent=2))
