
local machine=manager.machine
local p=machine.devices[':maincpu'].spaces.program
local frame=0
local function addr(offset)return 0xff800000+offset*8 end
local inserts={{0,5},{0,7},{2,8},{3,9},{1,6},{0,8}}
emu.register_frame(function()
 frame=frame+1
 if frame==600 then
  assert(p:read_u32(0xff8a11f0)==addr(0xf4580))
  assert(p:read_u32(0xff8a05c0)==addr(0xf4740))
  assert(p:read_u32(0xff8a0df0)==addr(0xf4780))
  for order=0,5 do
   local original=p:read_u32(0xff8a1260+order*32)
   local actual=p:read_u32(addr(0xf4580)+order*32)
   assert(actual==addr(0xf4600+order*0x30))
   local old_index,kano,sonya=0,0,0
   local ids={}
   for slot=0,12 do
    local id=p:read_u16(actual+slot*16)
    local expected
    if slot==inserts[order+1][1]then expected=order%2==1 and 18 or 17
    elseif slot==inserts[order+1][2]then expected=order%2==1 and 17 or 18
    else expected=p:read_u16(original+old_index*16);old_index=old_index+1 end
    assert(id==expected)
    if id==17 then kano=kano+1 elseif id==18 then sonya=sonya+1 end
    ids[#ids+1]=tostring(id)
   end
   assert(old_index==11 and kano==1 and sonya==1)
   for tail=0,4 do
    local id=p:read_u16(actual+(13+tail)*16)
    assert(id==p:read_u16(original+(11+tail)*16))
    ids[#ids+1]=tostring(id)
   end
   print('MK2_LADDER_TABLE order='..order..' ids='..table.concat(ids,',')..' original_regular_preserved=11 boss_tail_preserved=5 writes=0 assistance=none')
  end
  for slot=0,15 do
   local position=p:read_u16(addr(0xf4740)+slot*16)
   assert(position==940-math.floor((754*slot+7)/15))
   if slot>0 then
    local previous=p:read_u16(addr(0xf4740)+(slot-1)*16)
    assert(previous-position>=49)
   end
  end
  print('MK2_LADDER_GEOMETRY positions=16 minimum_frame_height=49 writes=0 assistance=none')
 end
 if frame>=700 then print('MK2_LADDER_RESULT frame=700 writes=0 assistance=none');machine:exit()end
end)
