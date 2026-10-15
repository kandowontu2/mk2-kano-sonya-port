-- Read-only provenance layered on the unchanged genuine-input stage driver.
dofile('mk2ks_native_stage_performer_v806.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local side=tonumber(assert(os.getenv('MK2KS_STAGE_SIDE')))
local actor_at=side==1 and 0x01060df0 or 0x01060220
local main_at=side==1 and 0x01060e30 or 0x01060260
local frame=0
local actor,taps=0,{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,s)print(string.format('MK2_STAGE_PROVENANCE_%s frame=%d writes=0 assistance=none %s',tag,frame,s))end
local function release()for _,t in ipairs(taps)do t:remove()end;taps={}end
emu.register_frame(function()
 frame=frame+1
 local a=p:read_u32(actor_at)
 if a~=actor then
  release();actor=a
  if valid(a)then
   for _,offset in ipairs({0xb0,0x60,0x20})do
    local width=offset==0xb0 and 16 or 32
    taps[#taps+1]=p:install_write_tap(a+offset,a+offset+width-1,'stage victim motion provenance',function(at,value,mask)
     if p:read_u16(0x01061ac0)~=1 or p:read_u16(0x01061b00)==0 then return end
     log('MOTION',string.format('actor=%08X main=%08X id=%d offset=%X at=%08X before=%08X value=%08X mask=%08X pc=%08X a8=%08X a13=%08X in0=%04X mode=%d',
      actor,p:read_u32(main_at),p:read_u16(actor+0x1f0),offset,at,p:read_u32(at),value,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x01600020),p:read_u16(0x010601d0)))
    end)
   end
  end
 end
 if valid(actor)and p:read_u16(0x01061ac0)==1 and p:read_u16(0x01061b00)~=0 then
  local main=p:read_u32(main_at)
  log('FIELD',string.format('actor=%08X main=%08X id=%d y=%d vy=%08X gravity=%08X action=%04X in0=%04X mode=%d',
   actor,main,p:read_u16(actor+0x1f0),p:read_i16(actor+0xb0),p:read_u32(actor+0x60),p:read_u32(actor+0x20),valid(main)and p:read_u16(main+0x1f0)or 0,p:read_u16(0x01600020),p:read_u16(0x010601d0)))
 end
end)
emu.register_stop(function()release();log('RESULT','guest_writes=0')end)
