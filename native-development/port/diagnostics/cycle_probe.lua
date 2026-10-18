-- Input-only controller and read-only observations for native source playback.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local hi=m.ioport.ports[':IN0'].fields
local sys
for _,port in pairs(m.ioport.ports) do if port.fields['Coin 1'] then sys=port.fields end end
assert(sys)
local k=assert(tonumber(os.getenv('KS_ART_KANO_PTR')))
local s=assert(tonumber(os.getenv('KS_ART_SONYA_PTR')))
local kt=assert(tonumber(os.getenv('KS_ART_KANO_STAGE')))
local st=assert(tonumber(os.getenv('KS_ART_SONYA_STAGE')))
local function u16(a) return p:read_u8(a)|(p:read_u8(a+8)<<8) end
local function u32(a) return u16(a)|(u16(a+16)<<16) end
local function observe(a)
 local object=u32(a)
 if object<0x01000000 or object>=0x01400000 then return object,-1,0 end
 return object,u16(object+0x1f0),u32(object+0x1d0)
end
local log=assert(io.open('cycle_objects.csv','w'))
log:write('frame,kobj,kid,kshape,kstage,sobj,sid,sshape,sstage,pc\n')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 sys['Coin 1']:set_value((frame>3000 and frame%600<6) and 1 or 0)
 sys['1 Player Start']:set_value((frame>3000 and frame%600>=60 and frame%600<66) and 1 or 0)
 hi['P1 High Punch']:set_value((frame>3000 and frame%120<4) and 1 or 0)
 if frame%17==0 then
  local ko,ki,kp=observe(k);local so,si,sp=observe(s)
  log:write(string.format('%d,%08x,%d,%08x,%d,%08x,%d,%08x,%d,%08x\n',frame,ko,ki,kp,u16(kt),so,si,sp,u16(st),m.devices[':maincpu'].state['PC'].value));log:flush()
 end
 if frame>=4000 and frame%1000==0 then m.screens[':screen']:snapshot(string.format('cycle_%05d.png',frame)) end
 if frame>=12000 then log:close();m:exit() end
end)
