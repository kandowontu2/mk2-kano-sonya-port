"""Current first-round native knife before the first live callback.

Whole original knife intro/flight/guard/impact/body/recovery/retirement rules.
Only one unblocked shot in cycle0 and its independently observed entry BEFORE
the first all-mode match callback differ. No synthetic pre-callback actor row.
Actual executing ungated parent/constructor/child and pool lifetime required.
"""
import hashlib,inspect,json,re,struct,sys,traceback
from pathlib import Path
import capture_native_selector_cpu_first_round_projectile as capture
import qualify_native_selector_cpu_startup_guard_knife as prior

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_first_round_knife_checked'
model=capture.prior.prior.allocation.phase.model
rows=prior.rows


def first_entry(log,entry,victim,by):
    observed=model.knife.one([r for r in rows(log,'MK2_STARTUP_PROJECTILE_EVENT')if r['kind']=='knife'],
                            'One independent ungated first-round parent entry')
    first=model.knife.one(model.original.stream.rounds.rows(log,'BEGIN'),'One original native match BEGIN')
    # There is genuinely no pre-callback match row at start: the original
    # all-mode observer begins on the NEXT video callback. Do not manufacture
    # a row from next-frame values or treat mode2 instruction execution as a
    # mode2 pre-callback. Bind actual instruction context and real first rows.
    start=entry['frame']
    need(first['frame']==start+1 and not [r for r in model.original.stream.rounds.rows(log,'FIELD')if r['frame']<=start],
         'Actual before-first-callback admission; no omitted or fabricated original match fields')
    need(observed['frame']==str(start)and observed['mode']=='2'and observed['states']=='1,0'and
         observed['roster']=='17,17'and observed['id']=='17'and observed['type']=='81'and
         observed['parent']=='00000000'and observed['a8']==observed['owner']==observed['p2']and
         observed['a13']==observed['p2main']and int(observed['p1'],16)==victim['actor']and
         int(observed['p1main'],16)==victim['main']and
         (int(observed['a8'],16),int(observed['a13'],16))==(entry['a8'],entry['a13'])and
         (by[start+1,2]['actor'],by[start+1,2]['main'])==(entry['a8'],entry['a13']),
         'Actual executing first-round parent/Main/type/roster/role and first independent physical callbacks')
    need(victim['id']==17 and victim['owner']==victim['actor']and
         by[start+1,2]['id']==17 and by[start+1,2]['owner']==entry['a8'],
         'Both independently observed native owners on the first callback, not invented entry-field victim data')
    raster=model.knife.one(rows(log,'MK2_FIRST_PROJECTILE_ENTRY'),'One independent original entry raster marker')
    need(raster['frame']==observed['frame']and raster['serial']=='1'and raster['kind']=='knife'and
         raster['actor']==raster['owner']==observed['a8']and raster['main']==observed['a13']and
         raster['id']=='17'and raster['mode']=='2'and raster['opcode']=='574A'and raster['mask']=='FFFF',
         'Independent actual executing raster entry/source word agrees with ungated parent')


def whole_knife():
    source=inspect.getsource(model.knife.knives)
    old="""        native=one([r for r in R.rows(log,'FIELD')if r['frame']==start and r['slot']==1],'Original entry-field physical identity')
        assert(native['actor'],native['main'],native['owner'],native['id'])==(victim['actor'],victim['main'],victim['actor'],17)
        assert native['mode']==(2 if serial==1 else 7)and by[start+1,2]['actor']==actor and by[start+1,2]['main']==main
"""
    changes={
        'assert len(actions)==len(births)==2':'assert len(actions)==len(births)==1',
        old:'        first_entry(log,entry,victim,by)\n',
        "child['cycle']==1":"child['cycle']==entry['cycle']==0",
        '(hit+24,m,0xff8b6830,actor,serial,1)':"(hit+24,m,0xff8b6830,actor,serial,entry['cycle'])",
        '(m,a,actor,17,81,0x80000,serial,1,0,2)':"(m,a,actor,17,81,0x80000,serial,entry['cycle'],0,2)"}
    for before,after in changes.items():
        need(source.count(before)==1,'Only actual first-callback boundary/one-shot/cycle context differs')
        source=source.replace(before,after,1)
    scope=dict(model.knife.knives.__globals__,first_entry=first_entry)
    exec(compile(source,__file__+'::entire_original_knife_true_before_first_callback_context','exec'),scope)
    return scope['knives']


