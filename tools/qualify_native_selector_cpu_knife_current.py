"""Whole current unblocked CPU knife and 1800-field native state/HP history.

Use the same retained terminal game, not another boot. The original capture
stays rejected for duplicate RGB requests. No visual/PCM acceptance from it.
Keep the entire original knife mechanics; only one shot and its real cycle
replace the old two-shot scenario cardinality. Ball and blade stay pending.
"""
import datetime,json,re,sys
from pathlib import Path
import capture_native_selector_cpu_blade_knife as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_knife_current_checked'
model=capture.allocation.phase.model


def bindings():
    knife=model.bind(model.knife.knives,{
        'assert len(actions)==len(births)==2':'assert len(actions)==len(births)==1',
        "child['cycle']==1":"child['cycle']==entry['cycle']",
        '(hit+24,m,0xff8b6830,actor,serial,1)':
            "(hit+24,m,0xff8b6830,actor,serial,entry['cycle'])",
        '(m,a,actor,17,81,0x80000,serial,1,0,2)':
            "(m,a,actor,17,81,0x80000,serial,entry['cycle'],0,2)"})
    def gate(text,guest):
        need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),
             'Actual game/observer no runtime warnings; host RGB collision separate')
        for parser,tags in((model.knife.rows,('FIELD','GUARD','TESTED','BLOCK','RESULT','CODE')),
                (model.knife.overlap.rows,('EVENT','CHILD','CHILD_FIELD','HEALTH','RETIRE','RESULT','CODE'))):
            for tag in tags:
                need(all(r['writes']==0 and r['assistance']=='none'for r in parser(text,tag)),
                     'All original actual projectile/guard observations passive')
        inventory=model.verify(text,guest)
        model.knife.source(text,guest)
        shots=knife(text,guest)
        need([(r['move'],r['frame'])for r in inventory['nativeChoices']]==
             [('ball',2211),('knife',3112)],'Exact observed current choices, no claimed blade')
        need(len(shots)==1 and shots[0]==dict(serial=1,start=3112,birth=3115,contact=3135,
            damage=22,actuallyBlocked=False,ownReady=3161,retirement=3159,
            childFields=44,bodyFields=49,impactGroups=6),
            'Whole exact source-derived actual current projectile chronology')
        return dict(passed=True,wholeNativeStateHPAndChoices=inventory,
            wholeOriginalKnifeMechanics=shots,allCPUContextsAccepted=False,
            ballPhaseAccepted=False,bladePhaseAccepted=False,
            fullArtAudioAcceptance=False,fullPortAcceptance=False)
    return gate


