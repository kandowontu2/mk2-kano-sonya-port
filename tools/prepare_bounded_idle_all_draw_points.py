"""Sparse per-point later-draw replay; no framebuffer model or media retention."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_idle_dma_clip_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker="   local index=q.cover_index or q.index";assert lua.count(marker)==1
    lua=lua.replace(marker,"   local index=q.all_index or q.cover_index or q.index",1)
    marker="   log('IDLE_SHADOW_COVER',string.format(";assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
   log('IDLE_ALL_DRAW_FINAL',string.format('source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d index=%d source=%08X command=%04X pc=%08X source_x=%d source_y=%d final=%06X actual=%06X match=%d',
    q.frame,q.slot,q.id,q.x,q.y,index,q.all_source or 0,q.all_command or 0,q.all_pc or 0,q.all_sx or -1,q.all_sy or -1,final,actual,final==actual and 1 or 0))
'''+marker,1)
    lua+=r'''
local function queried_source_pixel(source,w,h,c,sx,sy)
 local bpp=(c>>12)&7;if bpp==0 then bpp=8 end
 local mapped=source
 if source>=0x10000000 and source<0x1a000000 then mapped=source-0x0a000000
 elseif mapped>=0xf8000000 then mapped=mapped-0xf8000000
 elseif mapped>=0x02000000 then mapped=mapped-0x02000000 end
 assert(mapped>=0 and mapped<sole_gfx.size*8,'Actual later source region')
 local function read(bit,n)
  assert(bit+n<=sole_gfx.size*8)
  local at=bit//8;return ((sole_gfx:read_u8(at)|(sole_gfx:read_u8(at+1)<<8))>>(bit%8))&((1<<n)-1)
 end
 local bit=mapped
 local startskip=c&0x40~=0 and (actual_dma[0]&255) or 0
 local endskip=c&0x40~=0 and (actual_dma[0]>>8) or actual_dma[0]
 if sx<startskip or sx>=w-endskip then return nil end
 if c&0x80==0 then return read(bit+(sy*w+sx)*bpp,bpp)end
 for y=0,sy do
  local header=read(bit,8);bit=bit+8
  local pre=(header&15)<<((c>>8)&3);local post=(header>>4)<<((c>>10)&3)
  if y==sy then
   if sx<pre or sx>=w-post then return nil end
   return read(bit+(sx-pre)*bpp,bpp)
  end
  bit=bit+math.max(0,w-pre-post)*bpp
 end
end
local all_draw_tap=p:install_write_tap(0x01a80010,0x01a8001f,'all later draws at sparse shadow queries',function(at,data)
 if not ready or at~=0x01a80010 or data&0x8000==0 then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local c=data&65535;local w,h=reg(6)&1023,reg(7)&1023
 local x,y=reg(4)&1023,reg(5)&511;local src=reg(2)|(reg(3)<<16)
 if w==0 or h==0 then return end
 for _,q in ipairs(idle_points)do
  if q.kind=='shadow' and q.frame==frame then
   local sx=c&16~=0 and ((x-q.x)&1023)or((q.x-x)&1023)
   local sy=c&32~=0 and ((y-q.y)&511)or((q.y-y)&511)
   if sx<w and sy<h and q.x>=actual_dma[16] and q.x<=actual_dma[17] and q.y>=actual_dma[12] and q.y<=actual_dma[13]then
    assert((reg(10)==0 or reg(10)==256)and(reg(11)==0 or reg(11)==256),'Finite queried unit scale')
    local mode=c&15;local pixel=mode==12 and 1 or queried_source_pixel(src,w,h,c,sx,sy)
    if pixel~=nil then
     local index=nil
     if pixel~=0 then
      if mode&8~=0 then index=(reg(8)&0x7f00)|(reg(9)&255)
      elseif mode&2~=0 then index=(reg(8)&0x7f00)|pixel end
     else
      if mode&4~=0 then index=(reg(8)&0x7f00)|(reg(9)&255)
      elseif mode&1~=0 then index=reg(8)&0x7f00 end
     end
     if index then q.all_index=index;q.all_source=src;q.all_command=c;q.all_pc=regs.PC.value;q.all_sx=sx;q.all_sy=sy end
    end
   end
  end
 end
end)
emu.register_stop(function()assert(all_draw_tap)end)
'''
    out=root/'audit_bounded_idle_all_draw_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_dma_clip_runtime',f'audit_bounded_{fighter}_idle_all_draw_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
