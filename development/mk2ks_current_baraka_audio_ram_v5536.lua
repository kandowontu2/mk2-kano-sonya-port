-- Preserve failed5532 loader-scope counterexample; only supply its lexical
-- read closure to the complete original audio/controller observer namespace.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_baraka_audio_ram_v5532.lua','rb'))
local s=f:read('*a');f:close();s=s:gsub('\r\n','\n')
local before="assert(load(s,'@whole3939_original_DCS_routes_queue_port_ADSP_channels_and_PCM_Baraka_origin','t',_ENV))()"
local first,last=assert(s:find(before,1,true));assert(not s:find(before,last+1,true))
local after="assert(load(s,'@whole3939_original_DCS_routes_queue_port_ADSP_channels_and_PCM_Baraka_origin','t',setmetatable({read=read},{__index=_ENV})))()"
s=s:sub(1,first-1)..after..s:sub(last+1)
assert(load(s,'@entire5532_audio_wrapper_correct_lexical_read_transport','t',_ENV))()
