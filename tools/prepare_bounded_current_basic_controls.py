"""Normal physical controls after two projectile cycles, both added slots."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
out=sync.ROOT/'audit_bounded_current_basic_controls_preparation'
assert not out.exists()
out.mkdir()
source=(old/'cycles.lua').read_text()
marker="    pulse(side,forward,f,0,8);pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)"
assert source.count(marker)==1
source=source.replace(marker,marker+"\n    pulse(side,'Low Punch',f,176,3);pulse(side,'High Kick',f,240,3);pulse(side,'Low Kick',f,304,3);pulse(side,'Block',f,368,16);pulse(side,'Down',f,416,24);pulse(side,'Block',f,424,12)")
source=source.replace('if f==160 then','if f==500 then')
lua=out/'controls.lua'
lua.write_text(source)
for move in ('knife','ring'):
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/cycles.lua',out.name+'/controls.lua').replace(sync.sha(old/'cycles.lua'),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_special_cycles_{move}_p{side}_runtime',f'audit_bounded_current_basic_controls_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
