"""Original physical attack timing during native reverse transformation."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_morph_hits_preparation'
out=sync.ROOT/'audit_bounded_current_morph_reverse_attacks_preparation'
assert not out.exists()
out.mkdir()
for target in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_{target}_p{side}.ps1').read_text()
        runner=runner.replace("ADVERSITY_PHASE='formed'","ADVERSITY_PHASE='reverse'")
        runner=runner.replace('audit_bounded_current_morph_hit_','audit_bounded_current_morph_reverse_attack_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared4 original reverse-timed attacks; no media')
