-- Entire qualified physical/art/PCM/packet observer and read-only DAC queue.
-- No emu.item writes, forced flushes, sound calls or guest modifications.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_baraka_packet_origin_v5576.lua','rb'))
local s=f:read('*a');f:close()
assert(load(s,'@entire5576_native_physical_art_packet_audio_observers','t',_ENV))()
local frame,serial,previous,previous_time=0,0,nil,nil
local dac,dcs={},{}
local function bind(device,wanted)
 local result={}
 for name,index in pairs(assert(manager.machine.devices[device]).items)do
  for _,key in ipairs(wanted)do
   if name:match(key..'$')then assert(not result[key]);result[key]=emu.item(index)end
  end
 end
 for _,key in ipairs(wanted)do assert(result[key],'Missing original native item '..key)end
 return result
end
local function segment(first,count)
 assert(count>=0 and count<32768)
 local a=math.min(count,32768-first)
 local raw=dac.m_buffer:read_block(first*4,a*4)
 if a<count then raw=raw..dac.m_buffer:read_block(0,(count-a)*4)end
 assert(#raw==count*4);return raw
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  dac=bind(':dcs:dac',{'m_buffer','m_bufin','m_bufout','m_volume','m_enabled'})
  dcs=bind(':dcs',{'m_channels','m_size','m_incs','m_ireg','m_ireg_base','m_control_regs'})
  assert(dac.m_buffer.size==4 and dac.m_buffer.count==32768 and dcs.m_control_regs.size==2 and dcs.m_control_regs.count==32)
 end
end)
emu.register_sound_update(function()
 if not dac.m_bufout then return end
 local current=dac.m_bufout:read(0)
 local old,oldtime=previous,previous_time
 previous=current;previous_time=emu.time()
 local origin=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if not origin or frame<origin or frame>origin+749 then return end
 assert(old and oldtime and current<32768 and old<32768)
 local count=(current-old)%32768
 assert(count<4096,'No unaccounted native DAC reset or ring traversal')
 local raw=segment((old-4)%32768,count+4)
 serial=serial+1
 print(string.format('MK2_NATIVE_DAC_RAM frame=%d seconds=%.12f previous_seconds=%.12f index=%d writes=0 assistance=none previous_out=%d current_out=%d current_in=%d consumed=%d prefix=4 ring=32768 element_bytes=4 enabled=%d volume=%08X channels=%d size=%d incs=%d ireg=%d base=%d autobuffer=%04X syscontrol=%04X s1control=%04X sclkdiv=%04X bytes=%d hex=%s',
  frame,emu.time(),oldtime,serial,old,current,dac.m_bufin:read(0),count,dac.m_enabled:read(0),dac.m_volume:read(0),
  dcs.m_channels:read(0),dcs.m_size:read(0),dcs.m_incs:read(0),dcs.m_ireg:read(0),dcs.m_ireg_base:read(0),
  dcs.m_control_regs:read(15),dcs.m_control_regs:read(31),dcs.m_control_regs:read(18),dcs.m_control_regs:read(17),#raw,
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end)
emu.register_stop(function()
 print(string.format('MK2_NATIVE_DAC_RESULT frame=%d callbacks=%d writes=0 assistance=none',frame,serial))
end)
