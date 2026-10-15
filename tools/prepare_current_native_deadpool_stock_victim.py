"""Genuine selection of stock Sub-Zero victim; no opponent memory forcing."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_gate_hold_preparation'
out=sync.ROOT/'audit_current_native_deadpool_stock_victim_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old='local victim_id=id==17 and 18 or 17'
assert source.count(old)==1
source=source.replace(old,'local victim_id=8 -- Stock Sub-Zero, selected through native cursor navigation.')
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
for fighter,side in [('kano',1),('sonya',2)]:
 text=runner.replace('audit_current_native_deadpool_gate_hold_kano_p1_runtime',f'audit_current_native_deadpool_stock_{fighter}_p{side}_runtime')
 text=text.replace("$env:MK2KS_STAGE_WINNER='kano'",f"$env:MK2KS_STAGE_WINNER='{fighter}'")
 text=text.replace("$env:MK2KS_STAGE_SIDE='1'",f"$env:MK2KS_STAGE_SIDE='{side}'")
 (out/f'run_{fighter}_p{side}.ps1').write_text(text)
print('Prepared natural stock Sub-Zero selection, compact acid traces only')
