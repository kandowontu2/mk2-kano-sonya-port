"""Separate kick chip from cannonball chip and verify native blocked bounce."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_projectile_blocks.py')
source=prior.read_text()
for before,after in {
 "('17','FFFFB000') if move=='knife' else ('18','FFFFB400')":"('17','FFFFDE00')",
 "int(event['frame'])-command==8":"int(event['frame'])-command==86",
 "assert len(hits)==1":"assert len(hits)==2\n    assert [int(r['before'])-int(r['after']) for r in hits]==[6,5]\n    assert int(hits[0]['frame'])<int(event['frame'])<int(hits[1]['frame'])\n    assert all(r['slot']==str(3-side) and r['pc']=='FF836700' for r in hits)",
 "hit=hits[0];at=int(hit['frame'])":"hit=hits[1];at=int(hit['frame'])",
 "==6 and hit['pc']":"==5 and hit['pc']",
 'chipDamage=6':'chipDamage=5',
 'audit_bounded_current_projectile_blocks_checked':'audit_bounded_current_ball_blocks_checked',
 "for move in ('knife','ring'):":"for move in ('ball',):",
 'audit_bounded_current_projectile_block_{move}_p{side}_runtime':'audit_bounded_current_ball_block_p{side}_runtime',
 'physical knife/ring block':'physical cannonball block',
 'six chip damage':'kick six plus cannonball five chip damage',
 'checkerSHA256=sync.sha(Path(__file__)),':'checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),'
}.items():
    assert before in source;source=source.replace(before,after)
marker="    assert int(rows['RECOVERED'][0]['frame'])>=command+221"
source=source.replace(marker,marker+"""
    charge=[r for r in rows['INPUT'] if r['slot']==str(side) and r['button']=='Low_Kick' and command<=int(r['frame'])<command+84]
    assert [int(r['frame']) for r in charge]==list(range(command,command+84))
    assert any(r['action']=='1538' and r['y']!=r['floor'] and at<=int(r['frame'])<at+20 for r in own)
""")
source=source.replace('contexts=4','contexts=2')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
