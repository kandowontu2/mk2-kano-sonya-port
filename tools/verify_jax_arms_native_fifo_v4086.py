"""Native Jax arm-rip physical FIFO/projection/floor/shadow and prop-source proof.

Retain the complete3994 generic FIFO/cache/component/DMA/projection proof and
811 compressed native shadow-row algorithm. Replace only split-specific
actor/hat/cadence construction with actual original Jax state and five body
groups. Two actual palette-router props bind original single descriptors,
cadence, FIFO cursors and DMA. Prop world/camera motion is not separately
logged: complete4074 native CPU/DMA pixel replay covers its rendered result.
Dead Pool normal costume only, not every arena/alternate/audio/ending.
"""
import copy,inspect,json,re,struct,subprocess,traceback
from collections import defaultdict
from pathlib import Path
import run_jax_arms_native_scene_v4074 as capture
import verify_jax_arms_earned_v4078 as grammar
import verify_kung_lao_split_native_fifo_v3994 as old
ROOT,need,sha,model=capture.ROOT,capture.need,capture.sha,capture.model
OUT=ROOT/'audit_v4087_jax_arms_native_fifo_checked'

def make_contract():
    source=inspect.getsource(old.contract)
    before='    ids={side:identity,3-side:0};anchors={0:140,17:134,18:135}'
    need(source.count(before)==1,'One original physical identity/anchor declaration')
    source=source.replace(before,'    ids={side:identity,3-side:11};anchors={11:139,17:134,18:135}')
    first=source.index("    secondary={q['actor']")
    last=source.index("    for r in g['FLOOR_STATE']:",first)
    source=source[:first]+"""    phase_targets=set(struct.unpack_from('<5I',guest,0xfb980+(identity-17)*48))
    grammar.source_contract(guest)
    need(not any(q['slot']==3 for q in g['FLOOR_QUEUE']),'Jax arm-rip has no mirrored secondary victim; detached props have separate actual ID0')
    need(begin['id']==11 and begin['entry']==0xff8be240 and begin['actor']==actors[3-side]and begin['main']==mains[3-side]and
         retired['p1']==retired['p2']==0 and retired['victim_health']==0 and retired['mode']in(3,5),'True original Jax and actual both-pointer teardown')
    need(result['origin']==origin and result['retired']==end and result['snapshots']==end-origin+30 and
         [r['frame']for r in g['FLOOR_STATE']]==list(range(origin,end+31)),'Every physical state through native disappearance plus30')
"""+source[last:]
    changes={
      "active=q['actor']in(actors[1],actors[2])or(q['actor']==actors[3]and q['frame']>=creation)":"active=q['actor']in(actors[1],actors[2])",
      "s=q['slot'];owner=actors[side]if s==3 else actors.get(s)":"s=q['slot'];owner=actors.get(s)",
      "allowed_owner=hat if s==3-side and hat_owner_first<=q['frame']<hat_owner_first+12 else owner":"allowed_owner=owner",
      "s in(1,2,3)":"s in(1,2)",
      "q['kind']==(1 if s==3 else 0)":"q['kind']==0 ",
      "s in(side,3)and 0xfffdf100<=q['pose']<0xfffdf600":"s==side and q['pose']in phase_targets",
      "q['slot']in(side,3)and 0xfffdf100<=q['pose']<0xfffdf600":"q['slot']==side and q['pose']in phase_targets",
    }
    for before,after in changes.items():
        count=2 if before=='s in(1,2,3)'else 1
        need(source.count(before)==count,'Exact actual Jax physical actor/group adaptation '+before);source=source.replace(before,after)
    first=source.index('    phase_start=')
    last=source.index('    own_shadows=shadow_contract(g)',first)
    source=source[:first]+"""    need(set(phases)=={(side,p)for p in phase_targets}and all(phases[side,p]for p in phase_targets),'All five original native own arm-rip body groups genuinely publish')
    need(all(draws[s]>0 for s in(1,2)),'Both actual physical fighters publish and draw')
"""+source[last:]
    namespace=dict(vars(old));namespace.update(capture=capture,grammar=grammar)
    exec(compile(source,__file__+'::whole_generic_FIFO_Jax_physical_actor_binding','exec'),namespace)
    return namespace['contract']

def parsed(text):
    groups=defaultdict(list)
    for index,line in enumerate(text.splitlines()):
        p=model.parse(line)
        if p and p[0]!='FLOOR_CPU':p[1]['_observed_line']=index;groups[p[0]].append(p[1])
    return groups

