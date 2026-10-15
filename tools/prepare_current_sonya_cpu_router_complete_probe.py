"""Shorter declared deadline; same genuine controller and read-only router trace."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_cpu_router_probe_preparation'
out=sync.ROOT/'audit_current_sonya_cpu_router_complete_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
assert source.count('frame>=30000')==1 and source.count('maximum_fields=30000')==1
source=source.replace('frame>=30000','frame>=20000').replace('maximum_fields=30000','maximum_fields=20000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_cpu_router_probe_runtime','audit_current_sonya_cpu_router_complete_runtime')
(out/'run.ps1').write_text(runner)
checker=(sync.ROOT/'tools/qualify_current_sonya_cpu_router_probe.py').read_text()
checker=checker.replace('audit_current_sonya_cpu_router_probe_checked','audit_current_sonya_cpu_router_complete_checked')
checker=checker.replace('audit_current_sonya_cpu_router_probe_runtime','audit_current_sonya_cpu_router_complete_runtime')
checker=checker.replace(old.name,out.name).replace("['frame']=='30000'","['frame']=='20000'")
(out/'qualify.py').write_text(checker)
print('Prepared20000field physical router probe with unchanged host resource caps')
