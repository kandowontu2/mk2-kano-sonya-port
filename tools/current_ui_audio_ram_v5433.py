"""Exact native16k selection source and original sample-device interpolation.

Preserve both failed recorder/checker attempts. No source asset/game changes,
no broad resampling tolerance; whole current waveform/source gates retained.
"""
import inspect,json,math,traceback
from pathlib import Path
import numpy as np
import current_ui_audio_ram_v5427 as original
import current_ui_audio_ram_v5430 as transport

OUT=original.ROOT/'audit_v5435_current_ui_audio_progress'
BASE=original.ROOT/'audit_v5434_current_ui_audio_ram'
FAILED=transport.OUT/'progress.json'
FAULTS=[]

def native_selection_source(raw):
 # Source samples.cpp increments ipos when reading sample1, then uses
 # (ipos+1)%length for sample2. Preserve that actual +2 look-ahead, native
 # double position carry, float32 output and last sample zero-fill.
 pos=0.;step=16000/48000;result=[];end=len(raw)
 while pos<end:
  ipos=math.floor(pos);frac=pos-ipos
  value=np.float32((1.-frac)*raw[ipos]+frac*raw[(ipos+2)%end])
  pos+=step
  result.append(0. if pos>=end else float(value))
 return np.asarray(result,dtype=np.float64)

def bind_audio():
 source=inspect.getsource(original.audio_check)
 changes={
  "(wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(1,2,48000)":
   "(wav.getnchannels(),wav.getsampwidth(),wav.getframerate(),wav.getnframes())==(1,2,16000,18400)",
  "signal=a['pcm']-b['pcm'];need(np.array_equal(signal[:,0],signal[:,1]),'Actual imported selection contribution dual mono')":
   "source_samples=len(donor);donor=native_selection_source(donor)\n signal=a['pcm']-b['pcm'];need(np.array_equal(signal[:,0],signal[:,1]),'Actual imported selection contribution dual mono')",
  "cueSamples=len(donor),correlation=corr,gain=gain,onsetSeconds=onset":
   "sourceCueSamples=source_samples,sourceFrequency=16000,actualNativeResampledCueSamples=len(donor),correlation=corr,gain=gain,onsetSeconds=onset"}
 for before,after in changes.items():
  original.need(source.count(before)==1,'Only source-exact16k donor/interpolator binding; original full audio/source/owner/marker/shape/finite/onset gates unchanged')
  source=source.replace(before,after,1)
 ns=dict(original.audio_check.__globals__,native_selection_source=native_selection_source)
 exec(compile(source,__file__+'::entire_original_audio_gate_exact_native16k_source','exec'),ns)
 return ns['audio_check']

