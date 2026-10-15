"""Bounded read-only command-edge/action observer for failed uppercut attempts."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_historical_uppercut_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_uppercut_edges_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source=source.replace('frame>=18000','frame>=9000').replace('maximum_fields=18000','maximum_fields=9000')
source+='''
local sz_observed_start=nil
emu.register_frame_done(function()
 if not sz_leg or frame-sz_leg>14 then return end
 local own,other=sample(side),sample(opponent)
 if not own or not other or other.roster~=8 then return end
 log('SUBZERO_COMMAND_FIELD',string.format('start=%d age=%d actor=%08X main=%08X owner=%08X id=%d roster=%d action=%d flags=%04X body=%04X x=%d y=%d floor=%d cpu_action=%d cpu_x=%d in0=%04X in2=%04X health=%d,%d',
  sz_leg,frame-sz_leg,own.actor,own.main,own.owner,own.id,own.roster,own.action,own.flags,own.body,own.x,own.y,own.floor,other.action,other.x,p:read_u16(0x01600000),p:read_u16(0x01600020),own.hp,other.hp))
end)
taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'read-only native uppercut entry',function()
 if cpu.PC.value~=0xff870dd0 then return end
 local own=sample(side)
 if own and cpu.A8.value==own.actor then log('SUBZERO_UPPERCUT_ENTRY',string.format('actor=%08X id=%d pc=%08X',own.actor,own.id,cpu.PC.value))end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_historical_uppercut_runtime','audit_current_sonya_subzero_uppercut_edges_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared 9000-field failed uppercut edge trace; no memory writes or media')
