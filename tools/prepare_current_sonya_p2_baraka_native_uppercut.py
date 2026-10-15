"""Reuse existing physical uppercut branch only at Baraka3; preserve opening."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_prethrow_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_native_uppercut_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif strategy=='uppercut' then\n")
end=source.index("   elseif strategy=='jumpkick' then\n",start)
branch=source[start:end].replace("elseif strategy=='uppercut' then", "elseif fighter=='sonya' and side==2 and other.roster==3 then")
marker='   elseif leg_tactic and (other.roster==0 or (side==2 and other.roster==1)) then\n'
assert source.count(marker)==1
source=source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_prethrow_trace_runtime','audit_current_sonya_p2_baraka_native_uppercut_runtime')
(out/'run.ps1').write_text(runner)
print('Existing close uppercut physical branch:90sec/320MiB/10MiB/no media/no guest writes')
