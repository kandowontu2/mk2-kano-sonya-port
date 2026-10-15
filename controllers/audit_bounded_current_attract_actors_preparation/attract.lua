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

local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame_done(function()
 if p:read_u16(0x010601d0)~=1 then return end
 local r1,r2=p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)
 if r1~=17 and r1~=18 and r2~=17 and r2~=18 then return end
 for n,s in ipairs(slots)do
  local a,m=p:read_u32(s.actor),p:read_u32(s.main)
  if valid(a)and valid(m)then
   log('DEMO_ACTOR',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d pose=%08X y=%d floor=%d',
    n,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.roster),p:read_u16(s.state),p:read_u16(s.hp),p:read_u32(a+0x1d0),p:read_i16(a+0xb0),p:read_i16(m+0x200)))
  else log('DEMO_MISSING',string.format('slot=%d actor=%08X main=%08X roster=%d',n,a,m,p:read_u16(s.roster)))end
 end
end)
