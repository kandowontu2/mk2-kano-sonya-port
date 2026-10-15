"""Actual start/credit acceptance branch taps on unchanged physical request."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_challenger_input_reader_preparation'
out=sync.ROOT/'audit_current_native_challenger_credit_gate_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()+'''
for _,entry in ipairs({0xff8177b0,0xff817990,0xff8179b0,0xff817a10,0xff817a40,0xff817a70,
 0xffa53c50,0xffa53c70,0xffa53c80,0xffa53ce0,0xffa53cf0})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual challenger credit gate',function(at)
  if not join_start or frame-join_start>40 or at~=entry or cpu.PC.value~=entry+16 then return end
  log('JOIN_CREDIT_GATE',string.format('age=%d entry=%08X pc=%08X a0=%08X a1=%08X a2=%08X p1=%d p2=%d mode=%d',frame-join_start,entry,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(0x010601d0)))
 end)
end
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_challenger_input_reader_runtime','audit_current_native_challenger_credit_gate_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared passive native start/credit predicates, unchanged physical inputs,no media')
