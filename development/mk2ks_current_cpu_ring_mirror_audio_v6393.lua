-- Complete original physical mirror driver, without visual files.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local physical=read('mk2ks_current_cpu_ring_render_ram_v6375.lua')
local stop=assert(physical:find("local source=read('mk2ks_physical_p2_cpu_ring_display_v2014.lua')",1,true))
assert(load(physical:sub(1,stop-1),'@whole_original_physical_mirror_driver','t',_G))()
local source=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and frame<=origin+1800 end')
replace('0xff8bdfe0,0xff8bdfef','0xffffb400,0xffffb40f')
replace('at~=0xff8bdfe0','at~=0xffffb400')
replace("p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])",
 'p:read_u16(a+0x1f0)~=18')
-- Establish the passive window on the actual first live frame, before any
-- CPU Ring choice. Both identities/physical roles and Main ownership qualify
-- the origin. This observes the preceding KO, announcement and round reset.
replace("assert(#taps==15,'Every audio observer retained')\n frame=frame+1",
 [[assert(#taps==15,'Every audio observer retained')
 frame=frame+1
 if not origin and frame>700 and p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and p:read_u16(0x01060280)==18 and p:read_u16(0x01060e50)==18 then
  local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
  if valid(a)and valid(m)and p:read_u16(a+0x1f0)==18 and p:read_u32(m+0xc0)==a then
   origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=18',origin,a,m))
  end
 end]])
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin==1823 and frame==origin+1800,'Both complete sound ROM checks and full unchanged native mirror match terminal')")
assert(load(source,'@whole_native_Sonya_mirror_match_audio_v6393','t',_G))()
