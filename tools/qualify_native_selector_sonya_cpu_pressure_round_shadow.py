"""Whole retained pressure-match body/shadow geometry, including native KO launch.

Independent all-mode physical fields determine every expected draw callback.
Body publication is pre-CPU; shadow publication and POST are post-CPU. No
invented next live PAIR at the actual final mode5 boundary. The stock finishing
blow changes the victim Main floor by32; bind that exact epoch independently,
not a constant-floor waiver. Correct scanout pixels/audio remain separate gaps.
"""
import copy
import inspect
import json
import re
import traceback
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_body_shadow_bound as prior
import inspect_native_smoke_callers as disasm

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
mechanics,capture,body=prior.mechanics,prior.capture,prior.body
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_round_shadow_checked'
HEX={'actor','main','owner','pose','vx','vy','gravity','flags','body','trail'}


def source_gate(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430),
                  (0xff870f10,0xff8714d0),(0xff8de9f0,0xff8deab0),
                  (0xffa0d9d0,0xffa0e210)):
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:z]==stock[a:z],'Whole original body/shadow and finishing-blow source kernels unchanged')
    instructions={int(s.split(':',1)[0],16):s.split(':',1)[1].strip()
                  for s in disasm.disassemble()}
    expected={0xff871030:'MOVI   603h,A0',0xff8712c0:'MOVI   50Ah,A0',
        0xff8dea10:'CMPI   50Ah,A1',0xff8dea30:'JAEQ   FFA0D9D0h',
        0xffa0dcb0:'CMPI   130h,A6',0xffa0dcd0:'JRHI   FFA0DE70h',
        0xffa0de70:'MOVE   *A13(200h),A0,0',0xffa0de90:'SUBI   20h,A0',
        0xffa0deb0:'MOVE   A0,*A13(200h),0',0xffa0ded0:'MOVI   20000h,A0',
        0xffa0df00:'MOVI   FFF40000h,A1',0xffa0df30:'MOVI   6000h,A2',
        0xffa0df50:'MOVK   5h,A3',0xffa0df60:'MOVI   Fh,A9',
        0xffa0dfc0:'JA     FF876650h'}
    need(all(instructions.get(at)==s for at,s in expected.items()),
         'Independent unchanged native final-blow dispatch,32-pixel floor subtraction and launch operands')
    return {f'{at:08X}':s for at,s in expected.items()}


def prepare_context(text,guest):
    whole=mechanics.gate(text,guest)
    pair=mechanics.capture.base.choices.native_state.original.pair
    physical={r['frame']:r for r in pair.rows(text,'FIELD')}
    round_rows=mechanics.capture.base.choices.native_state.rows(text,'MK2_CPU_ROUND_FIELD')
    rounds={(int(r['frame']),int(r['slot'])):r for r in round_rows}
    need(len(rounds)==len(round_rows)==3602,'Every independent all-mode physical row unique and complete')
    expected=set()
    for f in sorted({f for f,s in rounds}):
        a,b=(rounds[f,s] for s in (1,2))
        live=all(r['mode']=='2' and r['states']=='1,0' and r['ids']=='17,18' and
                 r['valid']=='1' and r['actor']==r['owner'] and r['id']==str(16+s)
                 for s,r in ((1,a),(2,b)))
        if live:expected.add(f)
    need(expected==set(physical) and len(expected)==1075,
         'Entire independently derived native live drawing inventory, not a body-observer-defined subset')
    need(min(expected)==1818 and max(expected)==3175 and 2611 in expected and 2610 not in expected,
         'Real first match, round reset and final transition callback boundaries')
    pre={};post={}
    for f in sorted(expected):
        for s in (1,2):
            p=physical[f];prefix='v' if s==1 else ''
            pre[f,s]={k:p['vypos' if s==1 and k=='y' else prefix+k]
                      for k in ('actor','main','owner','pose','id','roster','state','hp','action',
                                'y','floor','vx','vy','gravity','flags','body','trail')}
            q=rounds[f+1,s]
            need(q['writes']=='0' and q['assistance']=='none' and q['valid']=='1',
                 'Genuine next all-mode field, including final mode5, with no fixture assistance')
            post[f,s]={k:int(q[k],16 if k in HEX or k=='action' else 10)
                       for k in ('actor','main','owner','id','hp','action','y','floor',
                                 'vx','vy','gravity','flags','body','trail','mode')}
            post[f,s]['roster']=int(q['ids'].split(',')[s-1])
            post[f,s]['state']=int(q['states'].split(',')[s-1])
            if f+1 in physical:
                p=physical[f+1]
                post[f,s]['pose']=p[prefix+'pose']
            need(pre[f,s]['floor']==(82 if s==1 and f<=3039 else 50 if s==1 else 81) and
                 post[f,s]['floor']==(82 if s==1 and f<3039 else 50 if s==1 else 81),
                 'Exact independent physical native floor epochs; only dead-victim launch changes human anchor')
    launch=[r for r in mechanics.capture.base.choices.native_state.original.overlap.rows(text,'EVENT')
            if r['kind']=='fling' and r['frame']==3039]
    need(len(launch)==1,'One actual native final-blow victim fling, not an invented phase event')
    r=launch[0];human=pre[3039,1]
    need((r['entry'],r['pc'],r['a8'],r['a13'],r['main_owner'],r['id'],r['action'],r['floor'])==
         (0xff876650,0xff876660,human['actor'],human['main'],human['actor'],17,0x50a,50) and
         tuple(r[k]for k in ('a0','a1','a2','a3','a9','a7'))==
         (0x20000,0xfff40000,0x6000,5,15,0xffa0dff0) and human['hp']==0 and
         pre[3039,2]['hp']==post[3039,2]['hp']==161 and post[3039,2]['action']==0x603,
         'Actual dead-victim ownership and source-native launch parameters bind the exact32-pixel epoch')
    return dict(whole=whole,frames=expected,pre=pre,post=post,
                finalPoseNextPhysicalUnavailable=[(3175,1),(3175,2)])


