"""Same physical controller; real cold-selected added/mirror/stock victims."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT / 'audit_bounded_air_throw_retirement_preparation'
out = sync.ROOT / 'audit_bounded_air_throw_victims_preparation'
assert not out.exists()
out.mkdir()
for victim in ('sonya', 'kano', 'kitana'):
    for side in (1, 2):
        runner = (old / f'run_kano_p{side}.ps1').read_text()
        assert runner.count("SPECIAL_VICTIM='jax'") == 1
        runner = runner.replace("SPECIAL_VICTIM='jax'", f"SPECIAL_VICTIM='{victim}'")
        runner = runner.replace(f'audit_bounded_air_throw_retirement_kano_p{side}_runtime',
                                f'audit_bounded_air_throw_victim_{victim}_p{side}_runtime')
        (out / f'run_{victim}_p{side}.ps1').write_text(runner)
print('Prepared6 same-controller victim cases; no new assets or media')
