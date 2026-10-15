-- Original current Kano campaign/RAM adapter, only ordinary-input victim phase.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='kano')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_kano_current_p2_campaign_ram_v4472.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')","assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')")
local boundary="local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()"
once(boundary,boundary..[=[
local function victim_once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
victim_once('  if winner==0 and human.hp>0 and other.hp>0 then',
 '  if winner==0 and human.hp>0 and other.hp>0 and not(stage==2 and other.roster==7 and not rawget(_G,\'MK2KS_KANO_PAIRED_CALLBACK\'))then')
victim_once('  local age=frame-css',
 '  local age=frame-css\n  if age==56 then plan=route(p:read_u16(slots[side].roster));log(\'SETTLED_ROUTE\',\'roster=\'..p:read_u16(slots[side].roster)..\' path=\'..table.concat(plan,\',\'))end')
]=])
assert(load(source,'@'..path..'::same_current_Ram_adapter_physical_Kano_Raiden_victim_phase','t',_ENV))()

-- Passive full state chronology after actual handoff; never assigns guest state.
local p=manager.machine.devices[':maincpu'].spaces.program
local screen=manager.machine.screens[':screen']
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,admitted,last_key,losses,in_loss=0,nil,nil,0,false
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 return {actor=a,main=m,owner=valid(m)and p:read_u32(m+0xc0)or 0,
  id=valid(a)and p:read_u16(a+0x1f0)or 65535,roster=p:read_u16(s.roster),state=p:read_u16(s.state),
  hp=p:read_u16(s.hp),x=valid(a)and p:read_i16(a+0x90)or 0,y=valid(a)and p:read_i16(a+0xb0)or 0,
  pose=valid(a)and p:read_u32(a+0x1d0)or 0,floor=valid(m)and p:read_i16(m+0x200)or 0}
end
local function emit()
 local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=kano_raiden_paired_frame%d.png seconds=%.12f width=400 height=254 bytes=406400 hex=%s',
  frame,emu.time(),raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
emu.register_frame_done(function()
 frame=frame+1
 local callback=rawget(_G,'MK2KS_KANO_PAIRED_CALLBACK')
 local mode,stage=p:read_u16(0x010601d0),p:read_u16(0x01061b30)
 local a,b=sample(1),sample(2)
 local loss=stage==2 and mode==3 and a.state==2 and a.actor==0 and p:read_u16(0x01061b00)==2
 if loss and not in_loss then losses=losses+1 end
 in_loss=loss
 if not callback and losses>=8 then
  print(string.format('MK2_KANO_RAIDEN_VICTIM_NO_HANDOFF frame=%d real_paid_losses=%d writes=0 assistance=none',frame,losses))
  manager.machine:exit();return
 end
 if not callback then return end
 print(string.format('MK2_KANO_RAIDEN_VICTIM_STATE frame=%d callback=%d admitted=%d mode=%d stage=%d actor1=%08X main1=%08X owner1=%08X id1=%d roster1=%d state1=%d hp1=%d x1=%d y1=%d floor1=%d pose1=%08X actor2=%08X main2=%08X owner2=%08X id2=%d roster2=%d state2=%d hp2=%d x2=%d y2=%d floor2=%d pose2=%08X writes=0 assistance=none',
  frame,callback,admitted or-1,mode,stage,a.actor,a.main,a.owner,a.id,a.roster,a.state,a.hp,a.x,a.y,a.floor,a.pose,
  b.actor,b.main,b.owner,b.id,b.roster,b.state,b.hp,b.x,b.y,b.floor,b.pose))
 local key=string.format('%d:%d:%d:%d:%d:%d',mode,a.state,b.state,a.id,b.id,admitted or-1)
 if key~=last_key or frame%120==0 then emit();last_key=key end
 if not admitted and mode==2 and stage==2 and a.state==1 and b.state==0 and
  a.id==17 and a.roster==17 and b.id==7 and b.roster==7 and
  valid(a.actor)and valid(b.actor)and a.owner==a.actor and b.owner==b.actor and a.hp==161 and b.hp==161 then
  admitted=frame
  print(string.format('MK2_KANO_RAIDEN_VICTIM_READMITTED frame=%d callback=%d ids=17,7 hp=161,161 writes=0 assistance=none',frame,callback))
  emit()
 end
 if admitted and frame-admitted>=500 then
  assert(mode==2 and stage==2 and a.state==1 and b.state==0 and a.id==17 and a.roster==17 and
   b.id==7 and b.roster==7 and a.owner==a.actor and b.owner==b.actor and a.hp>0 and b.hp>0,
   'Actual paid-reselected Kano/Raiden still owned and playable after500 native fields')
  print(string.format('MK2_KANO_RAIDEN_VICTIM_COMPLETE frame=%d admitted=%d alive_fields=%d health=%d,%d writes=0 assistance=none',
   frame,admitted,frame-admitted,a.hp,b.hp))
  emit();manager.machine:exit()
 end
end)
