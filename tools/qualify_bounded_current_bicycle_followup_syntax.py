"""Syntax-only successor; preserve failed checker bytes and all gates."""
from pathlib import Path
import verify_native_source_sync as sync
failed=Path(__file__).with_name('qualify_bounded_current_bicycle_followup_damage.py')
source=failed.read_text()
before="exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope))"
after="exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope)"
assert source.count(before)==1
source=source.replace(before,after)
exec(compile(source,str(failed),'exec'),dict(__file__=__file__))
