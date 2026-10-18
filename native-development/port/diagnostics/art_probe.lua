-- Physical inputs, read-only object observations. No guest-memory writes.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local sys
for _,port in pairs(m.ioport.ports) do if port.fields['Coin 1'] then sys=port.fields end end
assert(sys)
local k=assert(tonumber(os.getenv('KS_ART_KANO_PTR')))
local s=assert(tonumber(os.getenv('KS_ART_SONYA_PTR')))
local log=assert(io.open('art_objects.csv','w'))
log:write('frame,kobj,kid,kshape,sobj,sid,sshape\n')
local frame=0
local hi=m.ioport.ports[':IN0'].fields
local function u32(address)
 -- GSPA BSS symbols may be byte-aligned rather than DWORD-aligned on this
 -- bit-addressed CPU. Compose bytes rather than using an aligned bus read.
 local value=0
 for i=0,3 do value=value | (p:read_u8(address+i*8) << (i*8)) end
 return value
end
local function observe(address)
 local object=u32(address)
 if object<0x01000000 or object>=0x01400000 then return object,-1,0 end
 return object,p:read_u16(object+0x1f0),u32(object+0x1d0)
end
emu.register_frame_done(function()
 frame=frame+1
 sys['Coin 1']:set_value((frame>3000 and frame%600<6) and 1 or 0)
 sys['1 Player Start']:set_value((frame>3000 and frame%600>=60 and frame%600<66) and 1 or 0)
 hi['P1 High Punch']:set_value((frame>3000 and frame%120<4) and 1 or 0)
 -- Sample at a period coprime to the 5-tick rate and both pose-cycle lengths.
 if frame%29==0 then
  local ko,ki,kp=observe(k); local so,si,sp=observe(s)
  log:write(string.format('%d,%08x,%d,%08x,%08x,%d,%08x\n',frame,ko,ki,kp,so,si,sp)); log:flush()
 end
 if frame==3900 or frame==3930 or frame==4500 or frame==6000 then
  m.screens[':screen']:snapshot(string.format('art_%05d.png',frame))
 end
 if frame>=6600 then log:close(); m:exit() end
end)
