"""Same genuine Shang round/morph driver; original secondary commands."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_morphed_finishers_landing_preparation'
out = sync.ROOT/'audit_bounded_morphed_secondary_finishers_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
marker = 'local sequence=assert(commands[command])'
assert source.count(marker)==1
source=source.replace(marker,"commands.kano_laser={'Low Punch','Block','Block','High Kick'}\ncommands.sonya_orb={'Up','Up','Back','Down','High Kick'}\n"+marker)
marker='   local offset=10'
assert source.count(marker)==1
source=source.replace(marker,marker+"\n   if command=='sonya_orb' and command_age>=offset and command_age<offset+#sequence*8 then press(winner_side,'Block')end")
out.mkdir()
lua=out/'finishers.lua'
lua.write_text(source)
for fighter,command,gap in [('kano','kano_laser',150),('sonya','sonya_orb',256)]:
    for side in (1,2):
        runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/finishers.lua',out.name+'/finishers.lua')
        runner=runner.replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
        runner=runner.replace(f"MK2KS_STOCK_COMMAND='{fighter}_own'",f"MK2KS_STOCK_COMMAND='{command}'")
        runner=runner.replace(f"MK2KS_STOCK_GAP='{64 if fighter=='kano' else 96}'",f"MK2KS_STOCK_GAP='{gap}'")
        runner=runner.replace('audit_bounded_morphed_finisher_landing_', 'audit_bounded_morphed_secondary_finisher_')
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
checker=(sync.ROOT/'tools/qualify_bounded_morphed_finishers.py').read_text()
marker='source = inspect.getsource(prior.gate)'
assert checker.count(marker)==1
checker=checker.replace(marker,marker+"\nsource = source.replace(\"a['variant']=='1'\", \"a['variant']=='2'\")")
checker=checker.replace("{'kano':'FFFAAE00','sonya':'FFFAB200'}","{'kano':'FFD86600','sonya':'FFD7B000'}")
checker=checker.replace('audit_bounded_morphed_finishers_checked','audit_bounded_morphed_secondary_finishers_checked')
checker=checker.replace('audit_bounded_morphed_finisher_landing_', 'audit_bounded_morphed_secondary_finisher_')
checker=checker.replace(old.name+'/finishers.lua',out.name+'/finishers.lua')
checker=checker.replace('nativePrimaryFinisherFromActualForm','nativeSecondaryFinisherFromActualForm')
checker=checker.replace('primary finishers','secondary finishers')
checker=checker.replace('Not secondary/friendly finishers', 'Not friendly finishers')
(out/'qualify.py').write_text(checker)
print('Prepared four real transformed secondary-finisher cases; original command and earned-win gates retained')
