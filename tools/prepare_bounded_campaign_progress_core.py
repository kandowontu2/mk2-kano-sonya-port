"""Omit Kano-only read-only boss companion; physical campaign driver unchanged."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_campaign_progress_preparation'
out=sync.ROOT/'audit_bounded_campaign_progress_core_preparation';assert not out.exists();out.mkdir()
source=(old/'campaign.lua').read_text()
marker="dofile('mk2ks_campaign_shao_knife_observer_v3508.lua')"
assert source.count(marker)==1;source=source.replace(marker,'-- Kano-only read-only observer omitted; core physical policy unchanged.')
lua=out/'core.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
  runner=runner.replace(old.name+'/campaign.lua',out.name+'/core.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
  runner=runner.replace(f'audit_bounded_campaign_progress_{fighter}_p{side}_runtime',f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime')
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,onlyReadOnlyCompanionOmitted=True,physicalPolicyUnchanged=True,maximumFields=12000)))
