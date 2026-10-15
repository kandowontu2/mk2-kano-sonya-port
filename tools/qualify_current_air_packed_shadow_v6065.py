"""Whole air/body/clip/source/shadow proof, including original packed flip borrow.

Native shadow ADDXY width then scalar DEC can borrow into Y at X==0. The
previous width-minus-one geometric expression lost that borrow. Independently
execute the actual packed instructions; do not fit or discard any DMA row.
"""
import inspect,json,struct,traceback
from pathlib import Path
import qualify_current_air_native_clip_v6061 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6066_current_air_packed_shadow_checked'

def addxy(a,b):return ((a+b)&65535)|((((a>>16)+(b>>16))&65535)<<16)

def native_shadow_position(p,b4,b2,a5):
 subxy=prior.earlier.contacts.earlier.physical.body.subxy
 descriptor=(p['dx']&65535)|((p['dy']&65535)<<16)
 a0=subxy(b4,descriptor)                     # FF8012E0 SUBXY descriptor,A0
 a13=(subxy(b2,a0)>>16)<<14                 # SUBXY; SRL16; SLL14
 a14=subxy(b2,a13)                          # FF801340 packed subtraction
 a0=(a0&65535)|(a14&0xffff0000)             # MOVY A14,A0
 if p['command']&16:
  a0=addxy(a0,p['width'])                   # FF801410 ADDXY width,A0
  a0=(a0-1)&0xffffffff                     # FF801420 scalar DEC, retains Y borrow
 a0=addxy(a0,a5)                            # original native display-base ADDXY
 return a0&1023,(a0>>16)&511

def bindings():
 original=prior.bindings();source=inspect.getsource(prior.earlier.contacts.earlier.physical.body.check)
 first=source.index('  gap=(short(b2>>16)');last=source.index('  dkey=',first)
 geometry=source[first:last]
 # Obtain the actual full generated source without misleading original-file
 # inspect results: use the same6051 adapter function's whole source string.
 adapter=inspect.getsource(prior.earlier.bindings)
 before=" return scope['check']"
 need(adapter.count(before)==1,'Exact generated whole native body/shadow source returned')
 adapter=adapter.replace(before," scope['check'].source=source\n return scope['check']",1)
 scope=dict(prior.earlier.bindings.__globals__,state_gate=prior.prior.state_gate)
 exec(compile(adapter,__file__+'::entire_native_body_shadow_source_adapter','exec'),scope)
 generated=scope['bindings']();source=generated.source
 need(source.count(geometry)==1,'Only native packed-shadow coordinate expression changes')
 source=source.replace(geometry,'  x,y=native_shadow_position(p,b4,b2,a5)\n',1)
 scope=dict(generated.__globals__,native_shadow_position=native_shadow_position,
            check_body=original.__globals__['check_body'])
 exec(compile(source,__file__+'::whole_body_clip_fifo_native_shadow_packed_projection_every_row','exec'),scope)
 return scope['check']

def qualify_packed_source():
 guest=prior.earlier.current.expected();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 lo,hi=0xff8012b0,0xff801590
 need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],
      'Entire actual original packed projection/flip/display-base source instructions byte-exact')
 words={0xff8012e0:0xe3a0,0xff801300:0xe20d,0xff801310:0x2e0d,0xff801320:0x25cd,
        0xff801340:0xe3ae,0xff801350:0xefc0,0xff801410:0xe160,0xff801420:0x1420}
 need(all(struct.unpack_from('<H',guest,(at-0xff800000)//8)[0]==op for at,op in words.items()),
      'Exact actual original packed SUBXY/SRL/SLL/MOVY/ADDXY/scalar DEC instruction opcodes')
 cpu=prior.CPU;text=cpu.read_text();start=text.index('#define ADD_XY(R)');end=text.index('void tms340x0_device::add_xy_a',start)
 need('b->x += a.x;'in text[start:end]and 'b->y += a.y;'in text[start:end],
      'Original packed add treats X/Y independently before scalar decrement')
 p=dict(dx=79,dy=-95,width=65,command=0x6a90)
 need(native_shadow_position(p,0x0063000e,0x00f00000,0x01000038)==(55,484),
      'Independent actual source-instruction result retains full scalar Y borrow, not observed-row fitting')
 need(addxy(0x00e50000,0x00000041)==0x00e50041 and (addxy(0x00e5ffbf,65)-1)&0xffffffff==0x00e4ffff,
      'Independent packed carry/borrow edge arithmetic')
 return dict(passed=True,originalOpcodeWords={f'{at:08X}':f'{op:04X}'for at,op in words.items()},
             scalarFlipBorrowIntoYAccepted=True,inputHashes={str(cpu):sha(cpu)})

def run():
 failed=prior.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Every actual native floor-shadow copy has exact projected geometry'in failure['error'],
      'Actual complete14-row original packed-coordinate counterexample retained')
 source=qualify_packed_source()
 scope=dict(prior.run.__globals__,OUT=OUT,__file__=__file__,bindings=bindings)
 exec(compile(inspect.getsource(prior.run),__file__+'::whole_air_body_clip_shadow_matrix_and_edge_fault','exec'),scope)
 report=scope['run']();report['inputHashes'].update(source['inputHashes'])
 for p in(failed,Path(prior.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(originalPackedShadowSourceQualification=source,originalPackedFlipYBorrowAccepted=True,
               retainedPackedCoordinateAssumptionFailure=str(failed))
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete native packed-shadow qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases','actualExactZeroEdgePublications','originalNativeClipSourceQualification','originalPackedShadowSourceQualification')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
