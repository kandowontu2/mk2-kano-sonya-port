"""Actual current Reptile victim art, palette and full native scanout binding.

Preserve5479's completed first native run and incorrect negative-test field
target. Same original physical controller, new passive actual palette/VRAM
capture; every own body opaque pixel must match at the hardware-defined native
front-page DMA origin. No best-frame/position search or tolerance weakening.
"""
import inspect, json, re, struct, textwrap, traceback
from pathlib import Path
import numpy as np
import current_reptile_victims_ram_v5467 as canonical5467
import current_reptile_victims_ram_v5477 as current
import verify_native_floor_display_v602 as display

ROOT,need,sha=canonical5467.ROOT,canonical5467.need,canonical5467.sha
BASE=ROOT/'audit_v5481_current_reptile_victims_ram'
OUT=ROOT/'audit_v5482_current_reptile_victims_progress'
LUA=ROOT/'mk2ks_current_reptile_ram_v5480.lua'
FAILED=ROOT/'audit_v5479_current_reptile_victims_progress/progress.json'


def native_pixels(log,images,buffers,reference,actual_gfx,fighter):
    rows=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_DEATH_ART_V897_'+tag+' ')]
    dmas=rows('DMA')
    by_source={int(r['graphics'],16):r for r in reference['fighters'][fighter]['frames']}
    out=[]
    for filename,image in images.items():
        colors,meta=buffers[filename,'PALETTE']
        need(len(colors)==32768*4,'Whole actual hardware palette at every original snapshot')
        if int(meta['age'])not in(150,200,250):continue
        raw,vr=buffers[filename,'VRAM']
        need(meta==vr and meta['frame']==meta['flip_frame']and meta['pc']=='FF8168E0'and meta['mask']=='FFFF',
             'Exact actual original full-mask native scene flip/VRAM/palette association')
        scanout=display.check_latch(image,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16))
        # The actual display-start selects the front page. Select its latest
        # genuine body DMA, never search frames/positions for a better image.
        candidates=[r for r in dmas if int(r['frame'])<=int(meta['frame'])and
                    (int(r['y'])>>8)==(scanout['row']>>8)and r['fifo_actor']==r['fifo_physical']]
        need(candidates,'Actual front-page own body DMA exists')
        last=max(int(r['frame'])for r in candidates)
        candidates=[r for r in candidates if int(r['frame'])==last]
        need(len(candidates)==1 and 0<=int(meta['frame'])-last<=1,'One actual latest native front-page body dispatch, no chosen best field')
        d=candidates[0];asset=by_source[int(d['source'],16)]
        need(asset['kind']=='body'and d['queue_match']=='1','Exact actual owned body source and native FIFO')
        w,h=asset['size'];need((int(d['width']),int(d['height']))==(w,h),'Whole actual unscaled owned source geometry')
        at=int(d['source'],16)//8-0x1ec0000
        indices=np.frombuffer(canonical5467.assets.unpack(actual_gfx[at:at+(w*h*6+7)//8],w*h),np.uint8).reshape(h,w)
        command=int(d['command'],16)
        if command&16:indices=indices[:,::-1]
        if command&32:indices=indices[::-1]
        x=int(d['x'])-(w-1 if command&16 else 0)-scanout['column']
        y=int(d['y'])-(h-1 if command&32 else 0)-scanout['row']
        need(0<=x<=400-w and 0<=y<=254-h,'Actual complete owned body is visible at the source-defined native scanout origin')
        palette=np.frombuffer(colors,'<u4')
        words=palette[(int(d['palette'],16)+indices)&0x7fff]
        expected=np.stack((words>>16&255,words>>8&255,words&255),axis=2).astype(np.uint8)
        visible=indices!=0
        need(int(np.count_nonzero(visible))>100 and np.array_equal(image[y:y+h,x:x+w][visible],expected[visible]),
             'Every actual owned headless-body opaque pixel matches independent source art and actual hardware palette at native DMA/scanout origin')
        out.append(dict(filename=filename,age=int(meta['age']),**scanout,source=d['source'],bodyPose=asset['pose'],
          originalOpaquePixels=int(np.count_nonzero(visible)),displayOrigin=[x,y],nativeDMAFrame=last,
          nativePalette=d['palette'],allOriginalOpaqueBodyPixelsExact=True))
    need(len(out)==3,'All three full native scene and own-body pixel targets accepted')
    faults=[]
    first=out[0];filename=first['filename'];colors,meta=buffers[filename,'PALETTE'];raw,_=buffers[filename,'VRAM']
    def reject(label,fn):
        try:fn()
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Actual displayed pixel counterexample accepted: '+label)
    altered=images[filename].copy();altered[first['displayOrigin'][1],first['displayOrigin'][0],0]^=1
    reject('actual native displayed body-origin RGB pixel corrupted',lambda:display.check_latch(altered,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16)))
    index=int(np.frombuffer(raw,'<u2').reshape(512,512)[first['row'],first['column']])&0x7fff
    changed=bytearray(colors);struct.pack_into('<I',changed,index*4,int(np.frombuffer(colors,'<u4')[index])^1)
    reject('actual displayed native palette color corrupted',lambda:display.check_latch(images[filename],raw,changed,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16)))
    changed=bytearray(raw);palette=np.frombuffer(colors,'<u4');other=int(np.flatnonzero(palette!=palette[index])[0])
    struct.pack_into('<H',changed,(first['row']*512+first['column'])*2,other)
    reject('actual displayed native VRAM pen corrupted',lambda:display.check_latch(images[filename],changed,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16)))
    need(display.check_latch(images[filename],raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16))['passed'],
         'Same actual positive whole scanout restored after effective pixel counterexamples')
    return dict(passed=True,targets=out,effectiveActualScanoutRAMFaults=faults)


