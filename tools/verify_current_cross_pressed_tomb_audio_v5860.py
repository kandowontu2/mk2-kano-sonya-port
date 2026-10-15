"""Current opposite-character pressed Tomb: entire native audio and input gates.
Whole5795 source/window/channel/voice/packet/fault suites retained, with actual
cross victims and whole5774 cross cue producers. Exact enabled RAM source mixing
is accepted; a paired NOSAMPLES cross capture and broader full art are not.
"""
import gzip,hashlib,inspect,json,re,struct,traceback
from types import SimpleNamespace
from decimal import Decimal
from pathlib import Path
import run_current_cross_pressed_tomb_audio_v5856 as observed
import verify_current_tomb_cue_sources_v5774 as original_cues
import verify_current_cross_tomb_audio_v5842 as previous_cross_cues
import bisect
import current_cross_pressed_tomb_state_v5855 as branches
ROOT,need,sha=observed.ROOT,observed.need,observed.sha
OUT=ROOT/'audit_v5861_current_cross_pressed_tomb_enabled_audio_checked'


def inventory(text):
 result={}
 for line in text.splitlines():
  need('hex='not in line,'No raw native/guest/audio/ROM persisted')
  if not line.startswith('MK2_'):continue
  tag=line.split(' ',1)[0];pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs)
  need(len(r)==len(pairs),'Every actual native state/audio/ROM/DAC row has unique keys')
  result.setdefault(tag,[]).append(r)
 return result


def channel_gate(records,pcm,live,fighter):
 model=observed.model;waveform=live['waveform'];values,frequency=model.read_winner(fighter,{})
 sample,positions=model.sample_values(values,frequency);endpoint=positions[-1]
 source=2 if fighter=='kano'else 3;marker=waveform['sourceMarker']
 start=model.sample_clock(marker['seconds'],True)
 need(start==waveform['sourceStartStreamIndex'],'Actual marker and original ceil-before-start stream index')
 precise=records.get('MK2_TOMB_MIX_CHANNEL',[]);times=[Decimal(r['seconds'])for r in pcm]
 need(len(precise)==14*len(pcm)and
  {(int(r['index']),int(r['channel']))for r in precise}=={(i,n)for i in range(1,len(pcm)+1)for n in range(14)},
  'All14 precise states at every actual sound callback, no missing or duplicate state')
 def state(clock,channel):
  if channel:return 0xffffffff,0,0.0
  if Decimal(clock)<Decimal(marker['seconds']):return 0xffffffff,32000,endpoint
  previous=bisect.bisect_right(times,Decimal(clock))-1
  end=model.sample_clock(pcm[previous]['seconds'],True)if previous>=0 else start
  count=max(0,min(len(positions),end-start))
  return (source if count<len(positions)else 0xffffffff),32000,(positions[count-1]if count else 0.0)
 active=[]
 for r in precise:
  index=int(r['index']);channel=int(r['channel']);head=pcm[index-1]
  need(r['frame']==head['frame']and r['seconds']==head['seconds']and r['writes']=='0'and
   r['assistance']=='none','Exact real sound-callback source clock/provenance')
  number,length,position=state(r['seconds'],channel)
  need(int(r['sample'])==number and int(r['length'])==length and
   r['bits']==struct.pack('<d',position).hex().upper()and float(r['position'])==position and
   r['loop']==r['paused']=='0','Every original repeated-double position bit, correct native clip, finite tail and all other channels idle')
  if channel==0 and number!=0xffffffff:active.append(index)
 for r in records['MK2_MAUDIO_CHANNEL']:
  number,length,position=state(r['seconds'],int(r['channel']))
  need(int(r['sample'])==number and int(r['length'])==length and r['pos']==format(position,'.8f')and
   r['loop']==r['paused']=='0','Every video channel state matches native start/sample clock/retirement')
 need(active and active==list(range(active[0],active[-1]+1))and len(active)==100 and
  all(r['sample']=='4294967295'for r in precise if int(r['index'])>active[-1]),
  'One finite100callback winner playback and complete idle tail through original terminal')
 need(not records.get('MK2_TOMB_MIX_ITEM',[])and not records.get('MK2_TOMB_MIX_GAIN',[]),
  'Optional gain-name query emitted no items; saved gain state coverage is not claimed')
 return dict(passed=True,preciseSourceChannelStates=len(precise),
  videoChannelStates=len(records['MK2_MAUDIO_CHANNEL']),sourceWinnerSample=source,
  firstActiveCallback=active[0],lastActiveCallback=active[-1],consecutiveActiveCallbacks=100,
  sourceOutputSamples=len(sample),endingPosition=endpoint,allRepeatedDoublePositionBitsExact=True,
  allOtherChannelsIdle=True,fullNativeRetirementAccepted=True,actualSavedGainSnapshotsAvailable=False,
  compiledEffectiveGainSourceQualifiedAndWaveformExact=True)


