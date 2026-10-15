-- Preserve the earned physical Kano campaign, then genuinely join as Sonya.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='kano' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')
local path='mk2ks_natural_campaign_shao_knife_retreat_v3510.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local function one(before,after)
 local at=assert(source:find(before,1,true))
 assert(not source:find(before,at+#before,true),'Unique original source boundary')
 source=source:sub(1,at-1)..after..source:sub(at+#before)
end
local helper=[[
local join_css,join_plan,join_live,join_last_mode,join_done=nil,nil,nil,nil,false
local function join_log(tag,value)
 print(string.format('MK2_POSTENDING_%s frame=%d seconds=%.12f slot=2 target=18 writes=0 assistance=none %s',tag,frame,emu.time(),value or''))
end
local function join_press(key)
 buttons[key]:set_value(1);join_log('INPUT','button='..key:gsub(' ','_'))
end
local function join_route(start)
 local q={{start,{}}};local visited={[start]=true};local at=1
 while q[at]do
  local row=q[at];at=at+1
  if row[1]==18 then return row[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local next_id=p:read_u16(adjacency[key]+row[1]*16)
   if next_id<=18 and not visited[next_id]then
    local steps={};for _,step in ipairs(row[2])do steps[#steps+1]=step end
    steps[#steps+1]=key;q[#q+1]={next_id,steps};visited[next_id]=true
   end
  end
 end
 error('No native route to Sonya')
end
local function postending_join()
 local age=frame-ending_completed-300
 local mode,state=p:read_u16(0x010601d0),p:read_u16(slots[2].state)
 if age==0 then
  assert(mode==11 and p:read_u32(slots[1].actor)==0 and p:read_u32(slots[2].actor)==0)
  join_log('BEGIN','ending_completed='..ending_completed..' attract_fields=300 mode='..mode)
 end
 if age>=0 and age<4 then join_press('Coin')end
 if age>=20 and age<24 then join_press('Start')end
 if not join_css and mode==4 and state==3 then
  join_css=frame;join_plan=join_route(p:read_u16(slots[2].roster))
  join_log('SELECT','initial='..p:read_u16(slots[2].roster)..' path='..table.concat(join_plan,','))
 end
 if join_css and mode==4 then
  local css_age=frame-join_css
  for i,key in ipairs(join_plan)do
   local at=56+(i-1)*12
   if css_age>=at and css_age<at+4 then join_press(key)end
  end
  if css_age==130 or css_age==146 then
   join_log('SELECT_ID','roster='..p:read_u16(slots[2].roster)..' state='..state..' age='..css_age)
   _campaign_emit('postjoin_selection_'..css_age..'.png')
  end
  if css_age>=148 and css_age<156 then join_press('High Punch')end
 end
 if mode~=join_last_mode then
  join_log('MODE','mode='..mode..' state='..state..' roster='..p:read_u16(slots[2].roster))
  if join_css and mode~=4 then _campaign_emit('postjoin_mode_'..mode..'_'..frame..'.png')end
  join_last_mode=mode
 end
 local human,other=sample(2),sample(1)
 if mode==2 and state==1 and p:read_u16(slots[1].state)==0 and human and other and
  human.owner==human.actor and other.owner==other.actor then
  assert(human.id==18 and human.roster==18 and human.hp>0,'True live Sonya after ending, never proxy')
  if not join_live then
   join_live=frame
   join_log('MATCH','stage='..p:read_u16(0x01061b30)..' actor='..string.format('%08X',human.actor)..' main='..string.format('%08X',human.main)..' id=18')
   _campaign_emit('postjoin_match.png')
  end
  local live_age=frame-join_live
  join_log('LIVE',string.format('age=%d actor=%08X main=%08X id=%d roster=%d hp=%d x=%d y=%d floor=%d action=%d cpu=%d cpu_hp=%d',
   live_age,human.actor,human.main,human.id,human.roster,human.hp,human.x,human.y,human.floor,human.action,other.id,other.hp))
  if live_age>=10 and live_age<20 then join_press('Right')end
  if live_age>=50 and live_age<54 then join_press('Up')end
  if live_age>=80 and live_age<84 then join_press('High Punch')end
  if live_age>=90 then join_press('Block')end
  if live_age==180 then _campaign_emit('postjoin_match_180.png')end
  if live_age>=360 and not join_done then
   join_done=true;_campaign_emit('postjoin_match_final.png')
   join_log('COMPLETE','live_fields=361 identity=18 input=ordinary_coin_start_selection_walk_jump_punch_block')
   manager.machine:exit()
  end
 end
 if age>=1800 and not join_done then
  join_log('FAILED','reason=postending_join_deadline mode='..mode..' state='..state)
  manager.machine:exit()
 end
end
]]
one('-- Observe actual own special entries independently of intended button plans.',helper..'\n-- Observe actual own special entries independently of intended button plans.')
one("if frame>=300 and frame<304 then press('High Punch')end",
 "if ending_completed and frame-ending_completed>=300 then postending_join();return end\n if frame>=300 and frame<304 then press('High Punch')end")
one('if ending_completed and frame-ending_completed>=300 then manager.machine:exit()end',
 '-- The post-ending phase owns terminal exit after the original 300 attract fields.')
one("local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()",'_campaign_guest(raw)')
local adapted,count=source:gsub('screen:snapshot%(','_campaign_emit(')
assert(count==6,'All six original RAM-only raster sinks')
local prefix=[[
local function _campaign_guest(raw)
 assert(#raw==1048576)
 print('MK2_CAMPAIGN_GUEST_RAM frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
end
local function _campaign_emit(name)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=%s seconds=%.9f width=%d height=%d bytes=%d hex=%s',name,emu.time(),w,h,#raw,
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(prefix..adapted,'@'..path..'::RAM_sinks_then_postending_ordinary_join','t',_ENV))()
local limit=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_OBSERVER_LIMIT')))
assert(limit==5900)
emu.register_frame_done(function()
 if emu.time()>=limit then
  print('MK2_CAMPAIGN_HOST_DEADLINE seconds='..emu.time()..' limit=5900 assistance=none writes=0')
  manager.machine:exit()
 end
end)
dofile('mk2ks_mileena_campaign_trace_v3848.lua')
