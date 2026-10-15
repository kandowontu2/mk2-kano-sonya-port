local machine=manager.machine
local p=machine.devices[':maincpu'].spaces.program
local cpu=machine.devices[':maincpu'].state
local button=machine.ioport.ports[':IN0'].fields['P1 High Punch']
local frame,taps=0,{}
local function log(tag,text)print('MK2_LIGHT_ATTRACT_'..tag..' frame='..frame..' writes=0 assistance=none '..text)end
taps[#taps+1]=p:install_write_tap(0x01061ca0,0x01061caf,'native biography counter',function(at,data,mask)
 log('COUNTER',string.format('id=%d pc=%08X mask=%04X',data&0xffff,cpu.PC.value,mask))
end)
for _,id in ipairs({17,18})do
 local first=0xff800000+(0xf3780+id*12)*8
 taps[#taps+1]=p:install_read_tap(first,first+95,'own biography record',function(at,data,mask)
  log('BIO_READ',string.format('id=%d at=%08X pc=%08X data=%04X mask=%04X counter=%d',id,at,cpu.PC.value,data,mask,p:read_u16(0x01061ca0)))
 end)
end
local picture=0xff800000+0xf4900*8
taps[#taps+1]=p:install_read_tap(picture,picture+56*32-1,'native biography picture',function(at,data,mask)
 if cpu.PC.value==0xff8447e0 and(at-picture)%32==0 then
  log('PICTURE',string.format('row=%d pc=%08X data=%04X',(at-picture)//32,cpu.PC.value,data))
 end
end)
emu.register_frame(function()
 frame=frame+1;button:clear_value()
 if frame>=300 and frame<304 then button:set_value(1);log('INPUT','button=HighPunch slot=1')end
 if frame%60==0 then log('FIELD',string.format('mode=%d counter=%d roster=%d,%d',p:read_u16(0x010601d0),p:read_u16(0x01061ca0),p:read_u16(0x01060280),p:read_u16(0x01060e50)))end
 if frame>=24000 then log('BOUND','maximum_fields=24000');machine:exit()end
end)
emu.register_stop(function()log('RESULT','normal_callback=true');for _,tap in ipairs(taps)do tap:remove()end end)
