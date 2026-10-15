"""Controller-only forward jump variant, after rejected backward spacing trial."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_ready_backjump_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_ready_forwardjump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==2 and other.roster==3 then\n")
end=source.index('   elseif leg_tactic',start)
branch=source[start:end]
assert branch.count('bj_direction=back')==1
branch=branch.replace('bj_direction=back','bj_direction=forward').replace("press('Up');press(back)","press('Up');press(forward)")
branch=branch.replace("if gap<190 and frame%6<3 then press('High Kick')end", "if gap<115 and height<90 and bj_start and frame-bj_start>=9 and frame%6<3 then press('High Kick')end")
branch=branch.replace('ready and gap<190','ready and gap<210').replace('ready and gap>=190','ready and gap>=210')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_ready_backjump_runtime','audit_current_sonya_p2_baraka_ready_forwardjump_runtime')
(out/'run.ps1').write_text(runner)
print('Ready forward jump:90sec/320MiB/10MiB/no media, no guest writes')
