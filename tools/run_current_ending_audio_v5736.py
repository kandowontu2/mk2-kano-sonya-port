"""Same qualified cold campaigns; ending PCM/DAC/whole sound ROM stay in RAM."""
import argparse,gzip,inspect,json,re,traceback
from pathlib import Path
import numpy as np
import current_payload_metadata_context_v5229 as current
import run_corrected_p1_campaigns_v5230 as p1
import run_current_kano_p2_campaign_v5621 as kano_p2
import run_verified_subzero_sonya_p2_campaign_v5688 as sonya_p2
import current_ending_audio_model_v5733 as model
import qualify_current_ending_audio_source_v5737 as source
ROOT,need,sha=current.ROOT,current.need,current.sha


def collector(fighter,side):
 need(fighter in ('kano','sonya')and side in(1,2),'Only all four genuine physical character contexts')
 ref=(p1.kano if fighter=='kano'else p1.sonya)if side==1 else(kano_p2 if fighter=='kano'else sonya_p2)
 original=ref if side==1 else ref.original
 code=inspect.getsource(ref.capture)if side==1 else ref.capture_source()
 if side==1:
  before="stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:"
  after="stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict',creationflags=subprocess.CREATE_NO_WINDOW)as process:"
  need(code.count(before)==1,'One hidden native launch only');code=code.replace(before,after,1)
  before="      print('MK2_CURRENT_CAMPAIGN_PREVIEW_DATAURL data:image/png;base64,'+\n       base64.b64encode(preview.getvalue()).decode(),flush=True)"
  need(code.count(before)==1,'One raw preview removed, all RGB RAM comparison retained')
  code=code.replace(before,'      # Actual RGB/preview remain in RAM; only digest printed.',1)
 declared_physical_source=code
 edits=[
  ("pins=dict(build['input_hashes'])","""pins=dict(build['input_hashes'])
 pre=json.loads((source.OUT/'report.json').read_text())
 need(pre['passed']and all(sha(p)==h for p,h in pre['inputHashes'].items()),'Entire ending sound/model/control source qualified before native boot')
 pins[str(source.OUT/'report.json')]=sha(source.OUT/'report.json')
 expected_sound,sound_sources=model.expected_region(pins)
 pcm_chunks=[];pcm_headers=[];dac_chunks=[];dac_headers=[]
 dcs_buffers={'startup':bytearray(),'terminal':bytearray()};dcs_headers=[]"""),
  ("if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):","""if line.startswith(('MK2_EAUDIO_PCM ','MK2_NATIVE_DAC_RAM ','MK2_NATIVE_DCS_ROM ')):
     pairs=re.findall(r'(\\w+)=([^\\s]+)',line);fields=dict(pairs)
     need(len(pairs)==len(fields),'Every full actual audio header has unique keys')
     raw=bytes.fromhex(fields.pop('hex'));need(len(raw)==int(fields['bytes']),'Every actual audio/ROM buffer byte transported in RAM')
     fields['sha256']=model.original_dac.capture.digest(raw)
     if line.startswith('MK2_EAUDIO_PCM '):
      need(fields['bytes']=='3840','Entire50Hz native960-frame stereo PCM update')
      pcm_chunks.append(raw);pcm_headers.append(fields);tag='MK2_EAUDIO_PCM_DIGEST '
     elif line.startswith('MK2_NATIVE_DAC_RAM '):
      dac_chunks.append(raw);dac_headers.append(fields);tag='MK2_NATIVE_DAC_RAM_DIGEST '
     else:
      phase=fields['phase'];need(phase in dcs_buffers and fields['bytes']=='65536'and
       fields['size']=='12582912'and fields['bytewidth']=='2'and fields['bitwidth']=='16'and
       fields['writes']=='0'and fields['assistance']=='none'and int(fields['offset'])==len(dcs_buffers[phase]),
       'Every complete consecutive initialized/terminal original sound-region chunk')
      at=int(fields['offset']);need(raw==expected_sound[at:at+65536],'Every loaded original firmware/data/lane/mirror byte independently exact')
      dcs_buffers[phase].extend(raw);dcs_headers.append(fields);tag='MK2_NATIVE_DCS_ROM_DIGEST '
     log.write(tag+' '.join(k+'='+str(v)for k,v in fields.items())+'\\n')
    elif line.startswith('MK2_CAMPAIGN_GUEST_RAM '):"""),
  ('elapsedSeconds=time.time()-started,rawMediaGuestAudioFilesWritten=0,newBuilds=0',
   "actualEndingPCMCallbacks=len(pcm_headers),actualEndingDACCallbacks=len(dac_headers),actualEndingPCMBytes=sum(map(len,pcm_chunks)),actualSoundROMChunks=len(dcs_headers),\n  elapsedSeconds=time.time()-started,rawMediaGuestAudioFilesWritten=0,newBuilds=0"),
  ('return result','return result,pcm_headers,pcm_chunks,dac_headers,dac_chunks,dcs_headers,dcs_buffers,expected_sound')]
 for before,after in edits:
  need(code.count(before)==1,'Whole canonical cold capture only adds passive audio RAM transport '+before)
  code=code.replace(before,after,1)
 scope=dict(vars(original),__file__=__file__,native=current,
  OUT=ROOT/f'audit_v5739_{fighter}_p{side}_ending_audio',LUA=source.LUA,
  CONTROLLERS=[source.LUA,source.OBSERVER,*ref.CONTROLLERS],source=source,model=model,
  qualify_payload_metadata_warning=p1.metadata_clean,declared_physical_source=declared_physical_source)
 exec(compile(code,__file__+'::whole_current_cold_campaign_passive_audio_RAM','exec'),scope)
 return scope['capture']


