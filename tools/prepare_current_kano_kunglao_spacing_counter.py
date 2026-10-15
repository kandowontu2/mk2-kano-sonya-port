"""Start existing early physical kick outside observed close throw race."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kunglao_early_counter_preparation'
out=sync.ROOT/'audit_current_kano_kunglao_spacing_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if identity==17 and other.roster==0 then')
end=source.index('   elseif identity==17 and other.roster==4 then',start)
branch=source[start:end]
for before,after in [('ready and gap<105 and','ready and gap<120 and'),('ready and gap>=105 then','ready and gap>=120 then')]:
    assert branch.count(before)==1
    branch=branch.replace(before,after)
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kunglao_early_counter_runtime','audit_current_kano_kunglao_spacing_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000fields; only KungLao counter/approach threshold105to120,no media')
