"""Physical ready-state retreat before Reptile throw range, no game changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_damage_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_leg_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   elseif leg_tactic and (other.roster==0 or (side==2 and (other.roster==1 or other.roster==9))) then\n')
end=source.index("   elseif fighter=='sonya' and side==2",start)
branch=source[start:end]
old="    elseif height>8 then\n"
assert branch.count(old)==1
branch=branch.replace(old,"    elseif other.roster==9 and ready and gap<100 then\n     kg_leg=nil;press(human.x<other.x and 'Left' or 'Right')\n"+old)
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_damage_trace_runtime','audit_current_sonya_p2_reptile_leg_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('Physical Reptile ready retreat100, delayed leg outerrange;90sec/320MiB/10MiB/no media')