def bindings(guest):
    @lru_cache(maxsize=2)
    def context(text):return prepare_context(text,guest)
    def state_gate(b,current,payload):
        need(current==guest,'Same complete independently derived current guest')
        c=context(b['cpuLog']);posts=b['rows']['MK2_HPHASE_POST_FIELD']
        keys={(int(r['frame']),int(r['slot']))for r in posts}
        need(len(posts)==len(keys)==2150 and keys=={(f,s)for f in c['frames']for s in (1,2)},
             'Both complete draw publications for EVERY independent native live callback')
        by={(int(r['frame']),int(r['slot'])):r for r in posts}
        for key,r in by.items():
            need(r['writes']=='0'and r['assistance']=='none'and
                 all(int(r[k],16 if k in HEX else 10)==v for k,v in c['post'][key].items()),
                 'Every final source word equals genuine next physical actor/Main publication')
        for tag,table in (('MK2_HPHASE_CANDIDATE',c['pre']),('MK2_HPHASE_QUEUE',c['pre']),
                          ('MK2_HPHASE_SHADOW_BEGIN',c['post']),('MK2_HPHASE_PROJECTION',c['post'])):
            for r in b['rows'][tag]:
                key=int(r['frame']),int(r['slot']);need(key in table,'No native draw outside independently expected live fields')
                p=table[key]
                need(all(body.num(r,k)==p[k]for k in ('actor','main','owner','id','body')),
                     'Every body/shadow callback bound to independently observed physical owner and phase')
                need(body.num(r,'pose')==(p['pose'] if 'pose'in p else body.num(by[key],'pose')),
                     'Exact pre/post source pose; final transition agrees with actual POST rather than fake live PAIR')
                if tag=='MK2_HPHASE_PROJECTION':
                    need(body.num(r,'floor')==p['floor']and
                         body.short(body.num(r,'world')>>16)==p['y'],
                         'Every shadow uses exact independent post-CPU physical native floor and world Y')
        return dict(passed=True,wholeActualPressureMechanics=c['whole'],actualDrawFrames=len(c['frames']),
                    physicalDrawCompleteFields=len(posts),nextPhysicalPoseFields=2148,
                    finalTransitionPoseBoundToActualPostAndSourceShadow=True,
                    trueLiveOwnersNeverReallocated=True,nativeFloorLaunchFrame=3039,
                    nativeFloorBefore=82,nativeFloorAfter=50,fullPortAcceptance=False)
    source=inspect.getsource(body.check)
    first=source.index(' # The older physical/ownership/health checker')
    last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
    source=mechanics.phases.replace(source,source[first:last],
        " state=state_gate(b,guest,payload)\n entry_frames={int(r['frame'])for r in rows['MK2_HPHASE_CPU_NATIVE_ENTRY']}\n")
    source=mechanics.phases.replace(source,'ids={side:identity,3-side:4}','ids={1:17,2:18}')
    source=mechanics.phases.replace(source,"num(t,'floor')==floors[s]",
        "num(t,'floor')==context(b['cpuLog'])['post'][f,s]['floor']")
    scope=dict(vars(body),state_gate=state_gate,context=context)
    exec(compile(source,__file__+'::whole_original_geometry_independent_native_KO_floor_epoch','exec'),scope)
    return scope['check']


