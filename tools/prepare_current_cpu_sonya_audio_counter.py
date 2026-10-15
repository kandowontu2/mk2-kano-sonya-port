"""Physical first-fight crouch/uppercut against CPU launch; passive audio observer."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_cpu_sonya_bicycle_audio_preparation'
out=sync.ROOT/'audit_current_cpu_sonya_audio_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
needle='   if leg_tactic and other.roster==18 then'
assert source.count(needle)==1
replacement="""   if frame-first_live<60 then
    local age=frame-first_live
    press('Down')
    if age<12 then press('Block')
    elseif age<24 and age%6<3 then press('High Punch')end
    log('CPU_AUDIO_COUNTER_INPUT',string.format('age=%d down=1 block=%d hp=%d',age,age<12 and 1 or 0,age>=12 and age<24 and age%6<3 and 1 or 0))
   elseif leg_tactic and other.roster==18 then"""
source=source.replace(needle,replacement)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_cpu_sonya_bicycle_audio_runtime','audit_current_cpu_sonya_audio_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared4000fields; physical opening crouch-block/HP; no assistance/media')
