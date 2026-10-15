-- Preserve the original6478 executed failure. Native callback globals use a
-- separate environment; make the snapshot transport lexical to the driver.
local file=assert(io.open('mk2ks_current_continue_ram_v6478.lua','rb'))
local text=file:read('*a');file:close()
local inline=[=[do
 local raw,width,height=screen:pixels()
 assert(width==400 and height==254 and #raw==406400)
 print(string.format('MK2_CR_RGB frame=%d filename=%s bytes=%d hex=%s',frame,file,#raw,
  raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
end]=]
local count
text,count=text:gsub('"current_continue_rgb%(file,frame%)"',function()return 'function() return [=['..inline..']=] end'end)
assert(count==1,'Only missing lexical snapshot binding changes')
assert(load(text,'@mk2ks_current_continue_ram_v6478.lua::lexical_snapshot_binding'))()
