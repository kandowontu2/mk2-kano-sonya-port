"""Whole saved-pass native Knife renderer with original equations and RAM I/O.

Native CPU/DMA, packed row decoding, skips, scaling, flip and palette models
remain original. Only file reads become exact retained RAM buffer reads.
Each pass starts at its actual BEFORE-DMA anchor, never the target image.
This finite capture does not prove unsaved erasure or all CPU/arena contexts.
"""
import inspect
import json
import re
import textwrap
import traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
import capture_native_selector_walkin_knife_display_ram as capture
import inspect_secondary_display_v1231 as original
import inspect_native_scaled_arena_v1716 as scaling
from verify_cpu_pair_display_v635_v3 import group

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_walkin_knife_display_renderer_checked'


def once(source,before,after):
    need(source.count(before)==1,'Exactly original model RAM-I/O boundary '+before)
    return source.replace(before,after,1)


def data(text,display):
    groups=defaultdict(list)
    hexadecimal=original.HEX|{'op','before0','before1','before','after','first_source','row','effect_main',
        'parent','cursor','size','xy','b14','b10','a0','a1','a3','a7','entry','frame_table','descriptor',
        'field','p1','p2','main1','main2','word_F0','word_140','word_160','word_1A0','word_1D0',
        'parent_main','native_actor_owner','victim','victim_main','opcode'}
    strings=original.STR|{'register','words','reason','sha256'}
    for line in text.splitlines():
        match=re.match(r'MK2_NAT_CAMPAIGN_(FLOOR_\w+|SHADOW_\w+) ',line)
        if not match or match[1].endswith('_DIGEST'):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line);record=dict(pairs)
        need(len(pairs)==len(record),'Unique entire native drawing record')
        for key,value in record.items():
            if key not in strings:record[key]=int(value,16 if key in hexadecimal else 10)
        groups[match[1]].append(record)
    buffers={}
    for key,record in display['gfx'].items():
        buffers[key]=dict(key=key,offset=int(record['offset']),first=int(record['first']),
                          bytes=int(record['bytes']),data=record['raw'].hex())
    owners=defaultdict(list)
    for record in groups['FLOOR_OWNER']:owners[record['frame'],record['source'],record['slot']].append(record)
    return groups,buffers,None,None,owners


def bindings(text,display):
    scope=dict(vars(original),display=display)
    for method in ('begin','apply'):
        source=textwrap.dedent(inspect.getsource(getattr(original.Replay,method)))
        source=once(source,"(self.folder/base['file']).read_bytes()" if method=='begin' else
                          "(self.folder/d['file']).read_bytes()",
                          "display['buffers'][base['file']]" if method=='begin' else "display['buffers'][d['file']]")
        exec(compile(source,__file__+'::whole_original_'+method+'_RAM_read_only','exec'),scope)
    class Replay(original.Replay):
        begin=scope['begin']
        apply=scope['apply']
        def __init__(self,folder,groups,buffers,owners):
            super().__init__(folder,groups,buffers,owners);self.buffers=buffers
        scaled_dma=scaling.Replay.scaled_dma
        def dma(self,record):
            if record['width'] and record['height'] and (record['scaleX'] not in (0,256) or record['scaleY'] not in (0,256)):
                return self.scaled_dma(record)
            return super().dma(record)
    source=inspect.getsource(original.inspect)
    changes=(
        ("np.fromfile(folder/latch['file'],dtype='<u2')","np.frombuffer(display['buffers'][latch['file']],dtype='<u2')"),
        ("np.asarray(Image.open(folder/'snap'/snaps[frame]['file']).convert('RGB'))","display['rgb'][snaps[frame]['file']]"),
        ("(folder/display['palette_file']).read_bytes()","display_buffers[display['palette_file']]"),
        ('masks={n:crop(replay.body)==n for n in(1,2,3,4)}','masks={n:crop(replay.body)==n for n in(1,2,3,4)}'))
    # The original function uses local `display` for metadata; keep the RAM
    # namespace separate rather than altering actual latch/metadata equations.
    source=once(source,changes[0][0],changes[0][1].replace("display['buffers']","display_buffers"))
    source=once(source,changes[1][0],changes[1][1].replace("display['rgb']","display_rgb"))
    source=once(source,changes[2][0],changes[2][1])
    scope.update(Replay=Replay,data=lambda folder:data(text,display),
                 display_buffers=display['buffers'],display_rgb=display['rgb'])
    exec(compile(source,__file__+'::whole_original_cpu_DMA_flip_palette_renderer_RAM_only','exec'),scope)
    return scope['inspect']


