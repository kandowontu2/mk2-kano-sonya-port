"""Native knife, close low-health physical upper; no gameplay mutation."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_recovered_knife_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_knife_upper_finish_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local ku_down,ku_pulse,ku_last=nil,nil,nil\n'+source
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch=source[start:end]
old='     elseif height>8 then'
assert branch.count(old)==1
branch=branch.replace(old,"""     elseif other.hp<=35 and gap<=90 and height==0 then
      if not ku_last or frame-ku_last>1 then ku_down=nil;ku_pulse=nil end
      ku_last=frame
      if human.action==263 or human.action==1539 then
       press('Down');press('Block');ku_down=nil
      elseif ku_pulse and frame-ku_pulse<8 then
       press('Down');if frame-ku_pulse<3 then press('High Punch')end
      else
       ku_down=ku_down or frame;press('Down')
       if can_crouch and frame-ku_down>=4 and (not ku_pulse or frame-ku_pulse>=26)then
        ku_pulse=frame;decision('shao_low_health_upper_attempt');press('High Punch')
       end
      end
     elseif height>8 then""")
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_recovered_knife_runtime','audit_current_kano_p2_shao_knife_upper_finish_runtime')
(out/'run.ps1').write_text(runner)
print('Knife+physicalupperfinishHP<=35gap90;180sec/320MiB/10MiB/no media/guestwrites')
