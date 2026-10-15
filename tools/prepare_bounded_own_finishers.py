"""Existing genuine-win driver extended to owned Kano/Sonya commands."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_stock_head_finisher_preparation'
out=sync.ROOT/'audit_bounded_own_finishers_preparation'
assert not out.exists()
out.mkdir()
source=(old/'prepared_observer.lua').read_text()
marker='cage=2,baraka=3,kitana=4,kung_lao=0,jax=11'
assert source.count(marker)==1
source=source.replace(marker,marker+',kano=17,sonya=18')
marker='local sequence=assert(commands[command])'
assert source.count(marker)==1
source=source.replace(marker,"commands.kano_own={'Back','Down','Forward','High Kick'}\ncommands.sonya_own={'Back','Forward','Down','Down','Low Punch'}\n"+marker)
lua=out/'finishers.lua'
lua.write_text(source)
for fighter,gap in [('kano',64),('sonya',96)]:
 for winner in (1,2):
    runner=(old/'run_kano.ps1').read_text()
    runner=runner.replace(old.name+'/prepared_observer.lua',out.name+'/finishers.lua').replace(sync.sha(old/'prepared_observer.lua'),sync.sha(lua))
    runner=runner.replace("$env:MK2KS_TEST_FIGHTER='kano'","$env:MK2KS_TEST_FIGHTER='kitana'")
    runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='1'",f"$env:MK2KS_CAMPAIGN_SIDE='{3-winner}'")
    runner=runner.replace("$env:MK2KS_STOCK_KILLER='baraka'",f"$env:MK2KS_STOCK_KILLER='{fighter}'")
    runner=runner.replace("$env:MK2KS_STOCK_COMMAND='bbbb_hp'",f"$env:MK2KS_STOCK_COMMAND='{fighter}_own'")
    runner=runner.replace("$env:MK2KS_STOCK_GAP='64'",f"$env:MK2KS_STOCK_GAP='{gap}'")
    runner=runner.replace('audit_bounded_kano_stock_head_finisher_runtime',f'audit_bounded_own_finisher_{fighter}_p{winner}_runtime')
    (out/f'run_{fighter}_p{winner}.ps1').write_text(runner)
