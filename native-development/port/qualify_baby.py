"""Finite native babality command/completion evidence; victim render not certified."""
import csv
from finisher_observation_end import verify_end
import json
import re
from pathlib import Path
import sys
import zipfile
from qualify_bubble import BASE,HERE,SRC,sha
from current_graphics import verify_archive_sockets
from verify_finisher_roms import verify as verify_full_rom

run=BASE/sys.argv[1]
actor=int(sys.argv[2])
execution=json.loads((run/'execution.json').read_text())
side=2 if '--mirror' in execution['testArguments'] else 1
other=3-side
victim=(17 if actor==18 else 18) if '--own-victim' in execution['testArguments'] else 1
morphed='--finisher-morph' in execution['testArguments']
negative='--punch-wins' in execution['testArguments'] or (morphed and actor==18)
assert execution['exitCode']==0 and not execution['timedOut']
assert not execution['customDriver'] and not execution['gameMemoryWrites']
assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert execution['controllerSHA256']==sha(run/'autoboot.lua')
observer=(run/'autoboot.lua').read_text()
assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
assert '[LUA ERROR]' not in (run/'mame.log').read_text()
assert not (run/'baby_fault.txt').exists()
assert '--baby' in execution['testArguments']
assert ('--sonya' in execution['testArguments'])==(actor==18)
with zipfile.ZipFile(run/'roms/mk3.zip') as roms:
    verify_full_rom(roms,execution)
    for lane,chip in enumerate([54,63]):
        assert roms.read(f'mk321u{chip}.bin')==b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
    verify_archive_sockets(roms)
rows=list(csv.DictReader((run/'baby.csv').open()))
verify_end(run,execution,int(rows[-1]['frame']))
assert all(r['missing']=='0' for r in rows)
fight=[r for r in rows if r['mode']=='2' and r[f'p{side}char']==('6' if morphed else str(actor)) and r[f'p{other}char']==str(victim)]
knockouts=[r for prev,r in zip(fight,fight[1:]) if int(prev[f'p{other}hp'])>0 and r[f'p{other}hp']=='0']
assert len(knockouts)>=2
running=[r for r in fight if r['death']=='5']
completed=[r for r in fight if r['death']=='65535' and r['death2']=='1']
if negative:
    from finisher_eligibility import verify_punch_rejection
    eligibility_path,command_frames=verify_punch_rejection(run,actor,'baby',{r['frame'] for r in fight if r['winner']=='3' and r['death']=='0'})
    if morphed:
        from finisher_morph_identity import verify as verify_morph
        verify_morph(run,[dict(frame=str(frame)) for frame in command_frames],actor)
        assert '--punch-wins' not in execution['testArguments']
        eligibility=list(csv.DictReader(eligibility_path.open()))
        command_set=set(command_frames)
        assert all(r['hpTimestamp']=='0' and int(r['lpTimestamp'])>0 for r in eligibility if int(r['frame']) in command_set)
        assert any(r['hpTimestamp']==r['lpTimestamp']=='0' and int(r['frame'])<command_frames[0] for r in eligibility)
    assert not running and not completed
    assert len([r for r in fight if r['winner']=='3'])>=150
else:
    if morphed:
        from finisher_morph_identity import verify as verify_morph
        from finisher_eligibility import verify_command
        eligibility_path,command_frames=verify_command(run,actor,'baby',{r['frame'] for r in fight if r['winner']=='3' and r['death'] in ('0','5')},False)
        verify_morph(run,[dict(frame=str(command_frames[0]))],actor)
        identities={r['frame']:r for r in csv.DictReader((run/'morph_finish.csv').open())}
        assert all(identities[r['frame']]['selected']==identities[r['frame']]['actual']=='6' for r in running)
        # Native Babality immediately enters victory_animation; Shang's
        # original victory path returns form before delayed_baby_start wakes.
        baby_source=(SRC/'MKBABY.ASM').read_text()
        canned=(SRC/'MKCANNED.ASM').read_text()
        assert 'jauc\tvictory_animation' in baby_source
        assert 'jsrp\tback_to_shang_form' in canned.split('\nst_victory\n',1)[1].split('\nlk_victory\n',1)[0]
    assert len(running)==192
    first=int(running[0]['frame'])
    assert [int(r['frame']) for r in running]==list(range(first,first+192))
    assert all(r['winner']=='3' and r[f'p{other}hp']=='0' for r in running)
    assert completed and int(completed[0]['frame'])==first+192
assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in fight)
own_art=False
if victim in (17,18) and not negative:
    objects=list(csv.DictReader((run/'baby_objects.csv').open()))
    assert len(objects)>100 and len({r['object'] for r in objects})==1
    width,height=(27,44) if victim==17 else (35,54)
    assert all(int(r['width'])==width and int(r['height'])==height and int(r['y'])+height==int(r['ground']) for r in objects)
    import re
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    image=symbols['ks_kano_baby' if victim==17 else 'ks_sonya_baby']
    assert all(int(r['image'],16)==image for r in objects)
    # Existing victim process wakes a field later when scheduled after the actor.
    assert int(objects[0]['frame'])==first+61+(side==1)
    own_art=True
report=dict(scope='finite physical natural round wins, command dispatch/completion or punch-ineligibility rejection',
            actorID=actor,physicalActorSide=side,victimID=victim,frames=int(rows[-1]['frame']),naturalKnockouts=len(knockouts),nativeActionFields=len(running),
            nativeCompletionObserved=not negative,punchEligibilityRejectionObserved=negative,
            missingRootMarkers=0,ownBabyVictimArtRuntimeVerified=own_art,
            mirrorInvalidEligibilityAndCleanupQualified=False,fullPortVerified=False,releaseReady=False)
paths=[run/'execution.json',run/'autoboot.lua',run/'baby.csv',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
       SRC/'MKBABY.ASM',SRC/'KSCMD.ASM',SRC/'MOVES.ASM',SRC/'KSBABART.ASM',
       HERE/'baby_source.py',HERE/'generate_baby_data.py',HERE/'generated_baby/BABY_DATA.json',
       HERE/'prepare_game_candidate.py',BASE/'test_wolf_baseline.py',Path(__file__)]
if (run/'baby_objects.csv').exists():paths.append(run/'baby_objects.csv')
paths+=sorted((run/'snap').glob('*.png'))
if negative:
    paths += [eligibility_path,HERE/'finisher_eligibility.py']
    report['nativeIneligibleCommandObservedFrames']=command_frames
if morphed:
    report.update(selectedCharacter=6,activeCommandCharacter=actor,transformedBabality=True)
    report['nativeVictoryReturnToShangObserved']=not negative
    paths.extend([run/'morph_finish.csv',eligibility_path,HERE/'finisher_morph_identity.py',HERE/'finisher_eligibility.py',SRC/'MKST.ASM',SRC/'MKCANNED.ASM'])
report['pins']={str(p):sha(p) for p in paths}
report['pins'][str(HERE/'finisher_observation_end.py')]=sha(HERE/'finisher_observation_end.py')
report['pins'][str(HERE/'verify_finisher_roms.py')]=sha(HERE/'verify_finisher_roms.py')
report['currentFull26ROMBytesVerified']=True
(run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
