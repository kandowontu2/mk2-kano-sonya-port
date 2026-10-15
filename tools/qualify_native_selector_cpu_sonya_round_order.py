"""Current native Sonya tower5, ring lifetime and real post-KO completed leg.

Original tower1 capture rejection remains false. Prove the actually selected
whole tower from six native ROM tables and independent current guest, then
reuse the entire original1800-field HP/state/RNG models with only that table
context. Whole ring mechanics and post-reset cycle2 leg models unchanged.
No blocked-ring, whole shadow/raster/audio, other arenas or full-port claim.
"""
import hashlib,inspect,json,re,struct,sys,traceback
from pathlib import Path
import capture_native_selector_cpu_sonya_confirm264 as capture
import native_repeated_cpu_ring_contract_v2970 as ring

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_sonya_round_order_checked'
original=capture.prior.original.sonya


def rows(text,tag):
    result=[]
    for line in text.splitlines():
        if not line.startswith(tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(pairs)==len(dict(pairs)),'Unique original native provenance fields')
        result.append(dict(pairs))
    return result


def bind(function):
    source=inspect.getsource(function)
    need(source.count('0xfffa3180')==1,'Only actual native tower-list context differs')
    source=source.replace('0xfffa3180','schedule')
    scope=dict(function.__globals__,schedule=0xfffa3780)
    exec(compile(source,__file__+'::whole_original_'+function.__name__+'_actual_source_bound_tower5','exec'),scope)
    return scope[function.__name__]


