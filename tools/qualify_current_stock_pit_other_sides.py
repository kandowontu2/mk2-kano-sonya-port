"""Reuse complete earned stage ledger with explicit native performer/victim IDs."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_stock_tomb_other_sides.py').read_text()
for old,new in (('qualify_current_native_tomb_case','qualify_current_native_pit_case'),('stock_tomb','stock_pit'),('passedFiniteStockTombRoles','passedFiniteStockPitRoles')):
    assert old in code;code=code.replace(old,new)
code=code.replace("proof=context['gate'](base.load(folder/'run.log'))","proof=context['gate'](base.load(folder/'run.log'))\n    assert proof['nativePitActivated'] and proof['completeSceneFollowthrough']")
exec(compile(code,__file__,'exec'))
