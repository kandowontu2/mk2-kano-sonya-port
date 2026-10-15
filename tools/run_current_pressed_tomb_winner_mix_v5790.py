"""Exact current physical both-Down true-mirror Tomb, full native sound in RAM.

Preserve whole canonical4350/4212 collector and4344 earned/branch/801cleanup
gates. The first stage certifies native DCS output with samples disabled;
it cannot claim the enabled winner mix, complete stage art or whole port.
"""
import argparse,gzip,hashlib,inspect,json,re,time,traceback
from pathlib import Path
import numpy as np
import current_payload_metadata_context_v5229 as current
import run_tomb_mirror_audio_ram_v4350 as runtime
import current_tomb_winner_mix_fault_model_v5789 as model
import qualify_current_pressed_tomb_winner_mix_v5792 as source
import verify_pressed_tomb_mirror_contract_v4387 as pressed
import verify_native_tomb_scream_roles_v4394 as original_voice
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA='mk2ks_current_pressed_tomb_winner_mix_v5791.lua'
OBSERVER='mk2ks_current_tomb_winner_mix_observer_v5779.lua'


def once(code,before,after):
 need(code.count(before)==1,'Only declared whole capture source adapter '+before)
 return code.replace(before,after,1)


def fields(line):
 pairs=re.findall(r'(\w+)=([^\s]+)',line);result=dict(pairs)
 need(len(pairs)==len(result),'Every actual full audio/ROM/DAC header has unique keys')
 return result


def adapt(code):
 changes=[
  ('audit_v4351_tomb_mirror_{fighter}_p{side}_{suffix}','audit_v5794_current_pressed_tomb_winner_mix_{fighter}_p{side}_{suffix}'),
  ('mk2ks_tomb_mirror_audio_ram_v4342.lua',LUA),
  ('36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982',current.EXE_SHA),
  ('91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24',current.PAYLOAD_SHA),
  ("    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}",
   """    files.update(ROOT/p for p in (OBSERVER,'mk2ks_current_native_dac_ram_v5592.lua','mk2ks_current_dcs_rom_source_v5585.lua'))
    files.update(Path(p.__file__)for p in (current,model,source))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    pre=json.loads((source.OUT/'report.json').read_text())
    need(pre['passed']and all(sha(p)==h for p,h in pre['inputHashes'].items()),'Whole current controller/observer/native-model preflight before boot')
    pins[str(source.OUT/'report.json')]=sha(source.OUT/'report.json')
    expected_sound,_=model.expected_region(pins)"""),
  ("    frozen={}\n    for p in files:\n        if p.suffix in('.lua','.py','.ps1','.json'):\n            dest=folder/'input_sources/tree'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);need(sha(dest)==pins[str(p)],'Exact executed hierarchy snapshot');frozen[str(p)]=str(dest)",
   "    # Whole input hashes bind originals directly; no redundant source snapshots.\n    frozen={str(p):str(p)for p in files if p.suffix in('.lua','.py','.ps1','.json')}"),
  ('    chunks=[];headers=[];guest_sha=None',
   "    chunks=[];headers=[];guest_sha=None\n    dac_chunks=[];dac_headers=[];dcs_buffers={'startup':bytearray(),'terminal':bytearray()};dcs_headers=[]"),
  ("errors='strict')as process:","errors='strict',creationflags=subprocess.CREATE_NO_WINDOW)as process:"),
  ("dict(pid=process.pid,command=cmd)","dict(pid=process.pid,command=cmd,startedUnix=time.time(),hostPID=os.getpid(),hostSource=__file__)"),
  ("with(folder/'run.log').open('w',encoding='utf-8')as log:","with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:"),
  ("                if line.startswith('MK2_BBAUDIO_PCM '):",
   """                if line.startswith(('MK2_NATIVE_DAC_RAM ','MK2_NATIVE_DCS_ROM ')):
                    h=fields(line);raw=bytes.fromhex(h.pop('hex'));need(len(raw)==int(h['bytes']),'Every actual DAC/ROM byte transported in RAM')
                    h['sha256']=hashlib.sha256(raw).hexdigest().upper()
                    if line.startswith('MK2_NATIVE_DAC_RAM '):
                        dac_chunks.append(raw);dac_headers.append(h);tag='MK2_NATIVE_DAC_RAM_DIGEST '
                    else:
                        phase=h['phase'];need(phase in dcs_buffers and h['bytes']=='65536'and h['size']=='12582912'and
                         h['bytewidth']=='2'and h['bitwidth']=='16'and h['writes']=='0'and h['assistance']=='none'and
                         int(h['offset'])==len(dcs_buffers[phase]),'Full consecutive original initialized/terminal sound-ROM chunks')
                        at=int(h['offset']);need(raw==expected_sound[at:at+65536],'Every native sound-ROM byte independently stock-source exact')
                        dcs_buffers[phase].extend(raw);dcs_headers.append(h);tag='MK2_NATIVE_DCS_ROM_DIGEST '
                    log.write(tag+' '.join(k+'='+str(v)for k,v in h.items())+'\\n')
                elif line.startswith('MK2_BBAUDIO_PCM '):"""),
  ("h=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(h.pop('hex'))", "h=fields(line);raw=bytes.fromhex(h.pop('hex'))"),
  ("    text=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()",
   "    with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()\n    errors=(folder/'stderr.log').read_text()"),
  ("return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).copy()",
   "return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).copy(),dac_chunks,dac_headers,dcs_headers,dcs_buffers,expected_sound")]
 code=once(code,'mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua')
 extra="    files.update(ROOT/p for p in ('mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua'))\n    files.update(Path(p.__file__)for p in (pressed,original_voice))\n"
 code=once(code,"    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}",extra+"    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}")
 for before,after in changes:
  # The two original PCM/guest headers are both adapted to unique-key parsing.
  if before.startswith('h=dict('):
   need(code.count(before)==2,'Exactly two original PCM/guest header parsers');code=code.replace(before,after)
  else:code=once(code,before,after)
 return code


