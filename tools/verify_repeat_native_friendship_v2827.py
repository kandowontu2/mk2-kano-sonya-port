"""Three earned continuous native Kano Friendships per slot, not full-port proof.
Replay every palette word from boot, bind each actual allocation and native
release, and follow each task/sprite into the free pool and subsequent reuse.
No full-scene render/audio or global all-effect/all-arena claim is made here.
"""
import argparse, hashlib, json, re, traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import inspect_current_friendship_palette_lifecycle_v2732 as old

ROOT=assembly.ROOT
need=assembly.need
num=lambda r,k:int(r[k])
ptr=lambda r,k:int(r[k],16)
frame=lambda r:num(r,'frame')
FIRST,STRIDE,COUNT=0x0102d6f0,0x210,358
END=FIRST+STRIDE*COUNT

def parse(path):
    rows=[]
    with path.open(encoding='utf-8-sig') as stream:
        for line in stream:
            match=re.match(r'MK2_REPEAT_(\w+) (.*)',line)
            if match:rows.append((match[1],dict(re.findall(r'(\w+)=([^\s]+)',match[2]))))
    return rows

def select(rows,tag,context=None):
    return [r for kind,r in rows if kind==tag and (context is None or int(r.get('context',r['cycle']))==context)]

def one(rows,tag,context=None):
    found=select(rows,tag,context)
    need(len(found)==1,'Exactly one actual '+tag+' per context')
    return found[0]

def nodes(r,key):return [] if r[key]=='-' else [int(x,16) for x in r[key].split(',')]

def list_check(r):
    groups={key:nodes(r,key) for key in ('tasks','freeTasks','objects','freeObjects')}
    for key,values in groups.items():
        need(len(values)==num(r,key+'Count')==len(set(values)) and len(values)<1024,
             'Complete acyclic native linked-list snapshot')
        if key=='freeObjects':
            need(values and all(FIRST<=x<END and (x-FIRST)%STRIDE==0 for x in values),
                 'Only original fixed-stride sprite-pool nodes')
            need(values[-1]==END-STRIDE and
                 ((ptr(r,key+'Stop')==END and num(r,key+'Valid')==1) or
                  (ptr(r,key+'Stop')==0x00fe0190 and num(r,key+'Valid')==0)),
                 'Exact original boot/reset free-pool terminator, never an extra sprite')
        else:
            need(num(r,key+'Valid')==1 and ptr(r,key+'Stop')==0 and
                 all(0x01000000<=x<0x01100000 for x in values),'Complete original active/free list')
    need(not set(groups['tasks'])&set(groups['freeTasks']) and
         not set(groups['objects'])&set(groups['freeObjects']),'Actual active/free lists disjoint')
    return groups

