"""Six complete laser-source recordings, all five DCS slots, PCM RAM only.

Hardware-only sample extraction, never gameplay/activation acceptance.
Reuse the preserved real DCS byte-delivery probe and native48k NUL sink.
No guest character/health/AI/RNG writes; no raw PCM/WAV transport files.
Only the six verified authored waveform assets are saved, one copy each.
"""
import gzip
import hashlib
import inspect
import json
import os
import re
import time
import wave
from pathlib import Path
import numpy as np
import build_kano_launch_oracle_v6632 as oracle
import capture_native_secondary_kano_reference as hardware
import native_process_census_v6647 as identity

ROOT=oracle.ROOT
OUT=ROOT/'audit_native_kano_laser_original_samples'
need,sha=oracle.need,oracle.sha
GUARD=ROOT/'audit_native_kano_laser_original_audio_timer_path_review/report.json'
SOUNDS=[('kano_laser_charge',0x0352),('kano_laser_beam',0x276a),
        ('sonya_laser_scream',0x081b),('kano_laser_scream',0x17bb),
        ('kano_laser_burst_a',0x0140),('kano_laser_burst_b',0x0145)]


def exact_run():
    source=inspect.getsource(oracle.run)
    edits=[("'-video','none','-sound','none','-samplerate','48000'",
            "'-video','none','-sound','none','-samplerate','48000','-wavwrite','NUL'"),
        ('ROOT/\'mk3/mk3-maincpu.bin\',*list((ROOT/\'mk3\').glob(\'*music_spch*\'))]',
         "ROOT/'mk3/mk3-maincpu.bin',Path(oracle.__file__),Path(hardware.__file__),Path(identity.__file__),GUARD,*list((ROOT/'mk3').glob('*music_spch*'))]"),
        ("out=OUT/command;need(not out.exists(),'Fresh native oracle command leaf, no restart/overwrite')",
         "out=OUT/command;need(not out.exists() and not hardware.census() and not identity.census(),'One fresh exact hardware oracle; no native games live')"),
        ("process=subprocess.Popen(args,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace')",
         """born=time.time()
 process=subprocess.Popen(args,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
 actual=None
 for _ in range(100):
  actual=next((p for p in hardware.census() if p['ProcessId']==process.pid),None)
  if actual or process.poll()is not None:break
  time.sleep(.02)"""),
        ('dict(pid=process.pid,command=args,startedUTC=',
         'dict(pid=process.pid,command=args,actualWindowsIdentity=actual,startedUTC='),
        ('nativeExit=exitcode,pid=process.pid,inputHashes=pins,',
         'nativeExit=exitcode,pid=process.pid,actualWindowsIdentity=actual,inputHashes=pins,'),
        ("need(exitcode==0 and not stderr.strip()and any(l.startswith('MK3_LAUNCH_ORACLE_TERMINAL frame=1500 ')for l in text),",
         """need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
       Path(actual['ExecutablePath']).resolve()==exe.resolve() and
       not any(p['ProcessId']==process.pid for p in hardware.census()),'Same real PID/parent/path/creation handle terminal')
  need(exitcode==0 and not stderr.strip()and any(l.startswith('MK3_LAUNCH_ORACLE_TERMINAL frame=1500 ')for l in text),""")]
    for old,new in edits:
        need(source.count(old)==1,'Exact existing whole native48k hardware collector boundary')
        source=source.replace(old,new)
    scope=dict(vars(oracle),OUT=OUT,__file__=__file__,oracle=oracle,hardware=hardware,identity=identity,GUARD=GUARD,time=time)
    exec(compile(source,__file__+'::same_native_source_audio_handle','exec'),scope)
    return scope['run']


