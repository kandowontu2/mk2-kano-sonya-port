"""Unchanged complete paired observer; genuine Sonya primary commands."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_morphed_victim_pair_observer_preparation'
out=sync.ROOT/'audit_morphed_victims_sonya_primary_preparation';assert not out.exists()
out.mkdir()
for target in('kano','sonya'):
    for side in(1,2):
        runner=(old/f'run_{target}_p{side}.ps1').read_text()
        runner=runner.replace("MK2KS_STOCK_KILLER='kano'","MK2KS_STOCK_KILLER='sonya'")
        runner=runner.replace("MK2KS_STOCK_COMMAND='kano_own'","MK2KS_STOCK_COMMAND='sonya_own'")
        runner=runner.replace("MK2KS_STOCK_GAP='64'","MK2KS_STOCK_GAP='96'")
        runner=runner.replace(f'audit_morphed_victim_pair_{target}_p{side}_runtime',f'audit_morphed_victim_sonya_primary_{target}_p{side}_runtime')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared four original physical Sonya primary commands against actual morphed victims; same complete observer')
