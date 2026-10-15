"""Native Sonya control after shared palette routing changes.
Random cluck variants need not repeat an earlier RNG sequence. Require the
unchanged original native RNG/hold/channel code and independently replayed
first-free voice allocation. All cue frames, body geometry and game inputs
remain exact. Full audible PCM is a separate, unaccepted gate.
"""
import copy
import inspect_current_friendship_palette_lifecycle_v2732 as old
import inspect_native_friendship_palette_chronology_v2763 as typed
import verify_native_friendship_audio_v791 as audio

ROOT=old.ROOT
life=old.life
need=old.need

def compare(folder,control,pin,guest):
    side=int(__import__('json').loads((folder/'result.json').read_text(encoding='utf-8-sig'))['side'])
    actual=life.native.scene.previous.parse(folder/'run.log')
    previous_folder=ROOT/(f'audit_v2718_current_sonya_friendship_lifecycle_p2' if side==2 else 'audit_v2704_current_sonya_friendship_full_render_p1')
    pin(previous_folder/'run.log')
    previous=life.native.scene.previous.parse(previous_folder/'run.log')
    old_guest=life.native.scene.current.expected()[0]
    for first,last in ((0xfa200,0xfa700),((0xff80eae0-0xff800000)//8,(0xff80ed00-0xff800000)//8)):
        need(guest[first:last]==old_guest[first:last],'Entire native cluck RNG, original holds, stream callbacks and channel allocation code unchanged')
    pin(ROOT/'tools/verify_native_friendship_audio_v791.py')
    native=audio.runtime(actual,'sonya',side,'positive')
    old_native=audio.runtime(previous,'sonya',side,'positive')
    need(native['cues']==old_native['cues'] and native['ages']==old_native['ages'],
         'All original chicken cues retain exact native frame/pose cadence, independent of RNG variants')
    actual_life=life.parse(folder/'run.log');integrity=life.check(actual_life,control,'sonya',side)
    states={life.number(row,'frame'):row for row in life.select(actual_life,'STATE')}
    a=[(tag,dict(row)) for tag,row in actual if not tag.startswith('SHADOW_')]
    b=[(tag,dict(row)) for tag,row in previous if not tag.startswith('SHADOW_')]
    need(len(a)==len(b),'Same complete physical Sonya scene records')
    changes=[]
    for index,((tag,new),(old_tag,before)) in enumerate(zip(a,b)):
        need(tag==old_tag,'Same ordered physical Sonya record kinds')
        changed={key for key in set(new)|set(before) if new.get(key)!=before.get(key)}
        if not changed:continue
        record=dict(index=index,tag=tag,frame=life.number(new,'frame'),fields=sorted(changed))
        if tag in ('VOICE','AUDIO'):
            # This comparison is field-level. Complete PCM fidelity is never
            # inferred from different builds' within-field timestamps.
            for key in ('seconds',):new.pop(key,None);before.pop(key,None)
            if tag=='AUDIO':
                # Both complete sequences were independently checked above,
                # including every true owner, hold and first-free channel.
                for key in ('command','timers'):new.pop(key);before.pop(key)
        if tag=='ENTRY' and 'a13' in changed:
            need(life.pointer(new,'entry')==life.pointer(before,'entry') in typed.LOOKUPS and
                 life.number(new,'frame')==control['action'],'Only original common activation lookup context differs')
            state=states[life.number(new,'frame')];task=life.pointer(new,'a13')
            need(task in life.nodes(state,'tasks') and task not in life.nodes(state,'freeTasks'),
                 'Actual changed Sonya lookup context is a real active native task')
            new.pop('a13');before.pop('a13')
        need(new==before,'Every Sonya physical input/frame/ownership/health/pose/geometry/color/WIN/transition remains exact '+str(record))
        changes.append(record)
    outcomes=[]
    for name,key,transform,label in (
        ('wrong_audio_owner','id',lambda r:'1','Audio belongs to wrong actor/task'),
        ('wrong_original_free_voice','command',lambda r:f'{life.pointer(r,"command")+1:04X}','Not original first-free independent voice allocation'),
        ('wrong_native_cluck_hold','timers',lambda r:','.join([str(int(r['timers'].split(',')[0])+1)]+r['timers'].split(',')[1:]),'Native hold timers or overlap changed')):
        corrupted=copy.deepcopy(actual);at=next(i for i,(tag,row) in enumerate(corrupted) if tag=='AUDIO')
        corrupted[at][1][key]=transform(corrupted[at][1])
        try:audio.runtime(corrupted,'sonya',side,'positive')
        except ValueError as error:
            need(label in str(error),'Intended native Sonya audio rejection '+name)
            outcomes.append(dict(name=name,rejectedBy=str(error)))
        else:raise ValueError('Corrupted Sonya native audio accepted '+name)
    need(audio.runtime(actual,'sonya',side,'positive')==native,'Final original native Sonya audio control')
    return dict(actualCompletePhysicalRecords=len(a),nativeCluckSourceAndFirstFreeVoices=native,
                actualDifferentNativeRNGRecords=changes,allPhysicalInputsFramesIdentitiesHealthPosesGeometryColorsAndTransitionsUnchanged=True,
                nativeListIntegrity=integrity,rejectedNativeAudioCounterexamples=outcomes,
                priorLookupAllocationAddressBindingAvailable=side==2,fullPCMAcceptance=False)
