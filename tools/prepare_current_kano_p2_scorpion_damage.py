"""Passive scalar damage attribution on unchanged original zoning replay."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_32000_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_damage_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if cpu.PC.value==0xff836700 and p:read_u16(0x01061b30)==2 then')
end=source.index("   log('HEALTH'",start)
extra=source[start:end].replace('==2 then','==6 then').replace('a.id==2','a.id==3').replace('KANO_P2_LIU_DAMAGE','KANO_P2_SCORPION_DAMAGE')
source=source[:end]+extra+source[end:]
assert source.count("log('KANO_P2_SCORPION_DAMAGE'")==1
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_32000_runtime','audit_current_kano_p2_scorpion_damage_runtime')
(out/'run.ps1').write_text(runner)
print('Passive Scorpion nativeHP/action/owner scalar tap only;32000fields/90sec/320MiB/10MiB/no media')
