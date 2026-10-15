"""Same original repeated native commands; three cycles per current form/slot."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_morph_hits_preparation'
out=sync.ROOT/'audit_bounded_current_repeat_morphs_preparation'
assert not out.exists()
out.mkdir()
for target in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_{target}_p{side}.ps1').read_text()
        assert runner.count("ADVERSITY_PHASE='formed'")==1
        runner=runner.replace("ADVERSITY_PHASE='formed'","ADVERSITY_PHASE='repeat_morph'")
        runner=runner.replace('audit_bounded_current_morph_hit_','audit_bounded_current_repeat_morph_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared4 unchanged repeat-morph policies; three real cycles each, no media')
