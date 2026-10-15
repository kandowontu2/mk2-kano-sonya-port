-- Correct only exact source-defined snapshot return signature; retain the
-- entire original physical controller/audio observer and failed capture.
local file=assert(io.open('mk2ks_current_ui_audio_ram_v5427.lua','rb'))
local source=file:read('*a');file:close()
local before="local raw,width,height=manager.machine.video:snapshot_pixels()"
local after="local raw=manager.machine.video:snapshot_pixels()\n local width,height=manager.machine.video:snapshot_size()"
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@entire_UI_audio_only_snapshot_return_signature_corrected','t',_ENV))()