def bindings(guest):
    knife=whole_knife();cache={}
    def gate(text):
        need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),
             'Actual native game/observer has no runtime warnings')
        digest=hashlib.sha256(text.encode()).hexdigest()
        if digest not in cache:cache[digest]=model.verify(text,guest)
        inventory=cache[digest]
        model.knife.source(text,guest)
        shots=knife(text,guest)
        need(shots==[dict(serial=1,start=1814,birth=1817,contact=1838,damage=22,
             actuallyBlocked=False,ownReady=1863,retirement=1862,childFields=45,bodyFields=49,impactGroups=6)],
             'Whole actual unblocked first-round knife, no later-shot acceptance transferred')
        need([(r['move'],r['frame'])for r in inventory['nativeChoices']]==[('knife',1814),('ball',2949)],
             'Both actually chosen source-native routes retained; ball phase not falsely accepted')
        ordered=[]
        for line in text.splitlines():
            if line.startswith('MK2_STARTUP_PROJECTILE_'):ordered.extend(rows(line,line.split()[0]))
        need([int(r['sequence'])for r in ordered]==list(range(1,len(ordered)+1))and
             all(r['writes']=='0'and r['assistance']=='none'for r in ordered),'Entire original ungated observer sequence')
        code=rows(text,'MK2_STARTUP_PROJECTILE_CODE')
        need(len(code)==2 and {(int(r['start'],16),int(r['stop'],16))for r in code}==
             {(0xfffc3800,0xfffc8000),(0xff8b6820,0xff8b69a0)},'Complete constructor/child/retirement windows')
        for r in code:
            lo,hi=((int(r[k],16)-0xff800000)//8 for k in('start','stop'))
            words=[int(w,16)for w in r['words'].split(',')]
            need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi],'Every fetched code word equals current independent guest')
        events=rows(text,'MK2_STARTUP_PROJECTILE_EVENT')
        for r in events:
            at=int(r['entry'],16)
            need(int(r['pc'],16)==at+16 and int(r['mask'],16)==65535 and
                 int(r['opcode'],16)==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0],
                 'Every actual ungated executing opcode and read mask source-bound')
        born=model.knife.one([r for r in events if r['kind']=='knife_child'],'One original ungated child birth')
        ctor=model.knife.one([r for r in events if r['kind']=='knife_create'],'One original ungated constructor')
        entry=model.knife.one([r for r in events if r['kind']=='knife'],'One original ungated parent entry')
        a,m,parent,pm=(int(v,16)for v in(born['a8'],born['a13'],born['parent'],ctor['a13']))
        need((a,m,parent,pm)==(0x010356d0,0x0106d400,0x010350a0,0x0106bf30)and
             (int(entry['frame']),int(ctor['frame']),int(born['frame']))==(1814,1817,1817)and
             entry['a8']==ctor['a8']==ctor['owner']==born['parent']==born['p2']and
             ctor['a13']==born['p2main']and born['owner']==born['a8']and
             born['parent_id']==born['id']=='17'and born['type']=='81'and
             int(born['parameter'],16)==0x80000 and born['mode']=='2'and born['states']=='1,0'and born['roster']=='17,17',
             'Independent original executing constructor/child/type/parent/Main binding')
        fields=rows(text,'MK2_STARTUP_PROJECTILE_FIELD')
        native=model.knife.overlap.rows(text,'CHILD_FIELD');by={r['frame']:r for r in native}
        need([int(r['frame'])for r in fields]==list(range(1818,1863))and len(native)==len(fields)==45,
             'Every actual allocated child callback until native retirement')
        for r in fields:
            n=by[int(r['frame'])]
            need(r['kind']=='knife_child'and int(r['birth'])==1817 and
                 (r['active'],r['free'],r['active_valid'],r['free_valid'])==('1','0','1','1')and
                 int(r['original_parent'],16)==int(r['parent'],16)==n['shot_owner']==parent and
                 all(int(r[k],16)==n[k]for k in('actor','main','owner','pose','xraw','yraw','vx','vy','flags','body','parameter'))and
                 int(r['id'])==n['id']==17 and int(r['type'])==n['type']==81,
                 'Exact independent complete child words and source-native active/free pool membership')
        health=model.knife.one(rows(text,'MK2_STARTUP_PROJECTILE_HEALTH'),'One original independent child collision store')
        need((int(health['frame']),int(health['before']),int(health['after']),int(health['a10'],16))==(1838,161,139,22)and
             (int(health['a8'],16),int(health['a13'],16),int(health['owner'],16),int(health['parent'],16))==(a,m,a,parent)and
             int(health['pc'],16)==0xff836700 and int(health['mask'],16)==65535,
             'The formerly unexplained initial22 HP is an actual owned native child, not CPU or health assistance')
        heads=rows(text,'MK2_BLADE_ALLOC_HEAD_STORE')
        pop=[r for r in heads if r['frame']=='1817'and r['pc']=='FF809150']
        push=[r for r in heads if r['frame']=='1862'and r['pc']=='FF8097D0']
        need(len(pop)==len(push)==2,'Complete actual native low/high sprite pool pop and push')
        for group,pc in((pop,0xff809150),(push,0xff8097d0)):
            need([int(r['at'],16)for r in group]==[0x01060130,0x01060140]and
                 int(group[1]['sequence'])==int(group[0]['sequence'])+1,'Consecutive actual source-owned pool word stores')
            for r in group:
                before,data,mask,merged=(int(r[k],16)for k in('before','data','mask','merged'))
                shift=int(r['at'],16)-0x01060130
                need(int(r['target'],16)==int(r['a0'],16)==a and mask==65535 and
                     merged==((before&(~(mask<<shift)))|((data&mask)<<shift))&0xffffffff and
                     struct.unpack_from('<HHH',guest,(pc-48-0xff800000)//8)==tuple(int(r['op'+str(n)],16)for n in range(3)),
                     'Actual native masked pool arithmetic/object operand/complete source opcodes')
        need(int(pop[0]['before'],16)==a and int(pop[1]['merged'],16)==int(pop[0]['targetNext'],16)==int(pop[0]['a2'],16)and
             (int(pop[0]['a8'],16),int(pop[0]['a13'],16))==(parent,pm)and
             int(push[0]['targetNext'],16)==int(push[0]['before'],16)==int(push[0]['a2'],16)and
             int(push[1]['merged'],16)==a and (int(push[0]['a8'],16),int(push[0]['a13'],16))==(a,m),
             'Original actual constructor allocation and child-owned free-list return')
        retired=model.knife.one(rows(text,'MK2_STARTUP_PROJECTILE_RETIRE'),'One independently observed original retirement')
        need(retired['frame']=='1862'and retired['birth']=='1817'and retired['a8']==born['a8']and
             retired['a13']==born['a13']and int(retired['original_parent'],16)==parent and
             rows(text,'MK2_STARTUP_PROJECTILE_RESULT')[0]['live_children']=='0',
             'Same original child retirement and no remaining allocated observer children')
        return dict(passed=True,wholeNativeStateHPAndChoices=inventory,wholeOriginalFirstRoundKnife=shots,
            ungatedObserverRecords=len(ordered),independentNativePoolPop=pop,independentNativePoolPush=push,
            actualFirstEntryBeforeFirstCallback=True,initialFirstRoundKnifeAccepted=True,
            entryFieldVictimBodyInvented=False,allStartupProjectilesAccepted=False,
            ballPhaseAccepted=False,fullBodyShadowArtAudioAcceptance=False,fullPortAcceptance=False)
    return gate


def execute(state):
    need(not OUT.exists()and not capture.prior.prior.current.prior.identity.census(),'Same original terminal game; no native replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(meta['passed']and meta['nativeExit']==held['process'].poll()==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (44324,38752,1791744064.988737)and not meta['nativeTerminal']['hostDecodeErrors']and
         all(sha(p)==h for p,h in meta['inputHashes'].items()),'Exact original kernel identity, full input hashes and native terminal0')
    expected={'cold_high':state['WINDOWS']['high'],'cold_owned':state['WINDOWS']['owned'],
        'cold_graphics':state['WINDOWS']['graphics'],'guest':state['guest'],'gfx':state['gfx']}
    need(set(meta['proofs'])==set(expected),'All five complete current initialized windows')
    for k,raw in expected.items():
        need(meta['proofs'][k]==dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
            everyActualByteComparedInRAM=True),'Entire current initialized '+k+' independently compared')
    gate=bindings(state['guest']);positive=gate(text)
    mutate=model.original.mutate_field
    def change(tag,key,value,**where):
        return mutate(text,tag,key,value,lambda r:all(r.get(k)==str(v)for k,v in where.items()))
    trials=[
        ('initial_entry_roster',change('MK2_STARTUP_PROJECTILE_EVENT','roster','1,17',kind='knife')),
        ('initial_entry_parent',change('MK2_STARTUP_PROJECTILE_EVENT','p2','01000000',kind='knife')),
        ('initial_entry_main',change('MK2_STARTUP_PROJECTILE_EVENT','p2main','01000000',kind='knife')),
        ('initial_entry_before_callback',change('MK2_CPU_ROUND_BEGIN','frame','1814')),
        ('initial_raster_marker',change('MK2_FIRST_PROJECTILE_ENTRY','actor','01000000')),
        ('native_rng',change('MK2_CPU_CHOICE_EVENT','a0','000000FB',kind='first_call')),
        ('native_state_opcode',change('MK2_CPU_PAIR_FLAG','op0','FFFF')),
        ('knife_parent',change('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000')),
        ('knife_intro_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=1820)),
        ('knife_flight_velocity',change('MK2_CPU_OVERLAP_CHILD_FIELD','vx','00000000',frame=1837)),
        ('knife_impact_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=1842)),
        ('knife_unblocked_damage',change('MK2_CPU_OVERLAP_HEALTH','a10','00000006',frame=1838)),
        ('actual_guard_main',change('MK2_KNIFE_PAIR_TESTED','loaded_main','01000000',frame=1838)),
        ('physical_block',change('MK2_KNIFE_PAIR_BLOCK','controls','FFFFFFDF',frame=1838,decision=2)),
        ('block_branch',change('MK2_KNIFE_PAIR_BLOCK','decision','1',frame=1838,decision=0)),
        ('parent_body_pose',change('MK2_KNIFE_PAIR_FIELD','pose','00000000',frame=1820,slot=2)),
        ('parent_recovery',change('MK2_CPU_OVERLAP_EVENT','body','0056',frame=1863,kind='regain')),
        ('child_retirement',change('MK2_CPU_OVERLAP_RETIRE','frame','1861')),
        ('independent_child_owner',change('MK2_STARTUP_PROJECTILE_EVENT','owner','01000000',kind='knife_child')),
        ('independent_child_opcode',change('MK2_STARTUP_PROJECTILE_EVENT','opcode','FFFF',kind='knife_child')),
        ('independent_child_active',change('MK2_STARTUP_PROJECTILE_FIELD','active','0',frame=1838)),
        ('independent_child_free',change('MK2_STARTUP_PROJECTILE_FIELD','free','1',frame=1838)),
        ('independent_child_parent',change('MK2_STARTUP_PROJECTILE_FIELD','parent','01000000',frame=1838)),
        ('independent_health',change('MK2_STARTUP_PROJECTILE_HEALTH','a10','00000006',frame=1838)),
        ('native_pool_pop',change('MK2_BLADE_ALLOC_HEAD_STORE','a0','01000000',frame=1817,pc='FF809150')),
        ('native_pool_push',change('MK2_BLADE_ALLOC_HEAD_STORE','targetNext','01000000',frame=1862,pc='FF8097D0'))]
    faults=[]
    for label,bad in trials:
        need(bad!=text,'Actual effective first-round corruption '+label)
        try:gate(bad)
        except(AssertionError,ValueError,KeyError,IndexError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual first-round native knife fault admitted '+label)
        print('Current first-round knife fault rejected: '+label,flush=True)
    need(gate(text)==positive,'Whole untouched original native positive restored')
    pins=dict(meta['inputHashes'])
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)
    for path in(Path(__file__),*(p for p in folder.rglob('*')if p.is_file())):pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Complete immutable actual native/executed model inventory')
    OUT.mkdir();value=dict(passed=True,candidate=meta['candidate'],goalStatus='active',actualNativeIdentity=held['identity'],
        sameOriginalTerminalNativePID=44324,actualFirstRoundKnifeAndPool=positive,actualFaultsRejected=faults,
        completeCurrentColdProofs=meta['proofs'],inputHashes=pins,initialFirstRoundKnifeAccepted=True,
        allStartupProjectilesAccepted=False,fullBodyShadowArtAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    capture.prior.prior.current.prior.save(OUT/'report.json',value)
    print('PASS actual first-round knife before first callback/native pool/26 faults; full goal remains active',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original actual qualification failure')
        OUT.mkdir();capture.prior.prior.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),newNativeGames=0,goalStatus='active',fullPortAcceptance=False))
        raise
