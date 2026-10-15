"""Approach through physical directions between normal attack trials."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_basic_controls_preparation'
out=sync.ROOT/'audit_bounded_current_normal_contacts_preparation'
assert not out.exists()
out.mkdir()
source=(old/'controls.lua').read_text()
marker="    pulse(side,forward,f,0,8);pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)"
assert source.count(marker)==1
source=source.replace(marker,"""    if ((f>=0 and f<32)or(f>=140 and f<172)or(f>=204 and f<236)or(f>=268 and f<300))and math.abs(own.x-victim.x)>48 then input(side,own.x<victim.x and'Right'or'Left')end
    pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)""")
lua=out/'contacts.lua'
lua.write_text(source)
for move in ('knife','ring'):
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/controls.lua',out.name+'/contacts.lua').replace(sync.sha(old/'controls.lua'),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_basic_controls_{move}_p{side}_runtime',f'audit_bounded_current_normal_contacts_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
