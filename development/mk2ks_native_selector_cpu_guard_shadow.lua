-- Distinct real guard-hold route. Keep the entire original physical driver.
-- Observe owned fighter drawing in every actual live field, across round reset.
local file=assert(io.open('mk2ks_native_selector_cpu_blade_knife.lua','rb'))
local root=file:read('*a'):gsub('\r\n','\n');file:close()
local boundary="assert(load(source,'@whole_CPU_shadow_plus_whole_allocation','t',_G))()"
local first=assert(root:find(boundary,1,true));assert(not root:find(boundary,first+1,true))
local adapters=[==[
local function change(before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
 source=source:sub(1,at-1)..after..source:sub(at+#before)
end
change('local function window(f)return(f>=1870 and f<=1912)or(f>=2441 and f<=2509)end',[[
local first_live=nil
local function window(f)
 local a,b=sample(1),sample(2)
 local actual=p:read_u16(0x010601d0)==2 and a and b and
  a.owner==a.actor and b.owner==b.actor and a.id==17 and b.id==17 and
  a.roster==17 and b.roster==17 and a.state==1 and b.state==0
 if actual and not first_live then first_live=f end
 return actual and f<first_live+1800
end]])
local begin=assert(source:find('local checkpoints={',1,true))
local finish=assert(source:find('emu.register_frame(function()',begin,true))
source=source:sub(1,begin-1)..'local checkpoints={}\n'..source:sub(finish)
change(" move=frame<2200 and'blade'or'knife';attempt=frame<2200 and 1 or 2",' -- Move/serial below come only from actual executing CPU special entries.')
local entry_observer=[[
for _,item in ipairs({{'knife',0xffffb000},{'ball',0xffffde00},
                     {'blade',0xfff8cc00},{'choke',0xfff91400}})do
 taps[#taps+1]=p:install_read_tap(item[2],item[2]+15,'current actual CPU special visual window',function(at,data,mask)
  if at~=item[2]or regs.PC.value~=item[2]+16 then return end
  local own=sample(2)
  if not own or own.state~=0 or own.id~=17 or own.roster~=17 or own.owner~=own.actor or
     regs.A8.value~=own.actor or regs.A13.value~=own.main or p:read_u16(0x010601d0)~=2 then return end
  move=item[1];attempt=attempt+1
  for _,age in ipairs({0,3,8,16,24,40,49,50,64,96,128})do
   checkpoints[frame+age]='cpu_'..move..'_'..attempt..'_age'..age
  end
  marks[frame]=checkpoints[frame]
  phase_log('CPU_NATIVE_ENTRY',string.format('kind=%s entry=%08X pc=%08X actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d opcode=%04X mask=%04X',
   move,item[2],regs.PC.value,own.actor,own.main,own.owner,own.id,own.roster,own.state,data&0xffff,mask))
 end)
end
]]
change('emu.register_frame_done(function()\n if not ready then return end',
       entry_observer..'\nemu.register_frame_done(function()\n if not ready then return end')
]==]
root=root:sub(1,first-1)..adapters..'\n'..root:sub(first)
assert(load(root,'@whole_latest_CPU_root_live_shadow_guard_context','t',_G))()
