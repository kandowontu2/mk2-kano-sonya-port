"""Retain failed SonyaP1 pre-window stock-palette observation; exact successor.

Attract mode legitimately applies a stock Cage2 palette before physical
selection. Observe every valid19-roster palette primitive there, retaining the
unchanged strict8/17/18 actual FIFO/palette contract during the native scene.
No guest/game/controls/model/raster changes or source/build copies.
"""
from pathlib import Path
prior=Path(__file__).with_name('capture_current_subzero_scene_v6177.py')
source=prior.read_text()
before="r['actor']==r['owner']and int(r['id'])in(8,17,18)and r['slot']in('1','2')"
assert source.count(before)==1,'Only pre-window actual palette trace whitelist changes'
source=source.replace(before,"r['actor']==r['owner']and int(r['id'])in range(19)and r['slot']in('1','2')",1)
source=source.replace('audit_v6178_current_subzero_','audit_v6183_current_subzero_').replace('audit_v6179_current_subzero_','audit_v6184_current_subzero_')
before="OBSERVE_ADAPTER_UNUSED" # Pin the complete executed precursor explicitly.
anchor="    namespace=dict(prior.run.__globals__,current=current,__file__=__file__,sources=sources,palette_trace=palette_trace,native_palette=native_palette)"
assert source.count(anchor)==1,'Preserve whole renderer and bind precursor source'
source=source.replace(anchor,"    source=source.replace(\"OBSERVER,Path(__file__).resolve(),candidate/\",\"OBSERVER,Path(prior_adapter),Path(__file__).resolve(),candidate/\",1)\n"+anchor.replace('current=current,','current=current,prior_adapter=str(prior),'),1)
exec(compile(source,__file__+'::complete_native_pre_window_stock_palette','exec'),globals())
