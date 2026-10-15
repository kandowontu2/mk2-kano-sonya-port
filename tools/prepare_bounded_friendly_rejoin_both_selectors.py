"""Reselect both native cursors after paid rejoin; preserve prior attempts."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_friendly_rejoin_preparation'
out=sync.ROOT/'audit_bounded_friendly_rejoin_both_selectors_preparation'
assert not out.exists()
out.mkdir()
for kind in ('friendship','babality'):
    original=old/(kind+'.lua')
    source=original.read_text()
    marker='if age==310 then css[victim_side]=nil;exits[victim_side]=nil;plans[victim_side]=nil end'
    assert source.count(marker)==1
    source=source.replace(marker,'if age==310 then for n=1,2 do css[n]=nil;exits[n]=nil;plans[n]=nil end end')
    lua=out/original.name
    lua.write_text(source)
    for fighter in ('kano','sonya'):
        for side in (1,2):
            runner=(old/f'run_{kind}_{fighter}_p{side}.ps1').read_text()
            runner=runner.replace(old.name+'/'+original.name,out.name+'/'+lua.name).replace(sync.sha(original),sync.sha(lua))
            runner=runner.replace(f'audit_bounded_rejoin_{kind}_{fighter}_p{side}_runtime',f'audit_bounded_rejoin_both_selectors_{kind}_{fighter}_p{side}_runtime')
            (out/f'run_{kind}_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared corrected physical rejoin: both native selectors')
