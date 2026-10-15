"""Actual native DAC floats to independently computed original mixer waveform.

Preserve whole live physical/art/audio transport. Native DAC ring segments
and mixed PCM remain RAM-only. Source-normalized16-bit samples are checked
exactly. An explicit float32 original resampler/mono mixer prediction is
compared to every actual sample; a mismatch is retained as incomplete
waveform qualification, not silently ignored or claimed to be a game bug.
"""
import datetime, inspect, json, re, struct, traceback
from pathlib import Path
from decimal import Decimal
import numpy as np
import qualify_current_baraka_direct_packets_v5580 as direct

origin=direct.observed
capture=direct.capture
ROOT,need,sha=direct.ROOT,direct.need,direct.sha
PARENT=ROOT/'audit_v5591_current_dcs_rom_source_bound_progress/progress.json'
BASE=ROOT/'audit_v5594_current_native_dac_ram'
OUT=ROOT/'audit_v5595_current_native_dac_progress'
LUA=ROOT/'mk2ks_current_native_dac_ram_v5592.lua'
COMPLETED=[]

def dac_gate(chunks,headers,pcm_headers):
    need(len(chunks)==len(headers)==len(pcm_headers)==685,'Every original native DAC and whole mixed PCM callback')
    total=nonzero=0
    for i,(raw,r,p) in enumerate(zip(chunks,headers,pcm_headers)):
        n=int(r['consumed']);values=np.frombuffer(raw,'<f4')
        need(r['index']==str(i+1) and all(r[k]==p[k]for k in ('frame','seconds'))
             and r['writes']=='0' and r['assistance']=='none' and r['ring']=='32768'
             and r['prefix']=='4' and r['element_bytes']=='4' and len(raw)==(n+4)*4
             and n==(int(r['current_out'])-int(r['previous_out']))%32768 and 0<n<4096,
             'Complete actual native DAC callback/ring/cursor/PCM association')
        need(abs(float(r['seconds'])-float(r['previous_seconds'])-.02)<1e-9
             and (not i or r['previous_out']==headers[i-1]['current_out']),
             'Every actual20ms sound interval and native consumed ring segment continuous')
        need(r['enabled']=='1' and r['volume']=='3F800000' and r['channels']=='1' and r['incs']=='1'
             and int(r['autobuffer'],16)&2 and int(r['syscontrol'],16)&0x0800,
             'Actual original enabled mono unit-gain serial autobuffer, not synthetic channel audio')
        need(np.isfinite(values).all(),'Every actual native DAC float finite')
        integers=np.rint(values.astype(np.float64)*32767)
        need(np.all((integers>=-32768)&(integers<=32767)),'Original signed16 DCS output range')
        independently_scaled=integers.astype(np.float32)*np.float32(1.0/32767.0)
        need(np.array_equal(independently_scaled.view('<u4'),values.view('<u4')),
             'Every actual DAC float bit-exact original signed16 normalization, not approximate amplitude')
        total+=n;nonzero+=int(np.count_nonzero(values[4:]))
    need(nonzero>1000,'Actual entire native non-silent output, not a silent or empty buffer')
    return dict(passed=True,callbacks=len(chunks),consumedNativeSamples=total,nonzeroNativeSamples=nonzero,
                everyActualDACFloatOriginalSigned16NormalizationExact=True,
                allActualConsumedSegmentsAndPCMCallbacksBound=True)

def dac_faults(chunks,headers,pcm_headers):
    positive=dac_gate(chunks,headers,pcm_headers);rejected=[]
    for label,kind in (('one actual DAC float bit corrupted','float'),('one actual DAC sample missing','missing'),
                       ('actual ring cursor corrupted','cursor'),('wrong actual DAC volume','volume')):
        bad_chunks=list(chunks);bad_headers=[dict(r)for r in headers]
        if kind=='float':
            bad=bytearray(bad_chunks[200]);bad[17]^=1;bad_chunks[200]=bytes(bad)
        elif kind=='missing':bad_chunks[200]=bad_chunks[200][:-4]
        elif kind=='cursor':bad_headers[200]['current_out']=str((int(bad_headers[200]['current_out'])+1)%32768)
        else:bad_headers[200]['volume']='3F000000'
        try:dac_gate(bad_chunks,bad_headers,pcm_headers)
        except ValueError as error:rejected.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted corrupted actual DAC transport/source: '+label)
    need(dac_gate(chunks,headers,pcm_headers)==positive,'Entire actual native DAC positive restored after effective RAM faults')
    return rejected

