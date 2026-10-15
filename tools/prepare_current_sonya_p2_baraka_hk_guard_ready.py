"""Physical HK plans may leave native block/crouch instead of waiting for idle."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_hk_ring_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_hk_guard_ready_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==2 and (other.roster==8 or other.roster==2 or other.roster==0 or other.roster==9 or other.roster==3) then\n")
end=source.index('\n   elseif ',start+10)
branch=source[start:end]
old='(human.action==0 or human.action==771 or human.action==772)'
assert branch.count(old)==1
branch=branch.replace(old,'(human.action==0 or human.action==771 or human.action==772 or (other.roster==3 and (human.action==770 or human.action==1792 or human.action==1793)))')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_hk_ring_runtime','audit_current_sonya_p2_baraka_hk_guard_ready_runtime')
(out/'run.ps1').write_text(runner)
print('Baraka-only HK controller guard/crouch readiness;90sec/320MiB/10MiB/no media')