def execute(state):
    need(not OUT.exists(),'Fresh immutable whole pressure-match geometry result')
    parent=prior.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    need(proof['passed']and meta['passed']and held['process'].poll()==proof['nativeExit']==0 and
         held['identity']==proof['actualNativeIdentity']and all(sha(p)==h for p,h in pins.items()),
         'Same original terminal44780 RAM capture and all prior whole sources unchanged')
    instructions=source_gate(state['guest']);rows=defaultdict(list)
    for line in text.splitlines():
        if not line.startswith('MK2_HPHASE_'):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(pairs)==len(dict(pairs)),'Every actual whole rendering row unambiguous')
        rows[line.split()[0]].append(dict(pairs))
    b=dict(move='leg',side=2,folder=folder,report_path=folder/'result.json',report=meta,cpuLog=text,
           rows=rows,streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
    check=bindings(state['guest']);positive=check(b,state['guest'],state['payload'],state['gfx32'])
    need(positive['state']['wholeActualPressureMechanics']==
         proof['wholeActualInterruptedWindowBodyShadow']['state']['wholeActualPressureMechanics'],
         'Entire original physical/source gate unchanged; pure per-log cache changes no positive acceptance')
    print('PASS all1075 actual live body/shadow fields through both KOs/reset/native finishing blow',flush=True)
    runner=prior.geometry.template.scope['current'].prior.shadow_faults
    faults=runner(dict(b,report=dict(meta,sourceBoundBodyShadowSemantics=positive)),
                  state['guest'],state['payload'],state['gfx32'],check)
    # Effective faults at the actual KO, reset and floor-changing launch, not
    # merely the previous27-field startup/hurt window.
    additional=[]
    for label,tag,frame,slot,key,value in (
        ('first_KO_pose','MK2_HPHASE_POST_FIELD',2324,1,'pose','FF00DAC0'),
        ('first_KO_shadow_owner','MK2_HPHASE_SHADOW_BEGIN',2324,1,'owner','01000000'),
        ('reset_body_source','MK2_HPHASE_CANDIDATE',2611,2,'source','00000000'),
        ('reset_post_HP','MK2_HPHASE_POST_FIELD',2611,1,'hp','160'),
        ('second_KO_body','MK2_HPHASE_POST_FIELD',2942,1,'body','00000012'),
        ('launch_floor_held_standing','MK2_HPHASE_POST_FIELD',3039,1,'floor','82'),
        ('launch_shadow_floor','MK2_HPHASE_PROJECTION',3040,1,'floor','82'),
        ('launch_shadow_Y','MK2_HPHASE_PROJECTION',3040,1,'world','003202FC'),
        ('final_mode_faked_live','MK2_HPHASE_POST_FIELD',3175,1,'mode','2'),
        ('final_pose_disagrees_shadow','MK2_HPHASE_POST_FIELD',3175,2,'pose','FF0311E0')):
        changed=copy.deepcopy(b);r=next(r for r in changed['rows'][tag]if
            int(r['frame'])==frame and int(r['slot'])==slot)
        need(r[key]!=value,'Real effective KO/reset/launch/transition corruption');r[key]=value
        try:check(changed,state['guest'],state['payload'],state['gfx32'])
        except ValueError as error:additional.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Whole pressure geometry fault admitted: '+label)
    changed=copy.deepcopy(b)
    for tag in tuple(changed['rows']):
        changed['rows'][tag]=[r for r in changed['rows'][tag]if r.get('frame')!='2611']
    try:check(changed,state['guest'],state['payload'],state['gfx32'])
    except ValueError as error:additional.append(dict(kind='entire_reset_draw_missing',rejectedBy=str(error)))
    else:raise ValueError('Missing entire independently expected reset callback admitted')
    need(len(faults)==11 and len(additional)==11 and
         check(b,state['guest'],state['payload'],state['gfx32'])==positive,
         'All22 original/whole-round effective counterexamples rejected and full untouched positive restored')
    for p in (Path(__file__),parent,Path(disasm.__file__),ROOT/'mame-mkp/unidasm.exe',
              folder/'shadow_stream_memory_proofs.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source pin replaced');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole source/evidence input freshly checked')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        wholePressureBodyShadowGeometry=positive,nativeFinishBlowStockInstructions=instructions,
        originalBodyShadowFaultsRejected=faults,wholeRoundFaultsRejected=additional,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        wholePressureLiveRoundResetGeometryAccepted=True,nonliveRoundTransitionPixelsAccepted=False,
        completeFinisherChoreographyAccepted=False,wholeDisplayedPixelsAccepted=False,wholeSourceAudioAccepted=False,
        allArenaCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS whole actual pressure native geometry with22 effective faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual whole pressure geometry rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
