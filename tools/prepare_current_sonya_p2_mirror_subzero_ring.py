"""Keep earned mirror route; reuse physical ring spacing only for SubZero8."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_mirror_subzero_ring_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
ring=(sync.ROOT/'audit_current_sonya_reptile_ring_spacing_preparation/campaign.lua').read_text()
start=ring.index("   elseif strategy=='uppercut' then\n");end=ring.index("   elseif strategy=='jumpkick' then\n",start)
branch=ring[start:end].replace("   elseif strategy=='uppercut' then","   elseif leg_tactic and other.roster==8 then",1)
needle="   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(needle)==1
source=source.replace(needle,branch+needle)
source=source.replace('local guard_until=-1000','local guard_until=-1000\nlocal rs_last,rs_ring,rs_dir,rs_jumpdir=nil,nil,nil,nil\nlocal rs_jump=-1000',1)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_mirror_guard_runtime','audit_current_sonya_p2_mirror_subzero_ring_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared30k unchanged mirror phase, physical ring/retreat against SubZero8 only/no media')
