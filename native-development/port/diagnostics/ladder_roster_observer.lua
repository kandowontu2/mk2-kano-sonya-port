-- Bounded read-only ladder presentation capture; no controls or guest writes.
local machine=manager.machine
local space=machine.devices[':maincpu'].spaces.program
local function word(a) return space:read_u8(a)|(space:read_u8(a+8)<<8) end
local function long(a) return word(a)|(word(a+16)<<16) end
local mapPointer=assert(tonumber(os.getenv('KS_LADDER_MAP_POINTER')))
local worldY=assert(tonumber(os.getenv('KS_LADDER_WORLD_Y')))
local log=assert(io.open('ladder_roster.csv','w'))
log:write('frame,mode,worldY,mapPosition,mapPointer,roster\n')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if frame<3900 or frame>4350 then return end
 if frame%20==0 then
  local map=long(mapPointer)
  assert(map>=0xff800000 and map+17*16<0xffffffff)
  local ids={}
  for index=0,17 do ids[#ids+1]=word(map+index*16) end
  local y=word(worldY);if y>=32768 then y=y-65536 end
  log:write(string.format('%d,%d,%d,%d,%08x,%s\n',frame,word(0x010601d0),y,
   word(0x01061b30),map,table.concat(ids,';')))
  machine.screens[':screen']:snapshot(string.format('ladder_roster_%05d.png',frame))
 end
 if frame==4350 then log:close() end
end)
