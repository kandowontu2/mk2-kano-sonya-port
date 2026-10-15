"""Qualify the same terminal RAM capture with its actual initial Square clip.

First-load source_num=-1 does not imply an empty native sample pointer. Use
the complete independently retained48kHz Square source and actual precise
sample position at the first callback, not waveform/time/gain fitting. Keep
6395's failed idle-channel gate and every captured field and sample intact.
"""
import inspect,json,struct,subprocess,wave
from pathlib import Path
import numpy as np
import capture_current_cpu_ring_mirror_audio_v6394 as original
import current_tomb_winner_mix_fault_model_v5789 as mix
ROOT,need,sha=original.ROOT,original.need,original.sha
CASE=original.OUT
OUT=ROOT/'audit_v6397_current_cpu_ring_mirror_audio_ram_checked'
ASSET=ROOT/'samples/mk2ks/sonya_square_launch.wav'


def square_context(text,headers,pins):
 proof=json.loads((ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json').read_text())
 need(proof['passed'] and sha(ASSET)==proof['inputHashes'][str(ASSET)],'Whole previously source-qualified original Square clip unchanged')
 pins[str(ASSET)]=sha(ASSET)
 with wave.open(str(ASSET),'rb')as file:
  need((file.getnchannels(),file.getsampwidth(),file.getframerate(),file.getnframes())==(1,2,48000,45512),
       'Entire original mono48kHz45512sample Square source')
  values=np.frombuffer(file.readframes(file.getnframes()),dtype='<i2').copy()
 precise=[r for r in mix.rows(text,'MK2_TOMB_MIX_CHANNEL')if r['channel']=='12']
 need(len(precise)==len(headers) and precise[0]['seconds']==headers[0]['seconds'], 'Complete actual physical CPU channel12 callback clock')
 first=float(precise[0]['position'])
 need(first.is_integer() and 0<first<45512,'Actual whole initial48kHz source position, not a fitted waveform alignment')
 start=mix.sample_clock(headers[0]['seconds'],True)-int(first)
 for row,head in zip(precise,headers,strict=True):
  count=min(45512,max(0,mix.sample_clock(head['seconds'],True)-start))
  need(row['sample']=='4294967295' and row['length']=='45512' and row['frame']==head['frame'] and row['seconds']==head['seconds'] and
       row['bits']==struct.pack('<d',float(count)).hex().upper() and float(row['position'])==count and
       row['loop']==row['paused']==row['writes']=='0' and row['assistance']=='none',
       'Every first-load Square source position/EOF bit and complete actual callback clock')
 need(float(precise[-1]['position'])==45512,'Actual Square voice reaches original source EOF')
 source=ROOT/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 driver=ROOT/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 device=ROOT/'mame-mkp/src/devices/sound/samples.cpp'
 need(all(sha(p)==proof['inputHashes'][str(p)]for p in(source,driver,device)),'Whole previously qualified compiled route and sample-device first-load arithmetic unchanged')
 for p in(source,driver,device,ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json'):pins[str(p)]=sha(p)
 # All video states are also complete; use the immediately preceding source
 # sound callback as original sample state, not the later callback or a clock fit.
 from bisect import bisect_right
 from decimal import Decimal
 clocks=[Decimal(h['seconds'])for h in headers]
 for row in mix.rows(text,'MK2_MAUDIO_CHANNEL'):
  if row['channel']!='12':continue
  index=bisect_right(clocks,Decimal(row['seconds']))-1
  need(index>=0,'First actual video state follows a retained source callback')
  count=min(45512,max(0,mix.sample_clock(headers[index]['seconds'],True)-start))
  need(row['sample']=='4294967295' and row['length']=='45512' and row['pos']==format(float(count),'.8f') and
       row['loop']==row['paused']==row['writes']=='0','Every original Square video position through finite retained EOF')
 return values,start,dict(sourceFrames=45512,sourceFrequency=48000,channel=12,actualInitialPosition=int(first),
                          sourceStartStreamIndex=start,actualFirstLoadSourceNum=4294967295,preciseStates=len(precise),
                          actualCompleteClipEOF=45512,noWaveformFitOrTimingSearch=True)


def state(text,guest):
 source=inspect.getsource(original.state)
 before="if row['channel']!='0':need(row['length']=='0' and float(row['pos'])==0,'No unmodeled imported source')"
 need(source.count(before)==1,'Only already separately source-qualified initial Square channel differs')
 source=source.replace(before,"if row['channel']not in('0','12'):need(row['length']=='0' and float(row['pos'])==0,'All other native sample channels untouched')",1)
 scope=dict(original.state.__globals__)
 exec(compile(source,__file__+'::entire_original_mirror_state_with_full_Square_clock_gate','exec'),scope)
 return scope['state'](text,'sonya',2,guest)


def predict(chunks,headers,pcm,text,pins,values,start):
 source=inspect.getsource(mix.predict_mix)
 changes={
  'def predict_mix(chunks,headers,pcm,text,fighter,pins):':'def predict(chunks,headers,pcm,text,fighter,pins,square_values,square_start):',
  'voice=np.zeros_like(dcs);callback_states=[];first_offset=None':
  "voice=np.zeros_like(dcs);square=np.zeros_like(dcs);square_sample,_=sample_values(square_values,48000);callback_states=[];first_offset=None",
  'mixed=np.float32(dcs+voice)':
  "for index,head in enumerate(headers):\n  tick=int(Decimal(head['seconds'])*50)\n  mixer_start=(tick-1)*960*(ATTO//48000)\n  sec,fraction=divmod(mixer_start,ATTO);view=sec*48000+fraction//PERIOD\n  at=np.arange(view,view+960,dtype=np.int64)-square_start\n  valid=(at>=0)&(at<len(square_sample))\n  segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(square_sample[at[valid]]*gain)\n  square[index*960:(index+1)*960,0]=segment;square[index*960:(index+1)*960,1]=segment\n voice=np.float32(voice+square)\n mixed=np.float32(dcs+voice)",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Retain entire original DAC/source-winner/float32 mixer; add actual Square source only')
  source=source.replace(before,after,1)
 scope=dict(mix.__dict__)
 exec(compile(source,__file__+'::whole_native_float32_mix_plus_source_clocked_Square','exec'),scope)
 result=scope['predict'](chunks,headers,pcm,text,'sonya',pins,values,start)
 result['completeSourceModelSHA256']=mix.hashlib.sha256(source.encode()).hexdigest().upper()
 return result


def finish(carrier):
 need(not OUT.exists() and not original.prior.process_tools.census(),'Fresh host qualification; native process is terminal, never rerun')
 terminal=json.loads((CASE/'native_terminal.json').read_text());failure=json.loads((CASE/'failure.json').read_text())
 need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors'] and not failure['passed'] and
      failure['error']=="ValueError('No unmodeled imported source')",'Preserve actual same native terminal and failed initial idle-channel assumption')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'Complete actual executed current inputs unchanged')
 text=carrier['text'];headers=carrier['pcm_headers'];guest=carrier['guest']
 values,start,square=square_context(text,headers,pins);native=state(text,guest)
 gate,fault,gate_sha=original.prior.original.dac_models(len(headers))
 dac=gate(carrier['dac_chunks'],carrier['dac_headers'],headers);dac_faults=fault(carrier['dac_chunks'],carrier['dac_headers'],headers)
 pcm=np.frombuffer(b''.join(carrier['pcm_chunks']),dtype='<i2').reshape(-1,2)
 waveform=predict(carrier['dac_chunks'],carrier['dac_headers'],pcm,text,pins,values,start)
 need(waveform['passed'],'Entire actual full mirror mixed PCM, source-clocked initial Square plus Sonya winner, no trimming/fits')
 rg,rf=original.prior.original.model.rom_models(carrier['expected'])
 rom=[rg(bytes(carrier['rom'][p]),p)for p in carrier['rom']]
 rom_faults=[f for p in carrier['rom']for f in rf(bytes(carrier['rom'][p]),p)]
 for p in(CASE/'native_terminal.json',CASE/'run.log.gz',CASE/'failure.json',Path(__file__),Path(original.__file__)):
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All immutable source/capture bytes unchanged after retained-RAM host qualification')
 result=dict(passed=True,candidate=original.prior.original.current.NAME,nativeTerminal=terminal,sourceWinnerMixAccepted=True,
             nativeDCSWaveformAccepted=True,samplesEnabled=True,wholeNativeMirrorPhase=native,initialSquareSource=square,
             sourceDACGateSHA256=gate_sha,dacProof=dac,dacFaultsRejected=dac_faults,wholeOriginalSoundROM=rom,
             originalSoundROMFaultsRejected=rom_faults,pcmHeaders=headers,dacHeaders=carrier['dac_headers'],inputHashes=pins,
             completeStereoFrames=waveform['comparedStereoFrames'],preservedOriginalFailure=str(CASE/'failure.json'),
             sourceClockBoundaryNotObservedLaunchMarker=True,remaining=carrier['remaining'],goalStatus='active',
             newNativeBoots=0,newBuilds=0,newRawMedia=0,fullPortAcceptance=False)
 OUT.mkdir();original.prior.original.save(OUT/'waveform.json',waveform);original.prior.original.save(OUT/'report.json',result)
 for p in OUT.iterdir():
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Whole logical retained proof losslessly compressed')
 print(json.dumps(dict(passed=True,completeStereoFrames=waveform['comparedStereoFrames'],completeSoundCallbacks=len(headers),sourceSquare=square)),flush=True)
 return result
