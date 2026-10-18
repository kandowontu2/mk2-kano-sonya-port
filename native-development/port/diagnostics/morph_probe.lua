-- Physical selection/commands only; all guest-memory access is read-only.
local m=manager.machine
local cpu=m.devices[':maincpu']
local p=cpu.spaces.program
local hi={}
local mirror=os.getenv('KS_MORPH_MIRROR')=='1'
local specials=os.getenv('KS_MORPH_SPECIALS')=='1'
local ball=os.getenv('KS_MORPH_BALL')=='1'
local melee=os.getenv('KS_MORPH_MELEE')=='1'
local grapples=os.getenv('KS_MORPH_GRAPPLES')=='1'
local square=os.getenv('KS_MORPH_SQUARE')=='1'
local throws=os.getenv('KS_MORPH_THROWS')=='1'
local lateThrow=os.getenv('KS_MORPH_LATE_THROW')=='1'
local thrown={}
local morphPoses={}
local morphLastShape=0
local morphPending={}
for value in (os.getenv('KS_MORPH_POSES') or ''):gmatch('[^,]+') do morphPoses[assert(tonumber(value))]=true end
for _,port in pairs(m.ioport.ports) do
 for name,field in pairs(port.fields) do
  local normalized=name
  if mirror then
   if name:sub(1,2)=='P1' then normalized='P2'..name:sub(3)
   elseif name:sub(1,2)=='P2' then normalized='P1'..name:sub(3) end
  end
  hi[normalized]=field
 end
end
local sys
for _,port in pairs(m.ioport.ports) do
 if port.fields['Coin 1'] then sys=port.fields;break end
end
assert(sys)
local function u32(a)
 local v=0
 for i=0,3 do v=v|(p:read_u8(a+i*8)<<(i*8)) end
 return v
