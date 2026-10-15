# Derived from preserved v5740; repairs numeric-literal spacing only.
"""Actual complete current final-KO/own-ending/300attract native audio.

Whole cold reference chronology, true typed slots, every14-channel field,
every PCM/DAC callback, complete loaded sound ROM, source-exact102-byte packet
helper, full16-bit port words and every real ADSP read are mandatory. No
paired-off fixture, source-clock fit, trimmed waveform or fake audio writes.
"""
import argparse,gzip,hashlib,json,re,struct,traceback
from decimal import Decimal
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_current_ending_audio_v5736 as capture
ROOT,need,sha=current.ROOT,current.need,current.sha


def rows(text,prefix):
 result=[]
 for line in text.splitlines():
  if line.startswith(prefix+' '):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);fields=dict(pairs)
   need(len(pairs)==len(fields),'Every actual native sound row has unique fields')
   result.append(fields)
 return result


def phase_gate(text,reference,meta,live,fighter,side,guest,stock,expected_sound):
 identity=17 if fighter=='kano'else 18;other=3-side
 ignore=('MK2_EAUDIO_','MK2_NATIVE_DAC_','MK2_NATIVE_DCS_ROM_','Average speed: ')
 native=lambda t:[l for l in t.splitlines()if not l.startswith(ignore)]
 need(native(text)==native(reference),'Every actual cold guest/selection/ladder/combat/boss/own-ending/RGB event unchanged')
 own=lambda tag:rows(reference,'MK2_NAT_CAMPAIGN_'+tag)
 starts,ends,stops=map(own,('ENDING_START','ENDING_COMPLETED','RESULT'))
 need(len(starts)==len(ends)==len(stops)==1,'One actual qualified native own ending and ordinary terminal')
 origin,attract,terminal=map(lambda r:int(r['frame']),(starts[0],ends[0],stops[0]))
 zeros=[r for r in own('HEALTH')if r['slot']==str(other)and r['after']=='0'and int(r['frame'])<origin]
 final=max(zeros,key=lambda r:int(r['frame']));window=int(final['frame'])
 audio=lambda tag:rows(text,'MK2_EAUDIO_'+tag)
 def one(tag):
  found=audio(tag);need(len(found)==1,'One complete actual native audio '+tag);return found[0]
 w,b,e,end=(one(tag)for tag in ('WINDOW','BEGIN','ATTRACT','RESULT'))
 need(w['frame']==w['window']==str(window)and w['pc']=='FF836700'and
  w['at']==('010602F0'if other==1 else'01060EC0')and w['mask']=='FFFF'and
  int(w['before'])>0 and w['after']=='0'and w['identity']==str(identity)and
  w['own_boss_winner_reads']=='1'and all(w[k]==final[k]for k in ('before','after','pc','at','a8','a13')),
  'Actual original final boss collision/typed opponent/task/register provenance, never supplied victory or window')
 need(b['frame']==b['origin']==str(origin)and b['identity']==b['roster']==str(identity)and
  b['winner']==str(side)and b['health']==starts[0]['health']and
  b['actors']==starts[0]['actors']=='00000000,00000000',
  'Actual true own native winner and both retired actors exactly at qualified ending admission')
 need(e['frame']==str(attract)and e['origin']==str(origin)and int(e['age'])==attract-origin and
  e['mode']==ends[0]['mode']=='11'and e['roster']==ends[0]['roster']and
  end['frame']==str(terminal)and end['window']==str(window)and end['origin']==str(origin)and
  end['attract']==str(attract)and terminal==attract+300,
  'Complete native final-KO/ending/300realattract scope and ordinary terminal, not deadline success')
 fields=audio('FIELD');channels=audio('CHANNEL')
 need([int(r['frame'])for r in fields]==list(range(window+1,terminal+1)),
  'Every consecutive native final-KO/ending/attract field through original stop')
 pairs={(r['frame'],r['channel'])for r in channels}
 need(len(channels)==len(pairs)==len(fields)*14 and
  pairs=={(r['frame'],str(n))for r in fields for n in range(14)},
  'All fourteen actual channel states in every field, no duplicates, gaps or missing tails')
 need(all(int(r['sample'])==0xffffffff and r['loop']==r['paused']=='0'for r in channels),
  'No imported voice, loop or paused stale character channel persists after final native KO')
 for tag in ('WINDOW','BEGIN','WINNER','ATTRACT','FIELD','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','CHANNEL','RESULT'):
  need(all(r['writes']=='0'and r['assistance']=='none'for r in audio(tag)),
   'Every observed actual audio state/event strictly passive '+tag)
 winners=audio('WINNER')
 need(len(winners)==2 and all(r['entry']==f'{0xfffef800+identity*32:08X}'and
  r['pc']=='FF8296B0'and r['identity']==str(identity)and r['winner']==str(side)and r['mask']=='FFFF'
  for r in winners),'Both original own final boss winner table reads, bound to real identity/physical side')
 pcm=audio('PCM_DIGEST');dac=rows(text,'MK2_NATIVE_DAC_RAM_DIGEST')
 rom=rows(text,'MK2_NATIVE_DCS_ROM_DIGEST')
 need(pcm==live['pcmHeaders']and dac==live['dacHeaders']and rom==live['soundROMHeaders']and
  len(pcm)==len(dac)==meta['actualEndingPCMCallbacks']==meta['actualEndingDACCallbacks']and
  sum(int(r['bytes'])for r in pcm)==meta['actualEndingPCMBytes']and all(r['bytes']=='3840'for r in pcm),
  'Every full actual PCM/DAC/ROM decoder export binds the unaltered native transport log')
 need(pcm and Decimal('0')<=Decimal(pcm[0]['seconds'])-Decimal(w['seconds'])<Decimal('.02000001')and
  Decimal('0')<=Decimal(end['seconds'])-Decimal(pcm[-1]['seconds'])<Decimal('.02000001')and
  all(Decimal(y['seconds'])-Decimal(x['seconds'])==Decimal('.02')for x,y in zip(pcm,pcm[1:])),
  'Entire original50Hz stereo clock covers actual final KO through terminal, no omitted first or final update')
 need(len(rom)==meta['actualSoundROMChunks']==384 and
  all(r['phase']==phase and r['frame']==str(1 if phase=='startup'else terminal)and
   r['offset']==str(offset)and r['bytes']=='65536'and r['size']=='12582912'and
   r['sha256']==hashlib.sha256(expected_sound[offset:offset+65536]).hexdigest().upper()
   for phase in ('startup','terminal')for offset,r in zip(range(0,0xc00000,65536),
    [r for r in rom if r['phase']==phase],strict=True)),
  'Both whole actual sound-ROM source checkpoints, every firmware/data/erased lane/mirror byte digest')
 waveform=live['waveform'];dacproof=live['actualNativeDACSourceProof']
 need(live['passed']and waveform['passed']and waveform['differentChannelSamples']==0 and
  waveform['comparedStereoFrames']==len(pcm)*960 and waveform['predictedSHA256']==waveform['actualSHA256']and
  len(waveform['actualCallbackSourceClocks'])==len(pcm)and len(waveform['effectiveActualWholeWaveformFaults'])==4 and
  dacproof['passed']and dacproof['callbacks']==len(dac)and len(live['actualDACFaultsRejected'])==4 and
  len(live['actualWholeSoundROMProof'])==2 and len(live['actualSoundROMFaultsRejected'])==8,
  'Actual entire source-clock waveform, normalization, ring and real DAC/PCM/whole-ROM faults, not metadata-only sound acceptance')
 # The entire original102-byte helper, including shifts, FF00 ADDI words,
 # both absolute stores and busy-wait loops, remains independently exact.
 lo=(0xffa13ba0-0xff800000)//8;hi=(0xffa13ed0-0xff800000)//8
 need(guest[lo:hi]==stock[lo:hi]and hashlib.sha256(stock[lo:hi]).hexdigest().upper()==
  'E8BC3F411CC055D75D2FE50C65912240FC8E9C81F6C71B96529F11EB6C666BDB',
  'Complete original native packet byte-split/port-prefix/destination/handshake program, not arbitrary unchanged ROM')
 packets,sounds,deliveries=map(audio,('PACKET','SOUND','DELIVERY'))
 need(packets and len(sounds)==len(deliveries)==2*len(packets),
  'Every full actual native packet has both high/low stores and both actual ADSP reads')
 for i,packet in enumerate(packets):
  stores=sounds[2*i:2*i+2];word=int(packet['a3'],16)
  need(packet['entry']=='FFA13BA0'and word<=0xffff and
   [int(r['word'],16)for r in stores]==[0xff00|(word>>8),0xff00|(word&255)]and
   [r['pc']for r in stores]==['FFA13C90','FFA13D60']and all(r['mask']=='FFFF'and
    r['a8']==packet['a8']and r['a13']==packet['a13']for r in stores)and
   Decimal(packet['seconds'])<=Decimal(stores[0]['seconds'])<Decimal(stores[1]['seconds'])and
   (i==len(packets)-1 or Decimal(stores[1]['seconds'])<Decimal(packets[i+1]['seconds'])),
   'Entire actual16-bit original packet, native typed sender/task, high/low FF00 prefixes and operation order')
  for j,write in enumerate(stores):
   delivery=deliveries[2*i+j];nextwrite=sounds[2*i+j+1]if 2*i+j+1<len(sounds)else end
   need(0x3400<=int(delivery['at'],16)<=0x37ff and delivery['mask']=='FFFF'and
    int(delivery['word'],16)==int(write['word'],16)&255 and
    delivery['dsp_pc']==('03A1'if j==0 else'03A8')and
    Decimal(write['seconds'])<=Decimal(delivery['seconds'])<Decimal(nextwrite['seconds']),
    'Every actual original DCS input-latch byte read by real high/low firmware handlers before following store')
 need(not any('hex='in l for l in text.splitlines()),'No raw guest/PCM/DAC/ROM/raster persisted')
 return dict(passed=True,fighter=fighter,physicalSlot=side,identity=identity,window=window,ending=origin,
  attract=attract,terminal=terminal,consecutiveNativeFields=len(fields),actualChannelStates=len(channels),
  actualPCMCallbacks=len(pcm),actualDACCallbacks=len(dac),exactStereoPCMFrames=waveform['comparedStereoFrames'],
  actualFullWaveformSHA256=waveform['actualSHA256'],actualCompletePackets=len(packets),
  actualFull16BitPortStores=len(sounds),actualNativeADSPReads=len(deliveries),wholeSoundROMCheckpoints=2,
  noPostKOVoiceLoopOrStaleCharacterChannels=True,actualEntireNativeSourceClockAudioAccepted=True,
  independentStockEndingChoreographyWaveformAccepted=False,allEndingAudioContextsAccepted=False,fullPortAcceptance=False)


