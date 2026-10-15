-- Source-correct current rendered snapshot target, no persistent media.
-- Same original physical walk-in controls; newly complete passive display data.
-- Original full native CPU/DMA/FIFO/latch observer, RAM-only transport instead
-- of ROM/VRAM/palette/PNG files. No character/AI/RNG/HP/state/register writes.
dofile('mk2ks_native_selector_sonya_human_kano_cpu.lua')
local file=assert(io.open('mk2ks_human_projectile_full_display_v1289.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("dofile('mk2ks_human_special_matrix_v3.lua')",'-- Physical inputs already loaded exactly once above.')
once("local output=assert(os.getenv('MK2KS_PROJECTILE_DISPLAY_OUT'))","local output='RAM_ONLY'")
once("local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))",'local side=2')
once("local move=assert(os.getenv('MK2KS_HUMAN_SPECIAL_MOVE'))","local move='knife'")
once('frame<=origin+960','frame<=origin+150')
once('f>origin+960','f>origin+150')
once([[local function save(file,raw)
 local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()
end]],[[local function save(file,raw)
 print(string.format('MK2_PROJECTILE_RAM frame=%d file=%s bytes=%d hex=%s writes=0 assistance=none',
  frame,file,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end]])
local first=assert(source:find('-- The original helper allocates A10',1,true))
local last=assert(source:find("taps[#taps+1]=p:install_read_tap(0xff840b60",first,true))
local actual_child=[====[
-- The current source-defined child entry supplies its ACTUAL native Main.
-- This is not a synthetic classic allocator callback or a guessed parent.
for _,address in ipairs({0xfffc6000,0xff8b6820})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual current Knife child display owner',function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or not active()then return end
  local own=actor(side);if not own then return end
  if address==0xff8b6820 then
   if cpu.A8.value~=child.actor or cpu.A13.value~=child.process then return end
   child.retired=frame
   log('FLOOR_CHILD_RETIRE',string.format('entry=%08X actor=%08X main=%08X parent=%08X parent_main=%08X pc=%08X opcode=%04X mask=%04X',
    address,child.actor,child.process,child.parent,child.parent_main,cpu.PC.value,data&0xffff,mask))
   return
  end
  local a,m=cpu.A8.value,cpu.A13.value
  assert(not child.actor and valid(a)and valid(m)and a~=own.actor and m~=own.main and
   p:read_u32(m+0xc0)==a and p:read_u32(m+0x230)==own.actor and p:read_u16(a+0x1f0)==17,
   'Actual current native child/Main and true Kano parent before first observed publication')
  child={actor=a,process=m,parent=own.actor,parent_main=own.main}
  log('FLOOR_CHILD_SPAWN',string.format('entry=%08X actor=%08X parent=%08X parent_main=%08X main=%08X id=%d roster=%d body=%04X facing=%04X pose=%08X cache=%08X native_actor_owner=%08X victim=%08X victim_main=%08X pc=%08X opcode=%04X mask=%04X',
   address,a,own.actor,own.main,m,p:read_u16(a+0x1f0),own.roster,p:read_u16(a+0x160),p:read_u16(a+0xf0),
   p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_u32(m+0x230),p:read_u32(m+0x140),p:read_u32(m+0x170),cpu.PC.value,data&0xffff,mask))
 end)
end
]====]
source=source:sub(1,first-1)..actual_child..source:sub(last)
once('screen:snapshot(file)',[[local video=manager.machine.video;local rgb=video:snapshot_pixels();local w,h=video:snapshot_size();assert(w==400 and h==254 and #rgb==406400)
 print(string.format('MK2_PROJECTILE_RGB frame=%d file=%s width=%d height=%d bytes=%d hex=%s writes=0 assistance=none',
  frame,file,w,h,#rgb,rgb:gsub('.',function(c)return string.format('%02X',c:byte())end))) ]])
-- No disk payloads, snapshot calls, writes to the guest, or second input driver.
assert(not source:find("'wb'",1,true)and not source:find('screen:snapshot(',1,true)and
 not source:match(':write_[ui]%d+')and not source:match('%.value%s*=[^=]'))
assert(load(source,'@whole_original_native_walkin_Knife_display_RAM_only','t',_G))()
