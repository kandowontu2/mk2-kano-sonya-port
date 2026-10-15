"""Real secondary commands, genuine morphed victims, complete paired observer."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_morphed_victim_pair_observer_preparation'
out=sync.ROOT/'audit_morphed_victims_secondary_preparation';assert not out.exists()
source=(old/'finishers.lua').read_text()
marker='local sequence=assert(commands[command])';assert source.count(marker)==1
source=source.replace(marker,"commands.kano_laser={'Low Punch','Block','Block','High Kick'}\ncommands.sonya_orb={'Up','Up','Back','Down','High Kick'}\n"+marker)
marker='   local offset=10';assert source.count(marker)==1
source=source.replace(marker,marker+"\n   if command=='sonya_orb' and command_age>=offset and command_age<offset+#sequence*8 then press(winner_side,'Block')end")
out.mkdir();lua=out/'finishers.lua';lua.write_text(source)
for killer,command,gap in(('kano','kano_laser',150),('sonya','sonya_orb',256)):
    for victim in('kano','sonya'):
        for side in(1,2):
            runner=(old/f'run_{victim}_p{side}.ps1').read_text()
            runner=runner.replace(old.name+'/finishers.lua',out.name+'/finishers.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
            runner=runner.replace("MK2KS_STOCK_KILLER='kano'",f"MK2KS_STOCK_KILLER='{killer}'")
            runner=runner.replace("MK2KS_STOCK_COMMAND='kano_own'",f"MK2KS_STOCK_COMMAND='{command}'")
            runner=runner.replace("MK2KS_STOCK_GAP='64'",f"MK2KS_STOCK_GAP='{gap}'")
            runner=runner.replace(f'audit_morphed_victim_pair_{victim}_p{side}_runtime',f'audit_morphed_victim_secondary_{killer}_{victim}_p{side}_runtime')
            (out/f'run_{killer}_{victim}_p{side}.ps1').write_text(runner)
print('Prepared eight real secondary-finisher morphed-victim cases, existing resource caps retained')
