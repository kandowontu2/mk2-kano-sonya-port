"""True Kano/Sonya victim handoffs via physical cross-character grabs."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_mirror_grabs_preparation'
out=sync.ROOT/'audit_bounded_current_cross_grabs_preparation';assert not out.exists();out.mkdir()
for move,victim,newvictim in [('choke','kano','sonya'),('leg','sonya','kano')]:
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace(f"$env:MK2KS_HUMAN_SPECIAL_VICTIM='{victim}'",f"$env:MK2KS_HUMAN_SPECIAL_VICTIM='{newvictim}'")
        runner=runner.replace(f'audit_bounded_current_mirror_grab_{move}_p{side}_runtime',f'audit_bounded_current_cross_grab_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
