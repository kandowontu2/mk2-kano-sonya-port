"""Genuine wins and physical owned secondary finisher input sequences."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_own_finishers_dispatch_preparation'
out=sync.ROOT/'audit_bounded_secondary_finishers_preparation'
assert not out.exists()
out.mkdir()
source=(old/'finishers.lua').read_text()
marker='local sequence=assert(commands[command])'
assert source.count(marker)==1
source=source.replace(marker,"commands.kano_laser={'Low Punch','Block','Block','High Kick'}\ncommands.sonya_orb={'Up','Up','Back','Down','High Kick'}\n"+marker)
marker='   local offset=10'
assert source.count(marker)==1
source=source.replace(marker,marker+"\n   if command=='sonya_orb' and command_age>=offset and command_age<offset+#sequence*8 then press(winner_side,'Block')end")
lua=out/'finishers.lua'
lua.write_text(source)
for fighter,command,gap in [('kano','kano_laser',150),('sonya','sonya_orb',256)]:
 for side in (1,2):
    runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/finishers.lua',out.name+'/finishers.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
    runner=runner.replace(f"$env:MK2KS_STOCK_COMMAND='{fighter}_own'",f"$env:MK2KS_STOCK_COMMAND='{command}'")
    priorGap=64 if fighter=='kano' else 96
    runner=runner.replace(f"$env:MK2KS_STOCK_GAP='{priorGap}'",f"$env:MK2KS_STOCK_GAP='{gap}'")
    runner=runner.replace(f'audit_bounded_own_finisher_dispatch_{fighter}_p{side}_runtime',f'audit_bounded_secondary_finisher_{fighter}_p{side}_runtime')
    (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
