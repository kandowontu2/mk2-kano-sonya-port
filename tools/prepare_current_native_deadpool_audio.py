"""Reuse inspected passive channel observer on earned acid controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_gate_hold_preparation'
out=sync.ROOT/'audit_current_native_deadpool_audio_preparation'
assert not out.exists()
pit=(sync.ROOT/'audit_current_native_pit_audio_preparation/stage.lua').read_text()
marker='local channel={}'
assert pit.count(marker)==1
observer=pit[pit.index(marker):].replace('native Pit sound words','native acid sound words')
source=(base/'stage.lua').read_text()+'\n'+observer
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
for fighter,side in [('kano',1),('sonya',2)]:
 text=runner.replace('audit_current_native_deadpool_gate_hold_kano_p1_runtime',f'audit_current_native_deadpool_audio_{fighter}_p{side}_runtime')
 text=text.replace("$env:MK2KS_STAGE_WINNER='kano'",f"$env:MK2KS_STAGE_WINNER='{fighter}'")
 text=text.replace("$env:MK2KS_STAGE_SIDE='1'",f"$env:MK2KS_STAGE_SIDE='{side}'")
 (out/f'run_{fighter}_p{side}.ps1').write_text(text)
print('Prepared two earned acid audio traces; no PCM or media')
