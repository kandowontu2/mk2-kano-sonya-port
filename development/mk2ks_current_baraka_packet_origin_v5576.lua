-- Entire qualified5565 physical/raster/PCM/fighter/announcer observer, plus
-- two passive original packet entry/return taps. No state/output/audio writes.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local file=assert(io.open(root..'/mk2ks_current_baraka_announcer_ram_v5565.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@whole5565_qualified_physical_raster_and_dual_dispatcher','t',_ENV))()
local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,serial,taps,pending=0,0,{},{}
local function active()
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 return start and frame>=start and frame<=start+749
end
local function log(tag,id,entry)
 print(string.format('MK2_PORIGIN_%s frame=%d seconds=%.12f writes=0 assistance=none serial=%d entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X sp=%08X return_pc=%08X mute=%04X',
  tag,frame,emu.time(),id,entry,cpu.A1.value,cpu.A3.value,cpu.A4.value,cpu.A8.value,cpu.A13.value,
  cpu.SP.value,p:read_u32(cpu.SP.value),p:read_u16(0x01061990)))
end
for _,entry in ipairs({0xffa13ba0,0xffa13dd0})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual original packet caller and return',function(at)
  if at~=entry or cpu.PC.value~=at+16 or not active()then return end
  local main=cpu.A13.value
  if entry==0xffa13ba0 then
   assert(not pending[main],'No unaccounted nested native packet')
   serial=serial+1;pending[main]={serial=serial,actor=cpu.A8.value,sp=cpu.SP.value,caller=p:read_u32(cpu.SP.value)}
   log('ENTRY',serial,entry)
  else
   local item=assert(pending[main],'Native packet return requires actual entry')
   assert(item.actor==cpu.A8.value and item.sp==cpu.SP.value and item.caller==p:read_u32(cpu.SP.value),'Native packet actor/task/stack/caller restored')
   log('END',item.serial,entry);pending[main]=nil
  end
 end)
end
emu.register_frame(function()frame=frame+1;assert(#taps==2,'Both original passive packet observers retained')end)
emu.register_stop(function()
 local remaining=0;for _ in pairs(pending)do remaining=remaining+1 end
 print(string.format('MK2_PORIGIN_RESULT frame=%d calls=%d pending=%d writes=0 assistance=none',frame,serial,remaining))
 for _,tap in ipairs(taps)do tap:remove()end
end)
