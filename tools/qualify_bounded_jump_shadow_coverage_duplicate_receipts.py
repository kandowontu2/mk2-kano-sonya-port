"""Preserve predecessor failure; validate exact duplicated scalar receipts."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_jump_shadow_coverage.py')
source=prior.read_text()
marker="    for tag in ('FIELD','INPUT','READY','IDLE_TERMINAL','IDLE_SCANPOINT'):"
assert source.count(marker)==1
source=source.replace(marker,"""    assert len(rows['FIELD'])==2*len(old['FIELD'])
    for n in range(0,len(rows['FIELD']),4):
        assert rows['FIELD'][n:n+2]==rows['FIELD'][n+2:n+4]
    rows['FIELD']=[r for n,r in enumerate(rows['FIELD']) if n%4<2]
"""+marker)
source=source.replace("'audit_bounded_jump_shadow_coverage_checked'","'audit_bounded_jump_shadow_coverage_duplicate_receipts_checked'")
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),duplicateScalarReceiptsValidated=True,')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
