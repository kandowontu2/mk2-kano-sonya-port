"""Physical true-ID mirror grabs in both slots; no proxy/forced actors."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
out=sync.ROOT/'audit_bounded_current_mirror_grabs_preparation';assert not out.exists();out.mkdir()
for move,fighter in [('choke','kano'),('leg','sonya')]:
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'",f"$env:MK2KS_HUMAN_SPECIAL_VICTIM='{fighter}'")
        runner=runner.replace(f'audit_bounded_current_special_cycles_{move}_p{side}_runtime',f'audit_bounded_current_mirror_grab_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
