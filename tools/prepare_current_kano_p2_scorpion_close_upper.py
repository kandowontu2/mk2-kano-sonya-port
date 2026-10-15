"""Physical nearer crouch-only upper attempts and passive exact native entry."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_readiness_trace_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_close_upper_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source=source.replace('(human.action==770 or human.action==771 or human.action==772)','(human.action==770)')
assert source.count('gap>100 and height<=8 and other.flags&0x10==0')==1
source=source.replace('gap>100 and height<=8 and other.flags&0x10==0','gap>70 and height<=8 and other.flags&0x10==0')
source=source.replace('if ready and gap<105 and frame-sc_down>=12','if ready and gap<75 and frame-sc_down>=12')
source=source.replace("     elseif not ready and frame-sc_upper>=4 then press('Block')end","     end")
marker='for n,slot in ipairs(slots)do'
assert source.count(marker)==1
tap="""taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'passive actual own Scorpion upper handler',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=0xff870dd0 or p:read_u16(0x01061b30)~=6 then return end
 local h,c=sample(2),sample(1)
 if not h or not c or h.id~=17 or h.roster~=17 or c.id~=3 or h.owner~=h.actor or cpu.A8.value~=h.actor or cpu.A13.value~=h.main then return end
 log('SCORPION_UPPER_ENTRY',string.format('actor=%08X main=%08X owner=%08X a8=%08X a13=%08X gap=%d height=%d action=%d native_counter=%d hardware=%04X health=%d,%d',h.actor,h.main,h.owner,cpu.A8.value,cpu.A13.value,math.abs(h.x-c.x),h.floor-h.y,h.action,p:read_u16(h.main+0x220),p:read_u16(0x01600000),h.hp,c.hp))
end)
"""
source=source.replace(marker,tap+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_readiness_trace_runtime','audit_current_kano_p2_scorpion_close_upper_runtime')
(out/'run.ps1').write_text(runner)
print('Physical truecrouch/gap<75/Down12;native upperentry;32000fields/90sec/320MiB/10MiB/no media')
