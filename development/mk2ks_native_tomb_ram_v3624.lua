-- Preserve the complete original native observer, changing only its sinks.
-- No guest/register writes, physical-control changes, or forced random branch.
local previous={}
function MK2KS_TOMB_RAM_SAVE(file,raw)
 assert(#raw%4==0)
 local family=file:match('^display_(pre)_%d+%.bin$') or
  file:match('^display_(vram)_%d+%.bin$') or
  file:match('^display_(palette)_%d+%.bin$') or file
 local prior=previous[family]
 assert(not prior or #prior==#raw)
 local delta={}
 for first=1,#raw,64 do
  local block=raw:sub(first,first+63)
  if not prior or block~=prior:sub(first,first+63)then
   local hex=block:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end)
   delta[#delta+1]=string.format('%d:%s',(first-1)//64,hex)
  end
 end
 previous[family]=raw
 io.stdout:write(string.format('MK2_TOMB_RAM_BUFFER file=%s family=%s bytes=%d prior=%d blocks=%d block_bytes=64 encoding=u32le_numeric_hex_delta\n',file,family,#raw,prior and 1 or 0,#delta),table.concat(delta,','),'\n')
end
function MK2KS_TOMB_RAM_PIXELS(file)
 local raw=manager.machine.video:snapshot_pixels()
 assert(#raw==400*254*4)
 local hex=raw:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end)
 io.stdout:write(string.format('MK2_TOMB_RAM_PIXELS file=%s bytes=%d width=400 height=254 encoding=u32le_numeric_hex\n',file,#raw),hex,'\n')
end
local handle=assert(io.open('mk2ks_native_tomb_display_v2062.lua','rb'))
local source=handle:read('a');handle:close()
local count
source,count=source:gsub("dofile%('mk2ks_stage_branch_provenance_v1722%.lua'%)","dofile('mk2ks_current_stage_provenance_v3595.lua')")
assert(count==1)
source,count=source:gsub("local f=assert%(io%.open%(output%.%.%s*'/'%.%.file,'wb'%)%);f:write%(raw%);f:close%(%)","MK2KS_TOMB_RAM_SAVE(file,raw)")
assert(count==1)
source,count=source:gsub('screen:snapshot%(file%)','MK2KS_TOMB_RAM_PIXELS(file)')
assert(count==1)
assert(not source:find('io.open',1,true)and not source:find('screen:snapshot',1,true))
assert(load(source,'@mk2ks_native_tomb_display_v2062_RAM_sinks_only','t',_ENV))()
