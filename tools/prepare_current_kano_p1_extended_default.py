"""Retain default controls beyond earlier field bound, same resource caps."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p1_subzero_guard_ready_v2_preparation'
out=sync.ROOT/'audit_current_kano_p1_extended_default_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text();assert source.count('frame>=120000')==1
source=source.replace('frame>=120000','frame>=140000').replace('maximum_fields=120000','maximum_fields=140000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p1_subzero_guard_ready_v2_runtime','audit_current_kano_p1_extended_default_runtime')
(out/'run.ps1').write_text(runner)
print('Samephysicaldefault/freshcoldrun;140000fieldceiling;180sec/320MiB/10MiB/no media')
