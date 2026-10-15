"""Original physical blocking controller, remove three screenshot sinks."""
import json,re
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_current_projectile_blocks_preparation';assert not out.exists();out.mkdir()
original=sync.ROOT/'mk2ks_human_special_negative_v9.lua'
lua=original.read_text()
lua,count=re.subn(r"screen:snapshot\('[^']+'\)","log('NO_SNAPSHOT','raw_media=none')",lua)
assert count==3 and ':write_' not in lua and 'hex=' not in lua
target=out/'blocks.lua';target.write_text(lua)
old=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
for move in ('knife','ring'):
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/cycles.lua',out.name+'/blocks.lua').replace(sync.sha(old/'cycles.lua'),sync.sha(target))
        marker=f"$env:MK2KS_HUMAN_SPECIAL_MOVE='{move}'"
        runner=runner.replace(marker,marker+"\n$env:MK2KS_HUMAN_SPECIAL_SCENARIO='block'")
        runner=runner.replace(f'audit_bounded_current_special_cycles_{move}_p{side}_runtime',f'audit_bounded_current_projectile_block_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,physicalControllerSHA256=sync.sha(original),observerSHA256=sync.sha(target),rawMedia=False)))
