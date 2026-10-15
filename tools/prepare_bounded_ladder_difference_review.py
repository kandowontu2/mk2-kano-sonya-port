"""Four targeted images per run at actual differing scanout ages, no recording."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_ladder_scanout_preparation'
out=sync.ROOT/'audit_bounded_ladder_difference_review_preparation';assert not out.exists();out.mkdir()
source=(old/'scanout.lua').read_text()
marker="   log('SCANOUT',string.format('age=%d left=%016X right=%016X stock=%d',frame-exit_at,left,right,stock_control and 1 or 0))"
assert source.count(marker)==1
source=source.replace(marker,marker+"\n   local age=frame-exit_at\n   if age==87 or age==100 or age==200 or age==360 then screen:snapshot(string.format('difference_%03d.png',age))end")
lua=out/'review.lua';lua.write_text(source)
for suffix in ('added','stock'):
 runner=(old/f'run_sonya_p2_{suffix}.ps1').read_text()
 runner=runner.replace(old.name+'/scanout.lua',out.name+'/review.lua').replace(sync.sha(old/'scanout.lua'),sync.sha(lua))
 runner=runner.replace(f'audit_bounded_ladder_scanout_sonya_p2_{suffix}_runtime',f'audit_bounded_ladder_difference_sonya_p2_{suffix}_runtime')
 runner=runner.replace("rawMedia='none'","rawMedia='four targeted PNGs; no video/audio'")
 (out/f'run_{suffix}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,maximumPNGsPerRun=4,physicalInputsUnchanged=True)))