def make_cross_cues():
 fn,_=previous_cross_cues.cue_models()
 body=observed.once(fn.source,"branch='unpressed native RNG drop'if pressed else'held'",
  "branch='pressed physical both-Down'if pressed else'held'")
 namespace=dict(vars(original_cues))
 exec(compile(body,__file__+'::whole5774_actual_cross_pressed_cues','exec'),namespace)
 gate_fn=namespace['gate'];gate_fn.source=body
 exec(compile(inspect.getsource(original_cues.faults),__file__+'::whole5774_actual_cross_cue_faults','exec'),namespace)
 return SimpleNamespace(gate=gate_fn,faults=namespace['faults'],__file__=original_cues.__file__)

cues=make_cross_cues()

def input_faults(text,guest,fighter,side):
 positive=branches.qualify_pressed_drop(text,fighter,side,1,'positive',guest)
 origin=positive['actualBothDownBranchFrame']-positive['actualNativeCeilingArrivalOffset']
 lines=text.splitlines();variants=[]
 row=next(l for l in lines if l.startswith('MK2_STAGE_INPUT ')and
  'frame='+str(origin+32)+' 'in l and 'button=Down'in l)
 variants.append(('actual Down input omitted',text.replace(row+'\n','',1)))
 variants.append(('actual Down input duplicated',text.replace(row,row+'\n'+row,1)))
 row=next(l for l in lines if l.startswith('MK2_STAGE_DROP_INPUT '))
 variants.append(('actual physical drop callback omitted',text.replace(row+'\n','',1)))
 for label,prefix,key,value in [
  ('actual physical pressed count corrupted','MK2_STAGE_DROP_INPUT ','pressed_fields','0'),
  ('actual terminal physical count corrupted','MK2_STAGE_DROP_RESULT ','pressed_fields','31'),
  ('actual victim writer substituted with performer','MK2_STAGE_PROVENANCE_MOTION ','id',str(17 if fighter=='kano'else 18)),
  ('actual native NOT operand corrupted','MK2_STAGE_PROVENANCE_BRANCH ','a0','00000000')]:
  row=next(l for l in lines if l.startswith(prefix)and
   (prefix!='MK2_STAGE_PROVENANCE_MOTION 'or 'pc=FF83CD20'in l)and
   (prefix!='MK2_STAGE_PROVENANCE_BRANCH 'or 'entry=FF8EB1B0'in l))
  altered,n=re.subn(r'\b'+key+r'=[^\s]+',key+'='+value,row,count=1)
  need(n==1 and altered!=row,'Effective actual pressed-input/task/NOT mutation')
  variants.append((label,text.replace(row,altered,1)))
 result=[]
 for label,bad in variants:
  need(bad!=text,'Actual native input counterexample is nonvacuous')
  try:branches.qualify_pressed_drop(bad,fighter,side,1,'positive',guest)
  except Exception as error:result.append(dict(label=label,rejectedBy=str(error)))
  else:raise ValueError('Actual pressed input/source corruption admitted '+label)
  need(branches.qualify_pressed_drop(text,fighter,side,1,'positive',guest)==positive,
   'Whole original positive restored after each real physical input fault')
 need(len(result)==7,'All seven original physical-input/victim/NOT counterexamples rejected')
 return result


