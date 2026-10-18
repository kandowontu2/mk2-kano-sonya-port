"""Bounded pure PCM preparation for missing native Friendship cues.

No playlist/caller staging: original callback timing/track policy still needs
source review. Never infer that four existing samples constitute playback.
"""
import hashlib
import json
import math
from pathlib import Path
import wave
import numpy as np
from scipy.signal import resample_poly

PORT=Path(__file__).resolve().parent
ROOT=PORT.parents[1]
NAMES=('sonya_chicken_a5','sonya_chicken_aa','sonya_chicken_af','sonya_chicken_96')

def encode(path):
    with wave.open(str(path),'rb') as wav:
        assert wav.getnchannels()==1 and wav.getsampwidth()==2
        rate=wav.getframerate();count=wav.getnframes()
        assert rate in (22050,24000,31250,44100,48000) and 0<count<=rate*2
        raw=wav.readframes(count)
    values=np.frombuffer(raw,dtype='<i2').astype(np.float64)
    peak=float(np.max(np.abs(values)));assert peak>0
    divisor=math.gcd(rate,31250)
    pcm=resample_poly(values*(16384/peak),31250//divisor,rate//divisor,window=('kaiser',8.6))
    pcm=np.clip(np.rint(pcm),-32768,32767).astype('<i2')
    original_samples=len(pcm)
    padding=(-original_samples)%240+240
    pcm=np.pad(pcm,(0,padding))
    assert len(pcm)<=62500
    return pcm.tobytes(),dict(source=str(path),sourceSHA256=hashlib.sha256(path.read_bytes()).hexdigest().upper(),
        sourceRate=rate,sourceFrames=count,peak=peak,normalizationGain=16384/peak,
        samples=len(pcm),unpaddedSamples=original_samples,paddingSamples=padding,guardSamples=240,
        rate=31250,pcmSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper())

def main():
    # Dry analysis only; this deliberately does not mutate the current bank.
    clips=[encode(ROOT/'samples/mk2ks'/f'{name}.wav')[1] for name in NAMES]
    print(json.dumps(dict(scope='Dry bounded encoding, not native audio playback',clips=clips,
        originalTimingReviewed=False,nativeCallerImplemented=False,soundBankChanged=False,
        runtimeVerified=False,releaseReady=False),indent=2))

if __name__=='__main__':main()
