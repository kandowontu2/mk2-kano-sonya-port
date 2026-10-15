-- Preserve the executed6221 observer. Use Kitana's original921 controller,
-- matching its already qualified current scene; other contexts use1021.
local file=assert(io.open('mk2ks_current_stock_finisher_audio_v6221.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique native controller/terminal adapter')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
if os.getenv('MK2KS_STOCK_KILLER')=='kitana'then
 replace("dofile('mk2ks_stock_extended_earned_ram_v3958.lua')","dofile('mk2ks_stock_earned_ram_v3918.lua')")
end
replace('frame==origin+751','frame==origin+750')
assert(load(source,'@whole_stock_finisher_audio_native_terminal_v6225','t',_ENV))()
