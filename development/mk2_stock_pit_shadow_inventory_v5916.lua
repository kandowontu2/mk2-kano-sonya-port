-- Genuine original mk2 control: Cage2 versus Baraka3, earned paid arena rotation.
-- No ROM/RAM/register/position/health/arena writes, no imported-character proxy.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_native_stage_performer_v806.lua','rb'))
local source=f:read('*a');f:close();source=source:gsub('\r\n','\n')
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Exactly one controller edit: '..before)
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local id=assert(({kano=17,sonya=18})[winner]);local victim_id=id==17 and 18 or 17',
 'local id=assert(({cage=2})[winner]);local victim_id=3')
replace('local adjacent={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}',
 'local adjacent={Left=0xff898000,Right=0xff8980c0,Down=0xff897f40}')
replace('if next_id<=18 and not seen[next_id]then','if next_id<=11 and not seen[next_id]then')
replace('p:read_u16(slots[n].roster)<=18','p:read_u16(slots[n].roster)<=11')
replace("screen:snapshot('selection_match'..(match+1)..'_p'..n..'.png')",'-- Snapshot sink omitted; no new raster files.')
replace("if age<=600 and age%20==0 then screen:snapshot('stage_age'..age..'.png')end",
 '-- Stage snapshot sink omitted; no new raster files.')
replace('if arena==target_arena then','if false then -- Ordinary-arena inventory, never send port stage commands.')
replace("local f=assert(io.open(assert(os.getenv('MK2KS_STAGE_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 "local hex={};for i=1,#raw do hex[i]=string.format('%02X',raw:byte(i))end;print('MK2_STOCK_PIT_GUEST bytes='..#raw..' hex='..table.concat(hex))")
assert(load(source,'@whole806_stock_Cage2_Baraka3_native_tables_ordinary_controls_no_snapshots','t',_ENV))()

local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,first,terminal=0,nil,false
local fields={0x01060220,0x01060df0}
local mains={0x01060260,0x01060e30}
local states={0x010601f0,0x01060dc0}
local hps={0x010602f0,0x01060ec0}
local dma,taps=nil,{}
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
end end
assert(dma)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local stats={}
local function log(tag,value)
 print('MK2_STOCK_PIT_'..tag..' frame='..frame..' writes=0 assistance=none '..value)
end
local function counter(key)
 stats[key]=stats[key]or{entries=0,components=0,copies=0,all_mode8=0}
 return stats[key]
end
local function scope()
 return p:read_u16(0x010601d0)==2 and p:read_u16(states[1])==1 and p:read_u16(states[2])==1
end
for _,address in ipairs({0xff801070,0xff8012b0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'original stock shadow execution inventory',function(at,data,mask)
  if not scope()or at~=address or cpu.PC.value~=at+16 then return end
  local slot=0
  if address==0xff801070 then
   for n=1,2 do if cpu.A8.value==p:read_u32(fields[n])then slot=n end end
  else
   for n=1,2 do local a=p:read_u32(fields[n]);if valid(a)then
    local cache=p:read_u32(a+0x1a0);local row=cpu.A9.value
    if row>=cache and row<cache+112*12 and(row-cache)%112==0 then slot=n end
   end end
  end
  local item=counter(slot)
  if address==0xff801070 then item.entries=item.entries+1 else item.components=item.components+1 end
  if not item.first_entry then item.first_entry=at;item.op=data;item.mask=mask;item.pc=cpu.PC.value;item.b7=cpu.B7.value end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'every stock mode8 shadow DMA before handler',function(at,data,mask)
 if not scope()then return end
 local bank=((dma:read(15)or 0)>>5)&1;local reg=mapping[bank+1][(at-0x01a80000)//16]
 if reg~=1 then return end
 local command=(dma:read(1)&(~mask))|(data&mask)
 if command&0x8000==0 or command&15~=8 then return end
 local slot=0;local row=cpu.A9.value
 for n=1,2 do local a=p:read_u32(fields[n]);if valid(a)then
  local cache=p:read_u32(a+0x1a0)
  if row>=cache and row<cache+112*12 and(row-cache)%112==0 then slot=n end
 end end
 local item=counter(slot);item.all_mode8=item.all_mode8+1
 local pc=cpu.PC.value
 if pc==0xff8015a0 or pc==0xff801610 then item.copies=item.copies+1 end
 if not item.first_source then
  item.first_source=dma:read(2)|(dma:read(3)<<16);item.first_command=command
  item.first_pc=pc;item.first_width=dma:read(6)&0x3ff;item.first_height=dma:read(7)&0x3ff
 end
end)
emu.register_frame(function()frame=frame+1;stats={}end)
emu.register_frame_done(function()
 local arena,mode=p:read_u16(0x01061ac0),p:read_u16(0x010601d0)
 if scope()then
  local a1,a2=p:read_u32(fields[1]),p:read_u32(fields[2])
  if valid(a1)and valid(a2)and p:read_u16(a1+0x1f0)==2 and p:read_u16(a2+0x1f0)==3 then
   if arena==6 and not first then
    assert(p:read_u16(hps[1])==161 and p:read_u16(hps[2])==161,'Start genuine full-health stock Pit match')
    first=frame;log('PIT_START','arena=6 mode=2 ids=2,3 health=161,161')
   end
   -- Full field inventory throughout normal play; counts include every native row.
   for n=0,2 do
    local item=counter(n);local a=n>0 and p:read_u32(fields[n])or 0;local m=n>0 and p:read_u32(mains[n])or 0
    log('FIELD',string.format('arena=%d mode=%d slot=%d actor=%08X main=%08X owner=%08X id=%d body=%04X cache=%08X pose=%08X floor=%d y=%d stageY=%d hp=%d entries=%d components=%d copies=%d mode8=%d entry=%08X opcode=%04X mask=%04X entry_pc=%08X b7=%08X first_source=%08X first_command=%04X first_pc=%08X first_width=%d first_height=%d',
     arena,mode,n,a,m,valid(m)and p:read_u32(m+0xc0)or 0,valid(a)and p:read_u16(a+0x1f0)or -1,
     valid(a)and p:read_u16(a+0x160)or 0,valid(a)and p:read_u32(a+0x1a0)or 0,valid(a)and p:read_u32(a+0x1d0)or 0,
     valid(m)and p:read_i16(m+0x200)or 0,valid(a)and p:read_i16(a+0xb0)or 0,p:read_i16(0x0105ecd0),n>0 and p:read_u16(hps[n])or -1,
     item.entries,item.components,item.copies,item.all_mode8,item.first_entry or 0,item.op or 0,item.mask or 0,item.pc or 0,item.b7 or 0,
     item.first_source or 0,item.first_command or 0,item.first_pc or 0,item.first_width or 0,item.first_height or 0))
   end
  end
 end
 if first and frame>=first+300 then
  terminal=true;log('COMPLETE','first='..first..' age='..(frame-first)..' arena='..arena..' mode='..mode..' scope=ordinary_stock_Pit_shadow_execution_not_cinematic_or_RGB')
  manager.machine:exit()
 elseif manager.machine.time:as_double()>=890 then
  log('DEADLINE','terminal_acceptance=false');manager.machine:exit()
 end
end)
emu.register_stop(function()
 log('STOP','first='..(first or -1)..' completed='..tostring(terminal))
 for _,tap in ipairs(taps)do tap:remove()end
end)
