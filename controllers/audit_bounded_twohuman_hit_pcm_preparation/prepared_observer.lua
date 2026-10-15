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


 if frame>=3500 then log('FAILED','reason=bounded_timeout');manager.machine:exit();return end
 if ready then
  assert(pair_live(a,b),'True selected two-human pair')
  part(1,a);part(2,b)
  local own,victim=side==1 and a or b,side==1 and b or a
  if frame-ready>=420 then log('COUNTER_TERMINAL');manager.machine:exit();return end
  if not command then
   if math.abs(own.x-victim.x)>80 then input(side,own.x<victim.x and 'Right' or 'Left');settle=nil
   elseif clean(own) and clean(victim) then
    settle=settle or frame
    if frame-settle>=20 then
     command=frame;attempt=1;forward=own.x<victim.x and 'Right' or 'Left';backward=forward=='Right' and 'Left' or 'Right'
     log('COMMAND','gap='..math.abs(own.x-victim.x))
    end
   end
  end
  if command then
   local age=frame-command
   pulse(side,backward,age,0,3);pulse(side,backward,age,6,3);pulse(side,'Down',age,12,3);pulse(side,'High Kick',age,13,3)
   if age<30 then
    input(3-side,'Down');if age>=10 and age<14 then input(3-side,'High Punch')end
   end
  end
 end
end)
local counter_taps={}
counter_taps[1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual private cue',function(at,value,mask)
 if at==0x01d01030 and value>=0x6b00 and value<=0x6b03 then log('CUE',string.format('seconds=%.12f value=%04X',emu.time(),value))end
end)
for slot,address in ipairs({0x010602f0,0x01060ec0})do
 counter_taps[#counter_taps+1]=p:install_write_tap(address,address+15,'actual counter health',function(at,value,mask)
  if ready then log('HEALTH',string.format('seconds=%.12f slot=%d before=%d after=%d pc=%08X',emu.time(),slot,p:read_u16(address),value&65535,regs.PC.value))end
 end)
