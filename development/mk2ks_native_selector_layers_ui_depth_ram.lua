-- Explicit passive render-list completion, including genuinely empty transitions.
local f=assert(io.open('mk2ks_native_anchor_ui_depth_ram.lua','rb'))
local source=f:read('a');f:close()
local before='    end\n    local raw,w,h=screen:pixels()'
local after=[=[    end
    print(string.format('MK2_ANCHOR_UI_DEPTH_COMPLETE seq=%d label=%s frame=%d count=%d writes=0 assistance=none',snapshots,label,frame,n))
    local raw,w,h=screen:pixels()]=]
local at=assert(source:find(before,1,true))
assert(not source:find(before,at+#before,true),'One explicit native list completion')
source=source:sub(1,at-1)..after..source:sub(at+#before)
assert(load(source,'@mk2ks_native_anchor_ui_depth_ram.lua::explicit_empty_list_receipt','t',_ENV))()
