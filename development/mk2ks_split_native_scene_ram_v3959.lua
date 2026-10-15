-- Full native CPU/DMA/shift observer, real Kung Lao earned split finisher.
dofile('mk2ks_stock_extended_earned_ram_v3958.lua')
-- Retain the exact original ten native split constructor/cursor/mirror taps,
-- without loading the older observer that writes separate image/VRAM files.
local trace_file=assert(io.open('mk2ks_native_split_trace_v1098.lua','rb'))
local trace=trace_file:read('a');trace_file:close()
local trace_count
trace,trace_count=trace:gsub("dofile%('mk2ks_stock_fatality_display_v1021%.lua'%)",'-- Original1021 physical controller already loaded')
assert(trace_count==1)
assert(load(trace,'@mk2ks_native_split_trace_v1098_no_duplicate_driver','t',_ENV))()
local previous={}
function MK2KS_TOMB_RAM_SAVE(file,raw)
 assert(#raw%4==0)
 local family=file:match('^display_(pre)_%d+%.bin$')or file:match('^display_(vram)_%d+%.bin$')or file:match('^display_(palette)_%d+%.bin$')or file
 local prior=previous[family];assert(not prior or #prior==#raw)
 local delta={}
 for first=1,#raw,64 do
  local block=raw:sub(first,first+63)
  if not prior or block~=prior:sub(first,first+63)then
   delta[#delta+1]=string.format('%d:%s',(first-1)//64,block:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end))
  end
 end
 previous[family]=raw
 io.stdout:write(string.format('MK2_TOMB_RAM_BUFFER file=%s family=%s bytes=%d prior=%d blocks=%d block_bytes=64 encoding=u32le_numeric_hex_delta\n',file,family,#raw,prior and 1 or 0,#delta),table.concat(delta,','),'\n')
end
function MK2KS_TOMB_RAM_PIXELS(file)
 local raw=manager.machine.video:snapshot_pixels();assert(#raw==400*254*4)
 io.stdout:write(string.format('MK2_TOMB_RAM_PIXELS file=%s bytes=%d width=400 height=254 encoding=u32le_numeric_hex\n',file,#raw),raw:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end),'\n')
end
local file=assert(io.open('mk2ks_native_tomb_display_v2062.lua','rb'))
local source=file:read('a');file:close()
local count
local function exact(pattern,replacement)
 source,count=source:gsub(pattern,function()return replacement end);assert(count==1,'One explicit native observer adaptation '..pattern)
end
exact("dofile%('mk2ks_stage_branch_provenance_v1722%.lua'%)",'-- Original921 earned controller already loaded')
exact("local move='tomb'","local move='split'")
exact('local action_entry=0xff8bdfe0','local action_entry=0xff8c6040')
exact('tag,frame,1,identity==17','tag,frame,side,identity==17')
local old=[[
  local a=actor(side)
  if at==address and cpu.PC.value==address+16 and a and a.owner==a.actor and
     cpu.A8.value==a.actor and cpu.A13.value==a.main and a.id==identity then]]
local new=[[
  local a,victim=actor(3-side),actor(side)
  if at==address and cpu.PC.value==address+16 and a and victim and a.owner==a.actor and victim.owner==victim.actor and
     cpu.A8.value==a.actor and cpu.A13.value==a.main and a.id==0 and victim.id==identity and
     p:read_u16(side==1 and 0x010602f0 or 0x01060ec0)==0 then]]
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1)..new..source:sub(last+1)
-- Native split stores its actual mirrored second actor in the physical
-- victim Main+190. Read that attachment instead of the projectile-only
-- allocator, preserving the original shared Main/primary actor owner.
local old_child=[[
 if n==3 then
  if child.retired or child.parent~=parent or not valid(child.actor or 0)or not valid(child.process or 0)then return end
  -- Keep the original actor after the parent attachment clears, but stop at
  -- its actual native removal. The freed address can be reused by blood.
  a=child.actor;m=child.process
 end]]
local new_child=[[
 if n==3 then
  a=p:read_u32(m+0x190)
  if not valid(a)or a==parent or p:read_u16(a+0x1f0)~=identity then return end
 end]]
local cfirst,clast=assert(source:find(old_child,1,true));assert(not source:find(old_child,clast+1,true))
source=source:sub(1,cfirst-1)..new_child..source:sub(clast+1)
-- Report the actual victim's health on the original both-pointer teardown.
exact('p:read_u16%(side==1 and 0x01060ec0 or 0x010602f0%)','p:read_u16(side==1 and 0x010602f0 or 0x01060ec0)')
exact("local f=assert%(io%.open%(output%.%.%s*'/'%.%.file,'wb'%)%);f:write%(raw%);f:close%(%)",'MK2KS_TOMB_RAM_SAVE(file,raw)')
exact('screen:snapshot%(file%)','MK2KS_TOMB_RAM_PIXELS(file)')
assert(not source:find('io.open',1,true)and not source:find('screen:snapshot',1,true))
print('MK2_SPLIT_NATIVE_SCENE_WRAPPER writes=0 assistance=none window=actual_native_Kung_Lao_action_through_both_pointer_teardown_plus30')
assert(load(source,'@mk2ks_native_tomb_display_v2062_Kung_Lao_window_RAM_sinks','t',_ENV))()
