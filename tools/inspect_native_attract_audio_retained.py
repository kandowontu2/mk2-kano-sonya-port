"""Read original compressed speaker evidence; never replay or change audio."""
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
import qualify_native_ai_attract_audio as model
ROOT=model.ROOT
RUN=ROOT/'audit_native_ai_response_attract'

def read():
    report=json.loads((RUN/'native_attract_audio_finite.json').read_text())
    with gzip.open(RUN/'captured_native_audio.pcm.gz','rb') as f:raw=f.read()
    model.need(hashlib.sha256(raw).hexdigest().upper()==report['actualSHA256'] and len(raw)==report['comparedStereoFrames']*4,
               'Exact entire original native speaker evidence')
    with gzip.open(RUN/'run.log.gz','rt',encoding='utf-8') as f:text=f.read()
    records=[]
    for index,header in enumerate(report['wholeCapturedPCMHeaders']):
        block=raw[index*3840:(index+1)*3840]
        model.need(hashlib.sha256(block).hexdigest().upper()==header['sha256'],'Every original callback and full metadata bound')
        records.append(dict(header=header,pixels=block))
    return dict(text=text,pcm=records),report

def main():
    c,report=read()
    expected,actual,events,pins,headers=model.predict(c)
    sections=[];section=[]
    for index,header in enumerate(headers):
        if section and float(header['seconds'])-float(headers[section[-1]]['seconds'])>.021:
            sections.append(section);section=[]
        section.append(index)
    if section:sections.append(section)
    result=[]
    for indices in sections:
        lo,hi=indices[0]*960,(indices[-1]+1)*960
        e,a=expected[lo:hi],actual[lo:hi]
        off=np.all(e==0,axis=1)
        different=np.argwhere(e!=a)
        result.append(dict(first=headers[indices[0]],last=headers[indices[-1]],callbacks=len(indices),
            differentSamples=len(different),firstDifference=lo+int(different[0,0]) if len(different) else None,
            actualNonzeroWhenNamePredictionZero=int(np.count_nonzero(a[off])),
            maxActualWhenNamePredictionZero=int(np.max(np.abs(a[off].astype(np.int32)))) if off.any() else None,
            maximumDifference=int(np.max(np.abs(a.astype(np.int32)-e.astype(np.int32))))))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
