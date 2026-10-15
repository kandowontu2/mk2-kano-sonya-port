-- Whole genuine stock806 paid progression, Cage's original D,D,D+HK command.
-- Reuse the stock-table/no-snapshot/RAM-guest substitutions already executed5916.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2_stock_pit_shadow_inventory_v5916.lua','rb'))
local wrapper=f:read('*a');f:close();wrapper=wrapper:gsub('\r\n','\n')
local marker="assert(load(source,'@whole806_stock_Cage2_Baraka3_native_tables_ordinary_controls_no_snapshots','t',_ENV))()"
local at=assert(wrapper:find(marker,1,true));assert(not wrapper:find(marker,at+1,true))
wrapper=wrapper:sub(1,at-1)
local before="replace('if arena==target_arena then','if false then -- Ordinary-arena inventory, never send port stage commands.')"
local a,b=assert(wrapper:find(before,1,true));assert(not wrapper:find(before,b+1,true))
wrapper=wrapper:sub(1,a-1)..wrapper:sub(b+1)
wrapper=wrapper..[=[
replace([[if winner=='kano'then
      if age>=5 and age<35 then press(side,'Block')end
      if age>=10 and age<14 or age>=20 and age<24 then press(side,'Up')
      elseif age>=30 and age<34 then press(side,case=='wrong_command'and forward or back)
      elseif age>=40 and age<44 then press(side,'Low Kick')end
     else
      if age>=10 and age<14 or age>=20 and age<24 then press(side,forward)
      elseif age>=30 and age<34 then press(side,case=='wrong_command'and back or'Down')
      elseif age>=40 and age<44 then press(side,'High Punch')end
     end]],[[assert(winner=='cage'and case=='positive','Original Cage native stage command only')
     if age>=10 and age<14 or age>=20 and age<24 or age>=30 and age<34 then press(side,'Down')
     elseif age>=40 and age<44 then press(side,'High Kick')end]])
assert(load(source,'@whole806_stock_Cage2_Baraka3_native_DDD_HK_no_snapshots','t',_ENV))()
]=]
assert(load(wrapper,'@whole5916_stock_controller_prefix_only_Cage_original_stage_command','t',_ENV))()

