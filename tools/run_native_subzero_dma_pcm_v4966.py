"""Actual stock/added native DMA + full mixed PCM references, same immutable build."""
from pathlib import Path
prior=Path(__file__).with_name('run_native_subzero_reference_pcm_v4962.py')
text=prior.read_text()
for before,after in(
 ('mk2ks_native_subzero_reference_pcm_v4961.lua','mk2ks_native_subzero_dma_pcm_v4965.lua'),
 ('audit_v4963_subzero_','audit_v4967_subzero_'),('audit_v4964_subzero_','audit_v4968_subzero_'),
 ("'[*controllers,prior,Path(__file__),Path(native.__file__),ROOT/\\'mame-mkp/src/frontend/mame/luaengine.cpp\\''",
  "'[*controllers,prior,Path(__file__).with_name(\\'run_native_subzero_reference_pcm_v4962.py\\'),ROOT/\\'mk2ks_native_subzero_reference_pcm_v4961.lua\\',ROOT/\\'mame-mkp/src/mame/midway/midtunit_v.cpp\\',Path(__file__),Path(native.__file__),ROOT/\\'mame-mkp/src/frontend/mame/luaengine.cpp\\''"),
):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::actual_native_DMA','exec'),globals())
