"""Physical Block only after observed native upper acceptance, never force state."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_upper_contact_bounded180_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_upper_accepted_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local su_accepted=nil\n'+source
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch=source[start:end]
old='     if gap>80 then\n';assert branch.count(old)==1
new="""     if human.action==263 and (not su_accepted or frame-su_accepted>48) then
      su_accepted=frame
      log('SHAO_UPPER_ACCEPTED',string.format('actor=%08X main=%08X id=%d action=%d pulse=%d',human.actor,human.main,human.id,human.action,su_pulse or -1))
     end
     if su_accepted and frame-su_accepted<24 then
      press('Down');press('Block');su_down=nil
     elseif su_pulse and frame-su_pulse<8 then
      press('Down');if frame-su_pulse<3 then press('High Punch')end
     elseif gap>80 then
"""
branch=branch.replace(old,new)
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_upper_contact_bounded180_runtime','audit_current_kano_p2_shao_upper_accepted_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Observedupperacceptance thenphysicalguard24;180sec/320MiB/10MiB/no media/no guestwrites')