def predict_waveform(chunks,headers,pcm):
    # Exact original undersampled resampler at unit-gain mono speaker. Native
    # DAC source period and one-source-sample latency come from original
    # dcs.cpp/sound.cpp. No fitted offset, gain, tolerance or buffer search.
    predicted=[]
    for raw,r in zip(chunks,headers):
        frequency=(10000000//(2*(int(r['sclkdiv'],16)+1)*16)) if int(r['s1control'],16)&0x4000 else 31250
        need(frequency==31250,'This original native mono31250Hz source resampler contract')
        values=np.frombuffer(raw,'<f4')
        step=np.float32(frequency)/np.float32(48000);inv=np.float32(1.0/float(step))
        start=Decimal(r['seconds'])-Decimal('.02')
        adjusted=(start-Decimal(1)/frequency)*frequency
        source_index=int(adjusted.to_integral_value(rounding='ROUND_FLOOR'))
        source_position=np.float32(float(adjusted-source_index))
        # Current DAC stream is flushed through ceil(end); the four explicit
        # prefix samples precede the native callback's first consumed word.
        previous_end=int((start*frequency).to_integral_value(rounding='ROUND_CEILING'))
        at=4+source_index-previous_end
        need(0<=at<len(values),'Source-derived rebase fits actual explicitly captured DAC prefix')
        current=values[at];at+=1;mono=[]
        for _ in range(960):
            source_position=np.float32(source_position+step)
            if source_position<=1:sample=current
            else:
                source_position=np.float32(float(source_position)-1.0)
                old=current;need(at<len(values),'Entire actual original resampler neighbor retained');current=values[at];at+=1
                sample=np.float32(inv*np.float32(np.float32(old*np.float32(step-source_position))+np.float32(source_position*current)))
            sample=max(-1.0,min(1.0,float(sample)))
            mono.append(int(sample*32767.0))
        predicted.extend((v,v)for v in mono)
    guessed=np.asarray(predicted,dtype='<i2')
    need(guessed.shape==pcm.shape,'Every predicted original mixed PCM sample, no omitted tail or callback')
    mismatch=np.argwhere(guessed!=pcm)
    first=[]
    for sample,channel in mismatch[:16]:
        first.append(dict(stereoFrame=int(sample),callback=int(sample)//960+1,channel=int(channel),
                          sourcePrediction=int(guessed[sample,channel]),actualPCM=int(pcm[sample,channel])))
    return dict(passed=not len(mismatch),comparison='entire original float32 point/blend resampler and mono final conversion, no fitted parameters',
                comparedStereoFrames=len(pcm),differentChannelSamples=len(mismatch),firstDifferences=first,
                predictedSHA256=capture.digest(guessed.tobytes()),actualSHA256=capture.digest(pcm.tobytes()),
                independentOriginalStockMixedWaveformOracleAccepted=False)

source=capture.source
edits={
    '    chunks=[];pcm_headers=[];audio_guest=None':
    '    chunks=[];pcm_headers=[];audio_guest=None\n    dac_chunks=[];dac_headers=[]',
    "                if line.startswith(('MK2_BBAUDIO_PCM ','MK2_MAUDIO_GUEST ')):":
    """                if line.startswith('MK2_NATIVE_DAC_RAM '):
                    r=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
                    need(len(raw)==int(r['bytes']),'Complete original actual DAC ring segment inRAM')
                    r['sha256']=digest(raw);dac_chunks.append(raw);dac_headers.append(r)
                    out.write('MK2_NATIVE_DAC_RAM_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\\n')
                elif line.startswith(('MK2_BBAUDIO_PCM ','MK2_MAUDIO_GUEST ')):""",
    "    pcm=b''.join(chunks)":
    "    dac_proof=dac_gate(dac_chunks,dac_headers,pcm_headers);dac_rejected=dac_faults(dac_chunks,dac_headers,pcm_headers)\n"
    "    waveform=predict_waveform(dac_chunks,dac_headers,np.frombuffer(b''.join(chunks),'<i2').reshape(-1,2))\n"
    "    final.update(actualNativeDACSourceProof=dac_proof,effectiveActualNativeDACFaults=dac_rejected,nativeDACToMixedPCMComparison=waveform,actualNativeDACHeaders=dac_headers)\n"
    "    pcm=b''.join(chunks)",
}
for before,after in edits.items():
    need(source.count(before)==1,'Whole5533 actual physical/art/audio capture retained with additive passive DAC transport')
    source=source.replace(before,after,1)
scope=dict(capture.scope,ROOT=ROOT,BASE=BASE,LUA=LUA,COMPLETED=COMPLETED,dac_gate=dac_gate,dac_faults=dac_faults,predict_waveform=predict_waveform)
exec(compile(source,__file__+'.entire5533_actual_native_capture_plus_DAC_source_and_mixer_prediction','exec'),scope)
native_capture=scope['capture']

source=inspect.getsource(origin.run)
before="""    need(parent['passed'] and parent['goalStatus'] == 'active'
         and parent['allNormalBarakaVictimsAndSlotsObservedAnnouncerPriorityDeliveryAccepted'],
         'Completed actual both-victim/slot announcer proof and complete original remaining scope retained')"""
after="""    need(parent['passed'] and parent['goalStatus'] == 'active'
         and len(parent['actualOriginalDCSROMProof'])==2
         and all(r['wholeOriginalSoundRegionSourceExact']for r in parent['actualOriginalDCSROMProof']),
         'Actual complete original native sound firmware/data source and full remaining scope retained')"""
need(source.count(before)==1,'Whole5577 native audit starts from actual completed source-exact sound ROM proof')
source=source.replace(before,after,1)
edits={
    '    for p in (PARENT,Path(__file__),LUA,Path(announcer.__file__),Path(announcer.observed.__file__)):' :
    "    for p in (PARENT,Path(__file__),LUA,Path(announcer.__file__),Path(announcer.observed.__file__),\n"
    "              ROOT/'mame-mkp/src/mame/shared/dcs.cpp',ROOT/'mame-mkp/src/devices/sound/dmadac.cpp',\n"
    "              ROOT/'mame-mkp/src/devices/sound/dmadac.h',ROOT/'mame-mkp/src/emu/sound.cpp',\n"
    "              ROOT/'mame-mkp/src/emu/sound.h',ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp'):",
    "    record = capture.capture(('kano',1),guest,payload,gfx,reference,pins,image,True)":
    "    record = native_capture(('kano',1),guest,payload,gfx,reference,pins,image,True)",
    '    positive = gate(log,guest)':
    '    positive = gate(log,guest)\n    direct_positive=direct.gate(log,guest);direct_rejected=direct.faults(log,guest)',
    '        actualPacketOrigins=positive,effectiveActualPacketOriginFaults=rejected,retainedActualAnnouncerFaults=ann_faults,':
    '        actualPacketOrigins=positive,effectiveActualPacketOriginFaults=rejected,retainedActualAnnouncerFaults=ann_faults,\n'
    '        actualNativeDACSourceProof=meta["actualNativeDACSourceProof"],effectiveActualNativeDACFaults=meta["effectiveActualNativeDACFaults"],\n'
    '        nativeDACToMixedPCMComparison=meta["nativeDACToMixedPCMComparison"],qualifiedDirectSourceAndFullWordDelivery=direct_positive,\n'
    '        effectiveDirectSourceBranchAndPortFaults=direct_rejected,',
    "thisGoalTurnClassification='progress: actual original every-packet entry/caller/stack/return independently recorded, complete direct control packets and priority packets high/low/ADSP delivered;10new actual packet-origin faults plus12announcer/22priority faults, original full native physical/art/source voice/timer/RGB/PCM nonperturbance retained; exact direct original callers now available for semantic source decoding'":
    "thisGoalTurnClassification='progress: actual passive native DAC ring samples and real serial controls captured for every mixed PCM callback; complete original signed16-to-float normalization and exact ring/cursor/source/PCM associations independently qualified with effective actual RAM faults; entire prior physical/art/voice/packet/return/ADSP/timer/125-raster/full-PCM gates retained and original float32 resampler prediction compared to every actual output sample without fitted parameters or omitted tails'",
    "nextAction='Decode actual four original direct packet caller targets and control-word semantics from stock source; qualify source counterexamples without replay, then extend contexts and original waveform/all remaining requirement groups.'":
    "nextAction='Inspect the actual whole DAC-to-PCM source prediction result; qualify any original stream-clock/compressor differences from authoritative source and actual retained records, then bind independent stock waveform and broaden all original stage/move/finisher/CPU/campaign/UI/cleanup/release requirements.'",
}
for before,after in edits.items():
    need(source.count(before)==1,'Entire original5577 native physical/source/audio/terminal/storage audit retained: '+before)
    source=source.replace(before,after,1)
scope=dict(origin.__dict__,ROOT=ROOT,PARENT=PARENT,BASE=BASE,OUT=OUT,LUA=LUA,COMPLETED=COMPLETED,
           direct=direct,native_capture=native_capture,__file__=__file__)
exec(compile(source,__file__+'.entire5577_actual_native_audit_plus_readonly_native_DAC_source_and_waveform','exec'),scope)
run=scope['run']

if __name__=='__main__':
    need(not BASE.exists() and not OUT.exists(),'Fresh immutable actual native DAC source capture')
    try:report=run()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
                    goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','actualPacketOrigins',
        'effectiveActualPacketOriginFaults','retainedActualAnnouncerFaults','retainedActualPriorityFaults',
        'actualTimerCoverage','actualSourceVoiceEffectRoutes','completedNativeCaptures','qualifiedDirectSourceAndFullWordDelivery',
        'effectiveDirectSourceBranchAndPortFaults')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
