"""Crouch Block admits native collision but leg grab causes no damage."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_projectile_blocks.py')
source=prior.read_text()
for before,after in {
 "('17','FFFFB000') if move=='knife' else ('18','FFFFB400')":"('18','FFF80800')",
 "int(event['frame'])-command==8":"int(event['frame'])-command==5",
 "assert len(hits)==1":"assert not hits\n    hits=rows['HEALTH'];assert len(hits)==1",
 "int(hit['before'])-int(hit['after'])==6":"hit['before']==hit['after']=='161'",
 "r['action']=='1792'":"r['action']=='1793'",
 'chipDamage=6':'chipDamage=0',
 'audit_bounded_current_projectile_blocks_checked':'audit_bounded_current_leg_duck_blocks_checked',
 "for move in ('knife','ring'):":"for move in ('leg',):",
 'audit_bounded_current_projectile_block_{move}_p{side}_runtime':'audit_bounded_current_leg_duck_block_p{side}_runtime',
 'physical knife/ring block':'physical leg grab against crouching Block',
 'six chip damage':'zero damage despite native collision',
 'checkerSHA256=sync.sha(Path(__file__)),':'checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),',
 'contexts=4':'contexts=2'
}.items():
    assert before in source;source=source.replace(before,after)
marker="    assert [int(r['frame']) for r in defense]==list(range(command,command+220))"
source=source.replace(marker,marker+"""
    down=[r for r in rows['INPUT'] if r['slot']==str(3-side) and r['button']=='Down' and command<=int(r['frame'])<command+220]
    assert [int(r['frame']) for r in down]==list(range(command,command+220))
    assert all(r['hp']=='161' for r in rows['FIELD'])
""")
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
