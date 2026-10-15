-- Real Kano mirror damage earns a KO, native round reset, fresh roll and controls.
-- Whole prior physical route/passive audio retained; no game-state writes.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true))
 return s:sub(1,a-1)..after..s:sub(b+1)
end
local driver=read('mk2ks_special_repeat_v5099.lua')
driver=change(driver,'local attempt,completed=0,0','local attempt,completed=0,0\nlocal ko,reset,rearm,postfollowup=nil,nil,nil,nil')
driver=change(driver,'if ready then\n  local a,b=sample(1),sample(2)','if ready and not ko then\n  local a,b=sample(1),sample(2)')
driver=change(driver,'if attempt==2 then followup=frame+16 end','if attempt==99 then followup=frame+16 end')
driver=change(driver,'if recovered and attempt==1 and frame>=recovered+32 then','if recovered and attempt<4 and frame>=recovered+32 then')
driver=change(driver,"completed=1;log('REPEAT_READY');", "completed=attempt;log('REPEAT_READY');")
driver=change(driver,' if ready then\n  if not pair_live(a,b)then',[[
 if ready and not ko and a and b and(a.hp==0 or b.hp==0)then
  ko=frame;rawset(_G,'MK2PORT_KO_AT',frame)
  log('KO',string.format('p1HP=%d p2HP=%d mode=%d',a.hp,b.hp,mode))
 end
 if ko then
  if not reset and frame>ko+40 and pair_live(a,b)and clean(a)and clean(b)and a.hp==161 and b.hp==161 then
   reset=frame;rawset(_G,'MK2PORT_KO_RESET_AT',frame);log('ROUND_RESET','p1HP=161 p2HP=161')
  end
  if reset then
   local age=frame-reset
   if age==32 then
    rearm=frame;attempt=5;rawset(_G,'MK2PORT_DUAL_COMMAND',frame)
    log('REARM_COMMAND',string.format('p1HP=%d p2HP=%d',a.hp,b.hp));marks[frame]='reset_before'
   end
   if rearm then
    pulse(side,'Low Kick',frame-rearm,0,84)
    if not postfollowup and frame>rearm+100 and pair_live(a,b)and clean(a)and clean(b)and a.hp>0 and b.hp>0 then
     postfollowup=frame+16;log('REARM_RECOVERED','followup='..postfollowup);marks[frame]='reset_recovered'
    end
   end
   if postfollowup then
    local f=frame-postfollowup;local own,victim=side==1 and a or b,side==1 and b or a
    local direction=own.x<victim.x and'Right'or'Left'
    pulse(side,direction,f,0,8);pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)
    if f==160 then
     rawset(_G,'MK2PORT_NATIVE_AUDIO_FINAL',frame);completed=5;log('KO_FINAL','followup='..postfollowup)
     snapshot_ram('ko_round_final.png');rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)
    end
   end
  end
 end
 if ready and not ko then
  if not pair_live(a,b)then]])
-- The unchanged phase callback exits only after the final actual draw.
local dual=read('mk2ks_launch_dual_roll.lua')
dual=change(dual,"local source=read('mk2ks_launch_interrupt_v6680.lua')",
 "local source=read('mk2ks_launch_interrupt_v6680.lua')\nsource=change(source,\"local driver=read('mk2ks_special_repeat_v5099.lua')\",'local driver='.."..string.format('%q',string.format('%q',driver))..")")
assert(load(dual,'@actual_mirror_four_cycles_KO_round_reset_rearm','t',_G))()

local p=manager.machine.devices[':maincpu'].spaces.program
local frame=0
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()
 frame=frame+1
 if not rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then return end
 for slot,base in ipairs({0x010601f0,0x01060dc0})do
  local a,m=p:read_u32(base+0x30),p:read_u32(base+0x70)
  print(string.format('MK2_KO_FIELD frame=%d seconds=%.12f writes=0 assistance=none slot=%d mode=%d stage=%d state=%d actor=%08X main=%08X owner=%08X id=%d roster=%d hp=%d x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X action=%d flags=%04X body=%04X trail=%08X pose=%08X',
   frame,emu.time(),slot,p:read_u16(0x010601d0),p:read_u16(0x01061ac0),p:read_u16(base),a,m,
   valid(m)and p:read_u32(m+0xc0)or 0,valid(a)and p:read_u16(a+0x1f0)or-1,p:read_u16(base+0x90),p:read_u16(base+0x100),
   valid(a)and p:read_i16(a+0x90)or-32768,valid(a)and p:read_i16(a+0xb0)or-32768,valid(m)and p:read_i16(m+0x200)or-32768,
   valid(a)and p:read_u32(a+0x40)or 0,valid(a)and p:read_u32(a+0x60)or 0,valid(a)and p:read_u32(a+0x20)or 0,
   valid(m)and p:read_u16(m+0x1f0)or-1,valid(m)and p:read_u16(m+0x210)or 0,valid(a)and p:read_u16(a+0x160)or 0,
   valid(m)and p:read_u32(m+0x190)or 0,valid(a)and p:read_u32(a+0x1d0)or 0))
 end
end)
