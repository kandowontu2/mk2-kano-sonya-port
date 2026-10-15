-- Native mode4 is published before the cursor is initialized (FFFF sentinel).
-- Preserve prior observer failures; wait for the actual native valid roster.
-- Full6567 controller is reused, with paid inputs and this observer boundary.
local f=assert(io.open('mk2ks_single_continue_v6567.lua','rb'))
local source=f:read('*a');f:close()
local changes={
 {"local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Start',age,80,5)",
  "local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Coin',age,270,5);pulse('Start',age,310,5)"},
 {"if mode==4 and state==3 then reselect=frame;",
  "if mode==4 and state==3 and p:read_u16(slots[side].roster)<=18 then reselect=frame;"}}
for _,change in ipairs(changes)do
 local first,last=assert(source:find(change[1],1,true))
 assert(not source:find(change[1],last+1,true),'One exact native payment/initialization boundary change')
 source=source:sub(1,first-1)..change[2]..source:sub(last+1)
end
assert(load(source,'@mk2ks_single_continue_v6567.lua::native_cursor_initialized_boundary'))()
