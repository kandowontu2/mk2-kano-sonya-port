"""Independently qualify actual3836 inflation FIFO/grounding and native erase.

Retained continuous source-bound whole-scene pixel replay is prerequisite.
No broad arena/floor-shadow/audio/ending/full-port acceptance is implied.
"""
import copy,hashlib,json,re,struct,subprocess,traceback,types
from collections import defaultdict
from pathlib import Path
import run_kitana_inflation_native_scene_v3920 as capture
from verify_cpu_pair_display_v635_v3 import group
import inspect_current_ground_shadow_v811 as shadow
ROOT,need,sha,model=capture.ROOT,capture.need,capture.sha,capture.model
OUT=ROOT/'audit_v3925_kitana_inflation_native_fifo_checked'

def shadow_contract(g):
    # Keep the entire original compressed-row/copy/pen/caller algorithm. Only
    # provide the actual observer's equivalent DMA/component row schema.
    namespace=dict(vars(shadow))
    namespace['rows']=lambda unused,tag:g[{'DMA':'FLOOR_DMA','SHADOW_COMPONENT':'SHADOW_COMPONENT'}[tag]]
    exact=types.FunctionType(shadow.check_shadow_rows.__code__,namespace)
    buffers={r['key']:r for r in g['FLOOR_GFX']}
    result=exact('',buffers)
    return {k:v for k,v in result.items()if k!='owned_events'}

