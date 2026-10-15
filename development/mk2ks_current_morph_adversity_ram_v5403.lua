-- Preserve original physical controller routes and every passive native tap.
-- Only change capture transport: guest in RAM; disable old PNG snapshots.
local name=os.getenv('MK2KS_MORPH_ADVERSITY_PHASE')=='ko' and
 'mk2ks_morph_adversity_v3226.lua' or 'mk2ks_morph_adversity_v3215.lua'
local file=assert(io.open(name,'r'));local source=file:read('*a');file:close()
local old="local file=assert(io.open(output..'/guest_maincpu.bin','wb'));file:write(raw);file:close()"
assert(source:find(old,1,true))
local replacement="print('MK2_CURRENT_MORPH_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02x',string.byte(c))end))"
local a,b=source:find(old,1,true);source=source:sub(1,a-1)..replacement..source:sub(b+1)
local snapshot="manager.machine.screens[':screen']:snapshot("
local count=0
while source:find(snapshot,1,true)do
 a,b=source:find(snapshot,1,true);source=source:sub(1,a-1)..'discard_snapshot('..source:sub(b+1);count=count+1
end
assert(count==2)
assert(not source:find('guest_maincpu.bin',1,true)and not source:find(':snapshot(',1,true))
assert(load('local function discard_snapshot(...)end\n'..source,'@current-morph-ram-v5403','t',_ENV))()
