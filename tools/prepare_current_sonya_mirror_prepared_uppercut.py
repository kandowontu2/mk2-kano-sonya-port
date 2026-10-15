"""Transfer verified physical crouch timing only to real Sonya mirror."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_kunglao_guard_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_prepared_uppercut_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
tested=(sync.ROOT/'audit_current_sonya_subzero_range_uppercut_preparation/campaign.lua').read_text()
first=tested.index('   elseif leg_tactic and other.roster==8 then\n')
last=tested.index('   elseif (leg_tactic or strategy==',first)
branch=tested[first:last].replace('   elseif leg_tactic and other.roster==8 then','   if leg_tactic and other.roster==18 then').replace('sz_','mu_').replace('SUBZERO_UPPERCUT_ATTEMPT','MIRROR_PREPARED_UPPERCUT_ATTEMPT')
first=source.index('   if leg_tactic and other.roster==18 then\n')
last=source.index('   elseif leg_tactic and other.roster==0 then',first)
source='local mu_last,mu_leg,mu_retry,mu_upper,mu_guard=nil,nil,-1000,-1000,-1000\n'+source[:first]+branch+source[last:]
marker='for n,slot in ipairs(slots)do\n';assert source.count(marker)==1
observer=r'''
taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'native mirror uppercut activation',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=0xff870dd0 or p:read_u16(0x01061b30)~=5 then return end
 local actor,main=p:read_u32(slots[side].actor),p:read_u32(slots[side].main)
 if cpu.A8.value~=actor or cpu.A13.value~=main then return end
 log('MIRROR_NATIVE_UPPERCUT',string.format('actor=%08X main=%08X id=%d roster=%d owner=%08X',actor,main,p:read_u16(actor+0x1f0),p:read_u16(slots[side].roster),p:read_u32(main+0xc0)))
end)
'''
source=source.replace(marker,observer+'\n'+marker)
source=source.replace('frame>=18000','frame>=24000').replace('maximum_fields=18000','maximum_fields=24000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_kunglao_guard_runtime','audit_current_sonya_mirror_prepared_uppercut_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared native mirror crouch/uppercut timing;24000fields/90sec/320MiB/no media')
