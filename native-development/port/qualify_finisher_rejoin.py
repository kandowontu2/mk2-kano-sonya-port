"""Physical post-fatality fresh-match state, not exhaustive cleanup approval."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
for name in sys.argv[1:]:
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    args=receipt['testArguments'];assert '--finisher-rejoin' in args
    morphed='--finisher-morph' in args
    kinds=[kind for kind in ('laser','bubble','extract','kiss','friend','baby') if '--'+kind in args]
    assert len(kinds)==1
    kind=kinds[0]
    observer=(run/'autoboot.lua').read_bytes()
    assert hashlib.sha256(observer).hexdigest().upper()==receipt['controllerSHA256']
    text=observer.decode()
    assert ':write_u' not in text and not re.search(r'\.value\s*=(?!=)',text)
    assert '[LUA ERROR]' not in (run/'mame.log').read_text()
    assert not (run/(kind+'_fault.txt')).exists()
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
    events=list(csv.DictReader((run/'finisher_rejoin_events.csv').open()))
    assert [row['phase'] for row in events]==['selection','combat']
    selection,start=(int(row['frame']) for row in events)
    rows=list(csv.DictReader((run/(kind+'.csv')).open()))
    action={'laser':547,'bubble':544,'extract':540,'kiss':542}.get(kind)
    side=2 if '--mirror' in args else 1;other=3-side
    actor=(17 if '--kano' in args else 18) if kind=='friend' else ((18 if '--sonya' in args else 17) if kind=='baby' else (17 if kind in ('laser','extract') else 18))
    death_tag={'laser':'2','bubble':'2','extract':'1','kiss':'1','friend':'7','baby':'5'}[kind]
    active=[row for row in rows if int(row['frame'])<selection
            and (action is None or int(row[f'p{side}action'])==action) and row['death']==death_tag]
    expected=193 if kind=='friend' and actor==17 else (176 if kind in ('laser','bubble','friend') else (192 if kind=='baby' else 231))
    if kind=='bubble':
        from bubble_timing import expected_fields
        assert len(active)>54
        expected=expected_fields(active[54],other)
    assert len(active)==expected
    if morphed:
        assert kind in ('extract','kiss','laser','bubble')
        from finisher_morph_identity import verify as verify_morph
        verify_morph(run,active,actor)
    assert any(row['death']=='65535' and int(row['frame'])<selection for row in rows)
    victim=(1 if '--stock-victim' in args or (kind=='baby' and '--own-victim' not in args) else 35-actor)
    fresh=[row for row in rows if int(row['frame'])>=start]
    assert len(fresh)==600
    assert [int(row['frame']) for row in fresh]==list(range(start,start+600))
    assert all(row['mode']=='2' and row['death']=='0' and row['winner']=='0' for row in fresh)
    selected_actor=6 if morphed else actor
    assert all(int(row[f'p{side}char'])==selected_actor and int(row[f'p{other}char'])==victim for row in fresh)
    if morphed:
        identities={r['frame']:r for r in csv.DictReader((run/'morph_finish.csv').open())}
        assert all(identities[r['frame']]['selected']==identities[r['frame']]['actual']=='6' for r in fresh)
    assert fresh[0]['p1hp']==fresh[0]['p2hp']=='161'
    assert any(int(row[f'p{other}hp'])<161 for row in fresh)
    assert all(row['missing']=='0' for row in rows)
    assert all(row['child']=='00000000' for row in fresh)
    retired=False
    retired_frame=None
    if kind in ('laser','bubble'):
        lifetime=list(csv.DictReader((run/(kind+'_lifetime.csv')).open()))
        completion=min(int(row['frame']) for row in rows if row['death']=='65535' and int(row['frame'])<selection)
        prior=[row for row in lifetime if int(row['frame'])<completion]
        assert any(row['childActive']=='1' and row['processActive']=='1' for row in prior)
        at_completion=[row for row in lifetime if int(row['frame'])==completion]
        assert len(at_completion)==1
        assert at_completion[0]['childActive']==at_completion[0]['processActive']=='0'
        retired=True;retired_frame=completion
    cleanup=run/'finisher_cleanup.csv'
    cleanup_verified=False
    palette_sources_verified=False
    hardware_palette_verified=False
    baby_image_retired=False
    color_comparisons=0
    shapes=0
    if cleanup.exists():
        observations=list(csv.DictReader(cleanup.open()))
        assert len(observations)==600
        assert [int(row['frame']) for row in observations]==list(range(start,start+600))
        shapes=int(observations[0]['shapeCount'])
        assert shapes>0 or kind in ('friend','baby')
        assert all(int(row['shapeCount'])==shapes and int(row['objectsScanned'])>=2
                   and row['oldEffectObjects']=='0' for row in observations)
        cleanup_verified=shapes>0
        if 'p1source' in observations[0]:
            for row in observations[:60]:
                for side_number in (1,2):
                    source=row[f'p{side_number}source']
                    assert 0xff800000<=int(source,16)<=0xffffffff
                    assert source==row[f'initialP{side_number}source']
            palette_sources_verified=True
        if 'p1rgbMismatch' in observations[0]:
            for row in observations:
                for side_number in (1,2):
                    colors=int(row[f'p{side_number}colors'])
                    assert 1<=colors<=256
                    assert row[f'p{side_number}rgbMismatch']=='0'
                    color_comparisons+=colors
            hardware_palette_verified=True
        if kind=='baby' and 'babyObjects' in observations[0]:
            assert all(row['babyImageSeen']=='1' and row['babyObjects']=='0' for row in observations)
            baby_image_retired=True
    report=dict(scope='One physical fresh match after native finisher',run=name,kind=kind,
        performerSide=side,selectionFrame=selection,freshMatchFrame=start,freshCombatFields=600,
        currentFull26ROMBytesVerified=True,ownIdentitiesPreserved=True,fullStartingHealth=True,
        combatDamageObserved=True,noTrackedFinisherChild=True,deathAndWinnerStateReset=True,
        allObjectsProcessesPalettesAndAudioTailsVerified=False,releaseReady=False,
        observedOldEffectShapesAbsentFromActiveObjectList=cleanup_verified,
        priorEffectShapesChecked=shapes,
        trackedEffectObjectAndProcessAbsentAtCompletion=retired,
        completionRetirementFrame=retired_frame,
        originalPaletteSourcesRestoredFirst60Fields=palette_sources_verified,
        actualHardwarePaletteRGBVerified=hardware_palette_verified,
        freshMatchPaletteColorComparisons=color_comparisons,
        observedBabyImageAbsentFromFreshActiveList=baby_image_retired,
        freshSelectedCharacter=selected_actor,transformedFinisher=morphed,
        observerSHA256=receipt['controllerSHA256'],verifierSHA256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper())
    evidence=[run/'execution.json',run/(kind+'.csv'),run/'finisher_rejoin_events.csv',
              run/'autoboot.lua',Path(__file__),PORT/'verify_finisher_roms.py']
    evidence += [path for path in (cleanup,run/(kind+'_lifetime.csv')) if path.exists()]
    if morphed:evidence.extend([run/'morph_finish.csv',PORT/'finisher_morph_identity.py'])
    if kind=='bubble':evidence.append(PORT/'bubble_timing.py')
    report['evidenceSHA256']={str(path):hashlib.sha256(path.read_bytes()).hexdigest().upper() for path in evidence}
    (run/'FINISHER_REJOIN_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
