"""Finite stock-MAME Eye Laser checks; not full-port acceptance."""
import csv
from finisher_observation_end import verify_end
import json
from pathlib import Path
import re
import sys
import zipfile
from qualify_bubble import BASE, HERE, SRC, sha
from current_graphics import verify_archive_sockets

def qualify(name, side, victim, negative=False):
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
    assert ('--held-block' in execution['testArguments'])==negative
    with zipfile.ZipFile(run/'roms/mk3.zip') as roms:
        for lane, chip in enumerate([54,63]):
            assert roms.read(f'mk321u{chip}.bin')==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
        verify_archive_sockets(roms)
        sound='soundp' if '--sound-candidate' in execution['testArguments'] else 'soundw'
        for chip in range(2,6):
            assert roms.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==(SRC.parent/sound/f'U{chip}.ROM').read_bytes()
        root=HERE.parents[1]
        with zipfile.ZipFile(root/'roms/mk2.zip') as original:
            for bank,(first,second) in enumerate(((14,19),(16,20),(17,22))):
                for lane,(letter,socket) in enumerate((('ug',first),('uj',first),('ug',second),('uj',second))):
                    assert roms.read(f'l1_mortal_kombat_3_u{133-bank*4-lane}_game_rom.u{133-bank*4-lane}')==original.read(f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}')
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    rows=list(csv.DictReader((run/'laser.csv').open()))
    verify_end(run,execution,int(rows[-1]['frame']))
    assert all(r['missing']=='0' for r in rows)
    assert not (run/'laser_fault.txt').exists()
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    other=3-side
    morphed='--finisher-morph' in execution['testArguments']
    fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==('6' if morphed else '17') and r[f'p{other}char']==str(victim)]
    assert fight, 'No requested matchup observed'
    # After the two-player defeat the winner can enter the ordinary CPU ladder.
    # Do not mistake that legitimate new matchup for identity substitution.
    first,last=int(fight[0]['frame']),int(fight[-1]['frame'])
    assert all(r[f'p{side}char']==('6' if morphed else '17') and r[f'p{other}char']==str(victim)
               for r in rows if r['mode']=='2' and first<=int(r['frame'])<=last), 'Identity changed within tested matchup'
    knockouts=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0']
    assert len(knockouts)>=2
    running=[r for r in fight if r[f'p{side}action']=='547' and r['death']=='2']
    if morphed:
        from finisher_morph_identity import verify as verify_morph
        verify_morph(run,running,17)
    report=dict(scope='finite physical-input Eye Laser timing and child retirement', side=side,
                victimID=victim,frames=int(rows[-1]['frame']),naturalKnockouts=len(knockouts),heldBlockNegative=negative,
                allVictimsEdgesAndAIQualified=False,exactNativeAudioQualified=False,
                freshMatchCleanupQualified=False,fullMoveSetVerified=False,releaseReady=False,
                currentFull26ROMBytesVerified=True)
    if negative:
        assert not running and not any(r['death']=='2' for r in fight)
        report['heldBlockAtFinalHKRejected']=True
    else:
        data=json.loads((HERE/'generated_laser/LASER_DATA.json').read_text())
        assert len(running)==data['totalFields']==176
        first=int(running[0]['frame'])
        assert [int(r['frame']) for r in running]==list(range(first,first+176))
        body=beam=0; expected=[]; exists=False
        for phase,repeat in [(0,1),(1,data['sustainRepeats']),(2,1)]:
            events=data['phases'][phase]
            delay=data['phaseFields'][phase]//len(events)
            for _ in range(repeat):
                for event in events:
                    if event['body']:body=symbols[event['body']]
                    if event['beam']:beam=symbols[event['beam']]
                    exists|=event['create']
                    expected.extend([(body,beam if exists else 0)]*delay)
        assert [(int(r[f'p{side}shape'],16),int(r['childshape'],16)) for r in running]==expected
        assert all(r['child']=='00000000' for r in running[:12])
        assert len({r['child'] for r in running[12:]})==1 and running[12]['child']!='00000000'
        assert all(r['childx']==r[f'p{side}x'] and r['childy']==r[f'p{side}y'] for r in running[12:])
        wake=48+(side==1)
        base=int(running[0][f'p{other}y'])
        for j,r in enumerate(running[wake:wake+96]):
            assert r[f'p{other}action']=='548'
            assert int(r[f'p{other}shape'],16)==symbols[data['victims'][str(victim)]]
            assert abs(int(r[f'p{other}x'])-int(r[f'p{side}x']))==184
            assert int(r[f'p{other}y'])==base+((3 if j<30 else 5) if j%6<3 else 0)
        assert all(r[f'p{other}action']=='549' for r in running[wake+96:])
        completed=[r for r in fight if r[f'p{side}action']==('1028' if morphed else '547') and r['death']=='65535']
        assert completed and int(completed[0]['frame'])==first+176
        life={int(r['frame']):r for r in csv.DictReader((run/'laser_lifetime.csv').open())}
        assert all(life[first+i]['childActive']=='1' and life[first+i]['processActive']=='1' for i in range(12,176))
        assert life[first+176]['childActive']=='0' and life[first+176]['processActive']=='0'
        report.update(nativeActionFields=176,beamFields=164,victimReactionFields=96,
                      allBodyAndBeamEventsObserved=True,ownVictimPoseObserved=True,
                      beamObjectAndDummyProcessRetired=True,nativeCompletionObserved=True)
    paths=[run/'execution.json',run/'laser.csv',run/'laser_lifetime.csv',run/'autoboot.lua',
           SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'KSLASER.ASM',SRC/'KSLAANI.ASM',SRC/'KSCMD.ASM',
           SRC/'KSPAIR.ASM',SRC/'MKUTIL.ASM',SRC/'MOVES.ASM',SRC/'MKDEATH.ASM',
           HERE/'generate_laser_data.py',HERE/'generated_laser/LASER_DATA.json',
           HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',Path(__file__)]
    paths.append(HERE/'finisher_observation_end.py')
    if morphed:
        report.update(selectedCharacter=6,activeFinisherCharacter=17,transformedFinisher=True)
        paths.extend([run/'morph_finish.csv',HERE/'finisher_morph_identity.py',SRC/'MKST.ASM'])
    report['pins']={str(p):sha(p) for p in paths}
    (run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    print(json.dumps(qualify(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),'--negative' in sys.argv),indent=2))
