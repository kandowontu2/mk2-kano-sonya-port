"""Bounded physical morph identity/reversion evidence, not visual acceptance."""
import csv
import json
from pathlib import Path
import re
import sys
import zipfile
from qualify_bubble import BASE,HERE,SRC,sha
from verify_finisher_roms import verify

run=BASE/sys.argv[1]
execution=json.loads((run/'execution.json').read_text())
mirror='--mirror' in execution['testArguments']
specials='--morph-specials' in execution['testArguments']
ball='--morph-ball' in execution['testArguments']
melee='--morph-melee' in execution['testArguments']
grapples='--morph-grapples' in execution['testArguments']
square='--morph-square' in execution['testArguments']
throws='--morph-throws' in execution['testArguments']
late_throw='--morph-late-throw' in execution['testArguments']
assert execution['exitCode']==0 and not execution['timedOut']
assert not execution['customDriver'] and not execution['gameMemoryWrites']
assert execution['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert execution['controllerSHA256']==sha(run/'autoboot.lua')
observer=(run/'autoboot.lua').read_text()
assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
assert '[LUA ERROR]' not in (run/'mame.log').read_text()
assert not (run/'morph_fault.txt').exists()
with zipfile.ZipFile(run/'roms/mk3.zip') as roms:
    verify(roms,execution)
rows=list(csv.DictReader((run/'morph.csv').open()))
assert len(rows)==9000 and int(rows[-1]['frame'])==9000
assert all(r['missing']=='0' for r in rows)
fight=[r for r in rows if r['mode']=='2' and r['p1selected']=='6' and r['p2selected']=='18']
assert len(fight)>2700
assert all(r['p2char']=='18' for r in fight)
assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in fight)
segments=[]
for r in fight:
    if not segments or segments[-1]['id']!=int(r['p1char']):
        segments.append(dict(id=int(r['p1char']),firstFightField=int(r['fight']),fields=0))
    segments[-1]['fields']+=1
assert [s['id'] for s in segments]==[6,17,6,18,6,18,6]
if late_throw:
    assert throws and not specials
    durations=[s['fields'] for s in segments if s['id'] in (17,18)]
    assert all(524<=duration<=640 for duration in durations[:2]) and durations[2]==524
else:
    assert [s['fields'] for s in segments if s['id'] in (17,18)]==[524,524,524]
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
for actor,name in [(17,'kano'),(18,'sonya')]:
    own={v for k,v in symbols.items() if k.startswith(f'ks_{name}_pose_')}
    if throws:
        data=json.loads((HERE/'generated_throw/THROW_DATA.json').read_text())['actors'][name]
        own.update(symbols[p] for phase in data['bodyPhases'] for p in phase['poses'])
    assert own
    transition={symbols[f'ks_mo_{name}_pose{phase}'] for phase in range(3)}
    assert all(int(r['p1shape'],16) in own or
        (r['action']=='1028' and int(r['p1shape'],16) in transition)
        for r in fight if r['p1char']==str(actor))
special_report={}
if square:
    assert not any((specials,throws,ball,melee,grapples))
    active=[r for r in fight if r['action']==str(0x207)]
    assert active and all(r['p1char']=='18' and 1246<int(r['fight'])<1400 for r in active)
    assert active[0]['victimAction'] in ('776','779'), 'Opponent must be in native jump state at launch'
    by_field={int(r['fight']):r for r in fight}
    assert int(by_field[1230]['victimHP'])-int(by_field[1450]['victimHP'])==27
    assert any(1400<int(r['fight'])<1500 and r['p1char']=='18' and r['action']=='771' for r in fight)
    special_report['transformedSquare']=dict(actionFields=len(active),groundedAttemptRejected=True,
        jumpingOpponentAtLaunch=True,damage=int(by_field[1230]['victimHP'])-int(by_field[1450]['victimHP']),recoveredBeforeMorphReturn=True)
if grapples:
    assert not specials and not throws and not ball and not melee
    by_field={int(r['fight']):r for r in fight}
    cases=[]
    for actor,action,victim_action,start,end,fields,damage in [(17,535,536,310,600,69,32),(18,538,539,1150,1450,46,35)]:
        held=[r for r in fight if r['action']==str(action)]
        assert len(held)==fields and all(r['p1char']==str(actor) and r['victimAction']==str(victim_action) for r in held)
        assert all(int(b['frame'])==int(a['frame'])+1 for a,b in zip(held,held[1:]))
        assert all(start<int(r['fight'])<end for r in held)
        assert int(by_field[start]['victimHP'])-int(by_field[end]['victimHP'])==damage
        assert any(end-60<int(r['fight'])<end and r['p1char']==str(actor) and r['action']==r['victimAction']=='771' for r in fight)
        cases.append(dict(identity=actor,pairedFields=fields,damage=damage,bothRecoveredBeforeMorphReturn=True))
    special_report['transformedGrapples']=cases
