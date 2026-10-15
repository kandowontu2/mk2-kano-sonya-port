"""Passive real HP damage context, unchanged physical Reptile controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_slim_observation_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_damage_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do\n')
end=source.index('\nend\n',start)+5
block=source[start:end]
assert "~=1 then return end" in block and 'c.id~=8 or c.roster~=8' in block
block=block.replace('~=1 then return end','~=5 then return end').replace('c.id~=8 or c.roster~=8','c.id~=9 or c.roster~=9').replace('ids=8,18','ids=9,18').replace('SONYA_SUBZERO_DAMAGE','SONYA_REPTILE_DAMAGE').replace('passive actual Sonya Subzero damage','passive actual Sonya Reptile damage')
source=source[:end]+block+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_slim_observation_runtime','audit_current_sonya_p2_reptile_damage_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Unchanged inputs plus actual Reptile HP damage context;90sec/320MiB/10MiB/no media')
