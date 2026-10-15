"""Full two-cycle physical gameplay plus original PCM/DAC/ROM in RAM only.

This collector proves physical semantics and exact transport, not waveform
parity. Same-process buffers remain available to the independent source model.
On any later host rejection --hold retains RAM; never replays that process.
"""
import argparse,code,gzip,inspect,json,re,traceback
from pathlib import Path
import capture_kano_launch_native_identity_v6648 as physical
import current_ending_audio_model_v5733 as models
ROOT,need,sha=physical.prior.candidate.ROOT,physical.need,physical.prior.candidate.sha
LUA=ROOT/'mk2ks_kano_launch_audio_v6651.lua'
LAST_CAPTURE=None

def bindings(enabled,side):
 buffers=dict(pcm=[],pcmHeaders=[],dac=[],dacHeaders=[],rom={p:bytearray()for p in('startup','terminal')},guestCount=0)
 pins={};expected,_=models.expected_region(pins)
 source=inspect.getsource(physical.bindings)
 before="'audit_v6262_current_cmd_special_':'audit_v6649_kano_launch_special_'"
 need(source.count(before)==1,'Only fresh paired-audio evidence path')
 source=source.replace(before,"'audit_v6262_current_cmd_special_':'audit_v6653_kano_launch_audio_'+('on_'if enabled else'off_')",1)
 before='  for before,after in changes.items():'
 need(source.count(before)==1,'Whole original collector adaptations retained')
 source=source.replace(before,'  if fn is capture:changes.update(audio_edits)\n'+before,1)
 before='  scope.update(prior=prior,identity=identity,corrected=prior.corrected)'
 need(source.count(before)==1,'Whole capture scope, additional RAM-only sound inventory')
 source=source.replace(before,before+"\n  scope.update(LUA=LUA,audio_buffers=audio_buffers,audio_expected=audio_expected,audio_pins=audio_pins)",1)
 edits={
  "pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])":
  "pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes']);pins.update(audio_pins)",
  "args=[str(LAUNCHER),'-video'":
  "args=[str(LAUNCHER),'-wavwrite','NUL','-samples'if "+str(enabled)+" else'-nosamples','-video'",
  "if line.startswith(('MK2_HPHASE_GUEST ','MK2_HPHASE_GFX ','MK2_HPHASE_RGB ')):":
  "if line.startswith(('MK2_BBAUDIO_PCM ','MK2_NATIVE_DAC_RAM ','MK2_NATIVE_DCS_ROM ','MK2_MAUDIO_GUEST ')):\n      f=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(f.pop('hex'));tag=line.split()[0];need(len(raw)==int(f['bytes']),'Complete actual audio inventory transport');digest=hashlib.sha256(raw).hexdigest().upper()\n      if tag=='MK2_BBAUDIO_PCM':audio_buffers['pcm'].append(raw);audio_buffers['pcmHeaders'].append(f)\n      elif tag=='MK2_NATIVE_DAC_RAM':audio_buffers['dac'].append(raw);audio_buffers['dacHeaders'].append(f)\n      elif tag=='MK2_MAUDIO_GUEST':need(raw==guest,'Every actual audio guest byte equals independent complete constructor');audio_buffers['guestCount']+=1\n      else:\n       phase=f['phase'];need(phase in audio_buffers['rom'] and int(f['offset'])==len(audio_buffers['rom'][phase])and f['bytes']=='65536'and f['size']=='12582912'and f['bytewidth']=='2'and f['bitwidth']=='16'and f['writes']=='0'and f['assistance']=='none','Complete original ROM source inventory');at=int(f['offset']);need(raw==audio_expected[at:at+len(raw)],'Every actual original sound ROM byte');audio_buffers['rom'][phase].extend(raw)\n      log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in f.items())+' sha256='+digest+'\\n')\n     elif line.startswith(('MK2_HPHASE_GUEST ','MK2_HPHASE_GFX ','MK2_HPHASE_RGB ')):",
  "nativeStderrEmpty=not(folder/'stderr.log').read_text().strip(),canonicalCMDUsed=True":
  "nativeStderrEmpty=not(folder/'stderr.log').read_text().strip(),samplesEnabled="+str(enabled)+",nativeAudioTransportOnly=True,wholeWaveformAccepted=False,canonicalCMDUsed=True",
  "need(exitcode==0 and identity and not errors and len(proofs)==2 and report['nativeStderrEmpty'],'Actual successful immutable native terminal, no host/runtime errors')":
  "need(exitcode==0 and identity and not errors and len(proofs)==2 and report['nativeStderrEmpty'],'Actual successful immutable native terminal, no host/runtime errors');need(audio_buffers['guestCount']==1 and all(len(v)==12582912 for v in audio_buffers['rom'].values())and len(audio_buffers['pcm'])==len(audio_buffers['dac'])>200,'All audio guest/full ROM/complete PCM and DAC callbacks')",
 }
 # This replacement runs after the underlying isolation substitutions.
 edits["nativeStderrEmpty=not(folder/'stderr.log').read_text().strip(),canonicalCMDUsed=False"] = edits.pop("nativeStderrEmpty=not(folder/'stderr.log').read_text().strip(),canonicalCMDUsed=True").replace('canonicalCMDUsed=True','canonicalCMDUsed=False')
 for p in[Path(__file__),Path(physical.__file__),Path(models.__file__),LUA,ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua']:
  pins[str(p.resolve())]=sha(p)
 scope=dict(physical.__dict__,__file__=__file__,enabled=enabled,LUA=LUA,audio_edits=edits,audio_buffers=buffers,audio_expected=expected,audio_pins=pins)
 exec(compile(source,__file__+'::entire_original_physical_capture_plus_audio','exec'),scope)
 capture,load=scope['bindings']();return capture,load,buffers,pins,expected

def run(side,enabled):
 global LAST_CAPTURE
 capture,load,buffers,pins,expected=bindings(enabled,side)
 LAST_CAPTURE=dict(side=side,enabled=enabled,buffers=buffers,expectedROM=expected)
 folder=ROOT/f"audit_v6653_kano_launch_audio_{'on'if enabled else'off'}_ball_p{side}"
 LAST_CAPTURE.update(folder=folder,inputHashes=pins)
 try:result=capture('ball',side)
 finally:
  if (folder/'run.log.gz').exists():
   with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as file:LAST_CAPTURE['text']=file.read()
  if (folder/'result.json').exists():LAST_CAPTURE['report']=json.loads((folder/'result.json').read_text())
 b=load('ball',side);text=LAST_CAPTURE['text']
 LAST_CAPTURE.update(report=result,case=b,text=text,inputHashes=pins,folder=b['folder'])
 print(json.dumps(dict(physicalPassed=result['passed'],slot=side,samplesEnabled=enabled,completePCMCallbacks=len(buffers['pcm']),wholeWaveformAccepted=False,rawMediaFilesWritten=0)),flush=True)
 return LAST_CAPTURE

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--nosamples',action='store_true');parser.add_argument('--hold',action='store_true');a=parser.parse_args()
 try:run(a.side,not a.nosamples)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),wholeWaveformAccepted=False,fullPortAcceptance=False)),flush=True)
 if a.hold and LAST_CAPTURE:
  code.interact(banner='Same naturally terminal native process, original PCM/DAC/ROM retained in RAM. No replay.',local=dict(capture=LAST_CAPTURE,module=__import__(__name__)))