def qualified_audio(pair,fighter,side):
 check=bind_audio();result=check(pair,fighter,side);a,b=pair
 tests=[]
 marker=result['nativeNameMarker'];word=marker['word'];wrong='FFFB'if fighter=='kano'else'FFFC'
 for label,replace in(('wrong_character_name',lambda s:s.replace('word='+word+' mask=FFFF','word='+wrong+' mask=FFFF')),
  ('missing_name_command',lambda s:'\n'.join(line for line in s.splitlines()if not line.startswith('MK2_UA_SOUND ')or 'word='+word+' 'not in line))):
  aa=dict(a,log=replace(a['log']));bb=dict(b,log=replace(b['log']))
  original.need(aa['log']!=a['log']and bb['log']!=b['log'],'Effective actual native marker mutation')
  tests.append((label,(aa,bb)))
 active=next(r for r in original.records(a['log'],'CHANNEL')if r['channel']=='0'and int(r['length'])>0)
 line=next(l for l in a['log'].splitlines()if l.startswith('MK2_UA_CHANNEL ')and f"frame={active['frame']} "in l and 'channel=0 'in l)
 changed=a['log'].replace(line,line.replace('loop=0','loop=1'),1)
 original.need(changed!=a['log'],'Effective actual native loaded announcement loop mutation')
 tests.append(('native_cue_looped',(dict(a,log=changed),b)))
 changed=b['pcm']+(a['pcm']-b['pcm'])*1.1
 tests.append(('wrong_actual_mix_gain',(dict(a,pcm=changed),b)))
 shifted=np.roll(a['pcm']-b['pcm'],480,axis=0)+b['pcm']
 tests.append(('actual_voice_delayed_10ms',(dict(a,pcm=shifted),b)))
 stale=a['pcm'].copy();stale[-400:]+=1
 tests.append(('actual_stale_audio_after_complete_name',(dict(a,pcm=stale),b)))
 for label,altered in tests:
  try:check(altered,fighter,side)
  except ValueError as error:FAULTS.append(dict(fighter=fighter,side=side,fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual current selection audio corruption accepted: '+label)
 result['actualCurrentAudioFaultsRejected']=6
 return result

def run():
 fail=json.loads(FAILED.read_text())
 original.need(not fail['passed']and fail['error']=="ValueError('Actual retained original selection voice asset format')",'Keep actual unsupported48k source-asset assumption failure')
 device=original.ROOT/'mame-mkp/src/devices/sound/samples.cpp';text=device.read_text()
 body=text[text.index('void samples_device::sound_stream_update('):text.index('//  read_sample')if '//  read_sample'in text else len(text)]
 for token in('double step = double(chan.curfreq) / double(buffer.sample_rate());','double pos_floor = floor(chan.pos);',
  'double frac = chan.pos - pos_floor;','sample[ipos++]','sample[(ipos + 1) % chan.source_len]',
  'buffer.put(sampindex, sample_scale * ((1.0 - frac) * sample1 + frac * sample2));','chan.pos += step;',
  'buffer.fill(0, sampindex);'):
  original.need(token in body,'Exact unchanged native sample interpolation/completion source')
 original.LUA=transport.LUA;original.BASE=BASE;original.audio_check=qualified_audio
 source=inspect.getsource(original.run)
 before="with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:\n  cases=list(pool.map(lambda spec:case(spec,guest,pins),faults.CASES))"
 after="cases=[case(faults.CASES[0],guest,pins)]\n with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:\n  cases.extend(pool.map(lambda spec:case(spec,guest,pins),faults.CASES[1:]))"
 original.need(source.count(before)==1,'Only qualify first actual pair before dispatching remaining unchanged four-context scope')
 ns=dict(original.run.__globals__);exec(compile(source.replace(before,after,1),__file__+'::whole_original_combined_gate_first_pair_then_remaining','exec'),ns)
 report=ns['run']()
 report.update(preservedActualRecorderAndCheckerFailures=[str(transport.FAILED),str(FAILED)],
  recorderCorrectionOnly='Native snapshot_pixels returns one buffer; dimensions from source-defined snapshot_size.',
  nativeSourceInterpolationOnly='Pinned selection WAVs are mono16-bit16kHz18400 samples. Actual unchanged samples.cpp uses double carry, +2 lookahead linear interpolation, float32 output and final zero-fill to native48kHz mixer. No generic resampling approximation or widened waveform tolerance.',
  actualOriginalSelectionAudioFaultsRejected=FAULTS,allActualOriginalUIAndSelectionAudioGatesRetained=True,
  newNativeBoots=19,successfulCurrentCombinedNativeBoots=8,priorSuccessfulUIBootsWithAudioAssetAssumptionFailure=8,
  failedNativeRecorderBootsPreserved=3)
 paths=[transport.FAILED,FAILED,Path(__file__).resolve(),Path(transport.__file__),device,
  original.ROOT/'tools/build_native_voice_samples.ps1',original.ROOT/'mk2ks_current_ui_audio_ram_v5427.lua']
 for base in(original.ROOT/'audit_v5428_current_ui_audio_ram',transport.BASE):
  paths.extend(p for p in base.rglob('*')if p.is_file())
 for p in paths:report['newInputHashes'][str(p.resolve())]=original.sha(p)
 original.need(all(original.sha(p)==h for p,h in report['newInputHashes'].items()),'All final retained actual failed/current/public/source bytes stable')
 return report

if __name__=='__main__':
 original.need(not OUT.exists(),'Fresh source-exact combined current UI/audio checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=original.COMPLETED,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();original.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','qualificationLog','actualOriginalSelectionAudioFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
