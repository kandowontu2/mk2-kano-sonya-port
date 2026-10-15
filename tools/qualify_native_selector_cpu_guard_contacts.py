"""All actual direct CPU contacts after real guard-hold, including native KO clamp.

Exact two independent HP observers, real physical Block query, stock decision
entry and executing Main. This is ordinary contact blocking, not blocked knife,
all move cleanup or all victim/arena/slot acceptance. Reuse the terminal game.
"""
import hashlib,json,re,struct,traceback
from pathlib import Path
import capture_native_selector_cpu_guard_shadow as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_guard_contacts_checked'
model=capture.prior.allocation.phase.model


def rows(text,tag):
    answer=[]
    for line in text.splitlines():
        if not line.startswith(tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(pairs)==len(dict(pairs)),'Unique actual controller/guard query fields')
        answer.append(dict(pairs))
    return answer


def bindings(guest):
    cache={}
    def gate(text):
        digest=hashlib.sha256(text.encode()).hexdigest()
        if digest not in cache:cache[digest]=model.verify(text,guest)
        inventory=cache[digest]
        model.knife.source(text,guest)
        fields={r['frame']:r for r in model.original.pair.rows(text,'FIELD')}
        controls=rows(text,'MK2_CPU_PAIR_CONTINUATION_INPUT')
        cb={int(r['frame']):r for r in controls}
        need(len(cb)==len(controls)and controls and min(cb)==2244 and
             all(r['policy']=='guard_hold'and r['writes']=='0'and r['assistance']=='none'for r in controls),
             'Distinct genuine physical guard-hold route, not forced victim flags')
        rich=model.knife.overlap.rows(text,'HEALTH')
        health=model.knife.R.rows(text,'HEALTH')
        queries=model.knife.rows(text,'BLOCK')
        selected=[]
        for r in rich:
            f=r['frame'];native=fields.get(f)
            if f<min(cb)or r['before']<=r['after']or not native:continue
            if (r['a8'],r['a13'])!=(native['actor'],native['main']):continue
            selected.append(r)
        need(len(selected)==33,'Every observed direct CPU contact in the physical held-guard interval')
        accepted=[]
        for h in selected:
            f=h['frame'];native=fields[f];actor,main=native['actor'],native['main']
            victim,vmain=native['vactor'],native['vmain']
            need(f in cb and (h['slot'],h['at'],h['mask'],h['pc'],h['main_owner'],h['id'])==
                 (1,0x010602f0,65535,0xff836700,actor,17)and
                 native['owner']==actor and native['vowner']==victim and
                 (native['state'],native['vstate'],native['id'],native['vid'],native['mode'])==(0,1,17,17,2)and
                 h['writes']==0 and h['assistance']=='none',
                 'Direct actual executing CPU Main/target fighter/HP address, not projectile or actor aliases')
            matches=[r for r in health if all(r[k]==h[k]for k in
                ('frame','slot','at','before','after','mask','pc','a8','a13'))]
            need(len(matches)==1,'Exact independent all-mode HP store, original instruction and execution operands')
            button=model.knife.one([r for r in queries if r['frame']==f and r['actor']==actor and r['decision']==2],
                                   'One real target physical Block query at the exact contact')
            need((button['entry'],button['pc'],button['main'],button['owner'],button['process_slot'])==
                 (0xff832040,0xff832050,vmain,victim,1)and
                 ((~button['controls']&0xffffffff)&0x80000020)==0x20,
                 'Real P1 Block held, independently queried under its actual Main; no synthetic guard')
            decision=model.knife.one([r for r in queries if r['frame']==f and r['actor']==actor and r['decision']in(0,1)],
                                     'One actual native collision branch')
            need((decision['main'],decision['owner'],decision['process_slot'],decision['controls'])==
                 (main,actor,2,button['controls'])and decision['entry']==
                 (0xff837bd0 if decision['decision']else 0xff837ae0)and
                 decision['pc']==decision['entry']+16 and
                 all(q['writes']==0 and q['assistance']=='none'for q in(button,decision)),
                 'Actual source-native block branch executing under CPU Main, not inferred from held input alone')
            need(h['a10']>0 and h['after']==max(0,h['before']-h['a10']),
                 'Actual native damage operand and original zero-health clamp, including blocked chip KO')
            accepted.append(dict(frame=f,actuallyBlocked=bool(decision['decision']),
                before=h['before'],after=h['after'],nativeDamageOperand=h['a10'],
                actualDamage=h['before']-h['after'],actor=actor,main=main,victim=victim,vmain=vmain))
        blocked=[r for r in accepted if r['actuallyBlocked']]
        not_blocked=[r for r in accepted if not r['actuallyBlocked']]
        need(len(blocked)==32 and [(r['frame'],r['nativeDamageOperand'])for r in not_blocked]==[(3030,20)]and
             next(r for r in blocked if r['frame']==2548)['before']==1 and
             next(r for r in blocked if r['frame']==2548)['after']==0,
             'Exact observed32 blocked contacts, separate real unblocked branch and earned chip KO; no universal held-Block claim')
        return dict(passed=True,wholeNativeStateHPAndChoices=inventory,actualContacts=accepted,
            blockedDirectContacts=32,actualUnblockedWhileButtonHeld=not_blocked,
            blockedKnifeAccepted=False,allMoveVictimSlotArenaAccepted=False,fullPortAcceptance=False)
    return gate


