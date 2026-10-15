"""Whole current naturally chosen blocked ring, real input and native lifetime.

Reuse the entire original ring model (body, flight, impact, guard, damage,
locks, recovery and retirement). Independently retain ungated constructor,
pool membership and native free-list words. Preserve incomplete leg entries;
this is not their acceptance or a full audiovisual/campaign/release pass.
"""
import hashlib,inspect,json,re,struct,sys,traceback
from types import SimpleNamespace
from pathlib import Path
import capture_native_selector_cpu_sonya_continuous_guard_layout as capture
import native_repeated_cpu_ring_contract_v2970 as ring
import qualify_native_selector_cpu_sonya_round_order as previous

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_sonya_continuous_ring_checked'
rows=previous.rows


def physical_inputs(text):
    records=rows(text,'MK2_CPU_PAIR_CONTINUOUS_GUARD_INPUT')
    return [{k:v if k in('policy','buttons','assistance')else int(v,16 if k in('actor','main')else 10)
             for k,v in r.items()}for r in records]


def whole_inventory(text,guest):
    source=inspect.getsource(capture.original.whole_sonya)
    before="inputs=model.pair.rows(text,'CONTINUOUS_GUARD_INPUT')"
    need(source.count(before)==1,'Only new policy token parser repaired; whole prior state/HP/RNG/tower rules unchanged')
    source=source.replace(before,'inputs=physical_inputs(text)',1)
    scope=dict(capture.original.whole_sonya.__globals__,physical_inputs=physical_inputs)
    exec(compile(source,__file__+'::whole_inventory_new_policy_token_parser','exec'),scope)
    return scope['whole_sonya'](text,guest)


def all_rings(text,guest):
    events=ring.stream.overlap.rows(text,'EVENT')
    entries=[r for r in events if r['kind']=='ring']
    born=ring.stream.overlap.rows(text,'CHILD');dead=ring.stream.overlap.rows(text,'RETIRE')
    need(len(entries)==len(born)==len(dead)==2 and
         [r['serial']for r in entries]==[r['serial']for r in born]==[1,2]and
         [r['child_serial']for r in dead]==[1,2],
         'Complete actual two-ring inventory, no omitted unexplained native child')
    accepted=[]
    assignments={tag:set()for tag in('CHILD','CHILD_FIELD','RETIRE')}
    for entry in entries:
        serial=entry['serial']
        birth=ring.one([r for r in born if r['serial']==serial],'One source-owned birth per actual serial')
        retired=ring.one([r for r in dead if r['child_serial']==serial],'One actual retirement per serial')
        start,end=entry['frame'],retired['frame']
        def overlap_rows(log,tag):
            records=ring.stream.overlap.rows(log,tag)
            if tag in('EVENT','CHILD','HEALTH','CHILD_FIELD','RETIRE'):
                records=[r for r in records if r.get('child_serial',r.get('serial'))==serial]
            if tag in assignments:
                for r in records:
                    key=(r['frame'],r.get('a8',r.get('actor')))
                    need(key not in assignments[tag],'Every native child record belongs to exactly one lifetime')
                    assignments[tag].add(key)
            return records
        def guard_rows(log,tag):
            records=ring.original.rows(log,tag)
            if tag in('GUARD','TESTED','BLOCK'):
                records=[r for r in records if birth['frame']<=r['frame']<=end]
            return records
        overlap=SimpleNamespace(**{**vars(ring.stream.overlap),'rows':overlap_rows})
        stream=SimpleNamespace(**{**vars(ring.stream),'overlap':overlap})
        original=SimpleNamespace(**{**vars(ring.original),'rows':guard_rows})
        # The entire original ring function is unchanged. Only its local row
        # API selects an independently inventoried serial; global code, HP,
        # state, parent callbacks, locks and terminal history remain whole.
        source=inspect.getsource(ring.verify)
        scope=dict(ring.verify.__globals__,stream=stream,original=original)
        exec(compile(source,__file__+'::entire_original_ring_serial_'+str(serial),'exec'),scope)
        result=scope['verify'](text,guest,'sonya')
        shot=ring.one(result['acceptedRings'],'One entire original ring result per inventoried lifetime')
        need(shot['blocked']and shot['damage']==6,'Both actual rings use native blocked branch and six chip damage')
        accepted.append(shot)
    for tag,keys in assignments.items():
        actual=ring.stream.overlap.rows(text,tag)
        need(len(keys)==len(actual)and keys=={(r['frame'],r.get('a8',r.get('actor')))for r in actual},
             'Every actual original '+tag+' record covered exactly once by whole ring contracts')
    return dict(reached=True,acceptedRings=accepted,wholeOriginalRingContractsUnchanged=True,
        fullRasterOrAudioAccepted=False,allCPUAccepted=False,fullPortAcceptance=False)


