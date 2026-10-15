-- Read-only native palette allocation, reference count, reset and teardown.
-- Keep the existing physical inputs, rendering and real task/sprite observers.
dofile('mk2ks_current_friendship_lifecycle_v2715.lua')
local cpu=manager.machine.devices[':maincpu']
local p,state=cpu.spaces.program,cpu.state
local side=assert(tonumber(os.getenv('MK2KS_FRIEND_SIDE')))
local fighter=assert(os.getenv('MK2KS_FRIEND_WINNER'))
assert(fighter=='kano','Kano bubble palette lifecycle only')
local physical=side==1 and 0x01060220 or 0x01060df0
local frame,action,parent,parent_main,object,palette=0,nil,nil,nil,nil,nil
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print(string.format('MK2_CHILD_PAL_%s frame=%d fighter=%s side=%d writes=0 assistance=none %s',tag,frame,fighter,side,value or''))
end
local function table_state(tag)
 local words={}
 for index=0,59 do
  local cell=0x0105bb30+index*0x40
  words[#words+1]=string.format('%08X:%04X:%04X',p:read_u32(cell),p:read_u16(cell+0x20),p:read_u16(cell+0x30))
 end
 log(tag,string.format('table=%s object=%08X objectPalette=%04X objectPose=%08X objectCache=%08X physical=%08X physicalMain=%08X mode=%d clock=%d',table.concat(words,','),object or 0,object and p:read_u16(object+0x140)or 0,object and p:read_u32(object+0x1d0)or 0,object and p:read_u32(object+0x1a0)or 0,p:read_u32(physical),p:read_u32(physical+0x40),p:read_u16(0x010601d0),p:read_u16(0x0105d090)))
end
local action_address=0xff800000+0xf9a00*8
taps[#taps+1]=p:install_read_tap(action_address,action_address+15,'native palette lifetime action context',function(at)
 if action or at~=action_address or state.PC.value~=at+16 then return end
 local a,m=p:read_u32(physical),p:read_u32(physical+0x40)
 if not valid(a)or not valid(m)or p:read_u16(a+0x1f0)~=17 or state.A8.value~=a or state.A13.value~=m then return end
 action,parent,parent_main=frame,a,m
 log('ACTION',string.format('entry=%08X actor=%08X main=%08X id=17',at,a,m));table_state('BASELINE')
end)
taps[#taps+1]=p:install_read_tap(0xff83af70,0xff83af7f,'actual bubble palette after constructor',function(at)
 if not action or object or at~=0xff83af70 or state.PC.value~=at+16 or state.A13.value~=parent_main then return end
 local a=state.A8.value
 if not valid(a)or not(0xfe9d2610<=p:read_u32(a+0x1d0)and p:read_u32(a+0x1d0)<=0xfe9d2790)then return end
 object,palette=a,p:read_u16(a+0x140)
 log('CONSTRUCT',string.format('entry=%08X task=%08X object=%08X parent=%08X parentMain=%08X palette=%04X paletteIndex=%d cache=%08X pose=%08X',at,state.A0.value,a,parent,parent_main,palette,palette&255,p:read_u32(a+0x1a0),p:read_u32(a+0x1d0)));table_state('CONSTRUCT_TABLE')
end)
taps[#taps+1]=p:install_write_tap(0x0105bb30,0x0105ca2f,'all actual original palette table stores',function(at,data,mask)
 if not action then return end
 log('TABLE_STORE',string.format('at=%08X before=%04X data=%04X mask=%04X pc=%08X a0=%08X a1=%08X a2=%08X a3=%08X a8=%08X a13=%08X',at,p:read_u16(at),data,mask,state.PC.value,state.A0.value,state.A1.value,state.A2.value,state.A3.value,state.A8.value,state.A13.value))
end)
for _,item in ipairs({{'ALLOC_ENTRY',0xff80cf60},{'ALLOC_RETURN',0xff80d570},{'DELETE_OBJECT',0xff80cad0},{'RELEASE_ENTRY',0xff80d580},{'RELEASE_RETURN',0xff80d790},{'RESET_ALL',0xff80cce0},{'RESET_LOWER',0xff80ce40},{'RESET_UPPER',0xff80ced0},{'SPRITE_POOL_RESET',0xff83f060}})do
 local tag,address=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual native palette lifetime boundary',function(at)
  if not action or at~=address or state.PC.value~=at+16 then return end
  log(tag,string.format('entry=%08X a0=%08X a1=%08X a2=%08X a3=%08X a8=%08X a13=%08X object=%08X palette=%04X',at,state.A0.value,state.A1.value,state.A2.value,state.A3.value,state.A8.value,state.A13.value,object or 0,palette or 0))
 end)
end
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()if action then table_state('STATE')end end)
emu.register_stop(function()
 log('RESULT',string.format('action=%d object=%08X palette=%04X fullPortAcceptance=false',action or -1,object or 0,palette or 0))
 for _,tap in ipairs(taps)do tap:remove()end
end)
