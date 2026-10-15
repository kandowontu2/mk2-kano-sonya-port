"""Baraka-only ring finisher threshold20; preserve physical earlier stages."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_hk_spacing90_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_ring_finish20_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==2 and (other.roster==8")
end=source.index("   elseif (leg_tactic or strategy=='lowkick'",start)
branch=source[start:end];old='elseif other.hp<=33 and ready and safe and cpu_height<=8 then'
assert branch.count(old)==1
branch=branch.replace(old,'elseif other.hp<=(other.roster==3 and 20 or 33) and ready and safe and cpu_height<=8 then')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_hk_spacing90_runtime','audit_current_sonya_p2_baraka_ring_finish20_runtime')
(out/'run.ps1').write_text(runner)
print('Barakaonlyringhandoff20;180sec/320MiB/10MiB/no media/guestwrites')
