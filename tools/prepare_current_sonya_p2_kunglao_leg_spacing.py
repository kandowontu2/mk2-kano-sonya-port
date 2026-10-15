"""Physical delayed leg input before stock close-throw range."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_leg_attack_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_leg_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   elseif leg_tactic and other.roster==0 then\n')
end=source.index("   elseif fighter=='sonya' and side==2",start)
branch=source[start:end]
for old,new in [('local ready=height<=8','local ready=height==0 and p:read_u32(human.actor+0x60)==0'),('ready and safe and gap<85','ready and safe and gap<110'),('ready and safe and gap>75','ready and safe and gap>100')]:
    assert branch.count(old)==1
    branch=branch.replace(old,new)
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_leg_attack_guard_runtime','audit_current_sonya_p2_kunglao_leg_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('Physical leg gap110/approach100/exact native grounding;90sec/320MiB/10MiB/no media')
