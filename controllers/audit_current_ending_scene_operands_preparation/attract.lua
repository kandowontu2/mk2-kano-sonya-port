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
 if frame>=700 then log('BOUND','maximum_fields=700');machine:exit()end
end)
emu.register_stop(function()log('RESULT','normal_callback=true');for _,tap in ipairs(taps)do tap:remove()end end)

emu.register_frame_done(function()
 if frame~=600 then return end
 local copied=0
 for page=0,1 do
  local original=page==0 and 0xff8f5550 or 0xff8f59d0
  local relocated=0xff800000+(page==0 and 0xf4a00 or 0xf4b00)*8
  for index=0,35 do
   assert(p:read_u32(original+index*32)==p:read_u32(relocated+index*32))
   copied=copied+1
  end
  for fighter=0,1 do
   local id=17+fighter
   for segment=0,(page==0 and 2 or 1)do
    local ptr=p:read_u32(relocated+(id*3+segment)*32)
    local expected=0xff800000+(0xf4c00+(fighter*5+(page==0 and 0 or 3)+segment)*0xc0)*8
    assert(ptr==expected)
    local template=p:read_u32(original+(8*3+segment)*32)
    for byte=0,23 do assert(p:read_u8(ptr+byte*8)==p:read_u8(template+byte*8))end
    local hex=''
    for byte=0,167 do
     local value=p:read_u8(ptr+(24+byte)*8)
     if value==0 then break end
     hex=hex..string.format('%02X',value)
    end
    log('ENDING_SCRIPT',string.format('id=%d page=%d segment=%d ptr=%08X template=%08X header_exact=true texthex=%s',id,page,segment,ptr,template,hex))
   end
   if page==1 then assert(p:read_u32(relocated+(id*3+2)*32)==0)end
   local row=50+fighter*2+page
   local photo=p:read_u32(0xff800000+0xf4900*8+row*32)
   assert(photo>=0x07100000 and photo<0x07200000)
   log('ENDING_PHOTO',string.format('id=%d page=%d row=%d ptr=%08X',id,page,row,photo))
  end
 end
 log('ENDING_STOCK','preserved_pointers='..copied..' own_headers=10 page2_terminators=2')
end)

emu.register_frame_done(function()
 if frame~=600 then return end
 for _,row in ipairs({
  {0xff844700,0x0270},{0xff8448a0,0x0270},
  {0xff844720,0x0170},{0xff844970,0x0170},
  {0xff844740,0x0190},{0xff844ab0,0x0190},
  {0xff844760,0x01b0},{0xff844b40,0x01b0}})do
  local actual=p:read_u16(row[1]);assert(actual==row[2])
  log('ENDING_SCENE_WORD',string.format('at=%08X actual=%04X expected=%04X',row[1],actual,row[2]))
 end
 for _,row in ipairs({
  {0xff8f51c0,0xff800000+0xf4a00*8},
  {0xff8f53e0,0xff800000+0xf4b00*8},
  {0xff8447b0,0xff800000+0xf4900*8}})do
  local actual=p:read_u32(row[1]);assert(actual==row[2])
  log('ENDING_SCENE_TABLE',string.format('at=%08X actual=%08X expected=%08X',row[1],actual,row[2]))
 end
 local count=0
 for index=0,40 do
  assert(p:read_u32(0xff8f48f0+index*32)==p:read_u32(0xff800000+0xf4900*8+index*32))
  count=count+1
 end
 log('ENDING_SCENE_STOCK','picture_rows_preserved='..count)
end)
