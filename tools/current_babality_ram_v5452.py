"""Source-defined native FIFO/DMA/scanout floor binding, not world=screen."""
from pathlib import Path
import verify_native_floor_display_v602 as display
base=Path(__file__).with_name('current_babality_ram_v5446.py')
source=base.read_text()
changes={
 "BASE=ROOT/'audit_v5447_current_babality_ram'":"BASE=ROOT/'audit_v5453_current_babality_ram'",
 "OUT=ROOT/'audit_v5448_current_babality_progress'":"OUT=ROOT/'audit_v5454_current_babality_progress'",
 "LUA=ROOT/'mk2ks_current_babality_ram_v5446.lua'":"LUA=ROOT/'mk2ks_current_babality_ram_v5452.lua'",
 "need(1<count<=32,'Original baby palette bounds')":"need(1<count<=(1<<((command>>12)&7)),'Original baby palette bounded by native source bit depth')",
 "for path in(LUA,ORIGINAL,Path(__file__).resolve(),":"for path in(LUA,ORIGINAL,ROOT/'mk2ks_current_babality_ram_v5446.lua',ROOT/'tools/current_babality_ram_v5446.py',Path(display.__file__).resolve(),Path(__file__).resolve(),",
 "images={};headers=[];guest_seen=False":"images={};headers=[];guest_seen=False;scanout={}",
 "('MK2_BRAM_GUEST ','MK2_BRAM_RGB '))":"('MK2_BRAM_GUEST ','MK2_BRAM_RGB ','MK2_BRAM_VRAM ','MK2_BRAM_PALETTE '))",
 "     else:\n      need((r['width'],r['height'],len(raw))":"     elif tag in ('MK2_BRAM_VRAM','MK2_BRAM_PALETTE'):\n      scanout[(r['filename'],tag)]=(raw,r)\n     else:\n      need((r['width'],r['height'],len(raw))",
 "rows=model.v.records(log);runtime(rows,spec,ref);pixels=pixel_checks(rows,images,spec,ref,sprites);qualification=faults(rows,images,spec,ref,sprites)":
 "rows=model.v.records(log);runtime(rows,spec,ref);pixels=pixel_checks(rows,images,spec,ref,sprites);projection=scanout_check(log,rows,images,scanout,spec,ref,sprites);qualification=faults(rows,images,spec,ref,sprites)",
 "originalNativeRuntimeAndCommandModelAccepted=True,originalBabyArtPaletteFloorChecks=pixels,":"originalNativeRuntimeAndCommandModelAccepted=True,originalBabyArtPaletteFloorChecks=pixels,nativeProjectionAndScanout=projection,",
 "need(y==int(r['y'])and y+ref['records'][victim]['height']==216,'Actual displayed baby anchored on native floor')":
 "need(int(r['y'])+ref['records'][victim]['height']==216,'Native world floor remains216; screen origin independently gated by original native FIFO/DMA and actual display-start scanout')",
}
for before,after in changes.items():
 assert source.count(before)==1,before
 source=source.replace(before,after)

def scanout_check(log,rows,images,buffers,spec,ref,sprites):
 winner,victim,side,command=spec
 records=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_BRAM_'+tag+' ')]
 qrows=records('QUEUE');drows=records('DISPLAY_DMA');out=[]
 for age in(160,200,240):
  filename=f'babality_{age}.png';raw,r=buffers[filename,'MK2_BRAM_VRAM'];colors,pr=buffers[filename,'MK2_BRAM_PALETTE']
  need(all(r[k]==pr[k]for k in('frame','filename','flip_frame','start','control','tap','pc','mask')),'Actual latch/raster palette association')
  need(r['frame']==r['flip_frame']and r['pc']=='FF8168E0'and r['mask']=='FFFF','One actual native full-mask original display flip per target')
  actual=display.check_latch(images[filename],raw,colors,int(r['start'],16),int(r['control'],16),int(r['tap'],16))
  bound=dict(age=age,**actual)
  if command=='positive':
   baby=next(r for r in model.v.entries(rows,'BABY')if r['age']==str(age))
   matches=[d for d in drows if d['filename']==filename and d['cache']==baby['graphic']and d['actor']==baby['actor']]
   need(len(matches)==1,'Actual physical baby native display DMA')
   d=matches[0];qs=[q for q in qrows if q['frame']==d['queue_frame']and q['cursor']==d['cursor']and q['actor']==d['actor']]
   need(len(qs)==1 and int(d['dma_frame'])<=int(r['flip_frame'])and d['pc']=='FF804640','Actual source-defined original FIFO-to-hardware DMA dispatch')
   q=qs[0];need(q['cache']==d['cache']and q['source']==d['source']and q['writes']=='0'and q['assistance']=='none','Native physical source ownership')
   world=int(q['world'],16);camera=int(q['camera'],16);body=int(q['body'],16)
   coordinate=world if body&1 else (((world>>16)-(camera>>16))&65535)<<16|((world-camera)&65535)
   need(int(q['xy'],16)==coordinate and body&2==0,'Original single-frame native world/camera projection, no inferred sprite offset')
   descriptor=ref['records'][victim];expected_source=descriptor['source_bits']+(0x10000000 if victim!='liu_kang'else 0)
   need(int(q['source'],16)==expected_source and (int(d['width']),int(d['height']))==(descriptor['width'],descriptor['height']),
        'Original baby source bits and complete unscaled native geometry')
   (x,y),count=model.v.image_match(images[filename],sprites[victim])
   need((x,y)==(int(d['x'])-actual['column'],int(d['y'])-actual['row']),
        'Exact displayed baby origin equals actual hardware position minus actual native scanout origin')
   bound.update(originalOpaquePixels=count,displayOrigin=[x,y],nativeDMA=[int(d['x']),int(d['y'])],worldY=int(baby['y']),floorY=216)
  out.append(bound)
 return out

exec(compile(source,str(base)+'.native_FIFO_DMA_scanout_floor','exec'),globals())
