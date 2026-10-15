-- The UI adapters explicitly load into_G; mirror diagnostic stubs there too.
-- This hardware/parser process runs no game or observer callbacks.
local filename='mk2ks_native_kano_laser_ui_parse.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local before="dofile('mk2ks_native_kano_laser_ui.lua')"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..'_G.manager=manager;_G.emu=emu;_G.load=load\n'..source:sub(a)
assert(load(source,'@'..filename..'::explicit_global_parser_namespace','t',_ENV))()
