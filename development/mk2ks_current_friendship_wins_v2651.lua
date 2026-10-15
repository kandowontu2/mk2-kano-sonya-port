-- Existing physical Friendship commands and audio observations are unchanged.
-- Only add read-only original winner-table observations on the current build.
dofile('mk2ks_native_friendship_audio_v790.lua')
local frame,tap=0,nil
local side=assert(tonumber(os.getenv('MK2KS_FRIEND_SIDE')))
local fighter=assert(os.getenv('MK2KS_FRIEND_WINNER'))
local case=assert(os.getenv('MK2KS_FRIEND_CASE'))
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()
 frame=frame+1
 if frame~=1 then return end
 local cpu=manager.machine.devices[':maincpu'];local p=cpu.spaces.program
 tap=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,'current Friendship native wins',function(at)
  if (at-0xfffef800)%32~=0 then return end
  local winner=p:read_u16(0x01061b00)
  if winner~=1 and winner~=2 then return end
  local s=slots[winner];local actor,main=p:read_u32(s.actor),p:read_u32(s.main)
  print(string.format('MK2_FRIEND_WIN frame=%d side=%d winner=%s case=%s writes=0 assistance=none slot=%d id=%d entry=%08X pc=%08X actor=%08X main=%08X owner=%08X actor_id=%d roster=%d health=%d,%d',
   frame,side,fighter,case,winner,(at-0xfffef800)//32,at,cpu.state.PC.value,actor,main,
   valid(main)and p:read_u32(main+0xc0)or 0,valid(actor)and p:read_u16(actor+0x1f0)or-1,p:read_u16(s.roster),
   p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
 end)
end)
emu.register_stop(function()if tap then tap:remove()end end)
