"""Passive actual-PC acid eligibility trace; unchanged physical late-hold input."""
import verify_native_source_sync as sync

sync.verify()
base = sync.ROOT / 'audit_current_native_deadpool_late_hold_preparation'
out = sync.ROOT / 'audit_current_native_deadpool_gate_trace_preparation'
assert not out.exists()
source = (base / 'stage.lua').read_text()
source += '''
for _,entry in ipairs({0xff871080,0xff8710a0,0xff8710c0,0xff871100,
 0xff871160,0xff871240,0xff871270,0xff8712a0,0xff8714d0,0xff871530})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'acid eligibility execution',function(at)
  if not command or at~=entry or cpu.PC.value~=entry+16 then return end
  local own=sample(side)
  if not own or cpu.A8.value~=own.actor then return end
  log('ACID_GATE',string.format('entry=%08X age=%d a0=%08X a3=%08X b2=%08X actor=%08X id=%d arena=%d finish=%d in2=%04X',
   entry,frame-command,cpu.A0.value,cpu.A3.value,cpu.B2.value,own.actor,own.id,
   p:read_u16(0x01061ac0),p:read_u16(0x01061b00),p:read_u16(0x01600020)))
 end)
end
'''
out.mkdir()
lua = out / 'stage.lua'
lua.write_text(source)
runner = (base / 'run.ps1').read_text()
runner = runner.replace(base.name+'/stage.lua', out.name+'/stage.lua')
runner = runner.replace(sync.sha(base/'stage.lua'), sync.sha(lua))
runner = runner.replace('audit_current_native_deadpool_late_hold_kano_p1_runtime',
                        'audit_current_native_deadpool_gate_trace_kano_p1_runtime')
(out / 'run.ps1').write_text(runner)
print('Prepared passive actual-PC gate trace; controller unchanged; no media')
