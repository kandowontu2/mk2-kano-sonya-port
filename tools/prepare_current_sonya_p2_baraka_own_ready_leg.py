"""Physical leg chord gated by actual Sonya readiness, Baraka context only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_hk_ring_preparation'
prior=sync.ROOT/'audit_current_sonya_p2_reptile_own_ready_leg_preparation/campaign.lua'
out=sync.ROOT/'audit_current_sonya_p2_baraka_own_ready_leg_preparation'
assert not out.exists()
old=prior.read_text();start=old.index("   elseif fighter=='sonya' and side==2 and other.roster==9 then\n");end=old.index('   elseif leg_tactic and ',start)
branch=old[start:end].replace('other.roster==9 then','other.roster==3 then').replace('REPTILE_LEG_PLAN','BARAKA_LEG_PLAN')
source=(base/'campaign.lua').read_text()
marker='   elseif leg_tactic and (other.roster==0 or (side==2 and other.roster==1)) then\n'
assert source.count(marker)==1
source='local rl_last,rl_start,rl_retry=nil,nil,-1000\n'+source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_hk_ring_runtime','audit_current_sonya_p2_baraka_own_ready_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Baraka-only own-ready physical leg inputs;90sec/320MiB/10MiB/no media')
