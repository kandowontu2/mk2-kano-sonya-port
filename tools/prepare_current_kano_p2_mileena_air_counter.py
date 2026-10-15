"""Physical air approach and native air-state traces only against CPU5."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_recovery_trace_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_air_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   if fighter=='kano' and side==2 and other.roster==5 then")
end=source.index("   elseif fighter=='kano' and side==2 and (other.roster==18",start)
donor=(sync.ROOT/'audit_current_kano_p2_scorpion_close_air_preparation/campaign.lua').read_text()
ds=donor.index("   elseif fighter=='kano' and side==2 and other.roster==3 then")
de=donor.index("   elseif (leg_tactic",ds)
branch=donor[ds:de].replace('   elseif fighter=', '   if fighter=',1)
branch=branch.replace('other.roster==3','other.roster==5').replace('c.id~=3','c.id~=5')
branch=branch.replace('0x01061b30)~=6','0x01061b30)~=10')
branch=branch.replace('sc_', 'ma_').replace('Scorpion','Mileena').replace('SCORPION_AIR_WRITE','MILEENA_AIR_WRITE')
branch=branch.replace('(human.action==0 or human.action==771 or human.action==772)', '(human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==3)')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_recovery_trace_runtime','audit_current_kano_p2_mileena_air_counter_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only physical air approach;owned native jump/airkick taps;90sec/320MiB/10MiB/no media')
