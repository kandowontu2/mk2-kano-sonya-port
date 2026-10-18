-- Planning only: save an unedited, physically earned first Kintaro intro.
-- Never load a state here. This does not certify a campaign clear or video.
;(function()
 local m=manager.machine
 assert(m.system.supports_save,'Stock hardware does not support save states')
 local p=m.devices[':maincpu'].spaces.program
 local path=assert(os.getenv('KS_BOSS_CHECKPOINT_PATH'))
 local function word(a)return p:read_u8(a)|(p:read_u8(a+8)<<8)end
 local n,requested=0,nil
 local f=assert(io.open('boss_checkpoint.csv','w'))
 f:write('field,event,mode,map,p1selected,p2selected,p1hp,p2hp\n')
 emu.register_frame_done(function()
  n=n+1
  if not requested and word(0x010601d0)==7 and word(0x01061b30)==15 and
     word(0x01060280)==17 and word(0x01060e50)==12 then
   assert(not io.open(path,'rb'),'Never overwrite a planning checkpoint')
   requested=n
   f:write(string.format('%d,save_requested,7,15,17,12,%d,%d\n',n,word(0x010602f0),word(0x01060ec0)))
   f:flush();m:save(path)
  end
  if requested and n>=requested+4 then
   local state=io.open(path,'rb')
   if state then
    local size=assert(state:seek('end'));state:close()
    assert(size>1024,'Checkpoint file incomplete')
    f:write(string.format('%d,file_observed,%d,%d,%d,%d,%d,%d\n',n,
     word(0x010601d0),word(0x01061b30),word(0x01060280),word(0x01060e50),word(0x010602f0),word(0x01060ec0)))
    f:close();m:exit()
   elseif n>requested+120 then error('Scheduled checkpoint save did not produce a file') end
  end
 end)
end)()
