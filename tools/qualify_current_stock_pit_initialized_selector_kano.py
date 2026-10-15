"""Actual KanoP2/SubZero8 earned Pit route; keep every selection-ID check."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_stock_pit_sonya_serial.py').read_text()
code=code.replace('audit_current_stock_pit_sonya_serial','audit_current_stock_pit_initialized_selector_kano_p2_subzero')
code=code.replace('audit_current_stock_pit_other_sides_preparation/sonya_p1_kitana.lua','audit_current_stock_pit_initialized_selector_preparation/kano_p2_subzero.lua')
code=code.replace("('17,18','18,4')","('17,18','17,8')")
code=code.replace("(\"r['winner']=='kano'\",\"r['winner']=='sonya'\")","(\"r['side']=='1'\",\"r['side']=='2'\")")
code=code.replace("action['id']=='18'","action['id']=='17'").replace("row['id']=='18'","row['id']=='17'").replace("row['victim_id']=='4'","row['victim_id']=='8'")
code=code.replace('performer=18,side=1,victim=4','performer=17,side=2,victim=8')
needle="proof=context['gate'](base.load(folder/'run.log'))"
assert code.count(needle)==1
code=code.replace(needle,"rows=base.load(folder/'run.log')\nassert rows['SELECT_ID'] and all(r['actual']==r['target'] for r in rows['SELECT_ID'])\nproof=context['gate'](rows)")
exec(compile(code,__file__,'exec'))
