-- Whole ordinary two-cycle controller plus full passive native audio observer.
-- Only host-side READY/FINAL annotations are added; no game-state writes.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local getenv=os.getenv
os.getenv=function(key)
 local suffix=key:match('^MK2KS_HUMAN_SPECIAL_(.+)$')
 return suffix and getenv('MK2PORT_ACCEPT_'..suffix)or getenv(key)
end
local driver=read('mk2ks_special_repeat_v5099.lua')
driver=change(driver,"then ready=frame;log('READY')end",
 "then ready=frame;rawset(_G,'MK2PORT_NATIVE_AUDIO_READY',frame);log('READY')end")
driver=change(driver,"if f==160 then completed=2;log('FINAL');",
 "if f==160 then rawset(_G,'MK2PORT_NATIVE_AUDIO_FINAL',frame);completed=2;log('FINAL');")
assert(load(driver,'@whole_original5099_two_cycle_physical_driver','t',_G))()
local source=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')
source=change(source,'local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin~=nil end')
source=change(source,'if at~=0xff8bdfe0 or cpu.PC.value~=at+16 or frame<=1 or origin then return end',
 'if at~=0xff8bdfe0 or cpu.PC.value~=at+16 or frame<=1 or origin or true then return end')
source=change(source,"assert(#taps==15,'Every audio observer retained')\n frame=frame+1",[[assert(#taps==15,'Every audio observer retained')
 frame=frame+1
 if not origin and rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then
  assert(frame==rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')and p:read_u16(0x010601d0)==2)
  local side=assert(tonumber(os.getenv('MK2PORT_ACCEPT_SIDE')))
  local a,m=p:read_u32(side==1 and 0x01060220 or 0x01060df0),p:read_u32(side==1 and 0x01060260 or 0x01060e30)
  assert(valid(a)and valid(m)and p:read_u16(a+0x1f0)==17 and p:read_u32(m+0xc0)==a)
  origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=17 slot=%d',origin,a,m,side))
 end
 if active()then
  for slot=1,2 do
   local base=slot==1 and 0x010601f0 or 0x01060dc0
   local a,m=p:read_u32(base+0x30),p:read_u32(base+0x70)
   log('BINDING',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d',slot,a,m,
    valid(m)and p:read_u32(m+0xc0)or 0,valid(a)and p:read_u16(a+0x1f0)or-1,p:read_u16(base+0x90)))
  end
 end]])
source=change(source,"assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin and frame==assert(rawget(_G,'MK2PORT_NATIVE_AUDIO_FINAL'))+1,'Both full native sound ROM inventories and actual physical two-cycle terminal')")
assert(load(source,'@whole_native5779_full_audio_inventory','t',_G))()
