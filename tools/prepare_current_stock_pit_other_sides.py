"""Opposite-slot Pit roles, same earned seven-match standingHK route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_pit_longkick_preparation'
out=sync.ROOT/'audit_current_stock_pit_other_sides_preparation'
assert not out.exists();out.mkdir()
for case,side,fighter,victim in (('sonya_p1_kitana',1,'sonya',4),('kano_p2_subzero',2,'kano',8)):
    source=(base/'stage.lua').read_text()
    old='local victim_id=id==17 and 18 or 17'
    assert source.count(old)==1
    source=source.replace(old,'local victim_id='+str(victim))
    assert ':write_' not in source and ':snapshot(' not in source
    lua=out/(case+'.lua');lua.write_text(source)
    runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/'+case+'.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_native_pit_longkick_kano_p1_runtime','audit_current_stock_pit_'+case+'_runtime')
    runner=runner.replace("$env:MK2KS_STAGE_WINNER='kano'","$env:MK2KS_STAGE_WINNER='"+fighter+"'").replace("$env:MK2KS_STAGE_SIDE='1'","$env:MK2KS_STAGE_SIDE='"+str(side)+"'")
    (out/(case+'.ps1')).write_text(runner)
print('Prepared2stockPitroles,no media,90sec/320MiB per run')
