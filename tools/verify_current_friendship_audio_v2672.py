"""Current physical Friendships: original complete PCM, cue timing and overlap.

Reconstruct original DCS clips from the isolated hardware references, not from
port output. Current matched physical samples-off controls isolate audible
sample output. Retain v791's <=4-sample timing, .98..1.02 gain, >.9995
correlation and <2 PCM residual gates. This accepts only the captured human
Friendship audio windows, not full scene raster/shadows, other finishers or
the full port. No playable bytes or settings are changed.
"""
import copy,hashlib,json,re,struct,traceback,wave
from pathlib import Path
import numpy as np
import verify_current_friendship_v2655 as scene
import verify_current_friendship_restrictions_v2663 as restrictions
import verify_current_friendship_audio_baselines_v2668 as baselines
import verify_native_friendship_audio_v791 as native
import build_friendship_audio_v774 as oracle

ROOT=scene.ROOT
OUT=ROOT/'audit_v2673_current_friendship_audio_checked'
need=scene.need

def mono_asset(path):
 with wave.open(str(path),'rb')as w:
  need((w.getframerate(),w.getnchannels(),w.getsampwidth())==(48000,1,2),'Unchanged original mono 48k s16 asset format')
  return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)

def original_templates(pin):
 path=ROOT/'audit_v774_original_friendship_audio_checked/verification.json'
 pin(path);proof=json.loads(path.read_text())
 need(proof['all_20_cluck_channel_commands_pcm_identical_within_variant'],'Original five-channel oracle retained')
 for file,wanted in proof['checked_inputs'].items():pin(file,wanted)
 commands=['baseline','006e']+[f'{base+voice:04x}'for base in (0xa5,0xaa,0xaf,0x96)for voice in range(5)]
 baseline=oracle.audio(ROOT/'audit_v772_original_friendship_isolated_baseline/native_mix.wav')
 delivery=None;templates={};assets={}
 for command in commands:
  folder=ROOT/f'audit_v772_original_friendship_isolated_{command}'
  meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  need(meta['exit_code']==0 and meta['command']==command and meta['guest_ram_writes']==0 and meta['assistance']=='DCS_sound_port_only','Actual terminal original hardware-only command capture')
  for file,wanted in meta['input_hashes'].items():pin(file,wanted)
  pin(folder/'native_mix.wav',meta['mix_sha256'])
  for name in ('result.json','run.log'):pin(folder/name)
  if command=='baseline':continue
  log=(folder/'run.log').read_text(encoding='utf-8-sig')
  times=re.findall(r'MK3_FRIEND_ISOLATED_TIME frame=\d+ seconds=([\d.]+) address=01680000 data=([\dA-F]{4}) mask=00FF',log)
  need(len(times)==2 and [int(t[1],16)for t in times]==[int(command,16)>>8,int(command,16)&255],'Original actual hardware command bytes')
  first=float(times[0][0])
  need(abs(float(times[1][0])-first-.000025)<1e-9 and (delivery is None or delivery==first),'Original DCS delivery alignment and byte interval')
  delivery=first
 sound_rom=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
 for address,wanted in ((0xffaa65d0,(0x006e1f21,)*2),(0xffaa6ad0,(0x00a51010,0x00aa1017,0x00af1014,0x00961012))):
  need(struct.unpack_from('<'+'I'*len(wanted),sound_rom,(address-0xff800000)//8)==wanted,'Exact original Friendship sound-table command/hold words')
 for name,cmd in oracle.VARIANTS:
  delta=oracle.audio(ROOT/f'audit_v772_original_friendship_isolated_{cmd:04x}/native_mix.wav')-baseline
  start=round(delivery*48000)
  need(not np.any(delta[:start])and np.array_equal(delta[:,0],delta[:,1]),'Exact original dual-mono delta and hardware latency')
  source=delta[:,0];nz=np.flatnonzero(source)
  need(len(nz)>0 and nz[0]>=start,'Audible original source command')
  end=int(nz[-1])+3;raw=source[start:end];metadata=proof['assets'][name]
  digest=hashlib.sha256(raw.astype('<i2').tobytes()).hexdigest().upper()
  need(metadata['hardware_seconds']==delivery and metadata['command']==cmd and metadata['frames']==len(raw)and metadata['source_pcm_sha256']==digest and metadata['route']==.7,'Reconstructed complete original PCM matches pinned asset metadata')
  asset=ROOT/f'samples/mk2ks/{name}.wav';pin(asset,metadata['sha256']);clip=mono_asset(asset)
  need(len(clip)==len(raw)and np.max(np.abs(clip*.7-raw))<=.350001,'Complete original DCS latency/waveform/tail with reversible .70 route')
  if cmd!=0x6e:
   for voice in range(5):
    other=oracle.audio(ROOT/f'audit_v772_original_friendship_isolated_{cmd+voice:04x}/native_mix.wav')-baseline
    need(np.array_equal(delta,other),'All five actual original native channel variants byte-identical')
  templates[cmd]=clip*.7
  assets[name]=dict(command=cmd,frames=len(raw),sourcePCM_SHA256=digest,maximumRouteRoundingPCM=float(np.max(np.abs(clip*.7-raw))),originalChannels=1 if cmd==0x6e else 5)
 return templates,assets

def reject(call,label,expected):
 try:call()
 except ValueError as error:
  need(any(item in str(error)for item in expected),'Intended audio invariant rejection for '+label+': '+str(error))
  return dict(name=label,rejectedBy=str(error))
 raise ValueError('Specific malformed audio accepted '+label)

def pcm_counterexamples(delta,starts,clips,others,control,templates,fighter):
 # Every mutation targets the first actual audible cue group. The remaining
 # capture and all source/reference files are immutable and untouched.
 outcomes=[]
 attempts=[]
 shifted=list(starts);shifted[0]+=48
 attempts.append(('cue_shifted_48_PCM_samples',delta,shifted,clips,others))
 gain=list(clips);gain[0]=gain[0]*.85
 attempts.append(('wrong_original_loudness',delta,starts,gain,others))
 inverted=list(clips);inverted[0]=-inverted[0]
 attempts.append(('reversed_original_PCM_polarity',delta,starts,inverted,others))
 missing=list(clips);missing[0]=np.zeros_like(missing[0])
 attempts.append(('missing_audible_voice',delta,starts,missing,others))
 cropped=list(clips);cropped[0]=cropped[0].copy()
 nonzero=np.flatnonzero(cropped[0]);at=int(nonzero[len(nonzero)//2]);cropped[0][at:]=0
 need(np.any(clips[0][at:]),'Non-vacuous cropped original audible tail')
 attempts.append(('lost_complete_original_tail',delta,starts,cropped,others))
 wrong=list(clips);wrong[0]=templates[0xa5 if fighter=='kano'else 0x6e]
 attempts.append(('wrong_original_sound_variant',delta,starts,wrong,others))
 if fighter=='sonya':
  collapsed=list(starts);collapsed[1]=collapsed[0]
  need(starts[1]!=starts[0],'Actual distinct overlapping native voice start times')
  attempts.append(('overlapping_voice_restarted_at_first_cue',delta,collapsed,clips,others))
  attempts.append(('third_independent_voice_dropped',delta,starts[:2],clips[:2],others))
 for label,y,s,c,o in attempts:
  outcomes.append(reject(lambda:native.fit_overlap(y,s,c,o),label,('Source waveform gain or voice missing','Wrong waveforms, lost tails or overlapping voice restarted')+(('Friendship samples inaudible',)if label=='missing_audible_voice'else ())))
 need(native.fit_overlap(delta,starts,clips,others)==control,'Final untouched actual audio group after all PCM corruptions')
 return outcomes

def verify():
 pins={};cases={};negatives={};all_variants=set()
 def pin(path,wanted=None):
  path=str(path)
  if path in pins:need(wanted is None or pins[path]==wanted,'Consistent actual audio dependency '+path);return
  actual=scene.launch.sha(path);need(wanted is None or actual==wanted,'Unchanged actual audio dependency '+path);pins[path]=actual
 def proof(path,flag):
  pin(path);record=json.loads(path.read_text())
  need(record['passed']and record[flag]and not record['fullPortAcceptance'],'Actual scoped accepted current proof '+str(path))
  for file,wanted in record['inputHashes'].items():pin(file,wanted)
  return record
 baseline_proof=proof(baselines.OUT/'report.json','samplesSettingNeverChangedGameplay')
 templates,assets=original_templates(pin)
 guest,_,payload=scene.current.expected()
 need((ROOT/scene.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual current payload source reconstruction')
 for fighter in ('kano','sonya'):
  for side in (1,2):
   key=f'{fighter}_p{side}'
   positive=ROOT/f'audit_v2653_current_{fighter}_friendship_p{side}'
   quiet=ROOT/f'audit_v2667_current_{fighter}_friendship_nosamples_p{side}'
   proof(ROOT/f'audit_v2656_current_{fighter}_friendship_p{side}_checked/report.json','currentBuildPhysicalFriendshipAccepted')
   need((positive/'guest_maincpu.bin').read_bytes()==guest==(quiet/'guest_maincpu.bin').read_bytes(),'Whole actual current positive/baseline guest source reconstruction')
   rows=scene.previous.parse(positive/'run.log');quiet_rows=scene.previous.parse(quiet/'run.log')
   baselines.exact(rows,quiet_rows);scene.check(rows,fighter,side)
   need(baseline_proof['cases'][key]['exactNativeSceneRecords']==len(rows),'Whole actually identical current native chronology count')
   chronology=native.runtime(rows,fighter,side,'positive')
   a=native.audio(positive/'native_mix.wav');b=native.audio(quiet/'native_mix.wav')
   need(a.shape==b.shape,'Complete matched current samples-on/off PCM duration')
   delta=a-b;cues=scene.previous.select(rows,'AUDIO');others=[]
   for voice in scene.previous.select(rows,'VOICE'):
    cmd=int(voice['command'],16)
    others.append((round(float(voice['seconds'])*48000),native.existing_sample(ROOT,cmd)))
   groups=[];first_data=None;step=1 if fighter=='kano'else 3
   for first in range(0,len(cues),step):
    group=cues[first:first+step]
    commands=[0x6e if fighter=='kano'else (0xa5,0xaa,0xaf,0x96)[(int(c['command'],16)-0x6aa0)//5]for c in group]
    starts=[round(float(c['seconds'])*48000)for c in group];clips=[templates[cmd]for cmd in commands]
    fit=native.fit_overlap(delta,starts,clips,others)
    groups.append(dict(firstCue=first,commands=commands,startsPCM=starts,**fit));all_variants.update(commands)
    if first_data is None:first_data=(starts,clips,fit)
   pcm=pcm_counterexamples(delta,*first_data[:2],others,first_data[2],templates,fighter)
   changed=copy.deepcopy(rows);audio_index=next(i for i,(tag,row)in enumerate(changed)if tag=='AUDIO')
   changed[audio_index][1]['id']='1'
   timing=[reject(lambda:native.runtime(changed,fighter,side,'positive'),'proxy_audio_owner',('Audio belongs to wrong actor/task',))]
   if fighter=='kano':
    changed=copy.deepcopy(rows);changed[audio_index][1]['frame']=str(int(changed[audio_index][1]['frame'])+1)
    timing.append(reject(lambda:native.runtime(changed,fighter,side,'positive'),'pop_outside_native_burst_phase',('Pop is not at the native burst phase',)))
   else:
    changed=copy.deepcopy(rows);cmd=int(changed[audio_index][1]['command'],16)
    changed[audio_index][1]['command']=f'{cmd+1:04X}'
    timing.append(reject(lambda:native.runtime(changed,fighter,side,'positive'),'not_original_first_free_voice',('Not original first-free independent voice allocation',)))
   need(native.runtime(rows,fighter,side,'positive')==chronology,'Final untouched current native cue/voice chronology')
   cases[key]=dict(**chronology,audibleGroups=groups,PCMCorruptions=pcm,cueCorruptions=timing,finalUnmodifiedControlPassed=True,
    currentTrueID=17 if fighter=='kano'else 18,wholeNativeRecords=len(rows),existingAnnouncementEvents=len(others))
   print(key+': complete original audible waveforms, overlap and specific corruptions passed',flush=True)
   for command_case in ('wrong_command','punch_used'):
    path=ROOT/f'audit_v2664_current_{fighter}_friendship_{command_case}_p{side}_checked/report.json'
    proof(path,'actualPhysicalFriendshipRestrictionAccepted')
    folder=ROOT/f'audit_v2660_current_{fighter}_friendship_{command_case}_p{side}'
    need((folder/'guest_maincpu.bin').read_bytes()==guest,'Current physical negative whole guest unchanged')
    negative_rows=scene.previous.parse(folder/'run.log');restrictions.check(negative_rows,fighter,side,command_case)
    negatives[f'{fighter}_{command_case}_p{side}']=native.runtime(negative_rows,fighter,side,command_case)
 need(all_variants=={0x6e,0xa5,0xaa,0xaf,0x96},'All original Friendship audio variants actually exercised')
 pin(ROOT/'mame-mkp/src/devices/sound/samples.cpp');pin(Path(__file__).resolve());scene.launch.module_pins(pins)
 return dict(passed=True,candidate=scene.current.NAME,originalAssets=assets,cases=cases,physicalRestrictions=negatives,
  audibleCues=sum(case['cues']for case in cases.values()),audibleGroups=sum(len(case['audibleGroups'])for case in cases.values()),
  rejectedSpecificAudioCounterexamples=sum(len(case['PCMCorruptions'])+len(case['cueCorruptions'])for case in cases.values()),
  originalPCMAndAudibleOverlapAccepted=True,currentWholeGuestAndPayloadReconstructed=True,all20OriginalCluckChannelsReconstructed=True,
  inputHashes=pins,gameChanged=False,completeSceneRasterShadowAudioAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Immutable current original-PCM Friendship proof')
 try:r=verify()
 except Exception as error:r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in ('inputHashes','cases','physicalRestrictions','originalAssets')},indent=2),flush=True)
 raise SystemExit(0 if r['passed']else 1)
