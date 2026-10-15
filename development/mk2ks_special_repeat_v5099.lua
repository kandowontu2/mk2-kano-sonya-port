-- Cold real two-human selection, two physical special cycles and ordinary follow-up.
-- No guest writes or forced CPU/health/position/RNG. This is a diagnostic,
-- not complete native choreography/pixels/victim/CPU/finisher acceptance.
local move=assert(os.getenv('MK2KS_HUMAN_SPECIAL_MOVE'))
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local air=os.getenv('MK2KS_HUMAN_SPECIAL_AIR')=='1';assert(not air or move=='square')
local specs={knife={17,0xffffb000},ball={17,0xffffde00},blade={17,0xfff8cc00},choke={17,0xfff91400},
 ring={18,0xffffb400},square={18,0xffffca00},bicycle={18,0xfff9a400},leg={18,0xfff80800}}
local spec=assert(specs[move]);assert(side==1 or side==2)
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX',
 'MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
 assert(not os.getenv(key),'Unassisted observer refuses '..key)
end
local p=manager.machine.devices[':maincpu'].spaces.program
local regs=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local high,low,system=manager.machine.ioport.ports[':IN0'].fields,
 manager.machine.ioport.ports[':IN2'].fields,manager.machine.ioport.ports[':IN1'].fields
local fields={{},{}}
for n=1,2 do
 for _,button in ipairs({'High Punch','High Kick','Block','Left','Right','Up','Down'})do fields[n][button]=high['P'..n..' '..button]end
 for _,button in ipairs({'Low Punch','Low Kick'})do fields[n][button]=low['P'..n..' '..button]end
 fields[n].Coin=system['Coin '..n];fields[n].Start=system[n==1 and '1 Player Start' or '2 Players Start']
end
local victim_name=os.getenv('MK2KS_HUMAN_SPECIAL_VICTIM')or'sub_zero'
local ids={kung_lao=0,liu_kang=1,cage=2,baraka=3,kitana=4,mileena=5,
 shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11,kano=17,sonya=18}
local victim_id=assert(ids[victim_name])
local expected=side==1 and {spec[1],victim_id}or{victim_id,spec[1]}
local routes={
 {[17]={'Left'},[18]={'Right','Right','Right','Right'},[1]={},[0]={'Right'},
  [2]={'Right','Right'},[9]={'Right','Right','Right'},[8]={'Down'},
  [6]={'Right','Down'},[4]={'Right','Right','Down'},[11]={'Right','Right','Right','Down'},
  [5]={'Down','Down'},[3]={'Right','Down','Down'},
  [10]={'Right','Right','Down','Down'},[7]={'Right','Right','Right','Down','Down'}},
 {[18]={'Right'},[17]={'Left','Left','Left','Left'},[9]={},[2]={'Left'},[0]={'Left','Left'},
  [1]={'Left','Left','Left'},[11]={'Down'},[4]={'Left','Down'},[6]={'Left','Left','Down'},
  [8]={'Left','Left','Left','Down'},[7]={'Down','Down'},[10]={'Left','Down','Down'},
  [3]={'Left','Left','Down','Down'},[5]={'Left','Left','Left','Down','Down'}}}
local frame,css,live,ready,settle,command,entry,recovered,followup=0,nil,nil,nil,nil,nil,nil,nil,nil
local forward,backward,taps=nil,nil,{}
local attempt,completed=0,0
local marks,origins,css_marks,plans={},{},{},{}
local join_at=nil
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_HSPECIAL_%s frame=%d move=%s side=%d attempt=%d air=%d victim=%s writes=0 assistance=none %s',tag,frame,move,side,attempt,air and 1 or 0,victim_name,text or''))
end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),state=p:read_u16(s.state),hp=p:read_u16(s.hp),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
  action=p:read_u16(m+0x1f0),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),trail=p:read_u32(m+0x190),bank=p:read_u16(a+0x140)}
end
local function pair_live(a,b)
 return a and b and p:read_u16(0x010601d0)==2 and a.id==expected[1]and b.id==expected[2]
  and a.roster==a.id and b.roster==b.id and a.state==1 and b.state==1 and a.owner==a.actor and b.owner==b.actor
