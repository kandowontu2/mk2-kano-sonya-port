"""Bounded PCM superposition check of three isolated native tracks; diagnostic."""
import hashlib
import json
from pathlib import Path
import wave
import numpy as np

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def digest(path):
    value=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(65536):value.update(block)
    return value.hexdigest().upper()

def main():
    proof_paths=[PORT/'generated_dcs/DCS_CHICKEN_MATCHED_EVENTS.json']
    proof_paths += [PORT/f'generated_dcs/DCS_CHICKEN_TRACK{track}_EVENTS.json' for track in (1,2,3)]
    proofs=[json.loads(path.read_text()) for path in proof_paths]
    reference=proofs[0]['events']
    pins={}
    for proof in proofs:
        assert proof['events']==reference
        for name,value in proof['pins'].items():
            path=Path(name)
            assert digest(path)==value,(path,'stale event evidence')
            pins[name]=value
    control_paths=[BASE/proof['controlRun']/'native_dcs.wav' for proof in proofs]
    assert len({digest(path) for path in control_paths})==1
    paths=[BASE/proofs[0]['nativeRun']/'native_dcs.wav',control_paths[0]]
    paths += [BASE/proof['nativeRun']/'native_dcs.wav' for proof in proofs[1:]]
    handles=[wave.open(str(path)) for path in paths]
    try:
        params=handles[0].getparams()
        assert all(handle.getparams()==params for handle in handles)
        assert (params.framerate,params.nchannels,params.sampwidth)==(48000,1,2)
        begin=int(reference[0]['seconds']*48000)
        end=min(params.nframes,round((reference[-1]['seconds']+1)*48000))
        assert 0<end-begin<48000*15
        for handle in handles:handle.setpos(begin)
        aa=bb=ab=rr=0.;peak=0.;exact=total=0
        for offset in range(begin,end,16384):
            count=min(16384,end-offset)
            blocks=[np.frombuffer(handle.readframes(count),dtype='<i2').astype(np.float64) for handle in handles]
            assert all(len(block)==count for block in blocks)
            actual=blocks[0]-blocks[1]
            model=sum((block-blocks[1] for block in blocks[2:]),np.zeros(count))
            residual=actual-model
            aa+=float(actual@actual);bb+=float(model@model);ab+=float(actual@model)
            rr+=float(residual@residual);peak=max(peak,float(np.max(np.abs(residual))))
            exact+=int(np.count_nonzero(residual==0));total+=count
    finally:
        for handle in handles:handle.close()
    report=dict(scope='Production-minus-muted PCM versus sum of isolated-track-minus-muted PCM',
        nativeRun=proofs[0]['nativeRun'],isolatedRuns=[proof['nativeRun'] for proof in proofs[1:]],
        samples=total,beginSample=begin,endSample=end,chunkSamples=16384,
        fittedParameters=0,correlation=ab/(aa*bb)**.5 if aa and bb else None,
        relativeResidualNorm=(rr/aa)**.5 if aa else None,
        residualRMS=(rr/total)**.5,maxAbsoluteResidual=peak,exactSamples=exact,
        productionAudioAccepted=False,fullPortVerified=False,releaseReady=False,
        limitation='No source-waveform or all-audio certification. Nonlinear mixer/volume effects and PCM rounding may prevent exact superposition.')
    pins[str(Path(__file__))]=digest(Path(__file__))
    for path in proof_paths:pins[str(path)]=digest(path)
    report['pins']=pins
    (PORT/'generated_dcs/DCS_CHICKEN_TRACK_SUM_DIAGNOSTIC.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='pins'},indent=2))

if __name__=='__main__':main()
