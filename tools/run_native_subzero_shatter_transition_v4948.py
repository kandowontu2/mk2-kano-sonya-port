"""Fresh cases extending actual fracture through subsequent selection/live phase."""
from pathlib import Path
prior=Path(__file__).with_name('run_native_subzero_shatter_lifecycle_v4944.py')
text=prior.read_text()
for before,after in(
 ("LUA='mk2ks_native_subzero_shatter_lifecycle_v4943.lua'","LUA='mk2ks_native_subzero_shatter_transition_v4947.lua'"),
 ('audit_v4945_subzero_','audit_v4949_subzero_'),('audit_v4946_subzero_','audit_v4950_subzero_'),
 ("(LUA,'mk2ks_native_subzero_shatter_probe_v4939.lua'","(LUA,'mk2ks_native_subzero_shatter_lifecycle_v4943.lua','mk2ks_native_subzero_shatter_probe_v4939.lua'"),
 ('[*controllers,Path(__file__),Path(native.__file__)','[*controllers,prior,Path(__file__),Path(native.__file__)'),
):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::subsequent_native_phase','exec'),globals())
