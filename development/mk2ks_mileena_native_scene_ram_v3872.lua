-- Original physical controller. Retain full native CPU/DMA/shift observation,
-- adapt only diagnostic window from Tomb to actual swallowing victim/retire.
dofile('mk2ks_mileena_earned_fixed_v3824.lua')
local previous={}
function MK2KS_TOMB_RAM_SAVE(file,raw)
 assert(#raw%4==0)
 local family=file:match('^display_(pre)_%d+%.bin$') or
  file:match('^display_(vram)_%d+%.bin$') or
  file:match('^display_(palette)_%d+%.bin$') or file
 local prior=previous[family]
 assert(not prior or #prior==#raw)
 local delta={}
 for first=1,#raw,64 do
  local block=raw:sub(first,first+63)
  if not prior or block~=prior:sub(first,first+63)then
   local hex=block:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end)
   delta[#delta+1]=string.format('%d:%s',(first-1)//64,hex)
  end
 end
 previous[family]=raw
 io.stdout:write(string.format('MK2_TOMB_RAM_BUFFER file=%s family=%s bytes=%d prior=%d blocks=%d block_bytes=64 encoding=u32le_numeric_hex_delta\n',file,family,#raw,prior and 1 or 0,#delta),table.concat(delta,','),'\n')
end
function MK2KS_TOMB_RAM_PIXELS(file)
 local raw=manager.machine.video:snapshot_pixels()
 assert(#raw==400*254*4)
 local hex=raw:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end)
 io.stdout:write(string.format('MK2_TOMB_RAM_PIXELS file=%s bytes=%d width=400 height=254 encoding=u32le_numeric_hex\n',file,#raw),hex,'\n')
end
local handle=assert(io.open('mk2ks_native_tomb_display_v2062.lua','rb'))
local source=handle:read('a');handle:close()
local count
source,count=source:gsub("dofile%('mk2ks_stage_branch_provenance_v1722%.lua'%)","-- Physical controller loaded outside the read-only observer")
assert(count==1)
source,count=source:gsub("local move='tomb'","local move='swallowed_victim'")
assert(count==1)
source,count=source:gsub('local action_entry=0xff8bdfe0','local action_entry=0xff9e7d70')
assert(count==1)
source,count=source:gsub("tag,frame,1,identity==17","tag,frame,side,identity==17")
assert(count==1)
local removal=[[
taps[#taps+1]=p:install_read_tap(0xff838f60,0xff838f6f,'actual native swallowed victim disappearance',function(at)
 if at~=0xff838f60 or cpu.PC.value~=0xff838f70 or not active()or retired.frame then return end
 local a=actor(side)
 if not a or a.id~=identity or cpu.A0.value~=a.actor or cpu.A8.value~=a.actor or cpu.A13.value~=a.main then return end
 retired.frame=frame
 log('FLOOR_RETIRED',string.format('entry=FF838F60 id=%d actor=%08X main=%08X mode=%d p1=%08X p2=%08X winner=%d victim_health=%d',a.id,a.actor,a.main,p:read_u16(0x010601d0),p:read_u32(0x01060220),p:read_u32(0x01060df0),p:read_u16(0x01061b00),p:read_u16(side==1 and 0x010602f0 or 0x01060ec0)))
end)
]]
source,count=source:gsub('%-%- Observe actual native sound%-port writes',function()return removal..'\n-- Observe actual native sound-port writes'end)
assert(count==1)
source,count=source:gsub("local f=assert%(io%.open%(output%.%.%s*'/'%.%.file,'wb'%)%);f:write%(raw%);f:close%(%)","MK2KS_TOMB_RAM_SAVE(file,raw)")
assert(count==1)
source,count=source:gsub('screen:snapshot%(file%)','MK2KS_TOMB_RAM_PIXELS(file)')
assert(count==1)
assert(not source:find('io.open',1,true)and not source:find('screen:snapshot',1,true))
print('MK2_MILEENA_NATIVE_SCENE_WRAPPER writes=0 assistance=none window=actual_victim_task_through_native_disappearance_plus30')
assert(load(source,'@mk2ks_native_tomb_display_v2062_Mileena_window_RAM_sinks','t',_ENV))()
