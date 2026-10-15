"""Fresh Kano P2 actual PCM diagnosis; no raw PCM or game writes.

Keep the failed3700 gate unchanged. Localize every out-of-model PCM span,
retain exact chronology and source hashes, and attempt its original fit.
"""
import inspect,json,traceback
from pathlib import Path
import numpy as np
import run_natural_mirror_audio_ram_v3700 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v3707_mirror_pcm_gap_diagnosis_checked'
stats={}
original_collector=prior.collector

def collector(fighter):
    source=inspect.getsource(original_collector)
    need(source.count('audit_v3701_')==1,'Exact fresh diagnostic capture name')
    source=source.replace('audit_v3701_','audit_v3706_')
    scope=dict(prior.__dict__);scope['__file__']=__file__
    exec(compile(source,'<fresh_diagnostic_capture_only>','exec'),scope)
    return scope['collector'](fighter)

def diagnose(signal,headers,events):
    start=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000
    starts=[round((float(e['seconds'])-start)*48000)for e in events]
    clips=[prior.existing_sample(ROOT,int(e['word'],16))for e in events]
    allowed=np.zeros(len(signal),bool)
    for at,clip in zip(starts,clips):allowed[at-8:at+len(clip)+8]=True
    positions=np.flatnonzero((signal!=0)&~allowed)
    breaks=np.flatnonzero(np.diff(positions)>1)+1
    spans=np.split(positions,breaks)if len(positions)else[]
    records=[]
    for group in spans:
        first,last=int(group[0]),int(group[-1]);values=signal[group]
        records.append(dict(firstOutputSample=first,lastOutputSample=last,
          firstSeconds=start+first/48000,lastSeconds=start+last/48000,
          nonzeroSamples=len(group),minimum=float(values.min()),maximum=float(values.max())))
    stats.update(cues=[dict(event=e,theoreticalOutputSample=at,completeSourceOutputSamples=len(clip))
      for e,at,clip in zip(events,starts,clips)],capturedOutputSamples=len(signal),
      outsideModelNonzeroSamples=len(positions),outsideModelSpans=records,
      outsideModelMaxAbs=float(np.abs(signal[positions]).max())if len(positions)else 0,
      outsideModelL1=float(np.abs(signal[positions]).sum()),rawAudioFilesWritten=0)
    return original_fit(signal,headers,events)

original_fit=prior.fit_all
prior.collector=collector
prior.fit_all=diagnose
if __name__=='__main__':
    need(not OUT.exists(),'Fresh diagnostic evidence only')
    try:
        case=prior.pair('kano',2)
        report=dict(passed=True,case=case,diagnosis=stats)
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),diagnosis=stats)
    report['inputHashes']={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__).resolve()):sha(prior.__file__)}
    for leaf in('audit_v3706_kano_mirror_audio_p2_samples','audit_v3706_kano_mirror_audio_p2_nosamples'):
        for path in(ROOT/leaf).rglob('*'):
            if path.is_file():report['inputHashes'][str(path)]=sha(path)
    report.update(fullPortAcceptance=False,diagnosisOnly=True)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
