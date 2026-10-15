"""Keep native projectile block gate; explicit blade/bicycle entry and chip."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_projectile_blocks.py')
source=prior.read_text()
changes={
 "('17','FFFFB000') if move=='knife' else ('18','FFFFB400')":"('17','FFF8CC00') if move=='blade' else ('18','FFF9A400')",
 "int(event['frame'])-command==8":"int(event['frame'])-command==(8 if move=='blade' else 15)",
 "==6 and hit['pc']":"==3 and hit['pc']",
 'chipDamage=6':'chipDamage=3',
 'audit_bounded_current_projectile_blocks_checked':'audit_bounded_current_close_blocks_checked',
 "for move in ('knife','ring'):":"for move in ('blade','bicycle'):",
 'audit_bounded_current_projectile_block_{move}':'audit_bounded_current_close_block_{move}',
 'physical knife/ring block':'physical knife-uppercut/bicycle block',
 'six chip damage':'three chip damage',
 'checkerSHA256=sync.sha(Path(__file__)),':'checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),'}
for before,after in changes.items():
    assert before in source;source=source.replace(before,after)
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
