"""Same native grab damage/recovery gate with each actual cross-victim ID."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_mirror_grabs.py')
source=prior.read_text()
before="all(r['id']==r['roster']==ident and r['actor']==r['owner'] for r in fields)"
after="all(r['id']==r['roster']==(ident if r['slot']==str(side) else ('18' if ident=='17' else '17')) and r['actor']==r['owner'] for r in fields)"
assert source.count(before)==1;source=source.replace(before,after)
for before,after in {
 'audit_bounded_current_mirror_grabs_checked':'audit_bounded_current_cross_grabs_checked',
 'audit_bounded_current_mirror_grab_{move}_p{side}_runtime':'audit_bounded_current_cross_grab_{move}_p{side}_runtime',
 'twoMirrorActivations':'twoCrossActivations',
 'trueMirrorFields':'trueCrossFields',
 'Four current physical mirror grab contexts':'Four current physical Kano/Sonya cross-character grab contexts',
 'checkerSHA256=sync.sha(Path(__file__)),':'checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),'
}.items():
    assert before in source;source=source.replace(before,after)
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
