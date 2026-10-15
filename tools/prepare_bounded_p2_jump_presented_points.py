"""Same finite physical jumps in the second native player slot."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_jump_presented_points_preparation'
out=sync.ROOT/'audit_bounded_p2_jump_presented_points_preparation';assert not out.exists();out.mkdir()
lua=(old/'prepared_observer.lua').read_text()
for marker in ("input(1,'Up')","input(1,'Right')","input(1,'Left')"):
    lua=lua.replace(marker,marker.replace('input(1,','input(side,'))
target=out/'prepared_observer.lua';target.write_text(lua)
assert ':write_' not in lua
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_SIDE='1'","$env:MK2KS_HUMAN_SPECIAL_SIDE='2'")
    runner=runner.replace(f'audit_bounded_{fighter}_jump_presented_points_runtime',f'audit_bounded_{fighter}_p2_jump_presented_points_runtime')
    (out/f'run_{fighter}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,physicalPlayerSide=2,rawMedia=False,observerSHA256=sync.sha(target))))
