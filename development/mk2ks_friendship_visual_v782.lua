-- Read-only per-field palettes/body data around native Friendship setup.
dofile('mk2ks_native_friendship_probe_v782.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,action,window,tap=0,nil,nil,nil
local slots={{actor=0x01060220,main=0x01060260},{actor=0x01060df0,main=0x01060e30}}
local side=tonumber(os.getenv('MK2KS_FRIEND_SIDE')or'1')
local winner=os.getenv('MK2KS_FRIEND_WINNER');local id=({kano=17,sonya=18,cage=0,liu_kang=1})[winner]
local entry=id<17 and p:read_u32(0xff880d90+id*32)or 0xff800000+(id==17 and 0xf9a00 or 0xf9c00)*8
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  tap=p:install_read_tap(entry,entry+15,'Friendship visual action timing',function(at)
   if at==entry and window then action=action or frame end
  end)
 end
 if not window and frame>700 and p:read_u16(0x01061b00)==3 then window=frame end
end)
emu.register_frame_done(function()
 if not window then return end
 local age=action and frame-action or-1
 if age>240 and frame%8~=0 then return end
 for n,s in ipairs(slots)do
  local actor,main=p:read_u32(s.actor),p:read_u32(s.main)
  if valid(actor)and valid(main)then
   local bank=p:read_u16(actor+0x140)&0x7f00;local colors={}
   for i=0,64 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01800000+(bank+i)*16))end
   print(string.format('MK2_FRIEND_VISUAL frame=%d writes=0 assistance=none side=%d slot=%d age=%d actor=%08X main=%08X id=%d pose=%08X flags=%04X bank=%04X x=%d y=%d floor=%d stage_y=%d camera_x=%d colors=%s',frame,side,n,age,actor,main,p:read_u16(actor+0x1f0),p:read_u32(actor+0x1d0),p:read_u16(actor+0xf0),bank,p:read_i16(actor+0x90),p:read_i16(actor+0xb0),p:read_i16(main+0x200),p:read_i16(0x0105ecd0),p:read_i16(0x0105d350),table.concat(colors,',')))
  end
 end
 if age>=0 and age<=240 then manager.machine.screens[':screen']:snapshot('visual_field_'..age..'.png')end
end)
emu.register_stop(function()if tap then tap:remove()end end)
