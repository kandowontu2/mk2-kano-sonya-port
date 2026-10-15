"""Fix report-only predecessor binding shadowed by the original stage loop."""
from pathlib import Path
parent=Path(__file__).with_name('qualify_extended_sonya_campaign_final_snapshot.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=namespace['prior']))"
assert wrapper.count(marker)==1
context=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),context)
source=context['source']
assert 'predecessorSHA256=sync.sha(prior)' in source
source=source.replace('predecessorSHA256=sync.sha(prior)',"predecessorSHA256=sync.sha(Path(__file__).with_name('qualify_bounded_campaign_progress.py'))")
exec(compile(source,__file__,'exec'),dict(__file__=__file__))
