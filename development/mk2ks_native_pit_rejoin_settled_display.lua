-- Preserve the entire original native scene observer and its original window.
local f=assert(io.open('mk2ks_native_pit_display_v2092.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once("dofile('mk2ks_native_stage_performer_v806.lua')","dofile('mk2ks_native_pit_rejoin_settled_provenance.lua')")
once("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)')
once('screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)')
-- Reuse the unchanged complete3624 delta sinks, without loading its driver.
local sink=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','rb'))
local sinks=sink:read('a'):gsub('\r\n','\n');sink:close()
local boundary=assert(sinks:find("local handle=assert(io.open('mk2ks_native_tomb_display_v2062.lua'",1,true))
sinks=sinks:sub(1,boundary-1)
assert(load(sinks,'@complete3624_original_RAM_sinks_only','t',_ENV))()
local post=[=[
-- Later scanouts are separate native VRAM/palette bindings, not model anchors.
local post_previous,post_latch={},nil
local function post_active()return retired.frame and frame>retired.frame+30 end
local function post_save(file,raw)
 local family=assert(file:match('^display_(vram)_%d+%.bin$')or file:match('^display_(palette)_%d+%.bin$'))
 local prior=post_previous[family];local delta={};assert(not prior or #prior==#raw)
 for first=1,#raw,64 do
  local block=raw:sub(first,first+63)
  if not prior or block~=prior:sub(first,first+63)then
   local hex=block:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end)
   delta[#delta+1]=string.format('%d:%s',(first-1)//64,hex)
  end
 end
 post_previous[family]=raw
 io.stdout:write(string.format('MK2_TOMB_POST_BUFFER file=%s family=%s bytes=%d prior=%d blocks=%d block_bytes=64 encoding=u32le_numeric_hex_delta\n',file,family,#raw,prior and 1 or 0,#delta),table.concat(delta,','),'\n')
end
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'later native display latch',function(at,data,mask)
 if at~=0xc0000090 or not post_active()then return end
 post_latch={frame=frame,start=data&0xffff,control=p:read_u16(0xc0000080),tap=p:read_u16(0xc00001b0),raw=vram:read_block(0,512*512*2)}
end)
emu.register_frame_done(function()
 if not post_active()then return end
 local a1,a2=actor(1),actor(2)
 local function value(a,k)return a and a[k]or 0 end
 local latch_now=post_latch and post_latch.frame==frame
 local start=latch_now and post_latch.start or p:read_u16(0xc0000090)
 local control=latch_now and post_latch.control or p:read_u16(0xc0000080)
 local tap=latch_now and post_latch.tap or p:read_u16(0xc00001b0)
 print(string.format('MK2_TOMB_POST_STATE frame=%d writes=0 assistance=none retired=%d action=%d admitted=%d mode=%d arena=%d start=%04X control=%04X tap=%04X latched=%d actor1=%08X main1=%08X owner1=%08X id1=%d roster1=%d state1=%d hp1=%d actor2=%08X main2=%08X owner2=%08X id2=%d roster2=%d state2=%d hp2=%d',
  frame,retired.frame,command,MK2KS_TOMB_POST_ADMITTED or-1,p:read_u16(0x010601d0),p:read_u16(0x01061ac0),start,control,tap,latch_now and 1 or 0,
  value(a1,'actor'),value(a1,'main'),value(a1,'owner'),value(a1,'id'),p:read_u16(0x01060280),p:read_u16(0x010601f0),p:read_u16(0x010602f0),
  value(a2,'actor'),value(a2,'main'),value(a2,'owner'),value(a2,'id'),p:read_u16(0x01060e50),p:read_u16(0x01060dc0),p:read_u16(0x01060ec0)))
 post_save(string.format('display_vram_%d.bin',frame),latch_now and post_latch.raw or vram:read_block(0,512*512*2))
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',palette:pen_color(pen)&0xffffff)end
 post_save(string.format('display_palette_%d.bin',frame),table.concat(colors))
 local raw=manager.machine.video:snapshot_pixels();assert(#raw==400*254*4)
 local hex=raw:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end)
 io.stdout:write(string.format('MK2_TOMB_POST_PIXELS frame=%d bytes=%d width=400 height=254 encoding=u32le_numeric_hex\n',frame,#raw),hex,'\n')
end)
]=]
once('\nend\n-- END v2092 full-render read-only observer','\n'..post..'\nend\n-- END v2092 full-render read-only observer')
assert(not source:find(':write_',1,true)and not source:find('io.open',1,true))
assert(load(source,'@whole2062_then_later_native_scanouts_no_disk','t',_ENV))()
emu.register_frame_done(function()
 if emu.time()>=890 then print('MK2_CURRENT_PIT_RENDER_DEADLINE writes=0 assistance=none');manager.machine:exit()end
end)
