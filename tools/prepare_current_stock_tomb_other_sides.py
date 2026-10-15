"""The remaining player-side arrangements, genuine stock opponent selections."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_stock_tomb_other_sides_preparation'
assert not out.exists();out.mkdir()
for name,victim,runner_path,old_runtime in (
    ('sonya_p1_kitana',4,'audit_current_native_tomb_sonya_preparation/run_sonya_p1.ps1','audit_current_native_tomb_sonya_p1_runtime'),
    ('kano_p2_subzero',8,'audit_current_native_tomb_p2_preparation/run_kano_p2.ps1','audit_current_native_tomb_kano_p2_runtime')):
    source=(base/'stage.lua').read_text()
    old='local victim_id=id==17 and 18 or 17';assert source.count(old)==1
    source=source.replace(old,'local victim_id='+str(victim)+' -- physical stock selection')
    assert ':write_' not in source and 'read_range' not in source and 'snapshot(' not in source
    lua=out/(name+'.lua');lua.write_text(source)
    runner=(sync.ROOT/runner_path).read_text().replace(base.name+'/stage.lua',out.name+'/'+name+'.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace(old_runtime,'audit_current_stock_tomb_'+name+'_runtime')
    (out/(name+'.ps1')).write_text(runner)
print('Prepared2actualstockTombroles,no media,90sec/320MiB/10MiB per run')