def corrected_faults():
    source=inspect.getsource(canonical5467.faults)
    before="r'(^MK2_DEATH_ART_V897_QUEUE .*?y=)(-?\\d+)'"
    after="r'(^MK2_DEATH_ART_V897_QUEUE .*? y=)(-?\\d+)'"
    need(source.count(before)==1,'Only intended Y-coordinate counterexample field boundary corrected; body flags not silently mutated')
    source=source.replace(before,after)
    scope=dict(canonical5467.__dict__)
    exec(compile(source,__file__+'.whole5467_actual_floor_fault_whitespace_field_boundary','exec'),scope)
    return scope['faults']


def run():
    failed=json.loads(FAILED.read_text())
    need(not failed['passed']and failed['error']=="ValueError('Actual native-record counterexample accepted: actual body loses owned floor')"and
         not failed['completedCases'],'Preserved exact first native run/negative-test wrong-field failure')
    log=(ROOT/'audit_v5478_current_reptile_victims_ram/kano_p1/run.log').read_text()
    need('RESULT frame=5198'in log and 'native_dma=514 first=3265 last=3752'in log,'Actual prior native run complete; no expired live handle restarted')
    scope=dict(current.__dict__)
    scope.update(BASE=BASE,OUT=OUT,LUA=LUA,__file__=str(Path(__file__).resolve()),faults=corrected_faults(),native_pixels=native_pixels,COMPLETED=[])
    source=inspect.getsource(canonical5467.capture)
    changes={
      'ram,images,headers={},{},[]':'ram,images,headers,buffers={},{},[],{}',
      "                    else:\n                        need(tag.endswith('_RGB')":
      "                    elif tag.endswith(('_PALETTE','_VRAM')):\n                        kind=tag.rsplit('_',1)[1];need((r['filename'],kind)not in buffers,'Unique actual native palette/VRAM snapshot');buffers[r['filename'],kind]=(raw,r)\n                    else:\n                        need(tag.endswith('_RGB')",
      '    final=dict(passed=True,process=result,':
      "    visual=native_pixels(log,images,buffers,reference,ram['native_death_gfx.bin'],fighter)\n    final=dict(passed=True,actualNativePixelsAndWholeScanout=visual,process=result,",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Whole capture adaptation only actual palette/VRAM/pixel qualification: '+before)
        source=source.replace(before,after)
    exec(compile(source,__file__+'.whole5467_actual_palette_VRAM_pixel_capture','exec'),scope)
    source=inspect.getsource(canonical5467.run)
    changes={
      'reference,expected_gfx=independent_art(guest,payload,pins)':'reference,expected_gfx=corrected_art(guest,payload,pins)',
      "    physical_contract()":"    physical_contract()\n    for p in (ROOT/'tools/current_reptile_victims_ram_v5477.py',ROOT/'tools/current_reptile_victims_ram_v5473.py',ROOT/'mk2ks_current_reptile_ram_v5470.lua',ROOT/'tools/verify_native_floor_display_v602.py',FAILED):pins[str(p)]=sha(p)\n    for p in (ROOT/'audit_v5478_current_reptile_victims_ram').rglob('*'):\n        if p.is_file():pins[str(p)]=sha(p)",
      'independent selected source-PNG native encoding inRAM and84 effective actual record faults':
      'independent original900/1014 corrected source-PNG art, actual palette/body pixels and12 complete native scene scanouts inRAM,84 effective actual native-record faults and12 actual scanout RAM faults',
      'effectiveActualNativeRecordFaults=84,':'effectiveActualNativeRecordFaults=84,effectiveActualScanoutRAMFaults=12,',
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Whole current-run adaptation only added exact displayed-pixel evidence: '+before)
        source=source.replace(before,after)
    exec(compile(source,__file__+'.whole5467_current_corrected_source_art_and_actual_scanout_run','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable current Reptile victim/pixel checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();canonical5467.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','independentSourcePNGNativeReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