def run(fighter,side):
 source.observer_source()
 if side==2:
  if fighter=='kano':kano_p2.boundary.source_boundary()
  else:sonya_p2.source_boundary()
 meta,ph,pc,dh,dc,rh,rb,expected=collector(fighter,side)()
 folder=ROOT/f'audit_v5739_{fighter}_p{side}_ending_audio'
 need(meta['passed']and meta['nativeExit']==0 and len(ph)==len(dh)>2000,
  'Actual complete native ending PCM/DAC transport, no shortened or empty substitute')
 gate,faults=model.dac_models(len(ph));rom_gate,rom_faults=model.rom_models(expected)
 # Every captured final-KO/ending/attract callback is compared. Retain any
 # discrepancy as a real result, never silently trim it or fit a clock/gain.
 waveform=model.predict_waveform(dc,dh,np.frombuffer(b''.join(pc),'<i2').reshape(-1,2))
 report=dict(passed=waveform['passed'],fighter=fighter,physicalSlot=side,capture=str(folder),
  actualNativeDACSourceProof=gate(dc,dh,ph),actualDACFaultsRejected=faults(dc,dh,ph),
  actualWholeSoundROMProof=[rom_gate(bytes(rb[p]),p)for p in ('startup','terminal')],
  actualSoundROMFaultsRejected=[f for p in ('startup','terminal')for f in rom_faults(bytes(rb[p]),p)],
  waveform=waveform,pcmHeaders=ph,dacHeaders=dh,soundROMHeaders=rh,
  independentWindowRouteChannelQualificationPending=True,allEndingAudioAccepted=False,fullPortAcceptance=False,
  rawPCMGuestROMRGBFilesWritten=0,newBuilds=0,inputHashes=meta['inputHashes'])
 path=folder/'audio_live_source_model.json';need(not path.exists(),'Immutable actual full RAM audio/model export')
 path.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','pcmHeaders','dacHeaders','soundROMHeaders','waveform')},indent=2),flush=True)
 print(json.dumps({k:v for k,v in waveform.items()if k!='actualCallbackSourceClocks'},indent=2),flush=True)
 need(report['passed'],'Every actual whole native sound waveform error remains fatal; inspect retained discrepancy')


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  folder=ROOT/f'audit_v5739_{args.fighter}_p{args.side}_ending_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():
   path=folder/'audio_failure.json';need(not path.exists(),'Preserve actual audio failure');path.write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise
