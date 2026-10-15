"""Additive whole waveform/source/ownership proof on the retained native run.

Never replays, edits old reports, or writes PCM/DAC/guest/RGB transports. Real
state/channel/marker counterexamples are RAM copies of this exact execution.
"""
import copy,gzip,inspect,json,subprocess
from pathlib import Path
import kano_launch_waveform_model_v6654 as waveform
import capture_kano_launch_audio_v6652 as host
ROOT,need,sha=host.ROOT,host.need,host.sha

def dac_models(count):
 source=inspect.getsource(host.models.original_dac.dac_gate)
 before='len(chunks)==len(headers)==len(pcm_headers)==685'
 need(source.count(before)==1 and count>200,'Whole native window, original DAC duration only')
 source=source.replace(before,'len(chunks)==len(headers)==len(pcm_headers)==count',1)
 scope=dict(vars(host.models.original_dac),count=count)
 exec(compile(source,__file__+'::entire_original_DAC_source_gate','exec'),scope)
 exec(compile(inspect.getsource(host.models.original_dac.dac_faults),__file__+'::entire_original_actual_DAC_fault_suite','exec'),scope)
 return scope['dac_gate'],scope['dac_faults']

def qualify(record):
 side,enabled=record['side'],record['enabled'];folder=record['folder'];buffers=record['buffers'];text=record['text']
 out=ROOT/f"audit_v6657_kano_launch_audio_checked_{'on'if enabled else'off'}_p{side}"
 need(not out.exists(),'Fresh additive exact native proof')
 report=json.loads((folder/'result.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
 need(report['passed']and report['nativeAudioTransportOnly']and not report['wholeWaveformAccepted']and
      report['samplesEnabled']==enabled and terminal['naturalTerminal']and terminal['exitCode']==0 and not terminal['observationErrors'],
      'Actual physical native natural terminal, no inherited waveform acceptance')
 pins=dict(report['inputHashes'])
 for p in[Path(__file__),Path(waveform.__file__),Path(waveform.original.__file__),Path(host.models.__file__),
           ROOT/'mame-mkp/src/devices/sound/samples.cpp',ROOT/'audit_v6658_launch_source_number_discrepancy/executed_source.py',
           ROOT/'audit_v6658_launch_source_number_discrepancy/README.md',
           *[p for p in folder.rglob('*')if p.is_file()]]:pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actually executed full source/candidate/native evidence pins intact')
 pcm=buffers['pcmHeaders'];need(len(pcm)==len(buffers['dac'])==len(buffers['dacHeaders'])and all(h['bytes']=='3840'for h in pcm),
                                 'Every complete actual stereo48k20ms callback')
 need(all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(pcm,pcm[1:])),
      'No missing first/cache/tail or interior sound callback')
 begin=waveform.rows(text,'MK2_MAUDIO_BEGIN');end=waveform.rows(text,'MK2_MAUDIO_RESULT')
 ready=waveform.rows(text,'MK2_HSPECIAL_READY');final=waveform.rows(text,'MK2_HSPECIAL_RESULT')
 need(len(begin)==len(end)==len(ready)==len(final)==1 and begin[0]['origin']==begin[0]['frame']==ready[0]['frame']and
      begin[0]['id']=='17'and begin[0]['slot']==str(side)and end[0]['frame']==final[0]['frame']and
      end[0]['origin']==begin[0]['origin'],'Entire real-ready through physical terminal audio window')
 first,last=int(ready[0]['frame']),int(final[0]['frame'])
 pre={(int(r['frame']),int(r['slot'])):r for r in waveform.rows(text,'MK2_HSPECIAL_FIELD')}
 binding=waveform.rows(text,'MK2_MAUDIO_BINDING')
 need(len(binding)==(last-first+1)*2 and {(int(r['frame']),int(r['slot']))for r in binding}==
      {(f,s)for f in range(first,last+1)for s in(1,2)},'Every actual physical actor ownership in the full finite window')
 for r in binding:
  key=int(r['frame']),int(r['slot']);native=pre[key]
  need(all(r[k]==native[k]for k in('actor','main','owner','id','roster'))and r['writes']=='0'and r['assistance']=='none',
       'Whole audio ownership binds the same independently qualified native actors, not proxies')
 gate,fault=dac_models(len(pcm));dac=gate(buffers['dac'],buffers['dacHeaders'],pcm);dac_faults=fault(buffers['dac'],buffers['dacHeaders'],pcm)
 rg,rf=host.models.rom_models(record['expectedROM']);rom=[rg(bytes(buffers['rom'][p]),p)for p in buffers['rom']]
 rom_faults=[f for p in buffers['rom']for f in rf(bytes(buffers['rom'][p]),p)]
 result=waveform.predict(record)
 need(result['passed'],'Every actual output sample must equal full source prediction')
 channel_faults=[]
 channel_rows=waveform.rows(text,'MK2_TOMB_MIX_CHANNEL')
 selected=next(r for r in channel_rows if r['sample']=='16')if enabled else None
 if selected:
  before=next(line for line in text.splitlines()if line.startswith('MK2_TOMB_MIX_CHANNEL ')and
              f"index={selected['index']} "in line and f"channel={selected['channel']} "in line)
  for label,key,wrong in [('wrong physical source slot','channel',str(12 if side==1 else 10)),
                        ('wrong actual sample','sample','13'),('source loops','loop','1'),
                        ('source paused','paused','1'),('source length clipped','length','55464'),
                        ('source clock late','position',str(float(selected['position'])-1))]:
   bad=dict(record,text=text.replace(before,before.replace(key+'='+selected[key],key+'='+wrong,1),1))
   try:waveform.predict(bad)
   except ValueError as error:channel_faults.append(dict(kind=label,rejectedBy=str(error)))
   else:raise ValueError('Actual channel counterexample admitted '+label)
   need(waveform.predict(record)==result,'Whole source positive restored after every real channel fault')
 need(all(sha(p)==h for p,h in pins.items()),'All source and retained native evidence pins unchanged')
 proof=dict(passed=True,candidate=waveform.current.NAME,executableSHA256=waveform.current.EXE_SHA,guestSHA256=waveform.current.GUEST_SHA,
            physicalSlot=side,samplesEnabled=enabled,nativeTerminal=terminal,sourceDAC=dac,actualDACFaultsRejected=dac_faults,
            entireOriginalSoundROM=rom,actualSoundROMFaultsRejected=rom_faults,wholeWaveform=result,
            actualSourceChannelFaultsRejected=channel_faults,wholePhysicalOwnershipFields=len(binding),
            physicalSemantics=report['independentSemantics'],inputHashes=pins,rawMediaFilesWritten=0,
            authoredWAVAssetUsed=str(ROOT/waveform.current.NAME/'samples/mk2ks/kano_ball_launch.wav'),
            nativeFloorShadowAcceptance=False,fullInterruptionCoverageAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False)
 out.mkdir();p=out/'report.json';p.write_text(json.dumps(proof,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless source proof compression')
 print(json.dumps(dict(passed=True,physicalSlot=side,samplesEnabled=enabled,comparedStereoFrames=result['comparedStereoFrames'],
                       differentChannelSamples=result['differentChannelSamples'],channelFaults=len(channel_faults),fullPortAcceptance=False)),flush=True)
 return proof