def contract(g,guest,payload,identity,side):
    begin=g['FLOOR_BEGIN'];retired=g['FLOOR_RETIRED'];result=g['FLOOR_RESULT']
    need(len(begin)==len(retired)==len(result)==1,'Exactly one actual native victim window/removal/result')
    begin,retired,result=begin[0],retired[0],result[0];origin,end=begin['origin'],retired['frame']
    actors={s:g['FLOOR_STATE'][0][f'p{s}']for s in(1,2)};mains={s:g['FLOOR_STATE'][0][f'main{s}']for s in(1,2)}
    ids={side:identity,3-side:4};anchors={4:133,17:134,18:135}
    need(begin['id']==4 and begin['entry']==0xff8cc650 and begin['actor']==actors[3-side]and begin['main']==mains[3-side]and
         retired['p1']==retired['p2']==0 and retired['victim_health']==0 and retired['mode']in(3,5),'True native Kitana task and original both-pointer teardown')
    need(result['origin']==origin and result['retired']==end and result['snapshots']==end-origin+30 and
         [r['frame']for r in g['FLOOR_STATE']]==list(range(origin,end+31)),'Every physical state through real native disappearance plus30')
    for r in g['FLOOR_STATE']:
        need(all((r[f'p{s}']==actors[s]and r[f'main{s}']==mains[s]if r['frame']<end else r[f'p{s}']==0)and r[f'roster{s}']==ids[s]for s in(1,2))and
             all(0<=r[f'health{s}']<=161 for s in(1,2)),'No physical pointer/roster/health corruption across fatality')
    queues={(q['frame'],q['cursor']):q for q in g['FLOOR_QUEUE']};inventory={(q['frame'],q['cursor']):q for q in g['FLOOR_ALL_QUEUE']}
    transforms={(q['frame'],q['cursor']):q for q in g['FLOOR_QUEUE_TRANSFORM']}
    need(len(queues)==len(g['FLOOR_QUEUE'])and len(inventory)==len(g['FLOOR_ALL_QUEUE'])and set(transforms)==set(queues),'Unique complete actual FIFO inventory and camera transforms')
    parts=defaultdict(list);published=defaultdict(list);phases=defaultdict(set)
    for p in g['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
    for key,q in inventory.items():
        if q['actor']in actors.values():need(key in queues,'No hidden physical actor FIFO publication')
    for key,q in queues.items():
        s=q['slot'];need(s in(1,2)and q['actor']==q['owner']==q['parent']==actors[s]and q['main']==mains[s]and
            q['id']==q['roster']==ids[s]and q['kind']==0 and q['multipart']==1,'True physical FIFO identity/ancestry, never proxy')
        # Original drawing pass runs before the native task removes the actor
        # in that same field. Preserve and verify exact stream order; do not
        # mistake the preceding final draw for a post-removal publication.
        need(q['_observed_line']<retired['_observed_line'],'No physical FIFO publication after actual both-pointer teardown, exact within-field ordering')
        need(key in inventory and all(q[k]==inventory[key][k]for k in('actor','source','pose','cache','id','body','facing','bank','pc')),'Actual body FIFO agrees with complete native queue inventory')
        composition=group(q,payload,guest)
        need(len(composition)==len(parts[key])and all(all(p[k]==v for k,v in expected.items())for p,expected in zip(parts[key],composition)),'Every native source descriptor/component/offset/facing equals independent guest/payload')
        need(q['row']==q['cache']+112*q['part']and q['pc']==0xff804420,'Original native component-cache iterator')
        t=transforms[key];part=composition[q['part']]
        need(all(t[k]==q[k]for k in('slot','actor','main'))and t['world']==((q['y']&65535)<<16)|(q['x']&65535)and
             t['floor']==q['floor']==t['stageY']-anchors[q['id']],'Actual unchanged native world/camera/floor origin')
        signed=model.erase.short;x,y=signed(t['world']),signed(t['world']>>16)
        if not t['a7']&1:x-=signed(t['camera']);y-=signed(t['camera']>>16)
        x-=part['dx'];y-=part['dy'];command=q['command']>>16
        if command&16:x+=part['width']-1
        if command&32:y+=part['height']-1
        x+=signed(t['display']);y+=signed(t['display']>>16)
        need((q['xy']&1023,q['xy']>>16&511)==(x&1023,y&511),'Exact native descriptor/camera/display projection, no compensating overlay')
        published[q['cursor']].append(q)
        if s==side and 0xfffd8c00<=q['pose']<0xfffd8f00:phases[q['pose']].add(q['frame'])
    dmas={r['event']:r for r in g['FLOOR_DMA']};regs={r['event']:r for r in g['FLOOR_DMA_REGS']};dispatch={r['event']:r for r in g['FLOOR_QUEUE_DISPATCH']}
    need(len(dmas)==len(g['FLOOR_DMA'])and len(dispatch)==len(g['FLOOR_QUEUE_DISPATCH'])and set(regs)==set(dmas),'Every actual DMA and original cursor recorded')
    draws=defaultdict(int)
    for event,d in dmas.items():
        candidates=[q for q in published[regs[event]['b14']+192]if q['frame']<=d['frame']]
        q=max(candidates,key=lambda r:r['frame'])if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        need((event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),'Actual DMA body ownership recomputed by FIFO cursor, never palette')
        if not owned:continue
        actual=dispatch[event];part=group(q,payload,guest)[q['part']]
        need(queues[actual['queue_frame'],actual['cursor']]==q and all(actual[k]==q[k]for k in('actor','main','slot'))and
            d['source']==part['source']and(d['width'],d['height'])==(part['width'],part['height'])and
            d['command']==part['command']|0x8002 and(q['xy']&1023,q['xy']>>16&511,q['bank']&0x7f00)==(d['x'],d['y'],d['palette']),
            'Native consumer preserves original queued owner/source/size/facing/position/palette')
        draws[q['slot']]+=1
        if q['slot']==side and 0xfffd8c00<=q['pose']<0xfffd8f00:
            t=transforms[q['frame'],q['cursor']]
            ground=t['stageY']+5+t['displayY']-t['cameraY']-1-(t['displayY']&256)
            need(q['y']==q['floor']and(d['y']&255)+d['height']-1==ground,'Every owned inflation/burst phase genuinely contacts native raster floor')
    phase_start=0xfffd8c00+(identity-17)*6*64;count=6
    ages=(181,213,221,229,237,353)if side==1 else(182,214,222,230,238,354)
    lengths=(32,8,8,8,116,3)
    need(set(phases)=={phase_start+i*64 for i in range(count)}and all(phases[phase_start+i*64]==set(range(origin+age,origin+age+length))for i,(age,length)in enumerate(zip(ages,lengths))),'All six original native inflation/burst phase cadence fields retained exactly')
    need(all(draws[s]>0 for s in(1,2)),'Both true physical characters publish and draw')
    own_shadows=shadow_contract(g)
    return dict(origin=origin,disappearance=end,trueIds=ids,sourceBoundProjections=len(queues),originalOwnedBodyDispatches=dict(draws),
        nativePhaseFields={f'{p:08X}':sorted(f)for p,f in phases.items()},floorShadowCopyCommands=sum(d['command']&15==8 for d in dmas.values()),
        actualOwnedCompressedShadowRows=own_shadows,allArenaFloorShadowsAccepted=False)

def run():
    need(not OUT.exists(),'Fresh immutable native FIFO proof')
    base_guest,_,base_payload,_,_=capture.data.old.expected_current();payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=capture.data.check(base_payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base_guest,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    matrix=json.loads((ROOT/'audit_v3922_kitana_inflation_native_scene_observed/report.json').read_text())
    need(matrix['passed']and len(matrix['cases'])==4,'All four actual continuous native source-bound pixel contexts passed')
    pins={};cases=[]
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        folder=ROOT/f'audit_v3921_kitana_{fighter}_p{side}_native_scene_ram';meta=json.loads((folder/'result.json').read_text());text=(folder/'run.log').read_text()
        need(meta['exit_code']==0 and meta['candidate']==capture.NAME and not meta['modelErrors']and meta['ramGuestSHA256']==model.digest(guest),'Actual immutable3836 terminal/whole guest/pixel replay')
        for p,h in meta['input_hashes'].items():need(sha(p)==h,'Executed input unchanged');pins[p]=h
        need(not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav'))and not list(folder.rglob('display*.bin')),'No raw runtime raster/VRAM/audio copies')
        g=defaultdict(list)
        for line_index,line in enumerate(text.splitlines()):
            p=model.parse(line)
            if p and p[0]!='FLOOR_CPU':p[1]['_observed_line']=line_index;g[p[0]].append(p[1])
        identity=17 if fighter=='kano'else 18;positive=contract(g,guest,payload,identity,side);faults=[]
        own_index=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==side and 0xfffd8c00<=r['pose']<0xfffd8f00)
        q=g['FLOOR_QUEUE'][own_index];key=(q['frame'],q['cursor'])
        trials=[('proxy_id','FLOOR_QUEUE',own_index,'id',1),('wrong_owner','FLOOR_QUEUE',own_index,'owner',0),
            ('wrong_cached_row','FLOOR_QUEUE',own_index,'row',0),('wrong_source','FLOOR_QUEUE',own_index,'source',0),
            ('wrong_native_xy','FLOOR_QUEUE',own_index,'xy',q['xy']^1)]
        i=next(i for i,r in enumerate(g['FLOOR_QUEUE_TRANSFORM'])if(r['frame'],r['cursor'])==key)
        trials.append(('shifted_backdrop_projection','FLOOR_QUEUE_TRANSFORM',i,'camera',g['FLOOR_QUEUE_TRANSFORM'][i]['camera']^1))
        i=next(i for i,r in enumerate(g['FLOOR_QUEUE_PART'])if(r['frame'],r['cursor'])==key)
        trials.append(('wrong_owned_art_width','FLOOR_QUEUE_PART',i,'width',g['FLOOR_QUEUE_PART'][i]['width']+1))
        i=next(i for i,r in enumerate(g['FLOOR_QUEUE_DISPATCH'])if r['slot']==side)
        trials.append(('wrong_consumer_slot','FLOOR_QUEUE_DISPATCH',i,'slot',3-side))
        trials.extend([('wrong_teardown_pointer','FLOOR_RETIRED',0,'p1',1),('wrong_live_identity','FLOOR_STATE',0,f'roster{side}',1)])
        component=g['SHADOW_COMPONENT'][0]
        trials.extend([('wrong_shadow_owner','SHADOW_COMPONENT',0,'owner',0),('wrong_shadow_row_source','SHADOW_COMPONENT',0,'first_source',component['first_source']^1)])
        index=next(i for i,r in enumerate(g['FLOOR_DMA'])if r['event']==component['event'])
        trials.append(('wrong_native_shadow_caller','FLOOR_DMA',index,'pc',0))
        for label,tag,index,key,value in trials:
            changed=copy.deepcopy(g);changed[tag][index][key]=value
            try:contract(changed,guest,payload,identity,side)
            except (ValueError,KeyError,AssertionError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual-row fault accepted '+label)
            need(contract(g,guest,payload,identity,side)==positive,'Exact positive restored after actual-row corruption')
        records=json.loads((folder/'continuous_scene_records.json').read_text());later=[r for r in records if r['frame']>=positive['disappearance']+3]
        need(len(records)==meta['observedRGBFields']==meta['modelExactFields']and[ r['frame']for r in records]==list(range(positive['origin']+1,positive['disappearance']+31))and
            all(r['body'][str(side)]['pixels']==0 and r['shadowPixels']==0 for r in later),'Complete exact native display and erased victim, no persistent shadow/image after removal')
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        cases.append(dict(fighter=fighter,side=side,exactFields=len(records),nativeFIFO=positive,actualRowFaultsRejected=faults,postRemovalPixels=0))
    for p in(Path(__file__).resolve(),Path(shadow.__file__),ROOT/'audit_v3922_kitana_inflation_native_scene_observed/report.json'):pins[str(p)]=sha(p)
    return dict(passed=True,actualContexts=4,exactFields=sum(c['exactFields']for c in cases),actualRowFaultsRejected=52,cases=cases,
        actualNativeVictimArtFIFOProjectionDisplayEraseAccepted=True,artAestheticReviewPending=True,
        allArenaFloorShadowsAccepted=False,fullVictimAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Inherited compression')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
