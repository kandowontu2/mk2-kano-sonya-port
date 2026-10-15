"""Two physical projectile cycles against each fighter's true mirror."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT / 'audit_bounded_current_special_cycles_preparation'
out = sync.ROOT / 'audit_bounded_current_mirror_projectiles_preparation'
assert not out.exists()
out.mkdir()
for move, fighter in [('knife', 'kano'), ('ring', 'sonya')]:
    for side in (1, 2):
        runner = (old / f'run_{move}_p{side}.ps1').read_text()
        runner = runner.replace("$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'", f"$env:MK2KS_HUMAN_SPECIAL_VICTIM='{fighter}'")
        runner = runner.replace(f'audit_bounded_current_special_cycles_{move}_p{side}_runtime', f'audit_bounded_current_mirror_projectile_{move}_p{side}_runtime')
        (out / f'run_{move}_p{side}.ps1').write_text(runner)
