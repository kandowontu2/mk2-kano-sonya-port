-- Entire original two-cycle controller/body/shadow observer, byte unchanged.
local file=assert(io.open('mk2ks_special_shadow_v5131.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@entire_original_special_shadow_controller','t',_G))()
-- Passive current nineteen-channel/private-finisher-pool observer only.
local frame,channels,items=0,{},{}
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for channel=0,18 do local c=assert(channels[channel]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)end
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_finish_audio_(.+)$')
   if field then assert(not items[field]);items[field]=emu.item(index)end
  end
  assert(items.actor and items.main and items.slot and items.priority and items.remaining)
 end
 for channel=0,18 do
  local c=channels[channel];local pos=string.unpack('<d',c.pos:read_block(0,8))
  print(string.format('MK2_SS_CHANNEL frame=%d channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0 assistance=none',
   frame,channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
 end
 local values={};for n=0,4 do values[#values+1]=string.format('%04X,%d',items.priority:read(n),items.remaining:read(n))end
 print(string.format('MK2_SS_FINISH_POOL frame=%d slot=%d actor=%08X main=%08X slots=%s writes=0 assistance=none',
  frame,items.slot:read(0),items.actor:read(0),items.main:read(0),table.concat(values,';')))
end)
