-- Read-only original sprite allocation, actual blade attachment and retirement.
-- Delegates ALL physical selection/combat inputs to the established drivers.
local driver=assert(os.getenv('MK2KS_NATIVE_REGRESSION_DRIVER'))
assert(driver=='mk2ks_blade_interrupt_v4.lua' or driver=='mk2ks_blade_lifecycle_test.lua')
dofile('mk2ks_native_combat_regression_v2849.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local state=manager.machine.devices[':maincpu'].state
local frame,serial,stores=0,0,0
local taps,contexts,current,bound={},{},{},{}
local slots={{actor=0x01060220,main=0x01060260},{actor=0x01060df0,main=0x01060e30}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function pool(a)return a>=0x0102d6f0 and a<0x0105b950 and (a-0x0102d6f0)%0x210==0 end
local function log(tag,text)print(string.format('MK2_BLADE_ALLOC_%s frame=%d %s writes=0 assistance=none',tag,frame,text))end
local function chain(head,free)
 local at=p:read_u32(head);local nodes,seen={},{}
 while at~=0 do
  if free and at==0x0105b950 then return nodes,at,true end
  if free and at==0x00fe0190 and nodes[#nodes]==0x0105b740 then return nodes,at,true end
  if not pool(at) or seen[at] or #nodes>=358 then return nodes,at,false end
  seen[at]=true;nodes[#nodes+1]=at;at=p:read_u32(at)
 end
 return nodes,0,true
end
local function contains(nodes,target)for _,a in ipairs(nodes)do if a==target then return 1 end end;return 0 end
local function bind()
 if p:read_u16(0x010601d0)~=2 then return end
 for side,slot in ipairs(slots)do
  local actor,main=p:read_u32(slot.actor),p:read_u32(slot.main)
  if valid(actor) and valid(main) and p:read_u16(actor+0x1f0)==17 and p:read_u32(main+0xc0)==actor and not bound[main]then
   bound[main]=true
   taps[#taps+1]=p:install_write_tap(main+0x190,main+0x1af,'actual blade parent trail stores',function(at,data,mask)
    local ctx=current[main];if not ctx then return end
    local shift=at-(main+0x190);local before=p:read_u32(main+0x190)
    local merged=((before&(~(mask<<shift)))|((data&mask)<<shift))&0xffffffff
    log('TRAIL_STORE',string.format('context=%d side=%d actor=%08X main=%08X at=%08X before=%08X data=%04X mask=%04X merged=%08X pc=%08X a0=%08X a8=%08X a10=%08X a13=%08X op0=%04X op1=%04X',
     ctx.serial,side,actor,main,at,before,data,mask,merged,state.PC.value,state.A0.value,state.A8.value,state.A10.value,state.A13.value,p:read_u16(state.PC.value-32),p:read_u16(state.PC.value-16)))
    if state.PC.value==0xfff8d970 and merged==state.A10.value and pool(merged)then ctx.object=merged;ctx.attached=frame end
    if ctx.object and merged==0 and state.PC.value==0xff83f050 then ctx.detached=frame end
   end)
  end
 end
end
taps[#taps+1]=p:install_read_tap(0xfff8d800,0xfff8d80f,'actual blade create entry',function(at)
 if at~=0xfff8d800 or state.PC.value~=at+16 then return end
 local actor,main=state.A8.value,state.A13.value
 if not valid(actor) or not valid(main) or p:read_u16(actor+0x1f0)~=17 or p:read_u32(main+0xc0)~=actor then return end
 local side=p:read_u32(slots[1].actor)==actor and 1 or 2
 assert(p:read_u32(slots[side].main)==main,'Actual native blade parent Main')
 serial=serial+1;local ctx={serial=serial,parent=actor,main=main,side=side,start=frame}
 contexts[#contexts+1]=ctx;current[main]=ctx
 log('CREATE',string.format('context=%d side=%d actor=%08X main=%08X owner=%08X id=%d entry=%08X pc=%08X freeHead=%08X',serial,side,actor,main,p:read_u32(main+0xc0),p:read_u16(actor+0x1f0),at,state.PC.value,p:read_u32(0x01060130)))
end)
taps[#taps+1]=p:install_write_tap(0x01060130,0x0106014f,'original sprite free head store provenance',function(at,data,mask)
 stores=stores+1
 local shift=at-0x01060130;local before=p:read_u32(0x01060130)
 local merged=((before&(~(mask<<shift)))|((data&mask)<<shift))&0xffffffff
 local ctx=current[state.A13.value]
 local target=state.PC.value==0xff809150 and state.A0.value or state.PC.value==0xff8097d0 and state.A0.value or 0
 log('HEAD_STORE',string.format('sequence=%d context=%d at=%08X before=%08X data=%04X mask=%04X merged=%08X target=%08X targetNext=%08X pc=%08X a0=%08X a2=%08X a8=%08X a10=%08X a13=%08X sp=%08X returnPC=%08X op0=%04X op1=%04X op2=%04X',
  stores,ctx and ctx.serial or 0,at,before,data,mask,merged,target,pool(target)and p:read_u32(target)or 0,state.PC.value,state.A0.value,state.A2.value,state.A8.value,state.A10.value,state.A13.value,state.SP.value,p:read_u32(state.SP.value),p:read_u16(state.PC.value-48),p:read_u16(state.PC.value-32),p:read_u16(state.PC.value-16)))
end)
for _,entry in ipairs({{'CLEANUP',0xff83efd0},{'RETIRE',0xff840450}})do
 local kind,address=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual blade '..kind,function(at)
  if at~=address or state.PC.value~=address+16 then return end
  local ctx=current[state.A13.value];if not ctx or not ctx.object or ctx.detached then return end
  if kind=='RETIRE' and state.A0.value~=ctx.object then return end
  log(kind,string.format('context=%d actor=%08X main=%08X object=%08X trail=%08X entry=%08X pc=%08X a0=%08X a8=%08X a13=%08X',ctx.serial,ctx.parent,ctx.main,ctx.object,p:read_u32(ctx.main+0x190),address,state.PC.value,state.A0.value,state.A8.value,state.A13.value))
 end)
end
emu.register_frame(function()
 frame=frame+1;bind()
 if frame==1 then
  for _,range in ipairs({{0xff8090c0,0xff809280},{0xff8096c0,0xff809800},{0xff83efd0,0xff83f060},{0xfff8d800,0xfff8d980}})do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
 local active,activeStop,activeOK=chain(0x0105d480,false)
 local free,freeStop,freeOK=chain(0x01060130,true)
 for _,ctx in ipairs(contexts)do
  if ctx.object and(not ctx.detached or frame<=ctx.detached+2)then
   log('FIELD',string.format('context=%d side=%d parent=%08X main=%08X object=%08X attached=%d detached=%d trail=%08X pose=%08X descriptor=%08X palette=%04X active=%d free=%d activeValid=%d freeValid=%d freeStop=%08X freeCount=%d mode=%d parentOwner=%08X parentID=%d parentAction=%04X',
    ctx.serial,ctx.side,ctx.parent,ctx.main,ctx.object,ctx.attached or -1,ctx.detached or -1,p:read_u32(ctx.main+0x190),p:read_u32(ctx.parent+0x1d0),p:read_u32(ctx.object+0x1a0),p:read_u16(ctx.object+0x140),contains(active,ctx.object),contains(free,ctx.object),activeOK and 1 or 0,freeOK and 1 or 0,freeStop,#free,p:read_u16(0x010601d0),p:read_u32(ctx.main+0xc0),p:read_u16(ctx.parent+0x1f0),p:read_u16(ctx.main+0x1f0)))
  end
 end
end)
emu.register_stop(function()
 for _,ctx in ipairs(contexts)do log('CONTEXT_RESULT',string.format('context=%d side=%d parent=%08X main=%08X object=%08X start=%d attached=%d detached=%d',ctx.serial,ctx.side,ctx.parent,ctx.main,ctx.object or 0,ctx.start,ctx.attached or -1,ctx.detached or -1))end
 log('RESULT',string.format('contexts=%d headStores=%d',#contexts,stores))
 for _,tap in ipairs(taps)do tap:remove()end
end)