end
local function clean(a)
 return a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and a.body&0x0c==0 and a.trail==0 and a.action==0x303
end
local function part(n,a)
 local text={'slot='..n,'mode='..p:read_u16(0x010601d0)}
 for _,key in ipairs({'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank'})do text[#text+1]=string.format('%s=%08X',key,a[key])end
 for _,key in ipairs({'id','roster','state','hp','x','y','floor','action'})do text[#text+1]=key..'='..a[key]end
 log('FIELD',table.concat(text,' '))
end
local function input(n,button)
 fields[n][button]:set_value(1);log('INPUT','slot='..n..' button='..button:gsub(' ','_'))
end
local function pulse(n,button,age,start,hold)
 if age>=start and age<start+(hold or 4)then input(n,button)end
end
for _,address in ipairs({spec[2],0xff861350,0xff861500})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'human special actual entry',function(at,data,mask)
  if not command or at~=address or regs.PC.value~=address+16 then return end
  local own=sample(side)
  if not own or regs.A8.value~=own.actor or regs.A13.value~=own.main then return end
  if address==spec[2]then entry=entry or frame;marks[frame]='entry' end
  log('EVENT',string.format('entry=%08X pc=%08X at=%08X opcode=%04X mask=%04X actor=%08X main=%08X a8=%08X a13=%08X id=%d action=%d',
   address,regs.PC.value,at,data&0xffff,mask,own.actor,own.main,regs.A8.value,regs.A13.value,own.id,own.action))
 end)
end
taps[#taps+1]=p:install_write_tap(0x010602f0,0x010602ff,'human special P1 real health',function(at,data,mask)
 if command then log('HEALTH',string.format('slot=1 before=%d after=%d mask=%04X pc=%08X',p:read_u16(0x010602f0),data&0xffff,mask,regs.PC.value))end
end)
taps[#taps+1]=p:install_write_tap(0x01060ec0,0x01060ecf,'human special P2 real health',function(at,data,mask)
 if command then log('HEALTH',string.format('slot=2 before=%d after=%d mask=%04X pc=%08X',p:read_u16(0x01060ec0),data&0xffff,mask,regs.PC.value))end
end)
-- BEGIN v1763 read-only consecutive move-phase observer
local phase_snaps=0
local phase_slots={0x01060220,0x01060df0}
local function phase_active()return marks[frame]~=nil end
local function phase_log(tag,value)
 print(string.format('MK2_HPHASE_%s frame=%d move=%s side=%d attempt=%d writes=0 assistance=none %s',tag,frame,move,side,attempt,value or''))
end
local function phase_valid(a)return a>=0x01000000 and a<0x01100000 end
local phase_tap=p:install_read_tap(0xff804410,0xff80441f,'actual special-phase physical FIFO',function(at)
 if at~=0xff804410 or regs.PC.value~=0xff804420 or not phase_active()then return end
 for slot,field in ipairs(phase_slots)do
  local a,m=p:read_u32(field),p:read_u32(field+0x40)
  if a==regs.A0.value and phase_valid(a)and phase_valid(m)then
   local cache=p:read_u32(a+0x1a0);local row=regs.A3.value-112
   assert(phase_valid(cache)and row>=cache and row<cache+12*112 and(row-cache)%112==0)
   phase_log('QUEUE',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d pose=%08X facing=%04X body=%04X cache=%08X part=%d row=%08X source=%08X size=%08X xy=%08X command=%08X palette=%08X pc=%08X',
    slot,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(field+0x60),p:read_u32(a+0x1d0),p:read_u16(a+0xf0),p:read_u16(a+0x160),cache,(row-cache)//112,row,regs.A11.value,regs.A9.value,regs.A10.value,regs.A12.value,regs.A6.value,regs.PC.value))
  end
 end
end)
local phase_clip_tap=p:install_read_tap(0xff8042a0,0xff8042af,'actual special-phase pre-clip candidate',function(at)
 if at~=0xff8042a0 or regs.PC.value~=0xff8042b0 or not phase_active()then return end
 for slot,field in ipairs(phase_slots)do
  local a,m=p:read_u32(field),p:read_u32(field+0x40)
  if a==regs.A0.value and phase_valid(a)and phase_valid(m)then
   local cache=p:read_u32(a+0x1a0);local row=regs.A3.value-112
   assert(phase_valid(cache)and row>=cache and row<cache+12*112 and(row-cache)%112==0)
   phase_log('CANDIDATE',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d pose=%08X facing=%04X body=%04X cache=%08X part=%d row=%08X source=%08X size=%08X xy=%08X display=%08X command=%08X clipLow=%08X clipHigh=%08X pc=%08X',
    slot,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(field+0x60),p:read_u32(a+0x1d0),p:read_u16(a+0xf0),p:read_u16(a+0x160),cache,(row-cache)//112,row,regs.A11.value,regs.A9.value,regs.A10.value,regs.A5.value,regs.A12.value,regs.A14.value,regs.A13.value,regs.PC.value))
  end
 end
end)
local native_gfx=assert(manager.machine.memory.regions[':gfxrom'])
local function snapshot_ram(label)marks[frame]=label:gsub('%.png$','')end
local function route(start,target)
 local pending={{start,{}}};local seen={[start]=true};local next_index=1
 for _=1,40 do
  local item=pending[next_index];if not item then break end;next_index=next_index+1
  if item[1]==target then return item[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local address=({Left=0xffff1400,Right=0xffff1600,Down=0xffff1200})[key]
   local id=p:read_u16(address+item[1]*16)
   if id<=18 and not seen[id]then
    local path={table.unpack(item[2])};path[#path+1]=key;pending[#pending+1]={id,path};seen[id]=true
   end
  end
 end
 error('No actual native CSS route')
end
emu.register_frame_done(function()
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print('MK2_HPHASE_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02x',c:byte())end))
  local bytes={}
  for i=0,11943 do bytes[#bytes+1]=string.char(native_gfx:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(native_gfx:read_u8(0x1fa4000+i))end
  raw=table.concat(bytes)
  print('MK2_HPHASE_GFX frame=1 bytes=18976 hex='..raw:gsub('.',function(c)return string.format('%02x',c:byte())end))
 end
 if ready then
  local a,b=sample(1),sample(2)
  if not pair_live(a,b)then log('FAILED','reason=lost_owned_pair_at_field_done');manager.machine:exit();return end
  for n,actor in ipairs({a,b})do
   local text={'slot='..n,'mode='..p:read_u16(0x010601d0)}
   for _,key in ipairs({'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank'})do text[#text+1]=string.format('%s=%08X',key,actor[key])end
   for _,key in ipairs({'id','roster','state','hp','x','y','floor','action'})do text[#text+1]=key..'='..actor[key]end
   phase_log('POST_FIELD',table.concat(text,' '))
  end
 end
 if not phase_active()then return end
 local raw,width,height=screen:pixels();assert(width==400 and height==254 and #raw==406400);phase_snaps=phase_snaps+1
 print(string.format('MK2_HPHASE_RGB frame=%d move=%s side=%d attempt=%d stage=%s width=%d height=%d bytes=%d hex=%s',
  frame,move,side,attempt,marks[frame],width,height,#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
 phase_log('SNAP','stage='..marks[frame])
 if rawget(_G,'MK2_SPECIAL_EXIT_PENDING')then manager.machine:exit()end
end)
emu.register_stop(function()
 phase_log('RESULT',string.format('command=%d recovered=%d snaps=%d fullPortAcceptance=false rasterAcceptance=false',command or-1,recovered or-1,phase_snaps))
 phase_tap:remove();phase_clip_tap:remove()
end)
-- END v1763 read-only consecutive move-phase observer
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(fields[n])do field:clear_value()end end
 if frame>=300 and frame<304 then input(1,'High Punch')end
 if frame>=600 and frame<604 then input(1,'Coin')end
 if frame>=608 and frame<612 then input(2,'Coin')end
 if frame>=620 and frame<624 then input(1,'Start')end
 if join_at then
  local age=frame-join_at;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(2,'Start',age,20)
 end
 local mode=p:read_u16(0x010601d0)
 for n=1,2 do
  if mode~=4 then css_marks[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css_marks[n]then
   css_marks[n]=frame;css=css or frame;plans[n]=route(p:read_u16(slots[n].roster),expected[n])
   if n==1 and not join_at then join_at=frame;log('JOIN_BEGIN','slot=2')end
   log('SELECT','slot='..n..' target='..expected[n]..' path='..table.concat(plans[n],','))
  end
  if css_marks[n]and mode==4 then
   local age=frame-css_marks[n]
   for i,button in ipairs(plans[n])do pulse(n,button,age,56+(i-1)*12)end
   pulse(n,'High Punch',age,148,8)
  end
 end
 local a,b=sample(1),sample(2)
 if not live and frame>1200 and pair_live(a,b)then live=frame;log('LIVE')end
 if live and not ready and frame>=live+60 and pair_live(a,b)and clean(a)and clean(b)then ready=frame;log('READY')end
 if ready then
  if not pair_live(a,b)then log('FAILED','reason=lost_native_live_pair');manager.machine:exit();return end
  local own,victim=side==1 and a or b,side==1 and b or a
  part(1,a);part(2,b)
  if not command then
   local gap=math.abs(own.x-victim.x)
   local far=move=='knife'or move=='ring'
   if not far and gap>63 then input(side,own.x<victim.x and'Right'or'Left');settle=nil
   elseif clean(own)and clean(victim)then
    settle=settle or frame
    if frame-settle>=30 then
     attempt=attempt+1;command=frame;origins[attempt]=frame;forward=own.x<victim.x and'Right'or'Left';backward=forward=='Right'and'Left'or'Right'
     log('COMMAND',string.format('gap=%d forward=%s expectedEntry=%08X',gap,forward,spec[2]));snapshot_ram('special_before.png')
    end
   else settle=nil end
  end
  if command then
   local age=frame-command
   if air then pulse(3-side,'Up',age,0,3)end
   if move=='knife'or move=='ring'or move=='blade'or move=='choke'then
    pulse(side,'Down',age,0,3)
    pulse(side,move=='knife'and backward or forward,age,5,3)
    pulse(side,(move=='knife'or move=='blade')and'High Punch'or'Low Punch',age,6,3)
   elseif move=='square'then
    pulse(side,forward,age,0,3);pulse(side,backward,age,5,3);pulse(side,'High Punch',age,6,3)
   elseif move=='ball'then pulse(side,'Low Kick',age,0,84)
   elseif move=='bicycle'then
    pulse(side,backward,age,0,3);pulse(side,backward,age,6,3);pulse(side,'Down',age,12,3);pulse(side,'High Kick',age,13,3)
   elseif move=='leg'then
    pulse(side,'Down',age,0,7);pulse(side,'Low Punch',age,3,4);pulse(side,'Block',age,3,4)
   end
   if entry and not recovered and frame>entry+12 and clean(own)and clean(victim)then
    recovered=frame;if attempt==2 then followup=frame+16 end;log('RECOVERED');snapshot_ram('special_recovered.png')
   end
   if recovered and attempt==1 and frame>=recovered+32 then
    completed=1;log('REPEAT_READY');command=nil;entry=nil;recovered=nil;settle=nil
   end
   if entry then
    local entry_age=frame-entry
    if not marks[frame]and ({[8]=true,[16]=true,[24]=true,[40]=true,[64]=true,[96]=true})[entry_age]then marks[frame]='phase_'..entry_age end
   end
   if followup then
    local f=frame-followup
    pulse(side,forward,f,0,8);pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)
    if f==160 then completed=2;log('FINAL');snapshot_ram('special_final.png');rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)end
   elseif age>=400 then log('FAILED','reason=no_activation_or_full_recovery');manager.machine:exit()end
  end
 end
 if frame>=4300 then log('FAILED','reason=absolute_physical_deadline');manager.machine:exit()end
 if frame>=4200 and not ready then log('FAILED','reason=no_actual_match_ready');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('css=%d live=%d ready=%d command=%d entry=%d recovered=%d followup=%d completed=%d fullPortAcceptance=false scope=human_special_diagnostic_pending',
  css or-1,live or-1,ready or-1,command or-1,entry or-1,recovered or-1,followup or-1,completed))
 for _,tap in ipairs(taps)do tap:remove()end
end)