def replay(rows,side,wanted):
    need(rows and all(num(r,'side')==side and r['writes']=='0' and r['assistance']=='none'
                     for _,r in rows),'Every observation true unassisted physical slot')
    baseline=one(rows,'BASELINE');done=one(rows,'DONE');final=one(rows,'RESULT')
    need(frame(baseline)==0 and num(done,'matches')==num(final,'requested')==
         num(final,'completed')==num(final,'contexts')==wanted and frame(done)==frame(final),
         'Actual uninterrupted terminal completed matches')
    states=select(rows,'STATE')
    need([frame(r) for r in states]==list(range(1,frame(final)+1)),
         'Every consecutive native field from cold boot to terminal')
    need(not select(rows,'FAILED') and len(select(rows,'RESELECT'))==wanted-1,
         'Natural reselection between each match, no diagnostic timeout')
    values=old.words(baseline);stores=[];snapshots=0;increments=releases=0
    for tag,r in rows:
        if tag=='TABLE_STORE':
            at=ptr(r,'at');offset=at-old.PAL_FIRST
            need(0<=offset<old.PAL_COUNT*old.PAL_STRIDE and offset%16==0,
                 'Native palette store within original fixed table')
            slot=offset//16;before=ptr(r,'before');data=ptr(r,'data');mask=ptr(r,'mask');pc=ptr(r,'pc')
            need(before==values[slot] and 0<=data<=65535 and mask==65535,
                 'Uninterrupted palette store matches previous native word')
            if pc==0xff80d550:
                need(offset%64==32 and before<65535 and data==before+1 and ptr(r,'a1')==at-32,
                     'Exact native reference increment');increments+=1
            elif pc==0xff80d710:
                need(offset%64==32 and before>0 and data==before-1 and ptr(r,'a0')==data and ptr(r,'a1')==at-32,
                     'Exact positive native reference decrement');releases+=1
            elif pc==0xff80cd90:
                need(data==0 and ptr(r,'a1')==0,'Exact original native palette reset')
            values[slot]=data;stores.append(r)
        elif 'table' in r:
            need(old.words(r)==values,'Every complete palette snapshot matches continuous replay');snapshots+=1
    need(len(stores)==num(final,'paletteStores'),'All actual native palette stores retained')
    results=[]
    for cycle in range(1,wanted+1):
        action=one(rows,'ACTION',cycle);window=one(rows,'WINDOW',cycle);command=one(rows,'COMMAND',cycle)
        construct=one(rows,'CONSTRUCT',cycle);pre=one(rows,'ALLOC_PRE',cycle);taskrow=one(rows,'ALLOC_TASK',cycle)
        reset=one(rows,'BUBBLE_POOL_RESET',cycle);returned=one(rows,'BUBBLE_TASK_RETURN',cycle)
        complete=one(rows,'MATCH_COMPLETE',cycle);cleanup=one(rows,'CLEANUP',cycle)
        parent,main=ptr(action,'actor'),ptr(action,'main')
        task,obj=ptr(construct,'task'),ptr(construct,'object')
        encoded=ptr(construct,'palette');index=encoded&255;cell=old.PAL_FIRST+index*64
        need(ptr(action,'entry')==0xfffcd000 and num(action,'id')==17 and
             num(action,'kos')==num(window,'kos')==num(complete,'kos')==2 and
             num(action,'damage')==num(window,'damage')==num(complete,'damage')==322,
             'Two actual earned round wins before true Kano Friendship')
        damage=select(rows,'DAMAGE',cycle)
        need(damage and sum(num(r,'before')-num(r,'after') for r in damage)==322 and
             sum(num(r,'after')==0 for r in damage)==2 and
             all(0<=num(r,'after')<num(r,'before')<=161 and ptr(r,'mask')==65535 and
                 ptr(r,'own')==parent and ptr(r,'target')!=parent and frame(r)<frame(window) for r in damage),
             'Native damage stores actually earn both complete rounds')
        need(window['hp_counters']==window['lp_counters']=='0,0','Actual native no-punch Friendship eligibility')
        picks=select(rows,'SELECT_ID',cycle)
        need(len(picks)==2 and {num(r,'slot') for r in picks}=={1,2} and
             all(num(r,'actual')==num(r,'target')==(17 if num(r,'slot')==side else 18) for r in picks),
             'Both actual native selections retain true IDs')
        participant=[r for r in states if num(r,'cycle')==cycle and num(r,'mode')==2 and frame(r)<=frame(action)]
        need(participant and all(num(r,'ownID')==num(r,'ownRoster')==17 and
             num(r,'victimID')==num(r,'victimRoster')==18 and num(r,'ownState')==num(r,'victimState')==1 and
             ptr(r,'ownActor')==parent and ptr(r,'ownMain')==main for r in participant),
             'Every actual live combat field remains the selected native humans')
        inputs=select(rows,'INPUT',cycle);start=frame(command)
        for age,key,length in ((15,'Down',10),(20,'Low_Kick',4),(30,'Block',4),(40,'Block',4),(50,'High_Kick',4)):
            need(all(any(frame(r)==start+age+i and num(r,'slot')==side and r['button']==key for r in inputs)
                     for i in range(length)),'Actual physical Friendship command, not action injection')
        need(num(command,'gap')>=160 and frame(window)<start<frame(action)<frame(construct)<frame(cleanup)<frame(returned)<frame(reset)<frame(complete),
             'Native physical command, construction, cleanup and retirement chronology')
        need(ptr(pre,'freeHead')==task==ptr(taskrow,'task') and ptr(pre,'a1')==num(taskrow,'taskID')==0x109 and
             ptr(pre,'a7')==ptr(taskrow,'resume')==0xff83b070 and ptr(taskrow,'owner')==parent and
             ptr(construct,'parent')==parent and ptr(construct,'parentMain')==main and
             ptr(construct,'cache')==task+0x100 and ptr(construct,'objectTask')==0 and
             0xfe9d2610<=ptr(construct,'pose')<=0xfe9d2790 and 0<=index<60 and encoded==index*0x101,
             'Original allocator supplies independent task/sprite/cache, no parent proxy')
        constructor_table=old.words(one(rows,'CONSTRUCT_TABLE',cycle))
        need((constructor_table[index*4]|constructor_table[index*4+1]<<16)==0xfffe2800 and constructor_table[index*4+2]==1,
             'Actual typed bubble palette holds one genuine reference')
        entries=[r for r in select(rows,'ALLOC_ENTRY') if frame(r)==frame(construct) and ptr(r,'a8')==obj and ptr(r,'a13')==main]
        need(len(entries)==1 and ptr(entries[0],'a0')==0xfecdf710 and
             any(frame(r)==frame(construct) and ptr(r,'a0')==encoded and ptr(r,'a8')==obj and ptr(r,'a13')==main
                 for r in select(rows,'ALLOC_RETURN')),'Actual original bubble palette allocation/return')
        for r in states:
            if frame(construct)<=frame(r)<frame(reset):
                table=old.words(r)
                need((table[index*4]|table[index*4+1]<<16)==0xfffe2800 and table[index*4+2]==1,
                     'Every live bubble field retains owned source and one reference')
        drop=[r for r in stores if ptr(r,'at')==cell+32 and frame(construct)<frame(r)<=frame(reset) and ptr(r,'pc')==0xff80d710]
        need(len(drop)==1 and frame(drop[0])==frame(reset) and ptr(drop[0],'before')==1 and ptr(drop[0],'data')==0 and ptr(drop[0],'a8')==obj,
             'Exactly one actual bubble reference release at native reset, never early/leaked')
        release=[r for r in select(rows,'RELEASE_ENTRY') if frame(r)==frame(reset) and ptr(r,'a8')==obj and ptr(r,'a0')==encoded]
        stamp=[r for r in stores if frame(r)==frame(reset) and ptr(r,'at')==cell+48 and ptr(r,'pc')==0xff80d770]
        need(len(release)==len(stamp)==1 and ptr(stamp[0],'data')==ptr(stamp[0],'a0')&65535 and ptr(stamp[0],'a1')==cell,
             'Actual original palette release and native reuse-delay clock')
        phases=select(rows,'PHASE',cycle)
        need([frame(r) for r in phases]==list(range(frame(construct),frame(final)+1)),
             'Every actual child lifecycle field, including later matches')
        object_pop=[r for r in select(rows,'FREE_OBJECT_STORE',cycle) if frame(r)>=frame(reset) and ptr(r,'pc')==0xff809150 and
                    ptr(r,'at')==0x01060130 and ptr(r,'before')==ptr(r,'a0')==obj and ptr(r,'merged')==ptr(r,'a2')!=obj]
        need(object_pop,'Actual native sprite reuse after bulk pool reclaim')
        reuse=min(frame(r) for r in object_pop)
        for r in phases:
            need(ptr(r,'task')==task and ptr(r,'object')==obj and
                 all(num(r,k)==1 for k in ('tasksValid','freeTasksValid','objectsValid')) and
                 num(r,'freeObjectsValid')==(0 if frame(r)<frame(one(rows,'BUBBLE_POOL_RESET',1)) else 1),
                 'Continuous actual native child identity/list observations')
            if frame(r)<frame(returned):
                need(num(r,'taskActive')==1 and num(r,'taskFree')==0 and num(r,'taskID')==0x109 and ptr(r,'taskOwner')==parent,
                     'Actual child task remains owned and active until native return')
            if frame(returned)<=frame(r)<=frame(complete):
                need(num(r,'taskActive')==0 and num(r,'taskFree')==1,'Actual child task reclaimed into native free list')
            if frame(r)<frame(reset):
                need(num(r,'objectFree')==0 and ptr(r,'objectCache')==task+0x100 and 0xfe9d2610<=ptr(r,'objectPose')<=0xfe9d2790,
                     'Actual independent child sprite/cache retained until native reset')
            elif frame(r)<reuse:
                need(num(r,'objectFree')==1,'Actual bulk-reset sprite belongs to original free pool')
            elif frame(r)==reuse:
                need(num(r,'objectFree')==0 and not(ptr(r,'objectCache')==task+0x100 and 0xfe9d2610<=ptr(r,'objectPose')<=0xfe9d2790),
                     'Actual native reuse replaces retired bubble cache/pose')
        boundaries=select(rows,'BOUNDARY_LISTS',cycle)
        need({frame(r) for r in boundaries}=={frame(construct),frame(returned),frame(reset)},
             'Stable native constructor/return/reset full-list boundaries')
        for r in boundaries:list_check(r)
        groups=list_check(one(rows,'COMPLETE_LISTS',cycle))
        need(task in groups['freeTasks'] and task not in groups['tasks'],'Actual completed scene retains no active bubble task')
        results.append(dict(cycle=cycle,action=frame(action),construction=frame(construct),task=task,object=obj,
                            paletteIndex=index,taskReturn=frame(returned),nativePaletteRelease=frame(reset),spriteReuse=reuse,
                            earnedDamage=322,earnedRoundWins=2,continuousLifecycleFields=len(phases),liveCombatFields=len(participant)))
    return dict(matches=results,consecutiveNativeFields=len(states),completePaletteSnapshots=snapshots,
                nativePaletteStores=len(stores),referenceIncrements=increments,referenceReleases=releases,
                totalEarnedDamage=322*wanted,totalEarnedRoundWins=2*wanted,
                repeatedNativePaletteLifecycleAccepted=True,fullPortAcceptance=False)

