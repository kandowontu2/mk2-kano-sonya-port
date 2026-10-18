"""Stage a non-release matched SoundP control, muting only chicken playlists."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import argparse
from chicken_control_playlist import control_playlist
from current_sound import verify_latest_playlist

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SOURCE=BASE/'mk2-rebuild-main/soundp'
parser=argparse.ArgumentParser()
parser.add_argument('--keep-track',type=int,choices=(0,1,2,3),default=0)
args=parser.parse_args()
TARGET=BASE/('chicken_muted_control' if args.keep_track==0 else f'chicken_track{args.keep_track}_control')
assert not TARGET.exists(), 'Never overwrite an existing diagnostic build'
verify_latest_playlist()
original=(SOURCE/'MK2.PLS').read_bytes()
changed=[]
def mute(match):
    number=int(match[1])
    changed.append(number)
    return match[0].replace(b', 100',b', 0',1)
pattern=rb"playlist\s+(203[6-9]|204[0-7]), [123], 'Sonya Friendship [0-3]'\s+0\s+setvol\s+[123], 100"
modified=re.sub(pattern,mute,original)
assert changed==list(range(2036,2048))
assert modified.count(b', 100')==original.count(b', 100')-12
# Independent legacy all-muted transform must remain byte-identical.
assert control_playlist(original,0)==(modified,changed)
modified,changed=control_playlist(original,args.keep_track)
TARGET.mkdir()
(TARGET/'SNDS').mkdir()
inputs={}
for name in ('PLBUILD.EXE','DOS4GW.EXE','cwsdpmi.exe','MK2.DEF','MK2.EVD','MK2.LOC','MK2.MSK','VIDEOT6.BIN'):
    shutil.copy2(SOURCE/name,TARGET/name)
    inputs[name]=hashlib.sha256((SOURCE/name).read_bytes()).hexdigest().upper()
for source in (SOURCE/'SNDS').glob('*.CMP'):
    # PLBUILD only reads these; copy so this diagnostic cannot alter originals.
    shutil.copy2(source,TARGET/'SNDS'/source.name)
    inputs['SNDS/'+source.name]=hashlib.sha256(source.read_bytes()).hexdigest().upper()
(TARGET/'MK2.PLS').write_bytes(modified)
(TARGET/'BUILD.BAT').write_bytes(b'@echo off\r\nPLBUILD -e MK2 > EBUILD.LOG\r\nif errorlevel 1 goto failed\r\nPLBUILD -m MK2 > BUILD.LOG\r\nif errorlevel 1 goto failed\r\necho DONE > OK.TXT\r\ngoto end\r\n:failed\r\necho FAILED > FAIL.TXT\r\n:end\r\nexit\r\n')
config='[sdl]\nvideodriver=dummy\nautolock=false\nwaitonerror=false\noutput=surface\n[dosbox]\nmemsize=32\n[cpu]\ncore=normal\ncycles=max\n[mixer]\nnosound=true\n[dos]\nfiles=200\n[autoexec]\nmount c "'+TARGET.as_posix()+'"\nc:\ncall C:\\BUILD.BAT\n'
(TARGET/'dosbox.conf').write_text(config)
report=dict(diagnosticOnly=True,releaseReady=False,mutedPlaylistCalls=changed,preservedTrack=args.keep_track,
    change='Only selected chicken setvol operands: 100 -> 0; play, duration and routing unchanged',
    originalPlaylistSHA256=hashlib.sha256(original).hexdigest().upper(),
    controlPlaylistSHA256=hashlib.sha256(modified).hexdigest().upper(),inputs=inputs)
(TARGET/'INPUTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(target=str(TARGET),copiedCompressedClips=len(inputs)-8,mutedCalls=changed)))