def bindings(guest):
    cache={}
    def gate(text):
        need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),
             'Current native game/observer free of runtime errors')
        digest=hashlib.sha256(text.encode()).hexdigest()
        if digest not in cache:cache[digest]=whole_inventory(text,guest)
        inventory=cache[digest]
        mechanics=all_rings(text,guest)
        details=[]
        for shot in mechanics['acceptedRings']:
            details.append(lifetime(text,guest,shot))
        completes=previous.original.pair.rows(text,'COMPLETE')
        legs=[previous.original.pair.verify_pair(text,'sonya',r['cycle'],guest)for r in completes]
        need(len(legs)==2 and all(r['passed']and not r['errors']and r['damage']==35 for r in legs),
             'Both genuinely completed legs retain whole original paired phase/flight/individual cleanup contract')
        return dict(passed=True,wholeNativeInventory=inventory,wholeOriginalBlockedRing=mechanics,
            independentLifetimes=details,wholeOriginalCompletedLegs=legs,blockedRingAccepted=True,
            fullBodyShadowArtAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False)
    return gate


def lifetime(text,guest,shot):
        need(shot['blocked']and shot['damage']==6 and shot['actualPhysicalBlockDecisionVerified'],
             'Actual original blocked branch and six chip damage, not cached guard or held-button inference')
        start,birth,hit,end=(shot[k]for k in('start','birth','hit','retirement'))
        ordered=[]
        for line in text.splitlines():
            if line.startswith('MK2_STARTUP_PROJECTILE_'):
                ordered.extend(rows(line,line.split()[0]))
        need([int(r['sequence'])for r in ordered]==list(range(1,len(ordered)+1))and
             all(r['writes']=='0'and r['assistance']=='none'for r in ordered),
             'Whole ungated original observer sequence retained without missing callbacks')
        code=rows(text,'MK2_STARTUP_PROJECTILE_CODE')
        need(len(code)==2 and {(int(r['start'],16),int(r['stop'],16))for r in code}==
             {(0xfffc3800,0xfffc8000),(0xff8b6820,0xff8b69a0)},'Complete actual constructor/child/retirement code')
        for r in code:
            lo,hi=((int(r[k],16)-0xff800000)//8 for k in('start','stop'))
            words=[int(w,16)for w in r['words'].split(',')]
            need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi],'Every observed source word equals independent current guest')
        events=rows(text,'MK2_STARTUP_PROJECTILE_EVENT')
        for r in events:
            at=int(r['entry'],16)
            need(int(r['pc'],16)==at+16 and int(r['mask'],16)==65535 and
                 int(r['opcode'],16)==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0],
                 'Every actual executing ungated observer opcode/read mask source-bound')
        parent_entry=ring.one([r for r in events if r['kind']=='ring'and int(r['frame'])==start],'One independent original parent entry')
        ctor=ring.one([r for r in events if r['kind']=='ring_create'and int(r['frame'])==birth],'One independent original constructor')
        born=ring.one([r for r in events if r['kind']=='ring_child'and int(r['frame'])==birth],'One independent original child birth')
        a,m,parent,pm=(int(v,16)for v in(born['a8'],born['a13'],born['parent'],ctor['a13']))
        need(int(parent_entry['frame'])==start and int(born['frame'])==int(ctor['frame'])==birth and
             parent_entry['a8']==ctor['a8']==ctor['owner']==born['parent']==born['p2']and
             parent_entry['a13']==ctor['a13']==born['p2main']and born['a8']==born['owner']and
             born['parent_id']==born['id']=='18'and born['type']=='81'and
             int(born['parameter'],16)==0x80000 and born['states']=='1,0'and born['roster']=='18,18',
             'Independent executing parent/constructor/child ownership and process/type binding')
        fields=[r for r in rows(text,'MK2_STARTUP_PROJECTILE_FIELD')if int(r['birth'])==birth]
        native=[r for r in ring.stream.overlap.rows(text,'CHILD_FIELD')if birth<r['frame']<=end];by={r['frame']:r for r in native}
        need([int(r['frame'])for r in fields]==list(range(birth+1,end+1))and
             len(native)==len(fields)==shot['childFields'],'Entire independently observed allocated lifetime')
        for r in fields:
            n=by[int(r['frame'])]
            need(r['kind']=='ring_child'and int(r['birth'])==birth and
                 (r['active'],r['free'],r['active_valid'],r['free_valid'])==('1','0','1','1')and
                 int(r['original_parent'],16)==int(r['parent'],16)==n['shot_owner']==parent and
                 all(int(r[k],16)==n[k]for k in('actor','main','owner','pose','xraw','yraw','vx','vy','flags','body','parameter'))and
                 int(r['id'])==n['id']==18 and int(r['type'])==n['type']==81,
                 'Every complete child word and actual native active/free membership')
        health=ring.one([r for r in rows(text,'MK2_STARTUP_PROJECTILE_HEALTH')if int(r['frame'])==hit],'One independent owned projectile health store')
        need(int(health['frame'])==hit and int(health['before'])-int(health['after'])==6 and
             int(health['a10'],16)==6 and int(health['a8'],16)==a and int(health['a13'],16)==m and
             int(health['owner'],16)==a and int(health['parent'],16)==parent and
             int(health['pc'],16)==0xff836700 and int(health['mask'],16)==65535,
             'Independent source-owned actual six-damage projectile contact')
        held=ring.one([r for r in rows(text,'MK2_CPU_PAIR_CONTINUOUS_GUARD_INPUT')if int(r['frame'])==hit],
                      'Original real human input callback on contact field')
        need(held['buttons']=='Block'and held['policy']=='continuous_guard',
             'Independent input held; original ring contract additionally requires real stock blocked branch')
        heads=rows(text,'MK2_BLADE_ALLOC_HEAD_STORE')
        pop=[r for r in heads if int(r['frame'])==birth and r['pc']=='FF809150']
        push=[r for r in heads if int(r['frame'])==end and r['pc']=='FF8097D0']
        need(len(pop)==len(push)==2,'Full actual native low/high sprite free-list pop and push')
        for group,pc in((pop,0xff809150),(push,0xff8097d0)):
            need([int(r['at'],16)for r in group]==[0x01060130,0x01060140]and
                 int(group[1]['sequence'])==int(group[0]['sequence'])+1,'Consecutive full free-head word stores')
            for r in group:
                before,data,mask,merged=(int(r[k],16)for k in('before','data','mask','merged'))
                shift=int(r['at'],16)-0x01060130
                need(int(r['target'],16)==int(r['a0'],16)==a and mask==65535 and
                     merged==((before&(~(mask<<shift)))|((data&mask)<<shift))&0xffffffff and
                     struct.unpack_from('<HHH',guest,(pc-48-0xff800000)//8)==tuple(int(r['op'+str(n)],16)for n in range(3)),
                     'Native actual masked pool arithmetic, object operand and exact source opcodes')
        need(int(pop[0]['before'],16)==a and int(pop[1]['merged'],16)==int(pop[0]['targetNext'],16)==int(pop[0]['a2'],16)and
             (int(pop[0]['a8'],16),int(pop[0]['a13'],16))==(parent,pm)and
             int(push[0]['targetNext'],16)==int(push[0]['before'],16)==int(push[0]['a2'],16)and
             int(push[1]['merged'],16)==a and(int(push[0]['a8'],16),int(push[0]['a13'],16))==(a,m),
             'Independent original parent pool allocation and child-owned free-list return')
        retired=ring.one([r for r in rows(text,'MK2_STARTUP_PROJECTILE_RETIRE')if int(r['birth'])==birth],'One original independent retirement')
        need(int(retired['frame'])==end and int(retired['birth'])==birth and retired['a8']==born['a8']and
             retired['a13']==born['a13']and int(retired['original_parent'],16)==parent and
             rows(text,'MK2_STARTUP_PROJECTILE_RESULT')[0]['live_children']=='0',
             'Same child retired and no unresolved observer-owned child at native terminal')
        return dict(passed=True,start=start,birth=birth,contact=hit,retirement=end,
            independentAllocatedChildFields=len(fields),independentNativePoolPop=pop,
            independentNativePoolPush=push,ungatedObserverRecords=len(ordered),blockedRingAccepted=True,
            fullBodyShadowArtAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists()and not capture.original.original.prior.prior.current.prior.identity.census(),
         'Same original terminal continuous-guard game; no native replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(not meta['passed']and meta['error']=="ValueError(\"invalid literal for int() with base 10: 'continuous_guard'\")"and
         meta['nativeExit']==held['process'].poll()==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']and
         held['identity']['ParentProcessId']==38752 and not meta['nativeTerminal']['hostDecodeErrors']and
         all(sha(p)==h for p,h in meta['inputHashes'].items())and
         (held['identity']['ProcessId'],held['identity']['createdUnix'])==(38512,1791743126.3305721),
         'Original exact terminal kernel identity/input inventory; policy-token rejection stays false')
    expected={'cold_high':state['WINDOWS']['high'],'cold_owned':state['WINDOWS']['owned'],
        'cold_graphics':state['WINDOWS']['graphics'],'guest':state['guest'],'gfx':state['gfx']}
    need(set(meta['proofs'])==set(expected),'All five complete initialized current windows')
    for k,raw in expected.items():
        need(meta['proofs'][k]==dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
            everyActualByteComparedInRAM=True),'Whole initialized current '+k+' independently compared')
    gate=bindings(state['guest']);positive=gate(text)
    shot=positive['wholeOriginalBlockedRing']['acceptedRings'][0]
    start,birth,hit,end=(shot[k]for k in('start','birth','hit','retirement'))
    mutate=previous.original.mutate_field
    def change(tag,key,value,**where):
        return mutate(text,tag,key,value,lambda r:all(r.get(k)==str(v)for k,v in where.items()))
    trials=[
        ('tower_list',change('MK2_CPU_PAIR_ROM','list','FFFA0000',order=positive['wholeNativeInventory']['actualNativeTower'])),
        ('cold_proxy',change('MK2_P2CPU_COLD_LIVE','cpu_id','17')),
        ('native_state_opcode',change('MK2_CPU_PAIR_FLAG','op0','FFFF')),
        ('native_rng',change('MK2_CPU_CHOICE_EVENT','a0','000000FB',kind='first_call')),
        ('ring_parent',change('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000')),
        ('ring_flight_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=birth+3)),
        ('ring_flight_velocity',change('MK2_CPU_OVERLAP_CHILD_FIELD','vx','00000000',frame=birth+3)),
        ('ring_impact_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=hit+3)),
        ('ring_blocked_damage',change('MK2_CPU_OVERLAP_HEALTH','a10','00000016',frame=hit)),
        ('ring_actual_guard_main',change('MK2_RING_PAIR_TESTED','loaded_main','01000000',frame=hit)),
        ('ring_physical_block',change('MK2_RING_PAIR_BLOCK','controls','FFFFFFFF',frame=hit,decision=2)),
        ('ring_block_branch',change('MK2_RING_PAIR_BLOCK','decision','0',frame=hit,decision=1)),
        ('ring_parent_recovery',change('MK2_CPU_OVERLAP_EVENT','body','0004',kind='regain',frame=start+50)),
        ('ring_retirement',change('MK2_CPU_OVERLAP_RETIRE','frame',str(end-1))),
        ('real_input',change('MK2_CPU_PAIR_CONTINUOUS_GUARD_INPUT','buttons','Neutral',frame=hit)),
        ('independent_child_owner',change('MK2_STARTUP_PROJECTILE_EVENT','owner','01000000',kind='ring_child')),
        ('independent_child_opcode',change('MK2_STARTUP_PROJECTILE_EVENT','opcode','FFFF',kind='ring_child')),
        ('independent_child_active',change('MK2_STARTUP_PROJECTILE_FIELD','active','0',frame=birth+3)),
        ('independent_child_free',change('MK2_STARTUP_PROJECTILE_FIELD','free','1',frame=birth+3)),
        ('independent_child_parent',change('MK2_STARTUP_PROJECTILE_FIELD','parent','01000000',frame=birth+3)),
        ('independent_health',change('MK2_STARTUP_PROJECTILE_HEALTH','a10','00000016',frame=hit)),
        ('native_pool_pop',change('MK2_BLADE_ALLOC_HEAD_STORE','a0','01000000',frame=birth,pc='FF809150')),
        ('native_pool_push',change('MK2_BLADE_ALLOC_HEAD_STORE','targetNext','01000000',frame=end,pc='FF8097D0'))]
    faults=[]
    for label,bad in trials:
        need(bad!=text,'Actual effective current corruption '+label)
        try:gate(bad)
        except(AssertionError,ValueError,KeyError,IndexError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native blocked Sonya ring fault admitted '+label)
        print('Current continuous ring fault rejected: '+label,flush=True)
    need(gate(text)==positive,'Whole untouched actual native positive restored')
    pins=dict(meta['inputHashes'])
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)
    for path in(Path(__file__),*(p for p in folder.rglob('*')if p.is_file())):pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Whole immutable native and exact executed current model inventory')
    OUT.mkdir();value=dict(passed=True,candidate=meta['candidate'],goalStatus='active',
        actualNativeIdentity=held['identity'],sameOriginalTerminalNativePID=held['identity']['ProcessId'],
        actualNativeBlockedRingAndPool=positive,actualFaultsRejected=faults,
        completeCurrentColdProofs=meta['proofs'],inputHashes=pins,newNativeGames=0,newBuilds=0,
        newROMCopies=0,newRawMedia=0,newZIPs=0,blockedRingAccepted=True,
        fullBodyShadowArtAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False,
        originalPolicyTokenCaptureRemainsRejected=True,publicPlayableChanged=False)
    capture.original.original.prior.prior.current.prior.save(OUT/'report.json',value)
    print('PASS entire actual blocked Sonya ring/native pool and23 actual faults; full goal remains active',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original same-game qualification rejection')
        OUT.mkdir();capture.original.original.prior.prior.current.prior.save(OUT/'failure.json',dict(passed=False,
            error=repr(error),traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False,goalStatus='active'))
        raise
