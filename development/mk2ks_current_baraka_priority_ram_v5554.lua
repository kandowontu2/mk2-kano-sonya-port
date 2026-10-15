-- Entire qualified physical/raster/audio observer, seven additional passive
-- priority taps. Never write guest/register/output/controller/audio state.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local file=assert(io.open(root..'/mk2ks_current_baraka_audio_ram_v5536.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@whole5536_current_native_physical_raster_and_audio','t',_ENV))()
local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,serial,taps,pending=0,0,{},{}
local function active()
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 return start and frame>=start and frame<=start+749
end
local function log(tag,s)
 print(string.format('MK2_BPRIO_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),s))
end
local function tap(entry,callback)
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual original sound priority decision',function(at)
  if at==entry and cpu.PC.value==at+16 and active()then callback(entry)end
 end)
end
local function tuple(id,entry)
 return string.format('serial=%d entry=%08X a0=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X',
  id,entry,cpu.A0.value,cpu.A1.value,cpu.A3.value,cpu.A4.value,cpu.A8.value,cpu.A13.value)
end
tap(0xffa12530,function(entry)
 serial=serial+1
 local main=cpu.A13.value
 assert(not pending[main],'No unaccounted nested original command dispatcher')
 pending[main]={serial=serial,actor=cpu.A8.value}
 local command=cpu.A0.value;local table_at=(0xffa0ef20+((command<<5)&0xffffffff))&0xffffffff
 local header,base=0,0
 if table_at>=0xffa0ef20 and table_at<0xffa10ee0 then
  header=p:read_u16(table_at);base=p:read_u16(table_at+16)
 end
 log('CALL',tuple(serial,entry)..string.format(
  ' mute=%04X command=%08X table=%08X header=%04X base=%04X priority0=%04X priority1=%04X priority2=%04X duration0=%04X duration1=%04X duration2=%04X caller=%08X',
  p:read_u16(0x01061990),command,table_at,header,base,
  p:read_u16(0x010b8100),p:read_u16(0x010b8140),p:read_u16(0x010b8180),
  p:read_u16(0x010b8110),p:read_u16(0x010b8150),p:read_u16(0x010b8190),p:read_u32(cpu.SP.value)))
end)
for _,entry in ipairs({0xffa12a10,0xffa12a80,0xffa12b00})do
 tap(entry,function(at)
  local item=pending[cpu.A13.value]
  if item then
   assert(item.actor==cpu.A8.value,'Actual pending command actor remains native')
   assert(not item.queued,'Only one original simple priority slot')
   item.queued=at;log('QUEUE',tuple(item.serial,at))
  else log('UNBOUND_QUEUE',tuple(0,at))end
 end)
end
for _,entry in ipairs({0xffa129d0,0xffa12b90,0xffa13de0})do
 tap(entry,function(at)
  local main=cpu.A13.value;local item=pending[main]
  if item then
   assert(item.actor==cpu.A8.value,'Original sound decision actor remains native')
   log('END',tuple(item.serial,at)..string.format(' queued=%08X',item.queued or 0));pending[main]=nil
  else log('UNBOUND_END',tuple(0,at))end
 end)
end
emu.register_frame(function()frame=frame+1;assert(#taps==7,'All seven read-only priority observers retained')end)
emu.register_stop(function()
 local remaining=0;for _ in pairs(pending)do remaining=remaining+1 end
 log('RESULT',string.format('calls=%d pending=%d',serial,remaining))
 for _,item in ipairs(taps)do item:remove()end
end)
