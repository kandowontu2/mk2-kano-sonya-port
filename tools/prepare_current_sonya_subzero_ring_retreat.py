"""Release completed ring sequence sooner as CPU closes; physical controls only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_ring_finish_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_ring_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('if chip_ring and frame-chip_ring<64 then')==1
source=source.replace('if chip_ring and frame-chip_ring<64 then','if chip_ring and frame-chip_ring<64 and (frame-chip_ring<12 or gap>=150)then')
assert source.count('elseif gap<120 then')==1
source=source.replace('elseif gap<120 then','elseif gap<150 then')
source=source.replace('frame>=18000','frame>=9000').replace('maximum_fields=18000','maximum_fields=9000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_ring_finish_runtime','audit_current_sonya_subzero_ring_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared physical ring retreat at gap150 after command edges;9000fields/no media')
