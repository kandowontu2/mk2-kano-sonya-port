-- One original physical controller; complete current cold/state/visual chain.
dofile('mk2ks_native_selector_cpu_first_round_projectile.lua')
local file=assert(io.open('mk2ks_current_tomb_winner_mix_observer_v5779.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and frame<=origin+1801 end')
replace('0xff8bdfe0,0xff8bdfef','0xffffb000,0xffffb00f')
replace('at~=0xff8bdfe0','at~=0xffffb000')
replace("p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])",
 'p:read_u16(a+0x1f0)~=17')
-- All19 current sample channels, including all five private finisher channels.
local count=0
source=source:gsub('for n=0,13 do',function()count=count+1;return 'for n=0,18 do'end)
assert(count==2)
count=0
source=source:gsub('for channel=0,13 do',function()count=count+1;return 'for channel=0,18 do'end)
assert(count==2)
replace("assert(#taps==15,'Every audio observer retained')\n frame=frame+1",
 [[assert(#taps==15,'Every audio observer retained')
 frame=frame+1
 if not origin and frame>700 and p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and p:read_u16(0x01060280)==17 and p:read_u16(0x01060e50)==17 then
  local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
  if valid(a)and valid(m)and p:read_u16(a+0x1f0)==17 and p:read_u32(m+0xc0)==a then
   origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=17',origin,a,m))
  end
 end]])
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin and frame>=origin+1800 and frame<=origin+1801,'Both whole sound ROM checks and actual full-match terminal')")
assert(load(source,'@whole_original_current19channel_projectile_PCM','t',_G))()
