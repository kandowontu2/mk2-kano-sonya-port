-- Entire original cold earned Tomb driver; ordinary paid rejoin AFTER its window.
local f=assert(io.open('mk2ks_current_stage_ram_driver_v3594.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once("  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local f=assert(io.open(assert(os.getenv('MK2KS_STAGE_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 '  -- Whole guest goes to the original native render RAM sink.')
once('if at~=entry or not window then return end',
 'if at~=entry or cpu.PC.value~=at+16 or not window or(action and frame-action>1101)then return end')
once('if mask~=0xffff or pending or p:read_u16(0x010601d0)~=2 then return end',
 'if mask~=0xffff or pending or p:read_u16(0x010601d0)~=2 or(action and frame-action>1101)then return end')
once(' for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end',
 ' for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end\n if action and frame-action>1101 then return end')
once(' if not action then return end\n local age=frame-action;',
 ' if not action or frame-action>1101 then return end\n local age=frame-action;')
once(' if age>=1100 then manager.machine:exit()end',
 " if age==1100 then log('ORIGINAL_BOUNDARY','age='..age)end")
local extra=[=[
-- Separate later physical inputs and owned states, never fold them into old phase.
local join_css,join_at,admitted,completed={},nil,nil,nil
local function join_log(tag,s)
 print(string.format('MK2_TOMB_REJOIN_%s frame=%d writes=0 assistance=none %s',tag,frame,s or''))
end
local function join_press(n,key)
 buttons[n][key]:set_value(1);join_log('INPUT','slot='..n..' button='..key:gsub(' ','_'))
end
emu.register_frame(function()
 if not action or frame-action<=1101 then return end
 MK2KS_TOMB_POST_ACTION=action
 local mode=p:read_u16(0x010601d0)
 if frame-action>=1140 and not admitted then
  join_at=join_at or frame
  local age=(frame-join_at)%300
  for n=1,2 do
   if age<4 then join_press(n,'Coin')end
   local start=n==1 and 20 or 60
   if age>=start and age<start+4 then join_press(n,'Start')end
   if mode==4 and p:read_u16(slots[n].state)==3 then
    local target=n==side and id or victim_id
    if not join_css[n]then
     join_css[n]={at=frame,path=route(p:read_u16(slots[n].roster),target)}
     join_log('SELECT','slot='..n..' target='..target..' route='..table.concat(join_css[n].path,','))
    end
    local css_age=frame-join_css[n].at
    for i,key in ipairs(join_css[n].path)do
     local at=56+(i-1)*12;if css_age>=at and css_age<at+4 then join_press(n,key)end
    end
    if css_age==146 then
     local actual=p:read_u16(slots[n].roster)
     join_log('SELECT_ID','slot='..n..' actual='..actual..' target='..target);assert(actual==target)
    end
    if css_age>=148 and css_age<156 then join_press(n,'High Punch')end
   elseif mode~=4 then join_css[n]=nil end
  end
 end
 local a,b=sample(1),sample(2)
 local wanted1=side==1 and id or victim_id;local wanted2=side==2 and id or victim_id
 if not admitted and join_at and mode==2 and a and b and
  p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 and
  a.id==wanted1 and b.id==wanted2 and a.roster==wanted1 and b.roster==wanted2 and
  a.owner==a.actor and b.owner==b.actor then
  admitted=frame;MK2KS_TOMB_POST_ADMITTED=frame
  join_log('ADMITTED',string.format('ids=%d,%d actor1=%08X main1=%08X owner1=%08X actor2=%08X main2=%08X owner2=%08X hp=%d,%d',
   a.id,b.id,a.actor,a.main,a.owner,b.actor,b.main,b.owner,a.hp,b.hp))
 end
 if admitted then
  local age=frame-admitted
  if age>=10 and age<28 then join_press(1,'Right');join_press(2,'Left')end
  if age>=40 and age<44 then join_press(1,'Up')end
  if age>=80 and age<84 then join_press(2,'High Punch')end
  if age>=120 and age<140 then join_press(1,'Block')end
  if age>=160 and age<164 then join_press(1,'Low Kick')end
 end
end)
emu.register_frame_done(function()
 if admitted and frame-admitted>=180 and not completed then
  local a,b=sample(1),sample(2)
  assert(p:read_u16(0x010601d0)==2 and a and b and a.owner==a.actor and b.owner==b.actor)
  assert(a.id==(side==1 and id or victim_id)and b.id==(side==2 and id or victim_id))
  completed=frame;join_log('COMPLETE','admitted='..admitted..' alive_fields='..(frame-admitted))
  manager.machine:exit()
 elseif action and frame-action>=3600 and not completed then
  completed=frame;join_log('DEADLINE','admitted='..(admitted or-1));manager.machine:exit()
 end
end)
]=]
source=source..'\n'..extra
assert(not source:find(':write_',1,true)and not source:find("'wb'",1,true))
assert(load(source,'@whole3594_Tomb_then_physical_paid_rejoin','t',_ENV))()
