-- Entire original2092 Pit movie/raster observer, followed by the exact passive
-- later-scanout transport from Tomb. TOMB tags name an inherited protocol only.
local f=assert(io.open('mk2ks_native_tomb_rejoin_display.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once("local f=assert(io.open('mk2ks_native_tomb_display_v2062.lua','rb'))",
 "local f=assert(io.open('mk2ks_native_pit_display_v2092.lua','rb'))")
once("once(\"dofile('mk2ks_stage_branch_provenance_v1722.lua')\",\"dofile('mk2ks_native_tomb_rejoin_provenance.lua')\")",
 "once(\"dofile('mk2ks_native_stage_performer_v806.lua')\",\"dofile('mk2ks_native_pit_rejoin_provenance.lua')\")")
once("once('\\nend\\n-- END v2062 full-render read-only observer','\\n'..post..'\\nend\\n-- END v2062 full-render read-only observer')",
 "once('\\nend\\n-- END v2092 full-render read-only observer','\\n'..post..'\\nend\\n-- END v2092 full-render read-only observer')")
once('MK2_CURRENT_TOMB_RENDER_DEADLINE','MK2_CURRENT_PIT_RENDER_DEADLINE')
assert(load(source,'@whole2092_Pit_then_exact_inherited_passive_later_scanout','t',_ENV))()
