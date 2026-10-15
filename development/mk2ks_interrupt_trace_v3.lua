-- Read-only paired interruption/retry instruction, health and actor observer.
return function(move,side,names,context)
 local p=manager.machine.devices[':maincpu'].spaces.program
 local cpu=manager.machine.devices[':maincpu'].state
 local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
  {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
 local taps={};local entries={ready=0xff861350,idle=0xff861500}
 if move=='blade'then entries.action=0xfff8cc00;entries.create=0xfff8d800;entries.strike=0xfff8e400
 elseif move=='bicycle'then entries.action=0xfff9a400;entries.strike=0xfff9ee00;entries.tick=0xfff9d000;entries.release=0xfff9e000
 elseif move=='leg'then entries.action=0xfff80800;entries.strike=0xfff83800
 else error('Unknown interruption move')end
 print(string.format('MK2_INTERRUPT_BOOT move=%s side=%d names=%s,%s writes=0',move,side,names[1],names[2]))
 local function valid(a)return a>=0x01000000 and a<0x01100000 end
 for kind,address in pairs(entries)do
  taps[#taps+1]=p:install_read_tap(address,address+15,'interruption native '..kind,function(at)
   local frame,phase,epoch=context()
   if not epoch or frame<epoch or(kind~='strike'and cpu.PC.value~=address+16) then return end
   for n,s in ipairs(slots)do
    local a,m=p:read_u32(s.actor),p:read_u32(s.main)
    if valid(a)and valid(m)and cpu.A8.value==a and cpu.A13.value==m then
     print(string.format('MK2_INTERRUPT_EVENT frame=%d phase=%d age=%d slot=%d kind=%s entry=%08X pc=%08X a8=%08X a13=%08X actor=%08X main=%08X id=%d owner=%08X writes=0',
      frame,phase,frame-epoch,n,kind,address,cpu.PC.value,cpu.A8.value,cpu.A13.value,a,m,p:read_u16(a+0x1f0),p:read_u32(m+0xc0)))
    end
   end
  end)
 end
 for n,s in ipairs(slots)do
  taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'interruption original health',function(at,data,mask)
   local frame,phase,epoch=context()
   if epoch and frame>=epoch then
    print(string.format('MK2_INTERRUPT_HEALTH frame=%d phase=%d age=%d slot=%d before=%d after=%d mask=%04X pc=%08X writes=0',
     frame,phase,frame-epoch,n,p:read_u16(s.hp),data&0xffff,mask,cpu.PC.value))
   end
  end)
 end
 local function field()
  local frame,phase,epoch=context()
  if not epoch or frame<epoch then return end
  for n,s in ipairs(slots)do
   local a,m=p:read_u32(s.actor),p:read_u32(s.main)
   assert(valid(a)and valid(m),'Actual interruption owner required')
   print(string.format('MK2_INTERRUPT_FIELD frame=%d phase=%d age=%d slot=%d mode=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d action=%04X pose=%08X x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X trail=%08X writes=0',
    frame,phase,frame-epoch,n,p:read_u16(0x010601d0),a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.id),p:read_u16(s.state),p:read_u16(s.hp),
    p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_i16(m+0x200),p:read_u32(a+0x40),p:read_u32(a+0x60),
    p:read_u32(a+0x20),p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u32(m+0x190)))
  end
 end
 emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
 return {field=field}
end




