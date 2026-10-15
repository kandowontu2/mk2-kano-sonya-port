"""Physical forward/back positioning with settled range band, preserve overshoot."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_far_normal_contacts_preparation'
out=sync.ROOT/'audit_bounded_far_normals_range_band_preparation'
assert not out.exists()
out.mkdir()
source=(old/'normals.lua').read_text()
marker="if math.abs(own.x-victim.x)>80 then input(side,own.x<victim.x and'Right'or'Left');normal_settle=nil"
assert source.count(marker)==1
source=source.replace(marker,"if math.abs(own.x-victim.x)>112 then input(side,own.x<victim.x and'Right'or'Left');normal_settle=nil\n       elseif math.abs(own.x-victim.x)<80 then input(side,own.x<victim.x and'Left'or'Right');normal_settle=nil")
lua=out/'normals.lua'
lua.write_text(source)
for move in ('knife','ring'):
 for side in (1,2):
    runner=(old/f'run_{move}_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/normals.lua',out.name+'/normals.lua').replace(sync.sha(old/'normals.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_far_normal_contacts_{move}_p{side}_runtime',f'audit_bounded_far_normals_range_band_{move}_p{side}_runtime')
    (out/f'run_{move}_p{side}.ps1').write_text(runner)
