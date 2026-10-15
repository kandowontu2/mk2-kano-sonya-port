"""Real both-Down Tomb drop controls and sparse native branch observations."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_native_tomb_pressed_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
needle=' -- A normal paid challenger after an expired finish window. Never touch state.'
assert source.count(needle)==1
source=source.replace(needle,""" if action and frame-action>=32 and frame-action<64 then
  press(1,'Down');press(2,'Down')
  log('DROP_INPUT','age='..(frame-action))
 end
"""+needle)
source+='''
for _,entry in ipairs({0xff8eb0d0,0xff8eb150,0xff80ec20,0xff8eb1a0,0xff8eb1b0,0xff8eb200,0xff8eb290,0xff876650,0xff8eb3c0,0xff8eb400})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native Tomb branch',function(at)
  if not action or at~=entry or cpu.PC.value~=at+16 then return end
  local victim=sample(3-side)
  if not victim or cpu.A8.value~=victim.actor then return end
  log('DROP_BRANCH',string.format('entry=%08X pc=%08X a0=%08X a8=%08X a13=%08X actor=%08X main=%08X id=%d io0=%08X',
   entry,cpu.PC.value,cpu.A0.value,cpu.A8.value,cpu.A13.value,victim.actor,victim.main,victim.id,p:read_u32(0x01600000)))
 end)
end
'''
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_tomb_kano_p1_runtime','audit_current_native_tomb_pressed_kano_p1_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared native physical both-Down age32..63; same earned controller/no media/caps')
