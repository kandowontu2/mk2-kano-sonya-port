"""Read-only native router choices, longer existing physical guard probe."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_native_cpu_guard_probe_preparation'
out=sync.ROOT/'audit_current_sonya_cpu_router_probe_preparation';assert not out.exists()
source=(old/'campaign.lua').read_text()
source=source.replace('frame>=12000','frame>=30000').replace('maximum_fields=12000','maximum_fields=30000')
marker="emu.register_frame(function()\n if frame>=30000";assert source.count(marker)==1
observer='''local router=0xff800000+0xf7840*8
local router_marks={[router+16]='entry',[router+13*16]='ring',[router+16*16]='square',[router+19*16]='bicycle'}
taps[#taps+1]=p:install_read_tap(router,router+21*16-1,'actual Sonya CPU variety router',function(at)
 local choice=router_marks[at];if not choice or not first_live then return end
 local actual=sample(opponent)
 if not actual or actual.id~=18 or actual.roster~=18 or actual.state~=0 or
  actual.owner~=actual.actor or cpu.A8.value~=actual.actor or cpu.A13.value~=actual.main then return end
 log('CPU_ROUTER',string.format('choice=%s at=%08X pc=%08X slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d stage=%d',
  choice,at,cpu.PC.value,opponent,actual.actor,actual.main,actual.owner,actual.id,actual.roster,actual.state,actual.hp,p:read_u16(0x01061b30)))
end)
'''
source=source.replace(marker,observer+marker)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_cpu_guard_probe_runtime','audit_current_sonya_cpu_router_probe_runtime')
runner=runner.replace("'-str','400'","'-str','700'")
(out/'run.ps1').write_text(runner)
print('Prepared30000field natural CPU decision trace; unchanged90sec/320MiB/10MiB limits')
