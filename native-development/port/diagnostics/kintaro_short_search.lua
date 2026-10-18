-- Bounded loaded-state input planning ONLY. Never edit guest RAM/registers.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local root=assert(os.getenv('KS_SEARCH_ROOT'))
local out=assert(os.getenv('KS_SEARCH_OUT'))
local controls={}
for _,port in pairs(m.ioport.ports) do for name,field in pairs(port.fields) do controls[name]=field end end
local function set(name,v)assert(controls[name],name);controls[name]:set_value(v)end
local function word(a)return p:read_u8(a)|(p:read_u8(a+8)<<8)end
local function long(a)return word(a)|(word(a+16)<<16)end
local function signed(a)local v=word(a);return v<32768 and v or v-65536 end
local function clear()
 for _,name in ipairs({'High Punch','Low Punch','High Kick','Low Kick','Block','Up','Down','Left','Right'}) do set('P1 '..name,0) end
end
local actions={'kick','punch','counter','knife','guard','away','backkick'}
local s={phase='root_load',depth=1,index=1,age=0,ticks=0,children={},route={}}
local log=assert(io.open('search.csv','w'))
log:write('depth,action,p1hp,p2hp,p1wins,p2wins,map,mode,distance,score\n')
local chosen=assert(io.open('chosen.csv','w'))
chosen:write('depth,action,p1hp,p2hp,p1wins,p2wins,map,mode,distance,score\n')
local function metric(action)
 local a,b=long(0x01060220),long(0x01060df0)
 local distance=(a>=0x01000000 and b>=0x01000000) and math.abs(signed(a+0x90)-signed(b+0x90)) or 0
 local r={action=action,hp=word(0x010602f0),enemy=word(0x01060ec0),wins=word(0x01060310),
  losses=word(0x01060ee0),map=word(0x01061b30),mode=word(0x010601d0),distance=distance}
 r.score=r.wins*10000-r.losses*10000+2*r.hp-r.enemy+math.min(distance,260)/1000
 if r.map>15 then r.score=r.score+100000 end
 return r
end
local function record(file,r)
 file:write(string.format('%d,%s,%d,%d,%d,%d,%d,%d,%d,%.3f\n',s.depth,r.action,r.hp,r.enemy,
  r.wins,r.losses,r.map,r.mode,r.distance,r.score));file:flush()
end
local function save(path,phase)
 assert(not io.open(path,'rb'),'Refuse existing candidate')
 s.savedPath=path;s.wait=0;s.phase=phase;m:save(path)
end
local function load_child()
 s.phase='case_load';s.age=0;m:load(s.parent)
end
s.subscription=emu.add_machine_post_load_notifier(function()
 if s.phase=='root_load' then s.phase='intro'
 elseif s.phase=='case_load' then s.phase='acting';s.age=0
 else error('Unexpected load phase') end
end)
local function input(action,age)
 if word(0x010601d0)~=2 then return end
 local a,b=long(0x01060220),long(0x01060df0)
 if a<0x01000000 or b<0x01000000 then return end
 local toward=signed(a+0x90)<signed(b+0x90) and 'P1 Right' or 'P1 Left'
 local away=toward=='P1 Right' and 'P1 Left' or 'P1 Right'
 local phase=(age-1)%60+1
 if action=='kick' or action=='punch' or action=='backkick' then
  if phase<=3 then set('P1 Up',1);set(action=='backkick' and away or toward,1) end
  if phase>=28 and phase<=31 then set(action=='punch' and 'P1 High Punch' or 'P1 High Kick',1) end
 elseif action=='counter' then
  set('P1 Down',1);if (age-1)%12<3 then set('P1 High Punch',1) end
 elseif action=='knife' then
  if phase<=3 then set('P1 Down',1)
  elseif phase>=7 and phase<=9 then set(away,1)
  elseif phase>=13 and phase<=15 then set('P1 High Punch',1) end
 elseif action=='guard' then set('P1 Down',1);set('P1 Block',1)
 elseif action=='away' then set(away,1) end
end
local function finish(reason)
 local f=assert(io.open('search_end.txt','w'));f:write(reason..'\n');f:close()
 log:close();chosen:close();m:exit();s.phase='done'
end
local function tick()
 s.ticks=s.ticks+1;clear()
 if s.phase=='intro' then
  if word(0x010601d0)==2 and word(0x010602f0)==161 and word(0x01060ec0)==161 then
   save(out..'/root.sta','root_save')
  end
 elseif s.phase=='root_save' or s.phase=='case_save' then
  s.wait=s.wait+1
  if s.wait>=4 then
   local f=io.open(s.savedPath,'rb')
   if f then
    assert(f:seek('end')>1024);f:close()
    if s.phase=='root_save' then s.parent=s.savedPath;load_child()
    else
     s.children[#s.children+1]=s.pending
     s.index=s.index+1
     if s.index<=#actions then load_child()
     else
      local best=s.children[1]
      for _,r in ipairs(s.children) do if r.score>best.score then best=r end end
      record(chosen,best);s.route[#s.route+1]=best.action
      -- Only own generated temporary search states are removed. Input/results remain.
      for _,r in ipairs(s.children) do if r.path~=best.path then assert(os.remove(r.path)) end end
      if s.parent~=out..'/root.sta' then assert(os.remove(s.parent)) end
      s.parent=best.path
      if best.map>15 or (best.wins==2 and best.hp>0) then finish('planning_candidate_match_win')
      elseif s.depth>=60 then finish('depth_budget')
      elseif best.losses>=2 then finish('native_match_lost')
      else s.depth=s.depth+1;s.index=1;s.children={};load_child() end
     end
    end
   elseif s.wait>120 then error('Save file not observed') end
  end
 elseif s.phase=='acting' then
  s.age=s.age+1
  input(actions[s.index],s.age)
  if s.age==120 then
   clear();s.pending=metric(actions[s.index]);record(log,s.pending)
   s.pending.path=string.format('%s/step_%03d_%s.sta',out,s.depth,actions[s.index])
   save(s.pending.path,'case_save')
  end
 end
 if s.ticks>60000 and s.phase~='done' then finish('global_field_budget') end
end
emu.register_frame_done(function()
 local ok,err=pcall(tick)
 if not ok then print('SEARCH_ERROR: '..tostring(err));m:exit() end
end)
m:load(root)