def ownership(groups,payload,guest):
    born=groups['FLOOR_CHILD_SPAWN'];dead=groups['FLOOR_CHILD_RETIRE']
    need(len(born)==len(dead)==1 and (born[0]['frame'],dead[0]['frame'])==(2259,2312),
         'Actual current child allocation and original native removal')
    birth,retire=born[0],dead[0]
    need((birth['actor'],birth['main'],birth['parent'],birth['parent_main'],birth['native_actor_owner'],birth['victim_main'])==
         (0x01031d10,0x0106bf30,0x010350a0,0x0106a370,0x010350a0,0x0106b840) and
         birth['id']==birth['roster']==17 and birth['entry']==0xfffc6000 and birth['opcode']==0x09e0 and
         retire['actor']==birth['actor'] and retire['main']==birth['main'] and retire['entry']==0xff8b6820,
         'Independent actual true child/Main/parent/victim and source opcodes')
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
    need(len(queues)==len(groups['FLOOR_QUEUE']) and len(inventory)==len(groups['FLOOR_ALL_QUEUE']),
         'Whole native publication inventory, no hidden duplicate ownership')
    parts=defaultdict(list)
    for record in groups['FLOOR_QUEUE_PART']:parts[record['frame'],record['cursor']].append(record)
    counts=defaultdict(int)
    child_poses=set();child_sources=set()
    for key,q in queues.items():
        need(key in inventory and all(q[k]==inventory[key][k] for k in ('actor','source','pose','cache','id','body','facing','bank')),
             'Tracked native publication agrees with independent whole FIFO inventory')
        if q['slot']==3:
            need(birth['frame']<=q['frame']<=retire['frame'] and
                 (q['actor'],q['main'],q['owner'],q['parent'],q['id'],q['roster'],q['kind'])==
                 (birth['actor'],birth['main'],birth['actor'],birth['parent'],17,17,1),
                 'Actual projectile queue has original owner/Main/parent and live lifetime')
            child_poses.add(q['pose']);child_sources.add(q['source'])
        else:
            actor,main,identity=(0x01034e90,0x0106b840,18) if q['slot']==1 else (0x010350a0,0x0106a370,17)
            need(q['slot'] in (1,2) and (q['actor'],q['main'],q['owner'],q['parent'],q['id'],q['roster'],q['kind'])==
                 (actor,main,actor,actor,identity,identity,0),'True physical fighters and native ownership')
        composition=group(q,payload,guest)
        actual=parts[key]
        need(q['multipart']==1 and len(composition)==len(actual) and
             all(all(p[k]==v for k,v in expected.items()) for p,expected in zip(actual,composition)),
             'Every source composite equals actual native cached packed component')
        need(q['row']==q['cache']+q['part']*112 and q['pc']==0xff804420,
             'Exact original native cache iterator and FIFO publication PC')
        component=composition[q['part']]
        need(q['source']==component['source'] and (q['size']&65535,q['size']>>16)==(component['width'],component['height']) and
             q['command']>>16==component['command']|0x8002,'Entire actual source/size/flip command tuple')
        counts[q['slot']]+=1
    published=defaultdict(list)
    for q in queues.values():published[q['cursor']].append(q)
    dispatched={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    registers={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    need(len(dispatched)==len(groups['FLOOR_QUEUE_DISPATCH']) and set(registers)=={r['event'] for r in groups['FLOOR_DMA']},
         'Every actual native DMA command has executing register context')
    drawn=defaultdict(int)
    for d in groups['FLOOR_DMA']:
        candidates=[q for q in published[registers[d['event']]['b14']+192] if q['frame']<=d['frame']]
        q=max(candidates,key=lambda r:r['frame']) if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        need((d['event'] in dispatched)==owned and d['slot']==(q['slot'] if owned else 0),
             'Every actual DMA classified by executing FIFO cursor, never palette')
        if owned:
            dispatch=dispatched[d['event']]
            need(queues[dispatch['queue_frame'],dispatch['cursor']]==q and
                 d['source']==q['source'] and (d['width'],d['height'])==(q['size']&65535,q['size']>>16) and
                 d['command']==q['command']>>16 and d['palette']==q['bank']&0x7f00 and
                 (d['x'],d['y'])==(q['xy']&1023,q['xy']>>16&511),
                 'Complete queued source/size/command/palette/XY reaches actual native DMA')
            drawn[q['slot']]+=1
    need(counts[3]>30 and drawn[3]>30 and len(child_poses)>=16,'Complete actual Knife intro and flight publication/drawing')
    for key,q in inventory.items():
        if q['actor']==birth['actor'] and birth['frame']<=q['frame']<retire['frame']:
            need(key in queues and queues[key]['slot']==3,'No live child publication silently excluded')
        if q['frame']>retire['frame']:
            need(q['pose'] not in child_poses and q['source'] not in child_sources,'No old child artwork published after retirement/reuse')
    return dict(actualFIFOComponents=dict(counts),actualNativeDraws=dict(drawn),childSourcePoses=len(child_poses),
        completeNativePublications=len(inventory),nativeRetirementFrame=retire['frame'],sourceCompositeAndDMAExact=True)


def execute(state):
    need(not OUT.exists(),'New immutable full actual Knife renderer qualification')
    parent=json.loads((capture.OUT/'report.json').read_text())
    folder,text,_=capture.RAM_CASES[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY]
    need(parent['passed'] and held['process'].poll()==parent['nativeExit']==0 and
         parent['actualNativeIdentity']==held['identity'],'Same original current added display capture genuinely terminal')
    pins=dict(parent['inputHashes']);need(all(sha(p)==d for p,d in pins.items()),'Complete original capture and source hashes')
    display=capture.DISPLAY
    for record in display['gfx'].values():
        first=int(record['first']);raw=record['raw']
        need(raw==state['gfx32'][first:first+len(raw)],'Every actually used packed graphics byte equals independent current ROM/payload model')
    groups,*_=data(text,display)
    semantic=ownership(groups,state['payload'],state['guest'])
    render=bindings(text,display)
    positive=render(folder)
    need(positive['frames']==len(display['rgb']) and positive['frames']>100 and
         all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in positive['records']),
         'Every saved original native CPU/DMA/VRAM/palette/screenshot field is exact')
    sources=(Path(__file__).resolve(),Path(original.__file__).resolve(),Path(scaling.__file__).resolve(),
             ROOT/'tools/inspect_natural_arena_floor_v602.py',ROOT/'tools/verify_native_floor_display_v602.py',
             ROOT/'tools/verify_cpu_pair_display_v635_v3.py',capture.OUT/'report.json')
    for path in sources:
        key=str(path.resolve());digest=sha(path);need(key not in pins or pins[key]==digest,'No old executed model changed');pins[key]=digest
    need(all(sha(p)==d for p,d in pins.items()),'Whole source/native inventory after independent render')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],actualSourceFIFOAndDMA=semantic,
        wholeSavedNativePasses=positive,inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        exactWholeScreenPixels=sum(r['display_pixels'] for r in positive['records']),
        independentRendererAccepted=True,actualRenderFaultSuiteAccepted=False,actualVisualReviewAccepted=False,
        interPassEraseAccepted=False,allArenaCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS full actual Knife FIFO/cache/DMA and saved native RGB passes',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual renderer rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