def extract(name,base_command,baseline,variants):
    base=np.frombuffer(baseline['raw'],'<i2').reshape(-1,2).astype(np.int32)
    clocks=[(q['frame'],q['seconds'],q['bytes']) for q in baseline['report']['nativePCMHeaders']]
    first_buffer=float(baseline['report']['nativePCMHeaders'][0]['seconds'])-.02
    deltas=[];deliveries=[];start=None;delivery=None
    for command,value in variants:
        need([(q['frame'],q['seconds'],q['bytes']) for q in value['report']['nativePCMHeaders']]==clocks,
             'Every complete baseline/source channel PCM callback clock and dimension exactly equal')
        packets=re.findall(r'MK3_FRIEND_ISOLATED_TIME frame=\d+ seconds=([\d.]+) address=01680000 data=([\dA-F]{4}) mask=00FF',value['text'])
        need(len(packets)==2 and [int(p[1],16) for p in packets]==[command>>8,command&255],
             'Exactly the two requested actual hardware-only high/low bytes')
        seconds=float(packets[0][0]);need(abs(float(packets[1][0])-seconds-.000025)<1e-9,
                                        'Exact original25us byte-delivery interval')
        need(delivery is None or delivery==seconds,'Same native delivery clock across every real channel')
        delivery=seconds;start=round((seconds-first_buffer)*48000)
        actual=np.frombuffer(value['raw'],'<i2').reshape(-1,2).astype(np.int32)
        difference=actual-base
        need(not np.any(difference[:start]),'No predelivery source difference')
        need(np.array_equal(difference[:,0],difference[:,1]),'Whole original source is dual mono')
        deltas.append(difference[:,0]);deliveries.append(dict(command=f'{command:04X}',seconds=seconds,
            pcmSHA256=hashlib.sha256(value['raw']).hexdigest().upper(),nativePID=value['report']['pid']))
    need(len(deltas)==5 and all(np.array_equal(deltas[0],d) for d in deltas[1:]),
         'All five complete channelized original command recordings exactly equal; never assume variants')
    delta=deltas[0];nonzero=np.flatnonzero(delta)
    need(len(nonzero)>0 and nonzero[0]>=start,'Real complete original sound present after actual delivery')
    end=int(nonzero[-1])+3
    need(end<len(delta)-48000 and not np.any(delta[end:]),'Complete actual tail plus at least one second of verified silence')
    source=delta[start:end];scaled=np.rint(source/.70)
    need(np.max(np.abs(scaled))<32767 and np.max(np.abs(scaled*.70-source))<=.35+1e-8,
         'Only actual original0.70 route compensation, integer quantization bound, no clipping or creative gain')
    pcm=scaled.astype('<i2');asset=OUT/(name+'.wav')
    need(not asset.exists(),'One new authored full source sample, no duplicate build copy')
    with wave.open(str(asset),'wb')as file:
        file.setparams((1,2,48000,0,'NONE','not compressed'));file.writeframes(pcm.tobytes())
    return dict(name=name,baseCommand=f'{base_command:04X}',nativeChannelVariants=5,allVariantsExactlyEqual=True,
        frames=len(pcm),firstPCMDelaySeconds=(int(nonzero[0])-start)/48000,route=.70,
        verifiedFinalSilenceFrames=len(delta)-end,wholeSourcePCM_SHA256=hashlib.sha256(source.astype('<i2').tobytes()).hexdigest().upper(),
        stagedAsset=str(asset),assetSHA256=sha(asset),deliveryCases=deliveries)


def main():
    need(not OUT.exists(),'Fresh complete hardware sample extraction; preserve previous artifacts')
    guard=json.loads(GUARD.read_text())
    need(guard['passed'] and guard['earnedOriginalSoundAllocatorReplayAccepted'] and
         not guard['portAudioAccepted'] and all(sha(p)==h for p,h in guard['inputHashes'].items()),
         'Actual earned source cue/record/channel/timer trace conserved before asset extraction')
    need(guard['ownCueRecords']==['03525038','276A504C'] and guard['universalBurstRecords']==['01405066','01455063'] and
         guard['victimCue9Records'][0]=='081B41CB' and guard['victimCue9Records'][3]=='17BB41C1',
         'All six requested complete source recordings come from actual source records, not invented packets')
    OUT.mkdir();run=exact_run();baseline=run('baseline');results=[];jobs=[baseline['report']]
    for name,command in SOUNDS:
        variants=[]
        for offset in range(5):
            value=run(f'{command+offset:04x}');jobs.append(value['report']);variants.append((command+offset,value))
        result=extract(name,command,baseline,variants);results.append(result)
        (OUT/(name+'_asset_report.json')).write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(dict(asset=name,passed=True,frames=result['frames'],allFiveChannelsEqual=True)),flush=True)
    pins={}
    for job in jobs:pins.update(job['inputHashes'])
    for result in results:pins[result['stagedAsset']]=result['assetSHA256']
    need(all(sha(p)==h for p,h in pins.items()),'Every actual executed source/ROM/helper/sample input conserved')
    report=dict(passed=True,hardwareOnlyNotGameplayAcceptance=True,portAudioAccepted=False,fullPortAcceptance=False,
        actualNativeJobs=len(jobs),assets=results,inputHashes=pins,guestRAMWrites=0,
        diagnosticHardwareSoundWritesPerCommand=2,rawPCMTransportFiles=0,newROMCopies=0,newBuilds=0,newZIPs=0,
        originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],goalStatus='active',latestPlayableChanged=False)
    need(len(jobs)==31 and len(results)==6,'All31 real source hardware jobs and all6 complete assets')
    (OUT/'asset_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,assets=6,actualNativeJobs=31,portAudioAccepted=False)),flush=True)


if __name__=='__main__':main()
