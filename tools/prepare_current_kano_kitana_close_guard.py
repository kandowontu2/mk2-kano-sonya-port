"""Physical close crouch defense/punish, retain native knives at range."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_ground_spacing_preparation'
out=sync.ROOT/'audit_current_kano_kitana_close_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
needle='    if ks_start and frame-ks_start<12 then'
assert source.count(needle)==1
branch=r'''    if gap<105 and human.floor-human.y<=8 then
     ks_start=nil
     if not kc_start or frame-kc_start>=36 then kc_start=frame end
     local age=frame-kc_start
     press('Down')
     if age<10 or age>=24 then press('Block')end
     if age>=13 and age<24 and age%6<3 then press('High Punch')end
     if age==13 then log('KANO_KITANA_CLOSE_PUNISH',string.format('gap=%d action=%d cpu_action=%d',gap,human.action,other.action))end
    elseif ks_start and frame-ks_start<12 then'''
source='local kc_start=nil\n'+source.replace(needle,branch)
source+=r'''
taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'owned close counter uppercut',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=0xff870dd0 or p:read_u16(0x01061b30)~=3 then return end
 local own=sample(side)
 if own and own.id==17 and own.roster==17 and cpu.A8.value==own.actor and cpu.A13.value==own.main then
  log('KANO_CLOSE_NATIVE_UPPER',string.format('actor=%08X main=%08X owner=%08X id=%d',own.actor,own.main,own.owner,own.id))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kitana_ground_spacing_runtime','audit_current_kano_kitana_close_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18000field physical closeguard/punish,no media,90sec/320MiB')
