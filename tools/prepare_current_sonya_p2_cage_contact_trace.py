"""Add passive native Cage/Sonya contact trace; physical controls unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_cage_hk_retreat_preparation'
out=sync.ROOT/'audit_current_sonya_p2_cage_contact_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('for observed_slot,observed_hp in ipairs(')
end=source.index('for n,slot in ipairs(slots)do',start)
extra=source[start:end]
for before,after in (('~=1 then return end','~=2 then return end'),('c.id~=8 or c.roster~=8','c.id~=2 or c.roster~=2'),('SONYA_SUBZERO_DAMAGE','SONYA_CAGE_DAMAGE'),('ids=8,18','ids=2,18')):
    assert extra.count(before)==1
    extra=extra.replace(before,after)
source=source[:end]+extra+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_cage_hk_retreat_runtime','audit_current_sonya_p2_cage_contact_trace_runtime')
(out/'run.ps1').write_text(runner)
print('CPU2 paired passive HP trace; unchanged inputs;30k/90sec/320MiB/10MiB/no media')