end
local function u16(a) return p:read_u8(a)|(p:read_u8(a+8)<<8) end
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local ground=assert(tonumber(os.getenv('KS_GROUND_Y')))
local log=assert(io.open('morph.csv','w'))
local artLog=assert(io.open('morph_art.csv','w'))
artLog:write('frame,fight,character,action,shape,palette,flags,y,ground\n')
-- P1/P2 columns are normalized actor/opponent roles when mirror is enabled.
log:write('frame,fight,pc,mode,p1selected,p2selected,p1char,p2char,p1shape,p1x,p1y,missing,action,victimHP,victimAction\n')
local n,selection,fight=0,0,0
local locked=false
emu.register_frame_done(function()
 n=n+1
 for _,name in ipairs({'P1 High Punch','P1 Low Punch','P1 High Kick','P1 Low Kick','P1 Block',
 'P1 Left','P1 Right','P1 Up','P1 Down','P2 High Punch','P2 Left','P2 Right','P2 Down','P2 Up'}) do hi[name]:set_value(0) end
 for _,name in ipairs({'Coin 1','Coin 2','1 Player Start','2 Players Start','2 Player Start'}) do
  if sys[name] then sys[name]:set_value(0) end
 end
 local mode=u16(0x010601d0)
 local c1,c2=u16(0x01060280),u16(0x01060e50)
 if mirror then c1,c2=c2,c1 end
 if n>3000 and selection==0 then
  sys['Coin 1']:set_value(n%600<6 and 1 or 0)
  if sys['Coin 2'] then sys['Coin 2']:set_value(n%600<6 and 1 or 0) end
  sys['1 Player Start']:set_value(n%600>=60 and n%600<66 and 1 or 0)
  hi['P1 High Punch']:set_value(n%40<4 and 1 or 0)
 end
 if mode==4 and not locked then
  selection=selection+1
  local start2=sys['2 Players Start'] or sys['2 Player Start']
  if selection<160 and start2 then start2:set_value(selection%30<5 and 1 or 0) end
  if selection<120 then sys['Coin 1']:set_value(selection%30<5 and 1 or 0) end
  if selection>50 and selection%30<5 then
   if c1==1 then hi['P1 Right']:set_value(1)
   elseif c1==0 then hi['P1 Down']:set_value(1)
   elseif c1==9 or c1==2 then hi['P1 Left']:set_value(1) end
   if c2==1 or c2==0 or c2==2 or c2==9 then hi['P2 Right']:set_value(1) end
  end
  if selection>160 and c1==6 and c2==18 then
   hi['P1 High Punch']:set_value(1);hi['P2 High Punch']:set_value(1);locked=true
  end
 end
 local a,b=u32(0x01060220),u32(0x01060df0)
 local proc=u32(mirror and 0x01060e30 or 0x01060260)
 if mirror then a,b=b,a end
 if mode==2 and locked then
  fight=fight+1
  -- Away/down/away + LK, then wait beyond native 512-field morph lifetime.
  local away=mirror and 'P1 Right' or 'P1 Left'
  local toward=mirror and 'P1 Left' or 'P1 Right'
  if fight>=100 and fight<106 or fight>=120 and fight<126 then hi[away]:set_value(1) end
  if fight>=110 and fight<116 then hi['P1 Down']:set_value(1) end
  if fight>=130 and fight<134 then hi['P1 Low Kick']:set_value(1) end
  -- Down + LP + Block, in both physical button orders on separate attempts.
  if fight>=1000 and fight<1012 or fight>=1900 and fight<1912 then hi['P1 Down']:set_value(1) end
  if fight>=1002 and fight<1012 or fight>=1906 and fight<1912 then hi['P1 Low Punch']:set_value(1) end
  if fight>=1006 and fight<1012 or fight>=1902 and fight<1912 then hi['P1 Block']:set_value(1) end
  if specials then
   if fight>=250 and fight<256 or fight>=1150 and fight<1156 then hi['P1 Down']:set_value(1) end
   if fight>=260 and fight<266 then hi[away]:set_value(1) end
   if fight>=270 and fight<274 then hi['P1 High Punch']:set_value(1) end
   if fight>=1160 and fight<1166 then hi[toward]:set_value(1) end
   if fight>=1170 and fight<1174 then hi['P1 Low Punch']:set_value(1) end
  end
  if ball and fight>=250 and fight<350 then hi['P1 Low Kick']:set_value(1) end
  if square then
   if fight>=1230 and fight<1234 then hi['P2 Up']:set_value(1) end
   if fight>=1100 and fight<1103 or fight>=1236 and fight<1239 then hi[toward]:set_value(1) end
   if fight>=1106 and fight<1109 or fight>=1242 and fight<1245 then hi[away]:set_value(1) end
   if fight>=1112 and fight<1116 or fight>=1246 and fight<1250 then hi['P1 High Punch']:set_value(1) end
  end
  if grapples then
   if a~=0 and b~=0 and ((fight>=180 and fight<300) or (fight>=1040 and fight<1140)) and math.abs(u16(a+0x90)-u16(b+0x90))>56 then hi[toward]:set_value(1) end
   if fight>=310 and fight<316 then hi['P1 Down']:set_value(1) end
   if fight>=320 and fight<326 then hi[toward]:set_value(1) end
   if fight>=330 and fight<334 then hi['P1 Low Punch']:set_value(1) end
   if fight>=1150 and fight<1164 then hi['P1 Down']:set_value(1);hi['P1 Block']:set_value(1) end
   if fight>=1154 and fight<1164 then hi['P1 Low Punch']:set_value(1) end
  end
  if melee then
   if a~=0 and b~=0 and fight>=180 and fight<300 and math.abs(u16(a+0x90)-u16(b+0x90))>84 then hi[toward]:set_value(1) end
   if a~=0 and b~=0 and fight>=1040 and fight<1095 and math.abs(u16(a+0x90)-u16(b+0x90))>64 then hi[toward]:set_value(1) end
   if fight>=310 and fight<316 or fight>=1120 and fight<1123 then hi['P1 Down']:set_value(1) end
   if fight>=320 and fight<326 then hi[toward]:set_value(1) end
   if fight>=330 and fight<334 then hi['P1 High Punch']:set_value(1) end
   if fight>=1100 and fight<1103 or fight>=1110 and fight<1113 then hi[away]:set_value(1) end
   if fight>=1126 and fight<1130 then hi['P1 High Kick']:set_value(1) end
  end
  if throws and a~=0 and b~=0 then
   local identity=u16(a+0x1f0)
   local action=proc~=0 and u16(proc+0x1f0) or 0
   if action==0x507 then thrown[identity]=true end
   if (identity==17 or identity==18) and not thrown[identity] and
      (fight>=220 and fight<(lateThrow and 672 or 600) or fight>=1100 and fight<(lateThrow and 1548 or 1480)) then
    local x1,x2=u16(a+0x90),u16(b+0x90)
    hi[x1<x2 and 'P1 Right' or 'P1 Left']:set_value(1)
    local ready=not lateThrow or (identity==17 and fight>=650) or (identity==18 and fight>=1525)
    if ready and math.abs(x1-x2)<=64 then hi['P1 Low Punch']:set_value(fight%20<4 and 1 or 0) end
   end
  end
  if fight==190 or fight==1060 or fight==1960 then m.screens[':screen']:snapshot(string.format('morph_%05d.png',fight)) end
 end
 local char1=a~=0 and u16(a+0x1f0) or -1
 if a~=0 and mode==2 and locked then
  local shape=u32(a+0x1d0)
  if morphPoses[shape] then
   if shape~=morphLastShape then morphPending[n+2]=shape end
   artLog:write(string.format('%d,%d,%d,%d,%08x,%d,%d,%d,%d\n',n,fight,char1,u16(proc+0x1f0),shape,u16(a+0x140),u16(a+0xf0),u16(a+0xb0),u16(ground)))
   artLog:flush()
  end
  morphLastShape=shape
 end
 if morphPending[n] then m.screens[':screen']:snapshot(string.format('morph_pose_%08x_%05d.png',morphPending[n],n));morphPending[n]=nil end
 local char2=b~=0 and u16(b+0x1f0) or -1
 local victimProc=u32(mirror and 0x01060260 or 0x01060e30)
 log:write(string.format('%d,%d,%08x,%d,%d,%d,%d,%d,%08x,%d,%d,%d,%d,%d,%d\n',n,fight,cpu.state['PC'].value,mode,c1,c2,char1,char2,a~=0 and u32(a+0x1d0) or 0,a~=0 and u16(a+0x90) or 0,a~=0 and u16(a+0xb0) or 0,u32(missing),proc~=0 and u16(proc+0x1f0) or 0,u16(mirror and 0x010602f0 or 0x01060ec0),victimProc~=0 and u16(victimProc+0x1f0) or 0))
 if n%120==0 then log:flush() end
 if cpu.state['PC'].value==recovery then
  local fault=assert(io.open('morph_fault.txt','w'));fault:write('Native recovery PC reached\n');fault:close();log:close();m:exit()
 elseif n>=9000 then artLog:close();log:close();m:exit() end
end)
