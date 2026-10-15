"""Physical defence against observed CPU ring launch; earlier route unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_ring_spacing_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_ring_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local zone_guard=-1000\n'+source
first=source.index('   if leg_tactic and other.roster==18 then\n')
last=source.index('   elseif leg_tactic and other.roster==0 then',first)
branch=source[first:last]
needle='    chip_last=frame\n'
assert 'zone_last=frame' in branch
branch=branch.replace('    zone_last=frame\n',"    zone_last=frame\n    if other.action==4 or other.action==1540 then zone_guard=frame+40 end\n")
needle='    elseif height>8 then\n'
assert branch.count(needle)==1
branch=branch.replace(needle,"    elseif frame<zone_guard and height<=8 then\n     zone_ring=nil;press('Down');press('Block')\n"+needle)
# Existing 64-field post-shot cycle may hold controls while a CPU ring starts.
# Keep its initial command intact, then permit the defensive branch after12.
branch=branch.replace('(frame-zone_ring<12 or gap>=150)','(frame-zone_ring<12 or (gap>=150 and frame>=zone_guard))')
source=source[:first]+branch+source[last:]
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_ring_spacing_runtime','audit_current_sonya_mirror_ring_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared mirror CPU-ring guard,24000fields/90sec/320MiB/no media')
