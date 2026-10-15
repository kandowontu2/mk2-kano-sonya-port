"""Standing counter retained; real D/B/HP knife at low observed CPU health."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_subzero_standing_preparation'
out=sync.ROOT/'audit_current_kano_p2_subzero_low_knife_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local kz_finish_start,kz_finish_direction=nil,nil\n'+source
old='then kp_start=nil;kp_retry=-1000 end';assert source.count(old)==1
source=source.replace(old,'then kp_start=nil;kp_retry=-1000;kz_finish_start=nil end')
old="    if other.flags&0x10~=0 then kp_start=nil;press('Down');press('Block')"
assert source.count(old)==1
source=source.replace(old,"""    if other.roster==8 and kz_finish_start and frame-kz_finish_start<64 then
     local age=frame-kz_finish_start
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(kz_finish_direction)end
     if age>=8 and age<12 then press('High Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif other.roster==8 and other.hp<=33 and ready and safe and cpu_height<=8 then
     kz_finish_start=frame;kz_finish_direction=forward=='Right'and'Left'or'Right';kp_start=nil
     log('KANO_P2_SUBZERO_KNIFE_PLAN',string.format('gap=%d health=%d,%d action=%d cpu_action=%d',gap,human.hp,other.hp,human.action,other.action))
    elseif other.flags&0x10~=0 then kp_start=nil;press('Down');press('Block')""")
source+='''
taps[#taps+1]=p:install_read_tap(0xffffb000,0xffffb00f,'physical SubZero low-health knife entry',function(at)
 if at==0xffffb000 and p:read_u16(0x01061b30)==1 then
  local h,v=sample(2),sample(1)
  if h and v and h.id==17 and v.id==8 then log('KANO_P2_SUBZERO_KNIFE_ENTRY',string.format('a8=%08X a13=%08X own=%08X main=%08X owner=%08X health=%d,%d',cpu.A8.value,cpu.A13.value,h.actor,h.main,h.owner,h.hp,v.hp))end
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_subzero_standing_runtime','audit_current_kano_p2_subzero_low_knife_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared only low-CPU-health physical knife finisher;20000fields/90sec/320MiB/no media')
