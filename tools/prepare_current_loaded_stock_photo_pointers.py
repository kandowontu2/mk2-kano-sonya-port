"""Three input-free fields, original 41 stock pointers plus actual lookup operand."""
import json,struct
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_loaded_dispatch_boundaries_preparation'
out=sync.ROOT/'audit_current_loaded_stock_photo_pointers_preparation'
assert not out.exists()
rom=sync.ROOT/'mk2/mk2-maincpu.bin'
data=rom.read_bytes();off=(0xff8f48f0-0xff800000)//8
expected=list(struct.unpack_from('<41I',data,off))
out.mkdir()
(out/'expected.json').write_text(json.dumps(dict(stockSHA256=sync.sha(rom),values=expected),indent=2)+'\n')
source='''local p=manager.machine.devices[':maincpu'].spaces.program
local frame=0
emu.register_frame_done(function()
 frame=frame+1;if frame~=3 then return end
 for i=0,40 do print(string.format('MK2_PHOTO_ROW index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0xfffa4800+i*32)))end
 print(string.format('MK2_PHOTO_OPERAND value=%08X writes=0 assistance=none',p:read_u32(0xff8447b0)))
 manager.machine:exit()
end)
'''
lua=out/'tables.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/tables.lua',out.name+'/tables.lua').replace(sync.sha(base/'tables.lua'),sync.sha(lua)).replace('audit_current_loaded_dispatch_boundaries_runtime','audit_current_loaded_stock_photo_pointers_runtime').replace('TotalSeconds -gt 90','TotalSeconds -gt 12')
(out/'run.ps1').write_text(runner)
print('Three input-free fields;12sec/320MiB/10MiB; no media')