def prop_contract(g,text,guest,identity,side):
    rows=capture.arm_art.prior.rows(text,'MK2_ARM_PALETTE_V1073')
    entries=[r for tag,r in rows if tag=='ENTRY'];exits=[r for tag,r in rows if tag=='STOCK_FALLBACK']
    actions=capture.arm_art.prior.rows(text,'MK2_STOCK_HEAD_V921');action=next(r for tag,r in actions if tag=='ACTION')
    need(len(entries)==len(exits)==2 and len({r['prop']for r in entries})==2,'Two genuine original palette-router detached props, not duplicated actor aliases')
    need(not capture.arm_art.check_palette_route(text,action,identity,False),'Entire original1074 prop register/stack/status/true-victim normal route')
    end=g['FLOOR_RETIRED'][0]['frame'];props={int(r['prop'],16)for r in entries};births={int(r['prop'],16):int(r['frame'])for r in entries}
    need(not props&{g['FLOOR_STATE'][0][f'p{s}']for s in(1,2)},'Detached props are two separate allocator addresses, not either physical fighter')
    descriptors=struct.unpack_from('<6I',guest,0xfb980+(identity-17)*48+24);need(descriptors[-1]==0,'Five original single-frame arm descriptors with sentinel')
    specs={pointer:struct.unpack_from('<4hIHIH',guest,(pointer-0xff800000)//8)for pointer in descriptors[:5]}
    queues=[q for q in g['FLOOR_ALL_QUEUE']if q['actor']in props and q['frame']>=births[q['actor']]]
    phases=defaultdict(set)
    for q in queues:
        need(q['cache']in specs and q['id']==0 and q['body']==q['pose']==0 and q['_observed_line']<g['FLOOR_RETIRED'][0]['_observed_line'],'Actual native single-frame prop ID0/cache/lifetime; no hidden physical fighter or recycled blood task')
        spec=specs[q['cache']]
        need(q['source']==spec[4]and spec[5]==0x6000 and spec[6]==0xff800000+(0xfda00 if identity==17 else 0xfdb00)*8 and spec[7]==0,'Actual prop FIFO source and whole true own palette/descriptor')
        phases[q['actor'],q['cache']].add(q['frame'])
    for actor in props:
        first=births[actor]+1
        for index,pointer in enumerate(descriptors[:5]):
            lo=first+4*index;hi=lo+4 if index<4 else end
            need(phases[actor,pointer]==set(range(lo,hi)),'Both independently allocated arms retain every original four-field phase and terminal held source')
    inventory=defaultdict(list)
    for q in g['FLOOR_ALL_QUEUE']:inventory[q['cursor']].append(q)
    regs={r['event']:r for r in g['FLOOR_DMA_REGS']};draws=[]
    physical_palette={(q['frame'],q['bank']&0x7f00)for q in g['FLOOR_QUEUE']if q['slot']==side}
    for d in g['FLOOR_DMA']:
        cursor=regs[d['event']]['b14']+192
        before=[q for q in inventory[cursor]if q['_observed_line']<d['_observed_line']]
        q=max(before,key=lambda q:q['_observed_line'])if before else None
        if not(q and q['actor']in props and q['frame']>=births[q['actor']]and d['command']&15==2 and d['source']==q['source']):continue
        spec=specs[q['cache']]
        need(d['slot']==0 and(d['width'],d['height'])==spec[:2]and d['command']==spec[5]|(q['facing']&0x30)|0x8002 and
             d['palette']==q['bank']&0x7f00 and(q['frame'],d['palette'])in physical_palette,'Exact original single-prop FIFO cursor/source/dimensions/facing/own-normal palette reaches native DMA; no physical-slot relabelling')
        draws.append(dict(event=d['event'],frame=d['frame'],actor=q['actor'],descriptor=q['cache'],source=d['source'],width=d['width'],height=d['height'],palette=d['palette']))
    need({r['actor']for r in draws}==props and {r['descriptor']for r in draws}==set(descriptors[:5]),'Both real arm props and all five true source phases genuinely DMA draw')
    return dict(actualProps=sorted(props),sourceBoundPropFIFO=len(queues),originalPropDMAs=len(draws),nativeFourFieldCadenceAccepted=True,actualOwnPaletteFamilyAccepted=True,
        sourceBoundDescriptorConsumers=sorted({r['descriptor']for r in draws}),separatePropWorldCameraProjectionAccepted=False,completeNativeCPUSceneReplayRequired=True)

def expected():
    base,_,prior,_,_=capture.data.old.expected_current();payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=capture.data.check(prior,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    return guest,payload

def run():
    need(not OUT.exists(),'Fresh immutable FIFO qualification')
    scene=json.loads((capture.OUT/'report.json').read_text());state=json.loads((grammar.OUT/'report.json').read_text())
    need(scene['passed']and state['passed']and len(scene['cases'])==4 and state['actualContexts']==4,'Four complete actual native arm scenes and whole earned-state/prop palette contexts')
    guest,payload=expected();contract=make_contract();cases=[];pins={}
    for fighter in('kano','sonya'):
        for side in(1,2):
            folder=ROOT/f'audit_v4075_jax_arms_{fighter}_p{side}_native_scene_ram';meta=json.loads((folder/'result.json').read_text());text=(folder/'run.log').read_text()
            need(meta['exit_code']==0 and not meta['modelErrors']and meta['observedRGBFields']==meta['modelExactFields']and meta['ramGuestSHA256']==model.digest(guest),'Actual whole-scene terminal/guest/pixel replay')
            g=parsed(text);identity=17 if fighter=='kano'else 18;positive=contract(g,guest,payload,identity,side);prop_positive=prop_contract(g,text,guest,identity,side);faults=[]
            phases=set(struct.unpack_from('<5I',guest,0xfb980+(identity-17)*48))
            own=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==side and r['pose']in phases);q=g['FLOOR_QUEUE'][own];key=q['frame'],q['cursor']
            trials=[('proxy_id','FLOOR_QUEUE',own,'id',1),('wrong_owner','FLOOR_QUEUE',own,'owner',0),('wrong_main','FLOOR_QUEUE',own,'main',0),('wrong_cache_row','FLOOR_QUEUE',own,'row',0),('wrong_art_source','FLOOR_QUEUE',own,'source',0),('shifted_draw','FLOOR_QUEUE',own,'xy',q['xy']^1)]
            index=next(i for i,r in enumerate(g['FLOOR_QUEUE_TRANSFORM'])if(r['frame'],r['cursor'])==key)
            trials.extend((('shifted_camera','FLOOR_QUEUE_TRANSFORM',index,'camera',g['FLOOR_QUEUE_TRANSFORM'][index]['camera']^1),('floating_floor','FLOOR_QUEUE_TRANSFORM',index,'floor',q['floor']+1)))
            index=next(i for i,r in enumerate(g['FLOOR_QUEUE_PART'])if(r['frame'],r['cursor'])==key)
            trials.append(('wrong_art_width','FLOOR_QUEUE_PART',index,'width',g['FLOOR_QUEUE_PART'][index]['width']+1))
            index=next(i for i,r in enumerate(g['FLOOR_QUEUE_DISPATCH'])if r['slot']==side)
            trials.append(('wrong_physical_consumer','FLOOR_QUEUE_DISPATCH',index,'slot',3-side))
            for label,tag,index,key,new in trials:
                damaged=copy.deepcopy(g);damaged[tag][index][key]=new
                try:contract(damaged,guest,payload,identity,side)
                except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
                else:raise ValueError('Actual FIFO/projection/floor fault accepted '+label)
                need(contract(g,guest,payload,identity,side)==positive,'Exact positive restored after actual FIFO fault')
            prop_index=next(i for i,q in enumerate(g['FLOOR_ALL_QUEUE'])if q['actor']in prop_positive['actualProps']and q['cache']in prop_positive['sourceBoundDescriptorConsumers'])
            for key,new in(('id',17),('cache',0),('source',0),('body',2),('bank',0)):
                damaged=copy.deepcopy(g);damaged['FLOOR_ALL_QUEUE'][prop_index][key]=new
                try:prop_contract(damaged,text,guest,identity,side)
                except (ValueError,KeyError)as error:faults.append(dict(kind='actual_prop_'+key,rejectedBy=str(error)))
                else:raise ValueError('Actual original detached-prop fault accepted '+key)
                need(prop_contract(g,text,guest,identity,side)==prop_positive,'Original detached-prop positive restored')
            for p,h in meta['input_hashes'].items():need(sha(p)==h,'Executed input unchanged');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
            cases.append(dict(fighter=fighter,side=side,nativeFIFO=positive,nativeDetachedProps=prop_positive,actualRowCounterexamplesRejected=faults))
    for p in(Path(__file__).resolve(),Path(old.__file__),Path(grammar.__file__),capture.OUT/'report.json',grammar.OUT/'report.json'):pins[str(p)]=sha(p)
    return dict(passed=True,actualContexts=4,actualRowFaultsRejected=sum(len(c['actualRowCounterexamplesRejected'])for c in cases),cases=cases,inputHashes=pins,allArenaFloorShadowsAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
