"""Qualify the same naturally terminal RAM capture, never replay or edit it.

Finite genuine incoming-hit/recovery/source-output proof. No all-arena,
KO/reset/morph, full raster or release acceptance is inferred.
"""
import inspect,json,re,subprocess
from pathlib import Path
import launch_interruption_model_v6689 as model
import qualify_kano_launch_audio_v6656 as source_audio
import verify_current_tomb_winner_mix_v5785 as native_packets
ROOT,need,sha=model.ROOT,model.need,model.sha


def packet_gate(text):
 source=inspect.getsource(native_packets.gate)
 first=source.index(" packets=audio('PACKET');");last=source.index(' return dict(passed=True,',first)
 source=source[first:last]
 before="""need(len(markers)==1 and markers[0]['word']==('FFFE'if identity==17 else'FFFD')and markers[0]['mask']=='FFFF'and
  len(all_sounds)==len(sounds)+1 and packets and len(sounds)==len(delivery)==2*len(packets),
  'Every actual native sound write accounted, with one true winner marker and both port/ADSP bytes per packet')"""
 after="""launches=[r for r in all_sounds if r['word']in('6B00','6B01','6B02','6B03')]
 need(not markers and len(launches)in(2,4)and all(r['mask']=='FFFF'for r in launches)and
  len(all_sounds)==len(sounds)+len(launches)and packets and len(sounds)==len(delivery)==2*len(packets),
  'Every actual native port write accounted: complete startup sources, no winner, both actual ADSP bytes per packet')"""
 need(source.count(before)==1,'Whole original packet chronology; exact finite startup instead of winner inventory')
 source=source.replace(before,after,1)
 code="def gate(text):\n records=native_packets.inventory(text)\n audio=lambda tag:records.get('MK2_MAUDIO_'+tag,[])\n ends=audio('RESULT');need(len(ends)==1,'One actual terminal');end=ends[0]\n"+source+"\n return dict(passed=True,packets=len(packets),portWrites=len(sounds),nativeDSPReads=len(delivery),ownedStartupWrites=len(launches),winnerWrites=len(markers))\n"
 scope=dict(native_packets.gate.__globals__,native_packets=native_packets)
 exec(compile(code,__file__+'::whole_original_packet_ADSP_chronology','exec'),scope)
 return scope['gate'](text)


def inputs(carrier,phase):
 actual=model.rows(carrier['text'],'MK2_INTERRUPT_INPUT');expected=[]
 offset={'ball':79,'square':1,'bicycle':7}[carrier['move']]
 for i,c in enumerate(phase['wholePhysicalAndSourceBodyContract']['cycles'],1):
  common=dict(serial=str(i),slot=str(3-carrier['side']))
  for f in range(c['command']+offset,c['entry']+1):expected.append(dict(common,frame=str(f),button='Down',precrouch='1'))
  for age in range(1,carrier['delay']+9):
   f=c['entry']+age;expected.append(dict(common,frame=str(f),button='Down'))
   if carrier['delay']<=age<carrier['delay']+5:expected.append(dict(common,frame=str(f),button='High_Punch'))
 normalized=[{k:v for k,v in r.items()if k not in('seconds','writes','assistance')}for r in actual]
 need(normalized==expected and all(r['writes']=='0'and r['assistance']=='none'for r in actual),
      'Every complete actual opponent controller operation matches the executed pre-crouch and five-field HP route')
 io=model.rows(carrier['text'],'MK2_INTERRUPT_IO')
 need(io and all(r['at']=='01D00000'and r['mask']=='FFFF'and r['writes']=='0'and r['assistance']=='none'for r in io),
      'Actual native input reads retained; source bit-level isolation is not inferred from controller logs')
 return dict(passed=True,physicalOpponentOperations=len(actual),actualNativePortReads=len(io),forcedGuestWrites=0,fullInputBitIsolationAccepted=False)


