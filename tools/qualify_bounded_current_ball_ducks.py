"""Cannonball misses crouch; independently keep charge/control/identity gates."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_projectile_crouch_action.py')
scope={'__file__':str(prior)}
exec(compile(prior.read_text().split('exec(compile(source,__file__',1)[0],str(prior),'exec'),scope)
source=scope['source']
for before,after in {
 "('17','FFFFB000',8) if move=='knife' else ('18','FFFFB400',8)":"('17','FFFFDE00',86)",
 "for move in ('knife','ring'):":"for move in ('ball',):",
 'audit_bounded_current_projectile_ducks_checked':'audit_bounded_current_ball_ducks_checked',
 'audit_bounded_current_projectile_duck_{move}_p{side}_runtime':'audit_bounded_current_ball_duck_p{side}_runtime',
 'Four current-build physical crouch knife/ring misses':'Two current-build physical crouch cannonball misses',
 'contexts=4':'contexts=2'
}.items():
    assert before in source;source=source.replace(before,after)
marker="    assert int(event['frame'])-base==latency"
source=source.replace(marker,marker+"""
    charge=[r for r in rows['INPUT'] if r['slot']==str(side) and r['button']=='Low_Kick' and base<=int(r['frame'])<base+84]
    assert [int(r['frame']) for r in charge]==list(range(base,base+84))
""")
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=scope['scope']['prior'],failed=scope['prior']))
