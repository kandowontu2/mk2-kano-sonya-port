"""Stage7-only close-leg/readiness controller; native CPU and moves unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_short_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kano_short_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==2 and other.roster==3 and stage==6 then")
end=source.index("   elseif fighter=='sonya' and side==2 and (other.roster==8",start+1)
branch=source[start:end].replace('other.roster==3 and stage==6','other.roster==17 and stage==7').replace('bl_', 'kl_').replace('SONYA_BARAKA_SHORT_LEG_PLAN','SONYA_KANO_SHORT_LEG_PLAN')
source='local kl_last,kl_pulse=nil,nil\n'+source[:end]+branch+source[end:]
source+='''
for observed_slot,observed_hp in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(observed_hp,observed_hp+15,'passive actual Sonya Kano damage',function(at,data,mask)
  if at~=observed_hp or mask~=0xffff or p:read_u16(0x01061b30)~=7 then return end
  local before,after=p:read_u16(at),data&0xffff
  if after>=before or before>161 then return end
  local h,c=sample(2),sample(1)
  if not h or not c or h.id~=18 or h.roster~=18 or c.id~=17 or c.roster~=17 or h.owner~=h.actor or c.owner~=c.actor then return end
  log('SONYA_KANO_DAMAGE',string.format('victim_slot=%d before=%d after=%d pc=%08X ids=17,18 human_action=%d cpu_action=%d gap=%d height=%d cpu_height=%d',observed_slot,before,after,cpu.PC.value,h.action,c.action,math.abs(h.x-c.x),h.floor-h.y,c.floor-c.y))
 end)
end
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_short_leg_runtime','audit_current_sonya_p2_kano_short_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Stage7 Kano only physicalshortlegretry48; unchangedearlyroute;180sec/320MiB/10MiB/no media')
