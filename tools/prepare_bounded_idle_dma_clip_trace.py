"""Mirror only actual native DMA writes to resolve banked clip/skip state."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_idle_shadow_coverage_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker='local idle_points={}';assert lua.count(marker)==1
    mirror=r'''
local actual_dma={}
local clip_tap=p:install_write_tap(0x01a80000,0x01a800ff,'passive exact native DMA banked registers',function(at,data,mask)
 if (at-0x01a80000)%16~=0 then return end
 local n=(at-0x01a80000)//16
 if n==12 or n==13 then
  local bank=(p:read_u16(0x01a800f0)>>5)&1
  if bank==0 then n=n+4 end
 end
 mask=mask&65535;data=data&65535
 local before=actual_dma[n]or 0
 actual_dma[n]=(before&(~mask&65535))|(data&mask)
end)
local function clip_trace(kind,slot,id,source,x,y,w,h,c)
 assert(actual_dma[0]~=nil and actual_dma[12]~=nil and actual_dma[13]~=nil and actual_dma[16]~=nil and actual_dma[17]~=nil,'Clip and skip state actually initialized by native writes')
 log('IDLE_DMA_CLIP',string.format('kind=%s slot=%d id=%d source=%08X x=%d y=%d width=%d height=%d command=%04X lrskip=%04X top=%d bottom=%d left=%d right=%d config=%04X',
  kind,slot,id,source,x,y,w,h,c,actual_dma[0],actual_dma[12]&511,actual_dma[13]&511,actual_dma[16]&1023,actual_dma[17]&1023,p:read_u16(0x01a800f0)))
end
emu.register_stop(function()assert(clip_tap)end)
'''
    lua=lua.replace(marker,mirror+marker,1)
    marker=' coverage_context={x=x,y=y,bank=reg(8)&0x7f00,id=own.id,slot=own.slot,pc=regs.PC.value}'
    assert lua.count(marker)==1
    lua=lua.replace(marker," clip_trace('body',own.slot,own.id,src,x,y,w,h,c)\n"+marker,1)
    marker=" assert(h==1 and c&15==8,'Original one-row solid nonzero shadow')";assert lua.count(marker)==1
    lua=lua.replace(marker,marker+"\n clip_trace('shadow',slot,own.id,source,x,y,w,h,c)",1)
    out=root/'audit_bounded_idle_dma_clip_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_shadow_coverage_runtime',f'audit_bounded_{fighter}_idle_dma_clip_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
