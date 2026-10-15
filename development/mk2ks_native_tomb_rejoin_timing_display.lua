-- Full original scene plus its separate later captures. Additional data are
-- diagnostics, NEVER a best-buffer search or a substitute passing target.
local f=assert(io.open('mk2ks_native_tomb_rejoin_display.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once("dofile('mk2ks_native_tomb_rejoin_provenance.lua')","dofile('mk2ks_native_tomb_rejoin_guarded_provenance.lua')")
once("local family=assert(file:match('^display_(vram)_%d+%.bin$')or file:match('^display_(palette)_%d+%.bin$'))",
 "local family=assert(file:match('^display_(vram)_%d+%.bin$')or file:match('^display_(palette)_%d+%.bin$')or file:match('^display_(pre)_%d+%.bin$'))")
once('post_latch={frame=frame,start=data&0xffff,control=',
 'post_latch={frame=frame,vcount=p:read_u16(0xc00001c0),dpyadr=p:read_u16(0xc00001e0),before=p:read_u16(0xc0000090),pc=cpu.PC.value,start=data&0xffff,control=')
local old=" post_save(string.format('display_vram_%d.bin',frame),latch_now and post_latch.raw or vram:read_block(0,512*512*2))"
local extra=[=[
 print(string.format('MK2_TOMB_POST_TIMING frame=%d vcount=%04X dpyadr=%04X dpystart=%04X control=%04X tap=%04X flip_frame=%d flip_start=%04X flip_before=%04X flip_pc=%08X flip_vcount=%04X flip_dpyadr=%04X x1=%d y1=%d pose1=%08X x2=%d y2=%d pose2=%08X',
  frame,p:read_u16(0xc00001c0),p:read_u16(0xc00001e0),p:read_u16(0xc0000090),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),
  post_latch and post_latch.frame or-1,post_latch and post_latch.start or 0,post_latch and post_latch.before or 0,
  post_latch and post_latch.pc or 0,post_latch and post_latch.vcount or 0,post_latch and post_latch.dpyadr or 0,
  value(a1,'x'),value(a1,'y'),value(a1,'pose'),value(a2,'x'),value(a2,'y'),value(a2,'pose')))
 post_save(string.format('display_pre_%d.bin',frame),vram:read_block(0,512*512*2))
]=]
once(old,old..'\n'..extra)
assert(load(source,'@whole_rejoin_display_extra_native_timing_and_current_VRAM','t',_ENV))()
