"""Whole earned scene gate plus every explicit character-selection result."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_stock_pit_sonya_serial.py').read_text()
code=code.replace('audit_current_stock_pit_sonya_serial','audit_current_stock_pit_initialized_selector_sonya_p1_kitana')
code=code.replace('audit_current_stock_pit_other_sides_preparation','audit_current_stock_pit_initialized_selector_preparation')
needle="proof=context['gate'](base.load(folder/'run.log'))"
assert code.count(needle)==1
code=code.replace(needle,"rows=base.load(folder/'run.log')\nassert rows['SELECT_ID'] and all(r['actual']==r['target'] for r in rows['SELECT_ID'])\nproof=context['gate'](rows)")
exec(compile(code,__file__,'exec'))
