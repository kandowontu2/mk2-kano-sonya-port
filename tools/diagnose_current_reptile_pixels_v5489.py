"""Actual current first Reptile victim mismatch; RAM-only visual diagnosis.

Keep the strict failed pixel gate, do not run the remaining matrix after its
first failure. Show actual native frame and source-template preview with exact
DMA/palette/VRAM metadata. No accepted gameplay substitute or game mutation.
"""
import inspect, json, traceback
from pathlib import Path
import current_reptile_victims_ram_v5483 as original_run

ROOT,need,sha=original_run.ROOT,original_run.need,original_run.sha
BASE=ROOT/'audit_v5490_current_reptile_pixel_diagnostic_ram'
OUT=ROOT/'audit_v5491_current_reptile_pixel_diagnostic_progress'
LUA=original_run.LUA
FAILED=ROOT/'audit_v5488_current_reptile_victims_progress/progress.json'


def diagnostic_native_pixel_source():
    source=inspect.getsource(original_run.previous.native_pixels)
    before="(int(d['palette'],16)+indices)&0x7fff"
    need(source.count(before)==1,'One native palette-bank intermediate integer width')
    source=source.replace(before,"(int(d['palette'],16)+indices.astype(np.uint32))&0x7fff")
    before="""        need(int(np.count_nonzero(visible))>100 and np.array_equal(image[y:y+h,x:x+w][visible],expected[visible]),
             'Every actual owned headless-body opaque pixel matches independent source art and actual hardware palette at native DMA/scanout origin')"""
    after="""        crop=image[y:y+h,x:x+w]
        matched=np.all(crop==expected,axis=2)&visible
        good=int(np.count_nonzero(visible))>100 and np.array_equal(crop[visible],expected[visible])
        if not good:
            import base64
            from io import BytesIO
            from PIL import Image
            actual_words=np.frombuffer(raw,'<u2').reshape(512,512)[scanout['row']+y:scanout['row']+y+h,scanout['column']+x:scanout['column']+x+w]&0x7fff
            summary=dict(age=int(meta['age']),frame=int(meta['frame']),dma=d,asset=asset,scanout=scanout,origin=[x,y],
                originalOpaquePixels=int(visible.sum()),matchingOpaquePixels=int(matched.sum()),
                actualCropPaletteBanks=sorted(set((actual_words[visible]>>8).tolist())),
                actualPixelExamples=crop[visible][:12].tolist(),expectedPixelExamples=expected[visible][:12].tolist())
            print('MK2_CURRENT_REPTILE_PIXEL_DIAGNOSTIC '+json.dumps(summary),flush=True)
            for label,picture in ((fighter+'_actual_native',image),(fighter+'_source_template',expected)):
                encoded=BytesIO();Image.fromarray(picture).save(encoded,format='JPEG',quality=80)
                print('MK2_CURRENT_REPTILE_VISUAL_PREVIEW '+label+' '+base64.b64encode(encoded.getvalue()).decode(),flush=True)
        need(good,'Every actual owned headless-body opaque pixel matches independent source art and actual hardware palette at native DMA/scanout origin')"""
    need(source.count(before)==1,'One actual strict original body-pixel failure boundary, no tolerance adjustment')
    source=source.replace(before,after)
    return source


def run():
    failed=json.loads(FAILED.read_text())
    need(not failed['passed']and failed['error']=="ValueError('Every actual owned headless-body opaque pixel matches independent source art and actual hardware palette at native DMA/scanout origin')",
         'Preserved exact actual current display-pixel mismatch; no broad acceptance')
    source=inspect.getsource(original_run.run)
    before='source=inspect.getsource(previous.native_pixels)'
    need(source.count(before)==1,'Whole original current run with diagnostic source-only pixel reporting')
    source=source.replace(before,'source=diagnostic_native_pixel_source()')
    scope=dict(original_run.__dict__)
    scope.update(BASE=BASE,OUT=OUT,LUA=LUA,__file__=str(Path(__file__).resolve()),diagnostic_native_pixel_source=diagnostic_native_pixel_source)
    exec(compile(source,__file__+'.whole5483_actual_first_pixel_mismatch_diagnostic','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual current pixel diagnostic checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();original_run.previous.canonical5467.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','independentSourcePNGNativeReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
