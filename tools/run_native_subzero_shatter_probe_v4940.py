"""Actual physical shatter approach; immutable candidate, finite diagnostic only."""
from pathlib import Path
prior=Path(__file__).with_name('run_native_subzero_body_probe_v4934.py')
text=prior.read_text()
for before,after in(
 ('mk2ks_native_subzero_body_probe_v4933.lua','mk2ks_native_subzero_shatter_probe_v4939.lua'),
 ('audit_v4935_subzero_','audit_v4941_subzero_'),('audit_v4936_subzero_','audit_v4942_subzero_'),
 ('prior=Path(__file__).with_name(\'run_earned_subzero_victims_v4871.py\')',
  'prior=Path(__file__).with_name(\'run_earned_subzero_victims_v4871.py\')'),
 ("ROOT/LUA,ROOT/\\'mk2ks_stock_fatality_v1021.lua\\',prior,Path(__file__).resolve(),Path(native.__file__).resolve()",
  "ROOT/LUA,ROOT/\\'mk2ks_stock_fatality_v1021.lua\\',ROOT/\\'mk2ks_native_subzero_body_probe_v4933.lua\\',prior,Path(__file__).with_name(\\'run_native_subzero_body_probe_v4934.py\\'),Path(__file__).resolve(),Path(native.__file__).resolve()"),
):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::physical_shatter_probe','exec'),globals())