def gate(text,meta,live,fighter,side,guest,stock,expected_sound):
 identity=17 if fighter=='kano'else 18;victim_identity=18 if fighter=='kano'else 17;other=3-side;records=inventory(text)
 get=lambda tag:records.get(tag,[])
 audio=lambda tag:get('MK2_MAUDIO_'+tag)
 def one(tag):
  rs=audio(tag);need(len(rs)==1,'One actual full Tomb native audio '+tag);return rs[0]
 begin,end=one('BEGIN'),one('RESULT');origin=int(begin['origin']);terminal=int(end['frame'])
 native=observed.pressed.check_log(text,fighter,side,1,guest=guest)
 need(native==live['nativeEarnedTombState']and native['passed']and native['earned_matches']==2 and
  native['consecutive_fields']==801 and native['action_frame']==origin and
  begin['frame']==str(origin)and begin['id']==str(identity)and end['origin']==str(origin)and
  terminal==origin+1101 and end['raw_audio_files']=='0',
  'Entire real current cold two-full-health earned matches, true IDs/action/801cleanup and original1101terminal')
 phase=branches.qualify_pressed_drop(text,fighter,side,1,'positive',guest)
 need(phase==live['sourceQualifiedNativePressedBranch']and phase['passed']and
  phase['nativeRNGNotInvokedForThisBranch']and phase['actualPhysicalDownFields']==32 and
  phase['trueVictim']==victim_identity and len(live['actualPressedSourceWriterFaultsRejected'])==6,
  'Entire real original both-Down/drop/269motion/landing/retirement branch, no held or forced RNG substitute')
 fields=get('MK2_STAGE_FIELD');first=fields[0]
 need(begin['a8']==first['own']and begin['a13']==first['main']and first['id']==str(identity)and
  first['victim_id']==str(victim_identity),'Native audio admission owns actual performer actor/Main, not proxy')
 channels=audio('CHANNEL');pairs={(r['frame'],r['channel'])for r in channels}
 need(len(channels)==len(pairs)==14*1100 and pairs=={(str(f),str(n))for f in range(origin+1,origin+1101)for n in range(14)},
  'Every14 actual video channel state through full1100fields, no missing or duplicate observations')
 for tag in ('BEGIN','RESULT','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','CHANNEL'):
  need(all(r['writes']=='0'and r['assistance']=='none'for r in audio(tag)),
   'Every actual native sound admission/state/event passive '+tag)
 pcm=get('MK2_BBAUDIO_PCM_DIGEST');dac=get('MK2_NATIVE_DAC_RAM_DIGEST');rom=get('MK2_NATIVE_DCS_ROM_DIGEST')
 need(pcm==live['pcmHeaders']and dac==live['dacHeaders']and rom==live['soundROMHeaders']and
  len(pcm)==len(dac)==meta['mixedPCMUpdates']and all(r['bytes']=='3840'for r in pcm)and
  sum(int(r['bytes'])for r in pcm)==meta['mixedPCMBytesVerifiedInRAM'],
  'Every full actual native PCM/DAC/ROM export binds unaltered real transport')
 need(int(pcm[0]['frame'])in(origin,origin+1)and int(pcm[-1]['frame'])in(origin+1099,origin+1100)and
  Decimal('0')<=Decimal(pcm[0]['seconds'])-Decimal(begin['seconds'])<Decimal('.02000001')and
  Decimal('0')<=Decimal(end['seconds'])-Decimal(pcm[-1]['seconds'])<Decimal('.02000001')and
  all(Decimal(b['seconds'])-Decimal(a['seconds'])==Decimal('.02')for a,b in zip(pcm,pcm[1:])),
  'Complete original50Hz sound clock from genuine stage admission through original terminal, no trimmed first/last/tail')
 waveform=live['waveform']
 need(live['passed']and live['samplesEnabled']and waveform['passed']and
  waveform['differentChannelSamples']==0 and waveform['actualSHA256']==waveform['predictedSHA256']==meta['mixedPCMSHA256']and
  waveform['comparedStereoFrames']==len(pcm)*960 and len(waveform['actualCallbackSourceClocks'])==len(pcm)and
  len(waveform['expectedWinnerCallbackStates'])==len(pcm)and
  waveform['sourceWinnerFrequency']==16000 and waveform['sourceWinnerLength']==32000 and
  waveform['sourceOutputSamples']==96001 and waveform['sourceFloat32CompositeGain']==0.21000000834465027 and
  waveform['sourceSelectedWinnerSample']==(2 if identity==17 else 3)and waveform['maximumMixedMagnitude']<1 and
  live['actualNativeDACSourceProof']['passed']and live['actualNativeDACSourceProof']['callbacks']==len(dac)and
  len(live['actualDACFaultsRejected'])==4 and len(live['actualSoundROMFaultsRejected'])==8,
  'Whole native unquantized resampler/cache plus original winner interpolation/float gains and complete actual mixed stereo output; real DAC/ROM faults retained, no fit or clipping')
 winner=channel_gate(records,pcm,live,fighter)
 need(live['importedWinnerMixedWaveformAccepted']and live['actualMixedRawPCMByteFaultSuiteAccepted']and
  waveform['actualMixedRawPCMByteFaultSuiteAccepted']and len(waveform['actualRawMixedPCMFaultsRejected'])==4 and
  len(waveform['actualMixedSourceOperationFaultsRejected'])==4 and
  all(r['differentChannelSamples']>0 for r in waveform['actualMixedSourceOperationFaultsRejected'])and
  all(r.get('differentChannelSamples',1)>0 for r in waveform['actualRawMixedPCMFaultsRejected']),
  'Entire actual RAM mixed equality; four actual raw-byte/shape and four whole source-operation faults effective, positive fully restored')
 need(len(rom)==384 and all(r['phase']==phase and r['frame']==str(1 if phase=='startup'else terminal)and
  r['offset']==str(offset)and r['bytes']=='65536'and r['size']=='12582912'and
  r['sha256']==hashlib.sha256(expected_sound[offset:offset+65536]).hexdigest().upper()
  for phase in ('startup','terminal')for offset,r in zip(range(0,0xc00000,65536),
   [q for q in rom if q['phase']==phase],strict=True)),
  'Both whole actual loaded original sound-ROM checkpoints, every firmware/data/lane/mirror byte')
 # Entire original victim predecessor/Tomb/initial-impact/voice/fall/retire
 # program, including actual literal cue callers, is unchanged in current.
 off=lambda a:(a-0xff800000)//8
 need(guest[off(0xff8ea000):off(0xff8eb490)]==stock[off(0xff8ea000):off(0xff8eb490)],
  'Every original Tomb predecessor/victim/effect/packed-voice/branch instruction byte')
 need(guest[off(0xffa13ba0):off(0xffa13ed0)]==stock[off(0xffa13ba0):off(0xffa13ed0)]and
  hashlib.sha256(stock[off(0xffa13ba0):off(0xffa13ed0)]).hexdigest().upper()==
  'E8BC3F411CC055D75D2FE50C65912240FC8E9C81F6C71B96529F11EB6C666BDB',
  'Entire original102byte packet split/FF00prefix/absolute-port/handshake program')
 # The genuine Sonya female extension is the already qualified current
 # selector, not a fabricated role range or Liu-specific sound proxy.
 need(guest[off(0xffa12220):off(0xffa12430)]==bytes.fromhex(
  '02b5f001420bfbff14ca420bfaff11ca80c00002ffff420bfeff08caa2b52000420bfeff01ca0125012d05c00126012d02c00127012d5f0de0ea80ff2014204010c0'),
  'Whole source-qualified native female extension/Main-role/packed-byte/RNG dispatch program')
 routes=audio('ROUTE');victim,main=first['victim'],first['victim_main']
 for caller,command in [('FF8EAA30',0x1b),('FF8EAEA0',0x44)]:
  rs=[r for r in routes if r['return_pc']==caller]
  need(len(rs)==1 and rs[0]['entry']=='FFA12530'and int(rs[0]['a0'],16)==command and
   rs[0]['a8']==rs[0]['owner']==victim and rs[0]['a13']==main and rs[0]['id']==str(victim_identity),
   'Actual original literal Tomb cue caller owns true victim/Main '+caller)
 voice=[r for r in routes if r['return_pc']=='FF8EAED0']
 entries=['FFA12220','FFA123B0'if victim_identity==18 else'FFA122D0','FFA123D0','FFA12530']
 base=0xb7 if victim_identity==18 else 0x85;role=18 if victim_identity==18 else other
 need([r['entry']for r in voice]==entries and all(r['a8']==r['owner']==victim and
  r['a13']==main and r['id']==str(victim_identity)for r in voice)and
  all(Decimal(a['seconds'])<Decimal(b['seconds'])for a,b in zip(voice,voice[1:]))and
  voice[0]['a0']==voice[1]['a0']=='00000001'and voice[0]['a1']==voice[1]['a1']=='8585B8B7'and
  int(voice[1]['a2'],16)==victim_identity and int(voice[2]['a2'],16)==int(voice[3]['a2'],16)==role and
  int(voice[2]['a1'],16)==int(voice[3]['a1'],16)==int(voice[3]['a0'],16)==base,
  'Actual complete original one-variant ceiling voice, correct physical Main role or true female extension, never Liu proxy')
 vg,_=observed.voice_models()
 screams=[r for r in routes if r['entry']=='FFA11FD0']
 need(len(screams)==1,'One actual native falling victim scream')
 late=vg(text,fighter,side,guest,screams[0])
 need(late==live['sourceQualifiedNativeLateVictimVoice']and late['passed']and
  len(live['actualLateVictimVoiceFaultsRejected'])==8 and len(live['actualPressedPhaseFaultsRejected'])==4,
  'Whole late victim Main-role/female/source-RNG/caller chain and genuine drop motion/voice faults')
 packets=audio('PACKET');all_sounds=audio('SOUND');sounds=[r for r in all_sounds if r['pc']in('FFA13C90','FFA13D60')]
 delivery=audio('DELIVERY');markers=[r for r in all_sounds if r['pc']=='FFFB7140']
 need(len(markers)==1 and markers[0]['word']==('FFFE'if identity==17 else'FFFD')and markers[0]['mask']=='FFFF'and
  len(all_sounds)==len(sounds)+1 and packets and len(sounds)==len(delivery)==2*len(packets),
  'Every actual native sound write accounted, with one true winner marker and both port/ADSP bytes per packet')
 for i,p in enumerate(packets):
  stores=sounds[2*i:2*i+2];word=int(p['a3'],16)
  need(p['entry']=='FFA13BA0'and 0<=word<=0xffff and
   [int(r['word'],16)for r in stores]==[0xff00|(word>>8),0xff00|(word&255)]and
   [r['pc']for r in stores]==['FFA13C90','FFA13D60']and all(r['mask']=='FFFF'and
    r['a8']==p['a8']and r['a13']==p['a13']for r in stores)and
   Decimal(p['seconds'])<=Decimal(stores[0]['seconds'])<Decimal(stores[1]['seconds'])and
   (i+1==len(packets)or Decimal(stores[1]['seconds'])<Decimal(packets[i+1]['seconds'])),
   'Full actual native packet bytes/prefixes/source-PC/actor/task operation chronology')
  for j,write in enumerate(stores):
   d=delivery[2*i+j];later=sounds[2*i+j+1]if 2*i+j+1<len(sounds)else end
   need(0x3400<=int(d['at'],16)<=0x37ff and d['mask']=='FFFF'and
    int(d['word'],16)==int(write['word'],16)&255 and d['dsp_pc']==('03A1'if j==0 else'03A8')and
    Decimal(write['seconds'])<=Decimal(d['seconds'])<Decimal(later['seconds']),
    'Every full native DCS byte actually read by original high/low firmware before following write')
 return dict(passed=True,fighter=fighter,physicalSlot=side,identity=identity,victimIdentity=victim_identity,origin=origin,terminal=terminal,
  completeNativeEarnedContract=native,sourceQualifiedNativeBranch=phase,
  actualChannelStates=len(channels),actualPCMCallbacks=len(pcm),actualDACCallbacks=len(dac),
  exactStereoPCMFrames=waveform['comparedStereoFrames'],actualWholePCMSHA256=waveform['actualSHA256'],
  actualCompletePackets=len(packets),actualFull16BitPortStores=len(sounds),actualNativeADSPReads=len(delivery),
  actualTrueWinnerMarkers=1,sourceSelectedInitialVictimVoice=base,actualVictimRole=role,
  actualCurrentPressedTombEnabledWaveformVoiceClockAndCleanupAccepted=True,
  samplesEnabled=True,importedWinnerMixedWaveformAccepted=True,actualWinnerChannelClockAndRetirement=winner,
  actualSavedGainSnapshotsAvailable=False,actualMixedRawPCMByteFaultSuiteAccepted=True,
  dropLateVictimVoiceAccepted=True,fullStageArtAccepted=False,completeStageVictimAudioAccepted=False,
  fullPortAcceptance=False)


