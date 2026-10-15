"""Physical victim walks into a launched standing jab; no guest-state edits."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_far_normals_range_band_preparation'
out=sync.ROOT/'audit_bounded_standing_punch_walkin_preparation'
assert not out.exists()
out.mkdir()
source=(old/'normals.lua').read_text()
marker="      pulse(side,buttons[normal_index],frame-normal_start,0,3)"
assert source.count(marker)==1
source=source.replace(marker,marker+"\n      if normal_index<=2 then pulse(3-side,victim.x<own.x and'Right'or'Left',frame-normal_start,0,8)end")
lua=out/'normals.lua'
lua.write_text(source)
for move in ('knife','ring'):
 for side in (1,2):
    runner=(old/f'run_{move}_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/normals.lua',out.name+'/normals.lua').replace(sync.sha(old/'normals.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_far_normals_range_band_{move}_p{side}_runtime',f'audit_bounded_standing_punch_walkin_{move}_p{side}_runtime')
    (out/f'run_{move}_p{side}.ps1').write_text(runner)
