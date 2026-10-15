-- Original native buttons, no emulated state writes. A pre-established
-- physical guard prevents the initial LP from becoming an ordinary hit.
local filename='mk3_native_secondary_kano_reference.lua'
local file=assert(io.open(filename,'r'))
local source=file:read('a');file:close()
local replacements={
 {"local raw,w,h=machine.screens[':screen']:pixels()",
  "local screen=machine.screens[':screen'];local raw=screen:pixels();local w,h=screen.width,screen.height"},
 {'if gap>45 then press(forward)','if gap>65 then press(forward)'},
 {'if gap>20 then press(forward)','if gap>65 then press(forward)'},
 {'local ca=frame-command',
  "local ca=frame-command\n   if ca>=6 and ca<14 then press('block')end\n   for _,at in ipairs({4,14,24,34,44,70})do if ca==at then pending[#pending+1]='command_age_'..ca end end"}
}
for _,pair in ipairs(replacements)do
 local at=assert(source:find(pair[1],1,true))
 assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::physical_guarded_command'))()
