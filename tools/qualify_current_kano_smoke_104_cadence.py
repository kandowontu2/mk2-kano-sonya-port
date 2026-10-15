"""Same earned Kano/native decision/control/return gate for104-field rhythm."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_smoke_transition.py').read_text()
source=source.replace('audit_current_kano_smoke_transition','audit_current_kano_smoke_104_cadence')
old="assert terminal['observerSha256']==sync.sha(lua)==sync.sha(sync.ROOT/'audit_current_sonya_smoke_transition_batched_preparation/stage.lua')"
assert source.count(old)==1
source=source.replace(old,"""assert terminal['observerSha256']==sync.sha(lua)
baseline=load(sync.ROOT/'audit_current_kano_smoke_transition_runtime/run.log')""")
old="rows=load(folder/'run.log')"
assert source.count(old)==1
source=source.replace(old,"""rows=load(folder/'run.log')
for tag in set(rows)|set(baseline):
    if tag!='RESULT':
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<20697]==[r for r in baseline.get(tag,[]) if int(r['frame'])<20697],tag""")
source=source.replace('sameDriverAsSonya=True','priorEarnedPrefixUnchangedThrough=20696')
exec(compile(source,__file__+'::same_native_gate_actualKano17','exec'))
