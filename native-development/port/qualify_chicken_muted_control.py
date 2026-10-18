"""Qualify diagnostic source differences before interpreting control playback."""
import hashlib
import json
from pathlib import Path
import re
import argparse
from chicken_control_playlist import control_playlist,verify_location_map,verify_sample_rom
from current_sound import verify_latest_playlist

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SOURCE=BASE/'mk2-rebuild-main/soundp'
parser=argparse.ArgumentParser()
parser.add_argument('--keep-track',type=int,choices=(0,1,2,3),default=0)
args=parser.parse_args()
CONTROL=BASE/('chicken_muted_control' if args.keep_track==0 else f'chicken_track{args.keep_track}_control')
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
verify_latest_playlist()
assert (CONTROL/'OK.TXT').read_text().strip()=='DONE'
assert not (CONTROL/'FAIL.TXT').exists()
source=(SOURCE/'MK2.PLS').read_bytes()
pattern=rb"playlist\s+(203[6-9]|204[0-7]), [123], 'Sonya Friendship [0-3]'\s+0\s+setvol\s+[123], 100"
changed=[]
def mute(match):
    changed.append(int(match[1]))
    return match[0].replace(b', 100',b', 0',1)
legacy=re.sub(pattern,mute,source)
assert changed==list(range(2036,2048))
modified,changed=control_playlist(source,args.keep_track)
assert legacy==control_playlist(source,0)[0]
assert modified==(CONTROL/'MK2.PLS').read_bytes()
inputs=json.loads((CONTROL/'INPUTS.json').read_text())
for relative,digest in inputs['inputs'].items():
    assert sha((SOURCE/relative).read_bytes())==digest
    if relative=='MK2.LOC':
        verify_location_map((SOURCE/relative).read_bytes(),(CONTROL/relative).read_bytes())
    else:assert sha((CONTROL/relative).read_bytes())==digest
for name in ('MK2.EVD','MK2.DEF','MK2.MSK','VIDEOT6.BIN'):
    assert (CONTROL/name).read_bytes()==(SOURCE/name).read_bytes()
roms={};differences={}
for chip in range(2,6):
    name=f'U{chip}.ROM';a=(SOURCE/name).read_bytes();b=(CONTROL/name).read_bytes()
    assert len(a)==len(b)==1048576
    if chip>=3:verify_sample_rom(a,b,chip)
    roms[name]=sha(b)
    differences[name]=sum(x!=y for x,y in zip(a,b))
assert sum(differences.values())>0
assert len([name for name in inputs['inputs'] if name.upper().endswith('.CMP')])==455
report=dict(diagnosticOnly=True,releaseReady=False,
    playlistOnlyChangeProven=all(differences[f'U{chip}.ROM']==0 for chip in range(3,6)),
    playlistOnlyFunctionalChangeProven=True,sampleROMPayloadBytesUnchanged=True,preservedTrack=args.keep_track,
    generatedLocationMapBodyUnchanged=True,controlLocationMapSHA256=sha((CONTROL/'MK2.LOC').read_bytes()),
    mutedCalls=changed,compressedInputsUnchanged=455,
    currentPlaylistSHA256=sha(source),controlPlaylistSHA256=sha((CONTROL/'MK2.PLS').read_bytes()),
    controlROMSHA256=roms,differingBytes=differences,
    limitation='Runtime and DCS volume interactions require paired recording; this is not a release sound bank.')
(CONTROL/'QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