local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,origin,complete,cine=0,nil,false,nil
local dma,taps,entries,copies,mode8=nil,{},0,0,0
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
end end
assert(dma)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print('MK2_STOCK_CINE_'..tag..' frame='..frame..' writes=0 assistance=none '..value)
end
emu.register_frame(function()frame=frame+1;entries=0;copies=0;mode8=0 end)
taps[#taps+1]=p:install_read_tap(0xff8bdde0,0xff8bddef,'original physically earned stock Pit stage entry',function(at,data,mask)
 if at~=0xff8bdde0 or cpu.PC.value~=at+16 then return end
 assert(not origin and p:read_u16(0x01061ac0)==6 and p:read_u16(cpu.A8.value+0x1f0)==2)
 origin=frame
 log('BEGIN',string.format('entry=%08X opcode=%04X mask=%04X pc=%08X actor=%08X main=%08X id=2 arena=6',at,data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
end)
for _,address in ipairs({0xff801070,0xff8012b0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'all original stock shadow entries and components',function(at,data,mask)
  if origin and at==address and cpu.PC.value==at+16 then
   entries=entries+1;log('SHADOW_ENTRY',string.format('entry=%08X opcode=%04X mask=%04X pc=%08X a8=%08X a9=%08X',at,data,mask,cpu.PC.value,cpu.A8.value,cpu.A9.value))
  end
 end)
end
taps[#taps+1]=p:install_write_tap(0x0105ebc0,0x0105ebcf,'original global shadow enable stores',function(at,data,mask)
 if not origin then return end
 log('ENABLE_STORE',string.format('at=%08X before=%04X value=%04X mask=%04X pc=%08X',at,p:read_u16(at),data,mask,cpu.PC.value))
end)
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'every original stock cinematic mode8 DMA before handler',function(at,data,mask)
 if not origin then return end
 local bank=((dma:read(15)or 0)>>5)&1;local reg=mapping[bank+1][(at-0x01a80000)//16]
 if reg~=1 then return end
 local command=(dma:read(1)&(~mask))|(data&mask)
 if command&0x8000==0 or command&15~=8 then return end
 mode8=mode8+1;local pc=cpu.PC.value
 if pc==0xff8015a0 or pc==0xff801610 then copies=copies+1 end
 log('MODE8',string.format('pc=%08X source=%08X command=%04X width=%d height=%d',pc,dma:read(2)|(dma:read(3)<<16),command,dma:read(6)&0x3ff,dma:read(7)&0x3ff))
end)
taps[#taps+1]=p:install_read_tap(0xff906ef0,0xff906eff,'original stock native cinematic constructor ancestry',function(at)
 if origin and at==0xff906ef0 and cpu.PC.value==at+16 then
  log('CONSTRUCTOR',string.format('entry=%08X pc=%08X a0=%08X a8=%08X a11=%08X a13=%08X',at,cpu.PC.value,cpu.A0.value,cpu.A8.value,cpu.A11.value,cpu.A13.value))
 end
end)
taps[#taps+1]=p:install_read_tap(0xff838790,0xff83879f,'actual original stock native Pit movie draw',function(at)
 if not origin or at~=0xff838790 or cpu.PC.value~=at+16 or p:read_u16(0x010601d0)~=9 then return end
 local a,m=cpu.A8.value,cpu.A13.value
 assert(valid(a)and valid(m)and p:read_u16(a+0x1f0)==3 and p:read_u32(m+0x140)==a)
 cine={actor=a,main=m}
 log('DRAW',string.format('entry=%08X pc=%08X actor=%08X main=%08X owner=%08X id=3 body=%04X group=%08X x=%d y=%d',at,cpu.PC.value,a,m,p:read_u32(m+0x140),p:read_u16(a+0x160),cpu.A0.value,p:read_i16(a+0x90),p:read_i16(a+0xb0)))
end)
emu.register_frame_done(function()
 if origin then
  local a1,a2=p:read_u32(0x01060220),p:read_u32(0x01060df0)
  local m1,m2=p:read_u32(0x01060260),p:read_u32(0x01060e30)
  log('FIELD',string.format('age=%d arena=%d mode=%d shadow_enable=%04X entries=%d copies=%d mode8=%d p1=%08X p2=%08X main1=%08X main2=%08X id1=%d id2=%d body1=%04X body2=%04X owner1=%08X owner2=%08X victim_y=%d cine_actor=%08X cine_main=%08X cine_owner=%08X cine_id=%d cine_body=%04X',
   frame-origin,p:read_u16(0x01061ac0),p:read_u16(0x010601d0),p:read_u16(0x0105ebc0),entries,copies,mode8,a1,a2,m1,m2,
   valid(a1)and p:read_u16(a1+0x1f0)or -1,valid(a2)and p:read_u16(a2+0x1f0)or -1,
   valid(a1)and p:read_u16(a1+0x160)or 0,valid(a2)and p:read_u16(a2+0x160)or 0,
   valid(m1)and p:read_u32(m1+0xc0)or 0,valid(m2)and p:read_u32(m2+0xc0)or 0,valid(a2)and p:read_i16(a2+0xb0)or 0,
   cine and cine.actor or 0,cine and cine.main or 0,cine and p:read_u32(cine.main+0x140)or 0,
   cine and p:read_u16(cine.actor+0x1f0)or -1,cine and p:read_u16(cine.actor+0x160)or 0))
  if frame-origin>=1100 then complete=true;log('COMPLETE','origin='..origin..' age='..(frame-origin)..' ordinary_control=false');manager.machine:exit()end
 end
 if manager.machine.time:as_double()>=890 then log('DEADLINE','terminal_acceptance=false');manager.machine:exit()end
end)
emu.register_stop(function()
 log('STOP','origin='..(origin or -1)..' completed='..tostring(complete))
 for _,tap in ipairs(taps)do tap:remove()end
end)
