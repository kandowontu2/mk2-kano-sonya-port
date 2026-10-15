"""Preserve all5509 gates; compare stock commands after native copy dispatch.

Actual original Cage picture descriptors store format/flips, while the
native FIFO/hardware command adds 0x8002 (busy + transparent source-copy).
Do not compare a descriptor format word directly to an executing command.
The preserved first native capture terminal0 passed the original physical
contract and15 faults, then failed this overstrict command comparison.
"""
import inspect,json
from pathlib import Path
import verify_current_cage_sections_v5509 as original

failure=original.ROOT/'audit_v5511_current_cage_sections_progress/progress.json'
f=json.loads(failure.read_text())
original.need(not f['passed']and f['error']=="ValueError('Actual stock Cage component belongs to original ROM native pose')"and
              not f['completedCases'],'Preserve actual original physical pass / descriptor-dispatch comparison failure')
source=inspect.getsource(original.verify_pixels)
before="(p['graphic'],p['width'],p['height'],p['command'])==\n                             (d['source'],d['width'],d['height'],d['command']&0x7fff)"
after="(p['graphic'],p['width'],p['height'],p['command']|0x8002)==\n                             (d['source'],d['width'],d['height'],d['command'])"
original.need(source.count(before)==1,'Only exact native format-to-dispatch transformation, no ownership/raster tolerance changes')
source=source.replace(before,after,1)
scope=dict(original.__dict__)
exec(compile(source,__file__+'.whole5509_exact_native_stock_descriptor_dispatch_command','exec'),scope)
original.verify_pixels=scope['verify_pixels']
original.BASE=original.ROOT/'audit_v5513_current_cage_sections_ram'
original.OUT=original.ROOT/'audit_v5514_current_cage_sections_progress'


def preflight():
    # Revalidate every observed Cage component in the preserved actual run,
    # not just the one that caused the first useful counterexample.
    guest=original.model.current.expected()
    log=(original.ROOT/'audit_v5510_current_cage_sections_ram/kano_p1/run.log').read_text()
    rows=original.rows(log,'DMA');total=0
    for d in rows:
        if d['id']!=2 or d['pc']!=0xff804640 or d['source']>=0x0a000000:continue
        parts=original.graphics.native_group(dict(pose=f"{d['pose']:08X}",facing=f"{d['command']&0x30:08X}"),b'',guest)
        original.need(any((p['graphic'],p['width'],p['height'],p['command']|0x8002)==
                          (d['source'],d['width'],d['height'],d['command'])for p in parts),
                      'Every actual original Cage descriptor transforms to exact observed native dispatch')
        total+=1
    original.need(total>100,'Entire observed original native Cage foreground, not one hand-picked part')
    return total


run_source=inspect.getsource(original.run)
before='for p in(LUA,Path(__file__),Path(model.__file__)'
after='for p in(failure,Path(original.__file__),LUA,Path(__file__),Path(model.__file__)'
original.need(run_source.count(before)==1,'Preserve complete native matrix; pin corrected verifier and preserved failure')
run_source=run_source.replace(before,after,1)
run_scope=dict(original.__dict__,__file__=__file__,original=original,failure=failure)
exec(compile(run_source,__file__+'.whole5509_four_case_matrix_corrected_native_stock_dispatch','exec'),run_scope)
run=run_scope['run']


if __name__=='__main__':
    original.need(not original.OUT.exists(),'Fresh immutable native section command correction checkpoint')
    try:
        total=preflight();print(f'{total} preserved actual native Cage component commands source-exact after original copy-mode dispatch',flush=True)
        report=run();report['preservedOriginalNativeCageDescriptorDispatchCommands']=total
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=original.traceback.format_exc(),completedCases=original.COMPLETED,
                    goalStatus='active',fullPortAcceptance=False)
    original.OUT.mkdir();original.save(original.OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentSourceArtReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
