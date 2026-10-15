"""Whole native air matrix with original inclusive clipping-edge semantics.

Original ADDXY/SUBXY sets separate equality/ordering flags. JRC/JRV reject
strictly negative lower extents; JRHI/JRGE reject strictly beyond upper bounds.
An exact zero edge is still queued, though the DMA itself can draw no pixels.
Retain the failed geometric-area assertion; change only its source-derived
predicate. Every candidate/queue/pose/flip/display/shadow/source row remains.
"""
import copy,inspect,json,struct,subprocess,traceback
from pathlib import Path
import qualify_current_air_cooperative_handoff_v6059 as prior
import qualify_current_air_throw_roles_v6051 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
OUT=ROOT/'audit_v6062_current_air_native_clip_checked'
CPU=ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'

def native_visible(x,y,w,height):
 # Independent emulation of exact original packed-XY flag decisions. No
 # fitting to published rows, no discard of clipping/boundary candidates.
 short=earlier.contacts.earlier.physical.body.short
 extent_x,extent_y=short((x+w)&65535),short((y+height)&65535)
 lower_c,lower_v=0>extent_y,0>extent_x
 upper_c,upper_z=254>y,254==y
 upper_n,upper_v=400==x,400>x
 return not(lower_c or lower_v or(not upper_c and not upper_z)or
            (upper_n and upper_v)or(not upper_n and not upper_v))

def bindings():
 body=earlier.contacts.earlier.physical.body;source=inspect.getsource(body.check_body)
 before='shown=x+w>0 and y+h>0 and x<400 and y<254'
 need(source.count(before)==1,'Only original native packed-XY clipping predicate changes')
 source=source.replace(before,'shown=native_visible(x,y,w,h)',1)
 scope=dict(body.check_body.__globals__,native_visible=native_visible)
 exec(compile(source,__file__+'::whole_candidate_fifo_pose_flip_display_native_clip','exec'),scope)
 native_body=scope['check_body'];check=prior.bindings()
 scope=dict(check.__globals__,check_body=native_body)
 # The generated whole kernel's original source comes from6051.bindings;
 # compile it through the same explicit adapters, then replace only the
 # function referenced by its body gate, not source/row/projection checks.
 check.__globals__['check_body']=native_body
 return check

