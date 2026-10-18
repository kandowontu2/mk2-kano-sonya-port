"""Bounded audio-control comparison; not a gameplay/audio acceptance gate."""
import hashlib
import json
from pathlib import Path
import wave
import numpy as np

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
proof=json.loads((PORT/'generated_dcs/DCS_CHICKEN_EVENTS.json').read_text())
first=proof['events'][0]['seconds']
paths=[BASE/proof[key]/'native_dcs.wav' for key in ('nativeRun','controlRun')]
windows=[]
with wave.open(str(paths[0]),'rb') as native, wave.open(str(paths[1]),'rb') as control:
    assert native.getparams()==control.getparams()
    assert native.getframerate()==48000 and native.getnchannels()==1 and native.getsampwidth()==2
    # Each allocation is only half a second, irrespective of match length.
    for offset in (-3,-2.5,-2,-1.5,-1,-.5,0,.5,1,1.5,2,2.5):
        start=round((first+offset)*48000)
        native.setpos(start);control.setpos(start)
        a=np.frombuffer(native.readframes(24000),dtype='<i2').astype(np.float64)
        b=np.frombuffer(control.readframes(24000),dtype='<i2').astype(np.float64)
        assert len(a)==len(b)==24000
        d=a-b
        windows.append(dict(relativeStartSeconds=offset,samples=24000,
            differingSamples=int(np.count_nonzero(d)),
            nativeRMS=float(np.sqrt(np.mean(a*a))),
            controlRMS=float(np.sqrt(np.mean(b*b))),
            differenceRMS=float(np.sqrt(np.mean(d*d))),
            differencePeak=float(np.max(np.abs(d)))))
report=dict(nativeRun=proof['nativeRun'],controlRun=proof['controlRun'],
    firstCueSeconds=first,windows=windows,
    preCueWindowsIdentical=all(w['differingSamples']==0 for w in windows if w['relativeStartSeconds']<0),
    wholeSceneMixVerified=False,releaseReady=False,
    limitation='Pre-cue agreement cannot establish control equivalence after new cues allocate DCS voices.')
for key,path in zip(('nativeWaveSHA256','controlWaveSHA256'),paths):
    with path.open('rb') as stream:
        report[key]=hashlib.file_digest(stream,'sha256').hexdigest().upper()
(PORT/'generated_dcs/DCS_CHICKEN_CONTROL_RESIDUAL.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
