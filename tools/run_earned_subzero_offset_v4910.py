"""Actual earned offset regression only; does not accept own body or shatter."""
from pathlib import Path
prior=Path(__file__).with_name('run_earned_subzero_victims_v4871.py')
text=prior.read_text()
for before,after in (
 ('mk2ks_earned_subzero_victims_v4870.lua','mk2ks_earned_subzero_offset_v4909.lua'),
 ('audit_v4872_subzero_','audit_v4911_subzero_'),
 ('audit_v4873_subzero_','audit_v4912_subzero_'),
 ("MK2KS_STOCK_COMMAND='fdf_hp'","MK2KS_STOCK_COMMAND='ffd_hk'"),
 ('ROOT/LUA,ROOT/\'mk2ks_stock_fatality_v1021.lua\',Path(__file__).resolve()',
  'ROOT/LUA,ROOT/\'mk2ks_stock_fatality_v1021.lua\',prior,Path(__file__).resolve()'),
):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::native_dff_freeze','exec'),globals())
