-- Source-mapped original Kano first fatality: no guest-state assistance.
-- Previous physically earned trials are retained without modification.
local filename='mk3_native_secondary_kano_reference.lua'
local file=assert(io.open(filename,'r'))
local source=file:read('a');file:close()
local replacements={
 {"local raw,w,h=machine.screens[':screen']:pixels()",
  "local screen=machine.screens[':screen'];local raw=screen:pixels();local w,h=screen.width,screen.height"},
 {'if gap>45 then press(forward)','if gap>65 then press(forward)'},
 {"if gap>20 then press(forward)else command=frame;geometry('COMMAND_SPACING')end",
  "if gap<144 then press(x<y and 'left' or 'right')elseif gap>152 then press(forward)else command=frame;geometry('COMMAND_SPACING')end"},
 {'local ca=frame-command',
  "local ca=frame-command\n   for _,at in ipairs({4,14,24,34,44,70})do if ca==at then pending[#pending+1]='command_age_'..ca end end"},
 {'0xff991f70,0xffa5ef10',
  '0xff991f70,0xff992ee0,0xff993160,0xff9931f0,0xff993760,0xff992090,0xffa5ef10'}
}
for _,pair in ipairs(replacements)do
 local at=assert(source:find(pair[1],1,true))
 assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::original_source_distance'))()
