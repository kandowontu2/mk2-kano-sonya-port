-- Existing physical inputs, audio, shadow and rendering observers are unchanged.
-- Observe native group-task/sprite allocation, real free-list stores and lists.
dofile('mk2ks_current_friendship_full_render_v2702.lua')
local cpu=manager.machine.devices[':maincpu']
local p,state=cpu.spaces.program,cpu.state
local side=assert(tonumber(os.getenv('MK2KS_FRIEND_SIDE')))
local fighter=assert(os.getenv('MK2KS_FRIEND_WINNER'))
local id=assert(({kano=17,sonya=18,cage=2,liu_kang=1})[fighter])
local physical=side==1 and 0x01060220 or 0x01060df0
local action_address=id<17 and p:read_u32(0xff880d90+id*32)or 0xff800000+(id==17 and 0xf9a00 or 0xf9c00)*8
local frame,action,task,object,parent,parent_main=0,nil,nil,nil,nil,nil
local returned_task,returned_object=false,false
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print(string.format('MK2_CHILD_LIFE_%s frame=%d fighter=%s side=%d writes=0 assistance=none %s',tag,frame,fighter,side,value or''))
end
local function own()
 local a,m=p:read_u32(physical),p:read_u32(physical+0x40)
 if not valid(a)or not valid(m)or p:read_u16(a+0x1f0)~=id then return end
 return a,m
