"""Physical standing guard then counter from observed native charge recovery."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_charge_observer_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_charge_guard_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local cg_contact,cg_main,cg_down,cg_pulse=nil,nil,nil,nil\n'+source
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
source=source[:start]+'''    if stage==16 then
     if human.action==263 or human.action==1539 then
      press('Block');cg_down=nil
     elseif cg_pulse and frame-cg_pulse<8 then
      press('Down');if frame-cg_pulse<3 then press('High Punch')end
     elseif cg_contact and cg_main==other.main and frame-cg_contact<=36 and gap<=100 and height==0 then
      cg_down=cg_down or frame;press('Down')
      if can_crouch and frame-cg_down>=4 and(not cg_pulse or frame-cg_pulse>=26)then
       cg_pulse=frame;decision('shao_charge_recovery_upper_attempt');press('High Punch')
      end
     else
      cg_down=nil;press('Block')
     end
'''+source[end:]
old="  log('SHAO_CHARGE_TRACE',string.format"
assert source.count(old)==1
source=source.replace(old,"  if entry==0xff9d24c0 then cg_contact=frame;cg_main=c.main end\n"+old)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_charge_observer_runtime','audit_current_kano_p2_shao_charge_guard_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Physicalguard/chargecue/upper;180sec/320MiB/10MiB/no media/guestwrites')
