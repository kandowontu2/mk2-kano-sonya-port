-- Bounded read-only selection/ladder/first-combat screenshots, no inputs.
;(function()
 local machine=manager.machine
 local memory=machine.devices[':maincpu'].spaces.program
 local function word(address) return memory:read_u8(address)|(memory:read_u8(address+8)<<8) end
 local function long(address) return word(address)|(word(address+16)<<16) end
 local function body(address)
  if address<0x01000000 or address+0x210>=0x01400000 then return -1,0 end
  return word(address+0x1f0),long(address+0x1d0)
 end
 local log=assert(io.open('selection_ui.csv','w'))
 log:write('frame,mode,p1selected,p2selected,p1char,p2char,p1shape,p2shape\n')
 local frame=0
 local begin=tonumber(os.getenv('KS_SELECTION_UI_BEGIN') or '3500')
 assert(begin==3000 or begin==3500)
 emu.register_frame_done(function()
  frame=frame+1
  if frame<begin or frame>4500 then return end
  if (frame<=3950 and frame%4==0) or (frame>3950 and frame%10==0) then
   local c1,s1=body(long(0x01060220))
   local c2,s2=body(long(0x01060df0))
   log:write(string.format('%d,%d,%d,%d,%d,%d,%08x,%08x\n',frame,
    word(0x010601d0),word(0x01060280),word(0x01060e50),c1,c2,s1,s2))
   machine.screens[':screen']:snapshot(string.format('selection_ui_%05d.png',frame))
   log:flush()
  end
  if frame==4500 then log:close() end
 end)
end)()
