-- Input-free capture: one native frame at a time, never collect frame arrays.
local screen=manager.machine.screens[':screen']
local pipe=assert(io.open(assert(os.getenv('MK2KS_VIDEO_PIPE')),'wb'))
pipe:setvbuf('no')
local frame=0
emu.register_frame_done(function()
 local raw=screen:pixels()
 local w,h=screen.width,screen.height
 assert(w==400 and h==254 and #raw==400*254*4)
 assert(pipe:write(raw))
 frame=frame+1
 if frame==1 or frame==120 then
  print(string.format('VIDEO_SMOKE frame=%d guest_seconds=%.12f width=%d height=%d bytes=%d',frame,manager.machine.time:as_double(),w,h,#raw))
 end
 if frame>=120 then pipe:close();pipe=nil;manager.machine:exit()end
end)
emu.register_stop(function()
 if pipe then pipe:close();pipe=nil end
 print('VIDEO_SMOKE_STOP frames='..frame..' inputs=0 guestwrites=0')
end)
