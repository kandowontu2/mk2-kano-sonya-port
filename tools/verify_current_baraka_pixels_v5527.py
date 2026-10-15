"""Whole5523 pixel/ownership gate; native gore allocation bank0400 or0500.

The preserved actual Baraka run uses bank0505 for original fourteen-byte gore
sprites. Cage used0404. Require each full native descriptor and every source
palette pen exactly, rather than treating the palette allocation as static.
No dropped pixels, tolerances, injected allocation or gameplay changes.
"""
import inspect,json,struct
from pathlib import Path
import verify_current_baraka_pixels_v5523 as original

ROOT,need,sha=original.ROOT,original.need,original.sha
FAILURE=ROOT/'audit_v5525_current_baraka_pixels_progress/progress.json'
failure=json.loads(FAILURE.read_text())
need(not failure['passed']and failure['error']=="ValueError('Other legitimate occluder is true original Baraka, never substituted victim art')"and
     not failure['completedCases'],'Preserve actual native physical pass and unknown allocated gore palette counterexample')
source=inspect.getsource(original.verify_pixels)
edits={
 "d['palette']in(0x1c00,0x0400)":"d['palette']in(0x1c00,0x0400,0x0500)",
 "(0x1c1c if d['palette']==0x1c00 else 0x0404)":"(d['palette']|(d['palette']>>8))",
 "struct.unpack('<32768I',colors)[0x401:0x40f]":"struct.unpack('<32768I',colors)[d['palette']+1:d['palette']+15]",
}
for before,after in edits.items():
    need(source.count(before)==1,'Only exact native palette allocation, same full descriptor/color/owner/scanout gates')
    source=source.replace(before,after,1)
scope=dict(original.__dict__)
exec(compile(source,__file__+'.entire5523_exact_original_gore_colors_in_actual_allocated_bank','exec'),scope)
verified=scope['verify_pixels']
BASE=ROOT/'audit_v5528_current_baraka_pixels_ram'
OUT=ROOT/'audit_v5529_current_baraka_pixels_progress'
original.BASE=BASE;original.OUT=OUT
original.capture.__globals__.update(BASE=BASE,verify_pixels=verified)
run_source=inspect.getsource(original.run)
before='for p in(Path(__file__),Path(model.__file__)'
after="for p in(FAILURE,Path(original.__file__),ROOT/'tools/inspect_current_baraka_foreground_v5526.py',Path(__file__),Path(model.__file__)"
need(run_source.count(before)==1,'Entire native four-case matrix, pin corrected native allocation and executed failure')
run_source=run_source.replace(before,after,1)
run_scope=dict(original.__dict__,__file__=__file__,original=original,FAILURE=FAILURE)
exec(compile(run_source,__file__+'.entire5523_four_case_native_matrix_with_exact_allocated_gore_palette','exec'),run_scope)
run=run_scope['run']


def preflight():
    guest=original.model.current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    log=(ROOT/'audit_v5524_current_baraka_pixels_ram/kano_p1/run.log').read_text()
    total=0
    for d in original.rows(log,'DMA'):
        if d['palette']!=0x500 or d['command']&15!=2:continue
        need(d['queue_match']==1 and d['queue_frame']==d['frame']and d['id']==d['pose']==d['body']==0 and d['bank']==0x0505 and
             d['pc']==0xff804640 and 0xff800000<=d['cache']<=0xfffffff0 and d['cache']%8==0,
             'Every actually allocated native gore object has exact FIFO/type/bank/cache/consumer')
        at=(d['cache']-0xff800000)//8;w,h,dx,dy,s,c=struct.unpack_from('<HHhhIH',guest,at)
        need(guest[at:at+14]==stock[at:at+14]and(w,h,s)==(d['width'],d['height'],d['source'])and
             ((c&~0x30)|(d['command']&0x30)|0x8002)==d['command'],
             'Every complete original native allocated gore descriptor and hardware format/flip/dimension exact')
        total+=1
    need(total>100,'Complete actual original native allocated-gore command family, not one selected part')
    return total


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual native Baraka gore-allocation checkpoint')
    try:
        total=preflight();print(f'{total} actual native allocated gore commands descriptor/FIFO/source exact',flush=True)
        report=run();report['preservedActualNativeAllocatedGorePreflightCommands']=total
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=original.traceback.format_exc(),completedCases=original.COMPLETED,goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();original.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentSourceArtReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
