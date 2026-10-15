"""Reuse actually successful P1 Kitana physical controller in true P2 context."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_early_knife_campaign_40000_preparation'
donor=sync.ROOT/'audit_current_kano_standing_counter_long_preparation/campaign.lua'
out=sync.ROOT/'audit_current_kano_p2_kitana_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text();prior=donor.read_text()
start=prior.index('   if identity==17 and other.roster==4 then')
end=prior.index('   elseif (leg_tactic',start)
branch=prior[start:end].replace('   if identity==17 and other.roster==4 then',"   elseif fighter=='kano' and side==2 and other.roster==4 then",1)
marker='   elseif (leg_tactic'
assert source.count(marker)==1
source='local kh_last,kh_start,kh_retry=nil,nil,-1000\nlocal ks_last,ks_start,ks_direction=nil,nil,nil\n'+source.replace(marker,branch+marker,1)
start=source.index('   if cpu.PC.value==0xff836700 and p:read_u16(0x01061b30)==6 then')
end=source.index("   log('HEALTH'",start)
extra=source[start:end].replace('==6 then','==9 then').replace('a.id==3','a.id==4').replace('KANO_P2_SCORPION_DAMAGE','KANO_P2_KITANA_DAMAGE')
source=source[:end]+extra+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_early_knife_campaign_40000_runtime','audit_current_kano_p2_kitana_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Actual P1 Kitana HK6..10/knife-spacing controller reused P2 only;40000fields/90sec/320MiB/10MiB/no media')
