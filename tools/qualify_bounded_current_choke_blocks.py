"""Native standing-Block collision admits no choke damage; clean recovery."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_leg_duck_blocks.py')
scope={'__file__':str(prior)}
exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope)
source=scope['source']
for before,after in {
 "('18','FFF80800')":"('17','FFF91400')",
 "int(event['frame'])-command==5":"int(event['frame'])-command==8",
 "r['action']=='1793'":"r['action']=='1792'",
 'audit_bounded_current_leg_duck_blocks_checked':'audit_bounded_current_choke_blocks_checked',
 "for move in ('leg',):":"for move in ('choke',):",
 'audit_bounded_current_leg_duck_block_p{side}_runtime':'audit_bounded_current_choke_block_p{side}_runtime',
 'physical leg grab against crouching Block':'physical Kano choke against standing Block',
 'predecessorCheckerSHA256=sync.sha(prior),':'predecessorCheckerSHA256=sync.sha(prior),legDuckCheckerSHA256=sync.sha(legchecker),'
}.items():
    assert before in source;source=source.replace(before,after)
marker="    down=[r for r in rows['INPUT'] if r['slot']==str(3-side) and r['button']=='Down' and command<=int(r['frame'])<command+220]\n    assert [int(r['frame']) for r in down]==list(range(command,command+220))\n"
assert source.count(marker)==1;source=source.replace(marker,'')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=scope['prior'],legchecker=prior))
