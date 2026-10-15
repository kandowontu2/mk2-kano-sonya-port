-- Same real Kano P2/challenger controls; observe before the initial CPU cue.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true));return s:sub(1,a-1)..after..s:sub(b+1)
end
assert(os.getenv('MK2PORT_ACCEPT_MOVE')=='ball'and os.getenv('MK2PORT_ACCEPT_SIDE')=='2')
local source=read('mk2ks_launch_challenger_transition.lua')
source=change(source,' taps[#taps+1]])',' taps[#taps+1]\n]])')
source=change(source,"local source=read('mk2ks_current_challenger_v6486.lua')",[[local source=read('mk2ks_current_challenger_v6486.lua')
source=change(source,' frame=frame+1',' frame=frame+1\n if frame==2 then rawset(_G,\'MK2PORT_NATIVE_AUDIO_READY\',frame)end')]])
-- No CPU identity assertion against the human slot; record the actual slot.
source=change(source,"passive=change(passive,' if entry then\\n  local age=frame-entry',' if false and entry then\\n  local age=frame-entry')",[[passive=change(passive,' if entry then\n  local age=frame-entry',' if false and entry then\n  local age=frame-entry')
passive=change(passive,[=[   local actor=p:read_u32(side==1 and 0x01060220 or 0x01060df0)
   local main=p:read_u32(side==1 and 0x01060260 or 0x01060e30)
   assert(regs.A8.value==actor and regs.A13.value==main and p:read_u16(actor+0x1f0)==identity and p:read_u32(main+0xc0)==actor)
   entry=frame;serial=serial+1
   log('ENTRY',string.format('serial=%d slot=%d command=%04X pc=%08X actor=%08X main=%08X id=%d',serial,side,data,regs.PC.value,actor,main,identity))]=],[=[   local matched=false
   for slot=1,2 do
    local actor=p:read_u32(slot==1 and 0x01060220 or 0x01060df0)
    local main=p:read_u32(slot==1 and 0x01060260 or 0x01060e30)
    if regs.A8.value==actor and regs.A13.value==main then
     local id=p:read_u16(actor+0x1f0)
     assert(id==(data==0x6b03 and 17 or 18)and p:read_u32(main+0xc0)==actor)
     entry=frame;serial=serial+1;matched=true
     log('ENTRY',string.format('serial=%d slot=%d command=%04X pc=%08X actor=%08X main=%08X id=%d',serial,slot,data,regs.PC.value,actor,main,id))
    end
   end
   assert(matched,'Actual current native startup owner')]=])
passive=change(passive,[=[  assert(frame==rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')and p:read_u16(0x010601d0)==2)
  local side=assert(tonumber(os.getenv('MK2PORT_ACCEPT_SIDE')))
  local id=assert(({ball=17,square=18,bicycle=18})[os.getenv('MK2PORT_ACCEPT_MOVE')])
  local a,m=p:read_u32(side==1 and 0x01060220 or 0x01060df0),p:read_u32(side==1 and 0x01060260 or 0x01060e30)
  assert(valid(a)and valid(m)and p:read_u16(a+0x1f0)==id and p:read_u32(m+0xc0)==a)
  origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=%d slot=%d',origin,a,m,id,side))]=],[=[  assert(frame==2 and frame==rawget(_G,'MK2PORT_NATIVE_AUDIO_READY'))
  origin=frame;log('BEGIN','origin=2 scope=full_cold_audio_before_selection_and_CPU_launch')]=])]])
assert(load(source,'@same_physical_challenger_route_fullcold_audio_observer','t',_G))()
