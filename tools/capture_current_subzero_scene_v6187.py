"""Exact pre-window stock-palette successor; bind source paths explicitly.

Failed6182 stopped at a source-anchor assertion before any native process.
Preserve it and6177's actual failed SonyaP1. Keep every active-scene source,
integer renderer and target check; only allow genuine early stock palettes.
"""
from pathlib import Path
adapter_source=Path(__file__).with_name('capture_current_subzero_scene_v6177.py')
adapter_repair_source=Path(__file__).with_name('capture_current_subzero_scene_v6182.py')
source=adapter_source.read_text()
before="r['actor']==r['owner']and int(r['id'])in(8,17,18)and r['slot']in('1','2')"
assert source.count(before)==1,'Actual pre-window stock19palette observation'
source=source.replace(before,"r['actor']==r['owner']and int(r['id'])in range(19)and r['slot']in('1','2')",1)
source=source.replace('audit_v6178_current_subzero_','audit_v6183_current_subzero_').replace('audit_v6179_current_subzero_','audit_v6184_current_subzero_')
before=" namespace=dict(prior.run.__globals__,current=current,__file__=__file__,sources=sources,palette_trace=palette_trace,native_palette=native_palette)"
assert source.count(before)==1,'Exact complete one-space native replay scope'
after=" need(source.count(\"OBSERVER,Path(__file__).resolve(),candidate/\")==1,'Exact current native source pin anchor')\n source=source.replace(\"OBSERVER,Path(__file__).resolve(),candidate/\",\"OBSERVER,Path(adapter_source),Path(adapter_repair_source),Path(__file__).resolve(),candidate/\",1)\n"+before.replace('current=current,','current=current,adapter_source=adapter_source,adapter_repair_source=adapter_repair_source,')
source=source.replace(before,after,1)
exec(compile(source,__file__+'::complete_native_attract_palette_source_binding','exec'),globals())
