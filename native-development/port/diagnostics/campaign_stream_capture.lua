-- Optional frame/audio recording support only; no guest writes or inputs.
;(function()
 local machine=manager.machine
 local space=machine.devices[':maincpu'].spaces.program
 local endpoint=assert(os.getenv('KS_CAMPAIGN_STREAM_PIPE'))
 local maximum=assert(tonumber(os.getenv('KS_CAMPAIGN_STREAM_MAX_FIELDS')))
 local n,count,last,finished=0,0,nil,false
 local raw,log=nil,nil
 local function word(a)return space:read_u8(a)|(space:read_u8(a+8)<<8)end
 local function capture(frame)
  assert(not last or frame==last+1,'Noncontiguous campaign capture')
  count=count+1;assert(count<=maximum,'Campaign capture exceeded field budget')
  local screen=machine.screens[':screen'];local pixels=screen:pixels()
  assert(screen.width==400 and screen.height==254 and #pixels==406400)
  assert(raw:write(pixels))
  log:write(string.format('%d,%.12f,400,254,406400\n',frame,machine.time:as_double()))
  log:flush();last=frame
 end
 ks_stream_capture_close=function(frame)
  if finished then return end
  if raw then
   if last~=frame then capture(frame) end
   raw:close();log:close();raw=nil;log=nil
  end
  finished=true
 end
 emu.register_frame_done(function()
  n=n+1
  if finished then return end
  if not raw and n>=3000 and word(0x010601d0)==4 then
   raw=assert(io.open(endpoint,'wb'))
   log=assert(io.open('campaign_capture.csv','w'))
   log:write('frame,seconds,width,height,bytes\n')
  end
  if raw then capture(n) end
 end)
end)()
