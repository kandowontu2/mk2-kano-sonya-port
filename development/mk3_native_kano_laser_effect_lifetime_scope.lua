-- Successor to frozen failed passive observer: valid/log lexical scope only.
-- Physical original gameplay/controller timing remains unchanged.
local filename='mk3_native_kano_laser_effect_lifetime.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local changes={
 {'local laser_effect_jobs,laser_effect_objects,laser_effect_serial={},{},0',
  'local valid,log\nlocal laser_effect_jobs,laser_effect_objects,laser_effect_serial={},{},0'},
 {'local additions={\n', [=[local additions={
 {'local function valid(a)','function valid(a)'},
 {'local function log(tag,content)','function log(tag,content)'},
]=]}
}
for _,pair in ipairs(changes)do
 local at=assert(source:find(pair[1],1,true));assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::scope_successor'))()
