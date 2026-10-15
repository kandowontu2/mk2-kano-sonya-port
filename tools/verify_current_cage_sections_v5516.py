"""Complete5509 native section model plus typed original stock gore objects.

The actual Cage capture identifies palette0400, id0, pose0 single-image native
gore objects (14-byte offset descriptors), unlike Reptile's compact10-byte
palette1c00 blood objects. Every source/shape/format/color stays exact. Retain
all physical, six-phase, floor, ownership, command-order and pixel gates.
"""
import inspect,json,re,struct
from pathlib import Path
import verify_current_cage_sections_v5509 as original

ROOT,need,sha=original.ROOT,original.need,original.sha
FAILURES=[ROOT/'audit_v5511_current_cage_sections_progress/progress.json',ROOT/'audit_v5514_current_cage_sections_progress/progress.json']
for p,message in zip(FAILURES,("ValueError('Actual stock Cage component belongs to original ROM native pose')",
                              "ValueError('Other occluder is actual original Cage, never a foreign substituted body')")):
    f=json.loads(p.read_text());need(not f['passed']and f['error']==message and not f['completedCases'],'Preserved actual bounded native-owner model failure')
source=inspect.getsource(original.verify_pixels)
edits={
 "(p['graphic'],p['width'],p['height'],p['command'])==\n                             (d['source'],d['width'],d['height'],d['command']&0x7fff)":
 "(p['graphic'],p['width'],p['height'],p['command']|0x8002)==\n                             (d['source'],d['width'],d['height'],d['command'])",
 "                else:\n                    need(d['id']==2 and d['actor']==int(action['actor'],16)and d['source']<0x0a000000,":
 """                elif d['palette']==0x0400:
                    need(d['id']==0 and d['pose']==0 and d['body']==0 and d['bank']==0x0404 and
                         d['actor']not in {t['actor']for t in targets}and d['actor']!=int(action['actor'],16)and
                         0xff800000<=d['cache']<=0xfffffff0 and d['cache']%8==0 and d['source']<0x0a000000,
                         'Every native Cage gore occluder has exact original single-image object type/bank/cache/source')
                    at=(d['cache']-0xff800000)//8
                    w,h,dx,dy,s,c=struct.unpack_from('<HHhhIH',guest,at)
                    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
                    need(guest[at:at+14]==stock[at:at+14]and (w,h,s)==(d['width'],d['height'],d['source'])and
                         ((c&~0x30)|(d['command']&0x30)|0x8002)==d['command'],
                         'Original fourteen-byte offset gore descriptor exactly binds all format/flip/source/dimension words')
                    pal_at=(0xffaf2a40-0xff800000)//8
                    need(guest[pal_at:pal_at+32]==stock[pal_at:pal_at+32]and struct.unpack_from('<H',stock,pal_at)[0]==15,
                         'Entire immutable original15-pen native gore palette')
                    native_words=struct.unpack_from('<15H',stock,pal_at+2)
                    native_colors=[((((v>>10&31)<<3)|(v>>12&7))<<16)|((((v>>5&31)<<3)|(v>>7&7))<<8)|
                                   (((v&31)<<3)|(v>>2&7))for v in native_words]
                    actual_colors=struct.unpack('<32768I',colors)
                    need(list(actual_colors[0x401:0x40f])==native_colors[1:],
                         'All actual native gore RGB pens exactly equal the original stock palette, no ignored colors')
                    owner_kind='source-ROM Cage gore'
                else:
                    need(d['id']==2 and d['actor']==int(action['actor'],16)and d['source']<0x0a000000,""",
}
for before,after in edits.items():
    need(source.count(before)==1,'Exact typed native original gore/stock dispatch model extension')
    source=source.replace(before,after,1)
scope=dict(original.__dict__)
exec(compile(source,__file__+'.entire5509_source_owner_and_raster_contract_with_typed_native_gore','exec'),scope)
verified=scope['verify_pixels']


