"""Physical SonyaP2/stockJaxP1 selection, earned matches and native Tomb."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_native_tomb_stock_jax_sonya_p2_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old='local victim_id=id==17 and 18 or 17';assert source.count(old)==1
source=source.replace(old,'local victim_id=11 -- stock Jax selected through physical inputs')
assert ':write_' not in source and 'read_range' not in source and 'snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(sync.ROOT/'audit_current_native_tomb_sonya_p2_preparation/run_sonya_p2.ps1').read_text()
runner=runner.replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_native_tomb_sonya_p2_runtime','audit_current_native_tomb_stock_jax_sonya_p2_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared actualSonyaP2/stockJax11P1 Tomb,no forced arena/HP/identity,no media')
