"""Longer finite native Kano mirror, unchanged controller and host limits."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_kano_cpu_router_probe_preparation'
out=sync.ROOT/'audit_current_kano_cpu_mirror_long_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
source=source.replace('frame>=12000','frame>=20000').replace('maximum_fields=12000','maximum_fields=20000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(sync.ROOT/'audit_current_kano_cpu_mirror_probe_preparation/run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_kano_cpu_mirror_probe_runtime','audit_current_kano_cpu_mirror_long_runtime')
runner=runner.replace("'-str','400'","'-str','700'")
(out/'run.ps1').write_text(runner)
print('Prepared20000field true Kano mirror, original90sec/320MiB/10MiB caps')
