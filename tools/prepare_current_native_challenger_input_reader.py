"""Bounded native IN1 consumer PC trace on unchanged physical challenger control."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_challenger_controls_preparation'
out=sync.ROOT/'audit_current_native_challenger_input_reader_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()+'''
local system_read_count=0
taps[#taps+1]=p:install_read_tap(0x01600010,0x0160001f,'actual challenger system reader',function(at,data,mask)
 if not join_start or frame-join_start>40 or system_read_count>=250 then return end
 system_read_count=system_read_count+1
 log('JOIN_SYSTEM_READ',string.format('age=%d at=%08X data=%04X mask=%04X pc=%08X count=%d',frame-join_start,at,data&0xffff,mask,cpu.PC.value,system_read_count))
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_added.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_challenger_added_control_runtime','audit_current_native_challenger_input_reader_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared<=250native IN1 reader records over41fields; unchanged challenger inputs/no media')
