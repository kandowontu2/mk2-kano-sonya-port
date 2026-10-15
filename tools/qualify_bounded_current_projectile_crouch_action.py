"""Plain Down is native0302 crouch, not0701 crouching Block."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_projectile_ducks.py')
scope={'__file__':str(prior)}
exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope)
source=scope['source'];marker="r['action']=='1793'"
assert source.count(marker)==1;source=source.replace(marker,"r['action']=='770'")
source=source.replace('predecessorCheckerSHA256=sync.sha(prior),','predecessorCheckerSHA256=sync.sha(prior),failedCrouchBlockCheckerSHA256=sync.sha(failed),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=scope['prior'],failed=prior))
