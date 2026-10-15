"""Passive loaded-code check of ending scene continuation relocation."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_ending_asset_tables_preparation'
out=sync.ROOT/'audit_current_ending_scene_operands_preparation'
assert not out.exists()
source=(base/'attract.lua').read_text()
source+='''
emu.register_frame_done(function()
 if frame~=600 then return end
 for _,row in ipairs({
  {0xff844700,0x0270},{0xff8448a0,0x0270},
  {0xff844720,0x0170},{0xff844970,0x0170},
  {0xff844740,0x0190},{0xff844ab0,0x0190},
  {0xff844760,0x01b0},{0xff844b40,0x01b0}})do
  local actual=p:read_u16(row[1]);assert(actual==row[2])
  log('ENDING_SCENE_WORD',string.format('at=%08X actual=%04X expected=%04X',row[1],actual,row[2]))
 end
 for _,row in ipairs({
  {0xff8f51c0,0xff800000+0xf4a00*8},
  {0xff8f53e0,0xff800000+0xf4b00*8},
  {0xff8447b0,0xff800000+0xf4900*8}})do
  local actual=p:read_u32(row[1]);assert(actual==row[2])
  log('ENDING_SCENE_TABLE',string.format('at=%08X actual=%08X expected=%08X',row[1],actual,row[2]))
 end
 local count=0
 for index=0,40 do
  assert(p:read_u32(0xff8f48f0+index*32)==p:read_u32(0xff800000+0xf4900*8+index*32))
  count=count+1
 end
 log('ENDING_SCENE_STOCK','picture_rows_preserved='..count)
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(base/'attract.lua'),sync.sha(lua)).replace('audit_current_ending_asset_tables_runtime','audit_current_ending_scene_operands_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared700field passive ending-code audit; no media or forced scene')
