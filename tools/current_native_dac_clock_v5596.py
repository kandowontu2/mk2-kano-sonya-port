"""Original source-exact mixer floor clock and cached resampler view.

Preserve5593's measured discrepancy. The native sound manager uses floor
attoseconds per output sample; the stream buffer uses ceil attoseconds and
its requested speaker view rounds DOWN. Thus its first requested value is
the preceding cached resampler value, not the first newly generated value.
Derive that cache boundary from source clock arithmetic; no fitted shifts,
gain, tolerances or sample searches. Entire actual native run retained.
"""
import json, traceback
from decimal import Decimal
from pathlib import Path
import numpy as np
import current_native_dac_capture_v5593 as original

ROOT,need,sha=original.ROOT,original.need,original.sha
PARENT=original.OUT/'progress.json'
BASE=ROOT/'audit_v5597_current_native_dac_clock_ram'
OUT=ROOT/'audit_v5598_current_native_dac_clock_progress'
COMPLETED=[]
ATTO=10**18
FLOOR_OUTPUT_PERIOD=ATTO//48000
CEIL_OUTPUT_PERIOD=(ATTO+48000-1)//48000
INPUT_PERIOD=ATTO//31250

def clock(tick):
    mixer_start=(tick-1)*960*FLOOR_OUTPUT_PERIOD
    second,fraction=divmod(mixer_start,ATTO)
    read_index=fraction//CEIL_OUTPUT_PERIOD
    generated_index=(fraction+CEIL_OUTPUT_PERIOD-1)//CEIL_OUTPUT_PERIOD
    requested=second*ATTO+read_index*CEIL_OUTPUT_PERIOD
    generated=second*ATTO+generated_index*CEIL_OUTPUT_PERIOD
    need(generated-requested==CEIL_OUTPUT_PERIOD,'Original requested floor view precedes generated ceil stream by one output sample')
    adjusted=generated-INPUT_PERIOD
    source_index,remainder=divmod(adjusted,INPUT_PERIOD)
    return dict(tick=tick,mixerStartAttoseconds=mixer_start,requestedViewStartAttoseconds=requested,
                generatedStreamStartAttoseconds=generated,sourceIndex=source_index,
                sourceFraction=np.float32(remainder/INPUT_PERIOD))

