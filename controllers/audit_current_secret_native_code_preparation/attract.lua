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
 do local at=0xffa19fd0;local words={0x09e3,0x01f0,0x0106,0x4c0e,0xca03,0x09e3,0x0dc0,0x0106,0x8463,0x0b43,0xfffe,0xcb00,0x0255,0x05a0,0x01d0,0x0106,0x0b40,0xfffd,0xcb00,0x024e,0x05a0,0x1ac0,0x0106,0x0b40,0xfff8,0xcb00,0x0247,0x05a0,0x1cc0,0x0106,0x05a1,0xd090,0x0105,0x4401,0x0381,0x0b41,0xffbf,0xc300,0x023b,0x07a0,0x0000,0x0160,0x03e0,0x4dce,0xca04,0x1ec0,0xcb05,0xc000,0x0231,0x1fc0,0xca00,0x022e,0x09af,0x0001,0x09c0,0x0029,0x0d5f,0xc0c0,0xffa4,0x09c0,0x000e,0xb00d,0x0120,0xb1cd,0x0100,0x09c0,0x0003,0xb00d,0x0020,0x09c0,0x000f,0x0580,0x01d0,0x0106,0x5600,0x0580,0x0300,0x0106,0x0580,0x0ed0,0x0106,0x1820,0x0580,0x1cb0,0x0106,0x09e8,0xc600,0xffa1,0x4dce,0xca03,0x09e8,0xc790,0xffa1,0x0147,0x0b07,0x0060,0xa2ec,0xc080,0xea80,0xffa2}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do local at=0xffa1bda0;local words={0x09e5,0x0dc0,0x0106,0x09e6,0x0e50,0x0106,0xb5a0,0x0100,0x4c00,0xca06,0x09e5,0x01f0,0x0106,0x09e6,0x0280,0x0106,0x5621,0x84a3,0x8025,0x098c,0x1400,0x5600,0x0580,0x0310,0x0106,0x0580,0x0ee0,0x0106,0x0580,0x1af0,0x0106,0x0580,0x1c70,0x0106,0xb5a0,0x0120,0x8006,0x0d5f,0xf410,0xff83,0x0147,0x0b07,0x0060,0xa2ec,0xc080,0x9790,0xff81,0x0147,0x0b07,0x0060,0xa2ec,0xc080,0xa2c0,0xff81,0x0d5f,0x7090,0xff82,0x0d5f,0xa020,0xff82,0x1820,0x0580,0x1a90,0x0106,0x0147,0x0b07,0x0060,0xa2ec,0xc080,0x0340,0xff82,0x05a0,0x0310,0x0106,0x05a1,0x0ee0,0x0106,0x1842,0x0d5f,0xa170,0xff83,0xcbd3,0x09ac,0x0028,0x8065,0x09e2,0xd4a0,0x0105,0x0d5f,0x0310,0xff84,0x09e8,0xc920,0xffa1,0x0147,0x0b07,0x0060,0xa2ec,0xc080,0xea80,0xffa2,0x09c3,0x0033,0x0d5f,0x3ba0,0xffa1,0x09c0,0x0080,0x0d5f,0xdcc0,0xff80,0x0d5f,0xf520,0xff83,0x0d5f,0x9b50,0xff83,0x09c0,0x0040,0x0d5f,0xdcc0,0xff80,0x1900,0x0580,0x1ac0,0x0106,0x5600,0x0580,0x1af0,0x0106,0xc080,0x8b30,0xff81}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do local at=0xffa0ba10;local words={0x05a0,0x1ac0,0x0106,0x0b40,0xfff6,0xca80,0xde20,0xff80,0x05a0,0xd090,0x0105,0x0580,0x1cc0,0x0106}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do local at=0xff836650;local words={0x4cc7,0x24a6,0x0b26,0x6be0,0xff83,0x96c6,0x84c1,0x4541,0xcf01,0x5621,0x8026,0xc133,0x0de0,0x0960,0x24a2,0x0b22}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do local at=0xff8258b0;local words={0x0106,0x0000,0x0000,0x09c0,0x00a1,0x0580,0x02f0,0x0106,0x0580,0x0ec0,0x0106,0x0580,0xe500,0x0105,0x0580}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do local at=0xff9decb0;local words={0x0580,0x02f0,0x0106,0x0580,0x0ec0,0x0106,0x5600,0x0580,0xe500,0x0105,0x0580,0xe440,0x0105,0x188a,0x0d3f,0x0010,0x09c0,0x0001,0x0d5f,0xdcc0,0xff80,0x104a,0x0b4a,0xff5e,0xc8f5,0x09ca,0x00a1,0x0d3f,0x0003,0xc080,0xde20,0xff80,0x058a,0xe500,0x0105,0x058a,0xe440,0x0105,0x058a,0x02f0,0x0106,0x058a,0x0ec0,0x0106,0x0960,0x4d0b,0x5600}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do local at=0xff9037c0;local words={0xca14,0x09fa,0x4ee0}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do local at=0xff904ee0;local words={0x4d42,0x4e71,0x4f35,0x2fc5,0xc902,0x9a22,0x5001,0x9a22,0x5001,0x9a22,0x5001,0x3ca5,0x0bea,0xefff,0x4e23,0x4535,0x4935,0xc501,0x0960,0xc0ec}
 local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
 do
 local site=0xff829c10;local target=0xffff0000
 assert(p:read_u16(site)==0xc080 and p:read_u32(site+16)==target)
 local words={0x0b43,0xffef,0xca06,0x0b43,0xffed,0xca03,0xc080,0x9c70,0xff82,0xc080,0x9c40,0xff82};local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(target+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_PREDICATE',string.format('site=%08X target=%08X words=%d mismatches=%d',site,target,#words,mismatches))
 assert(mismatches==0)
 end
 do
 local site=0xff8d9580;local target=0xffff0100
 assert(p:read_u16(site)==0xc080 and p:read_u32(site+16)==target)
 local words={0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x95e0,0xff8d,0xc080,0x95b0,0xff8d};local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(target+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_PREDICATE',string.format('site=%08X target=%08X words=%d mismatches=%d',site,target,#words,mismatches))
 assert(mismatches==0)
 end
 do
 local site=0xffa122a0;local target=0xffff0200
 assert(p:read_u16(site)==0xc080 and p:read_u32(site+16)==target)
 local words={0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x22d0,0xffa1,0xc080,0x23b0,0xffa1};local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(target+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_PREDICATE',string.format('site=%08X target=%08X words=%d mismatches=%d',site,target,#words,mismatches))
 assert(mismatches==0)
 end
end)
