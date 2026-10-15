"""Physical ranged retreat with genuine standing ring readiness."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_standing_ready_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_standing_ring_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
tested=(sync.ROOT/'audit_current_sonya_mirror_ring_guard_preparation/campaign.lua').read_text()
first=tested.index('   if leg_tactic and other.roster==18 then')
last=tested.index('   elseif leg_tactic and other.roster==0 then',first)
branch=tested[first:last]
branch=branch.replace('frame-zone_ring<64','frame-zone_ring<48')
branch=branch.replace("press('Down');press('Block')","press('Block')")
old='(human.action==771 or human.action==770 or human.action==1793 or human.action==1792)'
assert branch.count(old)==1
branch=branch.replace(old,'(human.action==0 or human.action==771 or human.action==772)')
branch=branch.replace("    else\n     press('Block')", "    else\n     -- Release recovery inputs until a genuine standing command can start.")
first=source.index('   if leg_tactic and other.roster==18 then')
last=source.index('   elseif leg_tactic and other.roster==0 then',first)
source='local zone_last,zone_ring,zone_escape,zone_forward=nil,nil,nil,nil\nlocal zone_guard=-1000\n'+source[:first]+branch+source[last:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_standing_ready_runtime','audit_current_sonya_mirror_standing_ring_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared21000fields; standing ring readiness/retreat; no media')
