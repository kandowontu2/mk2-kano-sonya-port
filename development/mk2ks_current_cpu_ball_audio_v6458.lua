-- Entire original6290 physical match, full native5779 audio, RAM transport.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
assert(load(read('mk2ks_current_kano_cpu_extended_ram_v6290.lua'),'@whole_original6290_physical_RAM','t',_G))()
local source=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')
local function replace(before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and frame<=origin+1802 end')
-- Retain the original observer inventory, but do not let its Tomb-specific
-- origin select this ball window. The physical pre-entry field is authoritative.
replace('if at~=0xff8bdfe0 or cpu.PC.value~=at+16 or frame<=1 or origin then return end',
 'if at~=0xff8bdfe0 or cpu.PC.value~=at+16 or frame<=1 or origin or true then return end')
replace("assert(#taps==15,'Every audio observer retained')\n frame=frame+1",[[assert(#taps==15,'Every audio observer retained')
 frame=frame+1
 if frame==1813 then
  assert(p:read_u16(0x010601d0)==7 and p:read_u16(0x01060280)==17 and p:read_u16(0x01060e50)==17,'Exact qualified Kano mirror pre-entry')
  local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
  assert(valid(a)and valid(m)and p:read_u16(a+0x1f0)==17 and p:read_u32(m+0xc0)==a,'Actual native CPU Kano owner')
  origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=17',origin,a,m))
 end
 if active()then
  for slot=1,2 do
   local base=slot==1 and 0x010601f0 or 0x01060dc0
   local a,m=p:read_u32(base+0x30),p:read_u32(base+0x70)
   log('BINDING',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d',slot,a,m,
    valid(m)and p:read_u32(m+0xc0)or 0,valid(a)and p:read_u16(a+0x1f0)or-1,p:read_u16(base+0x90)))
  end
 end]])
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin==1813 and frame==3615,'Both complete sound ROM checks and unchanged original6293 terminal')")
assert(load(source,'@whole_native_CPU_Kano_ball_audio','t',_G))()
