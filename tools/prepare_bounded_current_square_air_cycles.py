"""Original opponent physical jump policy, no forced airborne actor."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
out=sync.ROOT/'audit_bounded_current_square_air_cycles_preparation';assert not out.exists();out.mkdir()
for side in (1,2):
    runner=(old/f'run_square_p{side}.ps1').read_text()
    marker="$env:MK2KS_HUMAN_SPECIAL_MOVE='square'"
    assert runner.count(marker)==1
    runner=runner.replace(marker,marker+"\n$env:MK2KS_HUMAN_SPECIAL_AIR='1'")
    runner=runner.replace(f'audit_bounded_current_special_cycles_square_p{side}_runtime',f'audit_bounded_current_square_air_cycles_p{side}_runtime')
    (out/f'run_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,observerUnchanged=True,physicalOpponentUpThreeFields=True,guestWrites=False)))