end
local function chain(head)
 local at=p:read_u32(head);local result,seen={},{}
 while at~=0 do
  if not valid(at)or seen[at]or #result>=1024 then return result,false,at end
  result[#result+1]=at;seen[at]=true;at=p:read_u32(at)
 end
 return result,true,0
end
local function csv(values)
 if #values==0 then return '-'end
 local s={};for _,v in ipairs(values)do s[#s+1]=string.format('%08X',v)end
 return table.concat(s,',')
end
local function lists(tag)
 local value={}
 for _,item in ipairs({{'tasks',0x01068e30},{'freeTasks',0x01068e50},{'objects',0x0105d480},{'layer1',0x0105d4a0},{'layer2',0x0105d4c0},{'freeObjects',0x01060130}})do
  local nodes,ok,bad=chain(item[2]);value[#value+1]=string.format('%s=%s %sCount=%d %sValid=%d %sBad=%08X',item[1],csv(nodes),item[1],#nodes,item[1],ok and 1 or 0,item[1],bad)
 end
 value[#value+1]=string.format('task=%08X object=%08X parent=%08X parentMain=%08X physical=%08X physicalMain=%08X mode=%d taskID=%d taskOwner=%08X taskResume=%08X objectTask=%08X objectCache=%08X objectPose=%08X parentTrail=%08X taskReturned=%d objectReturned=%d',
  task or 0,object or 0,parent or 0,parent_main or 0,p:read_u32(physical),p:read_u32(physical+0x40),p:read_u16(0x010601d0),
  task and p:read_u16(task+0x20)or -1,task and p:read_u32(task+0xc0)or 0,task and p:read_u32(task+0xe0)or 0,
  object and p:read_u32(object+0x20)or 0,object and p:read_u32(object+0x1a0)or 0,object and p:read_u32(object+0x1d0)or 0,
  parent_main and p:read_u32(parent_main+0x190)or 0,returned_task and 1 or 0,returned_object and 1 or 0)
 log(tag,table.concat(value,' '))
end
taps[#taps+1]=p:install_read_tap(action_address,action_address+15,'actual Friendship lifecycle activation',function(at)
 if action or at~=action_address or state.PC.value~=at+16 then return end
 local a,m=own();if not a or state.A8.value~=a or state.A13.value~=m then return end
 action=frame;log('ACTION',string.format('entry=%08X actor=%08X main=%08X id=%d',at,a,m,id))
end)
for _,address in ipairs({0xff83ae70,0xff83aea0,0xff83af70})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'original group task/sprite constructor',function(at)
  if not action or at~=address or state.PC.value~=at+16 then return end
  local a,m=own()
  if address~=0xff83af70 then
   if task or not a or state.A8.value~=a or state.A13.value~=m or id~=17 then return end
   if address==0xff83ae70 then
    parent,parent_main=a,m
    log('ALLOC_PRE',string.format('entry=%08X parent=%08X parentMain=%08X a1=%08X a7=%08X freeHead=%08X',at,a,m,state.A1.value,state.A7.value,p:read_u32(0x01068e50)))
    lists('ALLOC_PRE_LISTS')
   else
    task=state.A0.value
    log('ALLOC_POST',string.format('entry=%08X task=%08X parent=%08X parentMain=%08X taskID=%d resume=%08X owner=%08X',at,task,a,m,valid(task)and p:read_u16(task+0x20)or -1,valid(task)and p:read_u32(task+0xe0)or 0,valid(task)and p:read_u32(task+0xc0)or 0))
    if not valid(task)then log('INVALID','reason=group_task_pointer');task=nil;return end
    lists('ALLOC_POST_LISTS')
    local field=parent_main+0x190
    taps[#taps+1]=p:install_write_tap(field,field+31,'original parent attachment stores',function(where,data,mask)
     local shift=where-field;local before=p:read_u32(field)
     local merged=(before&(~(mask<<shift)))|((data&mask)<<shift)
     log('ATTACH_STORE',string.format('at=%08X data=%08X mask=%08X before=%08X merged=%08X pc=%08X a8=%08X a13=%08X',where,data,mask,before,merged,state.PC.value,state.A8.value,state.A13.value))
    end)
   end
  elseif task and not object and state.A13.value==parent_main and state.A0.value==task then
   object=state.A8.value
   log('CONSTRUCT',string.format('entry=%08X task=%08X object=%08X parent=%08X parentMain=%08X objectTask=%08X cache=%08X pose=%08X',at,task,object,parent,parent_main,valid(object)and p:read_u32(object+0x20)or 0,valid(object)and p:read_u32(object+0x1a0)or 0,valid(object)and p:read_u32(object+0x1d0)or 0))
   if not valid(object)then log('INVALID','reason=group_object_pointer');object=nil;return end
   lists('CONSTRUCT_LISTS')
  end
 end)
end
for _,item in ipairs({{'TASK',0x01068e50},{'OBJECT',0x01060130}})do
 local name,address=item[1],item[2]
 taps[#taps+1]=p:install_write_tap(address,address+31,'actual native effect free-list head stores',function(at,data,mask)
  local target=name=='TASK'and task or object
  if not action or not target then return end
  local shift=at-address;local before=p:read_u32(address)
  local merged=(before&(~(mask<<shift)))|((data&mask)<<shift)
  if merged~=target and before~=target then return end
  log('FREE_'..name..'_STORE',string.format('at=%08X data=%08X mask=%08X before=%08X merged=%08X target=%08X next=%08X pc=%08X a0=%08X a1=%08X a2=%08X a5=%08X a13=%08X',at,data,mask,before,merged,target,p:read_u32(target),state.PC.value,state.A0.value,state.A1.value,state.A2.value,state.A5.value,state.A13.value))
 end)
end
for _,item in ipairs({{'TASK',0xff80e250},{'TASK',0xff80e5d0},{'OBJECT',0xff8097d0},{'OBJECT',0xff8099c0}})do
 local name,address=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'original effect return after real free-list store',function(at)
  local target=name=='TASK'and task or object
  local head=name=='TASK'and 0x01068e50 or 0x01060130
  local returned=name=='TASK'and returned_task or returned_object
  if not action or not target or returned or at~=address or state.PC.value~=at+16 or p:read_u32(head)~=target then return end
  if name=='TASK'then returned_task=true else returned_object=true end
  log('RETURN_'..name,string.format('entry=%08X target=%08X head=%08X next=%08X pc=%08X a0=%08X a2=%08X',at,target,p:read_u32(head),p:read_u32(target),state.PC.value,state.A0.value,state.A2.value))
  lists('RETURN_'..name..'_LISTS')
 end)
end
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()if action then lists('STATE')end end)
emu.register_stop(function()
 log('RESULT',string.format('action=%d task=%08X object=%08X taskReturned=%d objectReturned=%d fullPortAcceptance=false',action or -1,task or 0,object or 0,returned_task and 1 or 0,returned_object and 1 or 0))
 for _,tap in ipairs(taps)do tap:remove()end
end)