def predict_waveform(chunks,headers,pcm):
    predicted=[];previous_tail=None;clocks=[]
    step=np.float32(31250)/np.float32(48000);inv=np.float32(1.0/float(step))
    def convert(value):return int(max(-1.0,min(1.0,float(value)))*32767.0)
    for raw,r in zip(chunks,headers):
        frequency=(10000000//(2*(int(r['sclkdiv'],16)+1)*16))if int(r['s1control'],16)&0x4000 else 31250
        need(frequency==31250,'Actual original native31250Hz mono source contract')
        stamp=Decimal(r['seconds']);tick=int(stamp*50)
        need(Decimal(tick)==stamp*50,'Actual exact50Hz host-independent sound callback')
        boundary=clock(tick);values=np.frombuffer(raw,'<f4');previous_end=(tick-1)*625
        if previous_tail is None:
            # Derive the preceding cached resampler value from its ORIGINAL
            # previous update's full float32 phase progression. Only its last
            # two source neighbors are needed; both are explicitly captured
            # in the four actual DAC prefix samples.
            old=clock(tick-1);position=old['sourceFraction'];index=old['sourceIndex'];crossed=False
            for _ in range(960):
                position=np.float32(position+step);crossed=position>1
                if crossed:position=np.float32(float(position)-1.0);index+=1
            at=4+index-previous_end
            need(0<=at<4 and (not crossed or at>0),'Original previous-update cache neighbors within actually captured prefix')
            tail=values[at]
            if crossed:
                tail=np.float32(inv*np.float32(np.float32(values[at-1]*np.float32(step-position))+np.float32(position*tail)))
            previous_tail=convert(tail)
        position=boundary['sourceFraction'];at=4+boundary['sourceIndex']-previous_end
        need(0<=at<len(values),'Exact source-clock new resampler view inside actual DAC capture')
        current=values[at];at+=1;generated=[]
        for _ in range(960):
            position=np.float32(position+step)
            if position<=1:sample=current
            else:
                position=np.float32(float(position)-1.0);old=current
                need(at<len(values),'All original source-clock resampler neighbors actually retained')
                current=values[at];at+=1
                sample=np.float32(inv*np.float32(np.float32(old*np.float32(step-position))+np.float32(position*current)))
            generated.append(convert(sample))
        requested=[previous_tail]+generated[:959]
        predicted.extend((v,v)for v in requested);previous_tail=generated[-1]
        clocks.append({k:float(v)if isinstance(v,np.float32)else v for k,v in boundary.items()})
    guessed=np.asarray(predicted,dtype='<i2')
    need(guessed.shape==pcm.shape,'Whole cached-view native waveform, no omitted first value or tail')
    mismatch=np.argwhere(guessed!=pcm)
    first=[dict(stereoFrame=int(s),callback=int(s)//960+1,channel=int(c),sourcePrediction=int(guessed[s,c]),actualPCM=int(pcm[s,c]))
           for s,c in mismatch[:16]]
    rejected=[]
    if not len(mismatch):
        bad=pcm.copy();bad[0,0]^=1
        need(not np.array_equal(guessed,bad),'Actual first PCM sample corruption rejected')
        rejected.append('actual first PCM sample corruption')
        bad=pcm.copy();bad[-1,1]^=1
        need(not np.array_equal(guessed,bad),'Actual final PCM sample corruption rejected')
        rejected.append('actual final PCM sample corruption')
        need(guessed.shape!=pcm[:-1].shape,'Actual omitted PCM tail rejected')
        rejected.append('actual last stereo frame omitted')
        wrong=np.asarray([v for pair in predicted[1:]for v in pair],dtype='<i2').reshape(-1,2)
        need(not np.array_equal(wrong,pcm),'Wrong original cached-view boundary rejected')
        rejected.append('original cached-view first value omitted')
    return dict(passed=not len(mismatch),comparedStereoFrames=len(pcm),differentChannelSamples=len(mismatch),
        firstDifferences=first,predictedSHA256=original.capture.digest(guessed.tobytes()),actualSHA256=original.capture.digest(pcm.tobytes()),
        originalFloorOutputPeriodAttoseconds=FLOOR_OUTPUT_PERIOD,originalCeilStreamPeriodAttoseconds=CEIL_OUTPUT_PERIOD,
        actualCallbackSourceClocks=clocks,effectiveActualWholeWaveformFaults=rejected,
        comparison='entire float32 original resampler, integer attosecond clock rounding, previous cached output and mono conversion; no fitted values',
        independentOriginalStockMixedWaveformOracleAccepted=False)

native_capture=original.native_capture
native_capture.__globals__.update(BASE=BASE,COMPLETED=COMPLETED,predict_waveform=predict_waveform)
source=original.source
before="""    need(parent['passed'] and parent['goalStatus'] == 'active'
         and len(parent['actualOriginalDCSROMProof'])==2
         and all(r['wholeOriginalSoundRegionSourceExact']for r in parent['actualOriginalDCSROMProof']),
         'Actual complete original native sound firmware/data source and full remaining scope retained')"""
after="""    need(parent['passed'] and parent['goalStatus']=='active'
         and parent['actualNativeDACSourceProof']['passed']
         and not parent['nativeDACToMixedPCMComparison']['passed'],
         'Actual native DAC source proof and measured original ideal-clock prediction discrepancy preserved')"""
need(source.count(before)==1,'Whole actual native audit preserves actual measured clock discrepancy')
source=source.replace(before,after,1)
before="              ROOT/'mame-mkp/src/emu/sound.h',ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp'):"
after="              ROOT/'mame-mkp/src/emu/sound.h',ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp',\n              Path(original.__file__),ROOT/'mame-mkp/src/emu/attotime.h'):"
need(source.count(before)==1,'Add exact original clock conversion source and preserve full previous native gates')
source=source.replace(before,after,1)
scope=dict(original.scope,ROOT=ROOT,PARENT=PARENT,BASE=BASE,OUT=OUT,COMPLETED=COMPLETED,
           native_capture=native_capture,original=original,__file__=__file__)
exec(compile(source,__file__+'.entire5593_native_audit_with_original_clock_and_cached_resampler_view','exec'),scope)
native_run=scope['run']

def run():
    report=native_run()
    waveform=report['nativeDACToMixedPCMComparison']
    report.update(allObservedKanoP1NativeDACToMixerWaveformSourceExact=waveform['passed'],
                  independentOriginalStockMixedWaveformOracleAccepted=False,
                  preservedMeasuredClockDiscrepancy=str(PARENT),fullPortAcceptance=False)
    report['thisGoalTurnClassification']='progress: entire actual native DAC-to-PCM waveform independently predicted using original integer attosecond floor/ceil clocks and source-derived previous cached speaker value, not fitted timing; complete685 callbacks/657600stereo frames compared with actual RAM PCM, effective first/last/missing/cache faults retained when positive; all prior physical/art/voice/direct-source/return/ADSP/timer and unchanged raster/full PCM proofs preserved; independent stock oracle and all other original scope remain unaccepted'
    return report

if __name__=='__main__':
    need(not BASE.exists() and not OUT.exists(),'Fresh immutable source-clock native waveform qualification')
    try:report=run()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
                    goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();original.capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','actualPacketOrigins',
        'effectiveActualPacketOriginFaults','retainedActualAnnouncerFaults','retainedActualPriorityFaults',
        'actualTimerCoverage','actualSourceVoiceEffectRoutes','completedNativeCaptures','qualifiedDirectSourceAndFullWordDelivery',
        'effectiveDirectSourceBranchAndPortFaults')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
