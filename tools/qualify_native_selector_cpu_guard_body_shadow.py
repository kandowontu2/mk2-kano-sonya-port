"""Actual current continuous native Kano bodies/shadows across KO and reset.

Whole original body, ROM stream and quarter-height shadow model. All live
drawing keys derive from independent all-mode physical pre-fields, not the
fields a collector happened to emit. No knife/blade/block/PCM/full-port claim.
"""
import copy,hashlib,inspect,json,re,struct,traceback
from collections import defaultdict
from pathlib import Path
import capture_native_selector_cpu_guard_shadow as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_guard_body_shadow_checked'
current=capture.prior.current
body=current.prior.shadow
model=capture.prior.allocation.phase.model


def bindings(guest):
    physical_cache={}
    def state_gate(b,current_guest,payload):
        need(current_guest==guest,'Entire retained independent current guest')
        text=b['cpuLog'];digest=hashlib.sha256(text.encode()).hexdigest()
        if digest not in physical_cache:
            physical_cache[digest]=model.verify(text,guest)
        physical=physical_cache[digest]
        round_fields=model.knife.R.rows(text,'FIELD')
        rb={(r['frame'],r['slot']):r for r in round_fields}
        last=max(f for f,s in rb)
        expected=set()
        for f,s in rb:
            if s!=1 or f>=last:continue
            a,c=rb[f,1],rb[f,2]
            if a['mode']==c['mode']==2 and a['states']==c['states']=='1,0'and
                    a['valid']==c['valid']==1 and a['id']==c['id']==17 and
                    a['owner']==a['actor']and c['owner']==c['actor']:
                expected.add(f)
        posts=b['rows']['MK2_HPHASE_POST_FIELD']
        by={(int(r['frame']),int(r['slot'])):r for r in posts}
        need(len(by)==len(posts)and set(by)=={(f,s)for f in expected for s in(1,2)},
             'Every independently expected live drawing field; KO/reset gaps not omitted ad hoc')
        pair={r['frame']:r for r in model.original.pair.rows(text,'FIELD')}
        begins={(int(r['frame']),int(r['slot'])):r for r in b['rows']['MK2_HPHASE_SHADOW_BEGIN']}
        owners={};floors={}
        for (f,s),r in by.items():
            target=rb[f+1,s]
            keys=('actor','main','owner','id','action','y','floor','vx','vy','gravity','flags','body','trail','hp','mode')
            need(r['writes']=='0'and r['assistance']=='none'and
                 all(body.num(r,k)==target[k]for k in keys)and
                 int(r['roster'])==17 and int(r['state'])==(1 if s==1 else 0),
                 'Each actual draw-complete actor word binds next independent all-mode pre-callback')
            identity=(body.num(r,'actor'),body.num(r,'main'))
            if s not in owners:owners[s]=identity;floors[s]=int(r['floor'])
            need(identity==owners[s]and body.num(r,'owner')==identity[0]and
                 int(r['floor'])==floors[s]==82,
                 'Stable true native owner and source-bound Main floor across real KO/reset')
            native=pair.get(f+1)
            if native:
                prefix='v'if s==1 else''
                need(all(body.num(r,k)==native[prefix+k]for k in
                    ('actor','main','owner','pose','action','floor','vx','vy','gravity','flags','body','trail'))and
                    int(r['x'])==native['vxpos'if s==1 else'x'],
                    'Every subsequent live pair pose/location/lock agrees with native completed drawing')
            begin=begins.get((f,s))
            need(begin and all(body.num(r,k)==body.num(begin,k)for k in
                ('actor','main','owner','id','pose','body')),
                'Even KO-boundary post pose binds independently executing actual native shadow call')
        entries=b['rows']['MK2_HPHASE_CPU_NATIVE_ENTRY']
        routines=dict(knife=0xffffb000,ball=0xffffde00,blade=0xfff8cc00,choke=0xfff91400)
        for r in entries:
            at=body.num(r,'entry') if 'entry'in body.HEX else int(r['entry'],16)
            need(r['kind']in routines and at==routines[r['kind']]and int(r['pc'],16)==at+16 and
                 int(r['opcode'],16)==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0]and
                 int(r['mask'],16)==65535 and (int(r['actor'],16),int(r['main'],16))==owners[2]and
                 r['owner']==r['actor']and r['id']==r['roster']=='17'and r['state']=='0'and
                 r['writes']=='0'and r['assistance']=='none'and int(r['frame'])in expected,
                 'Actual executing CPU routine entry/current opcode/role, not fixed expected-move labels')
        return dict(wholeNativeStateHPAndChoices=physical,expectedNativeDrawingFrames=sorted(expected),
            owners=owners,floors=floors,ids={1:17,2:17},actualSourceBoundCPUEntries=len(entries),
            physicalDrawCompleteFields=len(posts),fullMoveBlockPCMArtAcceptance=False)
    source=inspect.getsource(body.check)
    first=source.index(' # The older physical/ownership/health checker')
    last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
    source=current.replace(source,source[first:last],
        " state=state_gate(b,guest,payload)\n entry_frames={int(r['frame'])for r in rows['MK2_HPHASE_CPU_NATIVE_ENTRY']}\n")
    source=current.replace(source,'ids={side:identity,3-side:4}','ids={1:17,2:17}')
    namespace=dict(vars(body),state_gate=state_gate)
    exec(compile(source,__file__+'::entire_original_body_ROM_shadow_model_current_native_CPU','exec'),namespace)
    return namespace['check']


