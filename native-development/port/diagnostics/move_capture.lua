-- Appended read-only observer: capture one actual own move and its recovery.
do
 local machine=manager.machine
 local space=machine.devices[':maincpu'].spaces.program
 local side=assert(tonumber(os.getenv('KS_CAPTURE_SIDE')))
 local wanted=assert(tonumber(os.getenv('KS_CAPTURE_ACTION')))
 local notBefore=assert(tonumber(os.getenv('KS_CAPTURE_NOT_BEFORE')))
 local minimum=assert(tonumber(os.getenv('KS_CAPTURE_MIN_FIELDS')))
 local maximum=assert(tonumber(os.getenv('KS_CAPTURE_MAX_FIELDS')))
 local normalCapture=os.getenv('KS_CAPTURE_NORMAL')=='1'
 local function word(a)return space:read_u8(a)|(space:read_u8(a+8)<<8)end
 local function long(a)return word(a)|(word(a+16)<<16)end
 local raw,log=nil,nil
 local frame,count,rest=0,0,0
 local finished=false
 local function close()
  if raw then raw:close();log:close();raw=nil;log=nil end
  finished=true
 end
 emu.register_frame_done(function()
  frame=frame+1
  if finished then return end
  local mode=word(0x010601d0)
  local proc=long(side==1 and 0x01060260 or 0x01060e30)
  if mode~=2 or proc<0x01000000 or proc>=0x01400000 then
   if raw then close()end
   return
  end
  local action=word(proc+0x1f0)
  if not raw and frame>=notBefore and action==wanted then
   raw=assert(io.open('finisher_capture.bgra','wb'))
   log=assert(io.open('finisher_capture.csv','w'))
   log:write('frame,seconds,width,height,bytes\n')
  end
  if raw then
   count=count+1;assert(count<=maximum,'Move capture exceeded bounded duration')
   local screen=machine.screens[':screen'];local pixels=screen:pixels()
   assert(screen.width==400 and screen.height==254 and #pixels==406400)
   assert(raw:write(pixels))
   log:write(string.format('%d,%.12f,400,254,406400\n',frame,machine.time:as_double()));log:flush()
   local otherReady=true
   if wanted==0x404 then
    local ownObject=long(side==1 and 0x01060220 or 0x01060df0)
    otherReady=ownObject>=0x01000000 and ownObject<0x01400000 and word(ownObject+0x1f0)==6
   end
   if wanted==0x216 or wanted==0x219 or normalCapture then
    local otherProc=long(side==1 and 0x01060e30 or 0x01060260)
    otherReady=otherProc>=0x01000000 and otherProc<0x01400000 and word(otherProc+0x1f0)==0x303
   end
   if action==0x303 and otherReady then rest=rest+1 else rest=0 end
   if rest>=8 and count>=minimum then close()end
  end
 end)
end
