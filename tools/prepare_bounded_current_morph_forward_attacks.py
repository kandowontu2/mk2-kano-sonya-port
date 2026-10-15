"""Original physical attack timing during native forward transformation."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_morph_reverse_attacks_preparation'
out=sync.ROOT/'audit_bounded_current_morph_forward_attacks_preparation'
assert not out.exists()
out.mkdir()
for target in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_{target}_p{side}.ps1').read_text()
        assert runner.count("ADVERSITY_PHASE='reverse'")==1
        runner=runner.replace("ADVERSITY_PHASE='reverse'","ADVERSITY_PHASE='forward'")
        runner=runner.replace('audit_bounded_current_morph_reverse_attack_','audit_bounded_current_morph_forward_attack_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared4 physical forward-transition attacks; no media')
