"""Earlier physical HK edge following observed throw-before-kick windows."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kunglao_counter_trace_preparation'
out=sync.ROOT/'audit_current_kano_kunglao_early_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if identity==17 and other.roster==0 then')
end=source.index('   elseif identity==17 and other.roster==4 then',start)
branch=source[start:end]
before="if age>=6 and age<10 then press('High Kick')end"
assert branch.count(before)==1
branch=branch.replace(before,"if age>=2 and age<6 then press('High Kick')end")
source=source[:start]+branch+source[end:]
source=source.replace('frame>=19500','frame>=24000').replace('maximum_fields=19500','maximum_fields=24000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kunglao_counter_trace_runtime','audit_current_kano_kunglao_early_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000fields; only KungLao HK edge fourfields earlier,no media')