if melee:
    assert not specials and not throws and not ball
    by_field={int(r['fight']):r for r in fight}
    for actor,actions,start,end,damage in [(17,(0x117,),310,550,26),(18,(0x204,0x214),1100,1450,22)]:
        for action in actions:
            active=[r for r in fight if r['action']==str(action)]
            assert active and all(r['p1char']==str(actor) and start<int(r['fight'])<end for r in active)
        assert int(by_field[start]['victimHP'])-int(by_field[end]['victimHP'])==damage
        assert any(end<int(r['fight'])<end+60 and r['p1char']==str(actor) and r['action']=='771' for r in fight)
    special_report['transformedBladeAndBike']=dict(bladeDamage=26,bikeDamage=22,recoveredBeforeMorphReturn=True)
if ball:
    assert not specials and not throws
    active=[r for r in fight if r['action']==str(0x20b)]
    assert active and all(r['p1char']=='17' and 350<int(r['fight'])<430 for r in active)
    by_field={int(r['fight']):r for r in fight}
    damage=int(by_field[250]['victimHP'])-int(by_field[500]['victimHP'])
    assert damage==24,damage
    assert any(430<int(r['fight'])<600 and r['p1char']=='17' and r['action']=='771' for r in fight)
    special_report['transformedBall']=dict(actionFields=len(active),damage=damage,
        recoveredBeforeMorphReturn=True,requestedPhysicalLKChargeFields=100)
if throws:
    throw_cases=[]
    for identity in (17,18):
        active=[r for r in fight if r['p1char']==str(identity) and r['action']==str(0x507)]
        assert active
        first,last=int(active[0]['fight']),int(active[-1]['fight'])
        window=[r for r in fight if first<=int(r['fight'])<=last+180]
        damage=int(active[0]['victimHP'])-min(int(r['victimHP']) for r in window)
        assert damage==34,damage
        segment=next(s for s in segments if s['id']==identity)
        returned=segment['firstFightField']+segment['fields']
        assert last<returned
        if late_throw:
            nominal=segment['firstFightField']+524
            assert first<nominal<=last and last<returned<=last+64
        assert any(int(r['fight'])>last and int(r['fight'])<last+180 and r['action']!=str(0x507) and r['p1char']==str(identity) for r in fight)
        throw_cases.append(dict(identity=identity,ownerActionFields=len(active),damage=damage,recoveredBeforeMorphReturn=True,
            firstThrowField=first,lastThrowField=last,returnField=returned,throwOverlapsNominalExpiry=late_throw))
    special_report['transformedThrows']=throw_cases
if specials:
    by_field={int(r['fight']):r for r in fight}
    for actor,action,start,end,fields in [(17,529,250,400,25),(18,530,1150,1350,15)]:
        active=[r for r in fight if r['action']==str(action)]
        assert len(active)==fields and all(r['p1char']==str(actor) for r in active)
        assert all(start<int(r['fight'])<end for r in active)
        assert int(by_field[start]['victimHP'])-int(by_field[end]['victimHP'])==22
    special_report=dict(transformedKnifeAndRingActivated=True,knifeDamage=22,ringDamage=22,
                        knifeActionFields=25,ringChargeFields=15)
report=dict(scope='finite physical commands and automatic native return, stationary opponent; CSV roles normalized',
            physicalActorSide=2 if mirror else 1,
            frames=9000,segments=segments,kanoCommandObserved=True,
            sonyaBothButtonOrdersObserved=True,actualOwnIdentityAndPoseObserved=True,
            timedReturnObserved=True,missingRootMarkers=0,bespokeMorphArtComplete=False,
            currentFull26ROMBytesVerified=True,
            mirrorEdgesPaletteAndSpecialsQualified=False,fullPortVerified=False,releaseReady=False)
report.update(special_report)
paths=[run/'execution.json',run/'autoboot.lua',run/'morph.csv',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
       SRC/'MOVES.ASM',SRC/'MKST.ASM',SRC/'KSCMD.ASM',SRC/'MKCANNED.ASM',SRC/'MKUTIL.ASM',
       SRC/'KSPROJ.ASM',HERE/'morph_source.py',HERE/'prepare_game_candidate.py',
       BASE/'test_wolf_baseline.py',Path(__file__),HERE/'verify_finisher_roms.py']
if ball: paths.extend([SRC/'KANOMOV.ASM',HERE/'diagnostics/morph_probe.lua'])
if melee: paths.extend([SRC/'KSBLADE.ASM',SRC/'KSBIKE.ASM',HERE/'diagnostics/morph_probe.lua'])
if grapples: paths.extend([SRC/'KSCHOKE.ASM',SRC/'KSLEG.ASM',HERE/'diagnostics/morph_probe.lua'])
if square: paths.extend([SRC/'SONYAMOV.ASM',HERE/'diagnostics/morph_probe.lua'])
report['pins']={str(p):sha(p) for p in paths}
(run/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
