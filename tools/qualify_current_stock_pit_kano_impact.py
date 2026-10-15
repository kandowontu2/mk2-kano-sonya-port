"""Same neutral scene ledger and bounded image gate for Kano counterpart."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_stock_pit_sonya_impact.py').read_text()
for old,new in (('stock_pit_sonya_impact','stock_pit_kano_impact'),('sonya_p1_kitana','kano_p2_subzero')):
    assert old in code;code=code.replace(old,new)
exec(compile(code,__file__,'exec'))
