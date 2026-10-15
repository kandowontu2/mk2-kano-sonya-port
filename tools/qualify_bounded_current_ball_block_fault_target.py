"""Target the actual cannonball entry when testing ownership faults."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_ball_blocks.py')
scope={'__file__':str(prior)}
exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope)
source=scope['source']
marker="bad=copy.deepcopy(rows);bad[tag][0][key]=value"
assert source.count(marker)==1
source=source.replace(marker,"bad=copy.deepcopy(rows);target=next(r for r in bad[tag] if tag!='EVENT' or r['entry']=='FFFFDE00');target[key]=value")
source=source.replace('predecessorCheckerSHA256=sync.sha(prior),','predecessorCheckerSHA256=sync.sha(prior),failedFaultTargetCheckerSHA256=sync.sha(failed),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=scope['prior'],failed=prior))
