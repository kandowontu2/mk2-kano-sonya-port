"""Same one-image capture/caps on KanoP2 stock SubZero victim route."""
from pathlib import Path
code=Path(__file__).with_name('prepare_current_stock_pit_sonya_impact.py').read_text()
for old,new in (('stock_pit_sonya_impact','stock_pit_kano_impact'),('sonya_p1_kitana','kano_p2_subzero'),('sonya_p1_stock_pit_260','kano_p2_stock_pit_260')):
    assert old in code;code=code.replace(old,new)
exec(compile(code,__file__,'exec'))
