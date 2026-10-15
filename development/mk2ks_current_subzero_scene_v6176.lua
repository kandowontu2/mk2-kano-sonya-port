-- Complete original native render observer; genuine earned freeze/shatter.
-- Suppress only the older driver's duplicate raw transport. The complete
-- native2062 observer below owns guest/VRAM/palette/continuousRGB transport.
local actual_print=print
function print(...)
 local first=select(1,...)
 if type(first)=='string'and(first:match('^MK2_EARNED_SUBZERO_GUEST ')or first:match('^MK2_EARNED_SUBZERO_GFX ')or first:match('^MK2_EARNED_SUBZERO_RGB '))then
  actual_print('MK2_SUBZERO_DUPLICATE_RAW_TRANSPORT_SKIPPED writes=0 assistance=none')
  return
 end
 actual_print(...)
end
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local side=assert(tonumber(os.getenv('MK2KS_STAGE_SIDE')))
local palette_taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
-- Original actual palette primitive receives A0. Observe real source choice,
-- including native flashing and ice64, never infer it from desired pose/color.
palette_taps[#palette_taps+1]=p:install_read_tap(0xff841090,0xff84109f,'actual native palette source',function(at,data,mask)
 if at~=0xff841090 or cpu.PC.value~=at+16 then return end
 local actor,main=cpu.A8.value,cpu.A13.value
 if not valid(actor)or not valid(main)or p:read_u32(main+0xc0)~=actor then return end
 local slot=nil
 for n=1,2 do if p:read_u32(n==1 and 0x01060220 or 0x01060df0)==actor then slot=n end end
 if not slot then return end
 actual_print(string.format('MK2_SUBZERO_SCENE_PALETTE entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d slot=%d pointer=%08X writes=0 assistance=none',
  at,cpu.PC.value,data&0xffff,mask,actor,main,p:read_u32(main+0xc0),p:read_u16(actor+0x1f0),slot,cpu.A0.value))
end)
emu.register_stop(function()for _,tap in ipairs(palette_taps)do tap:remove()end end)
local file=assert(io.open('mk2ks_jax_clap_native_scene_ram_v4019.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'One exact complete native observer adaptation')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace("dofile('mk2ks_stock_extended_earned_ram_v3958.lua')","dofile('mk2ks_native_subzero_legs_nextmatch_v5000.lua')")
replace("local move='jax_clap'","local move='subzero_shatter'")
replace("local action_entry=0xff8c7820","local action_entry=0xff8c2320")
replace('local a,victim=actor(3-side),actor(side)','local a,victim=actor(side),actor(3-side)')
replace('a.id==11 and victim.id==identity','a.id==identity and victim.id==8')
replace('MK2_JAX_CLAP_NATIVE_SCENE_WRAPPER','MK2_CURRENT_SUBZERO_NATIVE_SCENE_WRAPPER')
assert(load(source,'@whole_native_Subzero_earned_scene_RAM_only','t',_ENV))()
