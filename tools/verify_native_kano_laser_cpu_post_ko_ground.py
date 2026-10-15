"""Same actual native KO/reset job with independently observed arena ground.

Keep the earlier 217-135 hardcoded-ground rejection intact. The actual native
stage floor is 216; both independent observers publish Main floor81. Derive
the imported135 anchor from each actual paired callback, not a guessed pixel
baseline. Preserve all native health/store/reset/window invariants.
"""
import inspect
import json
import re
import traceback
from collections import defaultdict
from pathlib import Path
import verify_native_kano_laser_cpu_post_ko_ledger as prior
import verify_native_kano_laser_cpu_leg_owned_trace as mutation

ROOT,need,once=prior.ROOT,prior.need,prior.once
base=mutation.base
sha=mutation.sha
OUT=ROOT/'audit_native_kano_laser_cpu_post_ko_ground_checked'


def binding():
    source=inspect.getsource(prior.check)
    source=once(source,'    for frame in range(restart,last+1):',
        """    paired_rows=original.pair.rows(text,'FIELD')
    paired={r['frame']:r for r in paired_rows}
    need(len(paired)==len(paired_rows),'Unique actual paired callback across native rounds')
    for frame in range(restart,last+1):
        need(frame in paired,'Every actual independently observed post-reset paired callback')""")
    source=once(source,"            r=by[frame,slot]\n            need(r['mode']==2",
        """            r=by[frame,slot];prefix='v'if slot==1 else''
            need(all(r[k]==paired[frame][prefix+k]for k in
                     ('actor','main','owner','id','action','floor','vx','vy','gravity','flags','body','trail','hp')),
                 'Both independent physical observers agree on every resumed owned actor/Main/health/state word')
            need(r['mode']==2""")
    source=once(source,"r['floor']==217-135 and 0<r['hp']<=161",
        "r['floor']==paired[frame]['stage_floor']-135 and 0<r['hp']<=161")
    scope=dict(vars(prior))
    exec(compile(source,__file__+'::whole_original_native_KO_ledger_actual_independent_arena_ground','exec'),scope)
    return scope['check']


def run(actual):
    need(not OUT.exists() and not base.identity.census(),'Same actual native post-KO terminal; no replay')
    folder,text,images=actual.RAM_CASES[actual.KEY]
    metadata=json.loads((folder/'result.json').read_text())
    need(not metadata['passed'] and metadata['nativeExit']==0 and not metadata['nativeTerminal']['hostDecodeErrors'] and
         metadata['error']=="ValueError('Both rebuilt true Sonya actors remain actually owned and grounded in live next-round combat')" and
         all(sha(p)==h for p,h in metadata['inputHashes'].items()),
         'Preserve actual 217-floor model rejection and every current compiled/native/observer source')
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
            rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    b=dict(move='leg',side=2,folder=folder,report=metadata,rows=rows,streams=[],human='sonya',cpuLog=text)
    check=binding();positive=check(b,actual.guest,actual.payload,actual.gfx32)
    passive=base.channels_gate(text,int(prior.rows(text,'RESULT')[0]['frame']))
    actual_rows=prior.original.rounds.rows(text,'FIELD')
    first_reset=positive['health']['actualRoundResets'][0]
    ko=positive['earnedKO'];restart=positive['actualNativeResume'];last=positive['last']
    mutate=lambda tag,key,value,predicate=lambda r:True:mutation.mutate_line(text,tag,key,value,predicate)
    def remove(tag,predicate=lambda r:True):
        line=next(s for s in text.splitlines()if s.startswith(tag+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',s))))
        return text.replace(line+'\n','',1)
    resumed_field=lambda r:int(r['frame'])==restart and r['slot']=='1'
    reset_store=lambda r:int(r['frame'])==first_reset['frame']and r['slot']==str(first_reset['slot'])
    trials=[
        ('all_mode_winner_field_missing',remove('MK2_CPU_ROUND_FIELD',lambda r:r['mode']=='5')),
        ('native_KO_health_store_missing',remove('MK2_CPU_ROUND_HEALTH',lambda r:r['mode']=='2'and r['after']=='0')),
        ('native_KO_health_amount_wrong',mutate('MK2_CPU_ROUND_HEALTH','after','1',lambda r:r['mode']=='2'and r['after']=='0')),
        ('native_round_reset_store_missing',remove('MK2_CPU_ROUND_HEALTH',reset_store)),
        ('native_round_reset_instruction_wrong',mutate('MK2_CPU_ROUND_HEALTH','op0','FFFF',reset_store)),
        ('native_round_reset_mask_wrong',mutate('MK2_CPU_ROUND_HEALTH','mask','00FF',reset_store)),
        ('native_round_reset_amount_wrong',mutate('MK2_CPU_ROUND_HEALTH','after','160',reset_store)),
        ('native_precombat_fill_sentinel_wrong',mutate('MK2_CPU_ROUND_HEALTH','after','5',lambda r:r['mode']=='7'and r['before']=='65535')),
        ('independent_winner_words_disagree',mutate('MK2_CPU_ROUND_FIELD','winner','99',lambda r:r['mode']=='5')),
        ('resumed_native_owner_wrong',mutate('MK2_CPU_ROUND_FIELD','owner','01000000',resumed_field)),
        ('resumed_native_identity_wrong',mutate('MK2_CPU_ROUND_FIELD','id','1',resumed_field)),
        ('resumed_native_floor_wrong',mutate('MK2_CPU_ROUND_FIELD','floor','999',resumed_field)),
        ('independent_resumed_stage_ground_wrong',mutate('MK2_CPU_PAIR_FIELD','stage_floor','999',lambda r:int(r['frame'])==restart)),
        ('resumed_native_Main_wrong',mutate('MK2_CPU_PAIR_FIELD','vmain','01000000',lambda r:int(r['frame'])==restart)),
        ('final_actual_round_field_missing',remove('MK2_CPU_ROUND_FIELD',lambda r:int(r['frame'])==last)),
        ('declared_resume_time_wrong',mutate('MK2_POST_KO_RESUMED','frame',str(restart+1)))]
    faults=[]
    for label,changed in trials:
        need(changed!=text,'Each native KO/reset fault changes one actual observed record')
        try:check(dict(b,cpuLog=changed),actual.guest,actual.payload,actual.gfx32)
        except(ValueError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native KO/reset/ownership fault accepted: '+label)
    need(len(faults)==16 and check(b,actual.guest,actual.payload,actual.gfx32)==positive,
         'All sixteen actual semantic counterexamples reject and full positive restores')
    pins=dict(metadata['inputHashes'])
    for p in (Path(__file__),Path(prior.__file__),Path(prior.original.__file__),Path(prior.original.rounds.__file__),
              folder/'result.json',folder/'native_terminal.json',folder/'run.log.gz',actual.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All executed code/candidate/evidence remains immutable')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=actual.native.NAME,key=actual.KEY,
        actualNativeKORoundResume=positive,actualSemanticFaultsRejected=faults,passiveSoundChannels=passive,
        originalHardcodedFloorModelFailurePreserved=True,gameplayReplayed=False,
        actualAllModeHealthFields=len(actual_rows),rawImagesStillInRAM=len(images),
        fullPostKOBodyShadowAcceptance=False,postResetHumanControlResponseAcceptance=False,
        fullVisualTimelineAccepted=False,fullAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False,
        inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active'))
    print(json.dumps(dict(passed=True,actualNativeModes=positive['actualModes'],nativeResume=restart,
                         allModeFields=len(actual_rows),semanticFaults=len(faults),fullPortAcceptance=False)),flush=True)


def execute(actual):
    try:run(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual post-KO successor failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
