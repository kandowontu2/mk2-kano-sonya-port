"""Require all non-guard PCM positions to exist in original-tool decode."""
import json
from pathlib import Path
import numpy as np
from scipy.signal import correlate
from prepare_dcs_candidate import DEST,OUT,sha

inputs=json.loads((OUT/'DCS_CHICKEN_INPUTS.json').read_text())
results=[]
for clip in inputs['clips']:
    path=DEST/f'SNDS/{clip["region"]}.SND'
    pcm=path.read_bytes();assert sha(pcm)==clip['pcmSHA256']
    decoded_bytes=path.with_suffix('.AUD').read_bytes()
    assert len(decoded_bytes)%2==0
    count=len(decoded_bytes)//2
    assert clip['unpaddedSamples']<=count<=clip['samples'],(clip['region'],count)
    omitted=pcm[count*2:]
    assert not any(omitted),'Nonzero source samples still absent from decoder output'
    reference=np.frombuffer(pcm,dtype='<i2')[:clip['unpaddedSamples']].astype(float)
    decoded=np.frombuffer(decoded_bytes,dtype='<i2')[:clip['unpaddedSamples']].astype(float)
    score=float(abs(np.dot(reference,decoded))/(np.linalg.norm(reference)*np.linalg.norm(decoded)))
    cross=correlate(decoded,reference,method='fft')
    center=len(reference)-1
    at=center-240+int(np.argmax(np.abs(cross[center-240:center+241])))
    aligned=float(abs(cross[at])/(np.linalg.norm(reference)*np.linalg.norm(decoded)))
    results.append(dict(region=clip['region'],inputSamples=clip['samples'],decodedSamples=count,
        originalPCMPositionsRetained=clip['unpaddedSamples'],omittedZeroGuardSamples=len(omitted)//2,
        zeroOffsetCorrelation=score,alignedCorrelation=aligned,alignmentSamples=at-center,
        decodedSHA256=sha(decoded_bytes)))
report=dict(scope='Original-tool cluck decode lengths and full original-position codec comparison',
    clips=results,allOriginalPCMPositionsRetained=True,
    allCodecCorrelationsAbove095=all(clip['alignedCorrelation']>.95 for clip in results),
    codecFidelityAccepted=False,runtimePlaybackVerified=False,
    finalMixAccepted=False,releaseReady=False)
(OUT/'DCS_CHICKEN_CODEC_LENGTHS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
