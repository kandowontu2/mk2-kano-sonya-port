-- One unchanged physical pressure controller. Missing stock effect metadata
-- only: native allocator/task lists, palette sources, FIFO and DMA tuples.
dofile('mk2ks_native_selector_sonya_cpu_pressure_bound.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial,armed=0,0,false
local taps={}
local function log(kind,value)
 serial=serial+1
 print(string.format('MK2_EFFECT_%s frame=%d sequence=%d %s writes=0 assistance=none',kind,frame,serial,value))
end
local function object(a)return a>=0x0102d6f0 and a<0x0105b950 and(a-0x0102d6f0)%0x210==0 end
local function main(a)return a>=0x01068ea0 and a<=0x01068ea0+168*0x6f0 and(a-0x01068ea0)%0x6f0==0 end
local function task(m)
 if not main(m)then return 'type=0000 owner=00000000 resume=00000000' end
 return string.format('type=%04X owner=%08X resume=%08X',p:read_u16(m+0x20),p:read_u32(m+0xc0),p:read_u32(m+0xe0))
end
local function chain(head,is_main,free)
 local a=p:read_u32(head);local nodes,seen={},{}
 local valid=true
 while a~=0 do
  if not is_main and free and(a==0x0105b950 or(a==0x00fe0190 and nodes[#nodes]==0x0105b740))then break end
  if seen[a]or #nodes>=358 or not(is_main and main(a)or not is_main and object(a))then valid=false;break end
  seen[a]=true;nodes[#nodes+1]=a;a=p:read_u32(a)
 end
 return nodes,a,valid
end
for _,head in ipairs({0x01060130,0x01068e50})do
 taps[#taps+1]=p:install_write_tap(head,head+31,'native effect allocator stores',function(at,data,mask)
  local shift=at-head;local before=p:read_u32(head)
  local merged=((before&(~(mask<<shift)))|((data&mask)<<shift))&0xffffffff
  local target=cpu.A0.value;local m=cpu.A13.value
  log('HEAD',string.format('head=%08X at=%08X before=%08X value=%04X mask=%04X merged=%08X target=%08X targetNext=%08X a2=%08X actor=%08X main=%08X pc=%08X returnPC=%08X %s',
   head,at,before,data,mask,merged,target,(object(target)or main(target))and p:read_u32(target)or 0,cpu.A2.value,cpu.A8.value,m,cpu.PC.value,p:read_u32(cpu.SP.value),task(m)))
 end)
end
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'all original effects FIFO metadata',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not armed then return end
 local a=cpu.A0.value;if not object(a)then return end
 local bank=p:read_u16(a+0x140)&0x7f00
 local pal=0x0105bb30+(bank>>8)*64
 log('QUEUE',string.format('actor=%08X cursor=%08X source=%08X cache=%08X pose=%08X id=%d body=%04X facing=%04X bank=%04X palette_source=%08X refs=%d size=%08X xy=%08X command=%08X world=%08X camera=%08X display=%08X pc=%08X',
  a,cpu.A1.value,cpu.A11.value,p:read_u32(a+0x1a0),p:read_u32(a+0x1d0),p:read_u16(a+0x1f0),p:read_u16(a+0x160),p:read_u16(a+0xf0),bank,p:read_u32(pal),p:read_u16(pal+32),cpu.A9.value,cpu.A10.value,cpu.A12.value,
  ((p:read_i16(a+0xb0)&65535)<<16)|(p:read_i16(a+0x90)&65535),cpu.A4.value,cpu.A5.value,cpu.PC.value))
end)
local dma
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
end end
assert(dma)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'all stock effects DMA tuples',function(at,data,mask)
 if not armed then return end
 local reg=mapping[(((dma:read(15)or 0)>>5)&1)+1][(at-0x01a80000)//16]
 local merged=(dma:read(reg)&(~mask))|(data&mask)
 if reg~=1 or merged&0x8000==0 then return end
 local r={};for i=0,17 do r[i]=dma:read(i)end;r[1]=merged
 log('DMA',string.format('cursor=%08X source=%08X command=%04X bank=%04X x=%d y=%d width=%d height=%d scaleX=%d scaleY=%d left=%d right=%d top=%d bottom=%d skip=%d pc=%08X',
  cpu.B14.value+192,r[2]|(r[3]<<16),r[1],r[8]&0x7f00,r[4]&1023,r[5]&511,r[6]&1023,r[7]&1023,r[10],r[11],r[16],r[17],r[12],r[13],r[0],cpu.PC.value))
end)
emu.register_frame(function()
 frame=frame+1
 if not armed and p:read_u16(0x010601d0)==2 then armed=true;log('BEGIN','mode=2')end
end)
emu.register_frame_done(function()
 if not armed then return end
 local oa,stopa,oka=chain(0x0105d480,false,false)
 local of,stopf,okf=chain(0x01060130,false,true)
 local ma,stopm,okm=chain(0x01068e30,true,false)
 local mf,stopmf,okmf=chain(0x01068e50,true,true)
 local function addresses(list)local result={};for _,v in ipairs(list)do result[#result+1]=string.format('%08X',v)end;return #result>0 and table.concat(result,',')or'-' end
 log('LISTS',string.format('mode=%d p1=%08X p2=%08X active=%s free=%s activeStop=%08X freeStop=%08X activeOK=%d freeOK=%d mains=%s mainFree=%s mainStop=%08X mainFreeStop=%08X mainOK=%d mainFreeOK=%d',
  p:read_u16(0x010601d0),p:read_u32(0x01060220),p:read_u32(0x01060df0),addresses(oa),addresses(of),stopa,stopf,oka and 1 or 0,okf and 1 or 0,addresses(ma),addresses(mf),stopm,stopmf,okm and 1 or 0,okmf and 1 or 0))
 for _,m in ipairs(ma)do
  log('TASK',string.format('main=%08X next=%08X %s count=%d attached=%08X parent=%08X action=%04X',
   m,p:read_u32(m),task(m),p:read_u16(m+0x30),p:read_u32(m+0x190),p:read_u32(m+0x230),p:read_u16(m+0x1f0)))
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('armed=%d terminalFrame=%d',armed and 1 or 0,frame))
 for _,tap in ipairs(taps)do tap:remove()end
end)
