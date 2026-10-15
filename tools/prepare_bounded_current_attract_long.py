"""Longer natural biography rotation, existing sparse observer and caps."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_attract_preparation'
out=sync.ROOT/'audit_bounded_current_attract_long_preparation';assert not out.exists()
source=(old/'attract.lua').read_text()
source=source.replace('frame>=12000','frame>=24000').replace('maximum_fields=12000','maximum_fields=24000')
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(old/'attract.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_current_attract_runtime','audit_bounded_current_attract_long_runtime')
runner=runner.replace("'-str','400'","'-str','600'")
(out/'run.ps1').write_text(runner)
print('Prepared24000field natural sparse attract, unchanged90sec/320MiB/10MiB caps')