def run():
 need(not OUT.exists(),'Fresh immutable actual current Tomb sound matrix')
 guest=observed.current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();pins={};cases=[]
 prepath=observed.source.OUT/'report.json';pre=json.loads(prepath.read_text())
 prior=json.loads((observed.source.held.previous.OUT/'report.json').read_text())
 fn,digest=observed.collector()
 need(pre['passed']and prior['passed']and len(prior['actualSourceFaultsRejected'])==8 and
  pre['transportSourceSHA256']==digest and fn.__globals__['model']is observed.model and
  fn.__globals__['state']is observed.pressed and pre['wholeEarnedPressedContractSHA256']==observed.pressed.CONTRACT_SHA256,
  'Whole enabled passive source preflight, retained eight original observer faults and actual bound mixed model')
 for p,h in pre['inputHashes'].items():need(sha(p)==h,'Whole qualified source intact');pins[p]=h
 for side in (1,2):
  for fighter in ('kano','sonya'):
   folder=ROOT/f'audit_v5859_current_cross_pressed_tomb_winner_mix_{fighter}_p{side}_samples'
   meta=json.loads((folder/'result.json').read_text());live=json.loads((folder/'audio_live_source_model.json').read_text())
   process=json.loads((folder/'process.json').read_text())
   need(meta['exit_code']==0 and meta['candidate']==observed.current.NAME and meta['samples_enabled']and
    meta['fighter']==fighter and meta['side']==side and meta['executable_sha256']==observed.current.EXE_SHA and
    meta['payload_sha256']==observed.current.PAYLOAD_SHA and meta['guestSHA256']==observed.current.GUEST_SHA and
    meta['guest_writes']==0 and meta['assistance']=='none'and meta['rawAudioRasterVRAMROMCopiesWritten']==0 and
    (folder/'stderr.log').read_text()==''and '-samples'in process['command']and '-nosamples'not in process['command']and '-nocheat'in process['command']and
    process['command'][0]==str(ROOT/observed.current.NAME/'mkport_candidate.exe'),
    'Actual complete current true-ID native terminal and declared DCS-only command, not samples-enabled audio acceptance')
   for p,h in meta['input_hashes'].items():need(sha(p)==h,'Actual executed full input retained');pins[p]=h
   expected,_=observed.model.expected_region(pins)
   with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
   # No cross NOSAMPLES duplicate is claimed. All real native DAC samples
   # and complete enabled stereo output have an independent whole source
   # prediction, including actual omitted-winner/raw-first/raw-last faults.
   need(live['waveform']['actualMixedRawPCMByteFaultSuiteAccepted']and
    live['waveform']['actualMixedSourceOperationFaultsRejected'][0]['differentChannelSamples']>0,
    'Actual winner contributes to the entire exact source waveform; no fabricated mirror baseline parity')
   positive=gate(text,meta,live,fighter,side,guest,stock,expected);faults=[]
   def reject(label,bad,bad_guest=guest):
    need(bad!=text or bad_guest!=guest,'Nonvacuous actual full Tomb sound counterexample')
    try:gate(bad,meta,live,fighter,side,bad_guest,stock,expected)
    except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
    else:raise ValueError('Actual corrupted full Tomb sound admitted '+label)
    need(gate(text,meta,live,fighter,side,guest,stock,expected)==positive,'Whole actual positive restored after every Tomb fault')
   def change(tag,key,value,where=''):
    line=next(l for l in text.splitlines()if l.startswith(tag+' ')and where in l)
    bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
    need(n==1 and bad!=line,'Actual row/key mutation');return text.replace(line,bad,1)
   for tag,key,value,label,where in [
    ('MK2_MAUDIO_BEGIN','id','0','wrong actual true performer',''),
    ('MK2_MAUDIO_CHANNEL','sample','7','stale imported channel in declared DCS-only mix',''),
    ('MK2_BBAUDIO_PCM_DIGEST','sha256','0'*64,'corrupted actual full PCM digest',''),
    ('MK2_NATIVE_DAC_RAM_DIGEST','current_out','65535','corrupted actual native DAC cursor',''),
    ('MK2_MAUDIO_PACKET','a3','00010000','wrong actual full packet word',''),
    ('MK2_MAUDIO_SOUND','word','0000','missing actual FF00 prefix','pc=FFA13C90'),
    ('MK2_MAUDIO_ROUTE','a0','00000000','wrong original victim voice selector','return_pc=FF8EAED0'),
    ('MK2_MAUDIO_ROUTE','owner','00000000','wrong native victim voice owner','return_pc=FF8EAED0'),
    ('MK2_MAUDIO_SOUND','word','FFFC','wrong native own winner marker','pc=FFFB7140')]:
    reject(label,change(tag,key,value,where))
   for tag,label in [('MK2_MAUDIO_CHANNEL','missing actual channel state'),
    ('MK2_BBAUDIO_PCM_DIGEST','missing actual sound callback'),('MK2_NATIVE_DCS_ROM_DIGEST','missing loaded sound-ROM chunk'),
    ('MK2_MAUDIO_DELIVERY','missing actual ADSP read')]:
    line=next(l for l in text.splitlines()if l.startswith(tag+' '));reject(label,text.replace(line+'\n','',1))
   line=next(l for l in text.splitlines()if l.startswith('MK2_MAUDIO_CHANNEL '))
   reject('duplicate actual channel',text.replace(line,line+'\n'+line,1))
   reject('duplicate actual native key',text.replace(line,line+' writes=0',1))
   for address,label in [(0xff8ea000,'original whole Tomb predecessor code'),(0xff8ea9e0,'original Tomb effect caller'),
    (0xffa12220,'native gender/Main selector'),(0xffa13ba0,'original full packet helper')]:
    bad=bytearray(guest);bad[(address-0xff800000)//8]^=1;reject(label,text,bytes(bad))
   for tag,key,value,label,where in [
    ('MK2_TOMB_MIX_CHANNEL','position','0','exact channel position corrupted','channel=0 '),
    ('MK2_TOMB_MIX_CHANNEL','bits','0000000000000000','exact double bits corrupted','channel=0 '),
    ('MK2_TOMB_MIX_CHANNEL','sample','0','wrong winner sample','channel=0 '),
    ('MK2_TOMB_MIX_CHANNEL','length','31999','winner length changed','channel=0 '),
    ('MK2_TOMB_MIX_CHANNEL','loop','1','winner clip loops','channel=0 '),
    ('MK2_TOMB_MIX_CHANNEL','paused','1','winner clip paused','channel=0 '),
    ('MK2_TOMB_MIX_CHANNEL','sample','7','foreign imported channel active','channel=1 '),
    ('MK2_TOMB_MIX_CHANNEL','index','0','wrong callback source index','channel=0 '),
    ('MK2_TOMB_MIX_CHANNEL','seconds','0','wrong real source clock','channel=0 ')]:
    reject(label,change(tag,key,value,where))
   line=next(l for l in text.splitlines()if l.startswith('MK2_TOMB_MIX_CHANNEL '))
   reject('missing precise channel state',text.replace(line+'\n','',1))
   reject('duplicate precise channel state',text.replace(line,line+'\n'+line,1))
   reject('duplicate precise native key',text.replace(line,line+' writes=0',1))
   need(len(faults)==31 and len(live['actualEarnedStateFaultsRejected'])==12,
    'All31 actual native audio/window/channel faults and all original12 earned faults retained')
   cue=cues.gate(text,guest,stock,fighter,side,True)
   need(cue['passed']and cue['actualGeneralCalls']==12 and len(cues.faults(text,guest,stock,fighter,side,True))==25,
    'Every original general cue producer and emitted slot word preserved under enabled mixing')
   positive.update(actualAudioSourceWindowFaultsRejected=faults,actualGeneralCueSourceProof=cue,
    actualNativeBranchFaultsRejected=branches.pressed_phase_faults(text,fighter,side,guest),capture=str(folder),
    actualPressedSourceWriterFaultsRejected=branches.source_faults(text,guest,fighter,side),
    actualPhysicalInputFaultsRejected=input_faults(text,guest,fighter,side))
   _,vf=observed.voice_models()
   positive['actualLateVictimVoiceFaultsRejected']=vf(text,fighter,side,guest)
   need(len(positive['actualNativeBranchFaultsRejected'])==4 and len(positive['actualLateVictimVoiceFaultsRejected'])==8 and
    len(positive['actualPressedSourceWriterFaultsRejected'])==6 and len(positive['actualPhysicalInputFaultsRejected'])==7 and
    positive['actualPressedSourceWriterFaultsRejected']==live['actualPressedSourceWriterFaultsRejected'],
    'All original real pressed269phase and eight native-role/female voice faults retained')
   need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in folder.rglob('*')if p.is_file()),
    'No raw native/guest/raster/audio/ROM or extra build/release copies')
   for p in folder.rglob('*'):
    if p.is_file():pins[str(p.resolve())]=sha(p)
   cases.append(positive)
 for p in (Path(__file__),Path(branches.__file__),Path(previous_cross_cues.__file__),Path(original_cues.__file__),prepath,ROOT/'mk2/mk2-maincpu.bin'):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every actual full native/source/model/state/window evidence byte intact')
 return dict(passed=True,candidate=observed.current.NAME,cases=cases,inputHashes=pins,
  actualCurrentBothCharactersBothSidesCrossPressedTombEnabledWinnerMixAccepted=True,
  exactStereoPCMFrames=sum(c['exactStereoPCMFrames']for c in cases),
  actualSourceAudioFaultsRejected=124,actualEarnedStateFaultsRejected=48,actualBranchFaultsRejected=16,
  actualPressedSourceWriterFaultsRejected=24,actualPhysicalInputFaultsRejected=28,pairedNOSAMPLESRunAccepted=False,
  samplesEnabled=True,importedWinnerMixedWaveformAccepted=True,dropLateVictimVoiceAccepted=True,
  actualRawMixedPCMFaultsRejected=16,actualMixedSourceOperationFaultsRejected=16,actualLateVictimVoiceFaultsRejected=32,
  actualSavedGainSnapshotsAvailable=False,actualMixedRawPCMByteFaultSuiteAccepted=True,
  fullStageArtAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False,
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,publicPlayableChanged=False)


if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual complete Tomb matrix');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
