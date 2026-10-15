"""CPU0 physical kick/retreat test, preserving earned CPU8/2 policies."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_cage_early_retreat_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_hk_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
changes=[('(other.roster==8 or other.roster==2) then','(other.roster==8 or other.roster==2 or other.roster==0) then'),
 ('(other.roster==2 and 100 or 90)','((other.roster==2 or other.roster==0) and 100 or 90)'),
 ("if frame>=30000 then log('HOST_BOUND','maximum_fields=30000 full_campaign_acceptance=false')","if frame>=40000 then log('HOST_BOUND','maximum_fields=40000 full_campaign_acceptance=false')")]
for before,after in changes:
    assert source.count(before)==1,before
    source=source.replace(before,after)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_cage_early_retreat_runtime','audit_current_sonya_p2_kunglao_hk_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('CPU0-only policy extension;40k target/90sec/320MiB/10MiB/no media')
