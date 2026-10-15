-- Same whole UI/GFX/battle-owner observers plus passive private-finisher pool.
local filename='mk2ks_launch_candidate_ui.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local before="dofile('mk2ks_current_ui_audio_ram_v5430.lua')"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1).."dofile('mk2ks_native_kano_laser_ui_channels.lua')"..source:sub(b+1)
assert(load(source,'@'..filename..'::same_UI_GFX_owners_all19channels','t',_G))()
local frame,items=0,{}
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_finish_audio_(.+)$')
   if field then assert(not items[field]);items[field]=emu.item(index)end
  end
  assert(items.actor and items.main and items.slot and items.priority and items.remaining)
 end
 local values={}
 for n=0,4 do values[#values+1]=string.format('%04X,%d',items.priority:read(n),items.remaining:read(n))end
 print(string.format('MK2_UI_FINISH_POOL frame=%d slot=%d actor=%08X main=%08X slots=%s writes=0 assistance=none',
 frame,items.slot:read(0),items.actor:read(0),items.main:read(0),table.concat(values,';')))
end)
