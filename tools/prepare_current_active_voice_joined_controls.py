"""Continue active CPU voice-cut join into own-ID physical two-player combat."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_cpu_sonya_active_voice_join_preparation'
out=sync.ROOT/'audit_current_active_voice_joined_controls_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if join_selection and frame-join_selection>=160 then log('JOIN_COMPLETE','selection_fields=160');manager.machine:exit()end"
assert source.count(old)==1
source=source.replace(old,"if join_selection and frame-join_selection==160 then log('JOIN_COMPLETE','selection_fields=160')end")
tested=(sync.ROOT/'audit_current_native_joined_controls_scoped_preparation/campaign.lua').read_text()
suffix=tested[tested.index('local joined_targets='):]
source+=suffix
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_cpu_sonya_active_voice_join_runtime','audit_current_active_voice_joined_controls_runtime')
runner=runner.replace("$env:MK2KS_TEST_FIGHTER='sonya'","$env:MK2KS_TEST_FIGHTER='sonya'\n$env:MK2KS_JOIN_P1='17'\n$env:MK2KS_JOIN_P2='18'")
(out/'run.ps1').write_text(runner)
print('Prepared active-voice paid join→true17/18→1600field physical controls; no media')
