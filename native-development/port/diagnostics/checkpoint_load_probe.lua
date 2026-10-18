-- Explicit loaded-state PLANNING ONLY. No writes to guest RAM/registers.
local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local path=assert(os.getenv('KS_PLANNING_STATE'))
local state={loaded=false,fields=0,combat=0}
local function word(a)return p:read_u8(a)|(p:read_u8(a+8)<<8)end
local function long(a)return word(a)|(word(a+16)<<16)end
local f=assert(io.open('planning_load.csv','w'))
f:write('field,mode,map,p1selected,p2selected,p1char,p2char,p1hp,p2hp,p1match,p2match,round\n')
state.subscription=emu.add_machine_post_load_notifier(function()state.loaded=true end)
emu.register_frame_done(function()
 if not state.loaded then return end
 state.fields=state.fields+1
 local a,b=long(0x01060220),long(0x01060df0)
 local mode=word(0x010601d0)
 local c1=(a>=0x01000000 and a<0x01400000) and word(a+0x1f0) or -1
 local c2=(b>=0x01000000 and b<0x01400000) and word(b+0x1f0) or -1
 f:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',state.fields,mode,
  word(0x01061b30),word(0x01060280),word(0x01060e50),c1,c2,
  word(0x010602f0),word(0x01060ec0),word(0x01060310),word(0x01060ee0),word(0x01061af0)))
 if mode==2 then state.combat=state.combat+1 end
 if state.combat>=120 or state.fields>=1200 then f:close();m:exit() end
end)
m:load(path)
