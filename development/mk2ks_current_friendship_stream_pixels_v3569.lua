-- ASCII stdout carries read-only actual screen pixels directly to the
-- verifier, not a disk image or inferred rendering. Controls are unchanged.
dofile('mk2ks_current_friendship_stream_wins_v3568.lua')
local frame,window,count=0,nil,0
local p=manager.machine.devices[':maincpu'].spaces.program
local screen=manager.machine.screens[':screen']
local side=assert(tonumber(os.getenv('MK2KS_FRIEND_SIDE')))
local identity=assert(({kano=17,sonya=18})[os.getenv('MK2KS_FRIEND_WINNER')])
local physical=side==1 and 0x01060220 or 0x01060df0
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()
 frame=frame+1
 if not window and p:read_u16(0x010601d0)==2 and p:read_u16(0x01061b00)==3 then
  local actor,main=p:read_u32(physical),p:read_u32(physical+0x40)
  if valid(actor)and valid(main)and p:read_u16(actor+0x1f0)==identity and
     p:read_u16(physical+0x60)==identity and p:read_u32(main+0xc0)==actor then
   window=frame
   print(string.format('MK2_FSTREAM_WINDOW frame=%d id=%d actor=%08X main=%08X writes=0 assistance=none',frame,identity,actor,main))
  end
 end
end)
emu.register_frame_done(function()
 if not window or frame<window+1 or frame>window+1600 then return end
 local pixels,width,height=screen:pixels()
 assert(width==400 and height==254 and #pixels==width*height*4)
 count=count+1
 -- Numeric-word hex avoids Windows stdout newline conversion corrupting
 -- raw binary pixels. The collector consumes the complete ASCII payload
 -- into RAM and verifies every RGB byte, not just a screen digest.
 local hex=pixels:gsub('....',function(word)
  local value=string.unpack('<I4',word);return string.format('%08X',value)
 end)
 assert(#hex==#pixels*2)
 io.stdout:write(string.format('MK2_FSTREAM_PIXELS frame=%d age=%d width=%d height=%d bytes=%d encoding=u32le_as_hex_numeric writes=0 assistance=none\n',
  frame,frame-window,width,height,#pixels),hex,'\n')
end)
emu.register_stop(function()
 print(string.format('MK2_FSTREAM_RESULT frame=%d window=%d screenframes=%d writes=0 assistance=none',frame,window or-1,count))
end)