end
emu.register_stop(function()assert(#counter_taps==3);log('STOP','raw_media=none')end)

local counter_port_tap=p:install_read_tap(0x01600000,0x0160000f,'actual native input admission',function(at,value,mask)
 if not command or frame-command<0 or frame-command>40 then return end
 log('PORT_READ',string.format('at=%08X value=%04X mask=%04X pc=%08X age=%d',at,value,mask,regs.PC.value,frame-command))
end)
emu.register_frame_done(function()
 if command and frame-command<=40 then
  log('PHYSICAL_PORT',string.format('age=%d in0=%04X in2=%04X',frame-command,manager.machine.ioport.ports[':IN0']:read(),manager.machine.ioport.ports[':IN2']:read()))
 end
end)
emu.register_stop(function()assert(counter_port_tap)end)

local action_write_tap=p:install_write_tap(0x01000000,0x010fffff,'actual counter action store',function(at,value,mask)
 if not command or frame-command<0 or frame-command>40 then return end
 local own=sample(3-side)
 if own and at==own.main+0x1f0 then
  log('ACTION_WRITE',string.format('age=%d seconds=%.12f slot=%d main=%08X at=%08X before=%04X value=%04X mask=%04X pc=%08X a8=%08X a13=%08X',frame-command,emu.time(),3-side,own.main,at,own.action,value&65535,mask,regs.PC.value,regs.A8.value,regs.A13.value))
 end
end)
emu.register_stop(function()assert(action_write_tap)end)

local hit_saved,hit_channels={},{}
local function bind_hit_voice()
 for name,index in pairs(manager.machine.devices[':'].items)do
  for _,field in ipairs({'actor','main','health','id','mode'})do
   if name:match('/m_mk2ks_battle_'..field..'$')then assert(not hit_saved[field]);hit_saved[field]=emu.item(index)end
  end
 end
 for _,field in ipairs({'actor','main','health','id','mode'})do assert(hit_saved[field])end
 for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
  local n,field=name:match('^(%x+)/chan%.(.+)$')
  if n then n=tonumber(n,16);if n>=10 and n<=13 then hit_channels[n]=hit_channels[n]or{};hit_channels[n][field]=emu.item(index)end end
 end
 for n=10,13 do for _,field in ipairs({'source_len','pos','paused','loop'})do assert(hit_channels[n][field])end end
end
local function hit_voice_observe(phase)
 if not command or frame-command>160 then return end
 for n=0,1 do
  log('VOICE_OWNER',string.format('seconds=%.12f phase=%s slot=%d actor=%08X main=%08X health=%d id=%d mode=%d',emu.time(),phase,n+1,hit_saved.actor:read(n),hit_saved.main:read(n),hit_saved.health:read(n),hit_saved.id:read(n),hit_saved.mode:read(n)))
 end
 for n=10,13 do
  local c=hit_channels[n]
  log('VOICE_CHANNEL',string.format('seconds=%.12f phase=%s channel=%d length=%d pos=%.8f paused=%d loop=%d',emu.time(),phase,n,c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.paused:read(0),c.loop:read(0)))
 end
end
emu.register_frame(function()if frame==1 then bind_hit_voice()end;hit_voice_observe('frame')end)
emu.register_sound_update(function()hit_voice_observe('sound')end)
emu.register_stop(function()assert(hit_saved.actor and hit_channels[10]);log('VOICE_STOP','raw_media=none')end)
-- Constant-memory SHA-256 for transient sound-update strings; no files/media.
local pcm_sha_k={
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2}
local function pcm_ror(x,n)return ((x>>n)|(x<<(32-n)))&0xffffffff end
local function pcm_sha256(raw)
 local size=#raw
 local padded=raw..'\128'..string.rep('\0',(55-size)%64)..string.pack('>I8',size*8)
 local h={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19}
 for offset=1,#padded,64 do
  local w={}
  for i=1,16 do w[i]=string.unpack('>I4',padded,offset+(i-1)*4)end
  for i=17,64 do
   local a,b=w[i-15],w[i-2]
   local s0=pcm_ror(a,7)~pcm_ror(a,18)~(a>>3)
   local s1=pcm_ror(b,17)~pcm_ror(b,19)~(b>>10)
   w[i]=(w[i-16]+s0+w[i-7]+s1)&0xffffffff
  end
  local a,b,c,d,e,f,g,j=table.unpack(h)
  for i=1,64 do
   local s1=pcm_ror(e,6)~pcm_ror(e,11)~pcm_ror(e,25)
   local ch=(e&f)~((~e)&g)
   local t1=(j+s1+ch+pcm_sha_k[i]+w[i])&0xffffffff
   local s0=pcm_ror(a,2)~pcm_ror(a,13)~pcm_ror(a,22)
   local maj=(a&b)~(a&c)~(b&c)
   local t2=(s0+maj)&0xffffffff
   j,g,f,e,d,c,b,a=g,f,e,(d+t1)&0xffffffff,c,b,a,(t1+t2)&0xffffffff
  end
  local v={a,b,c,d,e,f,g,j}
  for i=1,8 do h[i]=(h[i]+v[i])&0xffffffff end
 end
 local hex={};for i=1,8 do hex[i]=string.format('%08X',h[i])end
 return table.concat(hex)
end
assert(pcm_sha256('')=='E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855')
assert(pcm_sha256('abc')=='BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD')
assert(pcm_sha256(string.rep('a',1000000))=='CDC76E5C9914FB9281A1C7E284D73E67F1809A48A497200E046D39CCC7112CD0')

local human_hit_updates=0
emu.register_sound_update(function()
 if not command or frame-command>160 then return end
 local raw=manager.machine.sound:get_samples();assert(#raw>0 and #raw%4==0)
 local energy,peak=0,0
 for at=1,#raw,2 do local value=string.unpack('<i2',raw,at);energy=energy+value*value;peak=math.max(peak,math.abs(value))end
 human_hit_updates=human_hit_updates+1
 log('PCM',string.format('seconds=%.12f bytes=%d sha256=%s energy=%d peak=%d raw_media=none',emu.time(),#raw,pcm_sha256(raw),energy,peak))
end)
emu.register_stop(function()log('PCM_STOP','updates='..human_hit_updates..' raw_media=none')end)