def execute(state):
    need(not OUT.exists()and not capture.prior.current.prior.identity.census(),
         'Same current guard native terminal, new immutable qualification')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    report=json.loads((folder/'result.json').read_text())
    need(report['passed']and report['nativeExit']==capture.NATIVE_HANDLES[capture.KEY]['process'].poll()==0 and
         not report['nativeTerminal']['hostDecodeErrors']and
         all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Original full current native transport/state/terminal proof unchanged')
    gate=bindings(state['guest']);positive=gate(text)
    mutate=model.original.mutate_field
    def change(tag,key,value,**where):
        return mutate(text,tag,key,value,lambda r:all(r.get(k)==str(v)for k,v in where.items()))
    trials=[
        ('physical_block_not_held',change('MK2_KNIFE_PAIR_BLOCK','controls','FFFFFFFF',frame=2255,decision=2)),
        ('physical_wrong_main',change('MK2_KNIFE_PAIR_BLOCK','main','01000000',frame=2255,decision=2)),
        ('physical_wrong_slot',change('MK2_KNIFE_PAIR_BLOCK','process_slot','2',frame=2255,decision=2)),
        ('branch_not_blocked',change('MK2_KNIFE_PAIR_BLOCK','decision','0',frame=2255,decision=1)),
        ('branch_wrong_owner',change('MK2_KNIFE_PAIR_BLOCK','owner','01000000',frame=2255,decision=1)),
        ('branch_wrong_pc',change('MK2_KNIFE_PAIR_BLOCK','pc','FF837AF0',frame=2255,decision=1)),
        ('health_cpu_alias',change('MK2_CPU_OVERLAP_HEALTH','a8','01000000',frame=2255)),
        ('health_main_owner',change('MK2_CPU_OVERLAP_HEALTH','main_owner','01000000',frame=2255)),
        ('health_independent_context',change('MK2_CPU_OVERLAP_HEALTH','before','160',frame=2255)),
        ('health_damage_operand',change('MK2_CPU_OVERLAP_HEALTH','a10','00000003',frame=2255)),
        ('native_chip_ko_clamp',change('MK2_CPU_OVERLAP_HEALTH','after','65535',frame=2548)),
        ('held_button_does_not_fabricate_block',change('MK2_KNIFE_PAIR_BLOCK','decision','1',frame=3030,decision=0)),
        ('controller_policy',change('MK2_CPU_PAIR_CONTINUATION_INPUT','policy','neutral_hold',frame=2255)),
        ('missing_native_branch',text.replace(next(s+'\n'for s in text.splitlines()if
            s.startswith('MK2_KNIFE_PAIR_BLOCK ')and'frame=2255 'in s and'decision=1 'in s),'',1))]
    rejected=[]
    for label,bad in trials:
        need(bad!=text,'Actual effective contact/input fault '+label)
        try:gate(bad)
        except(AssertionError,ValueError)as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual contact/input corruption '+label)
        print('Current real block fault rejected: '+label,flush=True)
    need(gate(text)==positive,'Entire exact positive restored after all14 contact faults')
    pins=dict(report['inputHashes'])
    for path in(Path(__file__),Path(model.__file__),Path(model.knife.__file__),
                *(p for p in folder.rglob('*')if p.is_file())):pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All original native/model inputs stable')
    OUT.mkdir();value=dict(passed=True,candidate=report['candidate'],goalStatus='active',
        actualOriginalNativePID=capture.NATIVE_HANDLES[capture.KEY]['process'].pid,
        originalSourceBoundGuardContacts=positive,actualFaultsRejected=rejected,
        inputHashes=pins,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,
        publicPlayableChanged=False,blockedKnifeAccepted=False,fullPortAcceptance=False)
    capture.prior.current.prior.save(OUT/'report.json',value)
    print('PASS actual32 blocked direct contacts, one separate unblocked branch, 14 faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original contact qualifier rejection')
        OUT.mkdir();capture.prior.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False,goalStatus='active'))
        raise
