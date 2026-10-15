"""Transfer corrected physical jump readiness to Kano's natural Kitana fight."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
out=sync.ROOT/'audit_current_kano_kitana_confirmed_jump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
tested=(sync.ROOT/'audit_current_mirror_confirmed_jump_preparation/campaign.lua').read_text()
start=tested.index('   if leg_tactic and other.roster==18 then\n')
end=tested.index('   elseif leg_tactic and other.roster==0 then',start)
branch=tested[start:end].replace('if leg_tactic and other.roster==18 then','if identity==17 and other.roster==4 then').replace('MIRROR_','KANO_KITANA_')
marker="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(marker)==1
source='local cj_last,cj_request,cj_seen,cj_accepted=nil,nil,false,-1000\n'+source.replace(marker,branch+marker.replace('   if ','   elseif ',1))
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_bounded_compact_kano_campaign_p1_runtime','audit_current_kano_kitana_confirmed_jump_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared actual Kano/Kitana physical readiness successor,no media,18000fields/90sec')
