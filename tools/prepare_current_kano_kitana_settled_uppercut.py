"""Physical native crouch preparation against natural Kitana, unchanged earlier route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
out=sync.ROOT/'audit_current_kano_kitana_settled_uppercut_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
tested=(sync.ROOT/'audit_current_sonya_subzero_range_uppercut_preparation/campaign.lua').read_text()
start=tested.index('   elseif leg_tactic and other.roster==8 then\n')
end=tested.index("   elseif (leg_tactic or strategy==",start)
branch=tested[start:end].replace('elseif leg_tactic and other.roster==8 then','if identity==17 and other.roster==4 then').replace('sz_','ku_').replace('SUBZERO_UPPERCUT_ATTEMPT','KANO_KITANA_UPPERCUT_ATTEMPT')
marker="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(marker)==1
source='local ku_last,ku_leg,ku_retry,ku_upper,ku_guard=nil,nil,-1000,-1000,-1000\n'+source.replace(marker,branch+marker.replace('   if ','   elseif ',1))
source+=r'''
taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'native Kano uppercut observation',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=0xff870dd0 or p:read_u16(0x01061b30)~=3 then return end
 local own=sample(side)
 if own and own.id==17 and own.roster==17 and cpu.A8.value==own.actor and cpu.A13.value==own.main then
  log('KANO_KITANA_NATIVE_UPPER',string.format('actor=%08X main=%08X owner=%08X id=%d',own.actor,own.main,own.owner,own.id))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_bounded_compact_kano_campaign_p1_runtime','audit_current_kano_kitana_settled_uppercut_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared native settled uppercut controller,18000fields/90sec/320MiB,no media')