def qualify_clip_source():
 guest=earlier.current.expected();stockpath=ROOT/'mk2/mk2-maincpu.bin';original=stockpath.read_bytes()
 lo,hi=0xff8042a0,0xff804340
 need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],
      'Every original native geometry/flag/branch instruction byte-exact')
 words={0xff8042b0:0xe122,0xff8042c0:0xe3c2,0xff8042d0:0xc829,0xff8042e0:0xcc28,
        0xff804310:0xe3a2,0xff804320:0xc324,0xff804330:0xc523}
 need(all(struct.unpack_from('<H',guest,(at-0xff800000)//8)[0]==op for at,op in words.items()),
      'Original ADDXY/SUBXY/lower JRC-JRV/upper JRHI-JRGE exact original opcodes')
 text=CPU.read_text()
 need(all(t in text for t in('SET_N_LOG(a.x == b->x);','SET_C_LOG(a.y > b->y);','SET_Z_LOG(a.y == b->y);',
      'SET_V_LOG(a.x > b->x);','j_xx_8(!C_FLAG() && !Z_FLAG());',
      'j_xx_8((N_FLAG() && V_FLAG()) || (!N_FLAG() && !V_FLAG()));')),
      'Actual local TMS packed-XY comparison and branch semantics, no geometric area assumption')
 need(native_visible(-65,194,65,54)and not native_visible(-66,194,65,54)and native_visible(400,254,1,1)and
      not native_visible(401,254,1,1)and not native_visible(400,255,1,1),
      'Independent exact lower/upper edge and one-unit-outside branch tests')
 exe=ROOT/'mame-mkp/unidasm.exe'
 result=subprocess.run([str(exe),str(stockpath),'-arch','tms34010','-skip',hex((lo-0xff800000)//8),
   '-count',str(hi-lo),'-basepc',hex(lo)],capture_output=True,text=True)
 need(result.returncode==0 and not result.stderr and len(result.stdout)<4000 and
      all(f'{at:08x}: {op:04x}'in result.stdout for at,op in words.items()),'Actual bounded original clipping disassembly')
 return dict(passed=True,originalOpcodes={f'{at:08X}':f'{op:04X}'for at,op in words.items()},
             originalDisassembly=result.stdout,inputHashes={str(p):sha(p)for p in(CPU,exe,stockpath)})

def run():
 failed=prior.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Every actual complete body part published iff on screen'in failure['error'],
      'Actual native exact-zero-edge counterexample retained without source/evidence rewrite')
 clip=qualify_clip_source()
 scope=dict(prior.run.__globals__,OUT=OUT,__file__=__file__,bindings=bindings)
 exec(compile(inspect.getsource(prior.run),__file__+'::entire_current_air_matrix_native_clip','exec'),scope)
 report=scope['run']();report['originalNativeClipSourceQualification']=clip
 report['inputHashes'].update(clip['inputHashes'])
 edges=[]
 for fighter,side,victim in earlier.MATRIX:
  b=earlier.load(fighter,side,victim);body=earlier.contacts.earlier.physical.body
  for r in b['rows']['MK2_HPHASE_CANDIDATE']:
   x,y=body.short(body.num(r,'xy')),body.short(body.num(r,'xy')>>16)
   w,height=body.num(r,'size')&65535,body.num(r,'size')>>16
   if x+w==0 or y+height==0:
    key=tuple(body.num(r,k)for k in('frame','slot','part'))
    published=[q for q in b['rows']['MK2_HPHASE_QUEUE']if tuple(body.num(q,k)for k in('frame','slot','part'))==key]
    need(len(published)==1 and native_visible(x,y,w,height),'Actual complete native exact-zero-edge queue publication')
    changed=copy.deepcopy(b);changed['rows']['MK2_HPHASE_QUEUE']=[q for q in changed['rows']['MK2_HPHASE_QUEUE']if tuple(body.num(q,k)for k in('frame','slot','part'))!=key]
    guest=earlier.current.expected();payload=(ROOT/earlier.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    # Exact body check uses no GFX or fitted row addresses. Both actor owners
    # and IDs come from actual complete fields, already separately qualified.
    fields=b['rows']['MK2_HPHASE_POST_FIELD'];frames={body.num(t,'frame')for t in fields};first=min(frames)
    owners={s:(body.num(next(t for t in fields if body.num(t,'frame')==first and body.num(t,'slot')==s),'actor'),
               body.num(next(t for t in fields if body.num(t,'frame')==first and body.num(t,'slot')==s),'main'))for s in(1,2)}
    check_body=bindings().__globals__['check_body'];ids={side:17 if fighter=='kano'else 18,3-side:earlier.VID[victim]}
    try:check_body(changed,guest,payload,frames,owners,ids)
    except ValueError as error:report['actualSemanticFaultsRejected'].append(dict(fighter=fighter,side=side,victim=victim,fault='missing_exact_zero_edge_queue',rejectedBy=str(error)))
    else:raise ValueError('Missing true native zero-edge queue was accepted')
    edges.append(dict(fighter=fighter,side=side,victim=victim,key=key,x=x,y=y,width=w,height=height,actualCandidate=r,actualQueue=published[0]))
 need(len(edges)==1,'One actual original zero-edge publication retained, not clipped away to pass')
 for p in(failed,Path(prior.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Whole accepted/failed/native/source evidence stable after edge fault')
 report.update(retainedWrongGeometricAreaAssumptionFailure=str(failed),actualExactZeroEdgePublications=edges,
               everyOriginalNativeClipBoundaryAccepted=True)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete native airborne clipping qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases','actualExactZeroEdgePublications','originalNativeClipSourceQualification')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