def run(fighter,side):
 folder=ROOT/f'audit_v5739_{fighter}_p{side}_ending_audio'
 need((folder/'audio_live_source_model.json').exists(),'Await actual native full RAM sound-model terminal, never accept or restart on observation timeout')
 meta=json.loads((folder/'result.json').read_text());live=json.loads((folder/'audio_live_source_model.json').read_text())
 need(meta['passed']and meta['nativeExit']==0 and live['passed']and (folder/'stderr.log').read_text()=='',
  'Actual completed error-free current native+RAM source model, no discarded mismatch')
 need(meta['candidate']==current.NAME and meta['executableSHA256']==current.EXE_SHA and meta['guestSHA256']==current.GUEST_SHA,
  'Same actual current compiled character-state/gameplay binary and independently expected initialized guest')
 prepath=capture.source.OUT/'report.json';pre=json.loads(prepath.read_text())
 need(pre['passed']and all(sha(p)==h for p,h in pre['inputHashes'].items())and
  all(sha(p)==h for p,h in meta['inputHashes'].items()),'Every whole qualified observer/model/controller/game/source input retained')
 baseline=ROOT/(f'audit_v5231_{fighter}_corrected_p1_campaign'if side==1 else
  'audit_v5622_current_kano_p2_campaign'if fighter=='kano'else'audit_v5689_verified_subzero_sonya_p2_campaign')
 with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
 with gzip.open(baseline/'run.log.gz','rt')as reader:reference=reader.read()
 pins=dict(meta['inputHashes']);expected,_=capture.model.expected_region(pins)
 guest=current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 positive=phase_gate(text,reference,meta,live,fighter,side,guest,stock,expected);faults=[]
 def reject(label,bad):
  need(bad!=text,'Actual nonvacuous sound-window fault '+label)
  try:phase_gate(bad,reference,meta,live,fighter,side,guest,stock,expected)
  except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual altered complete sound window admitted '+label)
  need(phase_gate(text,reference,meta,live,fighter,side,guest,stock,expected)==positive,
   'Same actual entire native positive restored after every audio fault')
 def mutate(tag,key,value):
  line=next(l for l in text.splitlines()if l.startswith(tag+' '))
  changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and changed!=line,'Actual sound record/key mutation');return text.replace(line,changed,1)
 for tag,key,value,label in [
  ('MK2_EAUDIO_WINDOW','pc','FFF00000','wrong native final collision PC'),
  ('MK2_EAUDIO_WINDOW','before','0','missing actual health collision'),
  ('MK2_EAUDIO_BEGIN','identity','0','wrong true character ending'),
  ('MK2_EAUDIO_ATTRACT','roster','0,17','wrong native attract return'),
  ('MK2_EAUDIO_CHANNEL','sample','7','stale active character sound'),
  ('MK2_EAUDIO_PCM_DIGEST','sha256','0'*64,'corrupted actual PCM buffer digest'),
  ('MK2_NATIVE_DAC_RAM_DIGEST','current_out','0','corrupted actual native DAC cursor'),
  ('MK2_EAUDIO_PACKET','a3','00000001','wrong actual original packet word'),
  ('MK2_EAUDIO_SOUND','word','0001','missing FF00 full-word port prefix')]:
  reject(label,mutate(tag,key,value))
 for tag,label in [('MK2_EAUDIO_FIELD','missing actual consecutive field'),
  ('MK2_EAUDIO_CHANNEL','missing actual channel state'),('MK2_EAUDIO_PCM_DIGEST','missing actual PCM update'),
  ('MK2_NATIVE_DCS_ROM_DIGEST','missing original loaded sound-ROM chunk'),
  ('MK2_EAUDIO_DELIVERY','missing actual native ADSP read')]:
  line=next(l for l in text.splitlines()if l.startswith(tag+' '));reject(label,text.replace(line+'\n','',1))
 line=next(l for l in text.splitlines()if l.startswith('MK2_EAUDIO_CHANNEL '))
 reject('duplicate actual channel record',text.replace(line,line+'\n'+line,1))
 reject('duplicate actual sound key',text.replace(line,line+' writes=0',1))
 positive['actualAudioWindowFaultsRejected']=faults
 need(len(faults)==16,'Every actual full state/channel/buffer/ROM/packet/port/ADSP omission/corruption/duplicate fault rejected')
 for p in [Path(__file__),prepath,ROOT/'mk2/mk2-maincpu.bin',baseline/'run.log.gz',*folder.rglob('*')]:
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every complete actual source/native/model/phase/fault input byte intact')
 positive.update(inputHashes=pins,capture=str(folder),rawPCMGuestROMRGBFilesWritten=0,newBuilds=0,
  publicPlayableChanged=False,allEndingAudioAccepted=False)
 return positive


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 out=ROOT/f'audit_v5743_{args.fighter}_p{args.side}_ending_audio_window_checked'
 need(not out.exists(),'Fresh immutable complete audio phase/packet qualification')
 need((ROOT/f'audit_v5739_{args.fighter}_p{args.side}_ending_audio/audio_live_source_model.json').exists(),
  'Native source waveform still pending; do not convert a wait into failed acceptance')
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualAudioWindowFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
