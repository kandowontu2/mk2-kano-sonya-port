"""One cold P2 campaign with ordinary delayed coin/start, no guest assistance."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
out=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation'
assert not out.exists()
source=(old/'campaign.lua').read_text()
assert source.count('frame>=18000')==1 and source.count('maximum_fields=18000')==1
source=source.replace('frame>=18000','frame>=12000').replace('maximum_fields=18000','maximum_fields=12000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run_kano_p1.ps1').read_text()
changes={old.name+'/campaign.lua':out.name+'/campaign.lua',sync.sha(old/'campaign.lua'):sync.sha(lua),
 'audit_bounded_compact_kano_campaign_p1_runtime':'audit_current_sonya_p2_delayed_campaign_runtime',
 "MK2KS_TEST_FIGHTER='kano'":"MK2KS_TEST_FIGHTER='sonya'",
 "MK2KS_CAMPAIGN_SIDE='1'":"MK2KS_CAMPAIGN_SIDE='2'",
 "MK2KS_TEST_BOOT_FRAME='600'":"MK2KS_TEST_BOOT_FRAME='700'"}
for before,after in changes.items():
    assert before in runner;runner=runner.replace(before,after)
(out/'run.ps1').write_text(runner)
print('Prepared one bounded cold Sonya P2 campaign; only physical start timing changed')
