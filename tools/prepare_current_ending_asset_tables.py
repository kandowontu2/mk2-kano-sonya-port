"""Tiny read-only boot audit of actual loaded ending tables, not a clear."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_attract_preparation'
out=sync.ROOT/'audit_current_ending_asset_tables_preparation';assert not out.exists()
source=(old/'attract.lua').read_text().replace('frame>=12000','frame>=700').replace('maximum_fields=12000','maximum_fields=700')
source+='''
emu.register_frame_done(function()
 if frame~=600 then return end
 local copied=0
 for page=0,1 do
  local original=page==0 and 0xff8f5550 or 0xff8f59d0
  local relocated=0xff800000+(page==0 and 0xf4a00 or 0xf4b00)*8
  for index=0,35 do
   assert(p:read_u32(original+index*32)==p:read_u32(relocated+index*32))
   copied=copied+1
  end
  for fighter=0,1 do
   local id=17+fighter
   for segment=0,(page==0 and 2 or 1)do
    local ptr=p:read_u32(relocated+(id*3+segment)*32)
    local expected=0xff800000+(0xf4c00+(fighter*5+(page==0 and 0 or 3)+segment)*0xc0)*8
    assert(ptr==expected)
    local template=p:read_u32(original+(8*3+segment)*32)
    for byte=0,23 do assert(p:read_u8(ptr+byte*8)==p:read_u8(template+byte*8))end
    local hex=''
    for byte=0,167 do
     local value=p:read_u8(ptr+(24+byte)*8)
     if value==0 then break end
     hex=hex..string.format('%02X',value)
    end
    log('ENDING_SCRIPT',string.format('id=%d page=%d segment=%d ptr=%08X template=%08X header_exact=true texthex=%s',id,page,segment,ptr,template,hex))
   end
   if page==1 then assert(p:read_u32(relocated+(id*3+2)*32)==0)end
   local row=50+fighter*2+page
   local photo=p:read_u32(0xff800000+0xf4900*8+row*32)
   assert(photo>=0x07100000 and photo<0x07200000)
   log('ENDING_PHOTO',string.format('id=%d page=%d row=%d ptr=%08X',id,page,row,photo))
  end
 end
 log('ENDING_STOCK','preserved_pointers='..copied..' own_headers=10 page2_terminators=2')
end)
'''
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text().replace(old.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(old/'attract.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_current_attract_runtime','audit_current_ending_asset_tables_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared700field read-only own ending table audit; no media or forced campaign')
