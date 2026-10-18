"""Fixed post-cue PCM comparison; not individual voice or whole-mix proof."""
import hashlib
import json
from pathlib import Path
import wave
import sys
import numpy as np
from chicken_evidence_names import event_filename

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def inspect(mirror=False):
    evidence=PORT/'generated_dcs'/event_filename(matched=True,mirror=mirror)
    proof=json.loads(evidence.read_text())
    assert proof['physicalSide']==(2 if mirror else 1)
    paths=[BASE/proof[key]/'native_dcs.wav' for key in ('nativeRun','controlRun')]
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
    for path in paths:
        assert sha(path)==proof['pins'][str(path)]
    start=round((proof['events'][-1]['seconds']+1)*48000)
    count=5*48000
    samples=[]
    for path in paths:
        with wave.open(str(path)) as w:
            assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(48000,1,2)
            assert start+count<=w.getnframes()
            w.setpos(start)
            values=np.frombuffer(w.readframes(count),dtype='<i2').astype(np.int32)
            assert len(values)==count
            samples.append(values)
    delta=samples[0]-samples[1]
    report=dict(nativeRun=proof['nativeRun'],controlRun=proof['controlRun'],
                scope='Fixed five-second window one second after final recorded cluck command',
                startSample=start,samples=count,rate=48000,
                maxAbsoluteDifference=int(np.max(np.abs(delta))),
                rmsDifference=float(np.sqrt(np.mean(delta.astype(float)**2))),
                nativeRMS=float(np.sqrt(np.mean(samples[0].astype(float)**2))),
                identicalPCM=bool(np.array_equal(*samples)),
                individualTailsVerified=False,wholeMixVerified=False,releaseReady=False,
                pins={str(p):sha(p) for p in [*paths,evidence,Path(__file__),PORT/'chicken_evidence_names.py']})
    output='DCS_CHICKEN_CURRENT'+('_MIRROR' if mirror else '')+'_CONVERGENCE.json'
    (PORT/'generated_dcs'/output).write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--mirror'])
    print(json.dumps(inspect(bool(sys.argv[1:])),indent=2))
