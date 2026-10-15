"""Retain every field; honor the original native multipart body-skip branch.

The body is drawn before the captured native flag store on3028. Its later
shadow eligibility call sees the new flag. Independent pre-fields, actual
instruction/flag-store records and original branch code bind that ordering.
This is finite main-actor geometry, not acceptance of replacement corpse art.
"""
import inspect
import struct
from pathlib import Path
import qualify_native_selector_opposite_roles_throw_floor_geometry_words as parent

ROOT=parent.ROOT
body=parent.scope['body']
need=parent.scope['need']
current=parent.scope['current']
BODY_FAILURE=parent.OUT/'failure.json'


def hidden_gate(b,guest,frames):
    model=parent.scope['template'].scope['model']
    rows=model.knife.R.rows(b['cpuLog'],'FIELD')
    pre={(r['frame'],r['slot']):r for r in rows}
    expected={(f,s) for f in frames for s in (1,2) if pre[f,s]['body']&0x22!=0x22}
    skipped={(f,s) for f in frames for s in (1,2)}-expected
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for start,stop in ((0xff804000,0xff8045d0),(0xff838f60,0xff839090)):
        lo,hi=(start-0xff800000)//8,(stop-0xff800000)//8
        need(guest[lo:hi]==stock[lo:hi],'Whole original body flag loading/skip/next-object and hide/unhide code')
    lo=(0xff804160-0xff800000)//8
    need(guest[lo:lo+10]==struct.pack('<5H',0x5663,0x1FC7,0xCA11,0x1F47,0xCB3F),
         'Original multipart bit1/skip bit5 jumps directly to next object')
    lo=(0xff838f60-0xff800000)//8
    need(guest[lo:lo+18]==struct.pack('<9H',0xB404,0x0160,0x0BA4,0x0020,0,0x0B84,0x0010,0,0xC008),
         'Original hide branch sets32/clears16 before common actor body store')
    flags=parent.scope['checkpoint'].rows(b['cpuLog'],'MK2_CPU_PAIR_FLAG')
    stores=[r for r in flags if r['kind']=='body' and r['slot']=='1' and r['after']=='0026']
    need(len(stores)==1,'One actually captured native Sonya multipart suppression store')
    r=stores[0];f=int(r['frame']);actor=int(r['actor'],16)
    need(f==3028 and r['pc']=='FF839090' and r['op0']=='B080' and r['op1']=='0160' and
         int(r['at'],16)==actor+0x160 and int(r['a0'],16)==actor==pre[f,1]['actor'] and
         r['id']=='18' and r['before']=='0016' and pre[f,1]['body']==0x16 and
         pre[f+1,1]['body']==0x26 and int(r['after'],16)==(int(r['before'],16)|32)&~16 and
         r['writes']=='0' and r['assistance']=='none',
         'Actual original actor-targeted hide operation and next independent pre-field')
    need(len(skipped)==69 and skipped=={(q,1) for q in range(f+1,max(frames)+1)},
         'Every exact independent source-defined skipped body field; no omitted observation gaps')
    text=b['cpuLog'];lines=text.splitlines()
    candidates=b['rows']['MK2_HPHASE_CANDIDATE']
    for t in candidates:
        key=(int(t['frame']),int(t['slot']))
        need(key in expected and int(t['body'],16)==pre[key]['body'],
             'Every actual native body candidate binds independent pre-draw flags and eligibility')
    positions={}
    for i,line in enumerate(lines):
        if f'frame={f} ' not in line or 'slot=1 ' not in line:continue
        if line.startswith('MK2_HPHASE_CANDIDATE '):positions.setdefault('body',i)
        if line.startswith('MK2_CPU_PAIR_FLAG ') and 'kind=body ' in line:positions['store']=i
        if line.startswith('MK2_HPHASE_SHADOW_BEGIN '):positions['shadow']=i
    need(set(positions)=={'body','store','shadow'} and positions['body']<positions['store']<positions['shadow'],
         'Actual same-frame body then native store then shadow ordering, no fabricated timing exception')
    return dict(passed=True,expectedBodyKeys=sorted(expected),sourceDefinedSkippedBodyKeys=sorted(skipped),
        actualNativeBodyFlagStore=r,actualSameFrameRecordOrder=positions,
        actualBodyCandidatePreFlagsChecked=len(candidates),replacementCorpseArtAccepted=False)


def native_check_body(b,guest,payload,frames,owners,ids):
    proof=hidden_gate(b,guest,frames)
    expected_body_keys={tuple(k) for k in proof['expectedBodyKeys']}
    source=inspect.getsource(body.check_body)
    source=current.replace(source,'set(compositions)=={(f,s)for f in frames for s in(1,2)}',
        'set(compositions)==expected_body_keys')
    scope=dict(vars(body),expected_body_keys=expected_body_keys)
    exec(compile(source,__file__+'::whole_original_body_with_native_eligibility','exec'),scope)
    return scope['check_body'](b,guest,payload,frames,owners,ids)


source=parent.source
source=current.replace(source,
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_geometry_words_checked'",
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_hidden_body_checked'")
source=current.replace(source,
    'scope=dict(template.scope,checkpoint=checkpoint,floor_gate=floor_gate,__file__=__file__)',
    "body_proxy=type('OriginalBodyScope',(),dict(vars(body),check_body=staticmethod(native_check_body)))()\n    scope=dict(template.scope,body=body_proxy,checkpoint=checkpoint,floor_gate=floor_gate,__file__=__file__)")
source=current.replace(source,
    'for path in (Path(__file__),SOURCE,IMPORT_FAILURE,PARENT,FAILURE,Path(rejected.__file__),Path(template.__file__),',
    'for path in (Path(__file__),Path(parent.__file__),SOURCE,IMPORT_FAILURE,BODY_FAILURE,PARENT,FAILURE,Path(rejected.__file__),Path(template.__file__),')
source=current.replace(source,
    'value=dict(passed=True,actualNativeIdentity=held[\'identity\'],wholeNativeBodyROMShadowCase=positive,',
    "suppression=hidden_gate(b,state['guest'],set(positive['state']['expectedNativeDrawingFrames']))\n    value=dict(passed=True,actualNativeIdentity=held['identity'],wholeNativeBodyROMShadowCase=positive,sourceBoundNativeBodySuppression=suppression,")
scope=dict(__file__=__file__,struct=struct,SOURCE=parent.SOURCE,IMPORT_FAILURE=parent.IMPORT_FAILURE,
    BODY_FAILURE=BODY_FAILURE,parent=parent,native_check_body=native_check_body,hidden_gate=hidden_gate)
exec(compile(source,__file__+'::whole_native_geometry_with_source_bound_eligibility','exec'),scope)
OUT=scope['OUT']
execute=scope['execute']
safe_execute=scope['safe_execute']
