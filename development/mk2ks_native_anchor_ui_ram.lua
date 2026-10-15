-- Existing physical selector regression, native rasters transported in RAM.
-- No game-state/register/HP/AI/RNG writes and no persistent screenshots.
dofile('mk2ks_native_shang_drain_startup.lua')
local file=assert(io.open('mk2ks_selector_exit_test.lua','rb'))
local source=file:read('a');file:close()
local before='    manager.machine.video:snapshot()'
local replacement=[=[    local raw,w,h=screen:pixels()
    assert(w==400 and h==254 and #raw==406400)
    print(string.format('MK2_ANCHOR_UI_FRAME seq=%d label=%s frame=%d width=400 height=254 bytes=406400 writes=0 assistance=none hex=%s',snapshots,label,frame,
        raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))]=]
local first=assert(source:find(before,1,true))
assert(not source:find(before,first+#before,true),'Exactly one original snapshot boundary')
source=source:sub(1,first-1)..replacement..source:sub(first+#before)
assert(load(source,'@mk2ks_selector_exit_test.lua::same_inputs_ram_only_rasters','t',_ENV))()
