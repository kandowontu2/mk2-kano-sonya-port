"""Scorpion's successful physical guarded-ball/knife response reused versus CPU5."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_sparse_inputs_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_ball_knife_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="elseif fighter=='kano' and side==2 and other.roster==3 then"
assert source.count(old)==1
source=source.replace(old,"elseif fighter=='kano' and side==2 and (other.roster==3 or other.roster==5) then")
source=source.replace("log('SCORPION_LOW_KNIFE_PLAN',","log(other.roster==3 and 'SCORPION_LOW_KNIFE_PLAN' or 'MILEENA_LOW_KNIFE_PLAN',")
start=source.index('   if cpu.PC.value==0xff836700 and p:read_u16(0x01061b30)==9 then')
end=source.index("   log('HEALTH'",start)
extra=source[start:end].replace('==9 then','==10 then').replace('a.id==4','a.id==5').replace('KANO_P2_KITANA_DAMAGE','KANO_P2_MILEENA_DAMAGE')
source=source[:end]+extra+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_sparse_inputs_runtime','audit_current_kano_p2_mileena_ball_knife_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only physical guardedball/knife55;60000target/90sec/320MiB/10MiB/no media')