def execute(state):
    need(not OUT.exists()and not current.prior.identity.census(),'Same original guard trial terminal; no replay')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    report=json.loads((folder/'result.json').read_text())
    held=capture.NATIVE_HANDLES[capture.KEY]
    need(report['passed']and report['nativeExit']==held['process'].poll()==0 and
         not report['nativeTerminal']['hostDecodeErrors']and len(report['proofs'])==5 and
         all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Actual same original terminal native current startup/state/transport pass')
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith('MK2_HPHASE_'):
            pairs=re.findall(r'(\w+)=([^\s]+)',line)
            need(len(pairs)==len(dict(pairs)),'Unique actual native draw metadata')
            rows[line.split()[0]].append(dict(pairs))
    b=dict(move='choke',side=2,folder=folder,report_path=folder/'result.json',report=report,
        cpuLog=text,rows=rows,streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
    check=bindings(state['guest']);positive=check(b,state['guest'],state['payload'],state['gfx32'])
    print('Current complete native guard body/shadow positive PASS',flush=True)
    faults=current.prior.shadow_faults(dict(b,report=dict(report,sourceBoundBodyShadowSemantics=positive)),
        state['guest'],state['payload'],state['gfx32'],check)
    extra=[]
    for label,tag,key,value in (
        ('native_post_proxy','MK2_HPHASE_POST_FIELD','id','1'),
        ('native_post_pose','MK2_HPHASE_POST_FIELD','pose','00000000'),
        ('native_post_floor','MK2_HPHASE_POST_FIELD','floor','81'),
        ('native_entry_opcode','MK2_HPHASE_CPU_NATIVE_ENTRY','opcode','FFFF')):
        changed=dict(b,rows=copy.copy(rows));changed['rows'][tag]=copy.deepcopy(rows[tag])
        need(changed['rows'][tag][0][key]!=value,'Actual non-no-op corruption '+label)
        changed['rows'][tag][0][key]=value
        try:check(changed,state['guest'],state['payload'],state['gfx32'])
        except(ValueError,AssertionError)as error:extra.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native post/entry corruption admitted '+label)
        print('Current guard body/shadow fault rejected: '+label,flush=True)
    need(len(faults)==11 and len(extra)==4 and
         check(b,state['guest'],state['payload'],state['gfx32'])==positive,
         'All15 original/additive faults and exact whole positive restored')
    pins=dict(report['inputHashes'])
    for p in(Path(__file__),Path(body.__file__),Path(model.__file__),
             *(p for p in folder.rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All executed native/model/source bytes unchanged')
    OUT.mkdir();value=dict(passed=True,candidate=report['candidate'],goalStatus='active',
        originalNativePID=held['process'].pid,actualNativeIdentity=held['identity'],
        wholeOriginalBodyROMShadowCase=positive,originalBodyShadowFaultsRejected=faults,
        additionalNativePostEntryFaultsRejected=extra,exactCurrentMemoryProofs=report['proofs'],
        inputHashes=pins,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,
        publicPlayableChanged=False,blockedKnifeAccepted=False,fullArtAudioAcceptance=False,
        allCPUContextsArenasAccepted=False,fullPortAcceptance=False)
    current.prior.save(OUT/'report.json',value)
    print('PASS full current guard body/shadow/KO-reset drawing, 15 faults; no knife/PCM/full-port claim',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve exact independent native qualifier failure')
        OUT.mkdir();current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False,goalStatus='active'))
        raise
