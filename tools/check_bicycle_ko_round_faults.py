"""Retain the whole actual KO/reset/state/input/body/source fault suite."""
import inspect,types
from pathlib import Path
import check_sonya_ko_round_faults as original
import qualify_bicycle_launch_ko_round_v3 as current
model=types.SimpleNamespace(**current.scope)
source=inspect.getsource(original.check)
for before,after in (
 ('audit_sonya_ko_round_faults_p','audit_bicycle_ko_round_faults_p'),
 ('audit_sonya_launch_ko_round_checked_p','audit_bicycle_launch_ko_round_checked_p'),
 ('Path(__file__)','Path(__file__)'),
 ('for p in(Path(model.__file__),Path(faults.__file__))',
  'for p in(Path(model.__file__),Path(current.__file__),Path(original.__file__),Path(faults.__file__))'),
):
 if before!=after:
  model.need(source.count(before)==1,'Exact same-run fault suite scope adaptation');source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,model=model,current=current,original=original)
exec(compile(source,__file__+'::whole_twenty_two_actual_Bicycle_KO_faults','exec'),scope)
check=scope['check']