def execute(state):
    need(not OUT.exists(),'New immutable same-game qualification, never replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    report=json.loads((folder/'result.json').read_text())
    terminal=json.loads((folder/'native_terminal.json').read_text())
    retained=capture.NATIVE_HANDLES[capture.KEY]
    need(not report['passed']and report['error']==
         "ValueError('Same actual natural native terminal0, complete current inventories and no runtime/host warnings')"and
         terminal['hostDecodeErrors']==[dict(stage='transport',error=
            "ValueError('Unique original physical frame_done scene')")]*3,
         'Original exact three RGB-only host rejections preserved, no waiver of whole capture')
    need(retained['process'].pid==terminal['pid']==45992 and retained['process'].poll()==0 and
         terminal['nativeExit']==report['nativeExit']==0 and
         retained['identity']==terminal['actualWindowsIdentity'] and
         retained['identity']['ParentProcessId']==38752 and
         retained['identity']['createdUnix']==1791738335.6988811 and
         retained['identity']['CommandLine']==capture.current.prior.subprocess.list2cmdline(retained['command'])and
         not capture.current.prior.identity.census()and not(folder/'stderr.log').read_text(),
         'Exact original kernel PID/parent/birth/full command and naturally terminal handle')
    expected={'cold_high':state['WINDOWS']['high'],'cold_owned':state['WINDOWS']['owned'],
        'cold_graphics':state['WINDOWS']['graphics'],'guest':state['guest'],'gfx':state['gfx']}
    need(set(report['proofs'])==set(expected),'All five actual current byte proofs retained')
    import hashlib
    for kind,raw in expected.items():
        need(report['proofs'][kind]==dict(bytes=len(raw),
            sha256=hashlib.sha256(raw).hexdigest().upper(),everyActualByteComparedInRAM=True),
            'Entire original initialized/current '+kind+' independently compared')
    pins=dict(report['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'All original executed sources/build unchanged')
    gate=bindings();positive=gate(text,state['guest'])
    mutate=model.original.mutate_field
    def change(tag,key,value,**where):
        return mutate(text,tag,key,value,lambda row:all(row.get(k)==str(v)for k,v in where.items()))
    # All twelve applicable original v6304 knife/native faults; nine absent
    # blade faults remain pending rather than silently credited.
    trials=[
        ('knife_child_parent',change('MK2_CPU_OVERLAP_CHILD','shot_owner','01000000',frame=3115)),
        ('knife_child_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=3118)),
        ('knife_flight_speed',change('MK2_CPU_OVERLAP_CHILD_FIELD','vx','FFF00000',frame=3135)),
        ('knife_hit_damage',change('MK2_CPU_OVERLAP_HEALTH','a10','00000006',frame=3135)),
        ('knife_guard_main',change('MK2_KNIFE_PAIR_TESTED','loaded_main','01000000',frame=3135)),
        ('knife_false_button',change('MK2_KNIFE_PAIR_BLOCK','controls','FFFFFFDB',frame=3135,decision=2)),
        ('knife_impact_pose',change('MK2_CPU_OVERLAP_CHILD_FIELD','pose','00000000',frame=3137)),
        ('knife_early_retire',change('MK2_CPU_OVERLAP_RETIRE','frame','3158',frame=3159)),
        ('knife_body_pose',change('MK2_KNIFE_PAIR_FIELD','pose','00000000',frame=3120,slot=2)),
        ('knife_ready_lock',change('MK2_CPU_OVERLAP_EVENT','body','0056',frame=3161,kind='regain')),
        ('native_rng_threshold',change('MK2_CPU_CHOICE_EVENT','a0','000000FB',kind='first_call')),
        ('native_round_refill',change('MK2_CPU_ROUND_HEALTH','after','160',mode=6,slot=1)),
        ('knife_birth_owner',change('MK2_CPU_OVERLAP_CHILD','main_owner','01000000',frame=3115)),
        ('knife_birth_main',change('MK2_CPU_OVERLAP_CHILD','a13','01000000',frame=3115)),
        ('knife_birth_cycle',change('MK2_CPU_OVERLAP_CHILD','cycle','4',frame=3115)),
        ('knife_parent_entry',change('MK2_CPU_OVERLAP_EVENT','main_owner','01000000',frame=3112,kind='knife')),
        ('knife_child_lifetime_gap',text.replace(next(s+'\n'for s in text.splitlines()
            if s.startswith('MK2_CPU_OVERLAP_CHILD_FIELD ')and'frame=3120 'in s),'',1)),
        ('knife_intro_placement',change('MK2_CPU_OVERLAP_CHILD_FIELD','xraw','00000000',frame=3118)),
        ('knife_impact_placement',change('MK2_CPU_OVERLAP_CHILD_FIELD','yraw','00000000',frame=3137)),
        ('knife_contact_health',change('MK2_CPU_OVERLAP_HEALTH','after','108',frame=3135)),
        ('knife_retire_parent',change('MK2_CPU_OVERLAP_RETIRE','shot_owner','01000000',frame=3159)),
        ('knife_retire_cycle',change('MK2_CPU_OVERLAP_RETIRE','child_cycle','4',frame=3159)),
        ('knife_after_ready_lock',change('MK2_KNIFE_PAIR_FIELD','flags','0010',frame=3162,slot=2)),
        ('all_mode_field_gap',text.replace(next(s+'\n'for s in text.splitlines()
            if s.startswith('MK2_CPU_ROUND_FIELD ')and'frame=2729 'in s and'slot=1 'in s),'',1)),
        ('earned_ko_source',change('MK2_CPU_ROUND_HEALTH','op0','FFFF',frame=2542,slot=1)),
        ('post_reset_proxy',change('MK2_CPU_ROUND_FIELD','id','1',frame=3000,slot=2)),
        ('native_state_opcode',change('MK2_CPU_PAIR_FLAG','op0','FFFF')),
        ('native_state_target',change('MK2_CPU_PAIR_FLAG','at','01000000'))]
    rejected=[]
    for label,bad in trials:
        need(bad!=text,'Actual effective fault '+label)
        try:gate(bad,state['guest'])
        except(AssertionError,ValueError)as error:
            rejected.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual fault accepted: '+label)
        print('Current knife fault rejected: '+label,flush=True)
    need(gate(text,state['guest'])==positive,'Exact whole untouched positive restored')
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            pins[str(Path(file).resolve())]=sha(file)
    for path in [Path(__file__),*(p for p in folder.rglob('*')if p.is_file())]:
        need(path.suffix.lower()not in('.png','.wav','.bin','.exe','.zip'),
             'No raw media/build/ROM copies')
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All complete native/source inventories unchanged')
    OUT.mkdir();value=dict(passed=True,candidate=report['candidate'],goalStatus='active',
        observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        actualOriginalNativePID=terminal['pid'],nativeIdentity=retained['identity'],
        wholeOriginalNativeKnifeAndStateHP=positive,actualFaultsRejected=rejected,
        originalCaptureRemainsRejected=True,originalRGBRequestsRejected=3,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        publicPlayableChanged=False,inputHashes=pins,fullPortAcceptance=False,
        fullArtAudioAcceptance=False,allCPUContextsAccepted=False,
        originalApplicableKnifeNativeFaults=12,absentOriginalBladeFaultsStillPending=9,
        unknownProjectileOwnershipWaived=False,
        nextAction='Broader current CPU routes, actual projectile raster/shadows/audio, blocking and cross-victims')
    capture.current.prior.save(OUT/'report.json',value)
    print('PASS current original CPU knife, 1800-field state/HP, 28 faults; no full port claim',flush=True)
    return value
