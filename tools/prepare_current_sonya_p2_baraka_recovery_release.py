"""Sustained physical recovery release, no reasserted crouch guard fallback."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_ready_forwardjump_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_recovery_release_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==2 and other.roster==3 then\n")
end=source.index('   elseif leg_tactic',start)
branch=source[start:end]
old="else press('Down');press('Block')end"
assert branch.count(old)==1
branch=branch.replace(old,'else -- sustain released inputs until native recovery/standing readiness\n    end')
branch=branch.replace('(blocking or human.action==0 or human.action==771 or human.action==770 or human.action==772)', '(human.action==0 or human.action==771 or human.action==772)')
marker='    bj_air=height>8\n'
assert branch.count(marker)==1
branch=branch.replace(marker,marker+"    if frame%120==0 then log('BARAKA_RECOVERY_FIELD',string.format('actor=%08X main=%08X id=%d action=%d flags=%04X height=%d vy=%08X ready=%s gap=%d',human.actor,human.main,human.id,human.action,human.flags,height,p:read_u32(human.actor+0x60),tostring(ready),gap))end\n")
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_ready_forwardjump_runtime','audit_current_sonya_p2_baraka_recovery_release_runtime')
(out/'run.ps1').write_text(runner)
print('Recovery release controller trial:90sec/320MiB/10MiB/no media/no guest writes')
