"""Observe CPU0 actual paired HP changes with unchanged physical controls."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_campaign_render_skip_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_contact_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
end=source.index('for n,slot in ipairs(slots)do')
start=source.rindex('for observed_slot,observed_hp in ipairs(',0,end)
extra=source[start:end]
for before,after in (('~=2 then return end','~=3 then return end'),('c.id~=2 or c.roster~=2','c.id~=0 or c.roster~=0'),('SONYA_CAGE_DAMAGE','SONYA_KUNGLAO_DAMAGE'),('ids=2,18','ids=0,18')):
    assert extra.count(before)==1,before
    extra=extra.replace(before,after)
source=source[:end]+extra+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_campaign_render_skip_runtime','audit_current_sonya_p2_kunglao_contact_trace_runtime')
(out/'run.ps1').write_text(runner)
print('CPU0 passive actual damage;unchanged controls;60k ceiling/90sec/320MiB/10MiB/no media')
