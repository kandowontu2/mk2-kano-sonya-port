"""Accepted physical paid join, native BFS selectors, actual two-player match actors."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_challenger_two_coins_preparation'
out=sync.ROOT/'audit_current_native_joined_matches_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if join_selection and frame-join_selection>=160 then log('JOIN_COMPLETE','selection_fields=160');manager.machine:exit()end"
assert source.count(old)==1
source=source.replace(old,"if join_selection and frame-join_selection==160 then log('JOIN_COMPLETE','selection_fields=160')end")
source+='''
local joined_targets={tonumber(os.getenv('MK2KS_JOIN_P1')),tonumber(os.getenv('MK2KS_JOIN_P2'))}
assert((joined_targets[1]==17 and joined_targets[2]==18)or(joined_targets[1]==18 and joined_targets[2]==17))
local joined_css,joined_live=nil,nil
local joined_plan={{},{}}
local joined_buttons={}
for n=1,2 do
 joined_buttons[n]={}
 for _,key in ipairs({'Left','Right','Down','High Punch'})do
  joined_buttons[n][key]=manager.machine.ioport.ports[':IN0'].fields['P'..n..' '..key]
 end
end
local function joined_route(start,target)
 local queue={{start,{}}};local seen={[start]=true};local cursor=1
 local adjacent={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
 while queue[cursor]do
  local item=queue[cursor];cursor=cursor+1
  if item[1]==target then return item[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local next_id=p:read_u16(adjacent[key]+item[1]*16)
   if next_id<=18 and not seen[next_id]then
    local path={};for _,step in ipairs(item[2])do path[#path+1]=step end
    path[#path+1]=key;queue[#queue+1]={next_id,path};seen[next_id]=true
   end
  end
 end
 error('Native joined route missing')
end
emu.register_frame(function()
 if not join_selection then return end
 local mode=p:read_u16(0x010601d0)
 if not joined_css and mode==4 and p:read_u16(slots[1].state)==3 and p:read_u16(slots[2].state)==3 then
  joined_css=frame;log('JOINED_SELECT_START','targets='..joined_targets[1]..','..joined_targets[2])
 end
 if not joined_css or mode~=4 then return end
 local age=frame-joined_css
 for n=1,2 do
  if age==56 then
   local initial=p:read_u16(slots[n].roster)
   joined_plan[n]=joined_route(initial,joined_targets[n])
   log('JOINED_ROUTE',string.format('slot=%d initial=%d target=%d path=%s',n,initial,joined_targets[n],table.concat(joined_plan[n],',')))
  end
  for index,key in ipairs(joined_plan[n])do
   local at=56+(index-1)*12
   if age>=at and age<at+4 then joined_buttons[n][key]:set_value(1)end
  end
  if age==146 then
   local actual=p:read_u16(slots[n].roster);assert(actual==joined_targets[n])
   log('JOINED_SELECTED',string.format('slot=%d actual=%d target=%d',n,actual,joined_targets[n]))
  end
  if age>=148 and age<156 then joined_buttons[n]['High Punch']:set_value(1)end
 end
end)
emu.register_frame_done(function()
 if not joined_css or p:read_u16(0x010601d0)~=2 then return end
 local a,b=sample(1),sample(2)
 if not a or not b or a.state~=1 or b.state~=1 then return end
 assert(a.id==joined_targets[1]and a.roster==a.id and a.owner==a.actor)
 assert(b.id==joined_targets[2]and b.roster==b.id and b.owner==b.actor)
 joined_live=joined_live or frame
 local age=frame-joined_live
 for n,row in ipairs({a,b})do
  log('JOINED_MATCH_PAIR',string.format('age=%d slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d',age,n,row.actor,row.main,row.owner,row.id,row.roster,row.state,row.hp))
 end
 if age==160 then log('JOINED_MATCH_COMPLETE','fields=161');manager.machine:exit()end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_added.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
for p1,p2 in [(17,18),(18,17)]:
 text=runner.replace('audit_current_native_challenger_two_coins_added_runtime',f'audit_current_native_joined_{p1}_{p2}_runtime')
 text=text.replace("$env:MK2KS_TEST_FIGHTER='sonya'",f"$env:MK2KS_TEST_FIGHTER='sonya'\n$env:MK2KS_JOIN_P1='{p1}'\n$env:MK2KS_JOIN_P2='{p2}'")
 (out/f'run_{p1}_{p2}.ps1').write_text(text)
print('Prepared accepted two-credit join through both true-ID match arrangements/no media')
