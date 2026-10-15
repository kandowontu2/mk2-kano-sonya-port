"""Meet native start price with two physical coin pulses, no setting/state changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_challenger_controls_preparation'
out=sync.ROOT/'audit_current_native_challenger_two_coins_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=1 and age<5 then join_coin:set_value(1);log('JOIN_INPUT','button=Coin_1 age='..age)end"
assert source.count(old)==1
source=source.replace(old,"if (age>=1 and age<5) or (age>=41 and age<45) then join_coin:set_value(1);log('JOIN_INPUT','button=Coin_1 age='..age)end")
old="if age>=24 and age<28 then join_button:set_value(1);log('JOIN_INPUT','button=Start_1 age='..age)end"
assert source.count(old)==1
source=source.replace(old,"if age>=64 and age<68 then join_button:set_value(1);log('JOIN_INPUT','button=Start_1 age='..age)end")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
for label in ('added','stock'):
 runner=(base/f'run_{label}.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
 runner=runner.replace(f'audit_current_native_challenger_{label}_control_runtime',f'audit_current_native_challenger_two_coins_{label}_runtime')
 (out/f'run_{label}.ps1').write_text(runner)
print('Prepared two physical coin pulses/normal Start1, natural added and stock CPU controls')
