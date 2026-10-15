"""Wait for actual native continue state before physical credit/Start pulses."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_secondary_rejoin_preparation'
out=sync.ROOT/'audit_bounded_secondary_rejoin_state_preparation'
assert not out.exists()
out.mkdir()
source=(old/'rejoin.lua').read_text()
marker=" if age>=350 and age<354 then press(side,'Coin')end\n if age>=368 and age<372 then press(side,'Start')end\n local mode=p:read_u16(0x010601d0)"
assert source.count(marker)==1
source=source.replace(marker,""" local mode=p:read_u16(0x010601d0)
 if mode==3 and p:read_u16(slots[side].state)==2 and not rejoin_request then rejoin_request=frame;log('REJOIN_REQUEST','native_continue_state=2')end
 if rejoin_request then
  local request_age=frame-rejoin_request
  if request_age>=0 and request_age<4 then press(side,'Coin')end
  if request_age>=18 and request_age<22 then press(side,'Start')end
 end""")
lua=out/'rejoin.lua'
lua.write_text(source)
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text()
    runner=runner.replace(old.name+'/rejoin.lua',out.name+'/rejoin.lua').replace(sync.sha(old/'rejoin.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_secondary_rejoin_{fighter}_p1_runtime',f'audit_bounded_secondary_rejoin_state_{fighter}_p1_runtime')
    (out/f'run_{fighter}.ps1').write_text(runner)
