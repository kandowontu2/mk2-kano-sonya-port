"""Missing HEALTH records are expected for the preserved no-contact case."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_square_cycles.py')
scope={'__file__':str(prior)}
exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope)
source=scope['source'];marker="r for r in rows['HEALTH']"
assert source.count(marker)==1;source=source.replace(marker,"r for r in rows.get('HEALTH',[])")
source=source.replace('predecessorCheckerSHA256=sync.sha(prior),','predecessorCheckerSHA256=sync.sha(prior),failedSquareCheckerSHA256=sync.sha(failed),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=scope['prior'],failed=prior))
