"""Passive actual CPU action taps on the existing physical cold campaign."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation'
out=sync.ROOT/'audit_current_native_cpu_move_observer_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
marker="emu.register_frame(function()\n if frame>=12000";assert source.count(marker)==1
observer='''local cpu_move_specs={
 {'knife',17,0xffffb000},{'ball',17,0xffffde00},{'blade',17,0xfff8cc00},{'choke',17,0xfff91400},
 {'ring',18,0xffffb400},{'square',18,0xffffca00},{'bicycle',18,0xfff9a400},{'leg',18,0xfff80800}}
for _,spec in ipairs(cpu_move_specs)do
 local move,id,address=spec[1],spec[2],spec[3]
 taps[#taps+1]=p:install_read_tap(address+16,address+31,'actual natural CPU '..move,function(at)
  if at~=address+16 or not first_live then return end
  local actual=sample(opponent)
  if not actual or actual.id~=id or actual.roster~=id or actual.state~=0 or
   actual.owner~=actual.actor or cpu.A8.value~=actual.actor or cpu.A13.value~=actual.main then return end
  log('CPU_MOVE',string.format('move=%s entry=%08X pc=%08X slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d stage=%d',
   move,address,cpu.PC.value,opponent,actual.actor,actual.main,actual.owner,actual.id,actual.roster,actual.state,actual.hp,p:read_u16(0x01061b30)))
 end)
end
'''
source=source.replace(marker,observer+marker)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_delayed_campaign_runtime','audit_current_native_cpu_move_observer_runtime')
runner=runner.replace("MK2KS_TEST_BOOT_FRAME='700'","MK2KS_TEST_BOOT_FRAME='600'")
(out/'run.ps1').write_text(runner)
print('Prepared cold physical mirror-policy run with passive8CPU action taps; existing limits unchanged')
