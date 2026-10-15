"""Additive same-RAM whole current CPU startup source-audio qualification.

Native6664 remains terminal and its original host rejection remains false.
Reuse all actual state/HP/choice/motion evidence and complete retained audio.
This does not qualify all arenas, interruptions, UI raster or the full port.
"""
import gzip,json,re,subprocess
from pathlib import Path
import kano_cpu_launch_audio_model_v6668 as model
import qualify_kano_cpu_launch_motion_v6665 as motion
import qualify_kano_launch_audio_v6656 as source
import native_process_census_v6647 as process
ROOT,need,sha=model.ROOT,model.need,model.sha
CASE=motion.CASE
OUT=ROOT/'audit_v6671_kano_cpu_launch_audio_checked'


def finish(carrier):
 need(not OUT.exists()and not process.census(),'Fresh same terminal host qualification without native replay')
 terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(terminal['nativeExit']==carrier['code']==0 and not terminal['hostDecodeErrors']and not carrier['decode_errors']and
      (CASE/'stderr.log').read_text()==''and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|CACHE_OVERWRITE',carrier['text'],re.I),
      'Actual same native terminal and entire transport without observer or emulator error')
 native_identity=terminal['actualWindowsIdentity'];command=json.loads((CASE/'process.json').read_text())
 need(native_identity==command['actualWindowsIdentity']and native_identity['ProcessId']==terminal['pid']==command['pid']and
      Path(native_identity['ExecutablePath']).resolve()==(ROOT/model.original.candidate.NAME/'mkport_candidate.exe').resolve()and
      '-samples'in command['command']and '-nocheat'in command['command']and command['command'][command['command'].index('-wavwrite')+1]=='NUL',
      'Actual kernel-captured native executable identity, samples enabled48k and no disk WAV transport')
 motion_path=motion.OUT/'report.json';motion_result=json.loads(motion_path.read_text())
 need(motion_result['passed']and motion_result['nativeTerminal']==terminal and
      len(motion_result['proof']['allActualRollPhases'])==2 and
      len(motion_result['proof']['declaredCompletedPairs'])==2 and
      len(motion_result['proof']['actualNativeMotionFaultsRejected'])==47,
      'Same entire native match ledger, all actual choices and both complete source roll/pair contracts')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'All actually executed source and candidate pins unchanged')
 text=carrier['text'];headers=carrier['pcm_headers']
 waveform=model.predict(carrier,pins);need(waveform['passed']and waveform['differentChannelSamples']==0 and
      len(waveform['actualRawAndSourceFaultsRejected'])==8,'Entire actual CPU output equals complete original DAC plus both starts and genuine winner; all8 raw/source faults')
 channels=model.channels(text,headers,pins);packets=model.packet_gate(text)
 dg,df=source.dac_models(len(headers));dac=dg(carrier['dac_chunks'],carrier['dac_headers'],headers)
 dac_faults=df(carrier['dac_chunks'],carrier['dac_headers'],headers)
 rg,rf=source.host.models.rom_models(carrier['expected'])
 rom=[rg(bytes(carrier['rom'][phase]),phase)for phase in carrier['rom']]
 rom_faults=[f for phase in carrier['rom']for f in rf(bytes(carrier['rom'][phase]),phase)]
 need(len(dac_faults)==4 and len(rom_faults)==8 and len(rom)==2 and carrier['seen_guest']==2 and carrier['seen_gfx']==0,
      'Both whole loaded original sound ROMs and full DAC/cache source proof, all original faults')
 binding=model.original.rows(text,'MK2_MAUDIO_BINDING')
 need(len(binding)==1803*2 and {(int(r['frame']),int(r['slot']))for r in binding}==
      {(f,s)for f in range(1813,3616)for s in(1,2)}and
      all(r['actor']==r['owner']and r['id']==r['roster']=='17'and r['writes']=='0'and r['assistance']=='none'for r in binding),
      'Every true owned physical role through native entry, damage, KO, reset and natural terminal')
 rgb=carrier['raw_proofs']
 need(rgb==model.original.rows(text,'MK2_EARNED_SUBZERO_RGB_DIGEST')and
      len(rgb)==98 and all(r['width']=='400'and r['height']=='254'and r['bytes']=='406400'and re.fullmatch('[0-9A-F]{64}',r['sha256'])for r in rgb),
      'Every actual full native callback digest retained; no reduction to historical42 scenes')
 faults=[]
 def reject(label,bad,fn):
  need(bad!=text,'Actual native audio record changed')
  try:fn(bad)
  except(AssertionError,ValueError,KeyError,IndexError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual native CPU sound fault: '+label)
 for label,tag,key,value,where,fn in[
  ('wrong physical launch channel','MK2_TOMB_MIX_CHANNEL','channel','10',dict(channel=12,index=1000),lambda t:model.channels(t,headers,{})),
  ('wrong launched sample','MK2_TOMB_MIX_CHANNEL','sample','13',dict(channel=12,index=1000),lambda t:model.channels(t,headers,{})),
  ('looped launch','MK2_TOMB_MIX_CHANNEL','loop','1',dict(channel=12,index=1000),lambda t:model.channels(t,headers,{})),
  ('paused launch','MK2_TOMB_MIX_CHANNEL','paused','1',dict(channel=12,index=1000),lambda t:model.channels(t,headers,{})),
  ('clipped launch length','MK2_TOMB_MIX_CHANNEL','length','55464',dict(channel=12,index=1000),lambda t:model.channels(t,headers,{})),
  ('wrong native source clock','MK2_TOMB_MIX_CHANNEL','bits','000000000000F03F',dict(channel=12,index=1000),lambda t:model.channels(t,headers,{})),
  ('proxy startup owner','MK2_MAUDIO_SOUND','a13','01000000',dict(word='6B03',frame=2898),lambda t:model.sources(t,{})),
  ('wrong native startup PC','MK2_MAUDIO_SOUND','pc','FFFFDE00',dict(word='6B03',frame=1814),model.packet_gate),
  ('wrong native packet','MK2_MAUDIO_PACKET','a3','00010000',{},model.packet_gate),
  ('missing native high-byte prefix','MK2_MAUDIO_SOUND','word','0000',dict(pc='FFA13C90'),model.packet_gate),
  ('wrong original ADSP byte','MK2_MAUDIO_DELIVERY','word','FFFF',{},model.packet_gate),
  ('wrong true winner','MK2_MAUDIO_SOUND','word','FFFD',dict(pc='FFFB7140'),model.packet_gate),
 ]:
  reject(label,motion.mutate(text,tag,key,value,where),fn)
 for tag,label,fn in [('MK2_MAUDIO_DELIVERY','missing actual DSP read',model.packet_gate),
                      ('MK2_TOMB_MIX_CHANNEL','missing precise physical source',lambda t:model.channels(t,headers,{}))]:
  line=next(s+'\n'for s in text.splitlines()if s.startswith(tag+' '));reject(label,text.replace(line,'',1),fn)
 need(model.channels(text,headers,pins)==channels and model.packet_gate(text)==packets,'Whole actual source-positive restored after all record counterexamples')
 failure=json.loads((CASE/'failure.json').read_text());selector=ROOT/'audit_v6669_cpu_launch_observer_key_rejection'
 need(failure['passed']is False and json.loads((selector/'failure.json').read_text())['passed']is False,'Both actual host failures retained, not rewritten to pass')
 for p in(Path(__file__),Path(model.__file__),Path(model.original.__file__),Path(source.__file__),motion_path,
          *[p for p in selector.rglob('*')if p.is_file()],*[p for p in CASE.rglob('*')if p.is_file()]):
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All bound actual source, compiled, old-failure and native evidence bytes intact')
 need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in CASE.rglob('*')if p.is_file()),'No new raw native gameplay media/build/ZIP in this capture')
 result=dict(passed=True,candidate=model.original.candidate.NAME,nativeTerminal=terminal,
             wholeNativeMotionProof=str(motion_path),wholeNativeMotionProofSHA256=sha(motion_path),
             completeStereoFrames=waveform['comparedStereoFrames'],wholeNativePCM=waveform,
             allPrecisePhysicalSourceStates=channels,nativeDelivery=packets,originalNativeDAC=dac,
             actualNativeDACFaultsRejected=dac_faults,bothWholeOriginalSoundROMs=rom,actualSoundROMFaultsRejected=rom_faults,
             actualAudioRecordFaultsRejected=faults,completePhysicalBindingFields=len(binding),allNativeRGBCallbackDigests=rgb,
             originalTrajectoryMismatchNotClaimedEquivalent=True,sourceExactCPUStartupAudioAccepted=True,
             authoredDonorWAVAsset=str(ROOT/model.original.candidate.NAME/'samples/mk2ks/kano_ball_launch.wav'),
             sourceRasterAcceptance=False,fullInterruptionCoverageAccepted=False,fullPortAcceptance=False,
             preservedFailures=[str(CASE/'failure.json'),str(selector/'failure.json')],inputHashes=pins,
             remaining=carrier['remaining'],goalStatus='active',publicPlayableChanged=False,
             newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,
             thisGoalTurnClassification='progress: full same-run native CPU state/motion and source-exact startup/winner/DAC audio qualified, all actual choices retained')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact proof compressed losslessly')
 print(json.dumps(dict(passed=True,stereoFrames=result['completeStereoFrames'],nativePackets=packets['packets'],
                       actualRecordFaultsRejected=len(faults),newBuilds=0,fullPortAcceptance=False)),flush=True)
 return result
