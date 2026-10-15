"""Fresh explicit-source correction of flattened4972; failed preboot leaves retained."""
from pathlib import Path
prior=Path(__file__).with_name('run_native_subzero_dma_pcm_detail_v4972.py')
text=prior.read_text()
before='[*controllers,prior,Path(__file__).with_name('
after="[*controllers,prior,Path(__file__).with_name('run_native_subzero_shatter_lifecycle_v4944.py'),Path(__file__).with_name("
assert text.count(before)==1
text=text.replace(before,after,1).replace('audit_v4973_subzero_','audit_v4976_subzero_',1).replace('audit_v4974_subzero_','audit_v4977_subzero_',1)
exec(compile(text,str(Path(__file__).resolve())+'::explicit_flattened_sources','exec'),globals())
