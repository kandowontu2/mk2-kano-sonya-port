"""Native cache-owned shadow DMA with sparse transient displayed-point checks."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_idle_scanout_delayed_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    lua=lua.replace('source_frame=%d slot=%d id=%d dma_x=', 'kind=%s source_frame=%d slot=%d id=%d dma_x=',1)
    lua=lua.replace('q.frame,q.slot,q.id,q.x,q.y,','q.kind or "body",q.frame,q.slot,q.id,q.x,q.y,',1)
    lua+=r'''
local shadow_tap=p:install_write_tap(0x01a80010,0x01a8001f,'cache-owned native idle shadow output',function(at,data)
 if not ready or (frame-ready)%8~=0 or at~=0x01a80010 or (regs.PC.value~=0xff8015a0 and regs.PC.value~=0xff801610)then return end
 local row=regs.A9.value;local own,slot
 for n=1,2 do
  local a=sample(n);local cache=p:read_u32(a.actor+0x1a0)
  if valid(cache) and row>=cache and row<cache+12*112 and (row-cache)%112==0 and p:read_u32(row)~=0 then
   assert(not own,'Unique actual cache owner');own=a;slot=n
  end
 end
 assert(own and own.owner==own.actor,'Native owned shadow row')
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local c=data&65535;local source=reg(2)|(reg(3)<<16)
 local x,y,w,h=reg(4)&1023,reg(5)&511,reg(6)&1023,reg(7)&1023
 assert(h==1 and c&15==8,'Original one-row solid nonzero shadow')
 local count,top,bottom,bits,px,pixel=opaque_bounds(source,w,h,c)
 log('IDLE_SHADOW_DMA',string.format('slot=%d id=%d actor=%08X main=%08X owner=%08X pose=%08X cache_row=%08X graphic=%08X source=%08X command=%04X x=%d y=%d width=%d height=%d opaque=%d pc=%08X scaleX=%d scaleY=%d',
  slot,own.id,own.actor,own.main,own.owner,own.pose,row,p:read_u32(row),source,c,x,y,w,h,count,regs.PC.value,reg(10),reg(11)))
 if count>0 then idle_points[#idle_points+1]={frame=frame,slot=slot,id=own.id,kind='shadow',x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|(reg(9)&255)}end
end)
emu.register_stop(function()assert(shadow_tap,'Retained native shadow observer')end)
'''
    out=root/'audit_bounded_idle_shadow_points_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_scanout_delayed_runtime',f'audit_bounded_{fighter}_idle_shadow_points_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
