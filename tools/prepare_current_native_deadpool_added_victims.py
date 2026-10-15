"""Physical stock performer selection against both native added victims."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_gate_hold_preparation'
out=sync.ROOT/'audit_current_native_deadpool_added_victims_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old="local id=assert(({kano=17,sonya=18})[winner]);local victim_id=id==17 and 18 or 17"
assert source.count(old)==1
source=source.replace(old,"local id=assert(({subzero=8})[winner]);local victim_id=tonumber(os.getenv('MK2KS_ACID_VICTIM'));assert(victim_id==17 or victim_id==18)")
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
for victim,side in [(17,1),(18,2)]:
 text=runner.replace('audit_current_native_deadpool_gate_hold_kano_p1_runtime',f'audit_current_native_deadpool_victim_{victim}_runtime')
 text=text.replace("$env:MK2KS_STAGE_WINNER='kano'",f"$env:MK2KS_STAGE_WINNER='subzero'\n$env:MK2KS_ACID_VICTIM='{victim}'")
 text=text.replace("$env:MK2KS_STAGE_SIDE='1'",f"$env:MK2KS_STAGE_SIDE='{side}'")
 (out/f'run_victim_{victim}.ps1').write_text(text)
print('Prepared naturally selected stock performer vs Kano/Sonya victims; no media')
