"""Explain missing independent stock comparator without importing collectors."""
import gzip,json,re,collections,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
source=R/'tools/verify_current_ending_audio_window_v5744.py';text=source.read_text()
assert 'independentStockEndingChoreographyWaveformAccepted=False' in text
cases=[];pins={str(source):sha(source)}
for side in (1,2):
 proof=R/f'audit_v5745_sonya_p{side}_ending_audio_window_checked/report.json';d=json.loads(proof.read_text())
 assert d['passed'] and d['actualEntireNativeSourceClockAudioAccepted'] and not d['independentStockEndingChoreographyWaveformAccepted']
 path=R/f'audit_v5739_sonya_p{side}_ending_audio/run.log.gz'
 kinds=collections.Counter();routes=[];packets=[]
 for line in gzip.open(path,'rt'):
  if not line.startswith('MK2_EAUDIO_'):continue
  q=dict(re.findall(r'(\w+)=([^\s]+)',line))
  if not(d['ending']<=int(q.get('frame','-1'))<d['attract']):continue
  tag=line.split()[0].removeprefix('MK2_EAUDIO_');kinds[tag]+=1
  if tag=='ROUTE':routes.append({k:q[k] for k in ['frame','a0','return_pc']})
  if tag=='PACKET':packets.append({k:q[k] for k in ['frame','a3','a8','a13']})
 cases.append(dict(side=side,ownEnding=d['ending'],attractBoundary=d['attract'],actualEndingOnlyTags=dict(kinds),actualEndingOnlyRoutes=routes,actualEndingOnlyPackets=packets,wholeNativeAudioWindowFrames=d['exactStereoPCMFrames']))
 pins[str(proof)]=sha(proof);pins[str(path)]=sha(path)
out=R/'audit_current_ending_choreography_comparator_scope_checked';assert not out.exists();out.mkdir()
report=dict(historicalFullFiniteNativeWaveformsRetained=True,independentStockEndingComparatorAccepted=False,reason='Actual native waveform is independently modeled from observed DAC/clock/source bytes, but no separate stock ending cue schedule or waveform oracle is compared. False flag is explicit scope, not a detected audio mismatch.',cases=cases,nextSafeArtifactOnlyCheck='Compare existing own-ending-only route returnPC/cue/queue/packet ordering with independently decoded original stock routing and caller instruction ranges. Verify current source/loaded ending patch allowlist and add real record faults for wrongcue, omitted/reorderedroute, wrongcaller. Classify source-choreography invariants separately; do not claim independent waveform parity without comparator.',rawPCMNeeded=False,newEmulatorRuns=0,heardMixAccepted=False,fullPortAccepted=False,inputHashes=pins)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(report=str(out/'report.json'),ownEndingRouteCounts=[len(c['actualEndingOnlyRoutes']) for c in cases],wholeNativeWindowFrames=[c['wholeNativeAudioWindowFrames'] for c in cases])))
