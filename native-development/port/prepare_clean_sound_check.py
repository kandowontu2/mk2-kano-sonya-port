"""Replay authored sound staging from original inputs and eleven source WAVs."""
import contextlib
import hashlib
import importlib
import io
import json
from pathlib import Path
import zipfile
import prepare_dcs_candidate as initial

PORT=Path(__file__).resolve().parent
BUILD=initial.BASE
CLEAN=BUILD.parent/'clean_program'
assert CLEAN.is_dir() and not (CLEAN/'soundp').exists() and not (CLEAN/'dcs_manifest').exists()
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
archive=Path('C:/Users/kando/Downloads/mk2-rebuild-main.zip')
assert sha(archive.read_bytes())=='2EE5C1FAD3122B6A7FE20AEF948CF96E54D4625DA073CA64273372817961A4A5'
original_inputs={}
with zipfile.ZipFile(archive) as z:
    names={name.lower():name for name in z.namelist()}
    paths=[path for path in (initial.SOURCE/'SNDS').glob('*.CMP') if not path.name.startswith('KSREF')]
    assert len(paths)==439
    paths += [initial.SOURCE/name for name in ('MK2.PLS','PLBUILD.EXE','DOS4GW.EXE','cwsdpmi.exe','VIDEOT6.BIN','MK2.DEF','MK2.EVD','MK2.MSK','MK2.LOC')]
    paths += [initial.SOURCE/'SNDS'/name for name in ('HENRY.EXE','DOS4GW.EXE')]
    for path in paths:
        relative=path.relative_to(initial.SOURCE).as_posix()
        original=z.read(names[('mk2-rebuild-main/soundw/'+relative).lower()])
        if relative=='MK2.LOC':
            # Working LOC is a generated placement map; clean linking starts
            # from the archive's original map, not the working rebuild output.
            original_loc=original
        else:
            assert path.read_bytes()==original,path
        original_inputs[relative]=sha(original)
initial.DEST=CLEAN/'soundp'
initial.OUT=CLEAN/'dcs_manifest'
with contextlib.redirect_stdout(io.StringIO()):
    initial.main()
    (initial.DEST/'MK2.LOC').write_bytes(original_loc)
    (initial.OUT/'ANNOUNCER_ROUTE_AUDIT.json').write_bytes((PORT/'generated_dcs/ANNOUNCER_ROUTE_AUDIT.json').read_bytes())
    for name in ('extend_dcs_bike','extend_dcs_announcer','extend_dcs_kiss','extend_dcs_kano_pop','extend_dcs_kano_ball','extend_dcs_chicken'):
        stage=importlib.import_module(name)
        stage.main()
stages={}
for name in ('DCS_INPUTS.json','DCS_BIKE_INPUTS.json','DCS_ANNOUNCER_INPUTS.json','DCS_KISS_INPUTS.json','DCS_KANO_POP_INPUTS.json','DCS_KANO_BALL_INPUTS.json','DCS_CHICKEN_INPUTS.json'):
    old=json.loads((PORT/'generated_dcs'/name).read_text())
    new=json.loads((initial.OUT/name).read_text())
    assert new['stagedPlaylistSHA256']==old['stagedPlaylistSHA256'],name
    stages[name]=new['stagedPlaylistSHA256']
own=list((initial.DEST/'SNDS').glob('*.SND'))
assert len(own)==16
assert all(not path.with_suffix('.CMP').exists() for path in own)
assert not list(initial.DEST.glob('U*.ROM'))
(CLEAN/'SNDBUILD.BAT').write_bytes((BUILD/'SNDBUILD.BAT').read_bytes())
report=dict(scope='Independent own-WAV PCM and playlist regeneration with original sound inputs',
    originalInputZIP_SHA256=sha(archive.read_bytes()),originalInputSHA256=original_inputs,
    playlistStages=stages,ownClipsRegenerated=16,ownCompressedSamplesImported=False,
    existingSoundROMsImported=False,sourcePCM_SHA256={path.name:sha(path.read_bytes()) for path in own},
    cleanSoundRebuildVerified=False,releaseReady=False)
(PORT/'CLEAN_SOUND_INPUTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(ownWAVsRegenerated=16,originalCMPsVerified=439,
    playlistByteIdentical=True,ownCompressedSamplesImported=False,existingSoundROMsImported=False),indent=2))
