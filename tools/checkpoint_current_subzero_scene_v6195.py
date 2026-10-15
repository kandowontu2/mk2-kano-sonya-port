"""Exact native final-shadow/disable field aggregation successor.

Keep6193 and its executed failure. All original scene controls stay intact:
actual last owned shadow at origin+55, native flag disabled at origin+56.
No guest or underlying qualification changed; compression never ran in6193.
"""
from pathlib import Path
checkpoint_source=Path(__file__).with_name('checkpoint_current_subzero_scene_v6193.py')
source=checkpoint_source.read_text()
source=source.replace('audit_v6194_current_subzero_native_scene_progress','audit_v6196_current_subzero_native_scene_progress')
before="physical['lastPreFreezeShadowDraw']==physical['nativeShadowDisableFrame']==physical['origin']+56"
assert source.count(before)==1,'Exact failed last-shadow aggregation assumption'
source=source.replace(before,"physical['lastPreFreezeShadowDraw']==physical['nativeShadowDisableFrame']-1==physical['origin']+55",1)
before="pins={str(p.resolve()):sha(p)for p in(PARENT,Path(__file__),Path(storage.__file__))}"
assert source.count(before)==1,'Executed aggregate and failure retained'
source=source.replace(before,"pins={str(p.resolve()):sha(p)for p in(PARENT,checkpoint_source,ROOT/'audit_v6197_current_subzero_checkpoint_phase_failure/report.json',Path(__file__),Path(storage.__file__))}",1)
before="failures=[]"
assert source.count(before)==1,'Truthful actual host aggregation failure ledger'
source=source.replace(before,"failures=[dict(report=str(ROOT/'audit_v6197_current_subzero_checkpoint_phase_failure/report.json'),reason='Aggregate demanded a shadow draw after native flag disable; actual last draw is previous field',nativeBoots=0,nativeGameFailure=False)]",1)
exec(compile(source,__file__+'::exact_native_shadow_disable_checkpoint','exec'),globals())
