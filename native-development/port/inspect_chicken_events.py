"""Current native cue timing/variants, not waveform or final-mix acceptance."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from current_sound import verify_latest_playlist
from current_graphics import verify_archive_sockets
from chicken_evidence_names import event_filename

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';BUILD=BASE/'mk2-rebuild-main'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
verify_latest_playlist()
track_args=[arg.split('=',1)[1] for arg in sys.argv[1:] if arg.startswith('--single-track=')]
assert len(track_args)<=1 and all(track in ('1','2','3') for track in track_args)
single_track=int(track_args[0]) if track_args else 0
matched='--muted-control' in sys.argv or bool(single_track)
names=[arg for arg in sys.argv[1:] if arg!='--muted-control' and not arg.startswith('--single-track=')];assert len(names)==2
cases=[]
for name,candidate in zip(names,(True,False)):
    folder=BASE/name;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha(Path(receipt['emulator']).read_bytes())==receipt['emulatorSHA256']
    candidate_flag=f'--sound-chicken-track={single_track}' if single_track else '--sound-candidate'
    assert (candidate_flag in receipt['testArguments'])==candidate
    assert ('--sound-chicken-muted' in receipt['testArguments'])==(matched and not candidate)
    observer=(folder/'autoboot.lua').read_text()
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    assert ':write_u' not in observer and '[LUA ERROR]' not in (folder/'mame.log').read_text()
    assert 'return' not in observer.split('function(address,data,mask)',1)[1].split('end)',1)[0]
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((BUILD/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        verify_archive_sockets(archive)
        for chip in range(2,6):
            source=(BASE/f'chicken_track{single_track}_control/U{chip}.ROM' if single_track and candidate else
                    BASE/f'chicken_muted_control/U{chip}.ROM' if matched and not candidate else BUILD/f'{"soundp" if candidate else "soundw"}/U{chip}.ROM')
            assert archive.read(f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}')==source.read_bytes()
    rows=list(csv.DictReader((folder/'friend.csv').open()))
    active=[row for row in rows if row['death']=='7']
    assert len(active)==176 and all(row['missing']=='0' for row in rows)
    first=int(active[0]['frame'])
    expected=[83+index*3 for index in range(31) if index%14 in (2,4,6)]
    writes=list(csv.DictReader((folder/'native_sound_writes.csv').open()));events=[]
    for high,low in zip(writes,writes[1:]):
        code=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
        if 2036<=code<=2047:
            assert high['address']==low['address']=='01680000'
            events.append(dict(age=int(high['frame'])-first,frame=int(high['frame']),
                               seconds=float(high['seconds']),variant=(code-2036)//3,track=(code-2036)%3+1))
    action_events=[event for event in events if event['age']<176]
    assert [event['age']+1 for event in action_events]==expected,events
    assert all((event['age']+1-83)%42 in (6,12,18) for event in events)
    cases.append((folder,receipt,events))
assert cases[0][1]['controllerSHA256']==cases[1][1]['controllerSHA256']
assert set(cases[0][1]['testArguments'])-{candidate_flag}==set(cases[1][1]['testArguments'])-{'--sound-chicken-muted'}
assert [(event['age'],event['variant'],event['track']) for event in cases[0][2]]==[(event['age'],event['variant'],event['track']) for event in cases[1][2]]
mirror='--mirror' in cases[0][1]['testArguments']
report=dict(scope='Physical Friendship native port events aligned to donor cue positions',physicalSide=2 if mirror else 1,
    nativeRun=names[0],controlRun=names[1],events=cases[0][2],cueAges=expected,
    skippedOrExtraCuesDuringAction=False,
    totalCues=len(cases[0][2]),resultPresentationCues=sum(event['age']>=176 for event in cases[0][2]),
    resultCueCadencePreserved=True,resultEndCleanupVerified=False,
    allFourVariantsObserved=len({event['variant'] for event in cases[0][2]})==4,
    waveformVerified=False,overlapMixVerified=False,releaseReady=False)
output='DCS_CHICKEN_MIRROR_EVENTS.json' if mirror else 'DCS_CHICKEN_EVENTS.json'
report['pins']={str(path):sha(path.read_bytes()) for folder,_,_ in cases
                for path in [folder/item for item in ('execution.json','autoboot.lua','friend.csv','native_sound_writes.csv','native_dcs.wav')]}
report['pins'][str(Path(__file__))]=sha(Path(__file__).read_bytes())
report['pins'][str(PORT/'chicken_evidence_names.py')]=sha((PORT/'chicken_evidence_names.py').read_bytes())
if matched:
    report['controlBank']='current SoundP with only chicken playlist volume operands muted'
    output='DCS_CHICKEN_MATCHED_EVENTS.json'
if single_track:
    report.update(diagnosticSoundBank=True,audibleTrack=single_track,
                  audibleCueCount=sum(e['track']==single_track for e in cases[0][2]))
    output=f'DCS_CHICKEN_TRACK{single_track}_EVENTS.json'
output=event_filename(matched=matched,mirror=mirror,track=single_track)
(PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
