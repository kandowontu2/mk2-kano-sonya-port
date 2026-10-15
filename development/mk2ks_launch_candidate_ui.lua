-- Entire previously qualified physical UI controller/display/audio probe.
-- Extra inventory is read-only; no guest, source item or gameplay writes.
dofile('mk2ks_current_ui_audio_ram_v5430.lua')
local frame,owners=0,{}
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_battle_(.+)$')
   if field then assert(not owners[field]);owners[field]=emu.item(index)end
  end
  assert(owners.actor and owners.main and owners.health and owners.id)
  local region=assert(manager.machine.memory.regions[':gfxrom']);local bytes={}
  for i=0,11943 do bytes[#bytes+1]=string.char(region:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(region:read_u8(0x1fa4000+i))end
  local raw=table.concat(bytes);assert(#raw==18976)
  print('MK2_UA_GFX frame=1 bytes=18976 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
 end
 for slot=1,2 do
  print(string.format('MK2_UA_OWNER frame=%d seconds=%.12f slot=%d actor=%08X main=%08X health=%d id=%d writes=0 assistance=none',
   frame,emu.time(),slot,owners.actor:read(slot-1),owners.main:read(slot-1),owners.health:read(slot-1),owners.id:read(slot-1)))
 end
end)
