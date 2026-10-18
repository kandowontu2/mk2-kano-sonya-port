"""Stage one source-owned Sonya launch clip for original HENRY/PLBUILD tools.

This is an isolated sound candidate. It does not replace the accepted soundw
images or imply that final voice provenance/mix/all-event acceptance is closed.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import wave
import numpy as np
import scipy
from scipy.signal import resample_poly

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline/mk2-rebuild-main'
ROOT=PORT.parents[1]
SOURCE=BASE/'soundw'
DEST=BASE/'soundp'
OUT=PORT/'generated_dcs'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()

def main():
    assert not DEST.exists() and not OUT.exists(), 'Never overwrite a sound candidate'
    source=ROOT/'samples/mk2ks/sonya_square_launch.wav'
    raw=source.read_bytes()
    with wave.open(str(source),'rb') as clip:
        assert clip.getnchannels()==1 and clip.getsampwidth()==2
        rate=clip.getframerate();frames=clip.getnframes()
        samples=np.frombuffer(clip.readframes(frames),dtype='<i2').astype(np.float64)
    divisor=math.gcd(rate,31250)
    source_peak=float(np.max(np.abs(samples)))
    assert source_peak>0
    gain=16384/source_peak
    converted=resample_poly(samples*gain,31250//divisor,rate//divisor,window=('kaiser',8.6))
    converted=np.clip(np.rint(converted),-32768,32767).astype('<i2')
    assert len(converted)==math.ceil(frames*31250/rate)
    assert np.max(np.abs(converted.astype(np.int32)))>1000
    DEST.mkdir();(DEST/'SNDS').mkdir();OUT.mkdir()
    for name in ('PLBUILD.EXE','DOS4GW.EXE','cwsdpmi.exe','VIDEOT6.BIN','MK2.DEF','MK2.EVD','MK2.MSK','MK2.LOC'):
        shutil.copyfile(SOURCE/name,DEST/name)
    linked=0
    for path in (SOURCE/'SNDS').glob('*.CMP'):
        if path.name.startswith('KSREF'): continue
        os.link(path,DEST/'SNDS'/path.name);linked+=1
    for name in ('HENRY.EXE','DOS4GW.EXE'):
        os.link(SOURCE/'SNDS'/name,DEST/'SNDS'/name)
    (DEST/'SNDS/KSSQ.SND').write_bytes(converted.tobytes())
    playlists=(SOURCE/'MK2.PLS').read_bytes().decode('latin-1').replace('\r\n','\n')
    assert not re.search(r'^\s*(?:playlist\s+)?200[012]\b',playlists,re.M|re.I)
    # Insert calls before the END belonging to SOUNDCALLS, not TRANSITION.
    marker=re.search(r'^END\s*$',playlists,re.M)
    assert marker
    calls='; MK2KS native DCS Sonya Square launch, own region on all3 effect tracks.\n'
    calls+=''.join(f'\t{event}\timmed\t\t{event}\n' for event in (2000,2001,2002))
    playlists=playlists[:marker.start()]+calls+playlists[marker.start():]
    duration=math.ceil(len(converted)/240)+2
    additions='\n; MK2KS authored native playlist extension. No host sample callbacks.\n'
    for track,event in enumerate((2000,2001,2002),1):
        additions+=f"\tplaylist\t{event}, {track}, 'Sonya Square launch'\n"
        additions+=f"\t0\tsetvol\t{track}, 100\n\t0\tplay\t{track}, 'kssq', 1\n\t{duration}\tend\n\tend\n"
    playlists=playlists.replace('\x1a','').rstrip()+additions+'\n\x1a\n'
    (DEST/'MK2.PLS').write_bytes(playlists.encode('latin-1'))
    (OUT/'KSSOUND.PLS').write_text(calls+additions,encoding='ascii')
    report=dict(sourceClip=str(source),sourceSHA256=sha(raw),sourceRate=rate,sourceFrames=frames,
        stagedPCM='SNDS/KSSQ.SND',stagedPCM_SHA256=sha(converted.tobytes()),
        sampleRate=31250,samples=len(converted),sourcePeak=source_peak,normalizationGain=gain,
        targetPeakBeforeResampling=16384,finalMixAccepted=False,
        resampler='scipy.signal.resample_poly/kaiser8.6',
        scipyVersion=scipy.__version__,numpyVersion=np.__version__,originalCMPHardLinks=linked,
        originalPlaylistSHA256=sha((SOURCE/'MK2.PLS').read_bytes()),
        stagedPlaylistSHA256=sha((DEST/'MK2.PLS').read_bytes()),soundCalls=[2000,2001,2002],
        playlistDelay=duration,nativePriorityDuration=math.ceil(len(converted)/31250*60)+2,
        HENRYSHA256=sha((DEST/'SNDS/HENRY.EXE').read_bytes()),
        PLBUILDSHA256=sha((DEST/'PLBUILD.EXE').read_bytes()),
        sourceVoiceProvenanceFullyReviewed=False,compiled=False,runtimeVerified=False,fullPortVerified=False)
    (OUT/'DCS_INPUTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