def verify_pixels(log,images,buffers,gfx_streams,source_image,reference,fighter,guest):
    positive=verified(log,images,buffers,gfx_streams,source_image,reference,fighter,guest)
    actual=original.rows(log,'DMA');faults=[]
    kinds=set()
    for shot in positive['sections']:
        for serial,kind in shot['nativeOccluders'].items():
            if kind in kinds:continue
            kinds.add(kind)
            d=next(d for d in actual if d['serial']==serial)
            # Alter an actual occluding command in the full ledger and run
            # the entire ownership+pixel verifier again, not a toy predicate.
            line=next(line for line in log.splitlines()if line.startswith('MK2_CURRENT_CAGE_SCENE_DMA ')and
                      f" serial={serial} "in line)
            changed,n=re.subn(r' id=\d+ ',f" id={1 if d['id']!=1 else 0} ",line,count=1)
            need(n==1 and changed!=line,'Effective actual foreground-owner counterexample')
            corrupted=log.replace(line,changed,1)
            try:verified(corrupted,images,buffers,gfx_streams,source_image,reference,fighter,guest)
            except ValueError as error:faults.append(dict(label='actual '+kind+' identity corrupted',serial=serial,rejectedBy=str(error)))
            else:raise ValueError('Actual native foreground identity counterexample accepted: '+kind)
    restored=verified(log,images,buffers,gfx_streams,source_image,reference,fighter,guest)
    need(restored==positive,'Entire actual section positive restored after full native-owner counterexamples')
    positive['effectiveActualNativeForegroundOwnerFaults']=faults
    return positive


original.verify_pixels=verify_pixels
original.BASE=ROOT/'audit_v5517_current_cage_sections_ram'
original.OUT=ROOT/'audit_v5518_current_cage_sections_progress'
run_source=inspect.getsource(original.run)
before='for p in(LUA,Path(__file__),Path(model.__file__)'
after="for p in(*FAILURES,Path(original.__file__),ROOT/'tools/verify_current_cage_sections_v5512.py',ROOT/'tools/inspect_current_cage_foreground_v5515.py',LUA,Path(__file__),Path(model.__file__)"
need(run_source.count(before)==1,'Whole original four-case matrix plus immutable executed failures and typed native model')
run_source=run_source.replace(before,after,1)
run_scope=dict(original.__dict__,__file__=__file__,original=original,FAILURES=FAILURES)
exec(compile(run_source,__file__+'.whole5509_four_case_matrix_native_gore_ownership','exec'),run_scope)
run=run_scope['run']


def preflight():
    guest=original.model.current.expected()
    log=(ROOT/'audit_v5513_current_cage_sections_ram/kano_p1/run.log').read_text()
    commands=original.rows(log,'DMA');gore=0;cage=0
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for d in commands:
        if d['palette']==0x400:
            need(d['id']==d['body']==d['pose']==0 and d['bank']==0x404 and d['cache']>=0xff800000,'Actual original gore object type')
            at=(d['cache']-0xff800000)//8
            w,h,dx,dy,s,c=struct.unpack_from('<HHhhIH',guest,at)
            need(guest[at:at+14]==stock[at:at+14]and(w,h,s)==(d['width'],d['height'],d['source'])and
                 ((c&~0x30)|(d['command']&0x30)|0x8002)==d['command'],'All observed original gore descriptors exact')
            gore+=1
        if d['id']==2 and d['pc']==0xff804640 and d['source']<0x0a000000:
            parts=original.graphics.native_group(dict(pose=f"{d['pose']:08X}",facing=f"{d['command']&0x30:08X}"),b'',guest)
            need(any((p['graphic'],p['width'],p['height'],p['command']|0x8002)==(d['source'],d['width'],d['height'],d['command'])for p in parts),
                 'All observed Cage native pose components exact')
            cage+=1
    need(gore>100 and cage>100,'Complete observed native gore and Cage foreground, not one selected object')
    return dict(nativeGoreCommands=gore,nativeCageCommands=cage)


if __name__=='__main__':
    need(not original.OUT.exists(),'Fresh immutable typed native gore/section checkpoint')
    try:
        checked=preflight();print(json.dumps(checked),flush=True)
        report=run();report['preservedActualNativeForegroundPreflight']=checked
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=original.traceback.format_exc(),completedCases=original.COMPLETED,goalStatus='active',fullPortAcceptance=False)
    original.OUT.mkdir();original.save(original.OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentSourceArtReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
