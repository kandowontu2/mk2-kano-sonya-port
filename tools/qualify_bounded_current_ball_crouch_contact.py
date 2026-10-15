"""Crouch does not avoid actual cannonball; verify contact rather than assume miss."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_projectile_blocks.py')
source=prior.read_text()
for before,after in {
 "('17','FFFFB000') if move=='knife' else ('18','FFFFB400')":"('17','FFFFDE00')",
 "int(event['frame'])-command==8":"int(event['frame'])-command==86",
 "==6 and hit['pc']":"==24 and hit['pc']",
 "r['button']=='Block'":"r['button']=='Down'",
 "r['action']=='1792'":"r['action']=='770'",
 'chipDamage=6':'contactDamage=24',
 'audit_bounded_current_projectile_blocks_checked':'audit_bounded_current_ball_crouch_contact_checked',
 "for move in ('knife','ring'):":"for move in ('ball',):",
 'audit_bounded_current_projectile_block_{move}_p{side}_runtime':'audit_bounded_current_ball_duck_p{side}_runtime',
 "bad=copy.deepcopy(rows);bad[tag][0][key]=value":"bad=copy.deepcopy(rows);target=next(r for r in bad[tag] if tag!='EVENT' or r['entry']=='FFFFDE00');target[key]=value",
 'physical knife/ring block':'physical cannonball versus crouching opponent',
 'Native block action, six chip damage':'Native crouch action, twenty-four full collision damage',
 'contexts=4':'contexts=2',
 'checkerSHA256=sync.sha(Path(__file__)),':'checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),'
}.items():
    assert before in source;source=source.replace(before,after)
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
