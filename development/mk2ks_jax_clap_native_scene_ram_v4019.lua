-- Full native CPU/DMA/shift observer, real Jax earned head-clap finisher.
dofile('mk2ks_stock_extended_earned_ram_v3958.lua')
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
exact("local move='tomb'","local move='jax_clap'")
exact('local action_entry=0xff8bdfe0','local action_entry=0xff8c7820')
exact('tag,frame,1,identity==17','tag,frame,side,identity==17')
-- Reference captures physically select their actual stock roster IDs and
-- retain separate labels; never relabel them as Kano or Sonya evidence.
exact("local identity=assert%(%({kano=17,sonya=18}%)%[os%.getenv%('MK2KS_STAGE_WINNER'%)%]%)",
 "local identity=assert(({kano=17,sonya=18,liu_kang=1,kitana=4})[os.getenv('MK2KS_STAGE_WINNER')])")
exact("identity==17 and'kano'or'sonya'","os.getenv('MK2KS_STAGE_WINNER')")
local old=[[
  local a=actor(side)
  if at==address and cpu.PC.value==address+16 and a and a.owner==a.actor and
     cpu.A8.value==a.actor and cpu.A13.value==a.main and a.id==identity then]]
local new=[[
  local a,victim=actor(3-side),actor(side)
  if at==address and cpu.PC.value==address+16 and a and victim and a.owner==a.actor and victim.owner==victim.actor and
     cpu.A8.value==a.actor and cpu.A13.value==a.main and a.id==11 and victim.id==identity and
     p:read_u16(side==1 and 0x010602f0 or 0x01060ec0)==0 then]]
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1)..new..source:sub(last+1)
-- Retain original allocator lifetime handling. Jax head-clap does not use
-- Kung Lao's secondary mirrored victim attachment.
-- Report the actual victim's health on the original both-pointer teardown.
exact('p:read_u16%(side==1 and 0x01060ec0 or 0x010602f0%)','p:read_u16(side==1 and 0x010602f0 or 0x01060ec0)')
exact("local f=assert%(io%.open%(output%.%.%s*'/'%.%.file,'wb'%)%);f:write%(raw%);f:close%(%)",'MK2KS_TOMB_RAM_SAVE(file,raw)')
exact('screen:snapshot%(file%)','MK2KS_TOMB_RAM_PIXELS(file)')
assert(not source:find('io.open',1,true)and not source:find('screen:snapshot',1,true))
print('MK2_JAX_CLAP_NATIVE_SCENE_WRAPPER writes=0 assistance=none window=actual_native_Jax_action_through_both_pointer_teardown_plus30')
assert(load(source,'@mk2ks_native_tomb_display_v2062_Jax_clap_window_RAM_sinks','t',_ENV))()