def collector():
 # Derive the entire ordinary4350 factory; generated function source is kept
 # explicitly, never queried with inspect.getsource after exec.
 factory=inspect.getsource(runtime.collector)
 factory=once(factory,"    scope=dict(old.__dict__);scope.update(__file__=__file__,old=old,state=state)",
  "    source=adapt(source)\n    scope=dict(old.__dict__);scope.update(__file__=__file__,old=old,state=state,NAME=current.NAME,current=current,model=model,source=source_module,OBSERVER=OBSERVER,fields=fields,gzip=gzip,time=time,pressed=pressed,original_voice=original_voice)")
 factory=once(factory,"    return scope['capture'],hashlib.sha256(source.encode()).hexdigest().upper()",
  "    scope['capture'].source=source\n    return scope['capture'],hashlib.sha256(source.encode()).hexdigest().upper()")
 namespace=dict(vars(runtime),__file__=__file__,adapt=adapt,current=current,model=model,source_module=source,state=pressed,pressed=pressed,original_voice=original_voice,
  OBSERVER=OBSERVER,fields=fields,gzip=gzip,time=time)
 exec(compile(factory,__file__+'::whole4350_factory_current_RAM_DAC_ROM','exec'),namespace)
 return namespace['collector']()


def voice_models():
 # Whole original actual-role/female/native-RNG/owner gate; only current
 # whole-guest hash replaces its historical3836 compiled context.
 code=inspect.getsource(original_voice.qualify_scream)
 code=once(code,"'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(current.GUEST_SHA))
 scope=dict(vars(original_voice))
 exec(compile(code,__file__+'::whole4394_current_native_role_voice','exec'),scope)
 qualified=scope['qualify_scream'];qualified.source=code
 exec(compile(inspect.getsource(original_voice.faults),__file__+'::whole4394_actual_voice_faults','exec'),scope)
 return qualified,scope['faults']


def run(fighter,side):
 fn,transport_sha=collector();guest=current.expected()
 need(fn.__globals__['NAME']==current.NAME,'Actual bound current compiled native context')
 folder,headers,pcm,dac_chunks,dac_headers,rom_headers,buffers,expected=fn(fighter,side,True,guest)
 with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
 need((folder/'stderr.log').read_text()==''and 'MK2_TOMB_SOURCE_HOST_DEADLINE'not in text,
  'Actual ordinary native earned/action/cleanup terminal; no warning/deadline success')
 native=pressed.check_log(text,fighter,side,1,guest=guest)
 state_faults=pressed.actual_faults(text,fighter,side,guest)
 phase=pressed.qualify_pressed_drop(text,fighter,side,1,'positive',guest)
 phase_faults=pressed.pressed_phase_faults(text,fighter,side,guest)
 vg,vf=voice_models()
 screams=runtime.old.rows(text,'ROUTE')
 screams=[r for r in screams if r['entry']=='FFA11FD0']
 need(len(screams)==1,'One actual source-owned falling victim scream')
 voice=vg(text,fighter,side,guest,screams[0]);voice_faults=vf(text,fighter,side,guest)
 gate,fault=model.dac_models(len(headers));dac=gate(dac_chunks,dac_headers,headers);dac_faults=fault(dac_chunks,dac_headers,headers)
 mix_pins={}
 waveform=model.predict_mix(dac_chunks,dac_headers,pcm,text,fighter,mix_pins)
 (folder/'mixed_waveform_prediction.json').write_text(json.dumps(waveform,indent=2)+'\n')
 need(waveform['passed']and waveform['actualMixedRawPCMByteFaultSuiteAccepted'],
  'Whole real pressed Tomb native+winner stereo source equality and four actual raw/eight total waveform faults, no fit or trim')
 rg,rf=model.rom_models(expected)
 rom_proof=[rg(bytes(buffers[phase]),phase)for phase in ('startup','terminal')]
 rom_faults=[f for phase in ('startup','terminal')for f in rf(bytes(buffers[phase]),phase)]
 report=dict(passed=True,fighter=fighter,physicalSlot=side,identity=17 if fighter=='kano'else 18,
  candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
  transportSourceSHA256=transport_sha,capture=str(folder),nativeEarnedTombState=native,
  actualEarnedStateFaultsRejected=state_faults,sourceQualifiedNativePressedBranch=phase,
  actualPressedPhaseFaultsRejected=phase_faults,sourceQualifiedNativeLateVictimVoice=voice,
  actualLateVictimVoiceFaultsRejected=voice_faults,pcmHeaders=headers,dacHeaders=dac_headers,soundROMHeaders=rom_headers,
  actualNativeDACSourceProof=dac,actualDACFaultsRejected=dac_faults,waveform=waveform,
  actualWholeSoundROMProof=rom_proof,actualSoundROMFaultsRejected=rom_faults,
  actualCurrentNativeDCSStageWaveformAccepted=False,samplesEnabled=True,
  importedWinnerMixedWaveformAccepted=True,mixedWaveformSourceInputHashes=mix_pins,
  actualMixedRawPCMByteFaultSuiteAccepted=waveform['actualMixedRawPCMByteFaultSuiteAccepted'],completeStageVictimAudioAccepted=False,
  fullStageArtAccepted=False,fullPortAcceptance=False,rawPCMGuestROMRGBFilesWritten=0,newBuilds=0,publicPlayableChanged=False)
 (folder/'audio_live_source_model.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('pcmHeaders','dacHeaders','soundROMHeaders','waveform','actualEarnedStateFaultsRejected','nativeEarnedTombState')},indent=2),flush=True)
 print(json.dumps({k:v for k,v in waveform.items()if k not in('actualCallbackSourceClocks','expectedWinnerCallbackStates')},indent=2),flush=True)
 return report


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5794_current_pressed_tomb_winner_mix_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
