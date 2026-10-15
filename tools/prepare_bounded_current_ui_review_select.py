"""Fix screenshot parity only; preserve executed four-image predecessor."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_ui_review_preparation'
out=sync.ROOT/'audit_bounded_current_ui_review_select_preparation';assert not out.exists();out.mkdir()
original=old/'ui.lua';source=original.read_text()
marker='if frame%2==0 and(age>=54'
assert source.count(marker)==1
source=source.replace(marker,'if (age>=54')
lua=out/'ui.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
        runner=runner.replace(old.name,out.name).replace(sync.sha(original),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_ui_{fighter}_p{side}_runtime',f'audit_bounded_current_ui_select_{fighter}_p{side}_runtime')
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,onlySnapshotSchedulingChanged=True,maximumPNGsPerCase=8)))