def qualify(carrier):
 out=ROOT/f"audit_v6692_launch_interruption_checked_{carrier['move']}_p{carrier['side']}_delay{carrier['delay']}"
 need(not out.exists(),'Fresh immutable same-run qualification')
 terminal=json.loads((carrier['folder']/'native_terminal.json').read_text())
 need(terminal==carrier['terminal']and terminal['nativeExit']==0 and not terminal['hostDecodeErrors']and not carrier['decodeErrors'],
      'Same actual native job naturally terminal, no observation expiry')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'Every actually executed input intact')
 phase=model.phase(carrier);physical_inputs=inputs(carrier,phase);waveform=model.predict(carrier,pins)
 need(waveform['passed']and waveform['differentChannelSamples']==0,'Every complete output sample equals native source prediction')
 for event in waveform['sourceEvents']:
  path=event['sourceAsset']
  if event['sample_id']==16:expected=model.current.ASSET_SHA
  else:
   proof=ROOT/('audit_v5379_current_cpu_square_audio_ram_checked'if event['sample_id']==13 else'audit_v5325_current_cpu_bicycle_ram_checked')/'report.json'
   prior=json.loads(proof.read_text());need(prior['passed'],'Original source-qualified Sonya waveform proof')
   expected=prior['inputHashes'][path];pins[str(proof)]=sha(proof)
  need(event['sourceAssetSHA256']==expected==sha(path),'Entire launch asset identical to original source-qualified waveform, not an arbitrary current WAV')
 gate,fault=source_audio.dac_models(len(carrier['pcmHeaders']))
 dac=gate(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders'])
 dac_faults=fault(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders'])
 rg,rf=source_audio.host.models.rom_models(carrier['expectedROM'])
 rom=[rg(bytes(carrier['rom'][p]),p)for p in carrier['rom']]
 rom_faults=[f for p in carrier['rom']for f in rf(bytes(carrier['rom'][p]),p)]
 packet=packet_gate(carrier['text']);faults=[]
 def reject(label,tag,key,value,where,fn):
  line=next(s for s in carrier['text'].splitlines()if s.startswith(tag+' ')and all(f'{k}={v} 'in s+' 'for k,v in where.items()))
  changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and changed!=line,'Actual observed field changed: '+label)
  bad=dict(carrier,text=carrier['text'].replace(line,changed,1))
  try:fn(bad)
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual semantic counterexample admitted '+label)
 for cycle in phase['actualInterruptedCycles']:
  start,hit=cycle['entry'],cycle['hit'];side=carrier['side'];channel=10+2*(side-1)
  for label,tag,key,value,where in [
   ('owner identity before hit','OWNER','id','1',dict(frame=start+1,slot=side)),
   ('health store wrong source PC','HEALTH','pc','FF836710',dict(frame=hit,slot=side)),
   ('uppercut wrong opponent','UPPERCUT','id','17',dict(frame=cycle['uppercutEntry'])),
   ('owner persists after hit','OWNER','actor','01034E90',dict(frame=hit+1,slot=side)),
   ('identity persists after hit','OWNER','id','18',dict(frame=hit+1,slot=side)),
   ('source resumes after hit','CHANNEL','position','1',dict(frame=hit+2,channel=channel)),
   ('interrupted source loops','CHANNEL','loop','1',dict(frame=hit+1,channel=channel)),
   ('interrupted source pauses','CHANNEL','paused','1',dict(frame=hit+1,channel=channel)),
  ]:reject(str(start)+' '+label,'MK2_INTERRUPT_'+tag,key,value,where,model.phase)
 for tag,key,value in [('MK2_MAUDIO_PACKET','a3','FFFFFFFF'),('MK2_MAUDIO_SOUND','word','FF01'),('MK2_MAUDIO_DELIVERY','word','0100')]:
  r=next(r for r in model.rows(carrier['text'],tag)if tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90')
  reject('native packet '+tag,tag,key,value,dict(frame=r['frame']),lambda c:packet_gate(c['text']))
 need(model.phase(carrier)==phase and packet_gate(carrier['text'])==packet,'Full positive restored after actual faults')
 for p in(Path(__file__),Path(model.__file__),ROOT/'tools/launch_interruption_model_v6686.py',Path(source_audio.__file__),Path(native_packets.__file__),
          ROOT/'mame-mkp/src/devices/sound/samples.cpp',ROOT/'mame-mkp/src/emu/sound.cpp',*carrier['folder'].rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Source/evidence unchanged through complete qualification')
 proof=dict(passed=True,candidate=model.current.NAME,nativeTerminal=terminal,physicalAndOwnership=phase,physicalInputs=physical_inputs,
            completeSourceWaveform=waveform,sourceDAC=dac,actualDACFaultsRejected=dac_faults,entireOriginalSoundROM=rom,
            actualSoundROMFaultsRejected=rom_faults,completeNativeSoundDelivery=packet,actualSemanticFaultsRejected=faults,
            inputHashes=pins,newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,rawMediaFilesWritten=0,
            fullFourteenChannelClockAcceptance=False,fullRasterAcceptance=False,fullInterruptionCoverageAccepted=False,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(proof,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,'Lossless proof compression')
 print(json.dumps(dict(passed=True,report=str(path),stereoFrames=waveform['comparedStereoFrames'],actualHits=len(phase['actualInterruptedCycles']),semanticFaults=len(faults))),flush=True)
 return proof
