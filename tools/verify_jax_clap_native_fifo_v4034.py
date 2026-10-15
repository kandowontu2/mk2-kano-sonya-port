"""Native Jax head-clap full FIFO/components/projection/floor/shadow proof.

Retain the complete3994 generic FIFO/cache/component/DMA/projection proof and
811 compressed native shadow-row algorithm. Replace only split-specific
actor/hat/cadence construction with actual original Jax state and seven
original own headless groups. Dead Pool normal costume only.
"""
import copy,inspect,json,re,struct,subprocess,traceback
from collections import defaultdict
from pathlib import Path
import run_jax_clap_native_scene_v4028 as capture
import verify_jax_clap_earned_v4032 as grammar
import verify_kung_lao_split_native_fifo_v3994 as old
ROOT,need,sha,model=capture.ROOT,capture.need,capture.sha,capture.model
OUT=ROOT/'audit_v4035_jax_clap_native_fifo_checked'

def make_contract():
    source=inspect.getsource(old.contract)
    before='    ids={side:identity,3-side:0};anchors={0:140,17:134,18:135}'
    need(source.count(before)==1,'One original physical identity/anchor declaration')
    source=source.replace(before,'    ids={side:identity,3-side:11};anchors={11:139,17:134,18:135}')
    first=source.index("    secondary={q['actor']")
    last=source.index("    for r in g['FLOOR_STATE']:",first)
    source=source[:first]+"""    phase_targets=set(capture.death_art.GROUPS['kano'if identity==17 else'sonya'])
    grammar.source_contract(guest)
    need(not any(q['slot']==3 for q in g['FLOOR_QUEUE']),'Jax head-clap has no mirrored secondary split actor')
    need(begin['id']==11 and begin['entry']==0xff8c7820 and begin['actor']==actors[3-side]and begin['main']==mains[3-side]and
         retired['p1']==retired['p2']==0 and retired['victim_health']==0 and retired['mode']in(3,5),'True original Jax and actual both-pointer teardown')
    need(result['origin']==origin and result['retired']==end and result['snapshots']==end-origin+30 and
         [r['frame']for r in g['FLOOR_STATE']]==list(range(origin,end+31)),'Every physical state through native disappearance plus30')
"""+source[last:]
    changes={
      "active=q['actor']in(actors[1],actors[2])or(q['actor']==actors[3]and q['frame']>=creation)":"active=q['actor']in(actors[1],actors[2])",
      "s=q['slot'];owner=actors[side]if s==3 else actors.get(s)":"s=q['slot'];owner=actors.get(s)",
      "allowed_owner=hat if s==3-side and hat_owner_first<=q['frame']<hat_owner_first+12 else owner":"allowed_owner=owner",
      "s in(1,2,3)":"s in(1,2)",
      "q['kind']==(1 if s==3 else 0)":"q['kind']==0",
      "s in(side,3)and 0xfffdf100<=q['pose']<0xfffdf600":"s==side and q['pose']in phase_targets",
      "q['slot']in(side,3)and 0xfffdf100<=q['pose']<0xfffdf600":"q['slot']==side and q['pose']in phase_targets",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Unique actual Jax physical actor/group adaptation '+before);source=source.replace(before,after)
    first=source.index('    phase_start=')
    last=source.index('    own_shadows=shadow_contract(g)',first)
    source=source[:first]+"""    need(set(phases)=={(side,p)for p in phase_targets}and all(phases[side,p]for p in phase_targets),'All seven original native own headless groups genuinely publish; not assumed from descriptor addresses')
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

def expected():
    base,_,prior,_,_=capture.data.old.expected_current();payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=capture.data.check(prior,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    return guest,payload

def run():
    need(not OUT.exists(),'Fresh immutable FIFO qualification')
    scene=json.loads((capture.OUT/'report.json').read_text());state=json.loads((grammar.OUT/'report.json').read_text())
    need(scene['passed']and state['passed']and len(scene['cases'])==4 and state['actualContexts']==4,'Four complete actual native scene and whole earned-state contexts')
    guest,payload=expected();contract=make_contract();cases=[];pins={}
    for fighter in('kano','sonya'):
        for side in(1,2):
            folder=ROOT/f'audit_v4029_jax_clap_{fighter}_p{side}_native_scene_ram';meta=json.loads((folder/'result.json').read_text());text=(folder/'run.log').read_text()
            need(meta['exit_code']==0 and not meta['modelErrors']and meta['observedRGBFields']==meta['modelExactFields']and meta['ramGuestSHA256']==model.digest(guest),'Actual whole-scene terminal/guest/pixel replay')
            g=parsed(text);identity=17 if fighter=='kano'else 18;positive=contract(g,guest,payload,identity,side);faults=[]
            own=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==side and r['pose']in capture.death_art.GROUPS[fighter]);q=g['FLOOR_QUEUE'][own];key=q['frame'],q['cursor']
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
            for p,h in meta['input_hashes'].items():need(sha(p)==h,'Executed input unchanged');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
            cases.append(dict(fighter=fighter,side=side,nativeFIFO=positive,actualRowCounterexamplesRejected=faults))
    for p in(Path(__file__).resolve(),Path(old.__file__),Path(grammar.__file__),capture.OUT/'report.json',grammar.OUT/'report.json'):pins[str(p)]=sha(p)
    return dict(passed=True,actualContexts=4,actualRowFaultsRejected=sum(len(c['actualRowCounterexamplesRejected'])for c in cases),cases=cases,inputHashes=pins,allArenaFloorShadowsAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
