"""Guard through observed263/1539, then ordinary recovered state; inputs only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_upper_contact_bounded180_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_upper_full_recovery_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local su_lock,su_recovered,su_last=false,nil,nil\n'+source
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch=source[start:end]
old='     if gap>80 then\n';assert branch.count(old)==1
new="""     if not su_last or frame-su_last>1 then
      su_lock=false;su_recovered=nil;su_down=nil;su_pulse=nil;su_retry=-1000
     end
     su_last=frame
     if human.action==263 then su_lock=true end
     local guarded=false
     if su_lock then
      local stance=human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793
      local recovered=stance and height==0 and human.flags&0x1c==0
      if recovered then su_recovered=su_recovered or frame else su_recovered=nil end
      if su_recovered and frame-su_recovered>=12 then
       su_lock=false;su_recovered=nil;su_down=frame
       log('SHAO_UPPER_RECOVERED_RELEASE',string.format('actor=%08X main=%08X id=%d action=%d flags=%04X',human.actor,human.main,human.id,human.action,human.flags))
      else
       press('Down');press('Block');su_down=nil;guarded=true
      end
     end
     if guarded then
     elseif su_pulse and frame-su_pulse<8 then
      press('Down');if frame-su_pulse<3 then press('High Punch')end
     elseif gap>80 then
"""
branch=branch.replace(old,new)
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_upper_contact_bounded180_runtime','audit_current_kano_p2_shao_upper_full_recovery_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Physicalguardthroughnativeupper/recovery+12recoveredfields;180sec/320MiB/10MiB/no media/no guestwrites')
