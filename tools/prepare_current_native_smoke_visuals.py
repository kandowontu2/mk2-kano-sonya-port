"""Exactly two small native PNGs per unchanged earned secret/return driver."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_native_smoke_visuals_preparation'
assert not out.exists();out.mkdir()
for fighter,base_name in [('sonya','audit_current_sonya_smoke_transition_batched_preparation'),
                          ('kano','audit_current_kano_smoke_64_cadence_preparation')]:
    base=sync.ROOT/base_name
    source=(base/'stage.lua').read_text()
    assert ':write_' not in source and ':snapshot(' not in source
    source+='''
local visual_count=0
local fight_saved,return_saved=false,false
emu.register_frame_done(function()
 if secret and frame==secret and not fight_saved then
  assert(visual_count==0);screen:snapshot('secret_fight.png');fight_saved=true;visual_count=1
  log('VISUAL_SAVED','name=secret_fight.png count=1')
 end
 if returned and frame-returned==40 and not return_saved then
  assert(visual_count==1);screen:snapshot('normal_return.png');return_saved=true;visual_count=2
  log('VISUAL_SAVED','name=normal_return.png count=2')
 end
end)
'''
    lua=out/(fighter+'.lua');lua.write_text(source)
    runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/'+fighter+'.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
    runtime='audit_current_'+fighter+('_smoke_transition_batched_runtime' if fighter=='sonya' else '_smoke_64_cadence_runtime')
    assert runtime in runner
    runner=runner.replace(runtime,'audit_current_native_smoke_visuals_'+fighter+'_runtime')
    marker=' if($taskLimitReason){';assert runner.count(marker)==1
    runner=runner.replace(marker," $taskMediaBytes=(Get-ChildItem -LiteralPath $taskCase -File -Recurse -Filter '*.png' | Measure-Object Length -Sum).Sum\n if($taskMediaBytes -gt 112KB){$taskLimitReason='media_limit'}\n"+marker)
    runner=runner.replace("rawMedia='none'","rawMedia='two_png_max112KiB'")
    (out/(fighter+'.ps1')).write_text(runner)
print('Prepared exactly four PNG totalmax224KiB, same natural Kano/Sonya Smoke and normal return inputs; run serially')
