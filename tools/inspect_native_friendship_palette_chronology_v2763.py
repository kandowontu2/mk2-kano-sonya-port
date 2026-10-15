"""Typed native chronology comparison after the isolated palette patch.
Never normalize fighter ownership, inputs, health, poses, geometry, colors,
commands, frame numbers or teardown. Only independently allocated bubble
addresses, original lookup-task allocation addresses and <=4 PCM-sample
sub-frame cue offsets can differ. Full PCM remains a separate gate.
"""
import math
import inspect_current_friendship_palette_lifecycle_v2732 as old

life=old.life
ROOT=old.ROOT
need=old.need
LOOKUPS={0xff880770,0xff8808c0,0xff880960}

def check(actual,previous,actual_life,previous_life,actual_control,previous_control,fighter,side):
    physical=lambda rows:[(tag,dict(row)) for tag,row in rows if not tag.startswith('SHADOW_')]
    a,b=physical(actual),physical(previous)
    need(len(a)==len(b),'Same complete actual physical scene record count')
    current_alloc=life.check(actual_life,actual_control,fighter,side)
    prior_alloc=life.check(previous_life,previous_control,fighter,side) if previous_life else None
    states={life.number(row,'frame'):row for row in life.select(actual_life,'STATE')}
    previous_states={life.number(row,'frame'):row for row in life.select(previous_life,'STATE')}
    deltas=[]
    for index,((tag,new),(previous_tag,before)) in enumerate(zip(a,b)):
        need(tag==previous_tag,'Exact ordered actual physical record kinds')
        differences={key for key in set(new)|set(before) if new.get(key)!=before.get(key)}
        if not differences:continue
        record=dict(index=index,tag=tag,frame=life.number(new,'frame'),fields=sorted(differences))
        if 'seconds' in differences:
            need(tag in ('VOICE','AUDIO'),'Only real audio dispatch may differ within a native field')
            now,then=float(new['seconds']),float(before['seconds'])
            need(math.isfinite(now) and math.isfinite(then) and abs(now-then)<=4/48000,
                 'Actual within-field audio timestamp delta bounded to four 48kHz samples')
            record['audioOffsetSeconds']=now-then
            new.pop('seconds');before.pop('seconds');differences.remove('seconds')
        if tag=='ENTRY' and 'a13' in differences:
            need(life.pointer(new,'entry')==life.pointer(before,'entry') in LOOKUPS and
                 life.number(new,'frame')==actual_control['action']==previous_control['action'],
                 'Only original common lookup-task context at actual native activation')
            for row,membership in ((new,states),(before,previous_states)):
                need(life.number(row,'frame') in membership,'Actual lookup task has a real same-field list snapshot')
                state=membership[life.number(row,'frame')];task=life.pointer(row,'a13')
                need(task in life.nodes(state,'tasks') and task not in life.nodes(state,'freeTasks'),
                     'Lookup context is an independently observed active native task, not stale/free memory')
            record['lookupTaskAddresses']=[new['a13'],before['a13']]
            new.pop('a13');before.pop('a13');differences.remove('a13')
        if tag=='PART' and 'actor' in differences:
            need(fighter=='kano' and prior_alloc and life.pointer(new,'actor')==current_alloc['object'] and
                 life.pointer(before,'actor')==prior_alloc['object'],
                 'Both changed part addresses exactly independently allocated original bubble sprites')
            record['nativeBubbleAddresses']=[new['actor'],before['actor']]
            new.pop('actor');before.pop('actor');differences.remove('actor')
        if tag=='AUDIO' and 'timers' in differences:
            need(fighter=='kano' and prior_alloc and life.pointer(new,'command')==0x6ab4 and
                 life.number(new,'frame')==actual_control['action']+183,
                 'Only original pop dispatch observes attached bubble pointer in raw main+190 words')
            nw,bw=[int(v) for v in new['timers'].split(',')],[int(v) for v in before['timers'].split(',')]
            need(len(nw)==len(bw)==5 and nw[1]|nw[2]<<16==current_alloc['object'] and
                 bw[1]|bw[2]<<16==prior_alloc['object'] and [nw[i] for i in (0,3,4)]==[bw[i] for i in (0,3,4)],
                 'Raw audio observer main+190 attachment words match actual native bubble allocation; all other words unchanged')
            need(life.pointer(states[life.number(new,'frame')],'parentTrail')==current_alloc['object'] and
                 life.pointer(previous_states[life.number(before,'frame')],'parentTrail')==prior_alloc['object'],
                 'Actual same-field parent attachment independently contains corresponding allocated sprite')
            record['rawAttachmentPointers']=[current_alloc['object'],prior_alloc['object']]
            new.pop('timers');before.pop('timers');differences.remove('timers')
        need(not differences and new==before,
             'Every physical frame/input/fighter ownership/health/pose/geometry/color/WIN/cue/transition record unchanged except independently typed allocator addresses and bounded sub-frame audio '+str(record))
        deltas.append(record)
    return dict(actualCompletePhysicalRecords=len(a),typedAllocationAndSubFrameDifferences=deltas,
                allPhysicalFramesInputsFighterIdentityHealthPosesGeometryColorsAndNativeCuesUnchanged=True,
                fullPCMAcceptance=False)

def compare(folder,control,pin):
    meta=__import__('json').loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    fighter,side=meta['winner'],meta['side']
    if fighter=='kano':prior_folder=ROOT/f'audit_v2731_current_kano_friendship_palette_lifecycle_p{side}'
    elif side==2:prior_folder=ROOT/'audit_v2718_current_sonya_friendship_lifecycle_p2'
    else:prior_folder=ROOT/'audit_v2704_current_sonya_friendship_full_render_p1'
    actual=life.native.scene.previous.parse(folder/'run.log')
    previous=life.native.scene.previous.parse(prior_folder/'run.log')
    actual_life=life.parse(folder/'run.log');previous_life=life.parse(prior_folder/'run.log')
    pin(prior_folder/'run.log')
    prior_guest=life.native.scene.current.expected()[0]
    prior_control=life.native.inventory(previous,fighter,side,prior_guest,life.native.graphics.graphics({}))
    return check(actual,previous,actual_life,previous_life,control,prior_control,fighter,side)
