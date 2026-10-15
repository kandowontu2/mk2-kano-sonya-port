"""Same actual PCM; bind replacement between speaker callbacks to real next source."""
import gzip,inspect,json
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_native_current_attract_phase484 as original
ROOT,need,sha=original.ROOT,original.need,original.sha

def channels(c,model):
    # All precise pointer/length/position/EOF checks stay in the whole original
    # gate. The ownership timer may flush a source between PCM snapshots; the
    # next real source, not an absent exact-cutoff snapshot, proves replacement.
    events=model['events'];square=next(e for e in events if e['marker']['word']=='6B00')
    bicycle=next(e for e in events if e['marker']['word']=='6B01')
    replacement=square['replacement'];at=Decimal(bicycle['marker']['seconds'])
    precise=original.early.names.audio.rows(c['text'],'MK2_TOMB_MIX_CHANNEL')
    before=max((r for r in precise if r['channel']=='10' and Decimal(r['seconds'])<at),key=lambda r:Decimal(r['seconds']))
    after=min((r for r in precise if r['channel']=='10' and Decimal(r['seconds'])>=at),key=lambda r:Decimal(r['seconds']))
    atto=original.early.names.audio.ATTO
    need(Decimal(before['seconds'])*atto<replacement['lastStreamUpdate']==replacement['previousNativeOwnershipTick']<at*atto and
         replacement['generatedBeforeReplacement']==square['count']<len(square['signal']) and
         before['length']==str(square['length']) and before['sample']=='4294967295' and
         float(before['position'])<square['count'] and after['sample']=='14' and
         after['length']==str(bicycle['length']) and 0<float(after['position'])<bicycle['length'],
         'Independent actual old/new channel snapshots bracket the real native timer replacement between PCM callbacks')
    source=inspect.getsource(original.compound.channels)
    before_test="if event['marker']['word']=='6B00' and count==event['count']:"
    after_test="if event['marker']['word']=='6B01' and count>0:"
    need(source.count(before_test)==1,'Exact original stronger replacement-presence predicate')
    source=source.replace(before_test,after_test,1)
    scope=dict(vars(original.compound))
    exec(compile(source,__file__+'::whole_original_precise_channels_with_bound_real_replacement','exec'),scope)
    result=scope['channels'](c,model)
    return dict(result,realReplacementBetweenSpeakerCallbacks=True,
        actualLastSquareSnapshotIndex=int(before['index']),actualFirstBicycleSnapshotIndex=int(after['index']))

def qualify(c):
    failure=json.loads((c['folder']/'first_source_EOF_checker_failure.json').read_text())
    need(failure['checkerFailure'] and not failure['nativeGameFailure'] and
         failure['failedCheckerSourceSHA256']==sha(original.__file__),
         'Actual original failed checker source remains frozen')
    source=inspect.getsource(original.qualify)
    changes=[('current_native_audio_checked.json','current_native_audio_checked_v2.json'),
        ('executed_current_audio_sources.json.gz','executed_current_audio_sources_v2.json.gz'),
        ('compound.channels(','channels(')]
    for before,after in changes:
        count=3 if before=='compound.channels(' else 2 if before=='executed_current_audio_sources.json.gz' else 1
        need(source.count(before)==count,'Whole original qualification adaptation '+before)
        source=source.replace(before,after)
    scope=dict(vars(original),__file__=__file__,channels=channels)
    exec(compile(source,__file__+'::whole_original_PCM_and_source_faults','exec'),scope)
    receipt=scope['qualify'](c)
    # Effective independent source counterexamples, using the complete actual
    # buffer rather than the stronger gate's boolean alone.
    predicted,actual,model,_=original.predict(c)
    square=next(e for e in model['events'] if e['marker']['word']=='6B00')
    extend=original.compound.contribution(c,square,True)-original.compound.contribution(c,square,False)
    convert=lambda signal:(np.clip(signal,-1,1).astype(np.float64)*32767).astype('<i2')
    wrongs=[('native DCS source omitted',convert(model['voice'])),
        ('Square wrongly continues to EOF after Bicycle replaces it',convert(np.float32(model['dcs']+np.float32(model['voice']+extend))))]
    faults=[]
    for label,wrong in wrongs:
        count=int(np.count_nonzero(wrong!=actual));need(count>0,'Nonvacuous complete native source fault '+label)
        faults.append(dict(fault=label,differentSamples=count))
    path=c['folder']/'actual_native_source_replacement_faults_v2.json'
    need(not path.exists(),'Fresh finite source-replacement fault proof')
    path.write_text(json.dumps(dict(passed=True,wholeActualPositiveRestored=np.array_equal(predicted,actual),
        nativeGameSourceChanged=False,actualCounterexamples=faults,
        sourceHashes={str(Path(__file__).resolve()):sha(__file__),str(Path(original.__file__).resolve()):sha(original.__file__)},
        failedOriginalCheckerPreserved=True,fullPortAcceptance=False),indent=2)+'\n')
    with gzip.open(c['folder']/'executed_replacement_qualification_v2.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(wholeQualificationSource=source,wholeReplacementGate=inspect.getsource(channels),
            wrapperSource=Path(__file__).read_text()),f)
    print(json.dumps(dict(passed=True,actualSourceFaults=faults,entirePCMFrames=len(actual))),flush=True)
    return receipt
