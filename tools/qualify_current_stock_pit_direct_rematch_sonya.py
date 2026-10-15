"""Keep whole Pit ledger and prove direct rematch reset admitted full health."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_stock_pit_sonya_serial.py').read_text()
code=code.replace('audit_current_stock_pit_sonya_serial','audit_current_stock_pit_direct_rematch_sonya_p1_kitana')
code=code.replace('audit_current_stock_pit_other_sides_preparation','audit_current_stock_pit_direct_rematch_preparation')
needle="proof=context['gate'](base.load(folder/'run.log'))"
assert code.count(needle)==1
code=code.replace(needle,"rows=base.load(folder/'run.log')\nproof=context['gate'](rows)\nassert rows.get('DIRECT_REMATCH')\nassert all(r['health']=='161,161' and r['ids']=='18,4' for r in rows['DIRECT_REMATCH'])")
exec(compile(code,__file__,'exec'))
