-- Original MK3 close-range reference. Only physical walking is added to the
-- unchanged native reference scenario; all taps remain observational.
assert(os.getenv('MK3_PROJECTILE_TARGET')=='sonya')
assert(os.getenv('MK3_KNIFE_GUARD')=='hit')
dofile('mk3_projectile_choreography_reference.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local fields=manager.machine.ioport.ports[':IN0'].fields
local frame=0
emu.register_frame(function()
 frame=frame+1
 if frame>=3800 and frame<3890 then
  local a,b=p:read_u32(0x010609b0),p:read_u32(0x01061560)
  assert(a>=0x01000000 and a<0x01400000 and b>=0x01000000 and b<0x01400000)
  local x,y=p:read_i16(a+0x90),p:read_i16(b+0x90)
  fields['P1 Right']:set_value(math.abs(x-y)>63 and 1 or 0)
  print(string.format('MK3_CLOSE_WALK frame=%d own=%d victim=%d gap=%d writes=0',frame,x,y,math.abs(x-y)))
 elseif frame==3890 then fields['P1 Right']:set_value(0)
 end
end)
