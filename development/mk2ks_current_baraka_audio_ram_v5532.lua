-- Entire current physical/rendered Baraka observer plus original native audio
-- observer. All taps are passive; all guest/media buffers stay in verifier RAM.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local function read(name)
 local f=assert(io.open(root..'/'..name,'rb'));local s=f:read('*a');f:close()
 return(s:gsub('\r\n','\n'))
end
local s=read('mk2ks_kitana_audio_queue_ram_v3939.lua')
local function replace_once(before,after)
 local first,last=assert(s:find(before,1,true));assert(not s:find(before,last+1,true))
 s=s:sub(1,first-1)..after..s:sub(last+1)
end
replace_once("dofile('mk2ks_stock_earned_ram_v3918.lua')",
 "assert(load(read('mk2ks_current_baraka_ram_v5522.lua'),'@whole_current_Baraka_controller_and_rendered_observers','t',_ENV))()")
replace_once("local function active()return origin and frame<=origin+749 end",
 "local function active()return origin and frame<=origin+749 end\nlocal action_entry=p:read_u32(0xff8ba210+3*32)\nassert(action_entry>=0xff800000 and action_entry<0xffff0000)")
replace_once("p:install_read_tap(0xff8cc650,0xff8cc65f,'actual native inflation audio origin'",
 "p:install_read_tap(action_entry,action_entry+15,'actual native Baraka decapitation audio origin'")
replace_once('at~=0xff8cc650','at~=action_entry')
replace_once('p:read_u16(a+0x1f0)~=4','p:read_u16(a+0x1f0)~=3')
replace_once('origin=%d a8=%08X a13=%08X id=4','origin=%d a8=%08X a13=%08X id=3')
-- No early action+750 host exit: the current qualified controller continues
-- to its own true native terminal5198. Original audio window stays749fields.
assert(load(s,'@whole3939_original_DCS_routes_queue_port_ADSP_channels_and_PCM_Baraka_origin','t',_ENV))()
