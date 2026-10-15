"""Physical settled crouch normals, no artificial character state."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_basic_controls_preparation'
out=sync.ROOT/'audit_bounded_current_crouching_attacks_preparation'
assert not out.exists()
out.mkdir()
source=(old/'controls.lua').read_text()
marker="    if f==500 then"
assert source.count(marker)==1
source=source.replace(marker,"    pulse(side,'Down',f,440,24);pulse(side,'Low Punch',f,452,6);pulse(side,'Down',f,504,24);pulse(side,'Low Kick',f,516,6);pulse(side,'Down',f,568,24);pulse(side,'High Punch',f,580,6)\n    if f==660 then")
lua=out/'controls.lua'
lua.write_text(source)
for move in ('knife','ring'):
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/controls.lua',out.name+'/controls.lua').replace(sync.sha(old/'controls.lua'),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_basic_controls_{move}_p{side}_runtime',f'audit_bounded_current_crouching_attacks_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
