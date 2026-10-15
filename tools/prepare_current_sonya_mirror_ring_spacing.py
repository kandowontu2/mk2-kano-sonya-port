"""Use the physically proven ring sequence in the genuine mirror only."""
import verify_native_source_sync as sync

sync.verify()
base=sync.ROOT/'audit_current_sonya_kunglao_guard_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_ring_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
tested=(sync.ROOT/'audit_current_sonya_subzero_ring_retreat_preparation/campaign.lua').read_text()
first=tested.index('   elseif leg_tactic and other.roster==8 and other.hp<=41 then\n')
last=tested.index('   elseif leg_tactic and other.roster==8 then\n',first)
branch=tested[first:last].replace('   elseif leg_tactic and other.roster==8 and other.hp<=41 then','   if leg_tactic and other.roster==18 then')
branch=branch.replace('chip_', 'zone_').replace('SUBZERO_RING_FINISH_ATTEMPT','MIRROR_RING_SPACING_ATTEMPT')
first=source.index('   if leg_tactic and other.roster==18 then\n')
last=source.index('   elseif leg_tactic and other.roster==0 then',first)
source='local zone_last,zone_ring,zone_escape,zone_forward=nil,nil,nil,nil\n'+source[:first]+branch+source[last:]
source=source.replace('frame>=18000','frame>=24000').replace('maximum_fields=18000','maximum_fields=24000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_kunglao_guard_runtime','audit_current_sonya_mirror_ring_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared physical mirror ring-spacing controller;24000fields,90sec/320MiB/10MiB,no media')
