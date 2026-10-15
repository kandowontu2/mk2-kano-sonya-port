"""Pay native two-credit price during actual CPU voice, join before cry EOF."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_battle_audio_join_selection_preparation'
out=sync.ROOT/'audit_current_cpu_sonya_active_voice_join_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
coin="if age>=1 and age<5 then join_coin:set_value(1);log('JOIN_INPUT','button=Coin_1 age='..age)end"
assert source.count(coin)==1
source=source.replace(coin,"if (age>=1 and age<5) or (age>=41 and age<45) then join_coin:set_value(1);log('JOIN_INPUT','button=Coin_1 age='..age)end")
start="if age>=8 and age<12 then join_button:set_value(1);log('JOIN_INPUT','button=Start_1 age='..age)end"
assert source.count(start)==1
source=source.replace(start,"if age>=64 and age<68 then join_button:set_value(1);log('JOIN_INPUT','button=Start_1 age='..age)end")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_native_battle_audio_join_selection_runtime','audit_current_cpu_sonya_active_voice_join_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared two real coin pulses/Start during CPU cry; scalar-only audio')
