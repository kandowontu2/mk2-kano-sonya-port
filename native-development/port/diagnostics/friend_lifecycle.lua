-- Read-only native process observations; no retained pointer identities.
local lifecycleMachine=manager.machine
local lifecycleSpace=lifecycleMachine.devices[':maincpu'].spaces.program
local function life16(a) return lifecycleSpace:read_u8(a)|(lifecycleSpace:read_u8(a+8)<<8) end
local function life32(a) return life16(a)|(life16(a+16)<<16) end
local lifeActive=assert(tonumber(os.getenv('KS_ACTIVE_LIST')))
local lifeFrames=assert(tonumber(os.getenv('KS_CHICKEN_FRAMES')))
local lifeComplete=assert(tonumber(os.getenv('KS_CHICKEN_COMPLETE_WAKE')))
local lifeDeath=assert(tonumber(os.getenv('KS_F_DEATH')))
local lifeLog=assert(io.open('friend_lifecycle.csv','w'))
lifeLog:write('frame,mode,death,processes,danceContexts,completionContexts\n')
local lifeField=0
emu.register_frame_done(function()
 lifeField=lifeField+1
 local current=life32(lifeActive)
 local seen={}
 local count,dance,completion=0,0,0
 while current~=0 do
  assert(current>=0x01000000 and current<0x01400000,'Invalid process pointer')
  assert(not seen[current] and count<512,'Cyclic or oversized process list')
  seen[current]=true;count=count+1
  local animation=life32(current+0xa0)
  if animation>=lifeFrames and animation<lifeFrames+0x2a0 then dance=dance+1 end
  if life32(current+0xe0)==lifeComplete then completion=completion+1 end
  current=life32(current)
 end
 lifeLog:write(string.format('%d,%d,%d,%d,%d,%d\n',lifeField,life16(0x010601d0),life16(lifeDeath),count,dance,completion))
 lifeLog:flush()
end)
