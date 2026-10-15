"""Actual blocked CPU knife after native round refill, including pool lifetime.

Entire original knife intro/travel/block/impact/body/recovery/retirement rules.
Only one shot, actual cycle6 and the genuine mode7->2 entry-field context
replace old scenario cardinalities. No old blocked-shot runtime acceptance
transferred. First-round startup projectile ownership remains a separate gap.
"""
import hashlib,json,re,struct,sys,traceback
from pathlib import Path
import capture_native_selector_cpu_startup_guard as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_startup_guard_knife_checked'
model=capture.prior.prior.allocation.phase.model


def rows(text,tag):
    answer=[]
    for line in text.splitlines():
        if not line.startswith(tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(pairs)==len(dict(pairs)),'Unique ungated actual provenance fields')
        answer.append(dict(pairs))
    return answer


def bindings(guest):
    knife=model.bind(model.knife.knives,{
        'assert len(actions)==len(births)==2':'assert len(actions)==len(births)==1',
        "native['mode']==(2 if serial==1 else 7)":"native['mode']==7",
        "child['cycle']==1":"child['cycle']==entry['cycle']==6",
        'damage=22 if serial==1 else 6':'damage=6',
        "assert pressed==(serial==2),'Guard flag alone is not an actually held Block button'":
            "assert pressed,'Actual physical Block must be held, not just the cached guard flag'",
        '(hit+24,m,0xff8b6830,actor,serial,1)':
            "(hit+24,m,0xff8b6830,actor,serial,entry['cycle'])",
        '(m,a,actor,17,81,0x80000,serial,1,0,2)':
            "(m,a,actor,17,81,0x80000,serial,entry['cycle'],0,2)"})
    cache={}
    def gate(text):
        digest=hashlib.sha256(text.encode()).hexdigest()
        if digest not in cache:cache[digest]=model.verify(text,guest)
        inventory=cache[digest]
        model.knife.source(text,guest)
        shots=knife(text,guest)
        need([(r['move'],r['frame'])for r in inventory['nativeChoices']]==[('knife',3498)]and
             shots==[dict(serial=1,start=3498,birth=3501,contact=3527,damage=6,
                actuallyBlocked=True,ownReady=3547,retirement=3551,
                childFields=50,bodyFields=49,impactGroups=6)],
             'Exact genuine blocked shot after native refill, no fabricated first-round startup')
        ordered=[]
        for line in text.splitlines():
            if line.startswith('MK2_STARTUP_PROJECTILE_'):
                ordered.extend(rows(line,line.split()[0]))
        need([int(r['sequence'])for r in ordered]==list(range(1,len(ordered)+1))and
             all(r['writes']=='0'and r['assistance']=='none'for r in ordered),
             'Complete original ungated observer order with no dropped source events')
        code=rows(text,'MK2_STARTUP_PROJECTILE_CODE')
        need({(int(r['start'],16),int(r['stop'],16))for r in code}==
             {(0xfffc3800,0xfffc8000),(0xff8b6820,0xff8b69a0)}and len(code)==2,
             'Entire original constructor, child, release and retirement code windows')
        for r in code:
            lo,hi=((int(r[k],16)-0xff800000)//8 for k in('start','stop'))
            words=[int(w,16)for w in r['words'].split(',')]
            need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi],
                 'Every actually fetched child/constructor word matches current independent guest')
        events=rows(text,'MK2_STARTUP_PROJECTILE_EVENT')
        for r in events:
            at=int(r['entry'],16)
            need(int(r['pc'],16)==at+16 and int(r['mask'],16)==65535 and
                 int(r['opcode'],16)==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0],
                 'Each actual ungated executing source opcode and full read mask')
        birth=model.knife.one([r for r in events if r['kind']=='knife_child'],'One ungated child birth')
        ctor=model.knife.one([r for r in events if r['kind']=='knife_create'],'One ungated native constructor')
        entry=model.knife.one([r for r in events if r['kind']=='knife'],'One ungated native parent entry')
        a,m,parent,pm=(int(v,16)for v in(birth['a8'],birth['a13'],birth['parent'],ctor['a13']))
        need(a==0x010356d0 and m==0x0106cd10 and parent==0x010350a0 and pm==0x0106a370 and
             (int(entry['frame']),int(ctor['frame']),int(birth['frame']))==(3498,3501,3501)and
             entry['a8']==ctor['a8']==birth['p2']==birth['parent']and
             ctor['owner']==ctor['a8']and ctor['p2main']==ctor['a13']and
             birth['owner']==birth['a8']and birth['p2main']==ctor['a13']and
             birth['parent_id']==birth['id']=='17'and birth['type']=='81'and
             int(birth['parameter'],16)==0x80000 and birth['states']=='1,0'and
             birth['mode']=='2'and birth['roster']=='17,17',
             'Independent constructor and child parent/owner/type/process allocation, not global alias inference')
        fields=rows(text,'MK2_STARTUP_PROJECTILE_FIELD')
        native=model.knife.overlap.rows(text,'CHILD_FIELD')
        need([int(r['frame'])for r in fields]==list(range(3502,3552))and len(native)==len(fields),
             'Every ungated allocated child field through actual retirement, not sampled lifetime')
        nb={r['frame']:r for r in native}
        for r in fields:
            f=int(r['frame']);n=nb[f]
            need(r['kind']=='knife_child'and int(r['birth'])==3501 and
                 int(r['original_parent'],16)==parent and r['mode']=='2'and
                 (r['active'],r['free'],r['active_valid'],r['free_valid'])==('1','0','1','1')and
                 all(int(r[k],16)==n[k]for k in
                     ('actor','main','owner','pose','xraw','yraw','vx','vy','flags','body','parameter'))and
                 int(r['parent'],16)==n['shot_owner']==parent and int(r['id'])==n['id']==17 and
                 int(r['type'])==n['type']==81,
                 'Exact independent child words and actual native active/free sprite pool membership')
        health=model.knife.one(rows(text,'MK2_STARTUP_PROJECTILE_HEALTH'),'One ungated child health store')
        need((int(health['frame']),int(health['before']),int(health['after']),int(health['a10'],16))==
             (3527,161,155,6)and int(health['a8'],16)==a and int(health['a13'],16)==m and
             int(health['owner'],16)==a and int(health['parent'],16)==parent and
             int(health['pc'],16)==0xff836700 and int(health['mask'],16)==65535,
             'Independent actual projectile chip-damage store with same lifetime parent/Main')
        inputs={int(r['frame']):r for r in rows(text,'MK2_CPU_PAIR_INPUT')}
        need(all(inputs[f]['buttons']=='Block'and inputs[f]['phase']=='guard_wait'and
                 inputs[f]['writes']=='0'and inputs[f]['assistance']=='none'for f in range(3499,3552)),
             'Entire actual physical held-Block interval, not synthesized guard flags')
        heads=rows(text,'MK2_BLADE_ALLOC_HEAD_STORE')
        pop=[r for r in heads if int(r['frame'])==3501 and r['pc']=='FF809150']
        push=[r for r in heads if int(r['frame'])==3551 and r['pc']=='FF8097D0']
        need(len(pop)==len(push)==2,'Actual full native low/high sprite pool pop and push')
        for group,pc in((pop,0xff809150),(push,0xff8097d0)):
            need([int(r['at'],16)for r in group]==[0x01060130,0x01060140]and
                 int(group[1]['sequence'])==int(group[0]['sequence'])+1,
                 'Both original consecutive native free-head word stores')
            for r in group:
                before,data,mask,merged=(int(r[k],16)for k in('before','data','mask','merged'))
                shift=int(r['at'],16)-0x01060130
                need(mask==65535 and merged==((before&(~(mask<<shift)))|((data&mask)<<shift))&0xffffffff and
                     int(r['target'],16)==int(r['a0'],16)==a and
                     struct.unpack_from('<HHH',guest,(pc-48-0xff800000)//8)==
                         tuple(int(r['op'+str(n)],16)for n in range(3)),
                     'Actual free-head masked store arithmetic, object operand and original native opcodes')
        need(int(pop[0]['before'],16)==a and int(pop[1]['merged'],16)==int(pop[0]['targetNext'],16)==
             int(pop[0]['a2'],16)and int(pop[0]['a8'],16)==parent and int(pop[0]['a13'],16)==pm and
             int(push[0]['targetNext'],16)==int(push[0]['before'],16)==int(push[0]['a2'],16)and
             int(push[1]['merged'],16)==a and int(push[0]['a8'],16)==a and int(push[0]['a13'],16)==m,
             'Independent actual creator pool pop and child-owned native free-list return')
        retired=model.knife.one(rows(text,'MK2_STARTUP_PROJECTILE_RETIRE'),'One ungated retirement')
        need(retired['frame']=='3551'and retired['birth']=='3501'and
             int(retired['original_parent'],16)==parent and retired['a8']==birth['a8']and
             retired['a13']==birth['a13']and int(retired['parent'],16)==parent and
             rows(text,'MK2_STARTUP_PROJECTILE_RESULT')[0]['live_children']=='0',
             'Actual original child retirement and no outstanding observer children')
        return dict(passed=True,wholeNativeStateHPAndChoices=inventory,
            wholeOriginalBlockedKnifeMechanics=shots,independentAllocatedChildFields=len(fields),
            independentNativeSpritePoolPop=pop,independentNativeSpritePoolPush=push,
            ungatedObserverRecords=len(ordered),initialFirstRoundProjectileAccepted=False,
            fullEffectArtAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False)
    return gate


def execute(state):
    need(not OUT.exists()and not capture.prior.prior.current.prior.identity.census(),
         'Same terminal current guard-from-start trial, no new game')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(meta['passed']and meta['nativeExit']==held['process'].poll()==0 and
         not meta['nativeTerminal']['hostDecodeErrors']and len(meta['proofs'])==5 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (39784,38752,1791740868.5522785)and
         all(sha(p)==h for p,h in meta['inputHashes'].items()),
         'Original whole current cold proofs, exact kernel identity and same native terminal handle')
    gate=bindings(state['guest']);positive=gate(text)
    mutate=model.original.mutate_field
    def change(tag,key,value,**where):
        return mutate(text,tag,key,value,lambda r:all(r.get(k)==str(v)for k,v in where.items()))
    trials=[
        ('child_parent',change('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000',frame=3501)),
        ('child_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=3504)),
        ('flight_speed',change('MK2_CPU_OVERLAP_CHILD_FIELD','vx','FFF00000',frame=3527)),
        ('blocked_damage',change('MK2_CPU_OVERLAP_HEALTH','a10','00000016',frame=3527)),
        ('guard_main',change('MK2_KNIFE_PAIR_TESTED','loaded_main','01000000',frame=3527)),
        ('physical_block',change('MK2_KNIFE_PAIR_BLOCK','controls','FFFFFFFF',frame=3527,decision=2)),
        ('impact_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=3530)),
        ('early_retirement',change('MK2_CPU_OVERLAP_RETIRE','frame','3550',frame=3551)),
        ('parent_body_pose',change('MK2_KNIFE_PAIR_FIELD','pose','00000000',frame=3506,slot=2)),
        ('recovery_lock',change('MK2_CPU_OVERLAP_EVENT','body','0056',frame=3547,kind='regain')),
        ('native_rng',change('MK2_CPU_CHOICE_EVENT','a0','000000FB',kind='first_call')),
        ('native_refill',change('MK2_CPU_ROUND_HEALTH','after','160',mode=6,slot=1)),
        ('ungated_birth_owner',change('MK2_STARTUP_PROJECTILE_EVENT','owner','01000000',kind='knife_child')),
        ('ungated_constructor_main',change('MK2_STARTUP_PROJECTILE_EVENT','a13','01000000',kind='knife_create')),
        ('ungated_opcode',change('MK2_STARTUP_PROJECTILE_EVENT','opcode','FFFF',kind='knife_child')),
        ('ungated_source_window',change('MK2_STARTUP_PROJECTILE_CODE','stop','FFFC8010')),
        ('ungated_sequence',change('MK2_STARTUP_PROJECTILE_FIELD','sequence','1',frame=3502)),
        ('active_pool_missing',change('MK2_STARTUP_PROJECTILE_FIELD','active','0',frame=3527)),
        ('freed_too_early',change('MK2_STARTUP_PROJECTILE_FIELD','free','1',frame=3527)),
        ('bad_free_chain',change('MK2_STARTUP_PROJECTILE_FIELD','free_valid','0',frame=3527)),
        ('ungated_parent',change('MK2_STARTUP_PROJECTILE_FIELD','parent','01000000',frame=3527)),
        ('ungated_child_pose',change('MK2_STARTUP_PROJECTILE_FIELD','pose','00000000',frame=3527)),
        ('independent_chip_store',change('MK2_STARTUP_PROJECTILE_HEALTH','after','154',frame=3527)),
        ('pool_pop_target',change('MK2_BLADE_ALLOC_HEAD_STORE','a0','01000000',sequence=2859)),
        ('pool_pop_high_word',change('MK2_BLADE_ALLOC_HEAD_STORE','merged','01000000',sequence=2860)),
        ('pool_push_next',change('MK2_BLADE_ALLOC_HEAD_STORE','targetNext','01000000',sequence=2863)),
        ('pool_push_opcode',change('MK2_BLADE_ALLOC_HEAD_STORE','op0','FFFF',sequence=2864)),
        ('actual_guard_policy',change('MK2_CPU_PAIR_INPUT','buttons','Neutral',frame=3527)),
        ('wrong_native_block_branch',change('MK2_KNIFE_PAIR_BLOCK','decision','0',frame=3527,decision=1)),
        ('entry_mode_not_original',change('MK2_CPU_ROUND_FIELD','mode','2',frame=3498,slot=1)),
        ('child_lifetime_gap',text.replace(next(s+'\n'for s in text.splitlines()if
            s.startswith('MK2_STARTUP_PROJECTILE_FIELD ')and'frame=3510 'in s),'',1))]
    rejected=[]
    for label,bad in trials:
        need(bad!=text,'Actual effective fault '+label)
        try:gate(bad)
        except(AssertionError,ValueError,KeyError,IndexError)as error:
            rejected.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual blocked knife/lifetime fault admitted '+label)
        print('Current blocked knife/lifetime fault rejected: '+label,flush=True)
    need(gate(text)==positive,'Entire untouched original positive restored')
    pins=dict(meta['inputHashes'])
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            pins[str(Path(file).resolve())]=sha(file)
    for path in(Path(__file__),*(p for p in folder.rglob('*')if p.is_file())):
        need(path.suffix.lower()not in('.png','.wav','.bin','.exe','.zip'),'No new raw-media/build copies')
        pins[str(path.resolve())]=sha(path)
    OUT.mkdir();value=dict(passed=True,candidate=meta['candidate'],goalStatus='active',
        nativeIdentity=held['identity'],sameOriginalTerminalNativePID=39784,
        fullCurrentColdProofs=meta['proofs'],actualBlockedKnifeAndLifetime=positive,
        actualFaultsRejected=rejected,inputHashes=pins,fullPortAcceptance=False,
        initialFirstRoundProjectileAccepted=False,fullEffectArtAudioAcceptance=False,
        allCPUContextsAccepted=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    need(all(sha(p)==h for p,h in pins.items()),'Complete original native/model inventory unchanged')
    capture.prior.prior.current.prior.save(OUT/'report.json',value)
    print('PASS actual blocked knife, native sprite pool lifetime, 31 faults; full goal remains active',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original qualifier failure without native replay')
        OUT.mkdir();capture.prior.prior.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),fullPortAcceptance=False,newNativeGames=0,goalStatus='active'))
        raise