def bindings(guest):
    health=bind(original.stream.health_ledger);choices=bind(original.choice_gate)
    cache={}
    def gate(text):
        need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),
             'Actual native runtime/observer free of errors; scenario rejection retained separately')
        cold=original.pair.rows_prefix(text,'MK2_P2CPU_COLD_LIVE ')
        need(len(cold)==1 and (cold[0]['human_id'],cold[0]['cpu_id'],cold[0]['stage'],cold[0]['schedule'])==
             (18,18,0,0xfffa3780),'True original cold Sonya actors and actual native tower5 start')
        rom=original.pair.rows(text,'ROM');expected=original.pair.expected_orders()
        table=struct.unpack_from('<I',guest,(0xff8a11f0-0xff800000)//8)[0]
        need(len(rom)==6 and table==0xfffa2c00 and [r['order']for r in rom]==list(range(6)),
             'All six actual native tower tables and independent current table pointer')
        for i,r in enumerate(rom):
            ptr=struct.unpack_from('<I',guest,(table+i*32-0xff800000)//8)[0]
            ids=struct.unpack_from('<17H',guest,(ptr-0xff800000)//8)
            need(r['table']==table and r['list']==ptr==0xfffa3000+i*0x180 and
                 tuple(map(int,r['ids'].split(',')))==ids==expected[i]and
                 r['writes']==0 and r['assistance']=='none',
                 'Every actual original-derived ladder list byte matches independent native current source')
        need(expected[5][0]==18,'Actual selected tower begins with native Sonya, not a supplied CPU ID')
        digest=hashlib.sha256(text.encode()).hexdigest()
        if digest not in cache:
            hp,by=health(text,guest,'sonya')
            states=original.stream.state_ledgers(text,guest,'sonya',by)
            rng=choices(original.choice_rows(text),guest)
            cache[digest]=dict(wholeNativeHealthLedger=hp,wholeNativeStateLedger=states,nativeChoices=rng)
        inventory=cache[digest]
        complete=original.pair.rows(text,'COMPLETE')
        need(len(complete)==1 and complete[0]['cycle']==2 and complete[0]['frame']==3531,
             'One genuinely declared uninterrupted post-reset leg, not relabeled first mixed cycle')
        leg=original.pair.verify_pair(text,'sonya',2,guest)
        need(leg['passed']and not leg['errors']and (leg['start'],leg['release'],leg['complete'],
             leg['held_fields'],leg['victim_flight_fields'],leg['damage'],leg['own_handoff'],leg['victim_handoff'])==
             (3427,3483,3531,46,23,35,3493,3530),
             'Whole unchanged original leg poses/offsets/gravity/HP/individual cleanup after actual KO/reset')
        rings=ring.verify(text,guest,'sonya')
        need(len(rings['acceptedRings'])==1 and not rings['acceptedRings'][0]['blocked']and
             rings['acceptedRings'][0]['damage']==22,'Original first ring remains genuinely unblocked, not chip success')
        entries=rows(text,'MK2_STARTUP_PROJECTILE_EVENT')
        born=ring.one([r for r in entries if r['kind']=='ring_child'],'One independent ungated ring child birth')
        ctor=ring.one([r for r in entries if r['kind']=='ring_create'],'One independent original ring constructor')
        a,m,parent,pm=(int(v,16)for v in(born['a8'],born['a13'],born['parent'],ctor['a13']))
        need(int(born['frame'])==int(ctor['frame'])==2297 and
             born['owner']==born['a8']and born['parent_id']==born['id']=='18'and
             born['type']=='81'and int(born['parameter'],16)==0x80000 and
             ctor['a8']==ctor['owner']==born['parent']==born['p2']and
             ctor['a13']==born['p2main']and (parent,pm)==(0x010350a0,0x0106c620),
             'Independent original ring creator/parent/child owner, not actor-ID alias inference')
        for r in entries:
            at=int(r['entry'],16)
            need(int(r['pc'],16)==at+16 and int(r['mask'],16)==65535 and
                 int(r['opcode'],16)==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0],
                 'Every actual ungated executing observer opcode/read mask independently source-bound')
        fields=rows(text,'MK2_STARTUP_PROJECTILE_FIELD')
        old=ring.stream.overlap.rows(text,'CHILD_FIELD');by={r['frame']:r for r in old}
        need([int(r['frame'])for r in fields]==list(range(2298,2339))and len(old)==len(fields)==41,
             'Entire original allocated ring lifetime, not selected samples')
        for r in fields:
            n=by[int(r['frame'])]
            need((r['active'],r['free'],r['active_valid'],r['free_valid'])==('1','0','1','1')and
                 int(r['birth'])==2297 and int(r['original_parent'],16)==int(r['parent'],16)==parent and
                 all(int(r[k],16)==n[k]for k in('actor','main','owner','pose','xraw','yraw','vx','vy','flags','body','parameter'))and
                 int(r['id'])==n['id']==18 and int(r['type'])==n['type']==81,
                 'Independent complete child words and original active/free pool membership')
        heads=rows(text,'MK2_BLADE_ALLOC_HEAD_STORE')
        pop=[r for r in heads if r['frame']=='2297'and r['pc']=='FF809150']
        push=[r for r in heads if r['frame']=='2338'and r['pc']=='FF8097D0']
        need(len(pop)==len(push)==2,'Full independent native low/high sprite pool pop and push')
        for records,pc in((pop,0xff809150),(push,0xff8097d0)):
            need([int(r['at'],16)for r in records]==[0x01060130,0x01060140]and
                 int(records[1]['sequence'])==int(records[0]['sequence'])+1,
                 'Original complete consecutive native pool word stores')
            for r in records:
                before,data,mask,merged=(int(r[k],16)for k in('before','data','mask','merged'))
                shift=int(r['at'],16)-0x01060130
                need(int(r['target'],16)==int(r['a0'],16)==a and mask==65535 and
                     merged==((before&(~(mask<<shift)))|((data&mask)<<shift))&0xffffffff and
                     struct.unpack_from('<HHH',guest,(pc-48-0xff800000)//8)==
                        tuple(int(r['op'+str(n)],16)for n in range(3)),
                     'Every actual original ring pool store operand, masked arithmetic and native instruction')
        need(int(pop[0]['before'],16)==a and int(pop[1]['merged'],16)==int(pop[0]['targetNext'],16)==int(pop[0]['a2'],16)and
             (int(pop[0]['a8'],16),int(pop[0]['a13'],16))==(parent,pm)and
             int(push[0]['targetNext'],16)==int(push[0]['before'],16)==int(push[0]['a2'],16)and
             int(push[1]['merged'],16)==a and (int(push[0]['a8'],16),int(push[0]['a13'],16))==(a,m),
             'Source-owned native ring allocation and child free-list return')
        retired=ring.one(rows(text,'MK2_STARTUP_PROJECTILE_RETIRE'),'One independent original ring retirement')
        need(retired['frame']=='2338'and retired['birth']=='2297'and retired['a8']==born['a8']and
             retired['a13']==born['a13']and int(retired['original_parent'],16)==parent,
             'Exact independently observed original ring retirement and process identity')
        return dict(passed=True,actualNativeTower=5,wholeOriginalNativeInventory=inventory,
            unchangedOriginalRing=rings,unchangedOriginalPostResetLeg=leg,
            independentNativeRingPoolPop=pop,independentNativeRingPoolPush=push,
            independentlyBoundRingChildFields=41,blockedRingAccepted=False,
            fullArtShadowAudioAcceptance=False,fullPortAcceptance=False)
    return gate


def execute(state):
    need(not OUT.exists()and not capture.prior.original.prior.prior.current.prior.identity.census(),
         'Same original completed native game, no new game or timeout replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(not meta['passed']and meta['error']==
         "ValueError('Actual original-derived Sonya stage-zero tower and unchanged true roster')"and
         meta['nativeExit']==held['process'].poll()==0 and not meta['nativeTerminal']['hostDecodeErrors']and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (14472,38752,1791742067.0949306)and all(sha(p)==h for p,h in meta['inputHashes'].items()),
         'Original exact tower1 rejection remains false; same terminal native14472 identity/source preserved')
    expected={'cold_high':state['WINDOWS']['high'],'cold_owned':state['WINDOWS']['owned'],
        'cold_graphics':state['WINDOWS']['graphics'],'guest':state['guest'],'gfx':state['gfx']}
    need(set(meta['proofs'])==set(expected),'All five entire actual current/limited cold proofs')
    for k,raw in expected.items():
        need(meta['proofs'][k]==dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
            everyActualByteComparedInRAM=True),'Entire current actual cold '+k+' independently compared')
    gate=bindings(state['guest']);positive=gate(text)
    mutate=original.mutate_field
    def change(tag,key,value,**where):
        return mutate(text,tag,key,value,lambda r:all(r.get(k)==str(v)for k,v in where.items()))
    trials=[
        ('tower_list',change('MK2_CPU_PAIR_ROM','list','FFFA3180',order=5)),
        ('cold_proxy',change('MK2_P2CPU_COLD_LIVE','cpu_id','17')),
        ('wrong_tower_field',change('MK2_CPU_ROUND_FIELD','schedule','FFFA3180',frame=2208,slot=2)),
        ('earned_ko',change('MK2_CPU_ROUND_HEALTH','after','1',frame=2950,slot=1)),
        ('native_refill',change('MK2_CPU_ROUND_HEALTH','after','160',frame=3138,slot=1)),
        ('native_state_store',change('MK2_CPU_PAIR_FLAG','op0','FFFF')),
        ('native_rng_threshold',change('MK2_CPU_CHOICE_EVENT','a0','000000FB',kind='first_call')),
        ('post_reset_leg_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=3440)),
        ('post_reset_leg_victim_pose',change('MK2_CPU_PAIR_FIELD','vpose','00000000',frame=3440)),
        ('post_reset_leg_damage',change('MK2_CPU_PAIR_EVENT','a10','00000022',cycle=2,kind='damage')),
        ('post_reset_leg_handoff',change('MK2_CPU_PAIR_OWN_REGAIN','body','00000004',cycle=2)),
        ('post_reset_leg_flight',change('MK2_CPU_PAIR_FIELD','vvy','00000000',frame=3490)),
        ('ring_parent',change('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000')),
        ('ring_flight_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=2300)),
        ('ring_impact_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=2320)),
        ('ring_unblocked_damage',change('MK2_CPU_OVERLAP_HEALTH','a10','00000006',frame=2310)),
        ('not_a_blocked_ring',change('MK2_RING_PAIR_BLOCK','decision','1',frame=2310,decision=0)),
        ('ring_actual_guard_main',change('MK2_RING_PAIR_TESTED','loaded_main','01000000',frame=2310)),
        ('ring_retirement',change('MK2_CPU_OVERLAP_RETIRE','frame','2337')),
        ('independent_child_owner',change('MK2_STARTUP_PROJECTILE_EVENT','owner','01000000',kind='ring_child')),
        ('independent_child_active',change('MK2_STARTUP_PROJECTILE_FIELD','active','0',frame=2300)),
        ('independent_child_freed',change('MK2_STARTUP_PROJECTILE_FIELD','free','1',frame=2300)),
        ('independent_child_parent',change('MK2_STARTUP_PROJECTILE_FIELD','parent','01000000',frame=2300)),
        ('native_pool_pop',change('MK2_BLADE_ALLOC_HEAD_STORE','a0','01000000',frame=2297,pc='FF809150')),
        ('native_pool_push',change('MK2_BLADE_ALLOC_HEAD_STORE','targetNext','01000000',frame=2338,pc='FF8097D0'))]
    faults=[]
    for label,bad in trials:
        need(bad!=text,'Actual effective corruption '+label)
        try:gate(bad)
        except(AssertionError,ValueError,KeyError,IndexError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual original native Sonya fault admitted '+label)
        print('Current Sonya round/ring/leg/pool fault rejected: '+label,flush=True)
    need(gate(text)==positive,'Entire original untouched positive restored')
    pins=dict(meta['inputHashes'])
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)
    for path in(Path(__file__),*(p for p in folder.rglob('*')if p.is_file())):pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Whole immutable current original native/source/model inventory')
    OUT.mkdir();value=dict(passed=True,candidate=meta['candidate'],goalStatus='active',
        actualNativeIdentity=held['identity'],sameOriginalTerminalNativePID=14472,
        actualSonyaNativeRingLegRoundAndPool=positive,actualFaultsRejected=faults,
        originalTower1CaptureRemainsRejected=True,completeCurrentColdProofs=meta['proofs'],
        inputHashes=pins,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        blockedRingAccepted=False,fullArtShadowAudioAcceptance=False,allCPUContextsAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False)
    capture.prior.original.prior.prior.current.prior.save(OUT/'report.json',value)
    print('PASS original Sonya tower5/state/HP/ring/pool/post-reset leg,25 faults; blocked ring pending',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original same-game qualification rejection')
        OUT.mkdir();capture.prior.original.prior.prior.current.prior.save(OUT/'failure.json',dict(passed=False,
            error=repr(error),traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False,goalStatus='active'))
        raise
