"""One bounded resumed-match image per role; physical earned controller unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_continue_roles_preparation'
out=sync.ROOT/'audit_current_native_continue_visuals_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()+'''
emu.register_frame_done(function()
 if continued_fight and frame-continued_fight==30 then
  manager.machine.screens[':screen']:snapshot('continued_30.png')
  log('CONTINUE_VISUAL','age=30 count=1')
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=(base/f'run_{fighter}_p{side}.ps1').read_text()
  runner=runner.replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
  runner=runner.replace(f'audit_current_native_continue_{fighter}_p{side}_runtime',f'audit_current_native_continue_visual_{fighter}_p{side}_runtime')
  marker=' if($taskLimitReason){';assert runner.count(marker)==1
  runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object -Property Length -Sum).Sum\n if($taskMediaBytes -gt 128KB){$taskLimitReason='media_limit'}\n"+marker)
  runner=runner.replace("rawMedia='none'","rawMedia='one_png_max128KiB'")
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared four role checkpoints, one PNG each <=128KiB, total<=512KiB')