def verify(folder):
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/assembly.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(meta['exit_code']==0 and meta['candidate']==assembly.NAME and meta['side'] in (1,2) and meta['requested_matches']==3 and
         meta['assistance']=='none' and meta['guest_writes']==meta['emulator_resets']==0 and not meta['saved_states_used'] and
         not meta['cheats_enabled'] and meta['input_hashes']==before,'Terminal genuine continuous candidate capture')
    pins=assembly.source_check()
    def pin(path,wanted=None):
        path=str(Path(path).resolve());actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Immutable executed input '+path)
        need(path not in pins or pins[path]==actual,'Consistent source pin '+path);pins[path]=actual
    for file,wanted in before.items():
        pin(file,wanted)
        if Path(file).suffix in ('.ps1','.lua','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
    need(meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256'] and
         all(before.get(file)==wanted for file,wanted in build['input_hashes'].items()),'Every executed compiled input exactly pinned')
    guest,prior,payload,_,_=assembly.expected()
    need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,
         'Whole actual guest and donor payload independently reconstructed')
    driver=ROOT/'mk2ks_repeat_native_friendship_v2824.lua';source=driver.read_text()
    original=ROOT/'mk2ks_repeat_native_friendship_v2819.lua';original_source=original.read_text();pin(original)
    physical=lambda text:text[text.index('emu.register_frame(function()'):text.index('emu.register_frame_done(function()')]
    need(physical(source)==physical(original_source) and not re.search(r':write_|load_?state|\.value\s*=(?!=)|:reset\(',source),
         'Physical driver unchanged; no guest writes/register injection/saved states/emulator resets')
    stock_path=ROOT/'mk2/mk2-maincpu.bin';pin(stock_path,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
    stock=stock_path.read_bytes()
    for lo,hi in ((0xff8087b0,0xff808a20),(0xff83f0a0,0xff83f200),(0xff83ae20,0xff83b3f0),
                  (0xff80e0e0,0xff80e620),(0xff8090b0,0xff809270),(0xff80d580,0xff80d7a0)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Original native allocation/release/reset body unchanged')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    need(not re.search(r'LUA ERROR|fatal error|access violation|stack traceback|WRONG CHECKSUMS',log,re.I),'No runtime errors')
    rows=parse(folder/'run.log');result=replay(rows,meta['side'],meta['requested_matches'])
    initial=ROOT/f'audit_v2823_repeat_native_friendship_p{meta["side"]}/run.log';pin(initial)
    unobserved={'PHASE','BOUNDARY_LISTS'}
    need([(t,r) for t,r in rows if t not in unobserved]==parse(initial),'All original physical/palette/native chronology unchanged by stable field observer')
    for file in folder.rglob('*'):
        if file.is_file():pin(file)
    for file in (Path(__file__),Path(assembly.__file__),Path(assembly.prior.__file__),Path(old.__file__)):
        pin(file)
    return dict(passed=True,candidate=assembly.NAME,side=meta['side'],**result,inputHashes=pins,
                wholeActualGuestAndPayloadReconstructed=True,noEmulatorResetOrStateInjection=True,
                originalBootAndResetPoolTerminatorsPreserved=True,fullFinisherAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();need(not args.output.exists(),'Immutable new verification report')
    try:report=verify(args.folder)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
