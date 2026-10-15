-- Existing real coin/select/two-earned-round/held-HK controller, current build.
-- Stream actual initialized ROM/GFX and bounded native screens to host RAM.
local root=assert(os.getenv('MK2KS_CURRENT_ROOT'))
local path=root..'/mk2ks_mileena_earned_fixed_v3824.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local marker="dofile('mk2ks_cache_provenance_mileena_fixed_v3823.lua')"
local a,b=source:find(marker,1,true);assert(a and not source:find(marker,b+1,true))
source=source:sub(1,a-1).."dofile('"..root:gsub('\\','/').."/mk2ks_cache_provenance_mileena_fixed_v3823.lua')"..source:sub(b+1)
source=source..'\n'..[=[
local current_screen=manager.machine.screens[':screen']
local current_gfx=assert(manager.machine.memory.regions[':gfxrom'])
local current_shots={[0]=true,[8]=true,[16]=true,[24]=true,[32]=true,[64]=true,[128]=true,[600]=true}
local function current_buffer(tag,raw,detail)
 print('MK2_CURRENT_MILEENA_'..tag..' frame='..frame..' bytes='..#raw..' '..(detail or'')..' hex='..
       raw:gsub('.',function(c)return string.format('%02x',c:byte())end))
end
emu.register_frame_done(function()
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  current_buffer('GUEST',raw)
  local n=p:read_u32(0xff7b0040)+p:read_u32(0xff7b0080)
  assert(n>0 and n<=0x20000)
  local bytes={}
  for i=0,n-1 do bytes[#bytes+1]=string.char(current_gfx:read_u8(0x1f80000+i))end
  current_buffer('GFX',table.concat(bytes),'offset=1F80000')
 end
 if first then
  for slot=1,2 do
   local s=slots[slot];local actor,main=p:read_u32(s.actor),p:read_u32(s.main)
   if valid(actor)and valid(main)then
    print(string.format('MK2_CURRENT_MILEENA_FIELD frame=%d slot=%d mode=%d stage=%d stageY=%d flag=%d roster=%d state=%d hp=%d actor=%08X main=%08X owner=%08X id=%d pose=%08X xraw=%08X yraw=%08X floor=%d action=%d flags=%04X body=%04X bank=%04X writes=0 assistance=none',
     frame,slot,p:read_u16(0x010601d0),p:read_u16(0x01061ac0),p:read_i16(0x0105ecd0),p:read_u16(0x01061b00),
     p:read_u16(s.id),p:read_u16(s.state),p:read_u16(s.hp),actor,main,p:read_u32(main+0xc0),
     p:read_u16(actor+0x1f0),p:read_u32(actor+0x1d0),p:read_u32(actor+0x80),p:read_u32(actor+0xa0),
     p:read_i16(main+0x200),p:read_u16(main+0x1f0),p:read_u16(actor+0x160),p:read_u16(actor+0xf0),p:read_u16(actor+0x140)))
   else
    print(string.format('MK2_CURRENT_MILEENA_NO_ACTOR frame=%d slot=%d actor=%08X main=%08X writes=0 assistance=none',frame,slot,actor,main))
   end
  end
 end
 if action and current_shots[frame-action]then
  local raw,w,h=current_screen:pixels();assert(w==400 and h==254 and #raw==406400)
  current_buffer('RGB',raw,'age='..(frame-action)..' width='..w..' height='..h)
 end
end)
]=]
assert(load(source,'@'..path..'::current_read_only_mileena_v6081','t',_ENV))()
