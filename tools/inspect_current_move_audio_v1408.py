"""Source-bound real-input PCM/command inventory, not complete audio fidelity.

Nonzero music is never accepted as evidence of a move effect. Keep every native
port command in the special interval, including genuinely empty intervals.
"""
import json,re,wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve,resample_poly
import verify_ring_native_lookup_v1342 as current
import verify_human_special_matrix as human

ROOT=current.ROOT;OUT=ROOT/'audit_v1408_current_move_audio_checked'

def need(test,message):
 if not test:raise ValueError(message)

def records(log,tag):
 return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.splitlines() if line.startswith(tag+' ')]

def pcm(path):
 with wave.open(str(path),'rb') as wav:
  channels,width,rate,n=wav.getnchannels(),wav.getsampwidth(),wav.getframerate(),wav.getnframes()
  need(width==2,'Expected actual 16-bit PCM')
  data=np.frombuffer(wav.readframes(n),'<i2').reshape(n,channels).astype(np.float64)
 return rate,channels,data

def voice(mix,rate,path,seconds):
 voice_rate,channels,donor=pcm(path);need(channels==1 and rate%voice_rate==0,'Source voice format')
 recorded=resample_poly(mix.mean(axis=1),1,rate//voice_rate)
 donor=donor[:,0];radius=.04
 start=max(0,int((seconds-radius)*voice_rate));end=int((seconds+radius)*voice_rate)
 region=recorded[start:end+len(donor)]
 product=fftconvolve(region,donor[::-1],mode='valid')
 energy=np.r_[0,np.cumsum(region*region)]
 norms=np.sqrt(np.maximum(energy[len(donor):]-energy[:-len(donor)],1e-12)*np.sum(donor*donor))
 fits=product/norms;peak=int(np.argmax(fits));at=(start+peak)/voice_rate
 gain=float(product[peak]/np.sum(donor*donor))
 need(fits[peak]>.8 and abs(at-seconds)<.02,'Own announcement present at its native marker, not arbitrary recording time')
 need(.14<gain<.27,'Announcement level consistent with source .30 channel * .70 speaker route')
 return dict(time=at,markerSeconds=seconds,offsetSeconds=at-seconds,correlation=float(fits[peak]),gain=gain,
             scope='Own source donor audible at genuine selection marker; mix correlation is not an exact DCS waveform oracle')

def verify():
 pins={}
 def pin(path,wanted=None):
  path=Path(path);key=str(path)
  if key not in pins:pins[key]=current.digest(path)
  need(wanted is None or pins[key]==wanted,'Changed executed input '+key)
 compiled_path=ROOT/current.CANDIDATE/'build-info.json';compiled=json.loads(compiled_path.read_text(encoding='utf-8-sig'));pin(compiled_path)
 need(compiled['executable_sha256']=='A050762309CADA040B85214CCA435F10A37DD3AAA98173F2E17D12D70F034159','Current matched candidate')
 pin(ROOT/current.CANDIDATE/'mkport_candidate.exe',compiled['executable_sha256'])
 pin(ROOT/current.CANDIDATE/'roms/mk2ks/mk2ks.mdata',compiled['payload_sha256'])
 for path,h in compiled['input_hashes'].items():pin(path,h)
 source=(ROOT/current.CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
 driver=(ROOT/current.CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp').read_text()
 need('set_volume(0, 0.30f)' in source and '"mk2ksvoice", 0.70' in driver,'Source-bound announcement gain')
 prior_path=ROOT/'audit_v1389_current_human_matrix_checked/report.json';prior=json.loads(prior_path.read_text());pin(prior_path)
 need(prior['passed'] and prior['candidate']==current.CANDIDATE and prior['current52CaseHumanStateMatrixAccepted'],'Current human reference')
 for path,h in prior['inputHashes'].items():pin(path,h)
 observer=(ROOT/'mk2ks_human_special_audio_v1397.lua').read_text()
 need(observer.count("dofile('mk2ks_human_special_matrix_v3.lua')")==1,'Unchanged physical controls')
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',observer),'Read-only observer')
 cases=[]
 for move in human.SPECS:
  for side in (1,2):
   folder=ROOT/f'audit_v1398_human_audio_{move}_p{side}';launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
   before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
   need(launch['exit_code']==0 and launch['candidate']==current.CANDIDATE and launch['move']==move and launch['side']==side and not launch['air'] and launch['victim']=='sub_zero' and not launch['cheats_enabled'] and launch['assistance']=='none','Actual current unassisted audio case')
   need(launch['executable_sha256']==compiled['executable_sha256'] and launch['payload_sha256']==compiled['payload_sha256'],'Matched audio candidate')
   need(before==launch['input_hashes'] and all(before.get(p)==h for p,h in compiled['input_hashes'].items()),'Complete launch manifest')
   for path,h in before.items():
    pin(path,h)
    if Path(path).suffix in('.lua','.json','.ps1'):pin(folder/'input_sources'/Path(path).name,h)
   log=(folder/'run.log').read_text(encoding='utf-8-sig');state=human.verify_log(log,move,side)
   need(not re.search('WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation',log,re.I),'Actual runtime')
   baseline=ROOT/f'audit_v1365_human_{move}_p{side}'
   events=lambda text:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line) for line in text.splitlines() if line.startswith('MK2_HSPECIAL_')]
   need(events(log)==events((baseline/'run.log').read_text(encoding='utf-8-sig')),'Audio tap preserves all native inputs/identity/actions/contact/recovery events')
   images={name:(folder/'snap'/name).read_bytes()==(baseline/'snap'/name).read_bytes() for name in ('special_before.png','special_recovered.png','special_final.png')}
   sounds=records(log,'MK2_HAUDIO_SOUND');end=records(log,'MK2_HAUDIO_RESULT')
   need(len(end)==1 and int(end[0]['frame'])==human.rows(log,'RESULT')[0]['frame'] and end[0]['writes']=='0' and end[0]['assistance']=='none','Actual audio terminal')
   need(all(q['mask']=='FFFF' and q['writes']=='0' and q['assistance']=='none' for q in sounds),'Actual read-only native sound-port observations')
   need(all(float(a['seconds'])<=float(b['seconds']) for a,b in zip(sounds,sounds[1:])),'Actual sound chronology')
   rate,channels,mix=pcm(folder/'game_mix.wav');duration=len(mix)/rate
   need((rate,channels)==(48000,2) and duration>=float(end[0]['seconds'])-.05,'Complete synchronized stereo native mix')
   need(np.count_nonzero(mix)>48000 and np.max(np.abs(mix))<32767,'Non-silent unclipped capture, not move audio acceptance')
   identity=human.SPECS[move][0];fighter='kano' if identity==17 else 'sonya';marker='FFFC' if identity==17 else 'FFFB'
   selections=[q for q in sounds if q['word']==marker and q['pc']=='FFFF3DA0']
   need(len(selections)==1,'One genuine own character selection announcement')
   sample=ROOT/f'samples/mk2ks/{fighter}_select.wav';pin(sample)
   selection=voice(mix,rate,sample,float(selections[0]['seconds']))
   native=[];pending=None
   for q in sounds:
    pc=int(q['pc'],16);word=int(q['word'],16)
    if pc==0xffa13c90:
     need(pending is None and word&0xff00==0xff00,'Native sign-extended high DCS byte');pending=q
    elif pc==0xffa13d60:
     need(pending is not None and word&0xff00==0xff00 and q['frame']==pending['frame'],'Ordered native low DCS byte')
     native.append(dict(frame=int(q['frame']),seconds=float(pending['seconds']),command=f"{((int(pending['word'],16)&255)<<8)|(word&255):04X}",highPC=pending['pc'],lowPC=q['pc']))
     pending=None
   need(pending is None,'No truncated native DCS command')
   entry=state['entry'];recovered=state['recovered']
   interval=[q for q in native if entry<=q['frame']<=recovered]
   gameplay_markers=[q for q in sounds if entry<=int(q['frame'])<=recovered and int(q['pc'],16) not in (0xffa13c90,0xffa13d60)]
   need(not gameplay_markers,'Ordinary moves do not accidentally trigger character-only finisher/voice markers')
   cases.append(dict(case=folder.name,move=move,side=side,nativeState=state,everyCurrentNativeHumanEventMatched=True,
    priorActualScreensByteMatched=images,selectionVoice=selection,PCM=dict(rate=rate,channels=channels,duration=duration,peak=float(np.max(np.abs(mix))),rms=float(np.sqrt(np.mean(mix*mix)))),
    specialSoundCommands=interval,entireNativeCommands=native,silentSpecialInterval=not bool(interval),moveAudioFidelityAccepted=False))
   for path in folder.rglob('*'):
    if path.is_file():pin(path)
 for name in ('tools/inspect_current_move_audio_v1408.py','tools/verify_human_special_matrix.py','mk2ks_human_special_audio_v1397.lua','tools/run_current_human_special_audio_v1397.ps1'):pin(ROOT/name)
 return dict(passed=True,candidate=current.CANDIDATE,cases=cases,inputHashes=pins,selectionDonorAtNativeMarkerAccepted=True,
  physicalAudioTapRegressionAccepted=True,allMoveAudioAccepted=False,fullPortAccepted=False,
  scope='All16 current unassisted human move PCM captures and actual DCS command inventory, own selection waveform/timing/level, exact native input/state regression; not all move sounds, winner voices, CPU, finishers, or full-game audio fidelity')

if __name__=='__main__':
 need(not OUT.exists(),'Never overwrite evidence')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),allMoveAudioAccepted=False,fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),cases=len(report.get('cases',[]))),indent=2),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
