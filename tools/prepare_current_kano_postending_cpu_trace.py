"""Small passive post-ending CPU trace; identical failed-start inputs/bound."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_earned_postending_join_preparation'
out=sync.ROOT/'audit_current_kano_postending_cpu_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source+='''
emu.register_frame_done(function()
 if ending_completed and frame%120==0 then
  log('POST_ENDING_CPU_TRACE',string.format('pc=%08X a0=%08X a1=%08X a2=%08X a3=%08X a7=%08X a8=%08X a9=%08X a10=%08X a11=%08X a12=%08X a13=%08X mode=%d',cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A7.value,cpu.A8.value,cpu.A9.value,cpu.A10.value,cpu.A11.value,cpu.A12.value,cpu.A13.value,p:read_u16(0x010601d0)))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_earned_postending_join_runtime','audit_current_kano_postending_cpu_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Sameearnedroute/startattempt+50smallCPUrecords;180sec/320MiB/10MiB/no media')
